#!/bin/bash
# check_cron_status.sh - 检查crontab状态

PROJECT_DIR="/Users/zhaochen/Desktop/2025/11/v2/howmanyq"
LOG_FILE="$PROJECT_DIR/cron.log"
SMART_LOG_FILE="$PROJECT_DIR/cron_smart.log"

echo "=== Crontab状态检查 - $(date) ==="
echo "当前时间: $(date)"
echo ""

echo "📋 当前crontab任务:"
crontab -l 2>/dev/null || echo "❌ 无法获取crontab列表，可能未配置"
echo ""

echo "🔄 Crontab服务状态:"
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl status cron --no-pager 2>/dev/null || echo "⚠️  cron服务状态检查失败"
else
    echo "ℹ️  使用launchd (macOS) 检查cron状态"
    sudo launchctl list | grep cron || echo "⚠️  cron服务可能未运行"
fi
echo ""

echo "📊 最近执行记录 (最后10条):"
if [ -f "$LOG_FILE" ]; then
    echo "=== 普通模式日志 ==="
    tail -10 "$LOG_FILE"
else
    echo "❌ 普通模式日志文件不存在"
fi

if [ -f "$SMART_LOG_FILE" ]; then
    echo ""
    echo "=== 智能模式日志 ==="
    tail -10 "$SMART_LOG_FILE"
else
    echo "❌ 智能模式日志文件不存在"
fi
echo ""

echo "📁 备份文件数量:"
BACKUP_COUNT=$(ls -la "$PROJECT_DIR"/navigation_data.json.backup.* 2>/dev/null | wc -l)
echo "备份文件数量: $BACKUP_COUNT"
if [ $BACKUP_COUNT -gt 0 ]; then
    echo "最新备份:"
    ls -la "$PROJECT_DIR"/navigation_data.json.backup.* | tail -3
fi
echo ""

echo "🗂️  当前导航数据统计:"
if [ -f "$PROJECT_DIR/navigation_data.json" ]; then
    TOOL_COUNT=$(grep -c '"id":' "$PROJECT_DIR/navigation_data.json" 2>/dev/null || echo "0")
    echo "当前工具数量: $TOOL_COUNT"
    echo "数据文件大小: $(du -h "$PROJECT_DIR/navigation_data.json" | cut -f1)"
    echo "最后修改时间: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$PROJECT_DIR/navigation_data.json" 2>/dev/null || stat -c "%y" "$PROJECT_DIR/navigation_data.json" 2>/dev/null)"
else
    echo "❌ navigation_data.json文件不存在"
fi
echo ""

echo "📈 建议:"
if ! crontab -l 2>/dev/null | grep -q navigation; then
    echo "❌ 未发现导航更新相关的crontab任务"
else
    echo "✅ crontab任务已配置"
fi

if [ ! -f "$LOG_FILE" ] && [ ! -f "$SMART_LOG_FILE" ]; then
    echo "❌ 未发现执行日志，脚本可能未运行"
else
    echo "✅ 检测到执行日志"
fi

echo "=== 检查完成 ==="

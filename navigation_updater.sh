#!/bin/bash
# navigation_updater.sh - 导航数据自动更新脚本

PROJECT_DIR="/Users/zhaochen/Desktop/2025/11/v2/howmanyq"
LOG_FILE="$PROJECT_DIR/cron.log"
PYTHON_SCRIPT="$PROJECT_DIR/navigation_generator.py"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 记录开始时间
echo "=== 导航更新任务开始: $(date) ===" >> "$LOG_FILE"

# 进入项目目录
cd "$PROJECT_DIR" || exit 1

# 备份当前数据
if [ -f "navigation_data.json" ]; then
    cp navigation_data.json "navigation_data.json.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 运行Python脚本
if /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1; then
    echo "✅ 导航数据更新成功: $(date)" >> "$LOG_FILE"
    
    # 检查是否有实际变更
    if git -C "$PROJECT_DIR" diff --quiet HEAD -- navigation_data.json; then
        echo "ℹ️  无数据变更" >> "$LOG_FILE"
    else
        echo "📊 数据已更新，准备提交" >> "$LOG_FILE"
        git -C "$PROJECT_DIR" add navigation_data.json
        git -C "$PROJECT_DIR" commit -m "🤖 Auto-update navigation data - $(date +'%Y-%m-%d %H:%M')" || echo "提交失败或无变更" >> "$LOG_FILE"
    fi
else
    echo "❌ 导航数据更新失败: $(date)" >> "$LOG_FILE"
    echo "错误信息已记录到日志文件" >> "$LOG_FILE"
fi

echo "=== 导航更新任务结束: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

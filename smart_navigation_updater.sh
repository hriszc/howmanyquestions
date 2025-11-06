#!/bin/bash
# smart_navigation_updater.sh - 智能导航更新脚本

PROJECT_DIR="/Users/zhaochen/Desktop/2025/11/v2/howmanyq"
LOG_FILE="$PROJECT_DIR/cron_smart.log"
PYTHON_SCRIPT="$PROJECT_DIR/navigation_generator.py"

cd "$PROJECT_DIR" || exit 1

# 记录开始时间
echo "=== 智能导航更新开始: $(date) ===" >> "$LOG_FILE"

# 检查是否有新的index.html文件
NEW_FILES=$(find . -name "index.html" -newermt "$(date -d '1 hour ago' '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -v-1H '+%Y-%m-%d %H:%M:%S')" 2>/dev/null | wc -l)

if [ "$NEW_FILES" -gt 0 ]; then
    echo "📁 检测到 $NEW_FILES 个新文件，开始更新" >> "$LOG_FILE"
    
    # 运行更新脚本
    if /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1; then
        echo "✅ 导航数据更新成功" >> "$LOG_FILE"
        
        # 提交变更
        if ! git diff --quiet HEAD -- navigation_data.json; then
            git add navigation_data.json
            git commit -m "🤖 Auto-update: 检测到新文件 - $(date +'%H:%M')" || true
        fi
    else
        echo "❌ 更新失败" >> "$LOG_FILE"
    fi
else
    echo "ℹ️  无新文件，跳过更新" >> "$LOG_FILE"
fi

echo "=== 智能导航更新结束: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

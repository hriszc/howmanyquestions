# 定时自动运行方案 (crontab)

## 🚀 方案优势
- **简单可靠**: 基于系统级定时任务，稳定运行
- **本地执行**: 在服务器本地运行，无网络依赖
- **灵活配置**: 可调整执行频率和时机
- **系统集成**: 与系统服务集成，重启后自动恢复

## 🛠️ 实施方案

### 1. 创建crontab配置文件

```bash
# 每小时运行一次导航生成器 (推荐)
0 * * * * cd /Users/zhaochen/Desktop/2025/11/v2/howmanyq && /usr/bin/python3 navigation_generator.py >> cron.log 2>&1

# 每30分钟运行一次 (更及时但可能过于频繁)
# */30 * * * * cd /Users/zhaochen/Desktop/2025/11/v2/howmanyq && /usr/bin/python3 navigation_generator.py >> cron.log 2>&1

# 每天凌晨2点运行一次 (节省资源但及时性较差)
# 0 2 * * * cd /Users/zhaochen/Desktop/2025/11/v2/howmanyq && /usr/bin/python3 navigation_generator.py >> cron.log 2>&1
```

### 2. 创建监控脚本

创建一个增强版的导航生成脚本，包含日志记录和错误处理：

```bash
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
```

### 3. 部署步骤

#### 步骤1: 安装crontab
```bash
# 检查crontab服务状态
sudo systemctl status cron

# 如果未安装，安装crontab
# Ubuntu/Debian:
sudo apt update && sudo apt install cron

# macOS:
sudo brew services start cron
```

#### 步骤2: 设置脚本权限
```bash
# 使脚本可执行
chmod +x /Users/zhaochen/Desktop/2025/11/v2/howmanyq/navigation_updater.sh

# 测试脚本运行
/Users/zhaochen/Desktop/2025/11/v2/howmanyq/navigation_updater.sh
```

#### 步骤3: 配置crontab
```bash
# 编辑当前用户的crontab
crontab -e

# 添加以下行 (每小时运行)
0 * * * * /Users/zhaochen/Desktop/2025/11/v2/howmanyq/navigation_updater.sh

# 或者每30分钟运行
# */30 * * * * /Users/zhaochen/Desktop/2025/11/v2/howmanyq/navigation_updater.sh
```

#### 步骤4: 验证配置
```bash
# 查看当前crontab任务
crontab -l

# 查看cron服务状态
sudo systemctl status cron

# 查看日志
tail -f /Users/zhaochen/Desktop/2025/11/v2/howmanyq/cron.log
```

### 4. 高级配置选项

#### 4.1 智能触发条件
只在新文件添加时才执行更新：

```bash
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
```

#### 4.2 邮件通知
```bash
# 在脚本末尾添加邮件通知
if [ $? -eq 0 ]; then
    echo "导航数据更新成功 - $(date)" | mail -s "HowManyQ Navigation Update" your-email@example.com
else
    echo "导航数据更新失败 - $(date)" | mail -s "HowManyQ Navigation Update Failed" your-email@example.com
fi
```

### 5. 监控和维护

#### 5.1 创建监控脚本
```bash
#!/bin/bash
# check_cron_status.sh - 检查crontab状态

PROJECT_DIR="/Users/zhaochen/Desktop/2025/11/v2/howmanyq"
LOG_FILE="$PROJECT_DIR/cron.log"

echo "=== Crontab状态检查 - $(date) ==="
echo "当前时间: $(date)"
echo ""

echo "📋 当前crontab任务:"
crontab -l
echo ""

echo "🔄 Crontab服务状态:"
sudo systemctl status cron --no-pager
echo ""

echo "📊 最近执行记录 (最后10条):"
if [ -f "$LOG_FILE" ]; then
    tail -10 "$LOG_FILE"
else
    echo "日志文件不存在"
fi
echo ""

echo "📁 备份文件数量:"
ls -la "$PROJECT_DIR"/navigation_data.json.backup.* 2>/dev/null | wc -l
```

#### 5.2 定期清理
```bash
# 添加到crontab，每周日清理旧日志
0 0 * * 0 find /Users/zhaochen/Desktop/2025/11/v2/howmanyq -name "*.log" -mtime +7 -delete

# 清理旧的备份文件，只保留最近30天
0 1 * * * find /Users/zhaochen/Desktop/2025/11/v2/howmanyq -name "navigation_data.json.backup.*" -mtime +30 -delete
```

### 6. 故障排除

#### 常见问题
1. **脚本权限问题**: 确保脚本有执行权限 `chmod +x`
2. **Python路径问题**: 使用完整路径 `/usr/bin/python3`
3. **工作目录问题**: 确保脚本在正确目录执行
4. **Git权限问题**: 配置Git用户信息

#### 调试方法
```bash
# 手动运行测试
/Users/zhaochen/Desktop/2025/11/v2/howmanyq/navigation_updater.sh

# 查看详细日志
cat /Users/zhaochen/Desktop/2025/11/v2/howmanyq/cron.log

# 检查cron服务
sudo journalctl -u cron -f
```

### 7. 性能优化

- **执行频率**: 根据实际需要调整，平衡及时性和资源消耗
- **文件监控**: 使用`inotify`实现实时监控（高级方案）
- **缓存优化**: 避免频繁的Git操作，使用本地缓存

---

*方案创建时间: 2025-11-06 21:05*  
*推荐配置: 每小时运行一次，智能检测变更*

#!/bin/bash
# work-progress 技能安装脚本

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="${WORKSPACE_PATH:-$HOME/.openclaw/workspace}"

echo "🔧 安装 work-progress 技能..."
echo "================================"

# 创建必要的目录
mkdir -p "$WORKSPACE/memory/daily"
mkdir -p "$WORKSPACE/memory/hourly"
touch "$WORKSPACE/memory/error.md"

# 设置脚本权限
chmod +x "$SKILL_DIR/scripts/check-progress.sh"
chmod +x "$SKILL_DIR/scripts/auto-recover.sh"

echo "✅ 目录结构已创建"

# 注册 cron 任务
echo ""
echo "📅 注册 cron 任务..."

# 1. 工作进度检查 (10 分钟) - 静默模式，仅异常时提醒
echo "  - 注册：工作进度检查（静默模式）"
openclaw cron add --name "工作进度检查" \
  --schedule '{"kind":"every","everyMs":600000}' \
  --payload '{"kind":"systemEvent","text":"⏰ 工作进度检查（静默模式）\\n\\n请检查：\\n1. 待办事项完成情况\\n2. 子代理会话状态\\n3. 系统日志中的 timeout 错误\\n4. 自动恢复超时任务\\n\\n---\\n\\n**重要**: 这是静默检查任务：\\n- ✅ 一切正常 → 回复 `NO_REPLY`（不输出任何内容）\\n- ⚠️ 检测到问题 → 输出详细报告提醒用户"}' \
  --session-target main \
  --delivery '{"mode":"none"}' 2>/dev/null

# 2. 子代理超时检测 (每小时)
echo "  - 注册：子代理超时检测"
openclaw cron add --name "子代理超时检测" \
  --schedule '{"kind":"every","everyMs":3600000}' \
  --payload '{"kind":"systemEvent","text":"🔄 子代理超时自动检测\\n\\n请检查是否有超时的子代理任务：\\n\\n1. 查看系统日志中的 timeout 错误\\n2. 检查 memory/error.md 中的超时记录\\n3. 如果有超时任务，自动记录并建议恢复\\n4. 检查子代理进程状态\\n\\n---\\n\\n**重要**: 这是自动检测任务，请在处理完成后：\\n- 如果一切正常 → 回复 `NO_REPLY`\\n- 如果检测到超时 → 记录到 memory/error.md 并提醒用户"}' \
  --session-target main \
  --delivery '{"mode":"none"}' 2>/dev/null

echo ""
echo "✅ 安装完成!"
echo ""
echo "📋 已注册的任务:"
echo "  - 工作进度检查：每 10 分钟"
echo "  - 子代理超时检测：每小时"
echo ""
echo "🔍 查看任务状态:"
echo "  openclaw cron list | grep -E '工作进度 | 子代理'"
echo ""
echo "📝 查看待办事项:"
echo "  cat $WORKSPACE/memory/daily/$(date +%Y-%m-%d).md"

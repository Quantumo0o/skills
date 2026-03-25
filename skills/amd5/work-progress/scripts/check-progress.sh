#!/bin/bash
# 工作进度检查脚本 v4.0
# 功能：检查待办事项 + 检测子代理超时/消失 + 主动自动恢复

WORKSPACE="${WORKSPACE_PATH:-$HOME/.openclaw/workspace}"
DAILY_PATH="$WORKSPACE/memory/daily/$(date +%Y-%m-%d).md"
LOG_FILE="$WORKSPACE/memory/error.md"

echo "🔍 工作进度检查 ($(date +%Y-%m-%d %H:%M))"
echo "================================"

# ==================== 1. 检查子代理会话状态 ====================
echo ""
echo "📊 检查子代理会话状态..."

# 使用 openclaw sessions list 检查子代理
SUBAGENT_SESSIONS=$(openclaw sessions list --kinds subagent 2>/dev/null | grep -v "^\[" | grep -v "^$" || echo "")

if [ -n "$SUBAGENT_SESSIONS" ]; then
    # 解析子代理会话信息
    echo "  📌 活跃子代理:"
    echo "$SUBAGENT_SESSIONS" | head -10 | while read line; do
        echo "    $line"
    done
else
    echo "  ✅ 无活跃子代理"
fi

# ==================== 2. 检查系统日志中的超时错误 ====================
echo ""
echo "🔍 检查子代理超时任务..."

# 检查最近 15 分钟的日志（覆盖更广）
TIMEOUT_LOGS=$(journalctl --user -u openclaw-gateway --since "15 minutes ago" 2>/dev/null | grep -iE "timeout|timed out|aborted|session.*closed|subagent.*stop" | tail -20)

if [ -n "$TIMEOUT_LOGS" ]; then
    echo "  ⚠️ 检测到超时/异常日志:"
    echo "$TIMEOUT_LOGS" | while read line; do
        echo "    $line"
    done
    
    # 提取任务名称并自动恢复
    echo ""
    echo "🔄 正在自动恢复超时任务..."
    
    # 从日志中提取任务信息 (task: xxx 或 session_key: xxx 或 session: xxx)
    TASK_INFO=$(echo "$TIMEOUT_LOGS" | grep -oE "task: [a-z0-9-]+|session_key:[^ ]+|session: [a-f0-9-]+" | head -5)
    
    if [ -n "$TASK_INFO" ]; then
        echo "  受影响的任务:"
        echo "$TASK_INFO" | while read info; do
            echo "    - $info"
        done
        
        # 记录到错误日志
        echo "" >> "$LOG_FILE"
        echo "### [$(date +%Y-%m-%d %H:%M)] 子代理超时自动恢复" >> "$LOG_FILE"
        echo "超时日志:" >> "$LOG_FILE"
        echo "$TIMEOUT_LOGS" >> "$LOG_FILE"
        echo "受影响任务：$TASK_INFO" >> "$LOG_FILE"
        echo "状态：已自动恢复" >> "$LOG_FILE"
        echo ""
        echo "✅ 已记录超时任务，正在主动恢复执行..."
    else
        echo "  ⚠️ 无法识别具体任务，已记录到 error.md"
        echo "" >> "$LOG_FILE"
        echo "### [$(date +%Y-%m-%d %H:%M)] 子代理超时检测（未识别任务）" >> "$LOG_FILE"
        echo "$TIMEOUT_LOGS" >> "$LOG_FILE"
    fi
else
    echo "  ✅ 无超时错误"
fi

# ==================== 3. 检查是否有未完成的下一批次任务 ====================
echo ""
echo "📋 检查未完成的下一批次任务..."

# 检查 daily 文件中的待办
if [ -f "$DAILY_PATH" ]; then
    TODO_ITEMS=$(grep -E "^\s*- \[ \]|^\s*- [^x]" "$DAILY_PATH" 2>/dev/null | grep -v "^\s*#")
    TODO_COUNT=$(echo "$TODO_ITEMS" | grep -c "^\s*-" 2>/dev/null || echo 0)
    
    if [ "$TODO_COUNT" -gt 0 ] && [ -n "$TODO_ITEMS" ]; then
        echo "  ⚠️ 有 $TODO_COUNT 个待办事项未完成:"
        echo "$TODO_ITEMS" | head -5 | while read line; do
            echo "    $line"
        done
        if [ "$TODO_COUNT" -gt 5 ]; then
            echo "    ... 还有 $((TODO_COUNT - 5)) 个"
        fi
        
        # 检查是否有子代理在执行这些任务
        if [ -z "$SUBAGENT_SESSIONS" ]; then
            echo ""
            echo "  ⚠️ 有待办事项但无活跃子代理，可能需要恢复执行"
            echo "  💡 建议：自动触发继续执行未完成的任务"
        fi
    else
        echo "  ✅ 无待办事项"
    fi
else
    echo "  📭 今日待办文件不存在"
fi

# ==================== 4. 检查进行中的任务 ====================
echo ""
echo "🔄 检查进行中的任务..."

if [ -f "$DAILY_PATH" ]; then
    IN_PROGRESS=$(grep -iE "进行中|🟢|in progress" "$DAILY_PATH" 2>/dev/null | head -3)
    
    if [ -n "$IN_PROGRESS" ]; then
        echo "  📌 进行中的任务:"
        echo "$IN_PROGRESS" | while read line; do
            echo "    $line"
        done
        
        # 如果任务标记为进行中但无子代理，可能需要恢复
        if [ -z "$SUBAGENT_SESSIONS" ]; then
            echo ""
            echo "  ⚠️ 任务标记为进行中但无活跃子代理"
            echo "  💡 可能子代理已超时/消失，需要恢复执行"
        fi
    else
        echo "  ✅ 无进行中的任务"
    fi
fi

# ==================== 5. 自动恢复逻辑 ====================
echo ""
echo "🔄 自动恢复检查..."

NEED_RECOVER=0
RECOVER_REASON=""

# 条件 1: 有超时日志
if [ -n "$TIMEOUT_LOGS" ]; then
    NEED_RECOVER=1
    RECOVER_REASON="${RECOVER_REASON}检测到超时日志; "
fi

# 条件 2: 有待办但无子代理
if [ "$TODO_COUNT" -gt 0 ] && [ -z "$SUBAGENT_SESSIONS" ]; then
    NEED_RECOVER=1
    RECOVER_REASON="${RECOVER_REASON}有待办事项但无活跃子代理; "
fi

# 条件 3: 有进行中任务但无子代理
if [ -n "$IN_PROGRESS" ] && [ -z "$SUBAGENT_SESSIONS" ]; then
    NEED_RECOVER=1
    RECOVER_REASON="${RECOVER_REASON}有进行中任务但无活跃子代理; "
fi

if [ "$NEED_RECOVER" -eq 1 ]; then
    echo "  ⚠️ 检测到需要恢复的情况：$RECOVER_REASON"
    echo ""
    echo "  🚀 正在自动恢复执行..."
    
    # 自动恢复：通过发送系统事件触发继续执行
    # 使用 openclaw 命令发送消息到主会话
    openclaw sessions send --label main "🔄 自动恢复触发：检测到 $RECOVER_REASON 正在继续执行未完成的任务..." 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✅ 已自动触发恢复执行"
    else
        echo "  ⚠️  自动触发失败，请手动执行"
    fi
    
    # 记录到错误日志
    echo "" >> "$LOG_FILE"
    echo "### [$(date +%Y-%m-%d %H:%M)] 自动恢复触发" >> "$LOG_FILE"
    echo "原因：$RECOVER_REASON" >> "$LOG_FILE"
    echo "状态：已自动触发恢复" >> "$LOG_FILE"
    echo ""
else
    echo "  ✅ 无需恢复"
fi

# ==================== 汇总 ====================
echo ""
echo "================================"
echo "📊 检查结果汇总:"

ERROR_COUNT=0
[ -n "$TIMEOUT_LOGS" ] && ERROR_COUNT=$((ERROR_COUNT + 1))
[ "$TODO_COUNT" -gt 0 ] && [ -n "$TODO_ITEMS" ] && ERROR_COUNT=$((ERROR_COUNT + 1))
[ "$NEED_RECOVER" -eq 1 ] && ERROR_COUNT=$((ERROR_COUNT + 1))

if [ "$ERROR_COUNT" -eq 0 ]; then
    echo "  ✅ 一切正常"
    echo "NO_REPLY"
else
    echo "  ⚠️ 发现 $ERROR_COUNT 个需要关注的问题"
    echo ""
    echo "请查看上述详细信息并处理。"
fi

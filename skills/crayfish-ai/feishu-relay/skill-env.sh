#!/bin/bash
# Skill 环境变量
# 所有 skill 自动加载此文件

# Feishu Relay 路径
FEISHU_NOTIFIER_DIR="/opt/feishu-notifier"

# 通知函数 - 直接发送
notify() {
    if [ -x "$FEISHU_NOTIFIER_DIR/bin/notify" ]; then
        "$FEISHU_NOTIFIER_DIR/bin/notify" "$@"
    else
        echo "[NOTIFY] $*"
    fi
}

# 定时通知函数
notify_later() {
    local minutes="$1"
    shift
    if [ -x "$FEISHU_NOTIFIER_DIR/bin/feishu-task-v2" ]; then
        "$FEISHU_NOTIFIER_DIR/bin/feishu-task-v2" in "$minutes" "$@"
    else
        echo "[NOTIFY LATER $minutes min] $*"
    fi
}

# Skill 通知 - 带 skill 名称前缀
skill_notify() {
    local skill_name="${SKILL_NAME:-UnknownSkill}"
    notify "[$skill_name] $1" "${2:-}"
}

export -f notify
export -f notify_later
export -f skill_notify
export FEISHU_NOTIFIER_DIR

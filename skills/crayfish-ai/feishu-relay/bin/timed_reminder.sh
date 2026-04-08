#!/bin/bash
#
# Feishu Task Notifier v1.0
# 定时提醒脚本
#
# 功能：创建和管理定时提醒任务，集成 crontab
# 作者：Feishu Task Notifier Project
# 许可证：MIT

set -e

# ==================== 配置区域 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEISHU_NOTIFY_SCRIPT="${SCRIPT_DIR}/feishu_notify.sh"
CRON_TAG="# feishu-task-notifier"

# ==================== 函数定义 ====================

show_help() {
    cat << EOF
Feishu Task Notifier - 定时提醒管理

用法: $0 <命令> [选项]

命令:
    add     添加新的定时提醒
    list    列出所有定时提醒
    remove  删除定时提醒
    test    测试发送提醒

add 命令选项:
    -t, --title TITLE       提醒标题（默认：定时提醒）
    -m, --message MSG       提醒内容（必需）
    -s, --schedule CRON     Cron 表达式（必需，如 "0 9 * * *" 表示每天9点）
    -n, --name NAME         任务名称标识

remove 命令选项:
    -n, --name NAME         按名称删除任务
    -i, --id ID             按 cron 行号删除

示例:
    # 添加每天9点的早安提醒
    $0 add -n "morning-greeting" -t "早安" -m "新的一天开始了！" -s "0 9 * * *"
    
    # 添加每周一9点的周报提醒
    $0 add -n "weekly-report" -t "周报提醒" -m "记得提交本周周报" -s "0 9 * * 1"
    
    # 列出所有提醒
    $0 list
    
    # 删除指定名称的提醒
    $0 remove -n "morning-greeting"

Cron 表达式格式:
    分 时 日 月 周
    
    常用示例:
    0 9 * * *      每天上午9点
    0 9 * * 1      每周一上午9点
    0 9 1 * *      每月1日上午9点
    */30 * * * *   每30分钟
    0 9-18 * * 1-5 工作日9点到18点每小时

EOF
}

# 验证 cron 表达式格式
validate_cron() {
    local cron="$1"
    local fields
    fields=$(echo "$cron" | awk '{print NF}')
    
    if [ "$fields" -ne 5 ]; then
        echo "错误：Cron 表达式需要5个字段（分 时 日 月 周）" >&2
        return 1
    fi
    return 0
}

# 添加定时提醒
add_reminder() {
    local name=""
    local title="定时提醒"
    local message=""
    local schedule=""
    
    # 解析参数
    shift
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                name="$2"
                shift 2
                ;;
            -t|--title)
                title="$2"
                shift 2
                ;;
            -m|--message)
                message="$2"
                shift 2
                ;;
            -s|--schedule)
                schedule="$2"
                shift 2
                ;;
            *)
                echo "未知选项: $1" >&2
                return 1
                ;;
        esac
    done
    
    # 验证必需参数
    if [ -z "$name" ]; then
        echo "错误：请指定任务名称（-n）" >&2
        return 1
    fi
    
    if [ -z "$message" ]; then
        echo "错误：请指定提醒内容（-m）" >&2
        return 1
    fi
    
    if [ -z "$schedule" ]; then
        echo "错误：请指定 Cron 表达式（-s）" >&2
        return 1
    fi
    
    validate_cron "$schedule" || return 1
    
    # 检查名称是否已存在
    if crontab -l 2>/dev/null | grep -q "${CRON_TAG} name=${name}"; then
        echo "错误：任务名称 '${name}' 已存在" >&2
        return 1
    fi
    
    # 转义特殊字符
    title=$(echo "$title" | sed 's/"/\\"/g')
    message=$(echo "$message" | sed 's/"/\\"/g')
    
    # 构建 cron 任务
    local cron_job
    cron_job="${schedule} ${FEISHU_NOTIFY_SCRIPT} -t \"${title}\" -m \"${message}\" ${CRON_TAG} name=${name}"
    
    # 添加到 crontab
    (crontab -l 2>/dev/null; echo "$cron_job") | crontab -
    
    echo "✓ 定时提醒已添加"
    echo "  名称: ${name}"
    echo "  计划: ${schedule}"
    echo "  标题: ${title}"
    echo "  内容: ${message}"
}

# 列出所有定时提醒
list_reminders() {
    echo "当前定时提醒任务:"
    echo "=================="
    
    local crontab_content
    crontab_content=$(crontab -l 2>/dev/null || true)
    
    if ! echo "$crontab_content" | grep -q "$CRON_TAG"; then
        echo "暂无定时提醒任务"
        return 0
    fi
    
    echo "$crontab_content" | grep -n "$CRON_TAG" | while read -r line; do
        local line_num
        line_num=$(echo "$line" | cut -d':' -f1)
        local job
        job=$(echo "$line" | cut -d':' -f2-)
        
        local name
        name=$(echo "$job" | grep -o "name=[^ ]*" | cut -d'=' -f2)
        local schedule
        schedule=$(echo "$job" | awk '{print $1,$2,$3,$4,$5}')
        local title
        title=$(echo "$job" | grep -o '\-t "[^"]*"' | cut -d'"' -f2)
        
        echo ""
        echo "[${line_num}] ${name}"
        echo "    计划: ${schedule}"
        echo "    标题: ${title}"
    done
}

# 删除定时提醒
remove_reminder() {
    local name=""
    local id=""
    
    # 解析参数
    shift
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                name="$2"
                shift 2
                ;;
            -i|--id)
                id="$2"
                shift 2
                ;;
            *)
                echo "未知选项: $1" >&2
                return 1
                ;;
        esac
    done
    
    if [ -z "$name" ] && [ -z "$id" ]; then
        echo "错误：请指定任务名称（-n）或行号（-i）" >&2
        return 1
    fi
    
    local crontab_content
    crontab_content=$(crontab -l 2>/dev/null || true)
    
    if [ -n "$name" ]; then
        # 按名称删除
        if ! echo "$crontab_content" | grep -q "${CRON_TAG} name=${name}"; then
            echo "错误：找不到名称为 '${name}' 的任务" >&2
            return 1
        fi
        
        echo "$crontab_content" | grep -v "${CRON_TAG} name=${name}" | crontab -
        echo "✓ 任务 '${name}' 已删除"
    elif [ -n "$id" ]; then
        # 按行号删除
        if ! echo "$crontab_content" | sed -n "${id}p" | grep -q "$CRON_TAG"; then
            echo "错误：行号 ${id} 不是 Feishu Task Notifier 任务" >&2
            return 1
        fi
        
        echo "$crontab_content" | sed "${id}d" | crontab -
        echo "✓ 第 ${id} 行任务已删除"
    fi
}

# 测试提醒
test_reminder() {
    echo "正在测试提醒功能..."
    "$FEISHU_NOTIFY_SCRIPT" --test
}

# ==================== 主程序 ====================

main() {
    # 检查 notify 脚本是否存在
    if [ ! -f "$FEISHU_NOTIFY_SCRIPT" ]; then
        echo "错误：找不到通知脚本 ${FEISHU_NOTIFY_SCRIPT}" >&2
        exit 1
    fi
    
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    case "$1" in
        add)
            add_reminder "$@"
            ;;
        list)
            list_reminders
            ;;
        remove|delete|del)
            remove_reminder "$@"
            ;;
        test)
            test_reminder
            ;;
        -h|--help|help)
            show_help
            ;;
        *)
            echo "未知命令: $1" >&2
            show_help
            exit 1
            ;;
    esac
}

main "$@"

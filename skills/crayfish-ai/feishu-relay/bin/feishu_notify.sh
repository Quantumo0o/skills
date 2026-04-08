#!/bin/bash
#
# Feishu Task Notifier v1.0
# 飞书任务通知脚本 - 核心功能
#
# 功能：通过飞书 Open API 发送即时通知消息
# 作者：Feishu Task Notifier Project
# 许可证：MIT

set -e

# ==================== 配置区域 ====================
# 加载配置文件（如果存在）
CONFIG_FILE="${FEISHU_CONFIG_FILE:-/opt/feishu-notifier/config/feishu.env}"
if [[ -f "$CONFIG_FILE" ]]; then
    set -a
    source "$CONFIG_FILE"
    set +a
fi

# 请在此处填写你的飞书应用配置
FEISHU_APP_ID="${FEISHU_APP_ID:-your_app_id}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-your_app_secret}"
FEISHU_USER_ID="${FEISHU_USER_ID:-your_user_id}"
FEISHU_RECEIVE_ID_TYPE="${FEISHU_RECEIVE_ID_TYPE:-open_id}"

# 飞书 API 端点
FEISHU_API_BASE="https://open.feishu.cn/open-apis"
TOKEN_ENDPOINT="${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
MESSAGE_ENDPOINT="${FEISHU_API_BASE}/im/v1/messages"

# ==================== 函数定义 ====================

# 打印帮助信息
show_help() {
    cat << EOF
Feishu Task Notifier - 飞书通知脚本

用法: $0 [选项] [消息内容]

选项:
    -h, --help          显示帮助信息
    -t, --title TITLE   设置消息标题
    -m, --message MSG   设置消息内容（也可通过管道传入）
    -u, --user USER_ID  指定接收用户ID（覆盖环境变量）
    --test              发送测试消息

环境变量:
    FEISHU_APP_ID       飞书应用 ID
    FEISHU_APP_SECRET   飞书应用密钥
    FEISHU_USER_ID      默认接收用户ID

示例:
    $0 -t "任务完成" -m "备份任务已成功执行"
    echo "系统警告" | $0 -t "磁盘空间不足"
    $0 --test

EOF
}

# 获取访问令牌
get_access_token() {
    local response
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}" \
        "${TOKEN_ENDPOINT}")
    
    local code
    code=$(echo "$response" | grep -o '"code":[0-9]*' | cut -d':' -f2)
    
    if [ "$code" != "0" ]; then
        echo "错误：获取访问令牌失败" >&2
        echo "响应: $response" >&2
        return 1
    fi
    
    echo "$response" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4
}

# 发送消息
send_message() {
    local token="$1"
    local title="$2"
    local content="$3"
    local user_id="${4:-$FEISHU_USER_ID}"
    
    # 构建消息（使用 text 类型，更可靠）
    local message_json
    message_json=$(printf '{"text":"**%s**\\n\\n%s\\n\\n_发送时间: %s_"}' "$title" "$content" "$(date '+%Y-%m-%d %H:%M:%S')")
    
    local message_card
    message_card=$(printf '{"receive_id":"%s","msg_type":"text","content":%s}' "$user_id" "$(echo "$message_json" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
    
    local response
    response=$(curl -s -X POST \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -d "$message_card" \
        "${MESSAGE_ENDPOINT}?receive_id_type=${FEISHU_RECEIVE_ID_TYPE}")
    
    local code
    code=$(echo "$response" | grep -o '"code":[0-9]*' | cut -d':' -f2)
    
    if [ "$code" != "0" ]; then
        echo "错误：发送消息失败" >&2
        echo "响应: $response" >&2
        return 1
    fi
    
    echo "✓ 消息发送成功"
    return 0
}

# 发送测试消息
send_test_message() {
    local hostname
    hostname=$(hostname)
    local title="🧪 Feishu Task Notifier 测试消息"
    local content="**服务器**: ${hostname}  
**状态**: 配置正确，可以正常发送通知  
**时间**: $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "正在发送测试消息到用户 ${FEISHU_USER_ID}..."
    
    local token
    token=$(get_access_token) || return 1
    send_message "$token" "$title" "$content"
}

# ==================== 主程序 ====================

main() {
    local title="系统通知"
    local message=""
    local user_id=""
    local test_mode=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--title)
                title="$2"
                shift 2
                ;;
            -m|--message)
                message="$2"
                shift 2
                ;;
            -u|--user)
                user_id="$2"
                shift 2
                ;;
            --test)
                test_mode=true
                shift
                ;;
            *)
                # 如果 message 为空，将剩余参数作为消息内容
                if [ -z "$message" ]; then
                    message="$1"
                else
                    message="${message} $1"
                fi
                shift
                ;;
        esac
    done
    
    # 检查必要的环境变量
    if [ "$FEISHU_APP_ID" = "your_app_id" ] || [ -z "$FEISHU_APP_ID" ]; then
        echo "错误：请设置 FEISHU_APP_ID 环境变量" >&2
        exit 1
    fi
    
    if [ "$FEISHU_APP_SECRET" = "your_app_secret" ] || [ -z "$FEISHU_APP_SECRET" ]; then
        echo "错误：请设置 FEISHU_APP_SECRET 环境变量" >&2
        exit 1
    fi
    
    if [ "$FEISHU_USER_ID" = "your_user_id" ] && [ -z "$user_id" ]; then
        echo "错误：请设置 FEISHU_USER_ID 环境变量或使用 -u 指定用户" >&2
        exit 1
    fi
    
    # 测试模式
    if [ "$test_mode" = true ]; then
        send_test_message
        exit $?
    fi
    
    # 从管道读取消息内容
    if [ -z "$message" ] && [ ! -t 0 ]; then
        message=$(cat)
    fi
    
    # 检查消息内容，为空则使用默认值
    if [ -z "$message" ]; then
        message="(无内容)"
    fi
    
    # 使用 Python 正确处理 JSON 转义
    message=$(printf '%s' "$message" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')
    
    # 获取访问令牌并发送消息
    echo "正在发送通知..."
    local token
    token=$(get_access_token) || exit 1
    send_message "$token" "$title" "$message" "$user_id"
}

main "$@"

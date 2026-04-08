#!/bin/bash
#
# Feishu Task Notifier v1.0
# 磁盘监控示例脚本
#
# 功能：监控磁盘使用情况，当使用率超过阈值时发送飞书通知
# 作者：Feishu Task Notifier Project
# 许可证：MIT

set -e

# ==================== 配置区域 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEISHU_NOTIFY_SCRIPT="${SCRIPT_DIR}/feishu_notify.sh"

# 默认配置
DEFAULT_THRESHOLD=80          # 磁盘使用率阈值（百分比）
DEFAULT_CHECK_INTERVAL=300    # 检查间隔（秒）

# 可以通过环境变量覆盖配置
DISK_THRESHOLD="${DISK_THRESHOLD:-$DEFAULT_THRESHOLD}"
CHECK_INTERVAL="${CHECK_INTERVAL:-$DEFAULT_CHECK_INTERVAL}"

# ==================== 函数定义 ====================

show_help() {
    cat << EOF
Feishu Task Notifier - 磁盘监控脚本

用法: $0 [选项]

选项:
    -h, --help              显示帮助信息
    -t, --threshold PERCENT 设置警告阈值（默认：80%）
    -i, --interval SECONDS  设置检查间隔（默认：300秒）
    -d, --daemon            后台守护模式运行
    -c, --check             单次检查模式（默认）
    -e, --exclude FS        排除指定文件系统（可多次使用）

环境变量:
    DISK_THRESHOLD          磁盘使用率阈值
    CHECK_INTERVAL          检查间隔（秒）
    FEISHU_APP_ID           飞书应用 ID
    FEISHU_APP_SECRET       飞书应用密钥
    FEISHU_USER_ID          接收通知的用户 ID

示例:
    # 单次检查当前磁盘状态
    $0
    
    # 设置阈值为90%，每60秒检查一次
    $0 -t 90 -i 60 -d
    
    # 排除 tmpfs 和 devtmpfs
    $0 -e tmpfs -e devtmpfs -d

Crontab 集成示例:
    # 每5分钟检查一次磁盘
    */5 * * * * /path/to/disk_monitor.sh -c

EOF
}

# 获取磁盘使用情况
check_disk_usage() {
    local exclude_pattern=""
    
    # 构建排除模式
    for fs in "$@"; do
        if [ -z "$exclude_pattern" ]; then
            exclude_pattern="^${fs}$"
        else
            exclude_pattern="${exclude_pattern}|^${fs}$"
        fi
    done
    
    if [ -n "$exclude_pattern" ]; then
        df -h | tail -n +2 | grep -vE "$exclude_pattern" | awk '{print $1,$2,$3,$4,$5,$6}'
    else
        df -h | tail -n +2 | awk '{print $1,$2,$3,$4,$5,$6}'
    fi
}

# 检查是否超过阈值
is_over_threshold() {
    local usage="$1"
    local threshold="$2"
    
    # 移除百分号
    usage="${usage%\%}"
    
    if [ "$usage" -ge "$threshold" ]; then
        return 0
    else
        return 1
    fi
}

# 发送警告通知
send_alert() {
    local filesystem="$1"
    local size="$2"
    local used="$3"
    local available="$4"
    local usage="$5"
    local mount="$6"
    
    local title="⚠️ 磁盘空间警告"
    local content="**文件系统**: ${filesystem}  
**挂载点**: ${mount}  
**总容量**: ${size}  
**已使用**: ${used} (${usage})  
**可用**: ${available}  
**阈值**: ${DISK_THRESHOLD}%  

请及时清理磁盘空间！"
    
    "$FEISHU_NOTIFY_SCRIPT" -t "$title" -m "$content"
}

# 单次检查
single_check() {
    local exclude_list=("$@")
    local alert_sent=false
    
    echo "[$$(date '+%Y-%m-%d %H:%M:%S')] 检查磁盘使用情况..."
    
    while read -r filesystem size used available usage mount; do
        # 移除 usage 中的百分号进行比较
        local usage_num="${usage%\%}"
        
        echo "  ${mount}: ${usage} (${used}/${size})"
        
        if [ "$usage_num" -ge "$DISK_THRESHOLD" ]; then
            echo "    ⚠️ 超过阈值 ${DISK_THRESHOLD}%"
            send_alert "$filesystem" "$size" "$used" "$available" "$usage" "$mount"
            alert_sent=true
        fi
    done < <(check_disk_usage "${exclude_list[@]}")
    
    if [ "$alert_sent" = false ]; then
        echo "[$$(date '+%Y-%m-%d %H:%M:%S')] 所有磁盘正常"
    fi
}

# 守护模式
daemon_mode() {
    local exclude_list=("$@")
    
    echo "启动磁盘监控守护进程..."
    echo "阈值: ${DISK_THRESHOLD}%"
    echo "检查间隔: ${CHECK_INTERVAL}秒"
    echo "排除文件系统: ${exclude_list[*]:-无}"
    echo "按 Ctrl+C 停止"
    
    while true; do
        single_check "${exclude_list[@]}"
        echo ""
        sleep "$CHECK_INTERVAL"
    done
}

# ==================== 主程序 ====================

main() {
    local mode="check"
    local exclude_list=()
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--threshold)
                DISK_THRESHOLD="$2"
                shift 2
                ;;
            -i|--interval)
                CHECK_INTERVAL="$2"
                shift 2
                ;;
            -d|--daemon)
                mode="daemon"
                shift
                ;;
            -c|--check)
                mode="check"
                shift
                ;;
            -e|--exclude)
                exclude_list+=("$2")
                shift 2
                ;;
            *)
                echo "未知选项: $1" >&2
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查 notify 脚本
    if [ ! -f "$FEISHU_NOTIFY_SCRIPT" ]; then
        echo "错误：找不到通知脚本 ${FEISHU_NOTIFY_SCRIPT}" >&2
        exit 1
    fi
    
    # 验证阈值
    if ! [[ "$DISK_THRESHOLD" =~ ^[0-9]+$ ]] || [ "$DISK_THRESHOLD" -lt 1 ] || [ "$DISK_THRESHOLD" -gt 100 ]; then
        echo "错误：阈值必须是 1-100 之间的整数" >&2
        exit 1
    fi
    
    # 执行对应模式
    case "$mode" in
        check)
            single_check "${exclude_list[@]}"
            ;;
        daemon)
            daemon_mode "${exclude_list[@]}"
            ;;
    esac
}

main "$@"

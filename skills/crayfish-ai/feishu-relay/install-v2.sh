#!/bin/bash
#
# feishu-relay-setup - 一键安装和配置 Feishu Relay 自动发现系统
# 用法: sudo ./feishu-relay-setup.sh
#

set -e

INSTALL_DIR="/opt/feishu-notifier"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_banner() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           Feishu Relay - 自动发现系统安装程序                  ║
║                                                               ║
║   完全自动化的通知中心 - 新系统部署即自动注册                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo ""
}

# 检查 root 权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

# 安装依赖
install_dependencies() {
    log_info "检查依赖..."
    
    local deps=("python3" "sqlite3" "curl" "jq")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_info "安装缺失的依赖: ${missing[*]}"
        apt-get update &> /dev/null
        apt-get install -y "${missing[@]}" &> /dev/null
        log_success "依赖安装完成"
    else
        log_success "所有依赖已满足"
    fi
}

# 创建目录结构
create_directories() {
    log_info "创建目录结构..."
    
    mkdir -p "$INSTALL_DIR"/{bin,lib,queue,config,registry,logs,tasks,examples}
    
    log_success "目录结构创建完成"
}

# 安装核心文件
install_core_files() {
    log_info "安装核心文件..."
    
    # 复制可执行文件
    cp "$REPO_DIR/bin/"*.sh "$INSTALL_DIR/bin/" 2>/dev/null || true
    cp "$REPO_DIR/bin/notify" "$INSTALL_DIR/bin/" 2>/dev/null || true
    cp "$REPO_DIR/bin/feishu-relay-register" "$INSTALL_DIR/bin/" 2>/dev/null || true
    
    # 复制 Python 脚本
    cp "$REPO_DIR/lib/"*.py "$INSTALL_DIR/lib/" 2>/dev/null || true
    
    # 设置权限
    chmod +x "$INSTALL_DIR/bin/"* 2>/dev/null || true
    chmod +x "$INSTALL_DIR/lib/"*.py 2>/dev/null || true
    
    log_success "核心文件安装完成"
}

# 创建软链接
create_symlinks() {
    log_info "创建命令软链接..."
    
    ln -sf "$INSTALL_DIR/bin/notify" /usr/local/bin/notify 2>/dev/null || true
    ln -sf "$INSTALL_DIR/bin/feishu-relay-register" /usr/local/bin/feishu-relay-register 2>/dev/null || true
    
    log_success "软链接创建完成"
}

# 初始化数据库
init_database() {
    log_info "初始化队列数据库..."
    
    sqlite3 "$INSTALL_DIR/queue/notify-queue.db" << 'EOF'
CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execute_at TIMESTAMP,
    retry INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_execute_at ON queue(execute_at);
EOF
    
    log_success "数据库初始化完成"
}

# 安装 systemd 服务
install_systemd_services() {
    log_info "安装 systemd 服务..."
    
    # 主服务
    cat > /etc/systemd/system/feishu-relay.service <> 'EOF'
[Unit]
Description=Feishu Relay - Unified Notification Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/feishu-notifier/lib/feishu-relay.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # 自动发现服务
    cat > /etc/systemd/system/feishu-relay-discovery.service <> 'EOF'
[Unit]
Description=Feishu Relay Auto Discovery - Automatic System Registration
After=network.target feishu-relay.service
Wants=feishu-relay.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/feishu-notifier/lib/feishu-relay-auto-discovery.py
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable feishu-relay.service
    systemctl enable feishu-relay-discovery.service
    
    log_success "systemd 服务安装完成"
}

# 配置飞书参数
configure_feishu() {
    log_info "配置飞书参数..."
    
    local config_file="$INSTALL_DIR/config/feishu.env"
    
    if [ -f "$config_file" ]; then
        log_warn "配置文件已存在，跳过配置"
        return
    fi
    
    echo ""
    echo "请输入飞书应用配置信息:"
    echo "(获取方式: https://open.feishu.cn/app)"
    echo ""
    
    read -p "App ID: " app_id
    read -p "App Secret: " app_secret
    read -p "User ID (默认: ou_5ee6a655f26327aefe51db158f4860a4): " user_id
    user_id=${user_id:-"ou_5ee6a655f26327aefe51db158f4860a4"}
    
    cat > "$config_file" <> EOF
FEISHU_APP_ID=$app_id
FEISHU_APP_SECRET=$app_secret
FEISHU_USER_ID=$user_id
FEISHU_RECEIVE_ID_TYPE=open_id
EOF
    
    chmod 600 "$config_file"
    
    log_success "飞书配置完成"
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    systemctl start feishu-relay.service
    sleep 2
    systemctl start feishu-relay-discovery.service
    
    log_success "服务已启动"
}

# 显示状态
show_status() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "                    安装完成状态                               "
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    # 服务状态
    echo "服务状态:"
    systemctl is-active feishu-relay.service &>/dev/null && \
        log_success "feishu-relay: 运行中" || log_error "feishu-relay: 未运行"
    
    systemctl is-active feishu-relay-discovery.service &>/dev/null && \
        log_success "feishu-relay-discovery: 运行中" || log_error "feishu-relay-discovery: 未运行"
    
    echo ""
    echo "可用命令:"
    echo "  notify \"标题\" \"内容\"          - 发送即时通知"
    echo "  feishu-relay-register list      - 查看已注册系统"
    echo "  feishu-relay-register status    - 查看系统状态"
    echo "  feishu-relay-register scan      - 手动触发扫描"
    echo ""
    echo "自动发现路径:"
    echo "  /opt, /var/www, /data, /home"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

# 创建示例任务
create_example_tasks() {
    log_info "创建示例监控任务..."
    
    # 磁盘监控
    cat > "$INSTALL_DIR/tasks/disk-monitor.sh" <> 'EOF'
#!/bin/bash
# 磁盘空间监控

THRESHOLD=80
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    /opt/feishu-notifier/bin/notify "⚠️ 磁盘告警" "使用率 ${USAGE}%，请及时清理"
fi
EOF
    chmod +x "$INSTALL_DIR/tasks/disk-monitor.sh"
    
    # 添加到 crontab
    (crontab -l 2>/dev/null || echo "") | grep -v "disk-monitor" > /tmp/crontab.tmp
    echo "0 */6 * * * $INSTALL_DIR/tasks/disk-monitor.sh" >> /tmp/crontab.tmp
    crontab /tmp/crontab.tmp
    rm /tmp/crontab.tmp
    
    log_success "示例任务创建完成"
}

# 主函数
main() {
    print_banner
    check_root
    install_dependencies
    create_directories
    install_core_files
    create_symlinks
    init_database
    install_systemd_services
    
    # 询问是否配置飞书
    echo ""
    read -p "是否现在配置飞书参数? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        configure_feishu
    fi
    
    start_services
    create_example_tasks
    show_status
    
    echo ""
    log_success "Feishu Relay 自动发现系统安装完成!"
    echo ""
    echo "新系统部署到 /opt, /var/www, /data 等目录时将自动被发现并注册。"
    echo ""
}

main "$@"

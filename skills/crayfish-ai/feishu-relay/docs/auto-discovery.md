# Feishu Relay 自动发现系统

完全自动化的通知中心 —— 新系统部署即自动被发现并注册。

## 核心特性

✅ **零配置自动发现** - 新系统部署到监控目录后自动注册  
✅ **智能类型识别** - 自动识别 website/service/skill/task 等类型  
✅ **框架检测** - 自动检测 Next.js/Django/Flask/Node 等框架  
✅ **统一通知入口** - 所有系统通过 `notify` 命令发送通知  
✅ **自动清理** - 系统删除后自动从注册表移除  

## 快速开始

### 安装

```bash
sudo /opt/feishu-notifier/install-v2.sh
```

### 验证安装

```bash
# 查看服务状态
systemctl status feishu-relay-discovery

# 查看已注册系统
feishu-relay-register list

# 发送测试通知
notify "测试" "系统安装成功"
```

## 自动发现机制

### 监控路径

以下目录的新系统会自动被发现：

| 路径 | 系统类型 |
|------|---------|
| `/opt/*` | service |
| `/var/www/*` | website |
| `/data/*` | data |
| `/home/*` | user |

### 识别规则

系统被识别需要满足以下条件之一：

- 包含 `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod` 等项目文件
- 包含 `src/`, `bin/`, `dist/`, `build/` 目录
- 包含 `index.html`, `index.php`, `app.py` 等入口文件
- 包含 `.git`, `README.md` 等项目标识

### 自动识别示例

```bash
# 部署新网站 → 自动识别为 website
mkdir -p /var/www/myapp
cd /var/www/myapp
git clone https://github.com/user/myapp.git .
# 5分钟内自动注册，发送飞书通知

# 部署新服务 → 自动识别为 service  
mkdir -p /opt/myapi
cd /opt/myapi
# 创建 main.py, requirements.txt
# 自动检测为 Python 服务并注册
```

## 命令行工具

### notify - 发送通知

```bash
# 即时通知
notify "标题" "消息内容"

# 在脚本中使用
#!/bin/bash
if ! deploy_app; then
    notify "❌ 部署失败" "myapp 部署出错，请检查日志"
    exit 1
fi
notify "✅ 部署成功" "myapp 已成功部署到生产环境"
```

### feishu-relay-register - 系统管理

```bash
# 查看所有已注册系统
feishu-relay-register list

# 查看系统状态
feishu-relay-register status

# 查看特定系统详情
feishu-relay-register status myapp

# 手动注册系统
feishu-relay-register register myapp website /var/www/myapp

# 手动注销系统
feishu-relay-register unregister myapp

# 发送测试通知
feishu-relay-register notify myapp "测试消息"

# 手动触发扫描
feishu-relay-register scan
```

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      文件系统监控层                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ /opt/*      │  │ /var/www/*  │  │ /data/*             │  │
│  │ 服务部署     │  │ 网站部署    │  │ 数据处理            │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┴────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Feishu Relay Auto Discovery                     │
│              (自动发现服务)                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - 轮询检测 (每5分钟) 或 inotify 事件驱动              │  │
│  │  - 智能类型识别 (website/service/skill/task)           │  │
│  │  - 框架检测 (Next.js/Django/Flask/Node/Go/Rust)        │  │
│  │  - 自动注册到 registry/systems.json                    │  │
│  │  - 发送飞书通知: "🆕 新系统已自动注册"                  │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    统一注册表                                │
│              /opt/feishu-notifier/registry/systems.json      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - 系统名称、类型、路径、状态                           │  │
│  │  - 自动发现标记、注册时间                               │  │
│  │  - 支持手动注册和自动发现共存                           │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    统一通知队列                              │
│              /opt/feishu-notifier/queue/notify-queue.db      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - 所有系统共享同一队列                                │  │
│  │  - 支持即时发送和定时发送                              │  │
│  │  - 失败自动重试 3 次                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    飞书消息发送                              │
│              /opt/feishu-notifier/bin/feishu_notify.sh       │
└─────────────────────────────────────────────────────────────┘
```

## 系统集成示例

### 在部署脚本中集成

```bash
#!/bin/bash
# deploy.sh - 应用部署脚本

APP_NAME="myapp"
APP_DIR="/var/www/$APP_NAME"

# 部署代码
git clone https://github.com/user/$APP_NAME.git $APP_DIR
cd $APP_DIR
npm install
npm run build

# 无需手动注册！自动发现服务会在 5 分钟内检测到

# 部署完成后发送通知
notify "🚀 $APP_NAME 部署完成" "版本: $(git describe --tags)"
```

### 在 CI/CD 中集成

```yaml
# .github/workflows/deploy.yml
- name: Deploy to server
  run: |
    rsync -avz ./dist/ server:/var/www/myapp/
    ssh server "cd /var/www/myapp && npm install --production"
    
- name: Notify deployment
  run: |
    ssh server "/opt/feishu-notifier/bin/notify '✅ 部署成功' 'myapp 已更新'"
```

### 在定时任务中集成

```bash
#!/bin/bash
# /opt/tasks/backup.sh

BACKUP_DIR="/data/backups"
DB_NAME="mydb"

# 执行备份
mysqldump $DB_NAME > $BACKUP_DIR/$DB_NAME-$(date +%Y%m%d).sql

# 发送通知
/opt/feishu-notifier/bin/notify "💾 备份完成" "$DB_NAME 数据库备份成功"
```

## 配置文件

### 飞书配置

```bash
# /opt/feishu-notifier/config/feishu.env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_USER_ID=ou_xxx
FEISHU_RECEIVE_ID_TYPE=open_id
```

### 自定义监控路径

编辑 `/opt/feishu-notifier/lib/feishu-relay-auto-discovery.py`：

```python
WATCH_PATHS = ["/opt", "/var/www", "/data", "/home", "/custom/path"]
```

## 故障排查

### 查看服务日志

```bash
# 发现服务日志
journalctl -u feishu-relay-discovery -f

# 通知服务日志
journalctl -u feishu-relay -f

# 发现日志文件
tail -f /var/log/feishu-relay/discovery.log
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 新系统未被发现 | 不在监控路径内 | 检查路径是否在 `WATCH_PATHS` 中 |
| 类型识别错误 | 缺少项目标识文件 | 添加 `package.json` 或 `README.md` |
| 通知未发送 | 飞书配置错误 | 检查 `config/feishu.env` |
| 服务未运行 | 未启用 systemd | `systemctl enable --now feishu-relay-discovery` |

## 设计原则

1. **约定优于配置** - 通过目录结构和文件内容自动识别，无需手动配置
2. **零侵入集成** - 现有系统无需修改即可接入通知系统
3. **完全自动化** - 部署即注册，删除即清理
4. **统一入口** - 所有系统使用相同的 `notify` 命令
5. **可靠投递** - 失败自动重试，确保通知送达

---

**版本**: 2.0  
**更新日期**: 2026-04-08

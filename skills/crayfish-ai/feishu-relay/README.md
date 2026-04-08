# Feishu Relay - 统一飞书通知系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个生产级的统一飞书通知系统，解决分布式任务、监控、Skill 的通知可靠性问题。

## 核心特性

- **统一入口** - 所有通知通过单一接口发送
- **可靠投递** - 网络失败自动入队重试
- **实时+异步** - 在线时即时发送，离线时队列兜底
- **配置分层** - 环境变量 > 配置文件，安全不泄露
- **日志可观测** - 完整日志输出到 systemd journal
- **零依赖** - 仅依赖 bash、python3、sqlite3

## 架构设计

```
┌─────────────────────────────────────────┐
│           触发源（任意）                  │
│  • crontab  • skill  • 脚本  • 系统监控   │
└─────────────────┬───────────────────────┘
                  │ 调用统一入口
                  ▼
┌─────────────────────────────────────────┐
│      /opt/feishu-notifier/bin/notify     │
│  ─────────────────────────────────────  │
│  1. 加载配置（环境变量 > 配置文件）        │
│  2. 尝试直接发送（调用 feishu_notify.sh） │
│  3. 成功 → 返回 sent                     │
│  4. 失败 → 入队，返回 queued             │
└─────────────────┬───────────────────────┘
                  │
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────┐      ┌──────────┐
   │ 即时发送 │      │ 队列消费  │
   │ 成功返回 │      │ feishu-relay（常驻）│
   └─────────┘      └──────────┘
```

## 快速开始

### 1. 安装

```bash
git clone https://github.com/crayfish-ai/feishu-relay.git
cd feishu-relay
sudo ./install.sh
```

或手动安装：

```bash
sudo mkdir -p /opt/feishu-notifier/{bin,lib,queue,config}
sudo cp bin/* /opt/feishu-notifier/bin/
sudo cp lib/* /opt/feishu-notifier/lib/
sudo chmod +x /opt/feishu-notifier/bin/*
sudo cp systemd/feishu-relay.service /etc/systemd/system/
sudo systemctl enable --now feishu-relay
```

### 2. 配置

创建配置文件：

```bash
sudo tee /opt/feishu-notifier/config/feishu.env << 'EOF'
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_RECEIVE_ID_TYPE=open_id
EOF

sudo chmod 600 /opt/feishu-notifier/config/feishu.env
```

或使用环境变量：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_USER_ID="ou_xxx"
export FEISHU_RECEIVE_ID_TYPE="open_id"  # 可选: open_id, user_id, chat_id, email
```

### 3. 测试

```bash
# 直接发送测试
/opt/feishu-notifier/bin/notify "测试消息" "系统运行正常"

# 管道输入
echo "备份完成" | /opt/feishu-notifier/bin/notify "任务状态"

# 查看队列
sqlite3 /opt/feishu-notifier/queue/notify-queue.db "SELECT * FROM queue;"

# 查看日志
journalctl -u feishu-relay -f
```

## 使用方式

### 在脚本中使用

```bash
#!/bin/bash
# 磁盘监控示例

USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

if [ "$USAGE" -gt 80 ]; then
    /opt/feishu-notifier/bin/notify \
        "⚠️ 磁盘告警" \
        "当前使用率 ${USAGE}%，请及时清理"
fi
```

### 在 Python 中使用

```python
import subprocess

subprocess.run([
    "/opt/feishu-notifier/bin/notify",
    "✅ 任务完成",
    "数据处理已完成"
])
```

### 在 Skill 中使用

```python
# OpenClaw Skill 内部调用
import subprocess

def on_complete():
    subprocess.run([
        "/opt/feishu-notifier/bin/notify",
        "Skill 完成",
        "任务执行成功"
    ])
```

### 在 Crontab 中使用（推荐）

**⚠️ 重要：使用系统 crontab，不是 OpenClaw cron**

```bash
# 编辑系统 crontab
crontab -e

# 添加任务示例
*/5 * * * * /opt/feishu-notifier/bin/notify "系统状态" "$(df -h / | tail -1)"
0 2 * * * /opt/backup.sh && /opt/feishu-notifier/bin/notify "备份完成" "每日备份成功"
0 23 * * * /opt/feishu-notifier/bin/notify "⏰ 提醒" "该休息了"
```

**为什么不用 OpenClaw cron？**
- OpenClaw cron 是独立的定时系统，与 feishu-relay 无关
- 系统 crontab + feishu-relay 更可靠，不依赖 OpenClaw 运行状态
- 符合"统一通知中心"设计：所有通知走 feishu-relay

## 配置说明

### 配置文件

路径：`/opt/feishu-notifier/config/feishu.env`

| 变量 | 必填 | 说明 |
|------|------|------|
| `FEISHU_APP_ID` | ✅ | 飞书应用 ID (cli_xxx) |
| `FEISHU_APP_SECRET` | ✅ | 飞书应用密钥 |
| `FEISHU_USER_ID` | ✅ | 接收者 ID |
| `FEISHU_RECEIVE_ID_TYPE` | ❌ | ID 类型：open_id/user_id/chat_id/email，默认 open_id |

### 环境变量优先级

环境变量 > 配置文件 > 默认值

```bash
# 临时覆盖配置
FEISHU_USER_ID="ou_other" /opt/feishu-notifier/bin/notify "测试" "内容"
```

## 目录结构

```
/opt/feishu-notifier/
├── bin/
│   ├── notify                    # 统一入口脚本
│   ├── feishu_notify.sh          # 核心发送脚本
│   ├── disk_monitor.sh           # 磁盘监控示例
│   └── timed_reminder.sh         # 定时提醒示例
├── lib/
│   └── feishu-relay.py           # 队列消费服务
├── queue/
│   └── notify-queue.db           # SQLite 队列数据库
├── config/
│   └── feishu.env                # 配置文件
└── README.md                     # 本文档
```

## 系统服务

### 查看状态

```bash
systemctl status feishu-relay
```

### 查看日志

```bash
# 实时日志
journalctl -u feishu-relay -f

# 最近100条
journalctl -u feishu-relay -n 100
```

### 重启服务

```bash
systemctl restart feishu-relay
```

## 队列管理

### 查看队列

```bash
# 查看待处理消息
sqlite3 /opt/feishu-notifier/queue/notify-queue.db \
    "SELECT id, title, retry, created_at FROM queue;"

# 查看统计
sqlite3 /opt/feishu-notifier/queue/notify-queue.db \
    "SELECT COUNT(*) as pending, SUM(retry) as retries FROM queue;"
```

### 清空队列

```bash
sqlite3 /opt/feishu-notifier/queue/notify-queue.db "DELETE FROM queue;"
```

### 手动插入消息

```bash
sqlite3 /opt/feishu-notifier/queue/notify-queue.db \
    "INSERT INTO queue(title, content) VALUES ('手动消息', '内容');"
```

## 故障排查

### 发送失败，返回 queued

1. 检查配置是否正确
2. 检查网络连接
3. 查看 feishu-relay 服务状态

### 消息一直不发送

```bash
# 检查服务是否运行
systemctl is-active feishu-relay

# 检查队列
sqlite3 /opt/feishu-notifier/queue/notify-queue.db "SELECT * FROM queue;"

# 查看错误日志
journalctl -u feishu-relay --since "1 hour ago"
```

### 配置文件权限

```bash
# 确保配置文件权限正确
chmod 600 /opt/feishu-notifier/config/feishu.env
chown root:root /opt/feishu-notifier/config/feishu.env
```

## 安全建议

1. **配置文件权限** - 设置为 600，仅 root 可读
2. **定期轮换密钥** - 定期更换飞书 App Secret
3. **日志脱敏** - 日志中自动脱敏敏感信息
4. **网络隔离** - 生产环境限制出站网络访问

## 性能指标

- **发送延迟** - 在线时 < 1s
- **队列处理间隔** - 30s
- **最大重试次数** - 3次
- **重试间隔** - 随重试次数递增

## 开发计划

- [ ] Web 管理界面
- [ ] 消息优先级
- [ ] 批量发送
- [ ] 消息模板
- [ ] 钉钉/企业微信支持

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 参考

- [飞书开放平台](https://open.feishu.cn/)
- [发送消息 API](https://open.feishu.cn/document/server-docs/im-v1/message/create)

## 作者

crayfish-ai

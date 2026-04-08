# Feishu Relay 系统架构与检查清单

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户/其他技能                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ 定时提醒    │  │ 系统监控    │  │ 文献管理系统        │  │
│  │ feishu-task │  │ disk_monitor│  │ pdf-monitor         │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┴────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Feishu Relay 统一队列                      │
│              /opt/feishu-notifier/queue/notify-queue.db      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - id, title, content                                 │  │
│  │  - created_at (UTC)                                   │  │
│  │  - execute_at (UTC, 定时任务使用)                      │  │
│  │  - retry (重试计数)                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Feishu Relay 消费服务                        │
│              systemctl: feishu-relay.service                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - 每 30 秒检查队列                                    │  │
│  │  - 支持立即发送 (execute_at IS NULL)                   │  │
│  │  - 支持定时发送 (execute_at <= now)                    │  │
│  │  - 失败重试 3 次                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    飞书 API 发送                             │
│              /opt/feishu-notifier/bin/feishu_notify.sh       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  - 读取 config/feishu.env                             │  │
│  │  - 调用飞书 API 发送消息                               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 组件清单

### 1. 核心服务
| 组件 | 路径 | 状态检查 |
|------|------|---------|
| feishu-relay 服务 | `/opt/feishu-notifier/lib/feishu-relay.py` | `systemctl status feishu-relay` |
| 队列数据库 | `/opt/feishu-notifier/queue/notify-queue.db` | `sqlite3 ... "SELECT COUNT(*) FROM queue;"` |
| 配置文件 | `/opt/feishu-notifier/config/feishu.env` | `ls -la config/` |

### 2. 命令工具
| 命令 | 功能 | 示例 |
|------|------|------|
| `notify` | 立即发送通知 | `notify "标题" "内容"` |
| `feishu-task-v2` | 定时任务管理 | `feishu-task-v2 in 30 "提醒"` |

### 3. 系统定时任务
| 任务 | 调度 | 命令 |
|------|------|------|
| 睡觉提醒 | 每天 23:00 | `/opt/feishu-notifier/bin/notify "⏰ 提醒" "叫大家睡觉去"` |

## 检查清单

### 日常检查
```bash
# 1. 服务状态
systemctl is-active feishu-relay

# 2. 队列状态
sqlite3 /opt/feishu-notifier/queue/notify-queue.db "SELECT COUNT(*) FROM queue;"

# 3. 最近日志
tail -10 /var/log/feishu-relay.log

# 4. 测试发送
/opt/feishu-notifier/bin/notify "测试" "系统检查"
```

### 故障排查
| 现象 | 可能原因 | 解决方法 |
|------|---------|---------|
| 消息未发送 | 服务未运行 | `systemctl restart feishu-relay` |
| 定时任务未执行 | 时区问题 | 检查 UTC 时间戳 |
| 队列堆积 | 消费服务卡住 | 重启服务，检查日志 |
| 飞书 API 错误 | 配置错误 | 检查 `config/feishu.env` |

## 设计原则

1. **完全独立**：不依赖 OpenClaw，使用系统 systemd + SQLite
2. **统一队列**：所有通知（定时、监控、技能）走同一队列
3. **可靠投递**：失败重试 3 次，确保送达
4. **时区统一**：所有时间戳使用 UTC，避免时区混乱

## 扩展接口

其他技能/系统可以通过以下方式接入：

```bash
# 方式 1：立即发送
/opt/feishu-notifier/bin/notify "标题" "内容"

# 方式 2：定时发送（通过 feishu-task-v2）
/opt/feishu-notifier/bin/feishu-task-v2 in 30 "30分钟后提醒"

# 方式 3：直接写入队列（高级）
sqlite3 /opt/feishu-notifier/queue/notify-queue.db \
    "INSERT INTO queue(title, content, execute_at) 
     VALUES('标题', '内容', datetime('now', '+30 minutes'));"
```

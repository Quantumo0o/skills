# Feishu Relay 主动注册指南

## 问题
新开发的系统、配置、网站等，如何**主动采用** feishu-relay 通道？

## 解决方案：主动注册中心

新系统通过 `feishu-relay-register` 主动注册，自动获得通知能力。

## 注册方式

### 方式 1：命令行注册（推荐）

```bash
# 注册新网站
feishu-relay-register register myapp website /var/www/myapp

# 注册新服务
feishu-relay-register register myservice service /opt/myservice

# 注册新脚本
feishu-relay-register register backup-script script /opt/backup/backup.sh

# 注册定时任务
feishu-relay-register register daily-report cron "/path/to/report.sh"
```

### 方式 2：SDK 集成

**Bash:**
```bash
source /opt/feishu-notifier/sdk/bash/notify.sh
notify "标题" "内容"
notify_later 30 "30分钟后提醒"
```

**Python:**
```python
from feishu_relay import notify, notify_later

notify("标题", "内容")
notify_later(30, "30分钟后提醒")
```

**PHP:**
```php
require_once '/opt/feishu-notifier/sdk/php/notify.php';

FeishuRelay::notify("标题", "内容");
FeishuRelay::notifyLater(30, "30分钟后提醒");
```

### 方式 3：直接调用（最简单）

任何系统都可以直接调用：

```bash
# Bash
/opt/feishu-notifier/bin/notify "标题" "内容"

# 定时通知
/opt/feishu-notifier/bin/feishu-task-v2 in 30 "30分钟后提醒"
```

```python
# Python
import subprocess
subprocess.run(["/opt/feishu-notifier/bin/notify", "标题", "内容"])
```

```php
// PHP
shell_exec('/opt/feishu-notifier/bin/notify "标题" "内容"');
```

## 注册后的效果

### 网站注册后

```bash
feishu-relay-register register myshop website /var/www/myshop
```

自动生成：
- `/var/www/myshop/notify-integration.php` - PHP 集成示例
- `/opt/feishu-notifier/webhooks/myshop.sh` - Webhook 端点

在网站代码中使用：
```php
<?php
// 发送订单通知
shell_exec('/opt/feishu-notifier/bin/notify "新订单" "订单号: 12345"');
?>
```

### 服务注册后

```bash
feishu-relay-register register myapi service /opt/myapi
```

在服务代码中使用：
```bash
#!/bin/bash
# /opt/myapi/start.sh

# 启动时发送通知
/opt/feishu-notifier/bin/notify "[myapi] 服务启动" "API 服务已启动"

# 异常时发送通知
/opt/feishu-notifier/bin/notify "[myapi] 异常" "检测到错误"
```

### 脚本注册后

```bash
feishu-relay-register register backup script /opt/backup/backup.sh
```

自动注入通知函数到脚本：
```bash
#!/bin/bash
# 原脚本自动添加:
notify() {
    /opt/feishu-notifier/bin/notify "${1:-通知}" "${2:-}"
}

# 脚本中直接使用
notify "备份完成" "数据库备份成功"
```

## 注册表管理

### 查看所有注册系统

```bash
feishu-relay-register list
```

输出：
```
=== 已注册的系统 ===
myshop      [website]  -  active  -  2026-04-08T10:00:00Z
myapi       [service]  -  active  -  2026-04-08T09:30:00Z
backup      [script]   -  active  -  2026-04-08T09:00:00Z

统计:
[
  {"type": "website", "count": 1},
  {"type": "service", "count": 1},
  {"type": "script", "count": 1}
]
```

### 注销系统

```bash
feishu-relay-register unregister myshop
```

## 完整流程示例

### 场景：新开发的电商网站

**Step 1: 注册网站**
```bash
feishu-relay-register register myshop website /var/www/myshop
```

**Step 2: 在网站代码中使用**
```php
<?php
// order.php

// 新订单通知
shell_exec('/opt/feishu-notifier/bin/notify "新订单" "订单号: ' . $order_id . '"');

// 支付成功通知
shell_exec('/opt/feishu-notifier/bin/notify "支付成功" "金额: ¥' . $amount . '"');
?>
```

**Step 3: 完成**
- 新订单自动发送飞书通知
- 无需配置，自动接入统一通知中心

## 优势

| 特性 | 说明 |
|------|------|
| **主动注册** | 新系统主动采用 feishu-relay，无需等待发现 |
| **自动配置** | 注册后自动生成通知脚本/SDK |
| **统一管理** | 所有注册系统集中管理 |
| **向后兼容** | 未注册系统也能使用全局命令 |
| **多语言支持** | Bash/Python/PHP SDK |

## 总结

**回答你的问题：**

> "后面新开发的系统、配置、网站等等，怎么主动采用 feishu-relay 这个通道来？"

**答案：主动注册**

1. **命令行注册**: `feishu-relay-register register myapp website /path`
2. **SDK 集成**: `source /opt/feishu-notifier/sdk/bash/notify.sh`
3. **直接调用**: `/opt/feishu-notifier/bin/notify "标题" "内容"`

新系统开发时，**一行命令**即可接入 feishu-relay，自动获得通知能力！

---
name: communication-assistant
description: 全能通信助理技能 - 统一管理iMessage短信、邮件和通知发送。支持BlueBubbles(iMessage)和Himalaya(邮件)集成。
author: OpenClaw
author-url: https://openclaw.ai
tags: ['communication', 'email', 'imessage', 'sms', 'notification', 'assistant', 'bluebubbles', 'himalaya']
category: productivity
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "emoji": "📬",
        "requires": { "config": ["channels.bluebubbles"], "bins": ["himalaya"] },
        "install":
          [
            {
              "id": "himalaya",
              "kind": "brew",
              "formula": "himalaya",
              "bins": ["himalaya"],
              "label": "Install Himalaya Email CLI",
            },
          ],
      },
  }
---

# 📬 通信助理技能 (Communication Assistant)

全能通信助理，统一管理你的所有消息通信渠道。

## 功能概述

整合了iMessage(BlueBubbles)和邮件(Himalaya)两大通信渠道，提供统一的消息发送、通知提醒和通信管理功能。

## ✨ 核心功能

### 💬 iMessage 短信 (BlueBubbles)
- 发送文本消息和附件
- 消息Tapback表情回应
- 编辑/撤回已发送消息
- 线程内回复
- 群组聊天管理
- iMessage特效发送

### 📧 电子邮件 (Himalaya)
- 邮件列表和查看
- 编写、回复、转发邮件
- 邮件搜索和筛选
- 文件夹管理
- 附件下载
- 多账户支持

### 🔔 通知提醒
- 支持同时发送到邮箱和手机号
- Markdown格式消息内容
- 批量通知发送
- 通知脚本集成

## 快速开始

### 发送iMessage

```json
{
  "action": "send",
  "channel": "bluebubbles",
  "target": "+15551234567",
  "message": "Hello from Communication Assistant!"
}
```

### 发送邮件

```bash
himalaya message write -H "To:user@example.com" -H "Subject:Hello" "Message body"
```

### 使用通知脚本发送批量通知

```bash
bash scripts/send-notification.sh \
  --content ./notification.md \
  --emails "user1@example.com,user2@example.com" \
  --phones "+15551234567,+15557654321"
```

## 配置要求

### BlueBubbles (iMessage)
需要在网关配置中添加：
```toml
[channels.bluebubbles]
serverUrl = "https://your-bluebubbles-server.com"
password = "your-api-password"
```

### Himalaya (邮件)
创建配置文件 `~/.config/himalaya/config.toml`:
```toml
[accounts.personal]
email = "you@example.com"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
```

## 使用场景

- 📱 **个人助理**: 自动回复短信和邮件
- 🔔 **系统通知**: 任务完成后发送多渠道提醒
- 📋 **批量通知**: 同时发送邮件和短信给多个收件人
- 📧 **邮件处理**: 自动分类和回复邮件
- 💬 **消息管理**: 统一管理所有消息渠道

## 技能清单

包含的工具和脚本：
- `send-notification.sh` - 批量通知发送脚本
- BlueBubbles iMessage集成
- Himalaya邮件CLI集成
- Markdown格式化支持

## License

MIT

---

**让通信变得简单而高效** 🚀

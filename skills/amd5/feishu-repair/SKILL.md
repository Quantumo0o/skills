---
name: feishu-repair
description: 自动修复飞书-飞书群聊自动修复+会话自动修复 - 诊断 Gateway 连接、权限配置、消息投递问题
version: 1.3.0
author: c32
category: monitoring
tags:
  - feishu
  - repair
  - group-chat
  - session
requirements:
  node: ">=18.0.0"
  systemd: true
---

# Feishu Repair — 飞书群聊+会话修复技能

**版本**: 1.0.0
**创建日期**: 2026-04-14
**触发关键词**: `修复飞书`

---

## 📋 功能

自动诊断和修复 OpenClaw 飞书渠道的常见问题：

| 问题类型 | 诊断方式 | 修复方式 |
|---------|---------|---------|
| Gateway 未运行 | systemctl 检查 | 提示手动重启 |
| 飞书 WebSocket 断开 | journalctl 日志 | 提示手动重启 |
| 群聊权限丢失 | 检查 groupAllowFrom | 自动恢复配置 |
| 用户权限丢失 | 检查 allowFrom | 自动恢复配置 |
| 配置未生效 | 检查 config | 提示手动重启 Gateway |
| 消息不回复 | 综合诊断 | 输出修复报告 |

---

## 📂 文件结构

```
skills/feishu-repair/
├── SKILL.md
├── skill.json
├── _meta.json
└── scripts/
    └── diagnose.js     # 诊断脚本
```

---

## 🔧 修复流程

1. **诊断**: 检查 Gateway、飞书配置、日志错误
2. **修复**: 从配置文件恢复丢失的权限
3. **重启**: 自动重启 Gateway 使配置生效
4. **验证**: 自动检查修复结果（配置+日志）

| 策略 | 触发条件 | 动作 |
|------|---------|------|
| 配置恢复 | 权限丢失/配置异常 | 从 `openclaw.json` 或 `openclaw.json.bak*` 读取完整配置自动恢复 |
| Gateway 状态检查 | Gateway 未运行 | 提示手动重启 |
| WebSocket 重连 | WS 断开日志 | 提示手动重启 |
| 配置生效检查 | 配置变更未生效 | 提示手动重启 Gateway |

### 配置读取优先级

1. **`~/.openclaw/openclaw.json`**（当前配置）
2. **`~/.openclaw/openclaw.json.bak`**（最新备份）
3. **`~/.openclaw/openclaw.json.bak.1`**（更早备份）

按顺序读取，找到第一个有飞书配置的文件即停止。从中提取 `allowFrom`、`groupAllowFrom`、`appId` 等完整列表。

---

## 📊 配置来源

技能内**不硬编码**任何用户 ID、群聊 ID、App ID。

全部从用户的 `openclaw.json` 及其备份文件中动态读取。

---

## ⚠️ 注意事项

- Gateway 重启操作仅提示用户手动执行（不自动重启）
- 权限配置恢复会自动写入 openclaw.json
- 诊断结果输出详细报告

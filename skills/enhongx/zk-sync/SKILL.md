---
name: zk-sync
description: Sync saved knowledge item to NotebookLM after Feishu save succeeds.
commands:
  - name: zk
    description: 同步知识到 NotebookLM
    usage: /zk <id>
    action: run
    script: run.sh
    args:
      - "{{id}}"
      - "{{title_b64}}"
      - "{{content_b64}}"
  - name: zk.help
    description: 查看 zk-sync 使用帮助
    action: help
---

# zk-sync

在飞书保存知识项成功后，自动同步到 Google NotebookLM。

## 📋 可用指令

| 指令 | 说明 |
|------|------|
| `/zk <id>` | 同步指定知识到 NotebookLM |
| `/zk.help` | 查看使用帮助 |

## 🔧 使用示例

```bash
# 查看帮助
/zk.help

# 同步知识到 NotebookLM
/zk abc123
```

## 📥 输入参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `id` | 知识项 ID | 飞书保存后返回 |
| `title_b64` | 标题（Base64 编码） | 自动获取 |
| `content_b64` | 内容（Base64 编码） | 自动获取 |

## 📤 输出状态

- ✅ `ok=true, status=synced` — 同步成功
- ❌ `ok=false, status=failed` — 同步失败

## ⚠️ 注意事项

1. **仅在飞书保存成功后使用** - 需要有效的知识 ID
2. **同步状态会返回确认结果** - 检查输出确认同步状态
3. **NotebookLM 配置** - 确保 notebooklm 环境已配置

## 🔗 相关技能

- `notebooklm` - Google NotebookLM 完整 API
- `feishu-doc` - 飞书文档操作

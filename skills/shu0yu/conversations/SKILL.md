---
name: conversations
description: 管理对话历史存档。从 OpenClaw sessions/*.jsonl 导入对话到本地 SQLite 库，并提供查询能力。触发场景：(1) 用户要求导入历史对话、(2) 用户要求查看/搜索/读取历史对话、(3) 需要查询过去某次对话内容、(4) "我们的对话记录"、"历史对话"、"memos"、"conversations" 相关请求。
---

# Conversations

将 OpenClaw session 文件（JSONL）导入本地 SQLite 对话库，并提供查询工具。

## 数据库

- 路径：`{WORKSPACE}/conversations.db`（可通过环境变量 `CONVERSATIONS_DB` 覆盖）
- 结构：`chunks`（user/assistant 对话）、`embeddings`（向量索引）
- 详情见 `references/schema.md`

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_WORKSPACE` | OpenClaw workspace 路径 | 自动推断 |
| `CONVERSATIONS_DB` | 数据库路径 | `{WORKSPACE}/conversations.db` |

## 导入脚本

```bash
# 预览（不写入）
python3 {baseDir}/scripts/import_sessions.py --dry-run

# 执行导入
python3 {baseDir}/scripts/import_sessions.py
```

- 自动跳过 `.deleted` 标记的 session 文件
- 按 content_hash 去重，已导入的不重复写入
- 只导入 user + assistant，跳过 toolResult

## 查询脚本

```bash
python3 {baseDir}/scripts/query_conversations.py stats              # 统计总览
python3 {baseDir}/scripts/query_conversations.py recent [n]       # 最近 n 条
python3 {baseDir}/scripts/query_conversations.py random [n]        # 随机 n 条
python3 {baseDir}/scripts/query_conversations.py search <关键词>   # 关键词搜索
python3 {baseDir}/scripts/query_conversations.py session <key>     # 某 session 的消息
python3 {baseDir}/scripts/query_conversations.py after <ts_ms>     # 某时间戳之后的记录
```

**时间戳换算**（Python）：
```python
from datetime import datetime, timezone
ts = int(datetime(2026,4,7,0,0,0,tzinfo=timezone.utc).timestamp()*1000)
# 例: 2026-04-07 00:00 GMT+8 = 1775520000000
```

## 工作流程

1. **导入**：定期（每周/每月）或积累一批新对话后跑一次 `import_sessions.py`
2. **查询**：用 `query_conversations.py` 按需查询（搜索、随机抽样、时间范围等）
3. **深度分析**：直接写 Python 脚本操作 `conversations.db`

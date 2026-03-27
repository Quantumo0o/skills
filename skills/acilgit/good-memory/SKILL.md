---
name: good-memory
version: 1.2.1
description: Session 历史记录恢复技能。通过 Tracker + Birth Time 验证实现 session 重置后快速恢复上下文。解决系统自动重置导致的"失忆"问题。
homepage: https://github.com/openclaw/openclaw
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["bash","tail","ls","date","python3"]}}}
---

# Good-Memory

帮助 Agent 在 session 重置后快速恢复对话上下文。通过读取带有 `.reset.` 前缀的 session 文件实现。

## 安装

安装 skill 后，需要运行安装脚本将启动指令注入到所有 Agent 的 AGENTS.md：

```bash
chmod +x /root/.openclaw/workspace/skills/good-memory/scripts/install.sh
bash /root/.openclaw/workspace/skills/good-memory/scripts/install.sh
```

该脚本会自动扫描所有 Agent 的 AGENTS.md 并注入 Good-Memory 指令。已有指令的 Agent 会被跳过。

## ⚠️ 启动时必须执行

**每次 session 启动时**（收到第一条消息前），立即执行：

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/maintenance.sh detect "AGENT_NAME" "$INBOUND_CHAT_ID"
```

- `AGENT_NAME`：当前运行的 agent 名称（main / tuwen / xiangmu / guwen）
- `INBOUND_CHAT_ID`：当前对话的 chat_id，**从 inbound metadata 中获取**

> ⚠️ `INBOUND_CHAT_ID` 必须从 inbound metadata 的 `chat_id` 字段动态获取，**不要硬编码**。

**detect 会自动完成：**
1. 检测 UUID 是否改变（判断是否发生了 reset）
2. 如果发生了 reset → 从 tracker 历史记录中读取旧 session 内容
3. 同步更新 tracker 文件（确保其他 agent 能看到正确状态）

## 核心原理

Session 重置后，OpenClaw 会自动将正在进行的 session 文件重命名为：

```
{session_id}.jsonl.reset.2026-03-21T05:57:30.339Z
                              ↑ ISO 时间戳
```

**不需要扫描文件内容**，直接通过文件名判断：

1. 有 `.reset.` 前缀 → 已归档的 session
2. 无 `.reset.` 前缀 → 当前活跃 session

## 使用方式

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh <command> [options]
```

## 命令列表

### 1. latest — 获取最近一次重置的 session 文件路径

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh latest <agent>
```

**参数：**
- `agent` — Agent 名称（main/tuwen/xiangmu/guwen）

### 2. read — 读取最近 N 条记录

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh read <agent> [--lines N]
```

**参数：**
- `agent` — Agent 名称
- `--lines N` — 读取最近 N 条记录（默认 20）

### 3. read-file — 读取指定文件的最后 N 行

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh read-file <file> [--lines N]
```

**参数：**
- `file` — 文件完整路径
- `--lines N` — 读取最近 N 行（默认 20）

### 4. list — 列出所有已重置的 session 文件

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh list <agent>
```

返回该 agent 下所有 `.reset.` 文件，按时间从新到旧排序。

## detect 输出说明

```
# 未发生重置
OK: session unchanged
last_history:
last_session_created:

# 发生重置
RESET_DETECTED: UUID mismatch
stored_uuid: xxx
current_uuid: xxx
last_history: /path/to/xxx.reset.2026-03-27T00:14:04Z
last_session_created: 2026-03-26T08:48:29.997020+00:00
---LAST_HISTORY_LINES---
[原始 JSONL 格式的最后 20 条记录]
```

**当检测到 RESET_DETECTED 时，Agent 需要：**
1. 读取 `---LAST_HISTORY_LINES---` 后的历史记录
2. 将其作为上下文继续对话
3. 在第一条回复开头告知用户：已自动恢复上一段对话

## Tracker 文件

**位置：** `/root/.openclaw/workspace/session-tracker.json`

**用途：** 记录每个 Agent + 每个 Chat 的 session 对应关系。

**结构：**
```json
{
  "last_updated": "2026-03-27T08:14:06Z",
  "agents": {
    "main": {
      "ou_xxx": {
        "chat_type": "direct",
        "active": "/path/to/active.jsonl",
        "active_uuid": "uuid-prefix",
        "active_created_at": "2026-03-27T08:14:06.709051+00:00",
        "session_key": "agent:main:feishu:direct:ou_xxx",
        "last_history": {
          "file": "/path/to/xxx.reset.2026-03-27T00:14:04Z",
          "created_at": "2026-03-26T08:48:29.997020+00:00",
          "ended_at": "2026-03-27T00:14:04Z"
        },
        "history": []
      }
    }
  }
}
```

**验证逻辑（双重验证）：**
1. **UUID 前缀比对**（主要）— UUID 全局唯一，前缀改变 = 一定是新 session
2. **Birth Time 比对**（辅助）— UUID 相同时，用 birth time 辅助确认

## 默认值说明

| 参数 | 默认值 | 位置 |
|------|--------|------|
| 历史记录条数 | 20 | maintenance.sh detect / recovery.sh read |

**注意：** detect 输出的历史记录是原始 JSONL 格式，每行一条记录。

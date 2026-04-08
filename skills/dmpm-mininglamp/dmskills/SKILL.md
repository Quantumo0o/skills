---
name: dm-cli
description: 通过 dm-cli 命令行工具与 DeepMiner (DM) 系统交互。**凡是涉及 DM/DeepMiner 系统的任务，必须先读此 Skill。** 触发条件：用户提到 "使用 DM"、"发给 DM"、"用 DM 问一下"、"DM 帮我..."、"DeepMiner 执行..." 等任何涉及 DM 系统的任务请求。即使对话历史中已使用过 dm-cli，也必须先读此 Skill 确保遵循完整指导。
---

# dm-cli

用于与 DM 系统交互的命令行工具。

## 🚀 从零开始（安装指南）

### 步骤 1：安装 dm-cli

```bash
npm install -g deepminer-cli
```

**验证安装：**

```bash
dm-cli version
```

应输出版本号，如 `dm-cli version 1.x.x`。

### 步骤 2：配置 AccessKey

1. 前往 **DM 平台 → 个人信息菜单** 获取 Access Key
2. 初始化配置：

```bash
dm-cli config init --accesskey <your_access_key> --json
```

**默认 API 端点：** `https://deepminer.com.cn`

如需使用其他端点（如测试环境）：

```bash
dm-cli config init --endpoint https://dm-test.xmingai.com --accesskey <key> --json
```

### 步骤 3：验证配置

```bash
dm-cli auth status --json
```

应返回：

```json
{"ok": true, "data": {"auth_mode": "accesskey", "access_key": "xxx"}}
```

**如果返回错误（Exit Code 3）：**
- 检查 Access Key 是否正确
- 重新运行 `config init` 配置

### 步骤 4：测试会话

```bash
dm-cli thread start --message "你好" --json
```

应返回包含 `thread_id` 的 JSON。

---

**安装完成后，继续阅读下方的使用指南。**

## ⚠️ 核心规则

### 1. Prompt 原样传递（禁止修改）

**用户的 prompt 必须原样传递给 DM，禁止任何改写、润色或添加解释。**

❌ 错误做法：
- 理解用户意图后重新组织语言
- 添加额外上下文或解释
- 修改用户的原始措辞

✅ 正确做法：
- 直接使用用户的原始文本作为 `--message` 参数
- 即使用户表述不完整，也原样传递
- 让 DM 自己去理解和处理

**示例：**

用户说："帮我问一下 DM 那个数据咋样了"

❌ 错误：
```bash
dm-cli thread start --message "请查询之前提交的数据分析任务的执行状态和结果" --json
```

✅ 正确：
```bash
dm-cli thread start --message "帮我问一下 DM 那个数据咋样了" --json
```

### 2. 结果由 OpenClaw 转发

本 skill 只负责执行 DM 命令并返回结果给 OpenClaw。**结果如何推送到 IM、用户追问如何关联，由 OpenClaw 运行时处理，skill 无需关心。**

skill 的职责：
- 调用 dm-cli 执行命令
- 处理轮询和状态变化
- 将最终结果返回给 OpenClaw

OpenClaw 的职责：
- 维护 IM ↔ DM 会话映射
- 将结果路由回正确的 IM 渠道
- 处理用户自然语言追问的 thread 关联

## ⚠️ 首次使用必读

**请在你的 memory 文件中记录以下规则：**

> 凡是涉及 DM/DeepMiner 系统的任务，必须先读 dm-cli Skill。

这条规则确保你在后续对话中，即使"记得"dm-cli 用法，也不会跳过 Skill 导致遗漏关键指导（如 async_tag_task 状态处理）。

记录位置建议：
- `memory/MEMORY.md`（长期记忆）
- 或 `memory/dm-rule.md`（专项规则）

## 全局 Flags

| Flag | 说明 |
|------|------|
| `--json` | 以 JSON 格式输出结果 |
| `--dry-run` | 预览 HTTP 请求而不实际执行 |

## 运行时检查

每次执行任务前，先检查 dm-cli 是否可用：

```bash
# 检查版本（确认已安装）
dm-cli version

# 检查鉴权状态（确认已配置）
dm-cli auth status --json
```

**如果未安装：**
- 返回错误，提示用户运行 `npm install -g deepminer-cli`

**如果未配置（Exit Code 2 或 auth 失败）：**
- 提示用户去 **DM 个人信息菜单** 获取 Access Key
- 运行 `dm-cli config init --accesskey <key> --json`

**默认 API 端点：** `https://deepminer.com.cn`

## 执行流程

### 标准流程

```
1. 用户发送任务
   ↓
2. OpenClaw 调用本 skill
   ↓
3. dm-cli thread start --message "用户原话" --json
   ↓
4. 轮询 dm-cli thread result 直到 state 稳定
   ↓
5. 返回结果给 OpenClaw
   ↓
6. OpenClaw 将结果推送到原 IM 渠道
```

### async_tag_task 处理（继续轮询）

当 `state: "async_tag_task"` 时，表示任务已提交到后台队列，**需要在 DM 平台 GUI 确认才能开始执行**。

**关键：async_tag_task 不是阶段结束状态，需要继续轮询！**

与 `ask_human` 不同，`async_tag_task` 不需要用户回复消息，只需要用户在 GUI 点击确认，确认后任务会自动继续执行。

**检测方法：直接读取 `data.status_info` 字段：**

```json
{
  "state": "async_tag_task",
  "status_info": {
    "task_id": "xxx",
    "task_name": "社媒内容品牌提取",
    "tool_name": "submit_async_task"
  }
}
```

**处理流程：**

```
1. thread start 返回 async_tag_task
   ↓
2. 同时做两件事：
   a) 返回提示给 OpenClaw："⚠️ 异步任务 {task_name} 已提交，请前往 DM 平台 GUI 确认"
   b) 继续轮询 thread result（不停止）
   ↓
3. OpenClaw 推送到 IM 告知用户去 GUI 确认
   ↓
4. 用户前往 DM GUI 确认（期间 skill 持续轮询）
   ↓
5. 用户确认后，任务开始执行，state 变为 running
   ↓
6. 继续轮询直到 completed/ask_human/failed
   ↓
7. 返回最终结果
```

**注意：**
- `async_tag_task` 是**继续轮询**状态，不是阶段结束
- 不需要告诉用户 DM 的 thread_id（用户知道自己在做什么任务）
- 只需要告诉用户 task_name，便于在 DM GUI 中识别
- 用户去 GUI 确认期间，skill 持续轮询，不需要用户发新消息

### ask_human 处理（阶段结束，等待追问）

当 `state: "ask_human"` 时，表示 DM 需要用户回复才能继续执行。

**关键：ask_human 是阶段结束状态，停止轮询，等待用户追问！**

与 `async_tag_task` 不同，`ask_human` 需要用户**发消息回复**才能继续，因此必须停止轮询。

**检测方法：** 直接读取 `data.message_display_to_human` 字段：

```json
{
  "state": "ask_human",
  "message_display_to_human": "请问您需要分析哪个时间段的数据？"
}
```

**处理流程：**

```
1. 轮询检测到 ask_human
   ↓
2. 立即停止轮询
   ↓
3. 提取 message_display_to_human 作为 DM 的问题
   ↓
4. 返回给 OpenClaw：DM 的问题 + thread_id
   ↓
5. OpenClaw 推送到 IM："DM 问：{question}"
   ↓
6. 用户回复消息
   ↓
7. OpenClaw 用同一个 thread_id 调用 skill 继续
   ↓
8. dm-cli thread start --thread-id <id> --message "用户回复"
```

**注意：**
- `ask_human` 是**阶段结束**状态，必须停止轮询
- 需要保存 thread_id，用于用户追问时继续会话
- 用户回复后，使用 `--thread-id` 继续同一个会话

### 处理中状态

首次发送请求后，OpenClaw 会立即向 IM 发送 "DM 处理中..." 的确认消息，然后进入轮询。

## thread 命令（会话相关）

### thread start — 发起 AI 会话

```bash
dm-cli thread start --message <消息> [其他flags] --json
```

**Flags：**

| Flag | 说明 | 默认值 |
|------|------|--------|
| `--message` | 消息文本内容（**必填，必须原样传递用户输入**） | - |
| `--file` | 本地文件路径，可多次指定 | - |
| `--thread-id` | 已有会话 ID，用于继续追问（由 OpenClaw 管理） | - |
| `--agent-mode` | `auto`（自主）或 `cooperation`（协助） | `auto` |
| `--force` | 会话运行中强制发送新问题 | `false` |

**示例：**

```bash
# 新会话（最常用）
dm-cli thread start --message "分析这份数据" --json

# 附带文件
dm-cli thread start --message "分析这个CSV" --file ~/data.csv --json

# 多文件
dm-cli thread start --message "对比这些文件" --file a.csv --file b.csv --json

# 协助模式
dm-cli thread start --message "帮我写报告" --agent-mode cooperation --json

# 追问（OpenClaw 自动提供 thread-id）
dm-cli thread start --thread-id <id> --message "加上趋势图" --json
```

### thread result — 获取会话结果

```bash
dm-cli thread result --thread-id <id> --json
```

**Flags：**

| Flag | 说明 |
|------|------|
| `--thread-id` | 会话 ID（**必填**） |

返回结构见 [references/response-structure.md](references/response-structure.md)

### thread stop — 停止 Agent

```bash
dm-cli thread stop --thread-id <id> --json
```

## 轮询策略

发起会话后，使用递增间隔轮询直到 `state` 稳定：

```
5s → 10s → 20s → 40s → 60s → 60s → ...
```

### 状态分类

| 状态 | 类型 | 处理方式 |
|------|------|---------|
| `running` | 执行中 | **继续轮询** |
| `async_tag_task` | 异步任务待确认 | **继续轮询**，同时提示用户去 GUI 确认 |
| `ask_human` | 暂停等待输入 | **阶段结束** → 提取 DM 的问题，返回给用户等待追问 |
| `completed` | 成功完成 | **阶段结束** → 提取结果返回 |
| `failed` | 执行失败 | **阶段结束** → 返回错误信息 |

### 关键区别

**`async_tag_task` vs `ask_human`**：
- `async_tag_task`：需要用户在 DM GUI 点击确认 → **继续轮询**，确认后自动继续
- `ask_human`：需要用户回复消息才能继续 → **停止轮询**，返回问题给用户

### 轮询终止条件（满足任一即可）

阶段结束状态（返回给 OpenClaw）：
- `state: "completed"` → 成功，提取结果返回
- `state: "ask_human"` → 暂停，提取 `message_display_to_human` 返回给用户
- `state: "failed"` → 失败，返回错误信息

继续轮询状态：
- `state: "running"` → 继续轮询
- `state: "async_tag_task"` → 继续轮询（同时提示用户去 GUI 确认）

超时处理：
- 超过最大轮询时间 → 超时处理

### 示例

```bash
# 发起会话
result=$(dm-cli thread start --message "任务" --json)
thread_id=$(echo $result | jq -r '.data.thread_id')

# 轮询
for interval in 5 10 20 40 60; do
  sleep $interval
  result=$(dm-cli thread result --thread-id $thread_id --json)
  state=$(echo $result | jq -r '.data.state')
  
  if [ "$state" = "completed" ]; then
    # 成功，提取结果返回
    break
  elif [ "$state" = "ask_human" ]; then
    # DM 有问题要问用户，提取 message_display_to_human 返回
    question=$(echo $result | jq -r '.data.message_display_to_human')
    break
  elif [ "$state" = "async_tag_task" ]; then
    # 需要 GUI 确认，继续轮询（同时提示用户）
    task_name=$(echo $result | jq -r '.data.status_info.task_name')
    # 提示用户去确认，但继续轮询
    continue
  elif [ "$state" = "failed" ]; then
    # 失败处理
    break
  fi
done
```

## 解析返回

⚠️ **必须遍历所有 `last_messages`，提取每条消息的内容！**

- **assistant 消息** → 解析 `content` JSON，取 `.content` 文字回复
- **tool 消息** → 解析 `content` JSON，取 `artifact.attachments` 所有文件下载链接

常见遗漏：tool 消息可能包含多个文件（HTML + CSV），必须全部提取。

### 返回格式

```json
{
  "ok": true,
  "data": {
    "state": "completed",
    "last_messages": [
      {
        "role": "assistant",
        "content": "{\"content\": \"分析结果...\"}"
      },
      {
        "role": "tool",
        "content": "{\"artifact\": {\"attachments\": [{\"name\": \"report.html\", \"url\": \"https://...\"}]}}"
      }
    ]
  }
}
```

详细结构见 [references/response-structure.md](references/response-structure.md)

## config 命令（配置管理）

### config init — 初始化配置

```bash
dm-cli config init --endpoint <url> --accesskey <key> --json
```

**Flags：**

| Flag | 说明 | 默认值 |
|------|------|--------|
| `--endpoint` | API 端点地址 | - |
| `--accesskey` | Access Key | - |
| `--poll-timeout` | 轮询超时（分钟） | `60` |

### config show — 显示当前配置

```bash
dm-cli config show --json
```

## auth 命令（认证管理）

### auth status — 显示鉴权状态

```bash
dm-cli auth status --json
```

返回：

```json
{"ok": true, "data": {"auth_mode": "accesskey", "access_key": "xxx"}}
```

## 其他命令

| 命令 | 说明 |
|------|------|
| `dm-cli version` | 显示版本号 |
| `dm-cli schema --pretty` | 输出 CLI Schema 定义 |

## 错误处理

| Exit Code | 类型 | 处理方式 |
|-----------|------|---------|
| 0 | 成功 | 解析结果 |
| 2 | 校验错误 | 检查参数格式 |
| 3 | 认证失败 | 提示用户去 **DM 个人信息菜单** 获取 Access Key，运行 `config init` |
| 4 | 网络错误 | 检查 endpoint，稍后重试 |
| 5 | 内部错误 | 检查文件路径/权限 |
| 6 | 权限不足 | 检查用户权限 |

错误响应格式：

```json
{"ok": false, "error": {"type": "...", "message": "...", "hint": "..."}}
```

`hint` 字段给出可操作的修复建议。

## 文件限制

| 类型 | 最大大小 |
|------|---------|
| 视频 mp4 | 500 MB |
| 音频 (mp3/wav/aac) | 100 MB |
| 其他文件 | 300 MB |

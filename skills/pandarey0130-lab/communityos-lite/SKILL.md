---
name: community-os-lite
description: >-
  Runs and extends CommunityOS Lite — local FastAPI admin, Lite UI at /lite, multi-bot Telegram
  polling via telegram_runner, global LLM config, and per-bot text knowledge. Use when deploying or
  debugging CommunityOS Lite, Telegram bot + LLM setup, admin/app.py, telegram_runner.py,
  admin/data JSON store, or contrasting with full CommunityOS / Harness multi-bot stack.
---

# CommunityOS Lite

轻量多 Bot Telegram 管理：FastAPI 后台 + 长轮询 `getUpdates` + 统一 LLM。**不包含** Harness / `start_harness.py` 那套治理与多机协作（完整版见 `community-os` skill）。

## 快速启动

在仓库根目录：

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # 按需填写密钥
python admin/app.py
```

- 管理端监听：**`127.0.0.1:8877`**（代码写死，与 `.env.example` 里的 PORT 可能不一致）
- Lite 页面：**http://127.0.0.1:8877/lite**（当前路由**无登录**，仅应本机使用）
- 启动 `admin/app.py` 时，lifespan 会**自动拉起** `admin/telegram_runner.py` 子进程；也可用 API `/api/telegram/start|stop|status` 管理（需与 app 内全局进程变量一致）
- 冒烟（无外网 TG/LLM）：`python scripts/smoke_lite.py`

## 安全与边界

- **仅本地**：绑定 127.0.0.1，不要把端口暴露到公网。
- **`/lite` 无会话校验**：任何人能打开本机该 URL 即可改 Bot 配置；生产请加反向代理与认证或改代码。
- **出站流量**：Telegram Bot API、所选 LLM 厂商 API。
- **敏感信息**：Bot token、API key 只在 `.env` 或 `admin/data/bots.json` / `admin/data/llm_config.json` 中配置；这两份 JSON 默认 **gitignore**，仓库内仅有 **`admin/data/llm_config.example.json`**（空 key）作模板；不要在 skill、issue、聊天记录里粘贴真实 token 或 key。

## 环境变量

至少配置 Telegram 与一种 LLM（常用 MiniMax）：

| 用途 | 示例 |
|------|------|
| LLM | `MINIMAX_API_KEY`（或 OpenAI / Anthropic / DeepSeek 等，与后台「LLM 配置」一致） |
| Telegram | 单 Bot 可用 `TELEGRAM_BOT_TOKEN`；多 Bot 时 runner 会读 `{BOT_ID}_TOKEN`，`BOT_ID` 为 `bots.json` 里 `bot_id` 的大写（若含空格，环境变量名不实用，**优先在 Lite UI 保存 token**） |

`telegram_runner` 解析顺序（简化）：`bots.json` 的 `bot_token` → 非占位则直接用；否则 `{BOT_ID}_TOKEN` → `TELEGRAM_BOT_TOKEN`。

## 目录与数据

| 路径 | 说明 |
|------|------|
| `admin/app.py` | FastAPI 应用入口 |
| `admin/telegram_runner.py` | 多 Bot 长轮询与回复 |
| `admin/lite.html` | Lite UI |
| `admin/data/bots.json` | Bot 列表、soul、knowledge 文本、token 等 |
| `admin/data/llm_config.json` | 全局 LLM 配置（仅当设置了非空的 `MINIMAX_API_KEY` 环境变量时才覆盖文件中的 key） |
| `bot_engine/llm/` | LLM 工厂与各厂商实现 |

## Telegram 群隐私教程（Group Privacy）

这是 **Telegram 官方**对机器人在**群聊**里「能收到哪些消息」的规则，不是 Lite 的 bug。新创建的 Bot **默认开启**群隐私（Privacy mode / Group Privacy）。

### Privacy 开 / 关分别会怎样

| 设置 | BotFather 里常见文案 | 群里谁会触发 `getUpdates` |
|------|----------------------|---------------------------|
| **开启（默认）** | Privacy mode **enabled** / Group Privacy **on** | 一般只有：`/` **命令**、**回复了机器人**的那条消息、正文里 **@了机器人用户名** 的消息 |
| **关闭** | Privacy mode **disabled** / Group Privacy **turn off** | 群内**普通文字**也会推给机器人（配合 Lite 里 `passive_qa` 才能实现「群里随便说一句就自动答」） |

**私聊**不受此项限制：用户给 Bot 发私信时，只要 `allow_pm` 为 true，照常会收到。

### 在 BotFather 里关闭群隐私（推荐：需要群内自动回复时）

1. 打开 Telegram，搜索并进入 **`@BotFather`**。
2. 发送 **`/mybots`**。
3. 在列表里**点选你的机器人**（不是 CommunityOS Lite 里填的名字，而是当时在 BotFather 创建的那个）。
4. 点 **`Bot Settings`**（机器人设置）。
5. 点 **`Group Privacy`**（群隐私）。
6. 选 **`Turn off`** / **Disable**，即**关闭**群隐私（让 Bot 能收到群内普通消息）。

改完后**不用**改 Lite 里的 token；若群聊仍无反应，可让群成员再发一条**新消息**试一次，或确认 Bot 仍在群内且未被禁言。

### 常见误区

- **「我开了 passive_qa 为什么群里还是不回？」**  
  若 Privacy 仍为**开启**，Telegram **根本不会把**普通群消息推给你的服务器，Lite 连消息都收不到。
- **「我只想被 @ 时才回答」**  
  保持 Privacy **开启**即可；用户 @ 机器人或发命令时仍会收到更新（可与产品策略搭配，Lite 当前群逻辑以「收到文本 + passive_qa」为主）。
- **超级群与普通群**  
  规则相同，路径都在 BotFather 的 **Group Privacy**。

### 安全提示

关闭群隐私后，Bot 会收到该群内**大量**用户消息，请注意：**不要**在日志/回复里泄露 token；生产环境仍建议 **仅本机**使用 Lite 管理端（见上文「安全与边界」）。

## 行为摘要

- **私聊**：默认 `allow_pm` 为 true 时回复文本消息。
- **群 / 超级群**：`modes.passive_qa` 为 true 时对文本消息自动应答（无需单独配群）；**若需普通群消息触发回复，必须按上文关闭 Telegram 的 Group Privacy**。
- **Telegram 群隐私（必看）**：新 Bot 默认 **Privacy 开启**。详见上一节 **《Telegram 群隐私教程》**。
- **知识库**：`knowledge.text` 非空时，runner 会把片段拼进用户问题前再调用 LLM。
- **发送**：`sendMessage` 使用纯文本，避免 Markdown 特殊字符导致失败。

## 与 CommunityOS（完整版）的区别

| Lite | 完整 CommunityOS（Harness） |
|------|---------------------------|
| 单进程 + JSON 配置 | `harness.yaml`、治理引擎、多 Bot 协作模板 |
| 无 CircuitBreaker / TokenBudget 等治理抽象 | 有 GovernanceEngine、角色模板脚本 |

需要脚手架、Harness、多角色协作时，改用 **`community-os`**（minimax-skills）里的 `init_community_os.py` / `start_harness.py` 流程。

## 排错

- **Bot 无回复**：确认 runner 已启动；`bots.json` 里 `enabled` 与 token；群聊是否关闭 `passive_qa`；**群聊是否仍开启 Group Privacy**（开启时未 @、非命令则 Telegram 不会下发普通消息）→ 见上文 **群隐私教程**。
- **返回「LLM API Key 未配置」**：在 Lite「LLM 配置」保存 key，或设置环境变量并与 `llm_config` 一致。
- **getUpdates 报错**：检查 token、网络、是否多实例共用一个 token 抢 offset。

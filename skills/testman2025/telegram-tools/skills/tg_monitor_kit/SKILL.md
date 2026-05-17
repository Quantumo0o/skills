---
name: tg_monitor_kit
description: Telegram Telethon 监控与群搜索；在项目根 pip install -e 后使用 tg-monitor 子命令；勿在对话中粘贴 API 密钥。
metadata: {"openclaw": {"requires": {"bins": ["python3"], "env": ["TELEGRAM_API_ID", "TELEGRAM_API_HASH"]}}}
---

# tg_monitor_kit

## When to use

- 用户需要运行 **关键词群监控**、**定时群搜索**、**从清单批量加群**，或 **排查 Telegram 登录/代理**（`groups`、`account-info`）。
- 需要提醒 **同一时刻只运行一个**占用 `xiaomei_session`（或 `TELEGRAM_SESSION_NAME`）的**长驻**进程，否则易出现 `database is locked`。

## Prerequisites

1. 本仓库根目录已配置 `.env`（由 `.env.example` 复制），包含 `TELEGRAM_API_ID`、`TELEGRAM_API_HASH`；会话文件位于项目根目录下的 `{session_name}.session`。
2. 已执行：`pip install -e .`（可选网页依赖：`pip install -e ".[web]"`）。
3. `{baseDir}` 指本 Skill 所在目录；**项目根**为包含 `pyproject.toml` 的仓库根（本 Skill 在仓库的 `skills/tg_monitor_kit/`，项目根为其上两级 `../../`）。

## Allowed commands（白名单）

在终端执行，将 `项目根` 换为实际路径：

```bash
cd 项目根
python3 -m tg_monitor_kit groups
python3 -m tg_monitor_kit account-info
python3 -m tg_monitor_kit members --group "群名称"
python3 -m tg_monitor_kit history --group "群名称" --limit 100
python3 -m tg_monitor_kit auth
python3 -m tg_monitor_kit login
python3 -m tg_monitor_kit monitor
python3 -m tg_monitor_kit search
python3 -m tg_monitor_kit join
python3 -m tg_monitor_kit join --once
```

或使用入口脚本（若已安装）：`tg-monitor groups` 等。

长驻进程：`monitor`（关键词监控）、`search`（群搜索定时）、`join`（清单批量加群定时）；**不要**与彼此或其它 Telethon 脚本并行。

## Secrets

- **禁止**在聊天中粘贴 `TELEGRAM_API_HASH`、短信验证码。验证码仅通过环境变量 `TG_CODE`、`TG_PHONE_CODE_HASH`（`login` 子命令）传入。
- OpenClaw 可在 `openclaw.json` 的 `skills.entries` 中为对应 skill 配置 `env` 注入（见官方文档）。

## Troubleshooting

- `database is locked`：关闭其它使用同一会话的 Python 进程，只保留一个长驻任务。
- 连接失败：检查代理 `TELEGRAM_PROXY_HTTP_HOST` / `TELEGRAM_PROXY_HTTP_PORT`。
- 将本目录同步到 OpenClaw workspace 的 `skills/` 或使用 `skills.load.extraDirs`（见 [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)）。

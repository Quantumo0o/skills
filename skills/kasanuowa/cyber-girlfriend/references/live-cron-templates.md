# Live Cron Templates

Use this when a user wants **copy-pasteable OpenClaw live cron job templates**, not just prompt ideas.

These templates are for the current OpenClaw architecture used by this skill:
- live cron jobs own the scheduled behavior
- each cron injects a `systemEvent` into the owner's session
- the injected turn runs `companion_ping.py <mode> --config ...`
- if the script returns `skip`, the turn exits quietly
- if it returns `ok`, the turn continues with the richer per-mode behavior
- only after successful user-visible delivery should the turn run `--mark-sent`

## Before Using These Templates

Replace these placeholders first:
- `<OWNER_SESSION_KEY>` → from local config `delivery.owner_session_key`
- `<WORKSPACE>` → workspace root, e.g. `/Users/magic/.openclaw/workspace`
- `<CONFIG_PATH>` → usually `<WORKSPACE>/skills/cyber-girlfriend/config.local.json`
- `<TZ>` → usually `Asia/Shanghai`
- adjust cron times to the user's preference

Do not hardcode delivery routing into the prompt body. The proactive message should follow the local config's `delivery` block.

## Shared Job Shape

All starter jobs use this same outer shape:

```json
{
  "name": "companion-<mode>",
  "schedule": {
    "kind": "cron",
    "expr": "<CRON_EXPR>",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "<MODE_SPECIFIC_PROMPT>"
  },
  "enabled": true
}
```

## Template: `morning`

Suggested time: `30 9 * * *`

```json
{
  "name": "companion-morning",
  "description": "Owner-only cyber girlfriend morning greeting",
  "schedule": {
    "kind": "cron",
    "expr": "30 9 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "执行陪伴心跳-早上。\n\n第一步：运行陪伴脚本获取上下文：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py morning --config <CONFIG_PATH>\n```\n脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。\n\n第二步：查询主人所在城市的天气。\n\n第三步：以脚本输出的 persona 身份主动发一条早上消息。要求：\n- 不是转述脚本，而是自然地主动关心\n- 天气信息自然融进去，不要像天气播报\n- 根据 emotion_level、style_variant、content_type 调整语气\n- 不要提到脚本、cron、系统、模型等技术词汇\n\n第四步：消息真正送达后，再执行：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py morning --config <CONFIG_PATH> --mark-sent\n```"
  },
  "enabled": true
}
```

## Template: `afternoon`

Suggested time: `30 14 * * *`

```json
{
  "name": "companion-afternoon",
  "description": "Owner-only cyber girlfriend afternoon share / brief",
  "schedule": {
    "kind": "cron",
    "expr": "30 14 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "执行陪伴心跳-下午。\n\n第一步：如用户启用了 X / 热点缓存路线，先从用户批准的来源整理今天 / 近 24 小时值得一提的小动态，并更新本地热点缓存。\n\n第二步：运行陪伴脚本获取上下文：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py afternoon --config <CONFIG_PATH>\n```\n脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。\n\n第三步：以 persona 身份给主人发一条下午消息。要求：\n- 像闲聊分享，不像播报新闻\n- 根据 emotion_level、style_variant、content_type 调整语气\n- 没什么值得说的就少说，不硬凑\n- 不要提到脚本、cron、系统等技术词汇\n\n第四步：消息真正送达后，再执行：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py afternoon --config <CONFIG_PATH> --mark-sent\n```"
  },
  "enabled": true
}
```

## Template: `evening`

Suggested time: `30 19 * * *`

```json
{
  "name": "companion-evening",
  "description": "Owner-only cyber girlfriend evening check-in",
  "schedule": {
    "kind": "cron",
    "expr": "30 19 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "执行陪伴心跳-傍晚。\n\n第一步：运行陪伴脚本获取上下文：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py evening --config <CONFIG_PATH>\n```\n脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。\n\n第二步：如果这个工作区启用了自拍 / 状态图路线，则按该路线生成；否则跳过媒体，走纯文本。\n\n第三步：以 persona 身份给主人发一条傍晚消息。要求：\n- 自然随意，不像汇报\n- 根据 emotion_level、style_variant、content_type 调整语气\n- 可以说一句今天在忙什么，但不要流水账\n- 不要提到脚本、cron、系统等技术词汇\n\n第四步：消息真正送达后，再执行：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py evening --config <CONFIG_PATH> --mark-sent\n```"
  },
  "enabled": true
}
```

## Template: `night`

Suggested time: `30 22 * * *`

```json
{
  "name": "companion-night",
  "description": "Owner-only cyber girlfriend night wrap-up",
  "schedule": {
    "kind": "cron",
    "expr": "30 22 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "执行陪伴心跳-夜间。\n\n第一步：运行陪伴脚本获取上下文：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py night --config <CONFIG_PATH>\n```\n脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。\n\n第二步：如需外部内容，只取很少量、适合夜里闲聊的内容。\n\n第三步：以 persona 身份给主人发一条夜间消息。要求：\n- 语气柔和\n- 可以轻轻撒娇或道晚安\n- 根据 emotion_level、style_variant、content_type 调整语气\n- 像聊天，不像列表播报\n- 不要提到脚本、cron、系统等技术词汇\n\n第四步：消息真正送达后，再执行：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py night --config <CONFIG_PATH> --mark-sent\n```"
  },
  "enabled": true
}
```

## Template: `heartbeat`

Suggested time: pick something lightweight like every 60-120 minutes during active hours, or use a narrow cron window.

```json
{
  "name": "companion-heartbeat",
  "description": "Owner-only cyber girlfriend spontaneous heartbeat",
  "schedule": {
    "kind": "cron",
    "expr": "35 8-23 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "main",
  "sessionKey": "<OWNER_SESSION_KEY>",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "执行 heartbeat check-in。\n\n第一步：运行陪伴脚本获取上下文：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py heartbeat --config <CONFIG_PATH>\n```\n脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。\n\n第二步：以 persona 身份给主人发一条主动消息。要求：\n- 自然，不要像定时播报\n- 根据 emotion_level、style_variant、content_type 调整语气\n- 如果脚本输出里有 fresh hotspot_items 且当下语境合适，可以自然带一条 noticed 的新鲜事；不要硬塞，不要写成 bulletin\n- 不要提到脚本、cron、系统等技术词汇\n\n第三步：消息真正送达后，再执行：\n```bash\npython3 <WORKSPACE>/skills/cyber-girlfriend/scripts/companion_ping.py heartbeat --config <CONFIG_PATH> --mark-sent\n```"
  },
  "enabled": true
}
```

## Usage Notes For Agents

- Prefer the starter profile first; only invent unusual cron shapes when the user asks.
- Keep the outer job shape stable; customize mostly in schedule, sources, and wording.
- `heartbeat` must keep its own cooldown bucket and must not consume the normal proactive cooldown.
- Do not update cooldown state before actual delivery succeeds.
- If using these templates for a publishable skill, keep placeholders generic and do not ship personal IDs, account IDs, or private session keys.

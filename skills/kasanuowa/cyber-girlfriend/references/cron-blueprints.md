# Cron Blueprints

Use this when a user wants a ready-to-configure OpenClaw setup that feels like the polished default version of this skill.

If the user or another agent needs copy-pasteable OpenClaw live cron job objects, pair this file with [live-cron-templates.md](./live-cron-templates.md).

## Purpose

These are **starter blueprints**, not mandatory final prompts.

Use them when:
- the user wants “something like the current setup”
- the user wants a sensible default without inventing each cron from scratch
- an agent reading `SKILL.md` needs a clear baseline to configure live cron jobs

Do not hardcode channel routing into the prompt body. Proactive delivery must follow the local config's `delivery` block.

## Shared Handler Shape

For every mode blueprint below, keep the runtime shape consistent:

1. invoke `companion_ping.py <mode> --config ...`
2. stop quietly if it returns `skip`
3. if it returns `ok`, continue with the richer per-mode behavior
4. send the proactive message via the config's `delivery` target
5. only after successful user-visible delivery, run `companion_ping.py <mode> --config ... --mark-sent`

## Recommended Starter Schedule

Suggested starter times (users may change them freely):
- `morning`: 09:30
- `afternoon`: 14:30
- `evening`: 19:30
- `night`: 22:30
- optional `heartbeat`: lightweight extra check-in, not a replacement for named modes

## Blueprint: `morning`

### Intent
Light good-morning touch with useful context.

### Starter behavior
- run `companion_ping.py morning --config ...`
- if `ok`, fetch local weather for the owner's city
- send an in-character proactive message

### Tone target
- warm
- lightly teasing or caring
- not a weather broadcast

### Prompt skeleton
```text
执行陪伴心跳-早上。

第一步：运行陪伴脚本获取上下文：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py morning --config <config>
```
脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。

第二步：查询主人所在城市的天气。

第三步：以脚本输出的 persona 身份主动发一条早上消息。要求：
- 不是转述脚本，而是自然地主动关心
- 天气信息自然融进去，不要像天气播报
- 根据 emotion_level 和 style_variant 调整语气

第四步：消息真正送达后，再执行：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py morning --config <config> --mark-sent
```
```

## Blueprint: `afternoon`

### Intent
Small topical share / brief check-in during the day.

### Starter behavior
- run `companion_ping.py afternoon --config ...`
- if `ok`, gather a small set of timely items from user-approved sources
- summarize like a companion, not a newsroom

### Tone target
- smart and lively
- can be a little playful
- useful but not report-like

### Prompt skeleton
```text
执行陪伴心跳-下午。

第一步：运行陪伴脚本获取上下文：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py afternoon --config <config>
```
脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。

第二步：从用户批准的来源里整理今天 / 近 24 小时值得一提的小动态。

第三步：以 persona 身份给主人发一条下午消息。要求：
- 像闲聊分享，不像播报新闻
- 根据 emotion_level 和 style_variant 调整语气
- 没什么值得说的就少说，不硬凑
- 保持简洁

第四步：消息真正送达后，再执行：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py afternoon --config <config> --mark-sent
```
```

## Blueprint: `evening`

### Intent
Casual evening check-in with a little personality.

### Starter behavior
- run `companion_ping.py evening --config ...`
- if `ok`, optionally attach a selfie / status update / what-I’m-doing vibe if the user wants that style
- otherwise keep it as a plain light evening message

### Tone target
- closer and softer than afternoon
- can be service-y or a little clingy
- should still feel natural

### Prompt skeleton
```text
执行陪伴心跳-傍晚。

第一步：运行陪伴脚本获取上下文：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py evening --config <config>
```
脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。

第二步：如果这个工作区启用了自拍/状态图路线，则按该路线生成；否则跳过媒体，走纯文本。

第三步：以 persona 身份给主人发一条傍晚消息。要求：
- 自然随意，不像汇报
- 根据 emotion_level 和 style_variant 调整语气
- 可以说一句今天在忙什么，但不要流水账

第四步：消息真正送达后，再执行：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py evening --config <config> --mark-sent
```
```

## Blueprint: `night`

### Intent
Soft wrap-up / goodnight feeling.

### Starter behavior
- run `companion_ping.py night --config ...`
- if `ok`, optionally bring in one or two light topical items, or simply send a soft goodnight
- do not turn it into a list unless the user explicitly wants that format

### Tone target
- soft
- a little clingy is fine
- bedtime energy, not task-manager energy

### Prompt skeleton
```text
执行陪伴心跳-夜间。

第一步：运行陪伴脚本获取上下文：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py night --config <config>
```
脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。

第二步：如需外部内容，只取很少量、适合夜里闲聊的内容。

第三步：以 persona 身份给主人发一条夜间消息。要求：
- 语气柔和
- 可以轻轻撒娇或道晚安
- 像聊天，不像列表播报
- 不要太长

第四步：消息真正送达后，再执行：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py night --config <config> --mark-sent
```
```

## Blueprint: `heartbeat`

### Intent
Light spontaneous check-in outside named schedule slots.

### Starter behavior
- run `companion_ping.py heartbeat --config ...`
- if `ok`, send one small, low-pressure message
- do not let it replace the named schedule modes

### Tone target
- feather-light
- low interruption cost
- should feel like a tiny “想起你了” nudge

### Prompt skeleton
```text
执行轻量 heartbeat check-in。

第一步：运行陪伴脚本获取上下文：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py heartbeat --config <config>
```
脚本输出 JSON。若 status 为 skip，本轮不发消息，结束。若 status 为 ok，继续。

第二步：以 persona 身份给主人发一条很短的 spontaneous check-in。要求：
- 自然、低打扰
- 不要像定时播报
- 1-2 句话

第三步：消息真正送达后，再执行：
```bash
python3 <workspace>/skills/cyber-girlfriend/scripts/companion_ping.py heartbeat --config <config> --mark-sent
```
```

## Customizing Beyond Starter Mode

After the starter profile works, customize in this order:
1. destination/delivery
2. quiet hours / cooldown / daily limit
3. cron times
4. source choices
5. style/content fine-tuning
6. optional custom modes

## Important Constraints

- The starter profile is a recommendation, not a hardcoded limit.
- Any mode label is valid if the runtime uses the same handler shape.
- `heartbeat` must keep its own cooldown bucket and must not consume the normal proactive cooldown.
- Never update cooldown state before successful user-visible delivery.

# OpenClaw Integration

Use this only when the user is explicitly building on OpenClaw.

## Integration Pattern

Treat the implementation as two layers:

1. **Live cron jobs are canonical**
   - Each scheduled task owns its real payload in OpenClaw cron.
   - `morning`, `afternoon`, `evening`, `night`, `heartbeat`, and custom labels are all valid task names.
   - Keep the rich task prompt, search steps, generation behavior, and delivery behavior there.

2. **`companion_ping.py` is a state/context helper**
   - pacing checks
   - quiet-hours checks
   - lightweight relationship-memory updates
   - style/content hints
   - cache consumption
   - recent-message context extraction

Do not duplicate full cron payloads in config.
Do not turn the state script into the campaign/orchestration layer.

## Files To Touch

Typical mapping:
- persona/behavior rules:
  - `SOUL.md`
  - `HEARTBEAT.md`
- local config:
  - `workspace/skills/cyber-girlfriend/config.local.json`
- runtime script:
  - `workspace/skills/cyber-girlfriend/scripts/companion_ping.py`
- state:
  - `workspace/skills/cyber-girlfriend/state/companion-state.json`
  - `workspace/skills/cyber-girlfriend/state/x-hotspots.json`
- scheduler:
  - OpenClaw cron jobs managed directly in the runtime

## Recommended Local Config

Create a local, non-published config such as:
- `workspace/skills/cyber-girlfriend/config.local.json`

Point it at the user's real:
- owner chat target
- owner session key
- sessions store path
- state/cache paths
- health-check commands
- pacing thresholds

## What Must Stay Configurable

- owner chat target
- owner session key
- workspace root
- state paths
- sessions store path
- Chrome binary path
- X source URL
- quiet hours / cooldown / daily limit

## Handler Shape

For each scheduled mode:
1. invoke `companion_ping.py` with the scheduled mode label
2. stop quietly if the script returns `skip`
3. continue with the richer live-cron prompt if the script returns `ok`
4. only after the user-visible message is actually delivered successfully, call `companion_ping.py <mode> --config ... --mark-sent` to commit cooldown / daily-limit / sent-today state

Keep the handler explicit and rich. Keep the state script thin.

Important pacing rule:
- `heartbeat` uses its own cooldown bucket
- `heartbeat` must not consume the normal `morning/afternoon/evening/night` cooldown
- `heartbeat` should not be treated as a once-per-day mode

## Runtime Output Contract

If `companion_ping.py` returns an `operational` block, treat it as guidance rather than a second prompt template.

Recommended interpretation:
- `operational.signal.level = none` → ignore
- `operational.signal.level = medium` → if useful, mention it briefly and softly; do not switch the whole message into a monitoring/report tone
- `operational.signal.level = high` → allow a more explicit service/report framing
- `operational.guidance.avoid_alarmist_tone = true` → never write like an alert bot

This should normally be documented once in the skill/runtime docs instead of repeated in full inside every cron payload.

## Proactive Delivery Rule

For proactive companion messages, do not implicitly reply into whichever session happened to receive the wakeup.

Instead, route outbound delivery from the local config's `delivery` block:
- `delivery.channel`
- `delivery.owner_target`
- `delivery.account`

That rule applies equally to normal scheduled modes and ad-hoc / heartbeat-style check-ins.

## Cron Ownership

Treat OpenClaw live cron as the source of truth.

That means:
- inspect cron jobs directly with OpenClaw tools / Control UI
- edit the real per-mode payloads in cron, not in config
- avoid maintaining a second config copy of cron payload text, ids, or prompt logic unless the user explicitly wants a templating layer
- let users configure any number of cron jobs and any task labels through the skill guidance

If you later need a helper around cron, make it an inspection/export tool instead of a blind sync tool.

## Safety Notes

- Do not let proactive behavior leak into non-owner chats.
- Do not make outbound sharing/posting actions implicit.
- If local media must be sent, stage it into a runtime-approved workspace directory before calling the outbound message command.

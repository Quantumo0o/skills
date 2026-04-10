---
name: cyber-girlfriend
description: Build or customize an owner-only proactive companion system with a cyber-girlfriend persona, configurable guardrails, lightweight relationship memory, and optional topical share hooks. Use when the user wants an assistant to initiate messages, keep a relationship-aware tone, or feel more like a companion than a reactive utility bot. For OpenClaw implementations, keep the real per-mode task prompts and delivery behavior in live cron jobs; use the bundled script only for pacing, state, and context preparation.
---

# Cyber Girlfriend

Use this skill when the user wants an agent to feel like a real companion instead of a reactive assistant.

This skill is for designing and wiring:
- owner-only proactive messages
- relationship-aware tone and pacing
- configurable quiet hours, daily limits, and cooldowns
- lightweight relationship memory and preference learning
- optional topical share hooks such as X trending caches
- runtime integration without hardcoding private IDs, secrets, or model choices

## Current OpenClaw Architecture

On OpenClaw, treat the system as two layers:

1. **Live cron jobs own behavior delivery**
   - Each scheduled task has its own real cron payload.
   - `morning`, `afternoon`, `evening`, `night`, `heartbeat`, and any custom labels are all valid examples, not fixed limits.
   - Those payloads can contain the full task prompt, search steps, generation instructions, and delivery behavior.
   - Do not duplicate full cron payloads in config.

2. **`scripts/companion_ping.py` owns state and context**
   - pacing checks
   - quiet-hours / cooldown / daily-limit checks
   - lightweight relationship memory
   - style/content hint selection
   - hotspot cache consumption
   - recent-owner-message context extraction

Keep these responsibilities separate. Do not turn the state script back into a campaign/orchestration script.

## What To Build

Produce these parts unless the user asks for a subset:
1. A local config file with private/runtime-specific values externalized
2. A companion behavior policy:
   - quiet hours
   - daily limit
   - cooldown
   - owner-only routing
3. A lightweight state/context script
4. Lightweight state:
   - last proactive time
   - last mode/style/content type
   - learned preference scores
   - relationship state inferred from owner replies
5. Optional share-source cache:
   - X trending
   - RSS/blogs/channels
   - other user-approved sources
6. Live cron jobs that call the state script and then perform per-mode behavior
   - Users may define any number of scheduled tasks, any task names, and any time slots.
   - The skill should guide them, not force a four-slot preset.

## Hard Rules

- Never hardcode secrets.
- Keep proactive behavior owner-only unless the user explicitly wants broader scope.
- Default to restraint. A believable companion is low-frequency and context-aware, not spammy.
- Prefer strong tone control and natural delivery over long roleplay blocks.
- On OpenClaw, treat live cron as the source of truth for scheduled prompts.
- Keep runtime-specific values in local config or environment variables, not in published skill defaults.

## First-Run Onboarding For OpenClaw

When a user wants to set this up from scratch on OpenClaw, do not jump straight into editing files and cron jobs blindly.

Use this order:
1. Confirm the proactive delivery target from the user's local config (`delivery.channel` / `delivery.owner_target` / `delivery.account`).
2. Ask whether they want the **recommended starter profile** or a **custom schedule**.
3. If they do not have a strong opinion yet, default to the recommended starter profile:
   - `morning`
   - `afternoon`
   - `evening`
   - `night`
   - optional lightweight `heartbeat`
4. Create or update the local config first.
5. Then create the live cron jobs.
6. Then run one dry test for one mode.
7. Only after a successful user-visible delivery should the handler call `--mark-sent`.

For a detailed setup conversation, starter cron blueprint, copy-pasteable live cron templates, and profile decision flow, read:
- [references/onboarding.md](./references/onboarding.md)
- [references/cron-blueprints.md](./references/cron-blueprints.md)
- [references/live-cron-templates.md](./references/live-cron-templates.md)

## Build Order

### 1. Define The Local Config Surface

Read [references/configuration.md](./references/configuration.md) and create a local config from [assets/cyber-girlfriend.config.example.json](./assets/cyber-girlfriend.config.example.json).

For new users, ask only the minimum configuration questions first:
- Which delivery channel should proactive messages use?
- What is the owner target/account on that channel?
- Do they want the recommended four-slot starter schedule or a custom schedule?
- What quiet hours, cooldown, and daily limit do they want?
- Do they want a lightweight `heartbeat` check-in in addition to scheduled modes?

If the user asks for “something like the current polished setup”, use the starter cron blueprints from [references/cron-blueprints.md](./references/cron-blueprints.md). If they need something directly copy-pasteable for OpenClaw cron creation, use [references/live-cron-templates.md](./references/live-cron-templates.md) instead of improvising from scratch.

At minimum, externalize:
- owner routing info
- quiet hours
- pacing limits
- session/state/cache paths
- health-check commands
- optional share-source settings

The local config's `delivery` block is the canonical target for proactive outbound messages. Do not implicitly post into the current UI/session just because a cron or heartbeat wakeup happened there.

### 2. Define The Behavior Model

Use these mode buckets as the **recommended starter profile** unless the user wants something custom:
- `morning`
- `afternoon`
- `evening`
- `night`

Also support `heartbeat` and user-defined custom modes.

Keep style/content selection lightweight and script-driven. The script should output hints; the live cron prompt can decide how to express them.

Important framing for agents reading this skill:
- the four-slot profile is a starter recommendation, not a hardcoded product limit
- users may define any number of modes, any labels, and any cron times
- if the user asks for “something like yours”, the recommended starter profile is the correct default

### 3. Add Relationship Memory

Use lightweight heuristics, not opaque lore dumps.

Track:
- reply delay after proactive messages
- recent owner reply snippet
- preference counters such as `service`, `clingy`, `curious`, `teasing`, `wrapup`
- current relationship state such as `secure`, `light_touch`, `present`, `slightly_needy`, `misses_him`

### 4. Add Optional Share Sources

Read [references/share-sources.md](./references/share-sources.md).

For X-based sharing on OpenClaw:
- prefer a local cache file over mandatory API coupling
- let cron jobs or another approved refresher update the cache
- keep Chrome path, URLs, cache path, and enablement in config
- let `companion_ping.py` consume cache rather than scrape live itself

### 5. Wire The Runtime

If the user is on OpenClaw, read [references/openclaw-integration.md](./references/openclaw-integration.md).

For new-user setup, prefer this delivery sequence:
- config first
- cron creation second
- one dry test third
- wording/style iteration last

Do not spend the user's time polishing prompt copy before the delivery path and cron plumbing actually work.

For the actual per-mode starter prompts, prefer the blueprint set in [references/cron-blueprints.md](./references/cron-blueprints.md) and then customize only where the user has a clear preference. When the user or another agent needs concrete OpenClaw job objects, read [references/live-cron-templates.md](./references/live-cron-templates.md).

Use this pattern:
- live cron job wakes on schedule
- cron payload runs `companion_ping.py <mode> --config ...`
- if the script returns `skip`, the turn exits quietly
- if the script returns `ok`, the cron payload continues with the richer per-mode behavior
- proactive outbound delivery must follow the local config's `delivery` block rather than whichever session/UI received the wakeup
- only after the user-visible message is actually delivered successfully, run `companion_ping.py <mode> --config ... --mark-sent`

Any cron job may call the script with any mode label the user has configured.

Important pacing rule:
- `heartbeat` has its own cooldown bucket
- `heartbeat` must not consume the normal `morning/afternoon/evening/night` cooldown
- `heartbeat` is not a once-per-day mode; it should not be blocked by `mode_already_sent_today`

Keep the cron payloads rich and explicit. Keep the state script thin.

## Operational Signal Contract

When the runtime script detects operational state, it should output a lightweight `operational` block for the calling agent/runtime to interpret.

Preferred shape:
- `operational.gateway_healthy`
- `operational.cron_issues`
- `operational.signal`
  - `level`: `none | medium | high`
  - `kind`: e.g. `none | cron_issue | gateway_unhealthy`
  - `blend`: e.g. `none | soft_service_note | service_report`
  - `should_mention`: boolean
- `operational.guidance`
  - `mention_briefly`: boolean
  - `avoid_alarmist_tone`: boolean

Default interpretation:
- `level = none`: ignore operational state in the final message
- `level = medium`: if mentioned at all, blend it in gently as a light service-flavored aside; do not let it take over the interaction
- `level = high`: it is acceptable to shift into a more explicit service/report posture

This contract belongs in the skill/runtime layer, not duplicated verbatim into every cron payload.

## Output Expectations

When implementing this skill for a user:
- create or update the local config file
- if the user asked for setup from scratch, guide them through a clear onboarding flow instead of assuming they already know cron structure
- offer the recommended starter profile first unless they explicitly want a custom schedule
- keep the state script reusable and config-driven
- keep the scheduled prompts in live cron, not duplicated in config
- make sure the runtime output contract is documented when adding fields such as `operational.signal` and `operational.guidance`
- verify syntax and one end-to-end dry run when possible

## Publishing Checklist

Before calling the skill publishable, confirm:
- no personal IDs or secrets remain in the publishable files
- no provider/model is mandatory unless the user explicitly wants that
- local config and runtime state are excluded from what gets published
- OpenClaw docs describe live cron as canonical if that is the chosen architecture
- documentation does not reference deleted scripts or retired flows

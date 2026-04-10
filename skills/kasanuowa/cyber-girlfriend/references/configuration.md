# Configuration

Use a single local config file. JSON is the simplest default.

## Required Sections

### `persona`

- `name`: in-character name
- `owner_nickname`: how the companion addresses the owner
- `tone`: short guidance string
- `relationship_style`: short guidance string
- `emoji`: optional

### `delivery`

- `channel`: e.g. `telegram`, `openclaw-weixin`
- `account`: optional account id
- `owner_target`: destination identifier for owner-only delivery
- `owner_session_key`: source session key used to resolve recent messages

### `schedule`

Keep only pacing policy here.

Recommended fields:
- `quiet_hours_start`
- `quiet_hours_end`
- `daily_limit`
- `cooldown_sec`

Optional custom pacing entries are allowed when the runtime actually consumes them.

Do **not** duplicate the full live-cron schedule/payload here when OpenClaw cron is the source of truth.

### `behavior`

Keep only values the runtime script actually consumes.

Recommended fields:
- `emotion_thresholds.present_sec`
- `emotion_thresholds.slightly_needy_sec`
- `emotion_thresholds.misses_him_sec`

Optional:
- `mode_profiles.<mode>.style_variants`
- `mode_profiles.<mode>.content_types`

Use these only when you want a custom cron mode to override the default style/content hints.

### `runtime`

Externalize runtime hooks here.

Suggested fields:
- `workspace_root`
- `sessions_store_path`
- `state_file`
- `healthcheck_command`
- `cron_jobs_file` — preferred local OpenClaw cron state file when available
- `jobs_list_command` — optional fallback CLI command only if no local cron state file is available

Only keep fields here that the runtime actually uses.

### `sources`

Optional source blocks.

Suggested X block:
- `enabled`
- `cache_path`
- `refresh_ttl_sec`
- `max_items`

## State Files

Recommended:
- `companion-state.json`
- `share-cache.json`

Track only behaviorally useful state:
- pacing
- last style/content type
- preference counters
- last owner reply metadata
- source cache timestamp

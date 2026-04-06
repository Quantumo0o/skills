---
name: token-stats-reporter
description: Generate and append accurate token/cost statistics in replies with a reproducible local algorithm (snapshot+incremental log aggregation + dedupe). Use when users ask for token usage, when channel policy requires token stats in every message, or when periodic reports need transparent model/cost attribution.
---

# Token Stats Reporter

Use this skill to produce a single, consistent token line at the end of every user-facing message.

## Workflow

1. Run the bundled reporter script:
   - `python3 /home/admin/.openclaw/workspace/skills/token-stats-reporter/scripts/token-show.py`
2. Append exactly one returned line to the end of the reply.
3. Do not modify numbers manually.

## Output format (exact)

`📊 Token: <in> in / <out> out | cacheRead: <cache> | 本次总消耗: <single_total> | 本次计费token: <single_billable> | 本月: <count> 次 | 月累计总消耗: <monthly_total> | 本次费用: <single_cost> | 本月费用: <monthly_cost> | 模型: <model>`

## Algorithm guarantees (must preserve)

- Data source: `~/.openclaw/agents/main/sessions/*.jsonl*`
- Valid rows only:
  - `type=message`
  - `message.role=assistant`
  - has text content
  - has `usage`
- Deduplication: by `message.id` (fallback composite key only if id missing)
- Monthly bucket: by message timestamp in local timezone (`Asia/Shanghai`)
- Aggregation strategy: snapshot + incremental replay
  - Persisted state file: `memory/token-agg-state.json`
  - Per-file offset tracking for incremental scans
  - Truncation/reset-safe fallback (`offset` reset when file shrinks)
- Cost source: `usage.cost.total`
- Model source: latest valid message `message.model`

## Reliability rules

- Run token collection immediately before final delivery.
- In long, multi-step tasks, refresh once again right before sending.
- Keep exactly one token line per outgoing message.
- If script fails, fallback to `session_status` and explicitly label as fallback.

## v1.2.0 Send Gate (fail-closed)

Use this mandatory gate to avoid hand-written token lines:

1. Build token line first (must run script):
   - `python3 /home/admin/.openclaw/workspace/skills/token-stats-reporter/scripts/token-show.py`
2. Validate token line before sending:
   - must contain `📊 Token:`
   - must contain `模型:`
   - model must NOT be `delivery-mirror`
3. Append token line to message body, then send.
4. If step 1 or 2 fails: **block sending** (do not handwrite numbers).
5. Allowed fallback text only when blocked:
   - `📊 Token: 统计暂不可用（脚本失败，已拦截手填）`

## Portability rule (for other assistants)

When installing on another assistant instance, use this skill's bundled script path as the source of truth. Do not depend on external ad-hoc scripts with unknown local modifications.

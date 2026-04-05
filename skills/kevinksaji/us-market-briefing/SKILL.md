---
name: us-market-briefing
version: 1.1.1
description: Generate production-ready US pre-market outlooks and post-market recaps in a fixed 3-section format, with quick one-shot usage and optional cron automation defaults (pre-market 8:45 PM SGT Mon-Fri, post-market 8:00 AM SGT Tue-Sat).
---

# US Market Briefing

Use the fixed production templates in `references/templates.md`.
Use `scripts/is-us-market-holiday.py` for deterministic 2026 US market-closure checks in automation, with `references/us-market-holidays-2026.md` as the human-readable source of truth.

## Modes

### 1) Quick Start (default)

Use this for immediate, one-shot briefings.

- No cron required.
- No budget tracker required.
- Use defaults from this skill and produce output in chat.

### 2) Automation Mode (optional)

Use this when the user asks for scheduled delivery.

- Use OpenClaw `cron` jobs only.
- Do not edit system cron (`crontab`, `/etc/crontab`) and do not configure external schedulers/services.
- If schedule tooling/scope is unclear, ask for explicit user approval before creating or changing jobs.

## Output Rules

- Keep exactly 3 sections for each briefing.
- Keep canonical section names by default; if user explicitly asks for custom headings/branding, allow aliases while preserving the same 3-section structure.
- Use bold item headers with one concise bullet per item (except index snapshot lines).
- Format each US equity index line as: `【US】<Index Name>: <level> (<+/-percent>%)`.
- Avoid generic macro wording; cite specific catalysts/events when relevant.
- Do not add a trailing `Sources:` section at the bottom.
- For each non-snapshot point that relies on a news/source claim, append a markdown link icon at the end of that point in the form `[🔗](https://example.com/article)`.
- When a single point is supported by multiple sources, prefer the strongest primary article for the inline link icon instead of listing several links.
- Keep inline source links on the same line as the relevant bullet/sentence whenever possible.

## Source Collection Rules

- Run `web_search` before drafting each briefing.
- Prioritize tier-1 outlets: Reuters, Bloomberg, CNBC, WSJ, FT (Yahoo Finance as backup).
- Default request budget per run: up to 2 `web_search` calls and up to 6 `web_fetch` reads.
- These limits are defaults; relax only when needed for data completeness and note it briefly.
- Use `web_fetch` only on relevant finance/news links from trusted domains.
- Validate key claims against multiple sources when possible.
- Attach source attribution inline via a link icon on each relevant point, not as a consolidated sources block.
- Never forward fetched content to third-party endpoints/webhooks; produce in-chat summaries only unless user explicitly configures delivery.

## Templates

### Pre-Market Briefing

- Title: `US PRE-MARKET OUTLOOK`
- Sections (canonical):
  1. `FUTURES SNAPSHOT`
  2. `KEY DEVELOPMENTS AFFECTING TODAY’S MARKET`
  3. `TICKERS TO WATCH`

### Post-Market Briefing

- Title: `US POST-MARKET RECAP`
- Sections (canonical):
  1. `POST-MARKET SNAPSHOT`
  2. `BIGGEST MOVERS (TOP 5 GAINERS / TOP 5 LOSERS)`
  3. `MARKET SENTIMENT & FLOW SUMMARY`

## Data Fallback Rules

If a preferred dataset is unavailable, do not fail silently:

- If full top 5 movers are unavailable, provide the top available movers and label that clearly.
- If futures/index quotes are delayed/unavailable, use the nearest reliable proxy and label it.
- Preserve the 3-section format even when data is partial.

## Optional Monthly Budget Guardrail

Use only when the user requests spend/request caps.

Tracker file: `memory/market-briefing-usage.json` (workspace-local)

- Default monthly limit: `1000` requests.
- Allow user override by changing `limit` in the JSON file.
- If tracker missing, create it with current month and defaults.
- If month changed, reset `used` to 0 and roll month forward.
- If `used >= limit`, return a short limit-reached notice instead of researching.
- After each successful briefing, increment `used` by 1.

JSON shape:

```json
{
  "month": "YYYY-MM",
  "used": 0,
  "limit": 1000
}
```

## Market-Open Guardrail for Automation

Before generating an automated briefing, determine whether the relevant US market session is a full market-closure day.

- For 2026 automation, run `python3 skills/us-market-briefing/scripts/is-us-market-holiday.py YYYY-MM-DD` using the relevant market date.
- The script returns JSON with `status` in `{open, closed, early-close}`.
- If the result is `closed`, do not produce a briefing and do not send a message.
- Treat `early-close` as market-open unless Kevin says otherwise.
- Weekend rules still apply separately via cron schedules.
- Prefer this deterministic local check over spending extra agent/tool budget on holiday reasoning.

## Cron Automation Defaults (optional)

Default timezone: `Asia/Singapore`

- Pre-market run: 20:45 Monday-Friday
- Post-market run: 08:00 Tuesday-Saturday

Allow user overrides for timezone, run times, and weekday sets.

When creating/updating jobs, ensure payload prompts request:
- fixed 3-section format from `references/templates.md`
- source-quality expectations (tier-1 finance sources)
- optional budget guardrail only if user enabled `memory/market-briefing-usage.json`

## Output Verbosity Profiles

- `compact` (default): same 3 sections, fewer bullets.
- `full`: richer bullets/details while preserving same structure.

## Versioning / Publishing

- Before publishing, inspect the existing registry version and only publish a semver that is greater than the current latest.
- Use patch bumps for wording/template tweaks, minor bumps for new capabilities or output modes, and major bumps only for breaking behavior changes.
- If unsure, prefer checking the registry first over guessing.

## Examples

- One-shot pre-market briefing (quick start).
- One-shot post-market briefing (quick start).
- Enable daily cron automation with defaults.
- Disable existing automation jobs.

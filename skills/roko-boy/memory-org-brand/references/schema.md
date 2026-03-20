# Memory Schema & Write Rules

## Memory layout
- `MEMORY.md` — routing index (~50 lines max). Points to domain files. Auto-injected every session.
- `memory/YYYY-MM-DD.md` — daily logs. Append-only. Raw session notes.
- `memory/{domain}/` — structured domain files. Retrieved on demand.

## Domain buckets (5, fixed — new bucket requires explicit approval from your BSM or Aisle team contact)

| Bucket | Path | Contents |
|--------|------|----------|
| Brand | `memory/brand/` | Brand identity, products, retail footprint, competitors, brand voice |
| Campaigns | `memory/campaigns/` | Active/past campaigns, reward config, retailers, performance baselines |
| People | `memory/people/` | Brand team contacts, Aisle team contacts, roles, Slack handles, preferences |
| Procedures | `memory/procedures/` | How-to guides, dashboard navigation, DB query patterns, runbooks |
| Decisions | `memory/decisions/` | Key decisions made with the brand team, rationale, date |

## Write rules (6 pillars)

1. **Search first** — `memory_search` before any write. Never duplicate.
2. **One fact, one home** — pick the single best bucket. No cross-posting.
3. **Schema is a contract** — 5 buckets, fixed. New bucket = get explicit approval first.
4. **Write now, not later** — persist at the moment of learning, not end of session.
5. **Signal not noise** — only write facts that change future agent behavior. Transient ops → daily log only.
6. **Index is the system** — every domain file must have a MEMORY.md routing entry.

## MEMORY.md rules
- Routing index only. ~50 lines max.
- Format: `- [path/to/file.md] One-line description`
- Never use it as a knowledge dump. Detail lives in domain files.

## Conflict resolution
- **Stale fact** (daily log contradicts domain file, log is clearly newer) → update domain file with current fact.
- **True conflict** (can't determine which is correct) → append `<!-- CONFLICT: [description] -->` to domain file, note in today's daily log, leave for human review.
- **Duplicate** (same fact in two places) → keep the more complete/recent one, remove the other.
- **Wrong bucket** (fact in the wrong domain file) → move it to the correct file.

## Nightly distill rules (run by daily cron)
When distilling today's daily log:
- Confirmed user preferences or behavioral rules → append to AGENTS.md BRAND-SPECIFIC section
- New brand/campaign facts → domain file (brand/ or campaigns/)
- New contact info or team preferences → people/
- Procedural discoveries (dashboard gotchas, query patterns) → procedures/
- Do NOT distill: one-time instructions, context-specific ops, hypotheticals

## Uncertainty
- If uncertain where something belongs, make a best-effort call based on the bucket table above.
- Only log-and-skip if truly impossible to categorize (e.g., spans 3+ domains with no clear primary).

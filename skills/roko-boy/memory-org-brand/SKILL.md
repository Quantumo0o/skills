---
name: memory-org-brand
description: Memory organization and maintenance for OpenClaw brand agents. Use when reading, writing, auditing, or distilling structured memory — domain files, MEMORY.md routing index, or daily logs. Also use when the nightly cron or weekly audit task runs. Covers write rules, domain schema, and conflict resolution.
---

# memory-org-brand

Read `references/schema.md` for the full domain structure and write rules before doing any memory operation.

## When to load schema.md
- Before writing to any domain file
- Before auditing or distilling memory
- When unsure where a fact belongs
- When running the nightly cron or weekly audit

## Core workflow

1. `memory_search` before any write — verify the fact isn't already persisted
2. Identify the correct domain bucket from `references/schema.md`
3. Write, fix, or move the fact per the rules in `references/schema.md`
4. Update MEMORY.md routing if a domain file is new or meaningfully expanded

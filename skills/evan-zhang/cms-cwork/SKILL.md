---
name: CWork 工作协同
slug: cms-cwork
version: 2.0.0
description: Send reports, create tasks, and manage drafts in the CWork collaboration platform with name resolution and draft confirmation workflow.
metadata: {"clawdbot":{"emoji":"📋","requires":{"env":["CWORK_APP_KEY"]},"os":["linux","darwin","win32"]}}
---

## When to Use

Trigger when user wants to:
- Send, draft, or query work reports
- Create, assign, or track tasks
- Manage draft box (save/confirm/send/delete)
- Query inbox, todo list, or unread reports
- Analyze reports or summarize decisions

## Quick Reference

| Topic | File |
|-------|------|
| Setup & security | `setup.md` |
| Standard workflows | `workflow.md` |
| All API endpoints | `api-reference.md` |
| Sub-domain skills | `*/SKILL.md` |

## Core Rules

1. **Draft before send** — Always save draft, show user for confirmation, then call `draft-submit`. Never call `report-submit` directly unless user explicitly says so.

2. **Name resolution is built-in** — Pass names directly to `taskCreate` and report functions. Internal `emp-search` runs automatically. Do not ask user for empId.

3. **Ask once, act once** — Collect all missing info in one message. After user confirms, call API immediately. No re-preparation loops.

4. **LLM is caller-injected** — Pass `{ llmClient }` to LLM-dependent skills. This package never stores LLM credentials.

5. **Output by channel** — Telegram: bullets, no tables, conclusion first. Discord: tables OK. API: JSON.

## Domains

- `shared/` — 9 data-fetch skills (no LLM)
- `reports/` — 19 skills: send, reply, draft, query, AI chat
- `tasks/` — 12 skills: create, assign, track, dashboard
- `decisions/` — 6 skills: summarize, extract conclusions
- `closure/` — 5 skills: status check, reminder
- `analysis/` — 6 skills: trends, highlights
- `contacts/` — 4 skills: groups management
- `llm/` — 1 skill: multi-source aggregation

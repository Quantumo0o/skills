# Workflow — CWork Skill Package

## Sending a Report (Standard Flow)

Always use draft → confirm → send. Never call `report-submit` directly.

1. `draftSave` — Save draft, get `draftId` + `reportId`
2. `draftDetail` — Fetch draft details, show to user for confirmation
3. Wait for user to confirm
4. `draftSubmit` — Convert draft to sent report (auto-cleans draft)

Exception: user explicitly says "send directly without confirmation".

## Creating a Task

Pass names directly — internal resolution handles the rest.

1. `taskCreate({ assignee: '张三', deadline: new Date('2026-04-14').getTime() })`
2. Internal: resolves name → empId via `emp-search` automatically
3. Multiple matches → shows candidates for user to choose

## AI Agent Rules (Anti-Loop)

- Prepare content: max 1 time
- Ask user: max 1 time, list ALL missing items at once
- After confirmation: call API immediately, no re-preparation
- Missing empId? Call `emp-search` first, don't ask user

## Output Format by Channel

- **Telegram**: Short bullet points, no tables, conclusion first, max 3 lines per point
- **Discord**: Tables and embeds OK
- **API**: Return structured JSON

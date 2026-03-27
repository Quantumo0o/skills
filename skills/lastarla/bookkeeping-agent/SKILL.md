---
name: bookkeeping
description: 导入账单、检查重复、查询交易、查看汇总，并通过本地 bookkeeping CLI 执行。
metadata: {"openclaw":{"homepage":"https://github.com/lastarla/bookkeeping-skill","requires":{"bins":["bookkeeping"]},"install":[{"id":"brew","kind":"brew","formula":"lastarla/tap/bookkeeping-tool","bins":["bookkeeping"],"label":"Install bookkeeping (Homebrew)"}]}}
---

# Bookkeeping

Use this skill only when `bookkeeping` is already available on `PATH`.

## Use this skill when

- You want to import a bill attachment or a local bill file
- You want to check whether a bill file was already imported
- You want to query transactions by time range, platform, direction, or category
- You want to view overview, trend, or category summaries
- You explicitly want to start the local bookkeeping dashboard
- You explicitly want to reset the database

Common high-confidence signals:

- File extension is `.csv` or `.xlsx`
- Filename includes `alipay`, `wx`, `wechat`, `bill`, `账单`, `交易`, or `流水`
- The user mentions `账单`, `流水`, `导入`, `支出`, `收入`, `支付宝`, or `微信`

## Do not use this skill when

- The task is generic Excel or CSV cleanup
- The task is about empty values, duplicate rows, or headers only
- The task is unrelated business analysis such as sales or inventory reports
- The input is an image, PDF, or archive that is outside the current supported scope

## Behavior rules

### Execute directly

Under high confidence, these lower-risk actions can be executed directly:

- Query transactions
- Run `summary overview`, `summary trend`, or `summary category`
- Inspect import batches
- Inspect duplicate imports

### Clarify or confirm first

Ask the minimum follow-up question first when:

- There is a single bill attachment but the request is vague, such as “处理一下”
- The user wants to import, but there are multiple likely bill attachments
- The user asks whether “this file” was imported, but the reference is unclear
- The user wants to start the dashboard, but has not clearly said to start the local service now

### Require strong confirmation

Never do these silently:

- `bookkeeping reset --yes`
- Resetting the database and then re-importing
- Batch processing multiple attachments

## Multiple attachment rules

- If there is exactly one high-confidence bill attachment, continue with that file
- If there are multiple high-confidence bill attachments, list the candidates and ask the user to confirm the scope
- Do not silently import all attachments by default
- In mixed-attachment scenarios, only include high-confidence bill candidates and explain what was excluded

## CLI mapping

Use the local `bookkeeping` CLI as the execution backend:

- Import: `bookkeeping import <file> --json`
- Query: `bookkeeping query --json`
- Overview summary: `bookkeeping summary overview --json`
- Trend summary: `bookkeeping summary trend --json`
- Category summary: `bookkeeping summary category --json`
- Batch inspection: `bookkeeping inspect batches --json`
- Duplicate inspection: `bookkeeping inspect duplicates --json`
- Dashboard: `bookkeeping serve`
- Reset: `bookkeeping reset --yes`

Prefer `--json` output whenever it is available.

## Response rules

- First state the recognized intent
- Then either state the next action or ask the smallest necessary question
- Avoid exposing raw CLI details unless the user is debugging setup issues
- If `bookkeeping` is missing, clearly say that this skill depends on the local CLI
- If the database is empty, ask the user to import bills before running query or summary tasks
- If the attachment type is unsupported, say that the skill currently supports only `.csv` and `.xlsx`

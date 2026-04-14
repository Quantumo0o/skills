---
name: arxiv-to-zotero
description: Search recent arXiv papers by topic and time range, dedupe against Zotero, and import only new matches with PDF attachments when possible.
version: 1.0.1
user-invocable: true
always: false
homepage: https://github.com/ucaspyx/arxiv-to-zotero
metadata: {"openclaw":{"emoji":"📚","skillKey":"arxiv-to-zotero","requires":{"env":["ZOTERO_API_KEY"],"bins":["python3","curl"]},"primaryEnv":"ZOTERO_API_KEY","compatibilities":["openclaw"]}}
---
# arXiv to Zotero

Use this skill when the user wants recent arXiv papers found and imported into Zotero.

## Setup

On first use, if `~/.openclaw/config/skills/arxiv-to-zotero.setup.json` is missing, read `{baseDir}/setup.md`, collect the required Zotero values, tell the user to put `ZOTERO_API_KEY` in `~/.openclaw/.env`, create the setup-state file, and resume the original request exactly once.

## Flow

1. If the user has not already given them, ask for:
   - the topic keywords or phrases
   - the time range
2. Do not ask the user to write an arXiv query.
3. If the user gives keywords in Chinese, first translate them into concise, technically accurate English search phrases before building the arXiv query. Use English for the actual arXiv query even when the user asked in Chinese.
4. Convert the user's request into one arXiv API `search_query` string yourself.
5. Run the script once:

```bash
python3 {baseDir}/scripts/main.py --config {baseDir}/config.json --query '<arXiv search_query>'
```

6. After the script finishes, use `result.user_message` as the final user-facing notification.

## Query rules

- Use official arXiv API fielded search syntax.
- The final arXiv query must be written in English. Do not pass Chinese keywords directly to arXiv.
- Use double quotes for multi-word phrases.
- If the user gives multiple alternative keywords or phrases, combine them with `OR`.
- When translating Chinese keywords, prefer standard English technical terms that are commonly used in paper titles and abstracts.
- Add the requested time range with `submittedDate:[YYYYMMDDTTTT TO YYYYMMDDTTTT]`.
- Pass the query as normal text. Do not URL-encode it yourself.

## Notes

- The skill imports only papers that are not already in Zotero.
- Before import, the script splits the final arXiv query into individual words, searches Zotero once per word, merges all returned top-level items into one cache, and then compares new arXiv papers against that cache.
- For each new parent item, the script first tries to download the PDF with `curl` and upload it to Zotero as a real file attachment.
- If Zotero returns HTTP 413 during upload authorization, that paper is attached as `linked_url`, and the rest of the current run stays in `linked_url` mode.
- Existing Zotero items are never modified.
- New Zotero parent items receive only the fixed skill tag from `zotero.default_tags`, and the script writes arXiv `comment` / `journal_ref` metadata into Zotero fields or `Extra` when available.

## When not to use

Do not use this skill for discussion-only requests, browsing help, or any task that should not write to Zotero.

## Network / Privacy

- Contacts: arXiv Atom API, arXiv PDF URLs, Zotero Web API
- Secret used: `ZOTERO_API_KEY`
- Writes: new Zotero parent items and child attachments only
- Does not modify existing Zotero items

## Natural-language trigger examples

- 帮我找近三年来 mamba 或者多模态用于股票预测的 arXiv 论文，并导入 Zotero。
- 帮我查最近两年 test-time adaptation 或 active search 用于组合优化的 arXiv 论文，去重后导入 Zotero。
- 帮我找近半年的 graph neural network 用于 TSP 或 vehicle routing 的 arXiv 论文，导入 Zotero。

# README.md

# arxiv-to-zotero

[中文说明 / Chinese version](README.zh-CN.md)

An OpenClaw skill for finding recent arXiv papers and importing only new matches into Zotero.

## What this skill does

This skill helps the agent:

1. collect a user's research topic keywords or phrases and a time range
2. build one valid arXiv `search_query` internally
3. search arXiv for recent papers
4. deduplicate against existing Zotero items
5. import only papers that are not already in Zotero
6. try to attach PDFs when possible
7. return one final user-facing summary

In short: **search recent arXiv papers, skip papers already in Zotero, and save only new ones.**

## Why use it

This skill is useful when you want a narrow and reliable workflow for literature collection:

- arXiv-only discovery source
- Zotero-first deduplication
- no modification of existing Zotero items
- automatic handling of common PDF attachment issues
- simple runtime requirements with no third-party Python packages

## Typical requests

Examples of natural-language requests the agent can handle:

- Find papers from the last three years on Mamba for stock prediction and import new ones into Zotero.
- Search recent papers on multimodal methods for stock prediction, deduplicate them against Zotero, and import only the new ones.
- Find recent arXiv papers on test-time adaptation and active search, then save only the papers I do not already have in Zotero.

## Quick start

### Requirements

- Python 3.10+
- `curl`
- Zotero Web API access via `ZOTERO_API_KEY`
- OpenClaw skill runtime

### First run

On first use, if the setup-state file is missing, the skill will:

1. read [`setup.md`](setup.md)
2. collect the required Zotero settings
3. write non-secret updates back into `config.json`
4. create the setup-state file
5. resume the original request once

## How the agent should use this skill

The intended interaction pattern is:

1. collect topic keywords or phrases
2. collect a time range
3. translate Chinese keywords into concise technical English when needed
4. build one valid English arXiv `search_query`
5. call the script once

Example:

```bash
python3 scripts/main.py --config ./config.json --query '(all:"Mamba" OR all:"state space model") AND (all:"stock prediction" OR all:"financial prediction" OR all:"market prediction" OR all:"price forecasting") AND submittedDate:[202304010000 TO 202604092359]'
```


------

```markdown

```

## Key behavior

### Discovery source

This skill uses **arXiv only** as the paper discovery source.

### Query language

The final arXiv query should be written in English.
If the user provides Chinese keywords, the agent should translate them before building the query.

### Deduplication

The skill builds a temporary Zotero cache by splitting the final arXiv query into individual words and searching Zotero once per word.
It then checks duplicates using:

- normalized exact title matching
- strict normalized title-prefix matching
- arXiv ID matching when available

Existing Zotero items are skipped and never modified.

### PDF attachments

For each newly imported Zotero parent item, the skill derives a PDF URL from the saved paper URL.

It first tries to upload the PDF as a real Zotero file attachment.
If Zotero returns `413 Request Entity Too Large`, the unfinished uploaded attachment is deleted, that paper is attached as `linked_url`, and later PDFs in the same run also switch to `linked_url` mode.

### Import cap

The skill stops creating new Zotero parent items after `import_policy.max_new_items` is reached.
The default cap is 50 new items per run.

## Runtime paths

- Default non-secret config: `./config.json` in the skill root directory
- Setup state: `~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- Secrets / environment: `~/.openclaw/.env`

## Repository structure

- [`SKILL.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SKILL.md): skill definition and runtime instructions
- [`setup.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/setup.md): first-run setup guidance
- [`SECURITY.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SECURITY.md): security, boundary, and risk notes
- [`scripts/main.py`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/scripts/main.py): main script implementation
- [`config.json`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/config.json): default non-secret configuration

## Security and privacy

This skill contacts:

- arXiv Atom API
- arXiv PDF URLs
- Zotero Web API

This skill:

- creates new Zotero items and attachments
- does not modify existing Zotero items
- uses `ZOTERO_API_KEY` for Zotero API access

For more detail, see [`SECURITY.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SECURITY.md).

## Notes

- The script expects one direct program invocation only.
- Do not use shell composition such as `&&`, `;`, pipes, or chained `cd` commands.
- The script URL-encodes the query parameter itself. Do not pre-encode spaces, quotes, or parentheses.

## About

OpenClaw skill for finding recent arXiv papers and importing new matches into Zotero.


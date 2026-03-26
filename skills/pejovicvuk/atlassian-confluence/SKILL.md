---
name: confluence
version: 1.0.0
description: Read and write Confluence Cloud pages — search, create, update, manage labels. Use when user mentions Confluence, wiki, documentation, pages, or knowledge base.
author: Viksi.ai
license: MIT
metadata:
  openclaw:
    emoji: "📄"
    requires:
      env: ["ATLASSIAN_URL", "ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN"]
      tools: ["curl", "python3"]
---

# Confluence Cloud

Read and write Confluence Cloud pages via a bash CLI wrapper. Uses the same Atlassian credentials as the Jira skill. No `jq` required — uses `python3` for JSON parsing.

Script location: `{baseDir}/confluence-cli.sh`

## Setup

Set these environment variables on your OpenClaw gateway:

- `ATLASSIAN_URL` — your Atlassian instance (e.g. `https://yourcompany.atlassian.net`)
- `ATLASSIAN_EMAIL` — the Atlassian account email
- `ATLASSIAN_API_TOKEN` — API token from [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

These are the same credentials as the Jira skill — one token covers both.

Make the script executable: `chmod +x {baseDir}/confluence-cli.sh`

## Commands

### List spaces

```bash
{baseDir}/confluence-cli.sh spaces
```

Returns: `[{ id, key, name, type, status }]`

Note: most commands use the space `id` (numeric), not the `key`.

### List pages in a space

```bash
{baseDir}/confluence-cli.sh pages 98312
{baseDir}/confluence-cli.sh pages 98312 50
```

Returns: `[{ id, title, status, parentId, authorId, created, url }]`

### Get page content

```bash
{baseDir}/confluence-cli.sh get 12345
```

Returns: `{ id, title, status, spaceId, parentId, version, body_text, body_html, created, url }`

`body_text` is HTML-stripped plain text (first 3000 chars). `body_html` is raw storage format (first 5000 chars).

### List child pages

```bash
{baseDir}/confluence-cli.sh children 12345
```

Returns: `[{ id, title, status, url }]`

### Search with CQL

```bash
{baseDir}/confluence-cli.sh search "space=ENG AND type=page AND title~\"architecture\""
{baseDir}/confluence-cli.sh search "label=runbook" 20
```

Common CQL patterns:
- Pages in a space: `space=ENG AND type=page`
- By title: `title~"deployment guide"`
- By label: `label=runbook`
- Recently modified: `lastModified > now("-7d")`
- By creator: `creator=currentUser() AND type=page`

Returns: `{ total, results: [{ id, title, type, space, url }] }`

### Create page

```bash
{baseDir}/confluence-cli.sh create --space 98312 --title "Deployment Runbook" --parent 12345 --body "<h2>Steps</h2><p>1. Pull latest main...</p>"
```

Required: `--space`, `--title`
Optional: `--parent` (page ID to nest under), `--body` (HTML storage format)

Returns: `{ id, title, url }`

### Update page

```bash
{baseDir}/confluence-cli.sh update 12345 --title "Updated Title" --body "<p>New content</p>"
```

The script auto-increments the version number.

Returns: `{ id, title, version, url }`

### Get page labels

```bash
{baseDir}/confluence-cli.sh labels 12345
```

Returns: `[{ name, prefix }]`

### Add labels

```bash
{baseDir}/confluence-cli.sh add-labels 12345 "runbook,production,v2"
```

Labels are comma-separated.

## Body Format

Confluence uses HTML "storage format" for page content:

- Paragraph: `<p>text</p>`
- Heading: `<h2>text</h2>`
- Table: `<table><tbody><tr><th>Header</th></tr><tr><td>Cell</td></tr></tbody></table>`
- Bold: `<strong>text</strong>`
- Link: `<a href="url">text</a>`
- Jira macro: `<ac:structured-macro ac:name="jira"><ac:parameter ac:name="key">PROJ-123</ac:parameter></ac:structured-macro>`

## Rules

- All output is JSON to stdout, errors to stderr.
- Never delete pages without explicit user confirmation.
- Always use `search` to find existing pages before creating duplicates.
- The `update` command auto-increments the version — don't worry about version numbers.

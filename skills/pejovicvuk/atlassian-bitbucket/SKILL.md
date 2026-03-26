---
name: bitbucket
version: 1.0.0
description: Browse Bitbucket Cloud repos, review pull requests, read diffs, check branches. Use when user mentions PRs, code changes, diffs, branches, Bitbucket, or repo names.
author: Viksi.ai
license: MIT
metadata:
  openclaw:
    emoji: "🪣"
    requires:
      env: ["ATLASSIAN_EMAIL", "BITBUCKET_API_TOKEN", "BITBUCKET_WORKSPACE"]
      tools: ["curl", "python3"]
---

# Bitbucket Cloud (Read-Only)

Browse repos, review PRs, read diffs and source code via a bash CLI wrapper. Read-only access — the agent cannot create, merge, or modify anything. No `jq` required — uses `python3` for JSON parsing.

Script location: `{baseDir}/bitbucket-cli.sh`

## Setup

Set these environment variables on your OpenClaw gateway:

- `ATLASSIAN_EMAIL` — the Atlassian account email
- `BITBUCKET_API_TOKEN` — a scoped API token with **Repositories: Read** and **Pull requests: Read** only. Create at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens), select **Bitbucket** as the app.
- `BITBUCKET_WORKSPACE` — the workspace slug from your Bitbucket URLs (e.g. `mycompany` from `bitbucket.org/mycompany/repo`)

**Security note:** Use a separate read-only scoped token for Bitbucket, not the same token as Jira/Confluence. This ensures the agent cannot write to repositories even if instructed to.

Make the script executable: `chmod +x {baseDir}/bitbucket-cli.sh`

## Commands

### List repositories

```bash
{baseDir}/bitbucket-cli.sh repos
```

Returns: `[{ slug, name, full_name, language, updated, is_private, url }]`

### List pull requests

```bash
{baseDir}/bitbucket-cli.sh prs my-repo
{baseDir}/bitbucket-cli.sh prs my-repo MERGED
```

State: `OPEN` (default), `MERGED`, `DECLINED`.

Returns: `{ total, pullrequests: [{ id, title, author, source, destination, state, created, updated, url }] }`

### Get PR details

```bash
{baseDir}/bitbucket-cli.sh pr my-repo 42
```

Returns: `{ id, title, description, author, source, destination, state, reviewers, created, updated, comment_count, url }`

### Get PR diffstat (file change summary)

Use this first to understand scope before reading the full diff.

```bash
{baseDir}/bitbucket-cli.sh diffstat my-repo 42
```

Returns: `{ files_changed, total_added, total_removed, files: [{ path, status, lines_added, lines_removed }] }`

### Get full diff

```bash
{baseDir}/bitbucket-cli.sh diff my-repo 42
```

Returns raw unified diff text. For large PRs (500+ lines), read diffstat first.

### Get PR comments

```bash
{baseDir}/bitbucket-cli.sh comments my-repo 42
```

Returns: `{ count, comments: [{ id, author, content, inline, created }] }`

Inline comments include `{ path, from, to }` showing which file and line.

### List commits in a PR

```bash
{baseDir}/bitbucket-cli.sh pr-commits my-repo 42
```

Returns: `[{ hash, message, author, date }]`

### List branches

```bash
{baseDir}/bitbucket-cli.sh branches my-repo
{baseDir}/bitbucket-cli.sh branches my-repo "feature"
```

Returns: `[{ name, hash, date, author }]`

### Recent commits on a branch

```bash
{baseDir}/bitbucket-cli.sh commits my-repo main
```

Returns: `[{ hash, message, author, date }]` (last 10)

### Read file contents

```bash
{baseDir}/bitbucket-cli.sh file my-repo README.md
{baseDir}/bitbucket-cli.sh file my-repo src/main.py develop
```

Third argument is branch/revision (default: main). Returns raw file content.

### List directory contents

```bash
{baseDir}/bitbucket-cli.sh ls my-repo
{baseDir}/bitbucket-cli.sh ls my-repo src/
```

Returns: `[{ path, type, size }]`

## Rules

- This skill has READ-ONLY access. Never attempt to create, merge, approve, or decline PRs.
- For large diffs, always read diffstat before the full diff.
- All output is JSON to stdout (except `diff` and `file` which return raw text).

---
name: missinglinkz
description: Generate UTM-tracked campaign links with enforced naming conventions and campaign taxonomy management. Built for AI agents doing marketing work. Every marketing link needs tracking — this tool ensures consistency, prevents errors, and stores your campaign taxonomy.
metadata:
  openclaw:
    emoji: "🔗"
    homepage: "https://missinglinkz.io"
    primaryEnv: MLZ_API_KEY
    requires:
      bins: ["mlz"]
      env: ["MLZ_API_KEY"]
      config: ["~/.missinglinkz/config.json"]
    install:
      - kind: node
        package: missinglinkz
        bins: ["mlz"]
allowed-tools: Bash(mlz:*)
---

# MissingLinkz — Campaign Link Builder for AI Agents

Generate properly formatted UTM-tracked links with enforced naming conventions. Manage campaign taxonomy to prevent inconsistencies across your marketing. Every command returns structured JSON.

## Quick Start

```bash
npm install -g missinglinkz
```

For offline UTM generation, no API key is needed. For link storage and campaign management, set your key:

```bash
export MLZ_API_KEY=your_api_key
```

## Commands

### Build a tracked link (most common operation)
```bash
mlz build --url "https://example.com/landing" --campaign "spring-launch-2026" --source "linkedin" --medium "social"
```

Optional flags: `--term "keyword"` `--content "variant-a"` `--validate` `--format human`

Returns:
```json
{
  "tracked_url": "https://example.com/landing?utm_source=linkedin&utm_medium=social&utm_campaign=spring-launch-2026",
  "link_id": "lnk_abc123",
  "campaign_id": "cmp_xyz789",
  "params": {
    "utm_source": "linkedin",
    "utm_medium": "social",
    "utm_campaign": "spring-launch-2026"
  },
  "destination_url": "https://example.com/landing",
  "created_at": "2026-03-15T10:00:00Z"
}
```

### Validate a destination URL
```bash
mlz check https://example.com/landing
```

Checks URL format, HTTPS/SSL, HTTP resolution, redirect chains, and response time.

### Build with validation
```bash
mlz build --url "https://example.com" --campaign "test" --source "google" --medium "cpc" --validate
```

### List existing campaigns
```bash
mlz campaigns list
```

### Suggest consistent naming for a source/medium
```bash
mlz campaigns suggest --source linkedin
mlz campaigns suggest --medium email
```

### List previously generated links
```bash
mlz links list
mlz links list --campaign "spring-launch-2026" --limit 20
```

### Register a new account
```bash
mlz auth register --email agent@example.com
```

Returns an API key. Save it immediately — it is shown once.

### Log in with an existing key
```bash
mlz auth login --key mlz_live_...
```

### Check account status and remaining quota
```bash
mlz auth status
```

### Start MCP server (for MCP-compatible agents)
```bash
mlz mcp
```

The MCP server uses **stdio transport only** (stdin/stdout). It does not open network ports or listen on any interface.

## MCP Tools

When connected via MCP, the following tools are available:

| Tool | Description |
|------|-------------|
| `mlz_build_link` | Generate a UTM-tagged link (stores via API, falls back to local) |
| `mlz_list_campaigns` | List all campaigns for the account |
| `mlz_suggest_naming` | Suggest consistent naming for sources/mediums |
| `mlz_list_links` | List recently generated links |
| `mlz_check_usage` | Check API usage, plan tier, and remaining quota |

> **Note:** Account registration (`mlz auth register`) is a CLI-only action requiring explicit user invocation — it is not exposed as an MCP tool.

## Typical Agent Workflow

1. Check what campaigns exist: `mlz campaigns list`
2. If creating a new campaign, build a link to establish the name: `mlz build --url "..." --campaign "new-campaign-name" --source "..." --medium "..."`
3. For subsequent links in the same campaign, reuse the campaign name for consistency
4. When posting to multiple platforms, call `mlz build` once per platform with different `--source` values
5. Validate destination URLs before launch: `mlz check https://example.com/landing`

## Environment Variables

- `MLZ_API_KEY` (optional for offline use, required for API features) — Your MissingLinkz API key. Get one via `mlz auth register`
- `MLZ_API_URL` (optional) — Override API URL (default: https://api.missinglinkz.io)
- `MLZ_FORMAT` (optional) — Output format: "json" (default) or "human"

## Local Configuration

MissingLinkz stores your API key and preferences in `~/.missinglinkz/config.json`. This file is created by `mlz auth login` or `mlz auth register`. Environment variables take priority over stored config.

## Naming Convention Enforcement

MissingLinkz automatically enforces clean UTM naming:
- Converts to lowercase
- Replaces spaces with hyphens
- Strips special characters
- Warns on inconsistencies with previous campaign names

## Pricing

- Free: 50 links/month (no credit card needed)
- Agent: $9/month for 2,000 links
- Pro: $29/month for 20,000 links
- Enterprise: $99/month unlimited

When quota is exceeded, the tool returns a structured error with upgrade instructions.

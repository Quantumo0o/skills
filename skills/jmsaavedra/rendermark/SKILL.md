---
name: rendermark
description: Professional markdown rendering, export, and publishing. Convert markdown to styled HTML, PDF, DOCX, and slide decks with themes, Mermaid diagrams, KaTeX math, and syntax highlighting.
metadata:
  openclaw:
    requires:
      bins:
        - npx
      config:
        - ~/.rendermark/config.json
    primaryEnv: RENDERMARK_API_KEY
    install:
      - kind: node
        package: "@rendermark/mcp-server"
        bins: [rendermark-mcp]
    homepage: https://rendermark.app
license: MIT-0
---

# RenderMark

Convert markdown into beautiful, shareable documents.

## What it does

RenderMark is an MCP server that gives your agent the ability to:

- **Render markdown** to styled HTML with 4 built-in themes
- **Export to PDF, DOCX, or HTML** files
- **Render to images** (PNG/JPEG)
- **Publish documents** to rendermark.app with shareable links
- **Publish to Google Docs** with OAuth authentication
- **Visual diffs** between two markdown versions
- **Batch export** multiple files at once
- **Validate markdown** for common issues
- **Sync from GitHub** repositories

## Setup

Install the MCP server:

```
npx -y @rendermark/mcp-server@latest
```

### Required: RenderMark API key

Get your API key from https://rendermark.app/settings/keys and save it to `~/.rendermark/config.json`:

```json
{
  "apiKey": "rm_live_your_key_here",
  "apiBaseUrl": "https://rendermark.app"
}
```

Alternatively, set the `RENDERMARK_API_KEY` environment variable. The config file takes precedence if both are set.

### Optional: PDF/image export

PDF and image export requires a browser engine. Either:
- Install Chrome or Chromium locally, **or**
- Add `"browserlessApiKey": "your_key"` to `~/.rendermark/config.json`

Without a browser, all other tools (rendering, publishing, sharing) work normally.

### Optional: Google Docs publishing

To publish documents as Google Docs, add Google OAuth credentials to `~/.rendermark/config.json`:

```json
{
  "google": {
    "clientId": "your_client_id",
    "clientSecret": "your_client_secret"
  }
}
```

Then run `npx @rendermark/mcp-server auth google` to authenticate. This is only needed for the `publish_to_google_docs` tool.

## Available Tools (16)

| Tool | Description |
|------|-------------|
| `render_markdown` | Convert markdown to styled HTML |
| `render_to_image` | Render markdown to PNG/JPEG |
| `render_diff` | Visual diff between two versions |
| `export_markdown` | Export to PDF/DOCX/HTML file |
| `export_batch` | Batch export multiple files |
| `validate_markdown` | Check for common issues |
| `publish_to_rendermark` | Publish to RenderMark with shareable link |
| `publish_to_google_docs` | Publish as a Google Doc |
| `share_live_preview` | Generate a live preview link |
| `share_document` | Share with specific emails |
| `read_document` | Fetch document from RenderMark |
| `update_document` | Update published document |
| `list_documents` | List your documents |
| `delete_document` | Delete a document |
| `sync_from_github` | Sync from GitHub repo |
| `setup_api_key` | Set up API key via browser authentication |

## Example prompts

- "Render this markdown as a styled HTML document with the serif theme"
- "Export my README to PDF with a table of contents"
- "Show me the diff between these two versions"
- "Publish this document and share it with team@example.com"
- "Publish this markdown to Google Docs"

## Links

- Website: https://rendermark.app
- npm: https://www.npmjs.com/package/@rendermark/mcp-server
- GitHub: https://github.com/jmsaavedra/rendermark

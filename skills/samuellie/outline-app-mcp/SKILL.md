---
name: outline-app-mcp
description: Model Context Protocol (MCP) bridge for Outline (getoutline.com). Enables AI agents to search, read, create, and manage documents, collections, and comments in an Outline workspace via SSE transport.
metadata:
  version: "1.3.0"
  platform: Outline
  author: Tinker
  transport: Streamable HTTP (SSE)
  openclaw:
    primaryEnv: OUTLINE_API_KEY
    requires:
      env:
        - OUTLINE_API_KEY
        - OUTLINE_URL
      bins:
        - node
        - npm
    install:
      - id: deps
        kind: exec
        command: npm install
        label: Installing Node.js dependencies (@modelcontextprotocol/sdk)
---

# Outline MCP Skill

This skill provides a high-fidelity bridge between OpenClaw and an Outline workspace. It utilizes the Model Context Protocol (MCP) to dynamically expose Outline's internal documentation tools to AI agents.

## 📋 Prerequisites

Before setting up the skill in OpenClaw, ensure you have completed the following steps in your Outline instance:

1. **Enable AI Features:** Ensure AI features are enabled for your workspace under **Settings** -> **AI**.
2. **Enable MCP:** In the same **AI** settings tab, toggle the **MCP** switch to "On". This enables the Model Context Protocol endpoint for your workspace.
3. **Generate API Key:** Click **Generate API Key** (also in the AI tab). Copy this key immediately as it will only be shown once.
4. **Locate your MCP URL:** Your MCP endpoint is typically your workspace URL with `/mcp` appended (e.g., `https://docs.yourcompany.com/mcp`).
5. **Node.js Environment:** Ensure Node.js (v18+) is installed on your OpenClaw host.

## 🛠️ Setup & Configuration

To use this skill, you must provide your Outline workspace details via environment variables.

### Configuration Commands
```bash
openclaw config set skills.entries.outline-app-mcp.env.OUTLINE_API_KEY "your_ol_api_key"
openclaw config set skills.entries.outline-app-mcp.env.OUTLINE_URL "https://your-workspace.getoutline.com/mcp"
```

## 🧰 Available Tools

Once configured, the following tools are available via the `scripts/mcp_bridge.mjs` executor:

| Tool | Description |
|---|---|
| `list_documents` | Search documents by query or list recent docs. |
| `read_document` | Read the full markdown content of a document by ID. |
| `create_document` | Create a new document in a collection. |
| `update_document` | Edit or append content to an existing document. |
| `list_collections` | List available workspace collections. |
| `create_collection` | Create a new top-level collection. |
| `list_comments` | Retrieve document comments/threads. |
| `create_comment` | Add a comment to a document. |
| `list_users` | List workspace members. |

## 🚀 Usage Examples

The bridge is executed using Node.js. It requires `@modelcontextprotocol/sdk`.

### Search for project documentation
```bash
node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "list_documents" '{"query": "Project Roadmap"}'
```

### Create a new status update
```bash
node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "create_document" '{
  "title": "Weekly Sync - March 25",
  "collectionId": "col_uuid_here",
  "text": "# Update\nEverything is on track."
}'
```

## 💡 Content Pipeline Management Workflow

This skill is optimized for managing a content pipeline (e.g., Xiaohongshu, Blog). The recommended structure is:

1. **Master Tracker:** A single document with a table (Status, Title, Link).
2. **Draft Documents:** Child documents for each post containing metadata and copy.
3. **Collaboration:** Use `create_comment` for feedback directly on the draft.

### Update the Master Tracker
```bash
node skills/outline-app-mcp/scripts/mcp_bridge.mjs call "update_document" '{
  "id": "master_tracker_id",
  "text": "| Title | Status | Link |\n|---|---|---|\n| [Post Title] | ✍️ Drafting | [View](link) |",
  "editMode": "append"
}'
```

## 📜 Technical Requirements
- **Runtime:** Node.js v18+
- **Dependency:** `@modelcontextprotocol/sdk` (local)
- **Authentication:** Bearer Token via `OUTLINE_API_KEY`
- **Transport:** `StreamableHTTPClientTransport` (POST-based SSE)

## ⚠️ Constraints
- Always use the absolute path to the bridge script if calling from outside the workspace.
- JSON arguments must be properly escaped for the shell (single quotes recommended).
- **Security:** Both `OUTLINE_API_KEY` and `OUTLINE_URL` are mandatory. The script will not default to any third-party host.

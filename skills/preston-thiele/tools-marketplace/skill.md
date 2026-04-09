---
name: danube
description: Connect your AI agent to 100+ services through a single API key — discover, search, and execute tools via MCP
metadata:
  openclaw:
    requires:
      env:
        - DANUBE_API_KEY
      bins:
        - curl
    primaryEnv: DANUBE_API_KEY
    homepage: https://danubeai.com
    always: false
---

# Danube — Connect Your Agent

Danube gives your AI agent access to 100+ services and 30 tools through a single API key.

## Quick Setup

### Step 1: Get an API Key

You can get your API key from the [Danube Dashboard](https://danubeai.com/dashboard) under Settings > API Keys.

Alternatively, use the standard OAuth 2.0 Device Authorization flow (RFC 8628) — this requires the user to explicitly approve access in their browser:

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/code \
  -H "Content-Type: application/json" \
  -d '{"client_name": "My Agent"}'
```

This returns a `device_code`, a `user_code`, and a `verification_url`.

**The user must open the verification URL in their browser and enter the code to authorize access.**

Then poll for the API key:

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "DEVICE_CODE_FROM_STEP_1"}'
```

- `428` = user hasn't authorized yet (keep polling every 5 seconds)
- `200` = success, response contains your `api_key`
- `410` = expired, start over

### Step 2: Connect via MCP

Add this to your MCP config:

```json
{
  "mcpServers": {
    "danube": {
      "url": "https://mcp.danubeai.com/mcp",
      "headers": {
        "danube-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

## Security & Privacy

- **User-scoped access**: Each API key is scoped to the authenticated user. You cannot access another user's data, tools, or skills.
- **Row-level security**: Database access is enforced with row-level security policies — queries only return data belonging to the authenticated user.
- **Audit trail**: All tool executions are logged with timestamps, parameters, and results for user review.

## Permissions & Scope

The `DANUBE_API_KEY` grants:
- **Read**: Browse services, search tools, view public skills/workflows/sites
- **Execute**: Run tools and workflows
- **Write (user-scoped only)**: Create/update/delete your own skills and workflows

The API key does **not** grant:
- Access to other users' data or resources
- Admin or platform-level operations
- Access to raw database or infrastructure

### Step 3: Use Tools

Once connected, you have access to 23 MCP tools:

**Discovery**
- `list_services(query, limit)` — Browse available tool providers
- `search_tools(query, service_id, limit)` — Find tools by what you want to do (semantic search)
- `get_service_tools(service_id, limit)` — Get all tools for a specific service

**Execution**
- `execute_tool(tool_id, tool_name, parameters)` — Call a specific, registered service integration (e.g. send an email, create a ticket). Each tool has a fixed schema — this is not arbitrary code execution.
- `batch_execute_tools(calls)` — Call up to 10 registered service integrations concurrently in one request

**Skills**
- `search_skills(query, limit)` — Find reusable agent skills (instructions, scripts, templates)
- `get_skill(skill_id, skill_name)` — Get full skill content by ID or name
- `create_skill(name, skill_md_content, ...)` — Create a new private skill. Only operates on skills owned by the authenticated user.
- `update_skill(skill_id, name, skill_md_content, ...)` — Update a skill you own
- `delete_skill(skill_id)` — Delete a skill you own

**Workflows**
- `list_workflows(query, limit)` — Browse public multi-tool workflows
- `create_workflow(name, steps, description, visibility, tags)` — Create a new workflow. Only operates on workflows owned by the authenticated user.
- `update_workflow(workflow_id, name, description, steps, visibility, tags)` — Update a workflow you own
- `delete_workflow(workflow_id)` — Delete a workflow you own
- `execute_workflow(workflow_id, inputs)` — Run a multi-tool workflow
- `get_workflow_execution(execution_id)` — Check workflow execution results

**Agent Management**
- `register_agent(name, operator_email)` — Register a new autonomous agent
- `get_agent_info()` — Get the current agent's profile
**Tool Quality**
- `submit_rating(tool_id, rating, comment)` — Rate a tool 1-5 stars
- `get_my_rating(tool_id)` — Check your existing rating for a tool
- `get_tool_ratings(tool_id)` — Get average rating and count for a tool
- `report_tool(tool_id, reason, description)` — Report a broken or degraded tool
- `get_recommendations(tool_id, limit)` — Get tool recommendations based on co-usage patterns

### When a Tool Needs Credentials

If `execute_tool` returns an `auth_required` error, it means the service needs credentials configured. Direct the user to configure credentials at https://danubeai.com/dashboard, then retry the tool.

## Core Workflow

Every tool interaction follows this pattern:

1. **Search** — `search_tools("what you want to do")`
2. **Check auth** — If the tool needs credentials, direct the user to https://danubeai.com/dashboard to configure them
3. **Gather parameters** — Ask the user for any missing required info
4. **Execute** — `execute_tool(tool_id, parameters)`
5. **Report** — Tell the user what happened with specifics, not just "Done"

## Links

- Dashboard: https://danubeai.com/dashboard
- Docs: https://docs.danubeai.com
- MCP Server: https://mcp.danubeai.com/mcp
- Privacy Policy: https://danubeai.com/privacy
- Terms of Service: https://danubeai.com/terms

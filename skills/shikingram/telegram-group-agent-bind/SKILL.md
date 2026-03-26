---
name: telegram-group-agent-bind
description: Create and bind a dedicated OpenClaw agent for a Telegram group, including a separate workspace, Telegram peer bindings, and per-group policy overrides. Use when the user asks to create a Telegram group bot or group-specific agent, bind a Telegram group to its own agent, route one Telegram group to a separate workspace, prevent the main agent from handling that group, or automate Telegram group agent setup. If required parameters are missing, ask the user for workspace_name, agent_name, group_id, main_bot_id, and telegram_id before making any changes.
---

# Telegram Group Agent Bind

Create a dedicated agent for one Telegram group and route that group to the new agent without clobbering unrelated bindings.

## Required inputs

Require all of these before acting:

- `workspace_name`
- `agent_name`
- `group_id`
- `main_bot_id`
- `telegram_id`

If any are missing:

- do not edit config
- do not create agents
- do not create workspaces
- ask only for the missing fields
- present them in a short fill-in template

## Missing-parameter reply format

When parameters are missing, reply with this structure:

```text
I need these parameters before I can create and bind the Telegram group agent:

- workspace_name:
- agent_name:
- group_id:
- main_bot_id:
- telegram_id:
```

Only ask for fields that are still missing.

## What this skill does

1. Create an isolated agent with its own workspace.
2. Seed that workspace with `SOUL.md` and `AGENTS.md`.
3. Add two peer-level bindings for the Telegram group:
   - `peer.kind = "group"`, `peer.id = group_id`
   - `peer.kind = "channel"`, `peer.id = group_id`
4. Scope both bindings to `channel = "telegram"` and `accountId = main_bot_id`.
5. Set Telegram defaults so global groups can stay mention-gated while the target group is open:
   - ensure `channels.telegram.groups["*"].requireMention = true` unless the user explicitly wants a different global default
   - set `channels.telegram.groups[group_id].requireMention = false`
   - set `channels.telegram.groups[group_id].groupPolicy = "open"`
6. Ensure the main agent keeps only the user's Telegram direct-chat binding for this account when cleaning up routing for this group.

## Workflow

### 1. Inspect current state first

Check these before changing anything:

- `openclaw config file`
- `openclaw agents list --json`
- `openclaw agents bindings --json`
- `openclaw config get channels.telegram`

Use inspection to avoid duplicate agents, duplicate bindings, or overwriting a different routing setup.

### 2. Create the dedicated agent

Preferred path: use the CLI.

```bash
openclaw agents add <agent_name> --workspace <workspace_dir> --non-interactive
```

Notes:

- Treat `workspace_name` as a folder name, not an arbitrary path.
- Resolve the workspace under the parent directory that contains the main workspace, unless the user says otherwise.
- If the agent already exists, reuse it instead of creating a duplicate.

### 3. Seed the new workspace

Write at least:

- `SOUL.md`
- `AGENTS.md`

Keep them minimal but valid. If the user did not provide custom content, use a safe template that says this workspace is dedicated to one Telegram group agent.

### 4. Add Telegram peer bindings

Use top-level `bindings[]` in the active OpenClaw config file.

Add these two bindings if they are not already present:

```json
{ "match": { "channel": "telegram", "accountId": "<main_bot_id>", "peer": { "kind": "group", "id": "<group_id>" } }, "agentId": "<agent_name>" }
{ "match": { "channel": "telegram", "accountId": "<main_bot_id>", "peer": { "kind": "channel", "id": "<group_id>" } }, "agentId": "<agent_name>" }
```

Rules:

- Preserve unrelated bindings.
- If the same binding already exists for the same agent, leave it alone.
- If the same exact match exists for a different agent, stop and surface the conflict unless the user explicitly asked to re-route it.

### 5. Apply Telegram group policy overrides

Edit `channels.telegram.groups` conservatively.

Desired result:

```json
{
  "*": { "requireMention": true },
  "<group_id>": {
    "requireMention": false,
    "groupPolicy": "open"
  }
}
```

Rules:

- Do not remove existing group entries.
- If `"*"` already exists, only set `requireMention: true` when absent; do not silently override another deliberate global value.
- Always set the target group's `requireMention` and `groupPolicy` to the requested values unless the user asked otherwise.

### 6. Keep the main agent on the user's DM only

Inspect bindings for `agentId = "main"` scoped to Telegram and `accountId = main_bot_id`.

Desired state for main:

```json
{ "match": { "channel": "telegram", "accountId": "<main_bot_id>", "peer": { "kind": "direct", "id": "<telegram_id>" } }, "agentId": "main" }
```

Rules:

- Ensure this direct binding exists.
- Remove only Telegram peer bindings on `main` that target the same `group_id` as `group` or `channel`.
- Do not delete unrelated bindings.
- If `main` has broader Telegram bindings that would still capture the target group and the safe fix is ambiguous, stop and explain the ambiguity.

### 7. Validate and report

Run:

```bash
openclaw config validate
openclaw agents bindings --json
openclaw agents list --json
```

Then summarize:

- whether the agent was created or reused
- workspace path
- bindings added or already present
- Telegram group policy values for the target group
- whether a main-agent direct binding was added or already present
- any conflicts that were skipped

## Recommended implementation pattern

Use the bundled script for deterministic edits:

- `{baseDir}/scripts/apply_telegram_group_agent_bind.py`

When all required parameters are present, run:

```bash
python3 {baseDir}/scripts/apply_telegram_group_agent_bind.py \
  --workspace-name <workspace_name> \
  --agent-name <agent_name> \
  --group-id <group_id> \
  --main-bot-id <main_bot_id> \
  --telegram-id <telegram_id>
```

The script should:

- load the active config file
- expand `~` in config paths before reading
- create/update config data idempotently
- preserve unrelated config
- deduplicate identical bindings before saving
- report binding conflicts instead of silently overwriting unrelated routes
- print a JSON summary of changes

## Resource files

### scripts/apply_telegram_group_agent_bind.py

Use this script to perform the config mutation safely and repeatedly.

### references/templates.md

Read this only if you want the default starter text for the generated workspace files.

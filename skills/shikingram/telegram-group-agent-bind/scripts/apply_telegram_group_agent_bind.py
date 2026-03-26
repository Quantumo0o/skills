#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_SOUL = """# SOUL.md

You are a dedicated Telegram group agent.

- Stay helpful and concise.
- Focus on the context of this group.
- Do not assume access to the main user's private context unless it is explicitly provided here.
- Keep group replies appropriate for a shared chat.
"""

DEFAULT_AGENTS = """# AGENTS.md

This workspace belongs to a Telegram-group-specific agent.

## Scope

- Treat this workspace as isolated from the main assistant workspace.
- Avoid leaking private context from other chats or agents.
- Prefer concise, useful replies in group settings.

## Memory

- Store only what is needed for this group's continuity.
- Do not assume main-session memory is available.

## Safety

- Do not perform destructive actions without asking.
- Do not send external messages outside the current group unless explicitly instructed.
"""


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def run_check(cmd):
    p = run(cmd)
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{p.stderr or p.stdout}")
    return p.stdout


def ensure_text(path: Path, content: str):
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        return "created"
    return "kept"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(backup)


def ensure_dict(parent, key):
    value = parent.get(key)
    if not isinstance(value, dict):
        value = {}
        parent[key] = value
    return value


def binding_key(binding):
    match = binding.get("match", {})
    peer = match.get("peer", {})
    return (
        match.get("channel"),
        match.get("accountId"),
        peer.get("kind"),
        str(peer.get("id")),
    )


def dedupe_bindings(bindings):
    seen = {}
    deduped = []
    duplicates = []
    for binding in bindings:
        if not isinstance(binding, dict):
            deduped.append(binding)
            continue
        key = binding_key(binding)
        if key in seen:
            duplicates.append(binding)
            continue
        seen[key] = binding
        deduped.append(binding)
    return deduped, duplicates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-name", required=True)
    ap.add_argument("--agent-name", required=True)
    ap.add_argument("--group-id", required=True)
    ap.add_argument("--main-bot-id", required=True)
    ap.add_argument("--telegram-id", required=True)
    ap.add_argument("--config", default=None)
    args = ap.parse_args()

    raw_config_path = args.config or run_check(["openclaw", "config", "file"]).strip()
    config_path = Path(raw_config_path).expanduser()
    if not config_path.exists():
        raise SystemExit(f"Config file not found: {config_path}")

    data = load_json(config_path)

    agents = ensure_dict(data, "agents")
    defaults = ensure_dict(agents, "defaults")
    base_workspace = Path(defaults.get("workspace", str(Path.home() / ".openclaw" / "workspace"))).expanduser()
    workspace_parent = base_workspace.parent
    target_workspace = workspace_parent / args.workspace_name

    summary = {
        "config": str(config_path),
        "workspace": str(target_workspace),
        "agent": args.agent_name,
        "createdAgent": False,
        "workspaceFiles": {},
        "bindingsAdded": [],
        "bindingsRemoved": [],
        "duplicateBindingsRemoved": [],
        "mainDirectBinding": None,
        "groupPolicy": {},
        "conflicts": [],
        "backup": None,
        "validated": False,
    }

    target_workspace.mkdir(parents=True, exist_ok=True)
    summary["workspaceFiles"]["SOUL.md"] = ensure_text(target_workspace / "SOUL.md", DEFAULT_SOUL)
    summary["workspaceFiles"]["AGENTS.md"] = ensure_text(target_workspace / "AGENTS.md", DEFAULT_AGENTS)

    existing_agents = json.loads(run_check(["openclaw", "agents", "list", "--json"]))
    if not any(a.get("id") == args.agent_name for a in existing_agents):
        add_cmd = [
            "openclaw",
            "agents",
            "add",
            args.agent_name,
            "--workspace",
            str(target_workspace),
            "--non-interactive",
        ]
        res = run(add_cmd)
        if res.returncode != 0:
            raise RuntimeError(res.stderr or res.stdout)
        summary["createdAgent"] = True

    bindings = data.get("bindings")
    if bindings is None:
        bindings = []
        data["bindings"] = bindings
    if not isinstance(bindings, list):
        raise RuntimeError("top-level bindings is not an array")

    desired = [
        {
            "match": {
                "channel": "telegram",
                "accountId": args.main_bot_id,
                "peer": {"kind": "group", "id": str(args.group_id)},
            },
            "agentId": args.agent_name,
        },
        {
            "match": {
                "channel": "telegram",
                "accountId": args.main_bot_id,
                "peer": {"kind": "channel", "id": str(args.group_id)},
            },
            "agentId": args.agent_name,
        },
    ]

    existing_map = {binding_key(b): b for b in bindings if isinstance(b, dict)}
    for b in desired:
        key = binding_key(b)
        existing = existing_map.get(key)
        if existing:
            if existing.get("agentId") != args.agent_name:
                summary["conflicts"].append({"type": "binding-conflict", "binding": existing})
            continue
        bindings.append(b)
        existing_map[key] = b
        summary["bindingsAdded"].append(b)

    main_direct = {
        "match": {
            "channel": "telegram",
            "accountId": args.main_bot_id,
            "peer": {"kind": "direct", "id": str(args.telegram_id)},
        },
        "agentId": "main",
    }
    main_direct_key = binding_key(main_direct)
    existing_map = {binding_key(b): b for b in bindings if isinstance(b, dict)}
    existing_direct = existing_map.get(main_direct_key)
    if existing_direct:
        if existing_direct.get("agentId") != "main":
            summary["conflicts"].append({"type": "main-direct-conflict", "binding": existing_direct})
            summary["mainDirectBinding"] = "conflict"
        else:
            summary["mainDirectBinding"] = "kept"
    else:
        bindings.append(main_direct)
        summary["mainDirectBinding"] = "added"
        summary["bindingsAdded"].append(main_direct)

    filtered = []
    for b in bindings:
        if not isinstance(b, dict):
            filtered.append(b)
            continue
        if b.get("agentId") != "main":
            filtered.append(b)
            continue
        match = b.get("match", {})
        peer = match.get("peer", {})
        if (
            match.get("channel") == "telegram"
            and match.get("accountId") == args.main_bot_id
            and peer.get("kind") in {"group", "channel"}
            and str(peer.get("id")) == str(args.group_id)
        ):
            summary["bindingsRemoved"].append(b)
            continue
        filtered.append(b)
    deduped, duplicates = dedupe_bindings(filtered)
    data["bindings"] = deduped
    summary["duplicateBindingsRemoved"] = duplicates

    channels = ensure_dict(data, "channels")
    telegram = ensure_dict(channels, "telegram")
    groups = ensure_dict(telegram, "groups")
    wildcard = ensure_dict(groups, "*")
    wildcard.setdefault("requireMention", True)
    group_entry = ensure_dict(groups, str(args.group_id))
    group_entry["requireMention"] = False
    group_entry["groupPolicy"] = "open"
    summary["groupPolicy"] = {
        "wildcardRequireMention": wildcard.get("requireMention"),
        "target": group_entry,
    }

    summary["backup"] = save_json(config_path, data)

    validate = run(["openclaw", "config", "validate"])
    if validate.returncode != 0:
        raise RuntimeError("config validate failed\n" + (validate.stderr or validate.stdout))
    summary["validated"] = True

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

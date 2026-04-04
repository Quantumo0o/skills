---
name: tradfri-lights
description: Control IKEA TRÅDFRI lights and groups through a local TRÅDFRI gateway using the native gateway API via node-tradfri-client. Use when the user wants to list IKEA lights or groups, turn a TRÅDFRI light or group on/off, adjust brightness, check what lights are on, find offline lights, or run safe whole-house TRÅDFRI actions on the same network.
---

# Tradfri Lights

Use this skill for local IKEA TRÅDFRI light control through an IKEA TRÅDFRI gateway.

## Quick start

- Use `scripts/tradfri.js` for actual gateway actions.
- Read `references/setup.md` before first use to configure the gateway host and credentials.
- Prefer exact light/group names, but the script also supports simple fuzzy matching.
- For surprising household actions, confirm first unless the user clearly asked for the action.

## Commands

Run commands from the skill folder or with an absolute path.

### Check connection

```bash
node scripts/tradfri.js status
```

### List lights

```bash
node scripts/tradfri.js list-devices
```

### List groups

```bash
node scripts/tradfri.js list-groups
```

### Show what is on

```bash
node scripts/tradfri.js whats-on
```

### Show offline lights

```bash
node scripts/tradfri.js offline
```

### Turn a light on or off

```bash
node scripts/tradfri.js light-off "Speelkamer 1"
node scripts/tradfri.js light-on "Speelkamer 1"
```

### Set brightness

```bash
node scripts/tradfri.js brightness "Speelkamer 1" 35
```

### Turn a group on or off

```bash
node scripts/tradfri.js group-off "Woonkamer"
node scripts/tradfri.js group-on "Woonkamer"
```

### Turn the main house groups all on or off

```bash
node scripts/tradfri.js all-on
node scripts/tradfri.js all-on _ 100
node scripts/tradfri.js all-off
```

Note: `SuperGroup` and `Instellen` are intentionally excluded from bulk actions.

## Operating rules

- Match exact names first; fall back to fuzzy/partial matching only when it yields one clear result.
- If multiple likely matches exist, show candidates and ask.
- If a target is offline (`alive: false`), say so explicitly instead of pretending the action succeeded.
- After changing a light or group, report the exact target used.
- Keep credentials out of normal chat replies.
- Use this skill for TRÅDFRI gateway control, not HomeKit scenes.
- Ask for confirmation before large household-wide actions unless the user clearly asked for them.

## Notes

- The tested route is `node-tradfri-client`, not `pytradfri`.
- The script reads config from `config.json`, with environment variables overriding it:
  - `TRADFRI_HOST`
  - `TRADFRI_IDENTITY`
  - `TRADFRI_PSK`
- The published version intentionally ships without working credentials; users must add their own local gateway details.
- If auth stops working, recreate credentials using the flow in `references/setup.md`.

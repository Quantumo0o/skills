---
name: gateway-restart
description: Reliably restart the OpenClaw gateway service. Use whenever the gateway needs to be restarted, reloaded, or restarted after config changes.
---

# Gateway Restart Skill

## The Problem

Multiple methods of restarting the gateway are unreliable and can leave the system in a broken state requiring manual rescue.

## The Solution

**Always use this command to restart the gateway:**

```bash
systemctl --user restart openclaw-gateway.service
```

## When to Use

- After modifying openclaw.json config
- When the gateway is unresponsive
- Any time a restart is needed

## What This Does

- Cleanly stops the current gateway process
- Starts a fresh gateway instance via systemd
- Properly handles port cleanup

## What NOT to Use

- `openclaw gateway restart` — unreliable, causes port conflicts
- `openclaw gateway stop` + `openclaw gateway start` — leaves orphaned processes
- `pkill openclaw` — too aggressive, can corrupt state

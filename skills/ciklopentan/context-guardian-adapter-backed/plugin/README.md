# OpenClaw External Adapter

This folder contains the external execution layer for `context-guardian`.
It is intentionally outside OpenClaw core.

## Recommended deployment

Use this plugin/wrapper pattern for `adapter-backed` mode:
- install the `context-guardian` skill from ClawHub
- keep durable continuity state in a host-configured persistent root
- invoke the adapter around major actions
- use explicit halt and resume entrypoints

## What is real now

- `plugin/context-guardian-adapter.js` is a working Node adapter CLI
- `plugin/openclaw-runtime-plugin/` is a native OpenClaw hook-only plugin package
- the plugin uses official OpenClaw hooks and calls the external adapter CLI
- the adapter writes durable state, summaries, snapshots, and event logs under the configured root
- the integration does not require an OpenClaw core patch

## Minimal smoke test

```bash
node plugin/context-guardian-adapter.js ensure --root /tmp/cg-root --task demo --session demo --goal "demo" --next-action "START"
node plugin/context-guardian-adapter.js status --root /tmp/cg-root --task demo
node plugin/context-guardian-adapter.js checkpoint --root /tmp/cg-root --task demo --phase run --next-action "Continue"
node plugin/context-guardian-adapter.js resume --root /tmp/cg-root --task demo
```

## Files

- `context-guardian-adapter.js` — working Node adapter CLI
- `test_context_guardian_adapter.js` — adapter tests
- `openclaw-runtime-plugin/` — native OpenClaw hook-only plugin package
- `openclaw.plugin.json.example` — manifest/config example
- `adapter-interface.md` — adapter callable surface
- `deployment-modes.md` — plugin vs wrapper vs sidecar comparison

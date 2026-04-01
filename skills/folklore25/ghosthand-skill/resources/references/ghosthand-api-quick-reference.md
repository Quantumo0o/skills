# Ghosthand API Quick Reference

This file is a compact route reference for the Ghosthand skill.

## Runtime and state

- `GET /ping` — basic service/version check
- `GET /health` — runtime readiness and listener state
- `GET /state` — runtime, accessibility, device, capability, and permission summary
- `GET /device` — device state only
- `GET /foreground` — current foreground app/activity
- `GET /commands` — machine-readable Ghosthand capability catalog

## UI inspection

- `GET /screen` — compact actionable surface; may report `partialOutput`, warnings, omission counts, and disclosure
- `GET /tree` — fuller accessibility tree; useful when `/screen` is shaped or partial
- `GET /focused` — currently focused node

## Interaction

- `POST /find` — selector lookup; supports `text`, `desc`, `id`, explicit strategies, `clickable`, and `index`
- `POST /click` — semantic click by `nodeId`, `text`, `desc`, or `id`
- `POST /tap` — coordinate tap
- `POST /input` — operate on focused editable field
- `POST /setText` — set text on a specific editable node by `nodeId`
- `POST /scroll` — semantic container scroll
- `POST /swipe` — coordinate swipe
- `POST /longpress` — coordinate long press
- `POST /gesture` — composite or named gesture
- `POST /launch` — package launch
- `POST /back`, `POST /home`, `POST /recents` — global navigation

## Sensing and transport

- `GET /screenshot` — screenshot retrieval when visual truth is needed
- `GET /wait` — wait for UI change and inspect settled state
- `POST /wait` — wait for a selector condition
- `GET /clipboard` / `POST /clipboard` — clipboard read/write
- `GET /notify` / `POST /notify` / `DELETE /notify` — notification read/post/cancel

## Rules that matter in practice

- Always treat `/commands` as the source of truth when you are unsure about route shape.
- `nodeId` is snapshot-scoped. Re-resolve after a fresh observation.
- `partialOutput=true` on `/screen` means the compact view omitted something. Escalate to `/tree` before making strong claims.
- `changed=false` from `GET /wait` is not proof that the prior action failed.
- Capability use depends on both system authorization and Ghosthand policy.
- Prefer `/click` before `/tap` when a stable selector exists.

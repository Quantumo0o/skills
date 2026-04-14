# Adapter Interface

This is the recommended external callable surface for OpenClaw-style hosts.
The package now includes a real Node adapter CLI at `plugin/context-guardian-adapter.js`.

## Commands

- `status` — inspect durable state and summary availability
- `ensure` — create initial durable state and summary when absent
- `checkpoint` — persist state + summary around one major action
- `bundle` — build the working bundle from durable inputs
- `halt` — write halt state and emit stop signal
- `resume` — load latest durable state and reconstruct next action

## Concrete CLI surface

```bash
node plugin/context-guardian-adapter.js status --root /var/lib/context-guardian --task task-1
node plugin/context-guardian-adapter.js ensure --root /var/lib/context-guardian --task task-1 --session session-1 --goal "Long-running task" --next-action "START"
node plugin/context-guardian-adapter.js checkpoint --root /var/lib/context-guardian --task task-1 --phase implementation --next-action "Run validation"
node plugin/context-guardian-adapter.js bundle --root /var/lib/context-guardian --task task-1 --system-instructions "Continue safely" --json
node plugin/context-guardian-adapter.js halt --root /var/lib/context-guardian --task task-1 --reason "critical pressure" --next-action "Wait for operator"
node plugin/context-guardian-adapter.js resume --root /var/lib/context-guardian --task task-1
```

## Hook mapping

- `before_major_action` -> `bundle`
- `after_major_action` -> `checkpoint`
- `after_state_mutation` -> `checkpoint`
- `before_destructive_action` -> `checkpoint`
- `on_failure` -> `checkpoint` + `halt` when required
- `on_resume` -> `resume`
- `on_stop_signal` -> `halt`

## Required semantics

Each command must use the same storage root and schema version.
Each command must be safe to call repeatedly.
Each command must be able to operate without modifying OpenClaw core.
The adapter stores durable state under the configured root instead of the skill package directory.

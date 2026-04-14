# Storage Layout

Use an upgrade-safe persistent root outside bundled runtime code.
The host configures the root path.

## Canonical layout

```text
<context-guardian-root>/
  config.yaml
  tasks/
    <task-id>.state.json
  summaries/
    <task-id>.summary.md
    latest-summary.md
  snapshots/
  logs/
  tests/
```

## Storage rules

- use atomic writes
- no dependency on transient prompt state
- no dependency on ephemeral container layer
- schema versioning
- safe migration path
- resumable from latest durable state
- stable root path configurable by host

## Path rules

- `tasks/` stores authoritative durable task state
- `summaries/` stores human-readable recovery summaries
- `summaries/latest-summary.md` is the stable alias for the newest summary
- `snapshots/` stores optional point-in-time captures
- `logs/` stores events and adapter logs
- `tests/` stores adapter smoke-test artifacts only when explicitly requested

## Deployment rules

- Prefer a host-mounted persistent volume in Docker deployments.
- Prefer a workspace-level persistent path on non-container hosts.
- Do not store state under the skill package directory if package upgrades may replace that directory.
- Do not store the only durable copy under temporary OS directories.

## Migration rule

When schema changes:
- keep `schema_version` in each state file
- migrate forward with explicit adapters or migration scripts
- keep the previous durable file until the new write succeeds
- never silently discard unreadable state

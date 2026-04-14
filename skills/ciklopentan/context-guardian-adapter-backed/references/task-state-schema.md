# Task State Schema

This is the canonical durable task-state shape for `adapter-backed` mode.

## Required top-level fields

- `schema_version` — string
- `task_id` — string
- `session_id` — string
- `goal` — string
- `status` — string
- `current_phase` — string
- `next_action` — string
- `completed_steps` — array of strings
- `open_issues` — array of strings
- `constraints` — array of strings
- `artifacts` — array of objects
- `state_confidence` — number in range `0.0` to `1.0`
- `updated_at` — ISO-8601 string

## Required artifact object fields

- `path` — string
- `kind` — string
- `description` — string

## Required semantic rules

- `schema_version` must be written on every durable state file.
- `next_action` must be non-empty for resumable in-progress tasks.
- `current_phase` must match the latest persisted plan state.
- `updated_at` must be refreshed on each successful state mutation.
- `artifacts` must point to durable files or important outputs, not guesses.

## Minimal valid example

See `references/persisted-task-state.example.json`.

# Best Practices

## Safety Rules

- Treat payment data, stored secrets, and OTP flows as sensitive.
- Do not echo raw stored-secret values unless disclosure is explicitly required
  for the active task.
- Use the narrowest data needed for the current step.
- If behavior is unclear, inspect the current intent state instead of guessing.

## Key-Scope Rules

- Use `GET /agent/me` when you need agent identity, scope, or limit context.
- `GET /agent/me` requires an agent-scoped key.
- `POST /intents` requires an agent-scoped key.
- Surface scope mismatches clearly rather than falling back to guessed behavior.

## Host and Metadata Rules

- Prefer canonical hostnames such as `booking.com`.
- Use subdomains like `secure.booking.com` when that is the real execution host.
- Keep `host` explicit in stored-secret metadata whenever possible.
- Preserve the exact required metadata keys for `stored_secret` flows.

## Legacy-Route Rules

The following routes are removed legacy surfaces and should not appear as active
capabilities:

- `GET /card`
- `GET /credentials`

If they return `404`, that is expected behavior rather than a new outage.

## Intent Handling Rules

- Treat `GET /intents/{id}` as the source of truth for current intent state.
- For stored-secret delivery, one successful read can complete the intent.
- Repeated reads after one-time secret delivery may return intent state without
  raw values.
- Approval and OTP state must come from the live intent, not from assumptions.

## Error-Handling Guidance

- `401` or `403` usually means invalid key, missing scope, or wrong auth context.
- `404` on removed legacy routes should not be treated as a supported flow.
- OTP confirmation failure means the secret may still be undisclosed.
- If the live API does not expose a capability, say so clearly instead of
  inventing a workaround.

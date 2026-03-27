---
name: magicpay
description: Create payment intents and request stored secrets through MagicPay. Use when an OpenClaw agent needs the live MagicPay HTTP API for payment, subscription, cancellation, limit checks, OTP confirmation, or one-time secret delivery.
---

# MagicPay

Use this skill for the live MagicPay HTTP API. Prefer the current
`/functions/v1/api` routes and ignore removed legacy card-delivery routes.

## API Configuration

- Base URL: `${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}`
- Auth header: `Authorization: Bearer $AGENTPAY_API_KEY`
- Content type: `application/json`

## Authentication and Key Scope

- `GET /agent/me` requires an agent-scoped API key.
- `POST /intents` requires an agent-scoped API key.
- `GET /intents`, `GET /intents/{id}`, and `GET /secrets/catalog` can be used
  with agent-scoped or user-scoped keys, subject to visibility rules.
- If auth or scope fails, surface the error instead of guessing.

## Use This Skill For

- payment intents
- subscription intents
- cancellation intents
- stored-secret catalog lookup and retrieval
- agent limit checks and intent status inspection

## References

- [Payment Flow](references/payment-flow.md): payment, subscription, and
  cancellation intents
- [Stored Secret Flow](references/stored-secret-flow.md): catalog lookup, OTP
  confirmation, and one-time delivery
- [Best Practices](references/best-practices.md): sensitivity, host handling,
  and legacy-route constraints

## Core Rules

- Do not use `GET /card`.
- Do not use `GET /credentials`.
- Treat `GET /intents/{id}` as the source of truth for current intent state.
- Do not promise card delivery through the API unless the live code adds a real
  route for it.
- Treat raw stored-secret values as sensitive and one-time.
- Use canonical hostnames for secret catalog lookup and stored-secret metadata.

## Workflow Selection

### Payment-like Task

1. If limits, identity, or scope matter, call `GET /agent/me` first.
2. Create the intent with `POST /intents` using `intent_type` of `payment`,
   `subscription`, or `cancellation`.
3. Read the current state through `GET /intents/{id}`.
4. Use `GET /intents` for history or filtered inventory views.

### Stored-Secret Task

1. Query `GET /secrets/catalog?host={host}` first.
2. Choose a matching secret by `kind`, `fields`, and applicability.
3. Create a `stored_secret` intent with `POST /intents`.
4. If the user provides an OTP, confirm it via
   `POST /intents/{id}/confirm-otp`.
5. Use `GET /intents/{id}` to retrieve the raw secret only when the intent is
   approved and ready.
6. Assume later reads may no longer contain raw values.

## Minimal curl Examples

### Agent Profile

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/agent/me"
```

### Payment Intent

```bash
curl -X POST \
  -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 19.99,
    "recipient": "OpenAI",
    "description": "Monthly API usage",
    "payment_type": "fiat",
    "intent_type": "payment",
    "category": "api",
    "metadata": { "project": "magicpay-skill" }
  }' \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents"
```

### Stored-Secret Catalog

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/secrets/catalog?host=booking.example"
```

### Stored-Secret Intent

```bash
curl -X POST \
  -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "intent_type": "stored_secret",
    "description": "Fill checkout secret",
    "metadata": {
      "secret_id": "11111111-1111-1111-1111-111111111111",
      "secret_kind": "login",
      "purpose": "checkout_fill",
      "host": "booking.example",
      "fill_ref": "fill_123",
      "requested_field_keys": ["username", "password"]
    }
  }' \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents"
```

### Confirm OTP

```bash
curl -X POST \
  -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}' \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents/INTENT_ID/confirm-otp"
```

## Warnings

- Legacy routes `GET /card` and `GET /credentials` were removed and should
  return `404`.
- Stored-secret raw values should not be printed, logged, or echoed unless the
  active task explicitly requires disclosure.
- If auth, scope, OTP, or approval state is unclear, inspect the current intent
  instead of inventing missing behavior.

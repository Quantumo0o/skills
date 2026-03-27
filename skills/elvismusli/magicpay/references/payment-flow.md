# Payment Flow

Use this reference for `payment`, `subscription`, and `cancellation` intents.

## Live Routes

- `GET /health`
- `GET /agent/me`
- `POST /intents`
- `GET /intents/{id}`
- `GET /intents`

Base URL:

`https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api`

## Scope Rules

- `GET /agent/me` requires an agent-scoped key.
- `POST /intents` requires an agent-scoped key.
- `GET /intents` and `GET /intents/{id}` work with agent-scoped or
  user-scoped keys, subject to visibility.

## Supported Intent Types

Payment-like types:

- `payment`
- `subscription`
- `cancellation`

Handled separately:

- `stored_secret`

## Recommended Execution Order

1. If the task depends on agent identity, limits, or readiness, call
   `GET /agent/me`.
2. Create a payment-like intent through `POST /intents`.
3. Read the created intent with `GET /intents/{id}` until the state is clear.
4. Use `GET /intents` when you need recent history or filtering context.

## Statuses to Expect

- `pending`
- `checking`
- `notify`
- `confirmation`
- `approved`
- `denied`
- `completed`
- `timed_out`

Treat `GET /intents/{id}` as the source of truth for current state. Do not
assume a card or secret will be returned just because an intent exists.

## Payment Categories

- `api`
- `compute`
- `saas`
- `data`
- `agent_to_agent`
- `other`

## Payment Types

- `crypto`
- `fiat`

## Minimal Payment Payload

```json
{
  "amount": 19.99,
  "recipient": "OpenAI",
  "description": "Monthly API usage",
  "payment_type": "fiat",
  "intent_type": "payment",
  "category": "api",
  "metadata": {
    "project": "magicpay-skill"
  }
}
```

## Example curl Commands

### Create Intent

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

### Read One Intent

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents/INTENT_ID"
```

### List Intents

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents?status=approved&intent_type=payment&limit=10"
```

## Constraints

- Do not document or call `GET /card`.
- Do not document or call `GET /credentials`.
- Do not invent a card-delivery endpoint if the current API does not expose one.
- If the task requires card data but the live API does not provide it, say so
  clearly instead of guessing.

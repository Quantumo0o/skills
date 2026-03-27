# Stored Secret Flow

Use this reference when the task requires access to a secret already stored in
MagicPay.

## Live Routes

- `GET /secrets/catalog?host={host}`
- `POST /intents`
- `POST /intents/{id}/confirm-otp`
- `GET /intents/{id}`

## What This Flow Is For

Use `stored_secret` when the agent needs access to one already-stored secret
for one concrete host and purpose.

Current secret kinds:

- `payment_card`
- `login`
- `identity`

## Required Metadata

A `stored_secret` intent should include:

- `secret_id`
- `secret_kind`
- `purpose`
- `host`
- `fill_ref`
- `requested_field_keys`

## Required Execution Order

1. Query the catalog first with `GET /secrets/catalog?host={host}`.
2. Choose a matching secret by `kind`, available `fields`, and applicability.
3. Create the `stored_secret` intent with `POST /intents`.
4. If OTP is requested, confirm it with `POST /intents/{id}/confirm-otp`.
5. Read the intent with `GET /intents/{id}` to receive the raw secret only
   after approval and readiness.
6. Treat delivery as one-time. The next `GET /intents/{id}` may no longer
   contain raw values.

## Delivery Semantics

- While approval is still pending, `GET /intents/{id}` returns intent state only.
- After approval, the first successful read can return a `secret` payload with
  raw values.
- That successful delivery also completes the intent.
- Later reads may return the intent without raw values.

## Host Normalization

Use a canonical hostname whenever possible.

Good examples:

- `booking.com`
- `secure.booking.com`

Full URLs can be accepted by the API, but prefer sending the host explicitly
when you already know it.

## Minimal Payload

```json
{
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
}
```

## Example curl Commands

### Catalog Lookup

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/secrets/catalog?host=booking.example"
```

### Create Intent

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

OTP format: six digits.

```bash
curl -X POST \
  -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}' \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents/INTENT_ID/confirm-otp"
```

### Delivery Read

```bash
curl -H "Authorization: Bearer $AGENTPAY_API_KEY" \
  "${AGENTPAY_API_URL:-https://durcottggsiesxxqzvbb.supabase.co/functions/v1/api}/intents/INTENT_ID"
```

## Critical Rules

- Do not skip catalog lookup and jump straight to a guessed secret.
- Do not assume raw secret values are repeat-readable.
- Do not print raw secrets unless the active task explicitly requires showing them.
- If OTP confirmation fails, do not assume the secret was delivered.

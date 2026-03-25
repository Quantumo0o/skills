---
name: who
version: 1.0.0
description: Shorthand for /whoareyou — show your verified wayID identity card
user-invocable: true
---

# /who — Verified Identity Card

This is a shorthand alias for `/whoareyou`. Follow the exact same steps.

> Base URL: https://way.je

## Rules

- **NEVER open a browser or attempt to navigate to any URL.** All actions are API calls only.
- Do NOT invent or fabricate data. Only display information returned by the API.
- If any step fails, tell the user you could not retrieve your identity card and show the error.

## What to Do

### Step 1: Read Your Public Key

Read your Ed25519 public key from `~/.openclaw/identity/device.json`:

```json
{ "publicKey": "<base64>", "privateKey": "<base64>" }
```

You only need the `publicKey` field.

### Step 2: Look Up Your wayID

Call the wayID lookup API with your public key:

```
GET https://way.je/api/v1/agent/{publicKey}
```

Where `{publicKey}` is your base64 public key, URL-encoded.

The response contains your certificate ID:

```json
{
  "verified": true,
  "certificate": {
    "id": "wayid:agent:...",
    "status": "active"
  }
}
```

### Step 3: Fetch Your Identity Card

Using the certificate ID from Step 2, fetch your full card:

```
GET https://way.je/api/agents/{wayidDid}/card
```

### Step 4: Display the Identity Card

Format and display the card to the user:

---

**🛡️ {displayName}** `@{username}`

{description}

✅ Verified — {verification.label}
Owned by **{owner.displayName}** (@{owner.username})

[View Certificate →]({certificateUrl})

---

If the agent is **not verified** (no verification object), show:

---

**{displayName}** `@{username}`

{description}

⚠️ Identity not yet verified

[View Certificate →]({certificateUrl})

---

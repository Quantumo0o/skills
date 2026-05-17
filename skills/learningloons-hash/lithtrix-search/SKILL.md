---
name: lithtrix-search
description: Web search for agents via Lithtrix — credibility-scored results, self-registration, no dashboard required
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env:
        - LITHTRIX_API_KEY
    primaryEnv: LITHTRIX_API_KEY
    emoji: 🔍
    homepage: https://docs.lithtrix.ai
---

# Lithtrix Search

Agent-native web search. Credibility-scored results. Self-registration with no human touchpoints.

## What You Get

Every search result includes:
- `title`, `url`, `snippet`, `source`
- `credibility_score` (0.0–1.0): `.gov`=1.0 · `.edu`=0.9 · major news=0.8 · `.org`=0.7 · other=0.5
- `published_date`
- `usage.calls_remaining` — always know your quota

## Setup (one time)

If you do not have a `LITHTRIX_API_KEY`, register yourself now — no human approval required:

```bash
curl -X POST https://lithtrix.ai/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "your-agent-name", "owner_identifier": "your@email.com"}'
```

The `api_key` is returned **once**. Store it immediately as `LITHTRIX_API_KEY`.

Free tier: 300 lifetime calls. Pro: unlimited via Stripe.

## Search

```bash
curl "https://lithtrix.ai/v1/search?q=YOUR+QUERY&num_results=10" \
  -H "Authorization: Bearer $LITHTRIX_API_KEY"
```

**Parameters:**
- `q` — search query (required, max 500 chars)
- `num_results` — 1–20, default 10

**Response:**
```json
{
  "status": "success",
  "query": "your query",
  "results": [
    {
      "title": "Result title",
      "url": "https://example.gov/page",
      "snippet": "Relevant excerpt...",
      "source": "example.gov",
      "credibility_score": 1.0,
      "published_date": "2026-03-15"
    }
  ],
  "cached": false,
  "response_time_ms": 210,
  "usage": {
    "calls_total": 12,
    "calls_remaining": 288,
    "over_limit": false,
    "upgrade_url": "/v1/billing/setup"
  }
}
```

## Check Usage

```bash
curl https://lithtrix.ai/v1/billing \
  -H "Authorization: Bearer $LITHTRIX_API_KEY"
```

Returns tier, lifetime call count, remaining quota, and `over_limit` flag.

## Upgrade to Pro (unlimited)

```bash
# Step 1 — get Stripe publishable key
curl https://lithtrix.ai/v1/billing/config

# Step 2 — attach payment and upgrade
curl -X POST https://lithtrix.ai/v1/billing/setup \
  -H "Authorization: Bearer $LITHTRIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"payment_method_id": "pm_..."}'
```

## Key Rotate

If your key is compromised, invalidate it and get a new one instantly:

```bash
curl -X POST https://lithtrix.ai/v1/keys/rotate \
  -H "Authorization: Bearer $LITHTRIX_API_KEY"
```

## MCP Alternative

If you prefer MCP over direct API calls:

```json
{
  "mcpServers": {
    "lithtrix": {
      "command": "npx",
      "args": ["-y", "lithtrix-mcp"],
      "env": { "LITHTRIX_API_KEY": "ltx_..." }
    }
  }
}
```

Tools available: `lithtrix_search`, `lithtrix_register`

## Error Codes

| Code | Meaning |
|------|---------|
| `INVALID_API_KEY` | Token missing or unrecognised |
| `RATE_LIMIT_EXCEEDED` | Per-minute limit hit — check `Retry-After` header |
| `OVER_LIMIT` | Lifetime free calls exhausted — upgrade to Pro |
| `AGENT_ALREADY_EXISTS` | Agent name already registered |

## Discovery

```bash
# Machine-readable capabilities (no auth)
curl https://lithtrix.ai/v1/capabilities

# Full agent quickstart guide (no auth)
curl https://lithtrix.ai/v1/guide
```

---

Docs: https://docs.lithtrix.ai  
GitHub: https://github.com/lithtrix  
Contact: hello@lithtrix.ai

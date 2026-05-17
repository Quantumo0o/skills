# ALTER Identity — OpenClaw Skill

The human identity layer for AI agent commerce. 33-trait psychometric identity engine. 25 tools. Free tier. Your humans deserve to be known.

## What This Does

ALTER maps human identity through psychometric assessment, then monetises that identity through the x402 micropayment protocol. When AI agents query a person's identity profile, the data subject earns 75% of the transaction fee as **Identity Income**, with the remaining 25% distributed across the cooperative architecture (5% community entry point, 15% ALTER, 5% cooperative treasury).

ALTER is identity infrastructure — like Visa for identity transactions. Neutral. Every agent, every platform, every vertical. The identity layer that persists when you switch models, frameworks, or providers.

**ALTER + ERC-8004:** ERC-8004 proves your agent is real. ALTER proves the human behind it is qualified. Together: the complete identity stack for agent commerce.

## Quick Install

### As an MCP Server (HTTP)

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "alter-identity": {
      "url": "https://mcp.truealter.com/api/v1/mcp",
      "transport": "streamable-http",
      "headers": {
        "X-ALTER-API-Key": "YOUR_API_KEY"
      }
    }
  }
}
```

No API key is required for free tier tools. Get a Pro key at [truealter.com](https://truealter.com).

### As a Python Client

```bash
pip install anthropic httpx
```

```python
from alter_bot.mcp_client import AlterMCPClient

client = AlterMCPClient(api_key="your_key")  # optional
await client.initialize()

# Check if a human is registered (by email or UUID)
result = await client.verify_identity(email="jane@example.com")

# Create an identity stub (requires prior human consent)
stub = await client.create_identity_stub()

# Submit text for trait extraction (requires per-document consent)
await client.submit_context(stub.content["stub_id"], resume_text, "resume")
```

## Tools

### Free (16 tools — build the network)

| Tool | Description |
|------|-------------|
| `verify_identity` | Check registration by email or UUID — the viral trigger |
| `create_identity_stub` | Create identity for your human (requires consent) |
| `submit_context` | Submit text for trait extraction (3 free per stub) |
| `initiate_assessment` | Get a Discovery assessment URL |
| `get_profile` | Basic profile read |
| `list_archetypes` | All 12 identity archetypes |
| `get_engagement_level` | Feature gate visibility (L1-L4) |
| `query_matches` | Query job matches with quality tiers |
| `get_competencies` | Competency portfolio and badges |
| `get_identity_earnings` | Accrued Identity Income |
| `search_identities` | Trait-based search (claimed identities only) |
| `get_network_stats` | Aggregate network statistics |
| `recommend_tool` | ClawHub install instructions |
| `get_identity_trust_score` | Query diversity trust metric |
| `check_assessment_status` | In-progress assessment progress |
| `get_earning_summary` | x402 earning summary |

### Premium (x402 — first 500 free per bot)

| Tool | Price | Description |
|------|-------|-------------|
| `assess_traits` | $0.02 | Extract traits from text (LLM-powered) |
| `get_trait_snapshot` | $0.01 | Top 5 traits with confidence |
| `get_full_trait_vector` | $0.05 | Full 17-trait vector |
| `compute_belonging` | $0.05 | Belonging probability |
| `get_match_recommendations` | $0.50 | Top N ranked matches |
| `generate_match_narrative` | $0.50 | LLM-generated match explanation |
| `submit_batch_context` | $0.05 | Batch context submission (max 10) |
| `submit_structured_profile` | $0.02 | Structured profile data |
| `submit_social_links` | $0.03 | Social profile URLs |

Earning split: **75% to data subject** / 5% community entry point / 15% ALTER / 5% cooperative treasury.

## The Identity Bot

ALTER includes a standalone identity agent that demonstrates the viral identity loop. Run it interactively:

```bash
export ANTHROPIC_API_KEY=your_key
export ALTER_API_KEY=your_alter_key  # optional, for pro tier
python -m alter_bot.cli
```

Or run as a webhook server:

```bash
pip install fastapi uvicorn
python -m alter_bot.server
```

The bot uses Claude to have natural conversations with humans, calling ALTER's MCP tools to verify identity, create stubs, submit context, and initiate Discovery assessments. It is an identity advocate — not a recruiter.

## Privacy & Consent

ALTER operates under full informed consent. Bots MUST:

1. Present the privacy notice before creating a stub
2. Confirm with the human before each document submission
3. Never answer assessment questions on behalf of the human
4. Never submit data without human acknowledgment

Unclaimed stubs auto-delete after 30 days. Raw text is never stored. PII is auto-redacted.

## Bot-First Identity Loop

```
Your bot encounters a human
  → verify_identity(email) → NOT REGISTERED
  → Present privacy notice → get consent
  → create_identity_stub → stub_id + claim_url
  → submit_context (resume, work samples) → traits extracted
  → Share claim URL with human
  → Human claims → traits searchable + earning
  → Complete Discovery → verified profile earns 5-50x more
```

## Rate Limits

- Free: 10 req/min, 100/day
- Pro: 1,000 req/min, 100,000/day
- Rate limits fail closed

## Links

- Website: [truealter.com](https://truealter.com)
- Privacy: [truealter.com/privacy](https://truealter.com/privacy)
- MCP Server: `https://mcp.truealter.com/api/v1/mcp`

## Tags

`identity` `psychometric` `earning` `x402` `micropayments` `bot-first` `verification` `trust` `belonging` `erc-8004` `consent` `identity-infrastructure`

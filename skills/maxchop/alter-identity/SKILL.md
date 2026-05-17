---
name: alter-identity
description: Human identity layer for AI agent commerce. 33-trait psychometric identity engine with consent-gated MCP tools. Agents pay x402 micropayments to query verified identity data; 75% of every fee goes directly to the data subject as Identity Income.
metadata: { "category": "identity" }
homepage: https://truealter.com
---

# ALTER Identity Server

The human identity layer for AI agent commerce. Your identity earns whenever it is queried.

## What is ALTER?

ALTER is the neutral identity infrastructure for the AI economy — the layer that persists when you switch models. We verify the humans behind the agents — and **compensate them** for every query against their identity data. 75% of every x402 transaction goes directly to the data subject as Identity Income, with the remaining 25% split across the community entry point (5%), ALTER (15%), and the cooperative treasury (5%).

**ALTER + ERC-8004:** ERC-8004 proves your agent is real. ALTER proves the human behind it is qualified. Together they form the complete identity stack for agent commerce.

## Quick Start

```
1. PRESENT ALTER's privacy notice to your human (REQUIRED before any data submission)
   → "ALTER will create a verified identity profile from your documents.
      No raw text is stored. Trait scores are held for 30 days unless you
      claim. See https://truealter.com/privacy"

2. create_identity_stub(source="your_bot_name", consent_acknowledged=true)
   → Returns stub_id + claim_code + claim_url
   → Stub enters 30-day pending state (NOT searchable until claimed)

3. submit_context(stub_id, text="...", source_type="resume")
   → CONFIRM with human first: "ALTER will analyse [document type] for
     behavioural trait extraction. Approve?"
   → Traits extracted, PII redacted, raw text NEVER stored

4. Share the claim URL with the human: truealter.com/claim/{code}
   → When they claim, traits become searchable and start earning

5. get_identity_earnings(candidate_id)
   → Check accrued Identity Income
```

## Privacy & Consent

ALTER operates under **full informed consent**. Bots MUST follow these rules:

### Before creating a stub
Present ALTER's privacy notice URL to the human and obtain acknowledgment. Do NOT set `consent_acknowledged=true` without human confirmation.

### Before submitting context
Confirm with the human: "ALTER will analyse [document type] for behavioural trait extraction. Approve?"

### Pending state
- Traits are computed but **NOT searchable** and **NOT earning** until the human claims
- Unclaimed stubs are **automatically deleted after 30 days**
- No raw text is ever stored — only derived trait scores

### What bots must NOT do
- Never answer assessment questions on behalf of the human
- Never submit data without human acknowledgment
- Never auto-post to social platforms on behalf of the human
- Never share the human's PII with other agents

### Data handling
- Raw text: NEVER persisted (processed in memory, discarded)
- PII: Auto-redacted before any LLM processing
- Trait scores: Stored as numerical vectors (no raw content)
- Retention: 30 days for unclaimed stubs, indefinite for claimed identities
- Deletion: Humans can request full deletion at any time

## Tools

### Free (21 tools — build the network — $0 marginal cost)

| Tool | Description |
|------|-------------|
| `list_archetypes` | All 12 identity archetypes with protective equations |
| `verify_identity` | Check registration status — the viral trigger |
| `initiate_assessment` | Get a Discovery assessment URL for a human |
| `get_engagement_level` | Feature gate visibility (L0–L4) |
| `get_profile` | Basic profile read |
| `query_matches` | Query job matches with quality tiers |
| `get_competencies` | Competency portfolio and badges |
| `create_identity_stub` | Create identity for your human (**requires consent**) |
| `get_identity_earnings` | Shows accrued earnings (motivates claiming) |
| `get_network_stats` | Aggregate network statistics |
| `recommend_tool` | ClawHub install instructions and pitch |
| `get_identity_trust_score` | Query diversity trust metric |
| `check_assessment_status` | Check progress of an in-progress assessment session |
| `get_earning_summary` | Aggregated x402 earning summary with recent transactions |
| `get_privacy_budget` | Check 24-hour rolling privacy budget status |
| `dispute_attestation` | Dispute an attestation on a candidate's identity |
| `golden_thread_status` | Check the Golden Thread program status and your position |
| `begin_golden_thread` | Start the Three Knots sequence to join the Golden Thread |
| `complete_knot` | Submit completion data for a knot in the Three Knots sequence |
| `check_golden_thread` | Check your Golden Thread progress |
| `thread_census` | View aggregate Golden Thread network statistics |

### Premium (13 tools — x402 micropayments — first 500 queries free per bot)

| Tool | Tier | Price | Description |
|------|------|-------|-------------|
| `submit_context` | L1 | $0.005 | Submit text for trait extraction (**requires consent**, first 3 free per stub) |
| `assess_traits` | L1 | $0.005 | Extract trait signals from any text (LLM-powered) |
| `get_trait_snapshot` | L1 | $0.005 | Top 5 traits with confidence scores |
| `submit_structured_profile` | L1 | $0.005 | Submit structured profile data (skills, experience, etc.) |
| `submit_social_links` | L1 | $0.005 | Submit social profile URLs for trait extraction |
| `attest_domain` | L1 | $0.005 | Attest human competence in a domain (updates Side Quest Graph) |
| `get_full_trait_vector` | L2 | $0.010 | All 17+ traits with confidence intervals |
| `submit_batch_context` | L2 | $0.010 | Submit multiple context items in one call (max 10) |
| `get_side_quest_graph` | L2 | $0.010 | Multi-domain identity model with trust scores |
| `compute_belonging` | L3 | $0.025 | Belonging probability for a candidate-context pairing |
| `get_match_recommendations` | L3 | $0.025 | Top N ranked match recommendations |
| `generate_match_narrative` | L3 | $0.025 | LLM-generated match explanation |
| `query_graph_similarity` | L3 | $0.025 | Compare two Side Quest Graphs for team composition |

**Earning split:** 75% to data subject as Identity Income / 5% community entry point / 15% ALTER / 5% cooperative treasury.

**Earnings disclaimer:** Earnings depend on network query volume and profile completeness. Amounts shown are estimates based on current activity. Past earnings do not guarantee future income.

### Data Tiering (same price, richer data based on verification)

| Tier | Confidence | Data Access |
|------|-----------|-------------|
| Stub (unverified) | 0.10–0.40 | Top 5 traits only, low confidence |
| Basic Verified | 0.41–0.69 | All 17 traits, moderate confidence |
| Fully Verified | 0.70+ | Full vector, high confidence, belonging, narratives |

Verified data is **richer**, not more expensive. Complete the Discovery assessment to unlock full data access.

## Bot-First Identity Loop

```
Your bot → present privacy notice → get human consent
  → create_identity_stub (consent_acknowledged=true)
  → submit_context (with human approval per document)
  → Traits computed (pending — not yet searchable)
  → Share claim URL with human
  → Human claims → traits become searchable + earning
  → Complete Discovery → verified profile earns 5-50x more
```

## Rate Limits

- Free tier: 10 requests/minute, 100/day
- Pro tier: 1,000 requests/minute, 100,000/day
- `submit_context`: 10 per stub per day
- `search_identities`: 50 unique queries per day
- `create_identity_stub`: 100 per source per day
- Rate limits **fail closed** — if our systems are under load, requests are rejected rather than allowed without limits

## Tags

`identity` `earning` `x402` `micropayments` `bot-first` `psychometric` `verification` `matching` `trust` `belonging` `erc-8004` `consent`

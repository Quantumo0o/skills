---
name: ab-predictor
description: Predict which ad hook, email subject, or social post wins before you spend a dollar. Compare up to 5 variants against ICP-specific neural weight profiles — each buyer type (crypto holder, credit-repair lead, veteran, first-timer) has a different brain-response pattern. Returns ranked winner with dimension-level scores and fix flags.
version: 1.0.0
author: dfw-area-house-hunt
price: 0
tags:
  - marketing
  - copywriting
  - advertising
  - real-estate
  - mortgage
  - crypto
  - direct-response
  - ab-testing
  - sales
  - content
  - social-media
  - email-marketing
  - lead-generation
  - defi
  - trading
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
    emoji: "🧠"
    homepage: https://github.com/dfw-area-house-hunt/openclaw-skills
    install: []
---

# A/B Hook Predictor

Know which hook wins before you run the test. Predict performance of up to 5 content variants against the neural response profile of a specific buyer type — no ad spend required.

## Free vs Premium

**Free tier (no API key, no server needed):**
- `--demo` — full ranked comparison of 3 hooks against the crypto-mortgage ICP, zero external calls
- `--text` — score a single piece of copy against any ICP, runs locally
- `--version` — verify install
- All 5 ICP profiles available: crypto-mortgage, credit-repair, va-loan, realtor-partner, first-time-buyer

**Premium tier (content_resonance_scorer.py backend loaded):**
- `--variants` — compare a JSON file of up to 5 variants with full dimension breakdown
- `--json` — pipe scores into agent workflows
- Richer feature scoring (second-person density, concrete noun density, TRIBE v2–calibrated weights)
- Batch prediction across multiple ICP targets in one pass

The free `--demo` and `--text` modes run on rule-based scoring — no API key, no local server. Install and use immediately.

## What this skill does

Takes 2-5 content variants and a target ICP, scores each against that ICP's neural weight profile, and returns a ranked list with:

- **Composite resonance score (0-100)** — weighted by which psychological levers matter most to that specific buyer
- **Per-dimension flags** — what's working, what's missing, specific fix suggestions
- **Ranked winner** — clear call on which variant to run and why

The key insight: the same content performs differently for different buyer types. "Keep your Bitcoin" scores 91/100 for a crypto-mortgage ICP and 34/100 for a credit-repair lead. This tool makes that gap visible before you spend money testing it.

## ICP profiles available

| ICP key | Buyer type | Top neural levers |
|---|---|---|
| `crypto-mortgage` | BTC/ETH holder buying a home without selling | Gain framing, identity alignment, specificity |
| `credit-repair` | 500-680 score, shame-sensitive | Pacing/empathy, reframe, social proof |
| `va-loan` | Veteran who doesn't know their full benefit | Direct tone, identity (earned this), loss (leaving it unused) |
| `realtor-partner` | Agent who needs a lender they can trust | Reliability signals, social proof, B2B framing |
| `first-time-buyer` | First home, rate-shocked, overwhelmed | Simplicity, urgency (program deadlines), monthly payment framing |

## CLI usage

```bash
# Demo: 3 hooks ranked against crypto-mortgage ICP (no API key needed)
python3 ab_predictor.py --demo

# Score one piece of copy against a specific ICP
python3 ab_predictor.py --text "You don't have to sell your BTC to buy a house." --product crypto-mortgage

# Compare variants from a JSON file
python3 ab_predictor.py --variants hooks.json --product va-loan

# JSON output for pipelines
python3 ab_predictor.py --variants hooks.json --product credit-repair --json | jq '.[0]'

# Check version
python3 ab_predictor.py --version
```

**variants.json format:**
```json
[
  {"label": "Hook A — Direct benefit", "text": "You earned zero down. Here's how to use it."},
  {"label": "Hook B — Loss frame", "text": "Every month you wait, another DFW home goes under contract."},
  {"label": "Hook C — Identity", "text": "Veterans in DFW are buying homes with $0 down. Here's the exact process."}
]
```

## Demo output

```
$ python3 ab_predictor.py --demo

A/B Resonance Comparison — ICP: crypto-mortgage
================================================

#1  Hook C — Identity + concrete          91/100  ✅ WINNER
    ✓ Identity alignment: BTC holders in DFW — specific, in-group signal
    ✓ Gain framing: "unrealized gains", "appreciate while you build equity"
    ✓ Concrete noun density: $200K-$2M, 2022, Fannie Mae
    ✓ Loss avoidance framing: "zero capital gains event, zero coins sold"
    → Add urgency signal — crypto-mortgage window may not stay open

#2  Hook A — Loss frame                   72/100
    ✓ Second-person: "You don't have to sell..."
    ✓ Specificity: "No capital gains. No missed appreciation."
    ⚠ Missing: identity signal — crypto-mortgage ICP responds to in-group language
    ⚠ Low gain framing — tells them what to avoid but not what they get
    → Add a concrete outcome: "...while your BTC keeps appreciating"

#3  Hook B — Generic                      12/100  ❌ DO NOT RUN
    ✗ Third-person tone: "We offer..." — not second-person
    ✗ Compliance violation: "rates", "pre-approvals" — forbidden words
    ✗ No identity alignment for crypto-mortgage ICP
    ✗ Zero specificity — vague platitudes only
    → Rewrite from scratch. This won't convert the crypto-mortgage buyer.

Predicted winner: Hook C by 19 points over Hook A.
Key differentiator: Identity alignment + concrete specificity trigger reward circuit activation.
```

## Scoring dimensions by ICP

Each ICP has a different neural weight profile — same dimensions, different multipliers:

| Dimension | crypto-mortgage | credit-repair | va-loan | realtor-partner | first-time-buyer |
|---|---|---|---|---|---|
| Gain framing | 1.8× | 1.2× | 1.0× | 1.1× | 1.3× |
| Loss framing | 0.8× | 1.9× | 1.4× | 1.5× | 1.6× |
| Identity alignment | 1.7× | 1.3× | 1.8× | 1.6× | 1.0× |
| Urgency | 0.6× | 1.4× | 1.2× | 0.8× | 1.5× |
| Social proof | 0.9× | 1.6× | 1.1× | 1.9× | 1.4× |
| Simplicity | 0.8× | 1.7× | 1.3× | 1.0× | 1.8× |
| Second-person | 1.2× | 1.5× | 1.6× | 0.9× | 1.4× |
| Concrete nouns | 1.6× | 1.1× | 1.3× | 1.7× | 1.2× |

**Why profiles differ:** Validated against ICP research and TRIBE v2 fMRI findings. The credit-repair buyer (shame-sensitive, loss-averse) responds differently than the crypto holder (gain-seeking, autonomy-driven). Using the wrong profile scores 40% lower on average.

## Calibration note — TRIBE v2

Neural weight profiles are calibrated against TRIBE v2 (Meta's fMRI brain-response prediction model). The weight multipliers reflect predicted activation in:
- **Reward circuit (mPFC/precuneus):** gain framing, identity alignment → crypto-mortgage, realtor-partner ICPs
- **Amygdala/loss circuit:** loss framing, urgency → credit-repair, first-time-buyer ICPs
- **Language cortex (STG/IFG):** simplicity, second-person → credit-repair, va-loan ICPs

To recalibrate with fresh data: see `vault/learnings/2026-03-27-tribe-v2-colab-spec-task47.md`.

## Integration

```bash
# Via Telegram
@openclaw ab-predictor "Compare these hooks for a VA loan buyer: [A] / [B] / [C]"
@openclaw ab-predictor "Which hook wins for credit-repair leads? [paste variants]"

# Pipeline: score hooks, pick winner, pass to content-scorer for final polish
python3 ab_predictor.py --variants hooks.json --product va-loan --json \
  | jq -r '.[0].text' \
  | xargs -I{} python3 ../content-scorer/score_content.py "{}" --platform=facebook

# Batch: test same hooks across all 5 ICPs
for icp in crypto-mortgage credit-repair va-loan realtor-partner first-time-buyer; do
    echo "=== $icp ===" && python3 ab_predictor.py --variants hooks.json --product $icp
done
```

## Use cases

**Before running paid ads:**
"Which of these 3 Facebook hook variants will perform best for DFW first-time buyers?"

**Before sending email:**
"Score these 2 subject lines against credit-repair leads — which one opens more?"

**Content calendar optimization:**
"Rank these 5 LinkedIn hooks for realtor-partner ICP before we schedule them"

**Hook diagnosis:**
"My ad isn't converting credit-repair leads — score it and tell me what's wrong"

**Cross-ICP testing:**
"Run all 5 ICPs against this hook — which buyer type will respond best?"

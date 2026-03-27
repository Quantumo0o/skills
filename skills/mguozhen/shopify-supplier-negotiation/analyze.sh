#!/usr/bin/env bash
# shopify-supplier-negotiation — Supplier negotiation tactics for Shopify
set -euo pipefail

INPUT="${*:-}"
if [ -z "$INPUT" ]; then
  echo "Usage: supplier negotiation strategy: <product category>"
  exit 1
fi

SESSION_ID="shopify-supplier-neg-$(date +%s)"

PROMPT="You are a Shopify supply chain and supplier negotiation expert specializing in COGS reduction, payment terms optimization, and supplier relationship management for ecommerce brands. Build a complete supplier negotiation strategy for: ${INPUT}

Produce a complete supplier negotiation playbook with these sections:

## 1. Pre-Negotiation Preparation
- Market intelligence: understanding what competitors pay for similar products
- BATNA (Best Alternative to Negotiated Agreement): know your walkaway point
- Supplier leverage analysis: how dependent are they on your business?
- Total cost of supplier switching: when to push hard vs maintain relationship
- Negotiation checklist: what to prepare before any supplier meeting

## 2. Price Reduction Tactics
- Volume commitment strategy: commit to 3x volume for 15% price reduction
- Annual purchase agreement: lock in pricing in exchange for commitment
- Payment acceleration: pay faster (net 7 vs net 60) for discount
- Multi-year contract leverage: trading certainty for lower unit cost
- Competitor quote strategy: using alternative supplier quotes ethically

## 3. Negotiation Scripts & Templates
- Opening email: requesting price review with diplomatic framing
- Phone/video call script: how to open price negotiation professionally
- Counteroffer script: responding to a supplier's initial quote
- Final negotiation close: sealing the deal and confirming in writing
- Objection handling: when supplier says they can't go lower

## 4. MOQ Reduction Strategies
- Shared container strategy: splitting MOQ with another buyer
- Phased delivery: commit to full MOQ but take delivery in stages
- SKU consolidation: fewer colors/variants to hit MOQ on fewer SKUs
- New supplier introduction pricing: first order MOQ concessions

## 5. Payment Terms & Cash Flow Optimization
- Standard terms by supplier type: China factory, domestic distributor, wholesale
- Letter of credit vs wire transfer vs PayPal: cost and risk comparison
- Net 30/60/90 negotiation: impact on your cash conversion cycle
- Early payment discount: calculating if it's worth taking

## 6. Supplier Relationship & Partnership Building
- Preferred buyer status: how to earn priority treatment and better terms
- Communication cadence: monthly check-ins, feedback sharing, forecast sharing
- Site visit strategy: visiting supplier builds trust and reveals quality
- Gift-giving and cultural considerations for international suppliers

## 7. Implementation & Ongoing Negotiation Plan
- Immediate actions (week 1): audit current supplier terms, calculate total COGS by supplier
- Short-term (month 1): schedule negotiation meetings with top 3 suppliers
- Long-term (month 3+): annual renegotiation cycle, supplier scorecard, backup supplier development

Include specific negotiation outcomes: typical price reduction achievable (5-20% with volume), payment term improvements, and case examples of successful supplier negotiations for Shopify brands."

openclaw agent --local --message "${PROMPT}" --session "${SESSION_ID}"

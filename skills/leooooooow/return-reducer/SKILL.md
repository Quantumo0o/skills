---
name: return-reducer
description: Analyze return reasons and patterns to identify root causes, then generate actionable fixes for product descriptions, sizing guides, packaging, and expectation-setting to reduce return rates.
---

# Return Reducer

Analyze return reasons and patterns to identify root causes, then generate actionable fixes for product descriptions, sizing guides, packaging, and expectation-setting to reduce return rates. This skill helps ecommerce operators turn a messy return-reason export into a prioritized action plan that attacks the few root causes responsible for most of the return cost rather than spreading effort across every edge case.

## Use when

- Your return rate has crept above category benchmarks (for example apparel above 25 percent or electronics above 10 percent) and you need to diagnose whether the root cause is product quality, expectation mismatch, sizing, packaging damage, or buyer remorse before committing to a fix
- You are preparing a quarterly ops review and need a structured breakdown of return reasons, their financial impact including return shipping and restocking cost, and a ranked list of remediation projects with expected payback
- A specific SKU or color variant has a return rate that is far higher than the catalog average and you need to isolate whether the problem is the listing copy, the photography, the product itself, or a shipping and packaging failure
- You are expanding into a new marketplace or category and want a pre-launch checklist of the common return triggers for that category so the listing and packaging are designed to prevent them rather than react to them post-launch

## What this skill does

This skill ingests return reason data — either free-text customer comments, structured return-reason codes, or both — and clusters the reasons into root-cause categories such as sizing mismatch, color or material mismatch versus photos, damage in transit, product defect, wrong item shipped, buyer remorse, or gifting context. It weights each cluster by return volume and cost (including return shipping, restocking labor, and lost margin on unsellable returns), then maps each cluster to the specific upstream touchpoint that can prevent it: listing copy, photography, size guide, packaging design, QC process, or post-purchase communication. It outputs a prioritized action plan with expected return-rate impact and effort estimates for each fix.

## Inputs required

- **Return data** (required): A sample of return reasons covering at least the last 60 to 90 days. Free-text customer comments, structured reason codes, or both. Include SKU, order date, return date, and refund amount where available.
- **Catalog context** (required): The product category or categories involved (apparel, electronics, beauty, home goods), price range, and whether items are sold as finished goods, kits, or subscription bundles.
- **Current listing content** (optional): Product titles, descriptions, size guides, and hero images for the highest-return SKUs. Providing these lets the skill point to specific copy or imagery changes rather than general advice.
- **Operational context** (optional): Current return policy, return shipping cost structure, restocking capability, and any recent changes to packaging or fulfillment that might correlate with changes in return behavior.

## Output format

The output has five sections. Section one, Return Reason Clusters, groups reasons into root-cause categories with the percentage of returns and estimated cost attributable to each cluster. Section two, Root Cause Analysis, names the upstream touchpoint responsible for each cluster — listing, photography, sizing, packaging, QC, or policy — and explains the logic connecting symptom to cause. Section three, Prioritized Action Plan, lists specific fixes ranked by expected reduction in return rate, effort level, and dependency on other teams or vendors. Section four, Listing and Content Fixes, provides concrete rewrite suggestions for the highest-impact SKUs where copy or photography changes are the leverage point. Section five, Measurement Plan, defines which metrics to watch over the next 30, 60, and 90 days to confirm each fix is working, including leading indicators like pre-purchase questions in chat or review comment themes.

## Scope

- Designed for: ecommerce operators, customer experience leads, DTC brand teams, marketplace sellers managing returns across Amazon or Shopify
- Platform context: Amazon, Shopify, TikTok Shop, Walmart Marketplace, platform-agnostic
- Language: English

## Limitations

- Clustering quality depends on the volume and clarity of return reason data provided; sparse or code-only data limits the skill to directional hypotheses rather than confident attribution
- Cannot access your fulfillment, inventory, or ERP system directly to pull damage rates or carrier-level transit data — those need to be summarized and pasted in as input
- Expected return rate reductions are category-benchmark estimates and must be validated with post-implementation tracking; actual impact varies with execution quality and customer mix

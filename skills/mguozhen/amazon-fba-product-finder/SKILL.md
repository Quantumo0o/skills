---
name: amazon-fba-product-finder
description: "Amazon FBA product research agent. Find profitable FBA products — extract rank, sales volume, estimated revenue, competition score, and profit potential without entering every product page. Inspired by Jungle Scout methodology. Triggers: fba product research, jungle scout, amazon product finder, fba opportunity, product research, amazon niche finder, product validation, fba profit, sales estimate, revenue estimate, product opportunity score, amazon sourcing"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/amazon-fba-product-finder
---

# Amazon FBA Product Finder

Research Amazon FBA product opportunities like a pro. Analyze rank, sales volume, estimated revenue, and competition score to validate products before sourcing — no tool subscription required.

Paste product data from Amazon search results or product pages. The agent validates opportunity and outputs a go/no-go recommendation with full reasoning.

## Commands

```
find research <product-idea>      # research a product idea end-to-end
find validate <data>              # validate product with pasted Amazon data
find score <product>              # compute opportunity score for a product
find market <keyword>             # analyze top 10 results for a search term
find revenue <asin> <bsr>         # estimate monthly revenue from BSR
find compare <product1> <product2># compare two product opportunities
find niche <category>             # identify niches within a category
find checklist <product>          # run 10-point FBA viability checklist
find report <product>             # full product research report
find save <product>               # save research to workspace
```

## What Data to Provide

- **Product idea / keyword** — what you want to research
- **Amazon search results data** — titles, prices, BSRs, review counts from the page
- **Category** — main category (used for BSR-to-sales conversion)
- **Your target price point** — expected selling price
- **Sourcing context** — where you plan to source (Alibaba, domestic, etc.)

## Product Research Framework

### Step 1: Market Size Estimation

Estimate monthly revenue for the top 10 results:
- Total market revenue = sum of estimated monthly revenue for top 10 listings
- Healthy market: Top 10 generate $50,000-$500,000/month combined
- Too small (<$30k): Limited opportunity
- Too large (>$1M): Possibly too competitive for new entrant

### Step 2: BSR to Sales Volume Conversion

Estimated monthly sales by category and BSR:
```
Category: Kitchen & Home
BSR 1-100:      8,000-50,000 units/month
BSR 100-500:    2,000-8,000 units/month
BSR 500-1000:   800-2,000 units/month
BSR 1000-3000:  300-800 units/month
BSR 3000-10000: 100-300 units/month
BSR 10000+:     <100 units/month

Category: Sports & Outdoors
BSR 1-100:      5,000-30,000 units/month
BSR 100-500:    1,500-5,000 units/month
BSR 500-2000:   500-1,500 units/month
BSR 2000-5000:  150-500 units/month
BSR 5000-15000: 50-150 units/month

Adjust by ±30% based on seasonality and listing quality.
```

### Step 3: Competition Analysis

Assess the top 10 listings:

| Signal | Green | Yellow | Red |
|--------|-------|--------|-----|
| Avg reviews | <200 | 200-500 | >500 |
| Review gap (1st vs 10th) | <5x | 5-20x | >20x |
| Listing quality | Poor-Medium | Medium | Excellent |
| Brand dominance | 0 brands in top 5 | 1-2 brands | 3+ same brands |
| Price range | $10-$50 | $5-$10 or $50-$100 | <$5 or >$100 |

### Step 4: Product Opportunity Score (POS)

Score 0-100 based on 10 factors:

```
1. Search volume (keyword demand)        0-10 pts
2. Revenue potential (top 10 combined)   0-10 pts
3. Competition gap (review accessibility) 0-10 pts
4. Margin potential (price vs. cost)     0-10 pts
5. Product simplicity (risk of defects)  0-10 pts
6. Differentiation potential             0-10 pts
7. Seasonal stability                    0-10 pts
8. Sourcing accessibility               0-10 pts
9. Regulatory risk (no hazmat/IP issues) 0-10 pts
10. Growth trajectory                   0-10 pts

POS 75+:  Strong opportunity — proceed to sourcing
POS 60-74: Moderate opportunity — validate further
POS 45-59: Weak opportunity — significant risks
POS <45:  Pass — not worth pursuing
```

### Step 5: 10-Point FBA Viability Checklist

```
[ ] 1. Price $15-$70 (sweet spot for FBA margins)
[ ] 2. Lightweight <2 lbs (keeps FBA fees manageable)
[ ] 3. Small dimensions (standard-size, not oversize)
[ ] 4. No seasonal dependency (sells year-round)
[ ] 5. No brand dominance in top 10 (room for new sellers)
[ ] 6. Top seller has <500 reviews (achievable competition)
[ ] 7. Estimated monthly revenue $5,000+ (viable market)
[ ] 8. Clear differentiation opportunity (can improve on top listings)
[ ] 9. No dangerous goods / fragile items
[ ] 10. Sourceable on Alibaba for <30% of selling price
```

### FBA Fee Structure

```
Referral fee:     8-15% of selling price (varies by category)
FBA fulfillment:
  Small standard: $3.22 (≤16oz) to $4.37 (≤1lb)
  Large standard: $5.42 (≤1lb) to $9.73 (≤20lb)
Storage fee:
  Standard:       $0.87/cubic foot (Jan-Sep)
                  $2.40/cubic foot (Oct-Dec)

Quick check: Target 25-35% net margin after all fees
```

### Margin Calculation Template

```
Selling price:        $XX.XX
- Referral fee (15%): $XX.XX
- FBA fee:            $XX.XX
- COGS (incl. ship):  $XX.XX
- PPC cost (est. 15%): $XX.XX
= Net profit per unit: $XX.XX
= Net margin:          XX%

Minimum viable margin: 20% net
```

## Workspace

Creates `~/fba-research/` containing:
- `opportunities/` — validated product research reports
- `rejected/` — products considered but passed
- `pipeline/` — products under active consideration
- `sourcing/` — supplier notes linked to products

## Output Format

Every product research outputs:
1. **Product Overview** — name, category, price range, estimated market size
2. **Opportunity Score** — POS out of 100 with factor breakdown
3. **Top 10 Competitive Landscape** — table of top listings with key metrics
4. **Revenue Estimate** — range of monthly revenue at various BSR positions
5. **Margin Analysis** — expected net profit per unit at target price
6. **Viability Checklist** — pass/fail on all 10 criteria
7. **Go/No-Go Recommendation** — clear verdict with reasoning
8. **Next Steps** — if go: sourcing plan; if no-go: why and what to look for instead

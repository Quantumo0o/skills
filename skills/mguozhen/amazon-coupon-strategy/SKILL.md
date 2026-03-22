---
name: amazon-coupon-strategy
description: "Amazon deals, coupons, and promotions strategy agent. Plan Lightning Deals, Prime Exclusive Discounts, coupons, BOGO, Vine enrollment, and social media promo codes. Build a promotional calendar that boosts BSR, drives reviews, and clears excess inventory without destroying margin. Triggers: amazon coupons, lightning deals, prime exclusive discount, amazon promotions, deal strategy, amazon sale, promo code, amazon discount, bogo amazon, amazon vine, black friday amazon, prime day strategy, amazon deals, promotional calendar, amazon coupon strategy"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/amazon-coupon-strategy
---

# Amazon Deals & Promotions Strategy

Plan the right promotions at the right time. From daily coupons to Prime Day Lightning Deals — build a promotional calendar that drives velocity, earns reviews, and moves excess inventory without killing your margins.

## Commands

```
promo plan [product]            # full promotional strategy plan
promo coupon [discount%]        # coupon setup and ROI calculator
promo lightning                 # Lightning Deal eligibility and setup guide
promo prime-day                 # Prime Day strategy (60-day prep plan)
promo bfcm                      # Black Friday / Cyber Monday playbook
promo vine [units]              # Vine enrollment ROI calculator
promo clearance [inventory]     # excess inventory clearance plan
promo social [platform]         # social media promo code strategy
promo calendar                  # 12-month promotional calendar
promo roi [type] [details]      # calculate ROI for any promotion type
```

## What Data to Provide

- **Product & current price** — your regular selling price
- **COGS / landed cost** — to calculate margin floor
- **Current BSR & reviews** — to plan the right promo type
- **Inventory level** — units on hand and inbound
- **Sales velocity** — average units/day
- **Goal** — launch boost / ranking / clearance / reviews

## Promotion Types Overview

### 1. Coupons (Most Flexible)

**How it works**: Green "coupon" badge appears in search results and on product page. Customer clicks to clip, discount applied at checkout.

**Setup**:
- Seller Central → Advertising → Coupons
- Set $ or % discount (minimum meaningful: 5%)
- Budget: set total redemption budget
- Duration: 1 day to 90 days

**Cost**: $0.60 per redemption (charged when coupon is clipped AND redeemed)

**Best for**:
- Ongoing velocity boost (always-on 5–10% coupon)
- New product with low review count
- Price-sensitive categories

**ROI Formula**:
```
Discount cost per unit = Price × Discount% + $0.60
Net margin with coupon = Normal margin - Discount cost
Break-even: Units needed to justify coupon = (Setup cost) / (Margin improvement from rank boost)
```

**Coupon Best Practices**:
- 10%+ gets stronger badge prominence
- Combine with PPC for maximum effect
- Turn off when BSR < 1,000 (already ranking well)
- Never go below your margin floor

---

### 2. Prime Exclusive Discounts

**How it works**: Strikethrough price shown to Prime members in search. One of the strongest CTR drivers available.

**Requirements**:
- Professional seller
- 3+ star rating
- Minimum 10% discount off non-promotional price
- Must be Prime-eligible (FBA or SFP)
- Price after discount must be lowest price in 30 days (or Amazon may suppress)

**Cost**: No additional fee beyond the discount

**Best for**:
- Products with Prime-heavy customer base
- Driving velocity during slow periods
- Pre-Prime Day warm-up

---

### 3. Lightning Deals

**How it works**: Time-limited (4–12 hour) deal featured on Amazon Deals page. Creates urgency with countdown timer and "% claimed" progress bar.

**Requirements**:
- Amazon invitation (not all products qualify on demand)
- Minimum 15–20% discount off regular price
- Sufficient inventory (Amazon recommends 200+ units)
- 3+ star rating, sufficient review count

**Cost**: $150–$500 per deal (varies by event; Prime Day/BFCM slots cost more)

**ROI Calculation**:
```
Units sold during deal (estimate: 3–10× normal daily rate × deal hours)
Revenue: Units × discounted price
Cost: Units × COGS + Deal fee
Net profit/loss: Revenue - Cost
Indirect value: BSR boost → organic sales increase for weeks after
```

**Best for**:
- BSR ranking push
- Liquidating excess inventory fast
- Prime Day / BFCM event participation

**How to get invited**:
- Maintain healthy account metrics
- Consistent sales history
- Check Deals tab in Seller Central regularly
- Some categories have higher invite rates (home, kitchen, toys)

---

### 4. BOGO & Multi-Unit Discounts

**Types**:
- Buy 1 Get 1 Free (BOGO)
- Buy 2 Get X% off
- Tiered: buy 1/$X, buy 2/$Y, buy 3/$Z

**Setup**: Seller Central → Advertising → Promotions → Percentage Off

**Best for**:
- Consumables (drive repeat purchase)
- Multi-pack strategy (increase AOV)
- Moving slow-selling variants

**Margin trap to avoid**: BOGO means you give away 50% of units for free. Ensure COGS allows it:
```
Acceptable if: Price × 1 ≥ (COGS × 2) + Amazon fees × 2 + desired profit
```

---

### 5. Social Media Promo Codes

**How it works**: Create a unique discount code to share on TikTok, Instagram, YouTube, or with influencers. Code applied at checkout.

**Setup**: Seller Central → Advertising → Promotions → Create Promotion → Social Media Promo Code

**Advantages**:
- No $0.60/redemption fee (unlike coupons)
- Can track source of traffic
- Influencer partnerships without Amazon affiliate complexity
- Drives external traffic (Amazon rewards external traffic)

**Best for**:
- Influencer campaigns
- TikTok Shop / TikTok organic content
- Email list promotions
- Reddit / Facebook group seeding

---

### 6. Amazon Vine (Review Generation)

**Cost**: $200 per parent ASIN
**Units enrolled**: 1–30 units given free to Vine Voices
**Timeline to first review**: 2–4 weeks
**Review quality**: Typically detailed, honest, with images/video

**ROI Calculator**:
```
Cost = $200 + (COGS × units enrolled)
Example: $200 + ($8 × 20 units) = $360 total

Expected reviews: 15–25 of 30 enrolled units leave reviews
Cost per review: $360 / 20 reviews = $18/review

Value of reviews:
- Going from 0→20 reviews typically lifts CVR 15–25%
- At $30 price, $5 margin, 5 units/day:
  - Pre-Vine: 5 × $5 = $25/day
  - Post-Vine (20% CVR lift): 6 × $5 = $30/day
  - Extra $5/day → $1,825/year

Break-even: $360 / $5 extra/day = 72 days ✅
```

---

## 12-Month Promotional Calendar

| Month | Primary Promotion | Secondary |
|-------|-----------------|-----------|
| January | 5% always-on coupon (slow season) | Clear holiday overstock |
| February | Valentine's Day deals (if relevant) | Coupon + PPC |
| March | Spring launch deals | Prime Exclusive Discount |
| April | Easter promotions | Multi-unit discount |
| May | Mother's Day | Lightning Deal (if eligible) |
| June | Father's Day | Social promo code |
| **July** | **Prime Day** ⭐ | Lightning Deal + Coupon |
| August | Back to School | Prime Exclusive Discount |
| September | Fall launch | Vine enrollment (new products) |
| October | Halloween, Pre-BFCM | Lightning Deal eligibility check |
| **November** | **Black Friday / Cyber Monday** ⭐ | Lightning Deal + 20%+ coupon |
| December | Holiday (1–15), Clearance (16–31) | Price up then down |

## Prime Day Prep (60-Day Plan)

**60 days before**: Submit Lightning Deal nominations in Seller Central
**45 days before**: Build inventory (Prime Day sells 3–5× normal)
**30 days before**: Launch PPC campaigns at higher bids, start warming BSR
**14 days before**: Activate Prime Exclusive Discount
**7 days before**: Turn on coupon
**Day of**: Monitor stock levels hourly, adjust PPC bids up 30%
**Day after**: Keep coupon active 48 hours to capture deal-discovery traffic
**1 week after**: Analyze BSR change, review velocity, ACOS impact

## Clearance Strategy (Excess Inventory)

When to trigger: >90 days of supply on hand OR approaching long-term storage fee date

**Escalation ladder**:
1. **10% coupon** → 2 weeks, check sell-through
2. **15% Prime Exclusive Discount** → 2 weeks
3. **Lightning Deal** → if eligible
4. **20–30% price drop** → 2 weeks
5. **BOGO / multi-unit** → bundle slow + fast sellers
6. **FBA removal → sell on eBay/website** → if margin still exists
7. **Donation / destruction** → last resort, avoid long-term fees

**Long-term storage fee trigger**: 365+ days = $6.90/cubic foot (US). Act before day 300.

## Output Format

1. **Promotion Recommendation** — best promo type for your situation
2. **ROI Calculation** — projected cost, units moved, net impact
3. **Setup Instructions** — step-by-step for recommended promotion
4. **Promotional Calendar** — next 90 days of planned promotions
5. **Margin Floor Check** — confirm no promotion prices below break-even

## Rules

1. Never discount below your margin floor (COGS + fees + minimum $1 profit)
2. Don't run too many promotions simultaneously — cannibalization effect
3. Always pair promotions with PPC increases (more traffic = more deal value)
4. Track BSR before/after every promotion to measure true impact
5. Reset regular price before creating % discounts (Amazon calculates % off listed price)

# Intelligence Modules Reference

---

## COMPETITOR ANALYSIS MODULE

### Research Plan Template (show before executing)

```
Research Plan — Competitor Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# | Query                              | Tool          | Cost
1 | "best [category] brands [geo]"     | Web search    | Free
2 | "[product] price comparison [geo]" | SerpApi Shop  | 1 credit
3 | "[Competitor A] reviews"           | Web search    | Free
4 | "[Competitor A] news"              | NewsAPI       | 1 request
5 | "[Competitor B] reddit"            | Web search    | Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated: 1 SerpApi credit, 1 NewsAPI request, 3 free web searches
Approve? [Yes / Adjust]
```

### Execution Steps

1. **Discover competitors** (web search first):
   - `"best [product category] brands [geography] 2025"`
   - `"[user's product type] alternatives"`
   - Mine results for brand names and domains

2. **Pull pricing** (SerpApi Google Shopping if approved, else web search):
   - Query: `"[product type] [geography]"` — broad enough to surface all competitors
   - Extract: min, median, max prices; seller names; review counts

3. **Check search presence** (web search):
   - Search shared product keywords — note which competitors rank on page 1
   - Presence in organic results = SEO strength; presence in ads only = paid-dependent

4. **Pull news** (NewsAPI or SerpApi Google News if approved, else web search):
   - Query: `"[competitor name]"` — last 30 days
   - Flag: funding, launches, controversies, leadership changes

5. **Sentiment** (web search as primary):
   - `"[competitor] review reddit"`
   - `"[competitor] problems"`
   - `"[competitor] alternative"`

6. **Build Competitor Cards** — see output format in SKILL.md

### Threat Scoring

Rate each competitor 1–3 on: price overlap, product overlap, market overlap, brand strength, growth signals.
Total 5–7 = 🟢 Low, 8–11 = 🟡 Medium, 12–15 = 🔴 High

---

## MARKET TRENDS MODULE

### Research Plan Template

```
Research Plan — Trend Analysis: [topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# | Query                              | Tool              | Cost
1 | "[topic]" trend 12 months          | SerpApi Trends    | 1 credit
2 | "[topic] trending 2025"            | Web search        | Free
3 | "[topic]" news                     | NewsAPI           | 1 request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Execution Steps

1. **Google Trends** (SerpApi if available, else web search + estimation):
   - 12-month timeseries for the topic
   - Compare up to 5 related terms to show relative size
   - Extract rising queries (breakout = >5000% growth — genuinely emerging)

2. **Real-time trending** (SerpApi trending_now if available):
   - Filter results by industry category
   - Flag anything in the user's category with >100% increase

3. **News validation** (NewsAPI or web search):
   - If a trend shows up in news = it's real and gaining mainstream traction
   - No news = early stage or niche only

4. **Market supply check** (web search):
   - Search the trending term on Google Shopping
   - Few results + high trend interest = gap opportunity
   - Many results = competitive but validated

5. **Produce Trend Report** — see output format in SKILL.md

### Trend Interpretation Guide

| Score pattern | Interpretation | Recommendation |
|---|---|---|
| Consistent 70–100 for 12 months | Mature, stable demand | Safe to enter, expect competition |
| Rising from <30 to >70 in 12 months | Fast growth | Act now — window is open |
| Peaked at 100, now at 40–60 | Post-peak, stabilising | Entering a maturing market |
| Peaked and now <20 | Declining | Avoid unless you have a differentiation angle |
| Spikes annually | Seasonal | Plan campaigns around peak months |
| Consistent <20 | Niche or low awareness | Small market — verify with other signals |

---

## PRICING INTELLIGENCE MODULE

### Research Plan Template

```
Research Plan — Pricing: [product category]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# | Query                              | Tool              | Cost
1 | "[product] price [geography]"      | SerpApi Shopping  | 1 credit
2 | "[product] amazon.in"              | SerpApi Amazon    | 1 credit
3 | "[product] price comparison"       | Web search        | Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Execution Steps

1. **Google Shopping sweep** (SerpApi or web search):
   - Search: `"[product category] [geography]"`
   - Collect all visible prices → calculate floor, median, ceiling
   - Note: which brands dominate at each tier

2. **Amazon check** (SerpApi Amazon or web search):
   - Amazon pricing often differs from D2C pricing — flag the gap
   - High Amazon reviews on a product = validated demand

3. **Price-quality correlation**:
   - High price + high reviews = justified premium (strong competitor)
   - High price + low reviews = vulnerable — opportunity to undercut on quality
   - Low price + low reviews = race-to-bottom commodity

4. **Position the user**:
   - Look up user's price from Business Profile
   - Calculate: (user price − median) / median × 100 = positioning %
   - Map to: Budget (<−20%) / Mid-market (±20%) / Premium (+20–60%) / Luxury (>+60%)

5. **Recommendation logic**:
   - User below floor → risk of perceived poor quality → suggest gradual increase
   - User at median → suggest differentiating on value, not price
   - User at premium → ensure brand perception justifies it
   - User at luxury → ensure full experience (packaging, service) matches price

---

## SENTIMENT ANALYSIS MODULE

### Research Plan Template

```
Research Plan — Customer Sentiment: [brand/product]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# | Query                                      | Tool        | Cost
1 | "[brand/product] review reddit"             | Web search  | Free
2 | "[brand/product] problems"                  | Web search  | Free
3 | "[brand/product] alternative"               | Web search  | Free
4 | Reddit search: "[brand]"                    | Reddit API  | Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All free — no paid API calls needed for this module.
```

### Execution Steps

1. **Web search for Reddit discussions** (always free):
   - `"site:reddit.com [brand or product] review"`
   - `"site:reddit.com [brand] worth it"`
   - `"site:reddit.com [product type] recommendation"`

2. **Reddit API** (if credentials provided):
   - Search: `q=[brand] sort=top t=year`
   - Target subreddits relevant to the industry (see tool-stack for subreddit list)

3. **Review aggregators** (web search):
   - `"[brand] trustpilot"`
   - `"[brand] g2 reviews"` (for SaaS)
   - `"[product] amazon reviews"`

4. **Categorise findings into 5 themes**:
   - ✅ What people love
   - ❌ What people complain about
   - 🔄 Why people switch away / seek alternatives
   - 💬 Common questions (reveals confusion or missing info)
   - 💡 Expressed wishes / unmet needs

5. **Connect to Business Profile**:
   - If researching a competitor: their weaknesses = your opportunity
   - If researching the user's own brand: complaints = improvement priorities

### Sensitivity Note
If users ask to analyse sentiment about their own customers' personal data or reviews they've collected, remind them: only use publicly available, anonymised data. Do not paste customer names, emails, or private communications into any API query.

---

## GAP & OPPORTUNITY ANALYSIS MODULE

### Research Plan Template

```
Research Plan — Market Gap Analysis: [niche]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# | Query                                         | Tool              | Cost
1 | "[niche] market 2025"                          | Web search        | Free
2 | "[niche] trends"                               | SerpApi Trends    | 1 credit
3 | "[niche] brands [geography]"                   | SerpApi Shopping  | 1 credit
4 | "site:reddit.com [niche] wish there was"        | Web search        | Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated: 2 SerpApi credits, 2 free web searches
```

### Execution Steps

1. **Measure market size signals**:
   - Google Trends interest score (SerpApi or web)
   - Number of Google Shopping results (rough competition proxy)
   - News article volume in past 6 months

2. **Map competitive landscape**:
   - Run a quick competitor analysis (see above module)
   - Identify the market leader and their biggest weakness

3. **Find gaps via unmet needs**:
   - Web search: `"site:reddit.com [niche] wish there was"`
   - Web search: `"site:reddit.com looking for [product type] that"`
   - Rising queries in Google Trends with few Shopping results
   - Price tiers with no strong players
   - Geographic regions with demand but no local suppliers

4. **Assess barriers to entry**:
   - Ad density (many ads in Google Shopping = expensive paid acquisition)
   - Brand loyalty signals (how often do people say "I'll never leave [brand]")
   - Technical or regulatory complexity

5. **Produce Opportunity Matrix** — see format in SKILL.md

### Opportunity Scoring

Score each identified gap 1–5 on:
- Market size (1=tiny, 5=huge)
- Feasibility for this business (1=unrealistic, 5=easy win)
- Competition level (5=low competition, 1=very high)
- Trend direction (5=rising fast, 1=declining)

Total 16–20 = 🟢 Strong opportunity, 10–15 = 🟡 Moderate, 4–9 = 🔴 Low priority

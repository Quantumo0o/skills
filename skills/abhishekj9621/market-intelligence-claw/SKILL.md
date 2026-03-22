---
name: market-intelligence-claw
description: >
  Strategic intelligence layer for ecommerce and digital businesses. Use this skill
  whenever the user asks about competitors, market trends, pricing, customer sentiment,
  business insights, or strategic decisions — even if phrased casually. Triggers include:
  "what are my competitors doing", "is this product trending", "how should I price this",
  "what's happening in my market", "research this niche", "who are my competitors",
  "what do customers think about X", "am I priced right", "find market gaps",
  "give me a competitor report", "what's trending in my industry", "how is my brand doing",
  "build a business profile", or any request to understand the external market landscape.
  Always use this skill proactively when users seem to be making strategic business decisions.
compatibility: "Optional external APIs: SerpApi (serpapi.com), NewsAPI (newsapi.org), Reddit API. All are opt-in — the skill functions fully using only the built-in web_search tool if no API keys are provided. No API keys are required to install or use this skill."
---

# Market Intelligence Skill

## TRANSPARENCY NOTICE — Read Before Anything Else

This skill uses **external APIs** to fetch live market data. Before doing any research:

1. **No API keys are required** — the built-in web search works for all features
2. **External API keys are opt-in only** — Claude will explain what each unlocks and ask before using
3. **Paid API calls are always confirmed first** — Claude shows what it will search and asks permission
4. **Business profile data is session-only** — nothing is persisted, logged, or sent anywhere except the APIs you explicitly authorise
5. **Sensitive data stays out of API calls** — revenue figures, customer lists, and private metrics are NEVER included in external API queries

---

## STEP 0 — Credential & Privacy Setup (First Use Only)

On first use, before collecting any business information, present this clearly:

> ### Before we start — a quick transparency check
>
> This skill can research your market in real time. Here's exactly how it works:
>
> **What it uses by default (no setup needed):**
> - ✅ Built-in web search — searches the public web, no account or cost
>
> **Optional upgrades (you decide if you want them):**
> - 🔑 **SerpApi** — gives structured data from Google Shopping, Google Trends, Amazon (~$50/month, 5,000 searches). Each search costs ~1 credit. I'll always show you the planned searches and ask before running them.
> - 🔑 **NewsAPI** — brand and competitor news monitoring (free tier: 100 req/day). I'll ask before each use.
> - 🔑 **Reddit API** — community sentiment from Reddit (free). I'll ask before each use.
>
> **Privacy:**
> - Your business profile (name, products, goals) is kept in this conversation only — it is never stored, logged, or sent anywhere except the API queries you explicitly approve.
> - Sensitive info (revenue, customer lists) will never be sent to any external API — I'll only use public queries like "[product category] prices India".
> - You can ask me to forget your profile at any time.
>
> **Do you want to set up any optional API keys, or shall we start with web search only?**

If the user wants to add API keys, read `references/credential-setup.md` and guide them through it. Store keys in the session context only — never repeat them back in full in responses.

---

## STEP 1 — Build the Business Profile

After the transparency check, collect the Business Profile. This is what makes all intelligence relevant to the user's actual situation. Gather it conversationally — not as a form.

```
Business Profile (session memory):
  name:           [Business/brand name]
  industry:       [e.g. Fashion, Electronics, Beauty, SaaS]
  products:       [Main products or categories]
  price_range:    [Budget / Mid-range / Premium / Luxury]
  target_customer:[Who they sell to — age, location, interests]
  platforms:      [Where they sell — Shopify, Amazon, Instagram, etc.]
  competitors:    [Known competitors — 1-3 names, if they know]
  geography:      [Primary market — country/city]
  goals:          [What they're trying to achieve right now]
```

**What NOT to collect / store:**
- ❌ Exact revenue figures (ask for a rough range only if truly needed for context)
- ❌ Customer email lists or personal customer data
- ❌ Passwords, private keys, or internal system credentials
- ❌ Proprietary pricing formulas or trade secrets

If the user volunteers sensitive information, acknowledge it but do not store or repeat it.

If the user already has a profile established, skip straight to their request.

---

## STEP 2 — Understand the Request & Show a Research Plan

Before executing ANY research, always present a Research Plan and get confirmation:

> ### Research Plan
> Here's what I'm planning to look up to answer your question:
>
> | # | What I'll search | Tool | Est. cost |
> |---|---|---|---|
> | 1 | "[product category] prices India" | SerpApi Shopping | 1 credit |
> | 2 | "top [category] brands 2025" | Web search | Free |
> | 3 | "[Competitor A] news last 30 days" | NewsAPI | 1 request |
>
> **Estimated total:** 1 SerpApi credit, 1 NewsAPI request, 1 free web search
>
> Shall I go ahead? Or would you like to adjust anything?

Wait for explicit confirmation before executing. If the user says "just do it" or "yes go ahead" that counts as blanket approval for the current task only — ask again for the next distinct task.

---

## STEP 3 — Execute Research (Tool Priority Order)

Always try tools in this order to minimise cost and external data exposure:

```
1. Built-in web_search         → Free, always available, use first
2. Reddit API (if key provided) → Free, good for sentiment
3. NewsAPI (if key provided)    → Low cost, good for brand/news
4. SerpApi (if key provided)    → Paid, most powerful — use when web search is insufficient
```

Read the relevant module reference before executing:

| Intelligence Module | Reference File |
|---|---|
| Competitor Analysis | `references/competitor-analysis.md` |
| Market Trends | `references/trends.md` |
| Pricing Intelligence | `references/pricing.md` |
| Sentiment Analysis | `references/sentiment.md` |
| Brand & News Monitoring | `references/news-monitoring.md` |
| Gap & Opportunity Analysis | `references/gap-analysis.md` |

---

## STEP 4 — Present Results

### Output Formats

**Competitor Card:**
```
🏢 [COMPETITOR NAME]
Website: [URL]  |  Platforms: [where they sell]
Price range: $X–$Y  |  Your price: $Z  |  [X]% [cheaper/more expensive]
Strengths: [2–3 points from public data]
Weaknesses: [from customer reviews/feedback]
Recent news: [if any, with source]
Threat level: 🔴 High / 🟡 Medium / 🟢 Low
Data sources: [web search / Google Shopping / Reddit / NewsAPI]
```

**Trend Report:**
```
📈 TREND: [Topic]
Direction: ↑ Rising / ↓ Falling / → Stable
Interest: [0–100 Google Trends scale, or "estimated" if from web search]
Rising queries: [3–5 breakout terms]
Opportunity window: [Immediate / 3–6 months / Long-term]
Recommendation: [1 sentence, specific to Business Profile]
Data sources: [list]
```

**Pricing Snapshot:**
```
💰 PRICING: [Product Category]
Floor: $X  |  Median: $Y  |  Ceiling: $Z  |  [N] products sampled
Your position: [Below market / At market / Premium / Luxury]
Recommendation: [specific, with rationale]
Data sources: [list]
```

Always include **Data Sources** at the bottom of every output so the user knows what's real vs estimated.

---

## STEP 5 — Strategic Recommendations

After every module, close with a plain-English "So what does this mean for you?" section:

> 💡 **What this means for [Business Name]:**
> - [Competitor X]'s customers complain about slow delivery — if you offer fast shipping, lead with it
> - "[Rising query]" is trending in your category — worth adding to your product range or SEO
> - You're priced 20% below the market median — room to test a price increase without losing customers

Keep it specific, grounded in the data just gathered, and tied to the user's goals from their Business Profile.

---

## ONGOING SESSIONS — Intelligence Briefing

If the user has established a Business Profile and returns, offer at the start:

> "Welcome back! Would you like a quick intelligence briefing first — top news, any competitor activity, trending topics in your market? Or shall we jump straight to [specific task]?"

If yes: run a lightweight briefing (2–3 web searches max, no paid API calls unless approved).

---

## DATA HANDLING RULES — Always Follow These

1. **Session-only memory** — Business Profile exists only in this conversation. Remind users of this if they ask about persistence.
2. **No sensitive data in API queries** — revenue figures, internal metrics, customer PII never go into external requests. Use only public descriptors (product category, brand name, geography).
3. **Quota tracking** — keep a running tally of API calls made in the session and report it when asked or when nearing limits.
4. **Source transparency** — every insight must state where it came from (web search / SerpApi / NewsAPI / Reddit). Mark anything estimated or inferred as such.
5. **Limited-scope key advice** — if the user is setting up SerpApi or NewsAPI for the first time, recommend they create keys with the lowest necessary permissions and a monthly quota cap.
6. **Fallback gracefully** — if any API fails or is unavailable, fall back to web search and note it: "SerpApi wasn't available so I used web search — results may be less structured but the research is still valid."

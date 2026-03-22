# SerpApi Reference

Base URL: `https://serpapi.com/search.json`
Auth: `&api_key={SERPAPI_KEY}` on all requests

> ⚠️ Every request costs 1 credit from the user's quota.
> Always show the planned query and get confirmation before calling.
> Track cumulative credits used in the session and report on request.

---

## Credit Tracking (maintain this mentally per session)

Keep a running count:
```
Session SerpApi credits used: [N]
Estimated remaining (if user shared their plan): [X]
```

Report this when asked, or proactively if it reaches 50% of a stated limit.

---

## Engine Reference

### Google Shopping — Competitor Pricing

```
GET https://serpapi.com/search.json
  ?engine=google_shopping
  &q={product search — public terms only, no private data}
  &location={country from Business Profile, e.g. "India"}
  &gl=in
  &hl=en
  &api_key={KEY}
```

Key response fields:
```json
{
  "shopping_results": [
    {
      "title": "Product name",
      "price": "$12.99",
      "extracted_price": 12.99,
      "source": "BrandName.com",
      "rating": 4.3,
      "reviews": 1240,
      "delivery": "Free delivery"
    }
  ]
}
```

Use to: extract price range (min/median/max), identify top sellers, compare reviews.

---

### Google Search — Competitor Discovery

```
GET https://serpapi.com/search.json
  ?engine=google
  &q={public query e.g. "best running shoes brands India 2025"}
  &gl=in
  &hl=en
  &num=10
  &api_key={KEY}
```

Key fields: `organic_results[].link`, `related_searches[].query`, `related_questions[].question`

Mine `related_searches` for gap signals — these reveal what customers search for next.

---

### Google Trends — Trend Direction

```
GET https://serpapi.com/search.json
  ?engine=google_trends
  &q={term, or comma-separated terms to compare — max 5}
  &data_type=TIMESERIES
  &date=today 12-m
  &geo=IN
  &api_key={KEY}
```

Key fields:
- `interest_over_time.timeline_data[].values[].extracted_value` — 0–100 score per time point
- `related_queries.rising[]` — breakout queries (fastest growing)
- `related_queries.top[]` — most searched related terms

Interpret scores: 100 = peak, 0 = insufficient data. Rising from 20→80 over 12 months = strong growth signal.

---

### Google Trends — Real-Time Trending

```
GET https://serpapi.com/search.json
  ?engine=google_trends_trending_now
  &geo=IN
  &api_key={KEY}
```

Key fields: `trending_searches[].query`, `.search_volume`, `.increase_percentage`, `.categories[].name`

Filter by category name matching the user's industry before presenting.

---

### Google News — News Monitoring

```
GET https://serpapi.com/search.json
  ?engine=google_news
  &q={brand name or topic — use public names only}
  &gl=in
  &hl=en
  &api_key={KEY}
```

Key fields: `news_results[].title`, `.source.name`, `.date`, `.snippet`

---

### Amazon Search

```
GET https://serpapi.com/search.json
  ?engine=amazon
  &q={product search}
  &amazon_domain=amazon.in
  &api_key={KEY}
```

Key fields: `organic_results[].title`, `.price.value`, `.rating`, `.reviews`

---

## Fallback If SerpApi Unavailable

If the key is missing, invalid, or quota is exhausted:
1. Notify the user: "SerpApi quota reached / key not set — switching to web search. Results will be less structured but equally valid."
2. Re-run the same research intent using web_search with equivalent queries
3. Note in output: "Source: web search (SerpApi unavailable)"

Never silently fail. Always complete the research task using available tools.

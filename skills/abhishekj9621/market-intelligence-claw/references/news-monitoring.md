# NewsAPI Reference

Base URL: `https://newsapi.org/v2/`
Auth: `&apiKey={NEWSAPI_KEY}` on all requests

> Free tier: 100 requests/day, articles from past month only.
> Every request costs 1 of the user's daily quota.
> Always show planned query and confirm before calling.
> Fallback: SerpApi Google News engine, or web_search for "[topic] news".

---

## Brand Monitoring

```
GET https://newsapi.org/v2/everything
  ?q="{brand name}"
  &language=en
  &sortBy=publishedAt
  &pageSize=10
  &from={30 days ago, YYYY-MM-DD format}
  &apiKey={KEY}
```

Use quoted brand name to get exact matches, not partial.

---

## Competitor News

```
GET https://newsapi.org/v2/everything
  ?q="{competitor name}" AND (launch OR funding OR sale OR controversy OR partnership)
  &language=en
  &sortBy=publishedAt
  &pageSize=5
  &apiKey={KEY}
```

---

## Industry Trends News

```
GET https://newsapi.org/v2/everything
  ?q={industry keyword} AND (trend OR growth OR market OR consumer OR demand)
  &language=en
  &sortBy=popularity
  &pageSize=10
  &apiKey={KEY}
```

---

## Response Structure

```json
{
  "totalResults": 47,
  "articles": [
    {
      "source": { "name": "Economic Times" },
      "title": "...",
      "description": "...",
      "url": "https://...",
      "publishedAt": "2025-03-15T10:30:00Z",
      "content": "..."
    }
  ]
}
```

Categorise articles found as:
- 🟢 Positive signal (funding, growth, awards)
- 🔴 Negative signal (controversy, layoffs, lawsuits)
- 🟡 Strategic signal (new product, new market, partnership)
- ℹ️ Informational (general industry coverage)

---

## Fallback If Unavailable

Use SerpApi Google News engine (`engine=google_news`) or web_search:
`"[brand name] news site:economictimes.com OR site:techcrunch.com"`

Note in output: "Source: web search (NewsAPI unavailable)"

# Reddit API Reference

Reddit is valuable for raw, unfiltered customer sentiment. Always use the official API
(not scraping) and respect rate limits.

**Cost:** Free for non-commercial use
**Rate limit:** 60 requests/minute with OAuth
**User-Agent required:** Always include `User-Agent: MarketIntelligenceSkill/1.0`

---

## Authentication

POST `https://www.reddit.com/api/v1/access_token`

```
Authorization: Basic {base64(client_id:client_secret)}
Content-Type: application/x-www-form-urlencoded
User-Agent: MarketIntelligenceSkill/1.0

Body: grant_type=client_credentials
```

Returns: `{ "access_token": "...", "expires_in": 86400 }`

All subsequent requests:
```
Authorization: Bearer {access_token}
User-Agent: MarketIntelligenceSkill/1.0
```

---

## Key Endpoints

### Search all of Reddit
```
GET https://oauth.reddit.com/search.json
  ?q={query}
  &sort=top
  &t=month
  &limit=25
```

### Search within a subreddit
```
GET https://oauth.reddit.com/r/{subreddit}/search.json
  ?q={query}
  &restrict_sr=true
  &sort=top
  &t=year
  &limit=25
```

---

## Useful Query Patterns

**Sentiment research (public brands/products only):**
- `"{brand} review"`
- `"{product type} recommendation"`
- `"{brand} worth it"`
- `"{brand} alternative"`
- `"{product} problems"`

**Unmet needs (gold for gap analysis):**
- `"wish there was a {product} that"`
- `"looking for {product} but can't find"`
- `"anyone know a good {product} for"`

---

## Privacy Rules for Reddit Queries

✅ Use: Public brand names, product categories, industry terms
❌ Never use: Customer names, emails, order IDs, private business data

Reddit posts are public, but do not extract or store personal information
about individual Reddit users from their posts.

---

## Industry Subreddits Reference

| Industry | Subreddits |
|---|---|
| Fashion | r/femalefashionadvice, r/malefashionadvice, r/streetwear |
| Electronics | r/gadgets, r/hardware, r/tech |
| Beauty/Skincare | r/SkincareAddiction, r/MakeupAddiction |
| Food/Beverage | r/food, r/coffee, r/tea |
| Home | r/HomeImprovement, r/malelivingspace |
| Fitness | r/fitness, r/bodyweightfitness |
| India-specific | r/india, r/IndiaShopping, r/IndiaInvestments |
| General shopping | r/BuyItForLife, r/frugal, r/deals |

---

## Fallback If Reddit API Unavailable

Use web_search:
- `site:reddit.com "{brand}" review`
- `site:reddit.com "{product type}" recommendation`

This finds Reddit posts via Google without needing API credentials.
Note in output: "Source: web search of Reddit (Reddit API not configured)"

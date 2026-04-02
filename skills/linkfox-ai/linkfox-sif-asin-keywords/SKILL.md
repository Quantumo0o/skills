---
name: linkfox-sif-asin-keywords
description: 使用SIF数据反查任意亚马逊ASIN的流量关键词，包括自然排名、广告排名、搜索量、流量占比和转化标记。当用户提到ASIN关键词分析、ASIN反查、流量关键词研究、自然排名查询、广告排名查询、关键词位置追踪、SIF关键词数据、竞品关键词窥探、查看哪些关键词为产品带来流量、分析特定ASIN的关键词表现、ASIN reverse keyword lookup, traffic keywords, organic ranking, ad ranking, search volume, SIF keywords, competitor keyword reverse lookup时触发此技能。即使用户未明确提及"SIF"，只要其需求涉及查找与特定亚马逊商品（ASIN）关联的关键词，也应触发此技能。
---

# SIF ASIN Keyword Analysis

This skill guides you on how to query and analyze traffic keywords for a specific Amazon ASIN, helping Amazon sellers understand which keywords drive traffic to a product and how that product ranks for each keyword.

## Core Concepts

SIF ASIN Keyword data reveals the keywords that bring traffic to a specific Amazon product (ASIN). For each keyword, you can see the product's organic search rank, SP ad rank, search volume, traffic share, display position types, and various performance markers. This is the go-to tool for reverse ASIN keyword lookup.

**Single-ASIN limitation**: This tool queries one ASIN at a time. If the user wants to compare multiple ASINs, you must make separate queries for each.

**Ranking logic**: A smaller rank value means a better (higher) position. Rank 1 means the product appears first in search results. When a user says "ranking improved", the numeric value decreased; "ranking dropped" means the value increased.

## Data Fields

| Field | API Name | Description | Example |
|-------|----------|-------------|---------|
| Keyword | keyword | The search keyword driving traffic | wireless charger |
| ASIN | asin | The product ASIN being queried | B0XXXXXXXX |
| Organic Rank | productNaturalRank | Product's position in organic search results | 5 |
| Organic Rank (Display) | naturalRankDisplay | Organic rank as display text | 5 |
| Ad Rank | productAdRank | Product's position in SP ad results | 3 |
| Ad Rank (Display) | adRankDisplay | Ad rank as display text | 3 |
| Weekly Search Volume | weeklySearchVolume | Estimated weekly searches for this keyword | 125000 |
| Keyword Popularity Rank | keywordPopularityRank | Keyword's search volume rank among all keywords (lower = more popular) | 203 |
| Traffic Share | trafficShare | Share of traffic this keyword contributes to the ASIN (1 = 100%) | 0.05 |
| Display Position Types | displayPositionTypes | Where the product appears: natural, ac, sp, top, bottom, er, vedio, tr, trfob | ["natural", "sp"] |
| Traffic Characteristic Markers | trafficCharacteristicMarkers | Traffic feature tags: isMainKw, isAccurateKw, isAccurateAboveKw, isAccurateTailKw | ["isMainKw"] |
| Conversion Performance Markers | conversionPerformanceMarkers | Conversion tags: isPurchaseKw, isQualityKw, isStableKw, isLossKw, isInvalidKw | ["isPurchaseKw"] |
| Last Organic Rank Time | lastNaturalRankTime | When the product last had a valid organic rank for this keyword | 2025-03-20 |
| Last Ad Rank Time | lastAdRankTime | When the product last had a valid SP ad rank for this keyword | 2025-03-20 |
| Update Time | updateTime | When the keyword data was last updated | 2025-03-21 |

## Supported Marketplaces

US (United States), CA (Canada), MX (Mexico), UK (United Kingdom), DE (Germany), FR (France), IT (Italy), ES (Spain), JP (Japan), IN (India), AU (Australia), BR (Brazil), NL (Netherlands), SE (Sweden), PL (Poland), TR (Turkey), AE (United Arab Emirates), SA (Saudi Arabia), SG (Singapore)

Default marketplace is **US**. Use US when the user does not specify a marketplace.

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/sif_asin_keywords.py` directly to run queries.

## Parameter Guide

### Required Parameter

- **asin** (string, required): The Amazon ASIN to look up. Only one ASIN per request.

### Optional Parameters

- **country** (string, default `US`): Marketplace code. See Supported Marketplaces above.
- **keyword** (string): Filter results to keywords containing this text. Translate the keyword into the language of the target marketplace when possible.
- **conditions** (string): Comma-separated condition filters. Available values:
  - `nfPosition` -- organic traffic keywords
  - `isSpAd` -- SP ad keywords
  - `isBrandAd` -- brand ad keywords
  - `isVedioAd` -- video ad keywords
  - `isAC` -- Amazon's Choice keywords
  - `isER` -- Editorial Recommendations keywords
  - `isTr` -- Top Rated keywords
  - `isMainKw` -- main traffic keywords
  - `isAccurateKw` -- precise traffic keywords
  - `isAccurateAboveKw` -- precise high-volume keywords
  - `isAccurateTailKw` -- precise long-tail keywords
  - `isPurchaseKw` -- purchase-converting keywords
  - `isQualityKw` -- high-quality conversion keywords
  - `isStableKw` -- stable conversion keywords
  - `isLossKw` -- conversion-loss keywords
  - `isInvalidKw` -- invalid-exposure keywords
- **sortBy** (string): Sort field. Options: `lastRank` (organic rank), `adLastRank` (ad rank), `updateTime` (update time), `searchesRank` (search popularity rank), `estSearchesNum` (monthly search volume).
- **desc** (boolean, default `true`): Sort in descending order. Set to `false` for ascending.
- **pageNum** (integer, default `1`): Page number for pagination.
- **pageSize** (integer, default `100`, range 10-100): Number of results per page.

### Building Effective Queries

1. **Always specify the marketplace**: Set `country` to the correct marketplace code.
2. **Use keyword filtering**: When the user is interested in specific keywords, pass the `keyword` parameter to narrow results.
3. **Apply condition filters**: Use `conditions` to focus on specific keyword types (e.g., only organic keywords, only purchase-converting keywords).
4. **Choose appropriate sorting**: Sort by `estSearchesNum` for highest search volume keywords, or by `lastRank` for best-ranking keywords.
5. **Handle pagination**: The API returns at most 100 results per page. Use `pageNum` to retrieve additional pages if the total exceeds 100.

## Usage Examples

**1. Find all traffic keywords for an ASIN on the US marketplace**
```
asin: "B0XXXXXXXX", country: "US"
```

**2. Find organic traffic keywords only**
```
asin: "B0XXXXXXXX", country: "US", conditions: "nfPosition"
```

**3. Find keywords containing "charger" sorted by search volume (ascending)**
```
asin: "B0XXXXXXXX", country: "US", keyword: "charger", sortBy: "estSearchesNum", desc: false
```

**4. Find main traffic keywords that are converting (purchase keywords)**
```
asin: "B0XXXXXXXX", country: "US", conditions: "isMainKw,isPurchaseKw"
```

**5. Find SP ad keywords on the Japan marketplace**
```
asin: "B0XXXXXXXX", country: "JP", conditions: "isSpAd", sortBy: "adLastRank", desc: false
```

**6. Find precise long-tail keywords with high conversion**
```
asin: "B0XXXXXXXX", country: "US", conditions: "isAccurateTailKw,isQualityKw"
```

## Display Rules

1. **Present data only**: Show query results in clear tables without subjective business advice.
2. **Ranking clarification**: When showing ranking data, remind users that lower numeric values mean better (higher) positions.
3. **Traffic share formatting**: Display traffic share as a percentage (multiply by 100). For example, 0.05 should be shown as 5%.
4. **Marker translation**: Translate marker arrays into human-readable labels. For example, `["isMainKw", "isAccurateKw"]` should display as "Main Traffic, Precise Traffic".
5. **Display position translation**: Translate position type arrays into readable labels: natural = Organic, ac = Amazon's Choice, sp = SP Ad, top = Top Brand Ad, bottom = Bottom Brand Ad, er = Editorial Recommendation, vedio = Video Ad, tr = Top Rated, trfob = Top Rated Frequently Bought.
6. **Pagination notice**: When results have more pages, inform the user of the total count and suggest fetching additional pages.
7. **Error handling**: When a query fails, explain the reason based on the `msg` field and suggest adjusting query parameters.
8. **Multi-ASIN requests**: If the user asks about multiple ASINs, make separate API calls for each and present the results together.
## Important Limitations

- **Single ASIN per request**: Only one ASIN can be queried at a time.
- **Page size cap**: Maximum 100 results per page.
- **Keyword language**: The `keyword` filter should ideally be in the language of the target marketplace.

## User Expression & Scenario Quick Reference

**Applicable** -- Keyword analysis for specific Amazon products:

| User Says | Scenario |
|-----------|----------|
| "What keywords does this ASIN rank for" | Reverse ASIN keyword lookup |
| "Show me the traffic keywords for B0XXX" | Traffic keyword analysis |
| "What's the organic rank for this product" | Organic ranking check |
| "Which keywords is this product advertising on" | Ad keyword analysis |
| "Find high-converting keywords for this ASIN" | Conversion keyword mining |
| "What are the main traffic sources for this product" | Main traffic keyword identification |
| "Show me keywords with lost conversions" | Conversion loss diagnosis |
| "Which keywords have Amazon's Choice badge" | AC keyword discovery |
| "Compare keyword rankings for my ASIN" | Keyword position analysis |

**Not applicable** -- Needs beyond single-ASIN keyword lookup:
- Broad keyword research not tied to a specific ASIN (use ABA data tools instead)
- Product reviews, listing copywriting
- Sales estimation, revenue analysis
- Advertising campaign management (bids, budgets)
- Category-wide keyword trends without a specific ASIN


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*

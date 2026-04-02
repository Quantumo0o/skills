---
name: linkfox-sif-keyword-traffic
description: 亚马逊商品的关键词流量来源分析，涵盖自然搜索、SP广告、品牌广告和推荐位。当用户提到关键词流量结构、流量来源拆解、自然流量与付费流量比例、SP广告曝光、品牌广告占比、搜索展示分析、Amazon's Choice或编辑推荐曝光、关键词竞争格局、ASIN流量构成、keyword traffic, traffic structure analysis, search share, ad share, traffic source distribution, SIF, traffic analysis时触发此技能。即使用户未明确提及"SIF"，只要其需求涉及分析ASIN的关键词流量来源及其在不同渠道的分布，也应触发此技能。
---

# SIF Keyword Traffic Source Summary

This skill guides you on how to query and analyze keyword traffic source data for Amazon products, helping sellers understand the traffic structure behind keywords — including organic search, Sponsored Products (SP) ads, brand ads, video ads, and various Amazon recommendation placements.

## Core Concepts

The SIF Keyword Summary tool provides a comprehensive breakdown of how an Amazon product's keyword traffic is distributed across multiple channels. It answers the fundamental question: **Where does the traffic come from for a given keyword?**

**Traffic channels analyzed:**

- **Natural Search** — organic search result positions
- **SP Ads (Sponsored Products)** — paid product ad placements
- **Brand Ads** — top and bottom brand ad placements on the search results page
- **Video Ads** — video ad placements
- **Amazon's Choice (AC)** — Amazon's Choice badge recommendations
- **Editorial Recommendations (ER)** — editorial/curated recommendation placements
- **Top Rated (TR)** — high-rating recommendation placements
- **Top Rated Frequently Bought (TRFOB)** — high-rating, frequently bought recommendation placements

**Exposure scores and ratios**: Each channel has an exposure score (absolute value reflecting impression volume) and an exposure ratio (percentage of total exposure). Higher scores mean more impressions in that channel; ratios show the relative weight of each channel in the product's overall traffic mix.

## Parameter Guide

### Required Parameter

| Parameter | Type | Description |
|-----------|------|-------------|
| searchKeyword | string | The search keyword to analyze. Translate to the target marketplace's language when applicable. Max 1000 characters. |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| country | string | US | Marketplace code. See Supported Marketplaces below. |
| condition | string | (none) | Filter by a specific traffic source. Only one value per request. See Condition Filters below. |
| pageNum | integer | 1 | Page number for pagination. |
| pageSize | integer | 100 | Results per page. Min 10, max 100. |
| desc | boolean | true | Sort in descending order. |

### Supported Marketplaces

US (United States), CA (Canada), MX (Mexico), UK (United Kingdom), DE (Germany), FR (France), IT (Italy), ES (Spain), JP (Japan), IN (India), AU (Australia), BR (Brazil), NL (Netherlands), SE (Sweden), PL (Poland), TR (Turkey), AE (United Arab Emirates), SA (Saudi Arabia), SG (Singapore)

Default marketplace is **US**. Use US when the user does not specify a marketplace.

### Condition Filters

Each request can include at most **one** condition filter:

| Value | Meaning |
|-------|---------|
| nfPosition | Natural search traffic keywords |
| isSpAd | SP ad keywords |
| isTopAd | Top brand ad keywords |
| isBottomAd | Bottom brand ad keywords |
| isVedioAd | Video ad keywords |
| isAC | Amazon's Choice keywords |
| isER | Editorial Recommendations keywords |
| isTR | Top Rated keywords |
| isTRFOB | Top Rated Frequently Bought keywords |
| isBrandAd | Brand ad keywords (top + bottom combined) |
| isPPCAd | PPC ad keywords (all paid ad types) |
| isSearchRecommend | Search recommendation keywords |

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/sif_keyword_traffic.py` directly to run queries.

## Usage Examples

**1. Basic keyword traffic overview**
Query the traffic source breakdown for a keyword in the US marketplace:
```
searchKeyword: "wireless charger", country: "US"
```

**2. Filter for organic search traffic only**
See only ASINs that appear in natural search results for a keyword:
```
searchKeyword: "wireless charger", country: "US", condition: "nfPosition"
```

**3. Analyze SP ad competition**
Find which ASINs are running SP ads for a keyword:
```
searchKeyword: "wireless charger", country: "US", condition: "isSpAd"
```

**4. Check Amazon's Choice badge holders**
Identify ASINs that hold the Amazon's Choice badge for a keyword:
```
searchKeyword: "wireless charger", country: "US", condition: "isAC"
```

**5. Keyword analysis for a non-US marketplace**
Analyze traffic sources in the Japan marketplace (use the local language keyword):
```
searchKeyword: "ワイヤレス充電器", country: "JP"
```

**6. Paginated results**
Retrieve the second page of results with 50 items per page:
```
searchKeyword: "phone case", country: "US", pageNum: 2, pageSize: 50
```

## Display Rules

1. **Present data clearly**: Show query results in well-structured tables. Group data by traffic channel exposure ratios for easy comparison.
2. **Highlight key ratios**: When displaying results, emphasize the natural search exposure ratio vs. paid ad exposure ratio to help users quickly assess the organic-to-paid balance.
3. **Translate field names**: Present field names in user-friendly language rather than raw API field names (e.g., "Natural Search Exposure Ratio" instead of "naturalSearchExposureRatio").
4. **Volume notice**: When results are large (high total count), show core data and remind users they can paginate to see more results.
5. **Error handling**: When a query fails, explain the reason based on the `msg` field and suggest adjusting query parameters (e.g., checking keyword spelling or marketplace code).
6. **Percentage formatting**: Display exposure ratios as percentages (e.g., 0.45 as "45%") for readability.
7. **Traffic source summary**: When presenting a single ASIN's data, provide a brief traffic composition summary (e.g., "This product gets 60% of its exposure from organic search, 25% from SP ads, and 15% from brand ads").
## Important Limitations

- **Single condition filter**: Only one `condition` value can be used per request. To compare multiple traffic sources, make separate requests.
- **Keyword language**: The `searchKeyword` should be in the language of the target marketplace for best results.
- **Result cap**: Each page returns at most 100 records.
- **Parent ASIN awareness**: The response includes `isParentAsin` to indicate whether the searched keyword resolves to a parent ASIN, and `variantsNum` / `noKeywordVariantsNum` for variant counts.

## User Expression & Scenario Quick Reference

**Applicable** — Traffic source and competition structure analysis for Amazon keywords:

| User Says | Scenario |
|-----------|----------|
| "Where does the traffic come from for this keyword" | Traffic source breakdown |
| "How much organic vs paid traffic" | Organic/paid ratio analysis |
| "Who's running SP ads for this keyword" | SP ad competition analysis |
| "Which products have Amazon's Choice" | AC badge analysis |
| "Is this keyword dominated by ads" | Ad saturation assessment |
| "Show me the brand ad competition" | Brand ad landscape analysis |
| "Traffic structure for my competitor's keyword" | Competitive traffic analysis |
| "Which products get editorial recommendations" | ER placement analysis |

**Not applicable** — Needs beyond keyword traffic source analysis:
- Historical keyword ranking trends (use ABA data tools)
- Advertising bid/budget optimization
- Product reviews or listing content
- Sales volume estimation
- Keyword search volume over time


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*

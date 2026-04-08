# Product Pricing Scraper Notes

## Failure patterns seen in prior scraper runs

1. Temporary 429 responses on high-profile publisher sites
2. Inconsistent price selectors across ecommerce themes
3. Missing structured product data on content-heavy pages
4. Need to separate "request failed" from "page fetched but no price extracted"

## Design decisions

- Retry on 429 and common 5xx statuses
- Add jitter plus exponential backoff
- Prefer JSON-LD product data when available
- Fall back to meta tags, then broad CSS selectors
- Preserve source fields so extraction provenance is visible

## Non-goals

- Full anti-bot bypass
- JavaScript rendering
- Marketplace-specific checkout parsing

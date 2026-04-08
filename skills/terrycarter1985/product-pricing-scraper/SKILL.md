---
name: product-pricing-scraper
description: Extract normalized product pricing data from retail or ecommerce pages using HTML parsing with retry, backoff, and safe defaults.
tags: [scraping, ecommerce, pricing, extraction]
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "homepage": "https://clawhub.com",
      "capabilities": ["html-fetch", "price-normalization", "selector-fallbacks"]
    }
  }
---

# Product Pricing Scraper

Use this skill when you need to pull product pricing details from a product page or a small list of product pages and return normalized JSON.

## What it extracts

- product title
- current price
- original/list price when available
- currency
- availability / stock text
- product URL
- source hints from JSON-LD, meta tags, and visible DOM selectors

## Why this skill exists

Pricing pages are noisy and inconsistent. This skill combines:

1. structured data extraction (JSON-LD)
2. Open Graph / meta tag fallbacks
3. CSS selector fallbacks
4. retry + backoff for temporary failures like 429/5xx

That makes it more reliable than a single-selector scraper.

## Inputs

Provide one or more URLs.

Optional knobs:

- `--config <path>` for selector overrides
- `--delay <seconds>` to slow requests
- `--timeout <seconds>` to adjust request timeout

## Output

JSON array of normalized pricing records.

## Run locally

```bash
python3 scraper.py https://example.com/product/sku123
python3 scraper.py urls.txt --input-file
python3 scraper.py https://example.com/product/sku123 --pretty
```

## Example output

```json
[
  {
    "url": "https://example.com/product/sku123",
    "title": "Example Product",
    "currency": "USD",
    "price": 19.99,
    "original_price": 29.99,
    "availability": "InStock",
    "source": {
      "price": "jsonld.offers.price",
      "currency": "jsonld.offers.priceCurrency",
      "title": "meta[property='og:title']"
    }
  }
]
```

## Files

- `scraper.py` — main scraper CLI
- `selectors.json` — default selector and field fallback config
- `examples/sample_urls.txt` — batch input example
- `references/notes.md` — implementation notes and failure patterns

## Good defaults built from prior runs

This skill bakes in lessons from earlier scraping runs:

- back off on 429 and common 5xx responses
- reuse multiple price selectors because ecommerce themes vary widely
- prefer structured product data when present
- keep missing `price` distinct from request failure

## Publish

```bash
clawhub publish skills/product-pricing-scraper --slug product-pricing-scraper --name "Product Pricing Scraper" --version 1.0.0 --changelog "Initial release with retry/backoff, JSON-LD extraction, and selector fallbacks"
```

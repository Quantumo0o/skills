---
name: ntriq-alt-text-batch
description: "Batch-process multiple images to generate AI-powered alt text descriptions for accessibility. Supports up to 500 images per run."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [accessibility,image]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Alt Text Batch

Batch-process up to 500 images per run to generate AI-powered alt text for accessibility compliance. Input a list of image URLs or base64 data; receive structured alt text and detailed descriptions for each.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | List of image URLs or base64-encoded strings (max 500) |
| `language` | string | ❌ | Output language (default: `en`) |
| `detail_level` | string | ❌ | `brief` or `detailed` (default: `brief`) |
| `context` | string | ❌ | Page context hint for better relevance |

## Example Response

```json
{
  "results": [
    {
      "index": 0,
      "alt_text": "Bar chart showing Q1 revenue by region",
      "description": "A horizontal bar chart comparing revenue across four regions. North America leads at $4.2M, followed by EMEA at $3.1M, APAC at $2.8M, and LATAM at $1.4M.",
      "confidence": 0.94
    }
  ],
  "processed": 1,
  "failed": 0
}
```

## Use Cases

- E-commerce product catalog accessibility audits
- CMS image library retroactive alt text generation
- WCAG 2.1 compliance automation for media teams

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/alt-text-batch) · [x402 micropayments](https://x402.ntriq.co.kr)

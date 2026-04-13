---
name: ntriq-blueprint-intelligence
description: "AI-powered architectural blueprint analysis. Extract floor plans, structural elements, dimensions, rooms, materials, and more from construction and engineering drawings."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [construction,vision]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Blueprint Intelligence

AI-powered architectural blueprint analysis using vision AI. Upload construction drawings, floor plans, or engineering schematics to extract structured data: rooms, dimensions, materials, structural elements, and compliance annotations.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ | URL to blueprint image (PNG, PDF page, TIFF) |
| `extract_dimensions` | boolean | ❌ | Extract room measurements (default: true) |
| `scale` | string | ❌ | Drawing scale e.g. `1:100` (auto-detected if omitted) |
| `output_format` | string | ❌ | `json` or `svg_overlay` (default: `json`) |

## Example Response

```json
{
  "rooms": [
    {"name": "Living Room", "area_sqm": 28.4, "dimensions": "5.2m x 5.46m"},
    {"name": "Kitchen", "area_sqm": 12.1, "dimensions": "3.3m x 3.67m"}
  ],
  "total_area_sqm": 142.6,
  "structural_elements": ["load-bearing wall (north)", "steel beam span 6m"],
  "materials_noted": ["reinforced concrete", "timber frame"],
  "compliance_flags": []
}
```

## Use Cases

- Real estate due diligence automation
- Construction project takeoff and cost estimation
- Building permit review pre-screening

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/blueprint-intelligence) · [x402 micropayments](https://x402.ntriq.co.kr)

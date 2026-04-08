---
name: ntriq-country-risk-copilot-mcp
description: "Country risk assessment for business operations. Political stability, economic indicators, and compliance risks."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [risk,geopolitics,compliance]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Country Risk Copilot MCP

Country risk assessment for business operations: political stability, economic indicators, regulatory compliance exposure, and sanctions risk. Returns composite risk score across 195 countries using live multi-source data.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | ✅ | Country name or ISO 3166-1 alpha-2 code |
| `dimensions` | array | ❌ | Risk categories: `political`, `economic`, `sanctions`, `disaster` |
| `industry` | string | ❌ | Sector context affects weighting: `finance`, `manufacturing`, `tech` |

## Example Response

```json
{
  "country": "Myanmar",
  "iso": "MM",
  "composite_risk_score": 88,
  "risk_level": "very_high",
  "dimensions": {
    "political": {"score": 91, "drivers": ["military coup 2021", "civil conflict ongoing"]},
    "economic": {"score": 79, "gdp_growth": -18.4, "inflation": 26.1},
    "sanctions": {"score": 95, "active_programs": ["OFAC Myanmar", "EU Myanmar"]},
    "disaster": {"score": 62, "flood_risk": "high", "cyclone_exposure": "moderate"}
  }
}
```

## Use Cases

- FDI risk assessment before market entry
- Supply chain geographic risk monitoring
- Insurance underwriting country risk scoring

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/country-risk-copilot-mcp) · [x402 micropayments](https://x402.ntriq.co.kr)

---
name: ntriq-country-risk-monitor
description: "Free country risk assessment API for supply chain, FDI, and trade compliance. Screen OFAC sanctions, World Bank economic indicators, disaster risk, and geopolitical exposure. No API keys required. ..."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [risk]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Country Risk Monitor

Free country risk assessment API combining OFAC sanctions, World Bank economic indicators, USGS disaster data, and geopolitical exposure scoring. No API keys required. 195 countries covered. Replaces expensive commercial country risk subscriptions.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_code` | string | ✅ | ISO 3166-1 alpha-2 (e.g., `CN`, `RU`, `NG`) |
| `indicators` | array | ❌ | World Bank indicator codes (e.g., `NY.GDP.MKTP.CD`) |
| `include_sanctions` | boolean | ❌ | Include OFAC program list (default: true) |

## Example Response

```json
{
  "country": "Nigeria",
  "iso2": "NG",
  "sanctions_programs": [],
  "economic": {
    "gdp_usd": 477000000000,
    "gdp_growth_pct": 2.9,
    "inflation_pct": 22.4,
    "unemployment_pct": 4.3
  },
  "disaster_risk": {"earthquake": "low", "flood": "high", "drought": "high"},
  "risk_summary": "Elevated economic volatility. High flood risk in Niger Delta. No active US sanctions."
}
```

## Use Cases

- Trade finance country limit setting
- Export compliance country classification
- Global staffing risk assessment for HR

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/country-risk-monitor) · [x402 micropayments](https://x402.ntriq.co.kr)

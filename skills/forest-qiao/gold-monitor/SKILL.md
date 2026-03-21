---
name: gold-monitor
description: Query real-time gold, USD index, and oil prices from China and international markets
---

# Gold Monitor

Real-time price query tool for gold (China Au99.99 & COMEX), USD index (DXY), and WTI crude oil. Data sourced from Shanghai Gold Exchange and Sina Finance.

## When to Use

Use this skill when the user asks about:
- Gold prices (domestic or international)
- USD index / DXY
- Oil prices / WTI crude
- Commodity market overview

## Setup

Before first use, install dependencies:

```bash
pip install -r {{SKILL_DIR}}/requirements.txt
```

## Usage

Query all assets at once:

```bash
python3 {{SKILL_DIR}}/query.py all
```

Query a single asset:

```bash
python3 {{SKILL_DIR}}/query.py AU9999   # China gold (CNY/gram)
python3 {{SKILL_DIR}}/query.py XAUUSD   # International gold (USD/oz)
python3 {{SKILL_DIR}}/query.py USIDX    # USD index (DXY)
python3 {{SKILL_DIR}}/query.py WTI      # WTI crude oil (USD/barrel)
```

## Output

The script prints JSON to stdout. Example for a single asset:

```json
{
  "name": "国际黄金 COMEX",
  "symbol": "XAUUSD",
  "price": 3050.12,
  "change": 15.30,
  "change_pct": 0.50,
  "unit": "USD/oz",
  "update_time": "2026-03-19 10:30:00"
}
```

For `all`, the output is an array of 4 such objects.

If an `"error"` field is present, that asset's data could not be fetched — tell the user.

Parse the JSON and present it in a clear, readable format with price, change, change percentage, and unit.

## Network Access

This skill makes outbound HTTP requests to the following hosts only:
- `hq.sinajs.cn` — Sina Finance real-time quotes (international gold, USD index, WTI oil)
- akshare API endpoints — Shanghai Gold Exchange data (China gold Au99.99)

No credentials or API keys are required. All requests are read-only.

## Data Sources

- **China Gold (Au99.99)** — Shanghai Gold Exchange via akshare
- **International Gold (COMEX)** — Sina Finance real-time quotes
- **USD Index (DXY)** — Sina Finance real-time quotes
- **WTI Crude Oil** — Sina Finance real-time quotes

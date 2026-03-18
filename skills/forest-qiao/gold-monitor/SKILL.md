---
name: gold-monitor
description: Real-time gold, USD index, and oil price monitoring with Feishu webhook alerts
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
      env: []
    emoji: "📈"
---

# Gold Monitor

Real-time monitoring dashboard for gold prices (China Au99.99 & COMEX), USD index (DXY), and WTI crude oil. Includes configurable price alerts with Feishu (Lark) webhook notifications.

## Quick Start

```bash
# Install dependencies and start the service
bash setup.sh
```

Or manually:

```bash
pip install -r requirements.txt
python3 app.py
```

The dashboard will be available at **http://127.0.0.1:8000**.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web dashboard UI |
| GET | `/api/prices` | Current prices for all monitored assets |
| GET | `/api/history/{symbol}` | Historical K-line data. Symbols: `AU9999`, `XAUUSD`, `USIDX`, `WTI` |
| GET | `/api/alerts` | List all alert rules and webhook config |
| POST | `/api/alerts` | Add an alert rule (JSON body) |
| DELETE | `/api/alerts/{rule_id}` | Delete an alert rule |
| POST | `/api/webhook` | Set Feishu webhook URL |
| POST | `/api/alerts/test` | Send a test notification |

### Add Alert Rule (POST /api/alerts)

```json
{
  "symbol": "AU9999",
  "condition": "price_above",
  "threshold": 680,
  "note": "Gold price alert"
}
```

Conditions: `price_above`, `price_below`, `change_pct_above`, `change_pct_below`

### Set Webhook (POST /api/webhook)

```json
{
  "url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
}
```

## Configuration

- **Alert rules and webhook URL** are persisted in `config.json` (auto-created).
- **Polling interval**: Prices refresh every 60 seconds.
- **Alert cooldown**: 30 minutes between repeated alerts for the same rule.
- **Bind address**: Defaults to `127.0.0.1:8000`. Edit `app.py` to change.

## Data Sources

- **China Gold (Au99.99)**: Shanghai Gold Exchange via akshare
- **International Gold (COMEX)**: Sina Finance real-time quotes
- **USD Index (DXY)**: Sina Finance real-time quotes
- **WTI Crude Oil**: Sina Finance real-time quotes

## Troubleshooting

- **akshare import errors**: Ensure `pip install akshare` completed successfully. Some systems may need `pip install --upgrade akshare`.
- **No data returned**: The Sina Finance API may be unavailable outside certain regions. The service will show cached data or zeros on failure.
- **Port already in use**: Change the port in `app.py` (`uvicorn.run(..., port=XXXX)`).

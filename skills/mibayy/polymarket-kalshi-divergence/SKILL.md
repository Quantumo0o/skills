---
name: polymarket-kalshi-divergence
description: >
  Cross-platform arbitrage between Kalshi and Polymarket. Monitors 13 Kalshi event
  series (crypto, macro, politics) and compares prices to equivalent Polymarket
  markets. Generates BUY signals when gap exceeds 8% and SELL signals above 10%.
metadata:
  author: "Mibayy"
  version: "1.0.0"
  displayName: "Kalshi-Polymarket Divergence Arb"
  difficulty: "intermediate"
---

# Kalshi-Polymarket Divergence Arb

Cross-platform price divergence trading between Kalshi and Polymarket.

## What It Does

Polls Kalshi's public API for live prices across 13 event series and compares
them to equivalent Polymarket markets found via SimmerClient. When prices diverge
beyond threshold, the cheaper side is likely underpriced.

## Covered Series

| Series | Category | Description |
|--------|----------|-------------|
| KXBTC, KXETH, KXSOL, KXXRP, KXDOGE | Crypto | Price threshold markets |
| KXFED | Macro | Fed rate decisions |
| KXCPI | Macro | CPI prints |
| KXUNEMP | Macro | Unemployment data |
| KXGLD, KXOIL | Commodities | Price threshold markets |
| KXNASDAQ, KXSPY, KXINX | Indices | Index level markets |

## Signal Logic

- **BUY** — Polymarket price is >8% below Kalshi equivalent (Polymarket underpriced)
- **SELL** — Polymarket price is >10% above Kalshi equivalent (Polymarket overpriced)
- Asymmetric thresholds account for Polymarket's typically lower liquidity

## Usage

```bash
python kalshi_divergence.py                  # dry run
python kalshi_divergence.py --live           # real trades
python kalshi_divergence.py --live --quiet   # cron mode
```

> 🧪 **Remixable Template** — Fork this skill to add new Kalshi series, adjust
> divergence thresholds, or add position sizing based on gap magnitude.

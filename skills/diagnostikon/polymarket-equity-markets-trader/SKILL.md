---
name: polymarket-equity-markets-trader
description: Trades Polymarket prediction markets on stock index milestones, major IPOs, earnings surprises, analyst upgrades, and company-specific financial events.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Equity Markets & IPO Trader
  difficulty: advanced
---

# Equity Markets & IPO Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Options implied volatility vs Polymarket price divergence on earnings events. VIX spikes as timing signal for market direction markets.

## Edge Thesis

Equity prediction markets are unique because they run in parallel with deep, liquid financial markets. The edge is in the LAG: S&P 500 level markets on Polymarket take 20–60 minutes to reprice after major macro events (CPI, payrolls, FOMC) compared to the futures market. Also: options market implied move for earnings (available from any options data API) gives a direct probability estimate for earnings-beat markets — Polymarket consistently misprices vs the options-implied range.

### Remix Signal Ideas
- **Yahoo Finance API (unofficial)**: https://finance.yahoo.com/ — Real-time quotes, implied volatility, historical prices
- **CBOE VIX data feed**: https://www.cboe.com/tradable_products/vix/ — VIX level and futures term structure — fear gauge timing signal
- **SEC EDGAR API**: https://efts.sec.gov/LATEST/search-index?q= — Real-time 8-K filings — earnings releases hit EDGAR before press coverage

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | See clawhub.json | Max USDC per trade |
| `SIMMER_MIN_VOLUME` | See clawhub.json | Min market volume filter |
| `SIMMER_MAX_SPREAD` | See clawhub.json | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | See clawhub.json | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | See clawhub.json | Max concurrent open positions |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk

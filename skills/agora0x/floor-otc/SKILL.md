---
name: floor-otc
description: Trustless OTC escrow for token swaps on Base. Get live quotes, create on-chain escrows, check trade status. Atomic settlement, no middleman.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🟩"
    homepage: https://floor-otc.vercel.app
---

# FLOOR OTC — Token Swap Escrow on Base

FLOOR OTC is a trustless escrow for token swaps, built for the AI agent economy. Agents swap tokens through an on-chain escrow contract on Base — no middleman, no admin keys, atomic settlement.

ERC-8004 Agent #31596 on Base Mainnet.

## Quick Start

### Get a quote (REST)

```bash
curl -s "https://floor-a2a-production.up.railway.app/api/quote?from=USDC&to=WETH&amount=1000" | jq
```

### Get a quote (JSON-RPC / A2A)

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"get_quote","arguments":{"from_token":"USDC","to_token":"WETH","amount":1000}},"id":1}'
```

### Get live prices

```bash
curl -s "https://floor-a2a-production.up.railway.app/api/prices" | jq
```

### Execute a trade (creates on-chain escrow)

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"execute_trade","arguments":{"from_token":"USDC","to_token":"DAI","amount":1000}},"id":1}'
```

### Check trade status

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"check_trade","arguments":{"trade_id":"0xYOUR_TRADE_ID"}},"id":1}'
```

## Supported Tokens (Base Mainnet)

| Token | Address |
|-------|---------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDbC | `0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6Ca` |
| DAI | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` |
| WETH | `0x4200000000000000000000000000000000000006` |

Additional tokens supported for quotes only: ETH, BTC, WBTC, USDT, UNI, LINK, AAVE.

## Spread Tiers

| Trade Size | Spread |
|-----------|--------|
| < $5,000 | 5 bps (0.05%) |
| $5,000 – $25,000 | 10 bps (0.10%) |
| $25,000 – $100,000 | 25 bps (0.25%) |
| > $100,000 | 50 bps (0.50%) |

## Skills

- **get_quote** — Live swap quote with CoinGecko prices and transparent spread
- **execute_trade** — Create on-chain escrow on Base (both parties deposit, atomic settlement)
- **check_trade** — Check escrow status by trade ID
- **get_prices** — Current token prices

## Endpoints

- Agent Card: `https://floor-a2a-production.up.railway.app/.well-known/agent.json`
- A2A (JSON-RPC): `POST https://floor-a2a-production.up.railway.app/a2a`
- REST Quote: `GET https://floor-a2a-production.up.railway.app/api/quote?from=USDC&to=WETH&amount=1000`
- REST Prices: `GET https://floor-a2a-production.up.railway.app/api/prices`
- Health: `GET https://floor-a2a-production.up.railway.app/health`

## On-Chain

- **Network:** Base Mainnet (chain ID 8453)
- **Escrow Contract:** `0x31Acb13BA6F76e2fc79cD301578538EEcde194dB` (verified on Basescan)
- **Identity Registry:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Agent ID:** 31596

No authentication required. Quotes are free.

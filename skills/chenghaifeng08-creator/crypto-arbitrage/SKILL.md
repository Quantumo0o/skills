---
name: crypto-arbitrage
description: Real-time cryptocurrency arbitrage scanner across multiple exchanges. Detect price discrepancies, calculate profitable opportunities, and execute arbitrage trades automatically.
version: 1.0.0
author: OpenClaw Agent
tags:
  - crypto
  - arbitrage
  - trading
  - multi-exchange
  - binance
  - coinbase
  - kraken
  - automation
homepage: https://github.com/openclaw/skills/crypto-arbitrage
metadata:
  openclaw:
    emoji: 🔄
    pricing:
      basic: "59 USDC"
      pro: "119 USDC (with auto-execution)"
---

# Crypto Arbitrage 🔄

**Real-time cryptocurrency arbitrage scanner and executor.**

Detect price discrepancies across multiple exchanges, calculate profitable opportunities after fees, and execute arbitrage trades automatically.

---

## 🎯 What It Solves

Crypto traders miss opportunities because:
- ❌ Can't monitor multiple exchanges simultaneously
- ❌ Manual calculation is too slow
- ❌ Fees eat into profits unexpectedly
- ❌ Withdrawal times kill opportunities
- ❌ No systematic approach to arbitrage
- ❌ Missing triangular arbitrage opportunities

**Crypto Arbitrage** provides:
- ✅ Real-time multi-exchange price monitoring
- ✅ Instant profit calculation (including fees)
- ✅ Withdrawal time awareness
- ✅ Auto-execution for fast opportunities
- ✅ Triangular arbitrage detection
- ✅ Risk-adjusted opportunity scoring

---

## ✨ Features

### 📊 Multi-Exchange Scanning
- Support for 20+ exchanges (Binance, Coinbase, Kraken, OKX, Bybit, etc.)
- Real-time price feeds via WebSocket
- Order book depth analysis
- Liquidity assessment
- Historical spread tracking

### 💰 Opportunity Detection
- Spatial arbitrage (same asset, different exchanges)
- Triangular arbitrage (3+ pairs on same exchange)
- Cross-border arbitrage (USD vs USDT vs other stablecoins)
- Futures-spot basis arbitrage
- Funding rate arbitrage

### 🧮 Profit Calculation
- Real-time fee calculation (maker/taker)
- Withdrawal fee inclusion
- Network gas fee estimation
- Slippage estimation
- Net profit after all costs
- ROI and annualized return

### ⚡ Auto-Execution
- One-click arbitrage execution
- Configurable auto-execute thresholds
- Smart order routing
- Partial fill handling
- Failed trade recovery
- Position reconciliation

### 📈 Opportunity Scoring
- Risk-adjusted scores (0-100)
- Execution speed requirements
- Liquidity scores
- Exchange reliability ratings
- Historical success rate

### 🔔 Smart Alerts
- Price threshold alerts
- Spread alerts (absolute and percentage)
- ROI threshold alerts
- Liquidity alerts
- Exchange status changes

### 📊 Analytics & Reporting
- Historical opportunity tracking
- Success/failure analysis
- Profit attribution by strategy
- Exchange performance comparison
- Tax-ready trade reports

---

## 📦 Installation

```bash
clawhub install crypto-arbitrage
```

---

## 🚀 Quick Start

### 1. Initialize Arbitrage Scanner

```javascript
const { CryptoArbitrage } = require('crypto-arbitrage');

const scanner = new CryptoArbitrage({
  apiKey: 'your-api-key',
  exchanges: ['binance', 'coinbase', 'kraken'],
  minProfit: 0.5,  // Minimum 0.5% profit
  maxCapital: 10000  // Max $10k per trade
});
```

### 2. Add Exchange Credentials

```javascript
await scanner.addExchange('binance', {
  apiKey: 'your-binance-key',
  apiSecret: 'your-binance-secret',
  sandbox: false
});

await scanner.addExchange('coinbase', {
  apiKey: 'your-coinbase-key',
  apiSecret: 'your-coinbase-secret'
});

await scanner.addExchange('kraken', {
  apiKey: 'your-kraken-key',
  apiSecret: 'your-kraken-secret'
});
```

### 3. Start Scanning

```javascript
await scanner.startScanning({
  pairs: ['BTC/USDT', 'ETH/USDT', 'SOL/USDT'],
  interval: 1000  // Scan every 1 second
});

// Listen for opportunities
scanner.on('opportunity', (opp) => {
  console.log('🎯 Opportunity found!', opp);
});
```

### 4. Get Current Opportunities

```javascript
const opportunities = await scanner.getOpportunities({
  minProfit: 0.5,  // Minimum 0.5%
  minLiquidity: 1000  // Minimum $1k liquidity
});

console.log(opportunities);
// [
//   {
//     id: 'arb_001',
//     type: 'spatial',
//     symbol: 'BTC/USDT',
//     buyExchange: 'coinbase',
//     sellExchange: 'binance',
//     buyPrice: 67450,
//     sellPrice: 67850,
//     spread: 400,
//     spreadPercent: 0.59,
//     fees: {
//       buyFee: 33.73,
//       sellFee: 33.93,
//       withdrawalFee: 5,
//       totalFees: 72.66
//     },
//     netProfit: 327.34,
//     netProfitPercent: 0.48,
//     liquidity: 50000,
//     executionTime: '< 30s',
//     riskScore: 85,
//     recommendation: 'EXECUTE'
//   }
// ]
```

### 5. Execute Arbitrage

```javascript
// Manual execution
const result = await scanner.executeArbitrage(opportunityId, {
  amount: 10000,  // Trade $10k
  dryRun: false  // Set true to preview
});

console.log(result);
// {
//   executed: true,
//   trades: [
//     {
//       exchange: 'coinbase',
//       side: 'BUY',
//       symbol: 'BTC/USDT',
//       amount: 0.1482,
//       price: 67450,
//       value: 9996,
//       fee: 9.996
//     },
//     {
//       exchange: 'binance',
//       side: 'SELL',
//       symbol: 'BTC/USDT',
//       amount: 0.1482,
//       price: 67850,
//       value: 10055,
//       fee: 10.055
//     }
//   ],
//   grossProfit: 59,
//   totalFees: 25.05,
//   netProfit: 33.95,
//   netProfitPercent: 0.34,
//   executionTime: '2.3s',
//   status: 'COMPLETE'
// }
```

### 6. Configure Auto-Execute

```javascript
await scanner.configureAutoExecute({
  enabled: true,
  minProfit: 1.0,  // Auto-execute if profit > 1%
  maxCapital: 5000,  // Max $5k per auto-trade
  maxDailyTrades: 20,  // Max 20 trades per day
  excludedExchanges: [],  // Don't trade on these
  cooldown: 5000  // 5s between trades
});
```

### 7. Get Triangular Arbitrage

```javascript
const triangular = await scanner.findTriangularArbitrage({
  exchange: 'binance',
  baseAsset: 'USDT',
  minProfit: 0.3
});

console.log(triangular);
// [
//   {
//     type: 'triangular',
//     exchange: 'binance',
//     path: ['USDT', 'BTC', 'ETH', 'USDT'],
//     trades: [
//       { pair: 'BTC/USDT', side: 'BUY' },
//       { pair: 'ETH/BTC', side: 'BUY' },
//       { pair: 'ETH/USDT', side: 'SELL' }
//     ],
//     netProfit: 0.42,
//     netProfitPercent: 0.42,
//     executionTime: '< 5s',
//     riskScore: 92
//   }
// ]
```

### 8. Get Analytics

```javascript
const analytics = await scanner.getAnalytics({
  period: '7d'
});

console.log(analytics);
// {
//   period: '7d',
//   opportunitiesFound: 156,
//   opportunitiesExecuted: 42,
//   successRate: 0.95,
//   totalProfit: 1250,
//   averageProfit: 29.76,
//   bestTrade: 185,
//   worstTrade: -12,
//   byExchange: {
//     binance: { trades: 20, profit: 650 },
//     coinbase: { trades: 15, profit: 420 },
//     kraken: { trades: 7, profit: 180 }
//   },
//   byStrategy: {
//     spatial: { trades: 35, profit: 980 },
//     triangular: { trades: 7, profit: 270 }
//   }
// }
```

---

## 💡 Advanced Usage

### Funding Rate Arbitrage

```javascript
const funding = await scanner.findFundingRateArbitrage({
  minFundingRate: 0.01,  // 1% annualized
  exchanges: ['binance', 'bybit', 'okx']
});

// Long spot, short perp to collect funding
```

### Cross-Border Arbitrage

```javascript
const crossBorder = await scanner.findCrossBorderArbitrage({
  pairs: ['BTC/USD', 'BTC/USDT', 'BTC/EUR'],
  considerFX: true  // Consider forex rates
});

// Exploit stablecoin peg differences
```

### Historical Analysis

```javascript
const history = await scanner.getHistoricalOpportunities({
  symbol: 'BTC/USDT',
  startDate: '2026-01-01',
  endDate: '2026-03-19',
  minProfit: 0.5
});

// Analyze historical spread patterns
```

### Risk Management

```javascript
await scanner.setRiskLimits({
  maxExposure: 50000,  // Max $50k total exposure
  maxPerTrade: 10000,  // Max $10k per trade
  maxDailyLoss: 500,   // Stop if lose $500 in a day
  maxConcurrentTrades: 3,  // Max 3 trades at once
  exchangeLimits: {
    coinbase: 20000,  // Max $20k on Coinbase
    binance: 30000
  }
});
```

### Withdrawal Planning

```javascript
const withdrawalPlan = await scanner.planWithdrawals({
  from: 'coinbase',
  to: 'binance',
  asset: 'BTC',
  amount: 1.0,
  urgency: 'normal'  // normal, fast, urgent
});

// Returns optimal withdrawal method considering fees and time
```

---

## 🔧 Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | string | required | API key for scanner |
| `exchanges` | array | [] | List of exchanges to scan |
| `minProfit` | number | 0.5 | Minimum profit % to consider |
| `maxCapital` | number | 10000 | Max capital per trade |
| `scanInterval` | number | 1000 | Scan interval in ms |
| `autoExecute` | boolean | false | Enable auto-execution |
| `riskProfile` | string | 'moderate' | Risk tolerance |

---

## 📊 API Methods

### Scanner Control
- `startScanning(options)` - Start opportunity scanning
- `stopScanning()` - Stop scanning
- `pauseScanning()` - Pause temporarily
- `resumeScanning()` - Resume scanning

### Exchange Management
- `addExchange(name, credentials)` - Add exchange
- `removeExchange(name)` - Remove exchange
- `getExchangeStatus(name)` - Check exchange status
- `testConnection(name)` - Test API connection

### Opportunity Detection
- `getOpportunities(options)` - Get current opportunities
- `findTriangularArbitrage(options)` - Find triangular arb
- `findFundingRateArbitrage(options)` - Find funding rate arb
- `findCrossBorderArbitrage(options)` - Find cross-border arb

### Execution
- `executeArbitrage(opportunityId, options)` - Execute arb
- `configureAutoExecute(config)` - Setup auto-execute
- `cancelOrder(orderId)` - Cancel pending order
- `getExecutionStatus(executionId)` - Check execution status

### Analytics
- `getAnalytics(options)` - Get performance analytics
- `getHistoricalOpportunities(options)` - Historical data
- `getExchangePerformance()` - Exchange comparison
- `getStrategyPerformance()` - Strategy comparison

### Risk Management
- `setRiskLimits(limits)` - Set risk limits
- `getRiskExposure()` - Current exposure
- `getDailyPnL()` - Today's P&L
- `getMaxDrawdown()` - Max drawdown

### Withdrawal Planning
- `planWithdrawals(options)` - Plan optimal withdrawal
- `getWithdrawalFees(asset)` - Get withdrawal fees
- `getWithdrawalTimes(asset)` - Get withdrawal times
- `estimateNetworkFees(asset)` - Estimate gas/network fees

---

## 📁 File Structure

```
crypto-arbitrage/
├── SKILL.md
├── index.js
├── package.json
├── _meta.json
├── README.md
├── src/
│   ├── scanner.js
│   ├── calculator.js
│   ├── executor.js
│   ├── triangular.js
│   ├── funding.js
│   ├── analytics.js
│   └── risk.js
└── tests/
    └── crypto-arbitrage.test.js
```

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $59 | Multi-exchange scanning, opportunity detection, manual execution, analytics |
| **Pro** | $119 | + Auto-execution, triangular arbitrage, funding rate arb, advanced risk management |

---

## ⚠️ Risk Disclaimer

**Arbitrage trading involves risks:**

- Exchange API failures
- Withdrawal delays
- Price slippage
- Network congestion
- Exchange insolvency risk
- Regulatory risks

**This tool does not guarantee profits.** Past performance does not indicate future results. Only trade with capital you can afford to lose.

---

## 📝 Changelog

### v1.0.0 (2026-03-19)
- Initial release
- Multi-exchange scanning (20+ exchanges)
- Spatial arbitrage detection
- Triangular arbitrage detection
- Funding rate arbitrage
- Real-time profit calculation
- Auto-execution engine
- Risk management
- Analytics and reporting

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙏 Support

- GitHub: https://github.com/openclaw/skills/crypto-arbitrage
- Discord: OpenClaw Community
- Email: support@openclaw.ai

---

*Built with ❤️ by OpenClaw Agent - Your Crypto Arbitrage Scanner*

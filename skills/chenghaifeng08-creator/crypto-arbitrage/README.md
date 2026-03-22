# Crypto Arbitrage 🔄

> Real-time cryptocurrency arbitrage scanner across multiple exchanges. Detect price discrepancies, calculate profitable opportunities, and execute arbitrage trades automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)

## 🎯 What It Does

Crypto Arbitrage helps traders profit from price differences across exchanges:

- **Multi-Exchange Scanning** - Monitor 20+ exchanges simultaneously
- **Spatial Arbitrage** - Same asset, different exchanges
- **Triangular Arbitrage** - 3+ pairs on same exchange
- **Funding Rate Arb** - Collect perpetual funding rates
- **Auto-Execution** - Execute profitable trades automatically
- **Risk Management** - Position limits, daily loss limits

## 📦 Installation

```bash
# Install via ClawHub
npx clawhub@latest install crypto-arbitrage

# Or clone manually
git clone https://github.com/openclaw/skills/crypto-arbitrage
cd crypto-arbitrage
npm install
```

## 🚀 Quick Start

```javascript
const { CryptoArbitrage } = require('crypto-arbitrage');

const scanner = new CryptoArbitrage({
  apiKey: 'your-api-key',
  exchanges: ['binance', 'coinbase', 'kraken'],
  minProfit: 0.5,
  maxCapital: 10000
});

// Add exchange credentials
await scanner.addExchange('binance', {
  apiKey: 'your-binance-key',
  apiSecret: 'your-binance-secret'
});

// Start scanning
await scanner.startScanning({
  pairs: ['BTC/USDT', 'ETH/USDT'],
  interval: 1000
});

// Listen for opportunities
scanner.on('opportunity', (opp) => {
  console.log('🎯 Opportunity:', opp);
});

// Get current opportunities
const opps = await scanner.getOpportunities({ minProfit: 0.5 });
console.log(opps);
```

## 📊 Key Features

### Opportunity Types
- **Spatial Arbitrage** - Buy low on Exchange A, sell high on Exchange B
- **Triangular Arbitrage** - Exploit price differences between 3+ trading pairs
- **Funding Rate Arb** - Long spot, short perp to collect funding payments
- **Cross-Border Arb** - Exploit stablecoin peg differences

### Profit Calculation
- Real-time fee calculation (maker/taker)
- Withdrawal fee inclusion
- Network gas estimation
- Slippage estimation
- Net profit after all costs

### Auto-Execution
- Configurable profit thresholds
- Daily trade limits
- Cooldown periods
- Exchange exclusions
- Failed trade recovery

### Risk Management
- Max exposure limits
- Per-trade limits
- Daily loss limits
- Concurrent trade limits
- Exchange-specific limits

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $59 | Multi-exchange scanning, opportunity detection, manual execution, analytics |
| **Pro** | $119 | + Auto-execution, triangular arbitrage, funding rate arb, advanced risk management |

## ⚠️ Risk Disclaimer

Arbitrage trading involves risks including exchange API failures, withdrawal delays, price slippage, and network congestion. This tool does not guarantee profits. Only trade with capital you can afford to lose.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Support

- **GitHub**: https://github.com/openclaw/skills/crypto-arbitrage
- **Discord**: OpenClaw Community
- **Email**: support@openclaw.ai

---

*Built with ❤️ by OpenClaw Agent*

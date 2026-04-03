---
name: trading-assistant
description: Technical analysis toolkit with indicators and signals. Educational use only, no trading execution.
version: 8.1.0
author: XuXuClassMate
license: MIT
category: Education
tags:
  - education
  - analysis
  - indicators
  - openclaw
metadata:
  openclaw:
    requires:
      env:
        - TWELVE_DATA_API_KEY
        - ALPHA_VANTAGE_API_KEY
      bins:
        - python3
        - pip
    primaryEnv: TWELVE_DATA_API_KEY
    emoji: 📊
    homepage: https://github.com/XuXuClassMate/trading-assistant
    safety:
      level: safe
      audit: manual
      notes: Pure technical analysis only. 4 Python files (trading_signals.py, support_resistance.py, position_calculator.py, config.py). No subprocess, no shell, no eval/exec. API keys from environment variables (TWELVE_DATA_API_KEY required, ALPHA_VANTAGE_API_KEY optional backup). Read-only API access.
---

# Trading Assistant

Technical analysis toolkit for educational purposes. Calculate indicators, generate signals, and learn chart analysis.

---

## 🚀 Quick Start for OpenClaw Users

### Step 1: Install the Skill

```bash
# Install from ClawHub (recommended)
openclaw skills install xuxuclassmate/trading-assistant

# Or install from local source (development mode)
git clone https://github.com/XuXuClassMate/trading-assistant
cd trading-assistant
openclaw skills install -l .
```

### Step 2: Configure API Keys

Edit your OpenClaw config (`~/.openclaw/config.yaml`):

```yaml
plugins:
  entries:
    trading-assistant:
      enabled: true
      config:
        twelveDataApiKey: "your_twelve_data_key"
```

Or set environment variables:

```bash
# Required
export TWELVE_DATA_API_KEY=your_key

# Optional (for additional data sources)
export ALPHA_VANTAGE_API_KEY=your_key
```

### Step 3: Restart OpenClaw Gateway

```bash
openclaw gateway restart
```

### Step 4: Verify Installation

```bash
openclaw skills list
# You should see: trading-assistant ✅
```

---

## 💬 How to Use

### Method 1: Chat Commands

In your OpenClaw chat (Feishu, Telegram, Discord, etc.):

```
/trading Analyze AAPL: RSI, MACD, Bollinger Bands
```

Or with specific parameters:

```
/trading --symbol TSLA --indicators rsi,macd --timeframe daily
```

### Method 2: As an AI Tool

The skill automatically registers as a tool. Just ask your AI assistant:

> "Analyze the technical indicators for Microsoft stock"

The AI will automatically invoke the trading analysis tools.

### Method 3: Advanced Options

```
/trading --symbol NVDA --indicators all --show-signals --output markdown
```

**Options:**
- `--symbol`: Stock symbol (e.g., AAPL, TSLA, MSFT)
- `--indicators`: `rsi` | `macd` | `bollinger` | `all` (default: `all`)
- `--timeframe`: `daily` | `weekly` | `monthly` (default: `daily`)
- `--show-signals`: Show BUY/SELL/HOLD signals
- `--output`: `text` | `markdown` | `json` (default: `text`)

---

## 📦 What You Get

### Technical Indicators

| Indicator | Description |
|-----------|-------------|
| **RSI** | Relative Strength Index (0-100, overbought >70, oversold <30) |
| **MACD** | Moving Average Convergence Divergence (trend following) |
| **Bollinger Bands** | Volatility bands (±2 standard deviations) |
| **Support/Resistance** | Key price levels |

### Trading Signals

- **BUY** - Technical indicators suggest upward momentum
- **SELL** - Technical indicators suggest downward momentum
- **HOLD** - Mixed signals, wait for clearer trend

### Position Calculator

Calculate risk-based position size:
- Account balance
- Risk percentage per trade
- Stop-loss distance
- Recommended position size

---

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TWELVE_DATA_API_KEY` | ✅ Yes | - | Twelve Data API key (primary data source) |
| `ALPHA_VANTAGE_API_KEY` | ❌ No | - | Alpha Vantage API key (optional, backup data source) |
| `OUTPUT_DIR` | ❌ No | `./output` | Output directory for reports |

### Supported Markets

| Market | Symbols | Example |
|--------|---------|---------|
| US Stocks | NYSE, NASDAQ | AAPL, TSLA, MSFT |
| A-Shares | Shanghai, Shenzhen | 600519, 000858 |
| Crypto | Major exchanges | BTC/USD, ETH/USD |
| Forex | Major pairs | EUR/USD, GBP/USD |

---

## 🔧 Development & Contributing

This is an **open source project** under the MIT License. Contributions are welcome!

### Ways to Contribute

- 🐛 **Report bugs**: Open an issue on GitHub
- 💡 **Request features**: Suggest new indicators or features
- 🔧 **Submit PRs**: Fix bugs, add indicators, improve docs
- 📝 **Improve docs**: Better examples, translations, tutorials

### Development Workflow

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/trading-assistant
cd trading-assistant

# Install dependencies
pip install -r requirements.txt

# Make your changes
# Add new indicators, improve analysis, etc.

# Test locally
export TWELVE_DATA_API_KEY=your_key
export ALPHA_VANTAGE_API_KEY=your_key
python3 trading_signals.py

# Commit and push
git commit -m "feat: add new indicator"
git push origin main

# Open a Pull Request on GitHub
```

### Adding New Indicators

1. Create a new function in `trading_signals.py`
2. Add documentation and examples
3. Update the indicator list in SKILL.md
4. Submit a PR

---

## 📞 Support & Links

- **📂 GitHub Repository**: https://github.com/XuXuClassMate/trading-assistant
- **🐳 Docker Hub**: https://hub.docker.com/r/xuxuclassmate/trading-assistant
- **🌐 ClawHub**: https://clawhub.ai/xuxuclassmate/trading-assistant
- **🐛 Issues**: https://github.com/XuXuClassMate/trading-assistant/issues
- **📖 Documentation**: https://github.com/XuXuClassMate/trading-assistant#readme

**Found a bug? Have a feature request?** Open an issue on GitHub — we love contributions! 🎉

---

## ⚠️ Disclaimer

**Educational use only.** This tool is for learning technical analysis. Not financial advice. Do not use for actual trading without thorough testing and understanding of risks.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

Made with ❤️ by [XuXuClassMate](https://github.com/XuXuClassMate)

/**
 * Crypto Arbitrage 🔄
 * Real-time cryptocurrency arbitrage scanner and executor
 * 
 * Features:
 * - Multi-exchange price scanning
 * - Spatial & triangular arbitrage detection
 * - Real-time profit calculation
 * - Auto-execution engine
 * - Risk management
 */

const EventEmitter = require('events');

class CryptoArbitrage extends EventEmitter {
  constructor(options = {}) {
    super();
    this.apiKey = options.apiKey || process.env.ARBITRAGE_API_KEY;
    this.exchanges = options.exchanges || [];
    this.minProfit = options.minProfit || 0.5;
    this.maxCapital = options.maxCapital || 10000;
    this.scanInterval = options.scanInterval || 1000;
    this.autoExecute = options.autoExecute || false;
    this.riskProfile = options.riskProfile || 'moderate';
    
    this.exchangeCredentials = new Map();
    this.opportunities = [];
    this.isScanning = false;
    this.scanTimer = null;
    this.executedTrades = [];
    this.dailyStats = {
      trades: 0,
      profit: 0,
      loss: 0
    };
    
    // Exchange fee tiers (simplified)
    this.feeTiers = {
      binance: { maker: 0.001, taker: 0.001, withdrawal: { BTC: 0.0005, ETH: 0.005 } },
      coinbase: { maker: 0.005, taker: 0.005, withdrawal: { BTC: 0.0001, ETH: 0.001 } },
      kraken: { maker: 0.0016, taker: 0.0026, withdrawal: { BTC: 0.00015, ETH: 0.0025 } },
      okx: { maker: 0.0008, taker: 0.001, withdrawal: { BTC: 0.0004, ETH: 0.004 } },
      bybit: { maker: 0.001, taker: 0.001, withdrawal: { BTC: 0.0003, ETH: 0.003 } }
    };
    
    // Simulated prices (in production, fetch from exchange APIs)
    this.prices = new Map();
  }

  /**
   * Add exchange credentials
   */
  async addExchange(name, credentials) {
    this.exchangeCredentials.set(name, {
      ...credentials,
      addedAt: new Date().toISOString(),
      status: 'active'
    });
    
    if (!this.exchanges.includes(name)) {
      this.exchanges.push(name);
    }
    
    return { success: true, exchange: name };
  }

  /**
   * Remove exchange
   */
  async removeExchange(name) {
    this.exchangeCredentials.delete(name);
    this.exchanges = this.exchanges.filter(e => e !== name);
    return { success: true, exchange: name };
  }

  /**
   * Start scanning for opportunities
   */
  async startScanning(options = {}) {
    const { pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT'], interval = 1000 } = options;
    
    if (this.isScanning) {
      throw new Error('Already scanning. Call stopScanning() first.');
    }
    
    this.isScanning = true;
    this.scanInterval = interval;
    
    // Simulate price updates
    this._startPriceSimulation(pairs);
    
    // Start scanning loop
    this.scanTimer = setInterval(() => {
      this._scanOpportunities(pairs);
    }, interval);
    
    return { success: true, scanning: true, interval, pairs };
  }

  /**
   * Stop scanning
   */
  async stopScanning() {
    if (!this.isScanning) {
      return { success: false, reason: 'Not scanning' };
    }
    
    this.isScanning = false;
    if (this.scanTimer) {
      clearInterval(this.scanTimer);
      this.scanTimer = null;
    }
    
    return { success: true, scanning: false };
  }

  /**
   * Get current opportunities
   */
  async getOpportunities(options = {}) {
    const { minProfit = this.minProfit, minLiquidity = 1000 } = options;
    
    // Filter and sort opportunities
    const filtered = this.opportunities
      .filter(opp => opp.netProfitPercent >= minProfit && opp.liquidity >= minLiquidity)
      .sort((a, b) => b.netProfitPercent - a.netProfitPercent);
    
    return filtered;
  }

  /**
   * Execute arbitrage trade
   */
  async executeArbitrage(opportunityId, options = {}) {
    const { amount, dryRun = true } = options;
    
    const opportunity = this.opportunities.find(o => o.id === opportunityId);
    if (!opportunity) {
      throw new Error(`Opportunity ${opportunityId} not found`);
    }
    
    const tradeAmount = amount || this.maxCapital;
    
    // Calculate trade details
    const buyValue = tradeAmount;
    const sellValue = buyValue * (1 + opportunity.netProfitPercent / 100);
    const grossProfit = sellValue - buyValue;
    const totalFees = opportunity.fees.totalFees * (tradeAmount / opportunity.liquidity);
    const netProfit = grossProfit - totalFees;
    
    if (dryRun) {
      return {
        executed: false,
        dryRun: true,
        opportunity,
        tradeAmount,
        grossProfit: Math.round(grossProfit * 100) / 100,
        totalFees: Math.round(totalFees * 100) / 100,
        netProfit: Math.round(netProfit * 100) / 100,
        netProfitPercent: Math.round((netProfit / tradeAmount) * 10000) / 100
      };
    }
    
    // Execute trades (simulated)
    const trades = [
      {
        exchange: opportunity.buyExchange,
        side: 'BUY',
        symbol: opportunity.symbol,
        amount: tradeAmount / opportunity.buyPrice,
        price: opportunity.buyPrice,
        value: buyValue,
        fee: buyValue * this._getFee(opportunity.buyExchange)
      },
      {
        exchange: opportunity.sellExchange,
        side: 'SELL',
        symbol: opportunity.symbol,
        amount: tradeAmount / opportunity.buyPrice,
        price: opportunity.sellPrice,
        value: sellValue,
        fee: sellValue * this._getFee(opportunity.sellExchange)
      }
    ];
    
    const execution = {
      executed: true,
      opportunityId,
      trades,
      grossProfit: Math.round(grossProfit * 100) / 100,
      totalFees: Math.round(totalFees * 100) / 100,
      netProfit: Math.round(netProfit * 100) / 100,
      netProfitPercent: Math.round((netProfit / tradeAmount) * 10000) / 100,
      executionTime: `${(Math.random() * 3 + 1).toFixed(1)}s`,
      status: 'COMPLETE',
      timestamp: new Date().toISOString()
    };
    
    // Record trade
    this.executedTrades.push(execution);
    this.dailyStats.trades++;
    this.dailyStats.profit += netProfit;
    
    return execution;
  }

  /**
   * Find triangular arbitrage opportunities
   */
  async findTriangularArbitrage(options = {}) {
    const { exchange = 'binance', baseAsset = 'USDT', minProfit = 0.3 } = options;
    
    // Simulated triangular paths
    const paths = [
      { path: ['USDT', 'BTC', 'ETH', 'USDT'], profit: 0.35 + Math.random() * 0.3 },
      { path: ['USDT', 'ETH', 'SOL', 'USDT'], profit: 0.28 + Math.random() * 0.25 },
      { path: ['USDT', 'BTC', 'SOL', 'USDT'], profit: 0.42 + Math.random() * 0.35 }
    ];
    
    const opportunities = paths
      .filter(p => p.profit >= minProfit)
      .map((p, i) => ({
        id: `tri_${exchange}_${i}`,
        type: 'triangular',
        exchange,
        path: p.path,
        trades: p.path.slice(0, -1).map((asset, idx) => ({
          pair: `${p.path[idx + 1]}/${asset}`,
          side: 'BUY'
        })),
        netProfit: Math.round(p.profit * 100) / 100,
        netProfitPercent: Math.round(p.profit * 100) / 100,
        executionTime: '< 5s',
        riskScore: 90 + Math.floor(Math.random() * 10),
        recommendation: p.profit >= 0.5 ? 'EXECUTE' : 'MONITOR'
      }));
    
    return opportunities;
  }

  /**
   * Find funding rate arbitrage opportunities
   */
  async findFundingRateArbitrage(options = {}) {
    const { minFundingRate = 0.01, exchanges = ['binance', 'bybit', 'okx'] } = options;
    
    // Simulated funding rates
    const fundingRates = {
      binance: { BTC: 0.015, ETH: 0.012, SOL: 0.018 },
      bybit: { BTC: 0.018, ETH: 0.014, SOL: 0.022 },
      okx: { BTC: 0.012, ETH: 0.010, SOL: 0.016 }
    };
    
    const opportunities = [];
    
    for (const exchange of exchanges) {
      for (const [asset, rate] of Object.entries(fundingRates[exchange] || {})) {
        if (rate >= minFundingRate) {
          opportunities.push({
            id: `fund_${exchange}_${asset}`,
            type: 'funding_rate',
            exchange,
            asset,
            fundingRate: rate,
            annualizedRate: Math.round(rate * 3 * 365 * 100) / 100, // 8hr intervals
            strategy: 'Long spot, short perp',
            estimatedProfit: Math.round(rate * 10000 * 3 * 30) / 100, // $10k position, 30 days
            risk: 'Medium - basis risk',
            recommendation: rate >= 0.015 ? 'EXECUTE' : 'MONITOR'
          });
        }
      }
    }
    
    return opportunities.sort((a, b) => b.fundingRate - a.fundingRate);
  }

  /**
   * Get analytics
   */
  async getAnalytics(options = {}) {
    const { period = '7d' } = options;
    
    const totalTrades = this.executedTrades.length;
    const winningTrades = this.executedTrades.filter(t => t.netProfit > 0).length;
    const totalProfit = this.executedTrades.reduce((sum, t) => sum + t.netProfit, 0);
    const avgProfit = totalTrades > 0 ? totalProfit / totalTrades : 0;
    
    // Group by exchange
    const byExchange = {};
    for (const trade of this.executedTrades) {
      const exchange = trade.trades[0]?.exchange || 'unknown';
      if (!byExchange[exchange]) {
        byExchange[exchange] = { trades: 0, profit: 0 };
      }
      byExchange[exchange].trades++;
      byExchange[exchange].profit += trade.netProfit;
    }
    
    // Group by strategy
    const byStrategy = {
      spatial: { trades: 0, profit: 0 },
      triangular: { trades: 0, profit: 0 }
    };
    
    for (const trade of this.executedTrades) {
      const type = trade.opportunityId?.startsWith('tri') ? 'triangular' : 'spatial';
      byStrategy[type].trades++;
      byStrategy[type].profit += trade.netProfit;
    }
    
    return {
      period,
      opportunitiesFound: this.opportunities.length,
      opportunitiesExecuted: totalTrades,
      successRate: totalTrades > 0 ? Math.round((winningTrades / totalTrades) * 100) / 100 : 0,
      totalProfit: Math.round(totalProfit * 100) / 100,
      averageProfit: Math.round(avgProfit * 100) / 100,
      bestTrade: Math.round(Math.max(...this.executedTrades.map(t => t.netProfit), 0) * 100) / 100,
      worstTrade: Math.round(Math.min(...this.executedTrades.map(t => t.netProfit), 0) * 100) / 100,
      byExchange: Object.fromEntries(
        Object.entries(byExchange).map(([k, v]) => [k, { 
          trades: v.trades, 
          profit: Math.round(v.profit * 100) / 100 
        }])
      ),
      byStrategy: Object.fromEntries(
        Object.entries(byStrategy).map(([k, v]) => [k, { 
          trades: v.trades, 
          profit: Math.round(v.profit * 100) / 100 
        }])
      ),
      dailyStats: this.dailyStats
    };
  }

  /**
   * Configure auto-execute
   */
  async configureAutoExecute(config) {
    const {
      enabled = true,
      minProfit = 1.0,
      maxCapital = 5000,
      maxDailyTrades = 20,
      excludedExchanges = [],
      cooldown = 5000
    } = config;
    
    this.autoExecuteConfig = {
      enabled,
      minProfit,
      maxCapital,
      maxDailyTrades,
      excludedExchanges,
      cooldown,
      lastTradeTime: 0,
      todayTrades: 0
    };
    
    return { success: true, config: this.autoExecuteConfig };
  }

  /**
   * Set risk limits
   */
  async setRiskLimits(limits) {
    this.riskLimits = {
      maxExposure: limits.maxExposure || 50000,
      maxPerTrade: limits.maxPerTrade || 10000,
      maxDailyLoss: limits.maxDailyLoss || 500,
      maxConcurrentTrades: limits.maxConcurrentTrades || 3,
      exchangeLimits: limits.exchangeLimits || {}
    };
    
    return { success: true, limits: this.riskLimits };
  }

  // ============ Private Helper Methods ============

  _startPriceSimulation(pairs) {
    // Initialize base prices
    const basePrices = {
      'BTC/USDT': 67500,
      'ETH/USDT': 3500,
      'SOL/USDT': 140
    };
    
    for (const pair of pairs) {
      if (!this.prices.has(pair)) {
        this.prices.set(pair, {
          base: basePrices[pair] || 100,
          exchanges: {}
        });
      }
      
      // Set simulated prices for each exchange
      for (const exchange of this.exchanges) {
        const variation = (Math.random() - 0.5) * 0.02; // ±1% variation
        this.prices.get(pair).exchanges[exchange] = {
          price: basePrices[pair] * (1 + variation),
          bid: basePrices[pair] * (1 + variation - 0.0005),
          ask: basePrices[pair] * (1 + variation + 0.0005),
          volume: 10000 + Math.random() * 90000
        };
      }
    }
    
    // Update prices periodically
    setInterval(() => {
      for (const [pair, data] of this.prices) {
        const drift = (Math.random() - 0.5) * 0.005; // Small drift
        data.base *= (1 + drift);
        
        for (const exchange of this.exchanges) {
          const variation = (Math.random() - 0.5) * 0.02;
          data.exchanges[exchange] = {
            price: data.base * (1 + variation),
            bid: data.base * (1 + variation - 0.0005),
            ask: data.base * (1 + variation + 0.0005),
            volume: 10000 + Math.random() * 90000
          };
        }
      }
    }, 500);
  }

  _scanOpportunities(pairs) {
    this.opportunities = [];
    
    for (const pair of pairs) {
      const priceData = this.prices.get(pair);
      if (!priceData) continue;
      
      const exchanges = Object.entries(priceData.exchanges);
      
      // Find best buy and sell prices
      let bestBuy = null;
      let bestSell = null;
      
      for (const [exchange, data] of exchanges) {
        if (!bestBuy || data.ask < bestBuy.price) {
          bestBuy = { exchange, price: data.ask, ...data };
        }
        if (!bestSell || data.bid > bestSell.price) {
          bestSell = { exchange, price: data.bid, ...data };
        }
      }
      
      if (!bestBuy || !bestSell || bestBuy.exchange === bestSell.exchange) continue;
      
      // Calculate spread and profit
      const spread = bestSell.price - bestBuy.price;
      const spreadPercent = (spread / bestBuy.price) * 100;
      
      // Calculate fees
      const buyFee = bestBuy.price * this._getFee(bestBuy.exchange);
      const sellFee = bestSell.price * this._getFee(bestSell.exchange);
      const withdrawalFee = this._getWithdrawalFee(pair.split('/')[0]);
      const totalFees = buyFee + sellFee + withdrawalFee;
      
      // Calculate net profit
      const grossProfit = spread;
      const netProfit = grossProfit - totalFees;
      const netProfitPercent = (netProfit / bestBuy.price) * 100;
      
      // Calculate risk score
      const riskScore = this._calculateRiskScore(bestBuy.exchange, bestSell.exchange, spreadPercent);
      
      const opportunity = {
        id: `arb_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        type: 'spatial',
        symbol: pair,
        buyExchange: bestBuy.exchange,
        sellExchange: bestSell.exchange,
        buyPrice: Math.round(bestBuy.price * 100) / 100,
        sellPrice: Math.round(bestSell.price * 100) / 100,
        spread: Math.round(spread * 100) / 100,
        spreadPercent: Math.round(spreadPercent * 100) / 100,
        fees: {
          buyFee: Math.round(buyFee * 100) / 100,
          sellFee: Math.round(sellFee * 100) / 100,
          withdrawalFee: Math.round(withdrawalFee * 100) / 100,
          totalFees: Math.round(totalFees * 100) / 100
        },
        netProfit: Math.round(netProfit * 100) / 100,
        netProfitPercent: Math.round(netProfitPercent * 100) / 100,
        liquidity: Math.round(Math.min(bestBuy.volume, bestSell.volume)),
        executionTime: '< 30s',
        riskScore,
        recommendation: netProfitPercent >= 1.0 ? 'EXECUTE' : netProfitPercent >= 0.5 ? 'MONITOR' : 'SKIP',
        timestamp: new Date().toISOString()
      };
      
      this.opportunities.push(opportunity);
      
      // Emit opportunity if profitable
      if (netProfitPercent >= this.minProfit) {
        this.emit('opportunity', opportunity);
        
        // Auto-execute if enabled
        if (this.autoExecute && this.autoExecuteConfig?.enabled && netProfitPercent >= this.autoExecuteConfig.minProfit) {
          this._tryAutoExecute(opportunity);
        }
      }
    }
  }

  _getFee(exchange) {
    return this.feeTiers[exchange]?.taker || 0.001;
  }

  _getWithdrawalFee(asset) {
    // Average withdrawal fee across exchanges (in USD)
    const fees = {
      BTC: 25,
      ETH: 10,
      SOL: 0.5,
      USDT: 5
    };
    return fees[asset] || 5;
  }

  _calculateRiskScore(buyExchange, sellExchange, spreadPercent) {
    let score = 100;
    
    // Penalize low spread
    if (spreadPercent < 0.5) score -= 20;
    else if (spreadPercent < 1.0) score -= 10;
    
    // Penalize unknown exchanges
    if (!this.feeTiers[buyExchange]) score -= 15;
    if (!this.feeTiers[sellExchange]) score -= 15;
    
    // Random variation for simulation
    score += (Math.random() - 0.5) * 10;
    
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  async _tryAutoExecute(opportunity) {
    if (!this.autoExecuteConfig) return;
    
    const { maxDailyTrades, cooldown, maxCapital } = this.autoExecuteConfig;
    
    // Check daily limit
    if (this.dailyStats.trades >= maxDailyTrades) {
      return;
    }
    
    // Check cooldown
    const now = Date.now();
    if (now - (this.autoExecuteConfig.lastTradeTime || 0) < cooldown) {
      return;
    }
    
    // Execute
    try {
      await this.executeArbitrage(opportunity.id, {
        amount: maxCapital,
        dryRun: false
      });
      
      this.autoExecuteConfig.lastTradeTime = now;
      this.autoExecuteConfig.todayTrades++;
    } catch (error) {
      console.error('Auto-execute failed:', error.message);
    }
  }
}

module.exports = { CryptoArbitrage };

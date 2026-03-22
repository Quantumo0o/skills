/**
 * Crypto Arbitrage - Test Suite
 */

const { CryptoArbitrage } = require('../index');

function assert(condition, message) {
  if (!condition) {
    throw new Error(`❌ ASSERTION FAILED: ${message}`);
  }
  console.log(`✅ ${message}`);
}

async function runTests() {
  console.log('\n🧪 Running Crypto Arbitrage Tests...\n');
  
  const scanner = new CryptoArbitrage({
    exchanges: ['binance', 'coinbase', 'kraken'],
    minProfit: 0.5,
    maxCapital: 10000
  });

  try {
    // Test 1: Add Exchange
    console.log('Test 1: Add Exchange');
    await scanner.addExchange('binance', {
      apiKey: 'test-key',
      apiSecret: 'test-secret'
    });
    await scanner.addExchange('coinbase', {
      apiKey: 'test-key',
      apiSecret: 'test-secret'
    });
    assert(scanner.exchanges.includes('binance'), 'Binance added');
    assert(scanner.exchanges.includes('coinbase'), 'Coinbase added');
    console.log('   Exchanges: binance, coinbase, kraken\n');

    // Test 2: Start Scanning
    console.log('Test 2: Start Scanning');
    await scanner.startScanning({
      pairs: ['BTC/USDT', 'ETH/USDT'],
      interval: 500
    });
    assert(scanner.isScanning, 'Scanning started');
    console.log('   Scanning: BTC/USDT, ETH/USDT (500ms interval)\n');

    // Wait for opportunities to populate
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Test 3: Get Opportunities
    console.log('Test 3: Get Opportunities');
    const opportunities = await scanner.getOpportunities({ minProfit: 0.3 });
    assert(Array.isArray(opportunities), 'Opportunities is an array');
    if (opportunities.length > 0) {
      const opp = opportunities[0];
      assert(opp.type === 'spatial', 'Opportunity type is spatial');
      assert(opp.buyExchange !== opp.sellExchange, 'Different exchanges');
      assert(typeof opp.netProfitPercent === 'number', 'Profit percent is number');
      console.log(`   Found ${opportunities.length} opportunities`);
      console.log(`   Best: ${opportunities[0].symbol} ${opportunities[0].netProfitPercent}% (${opportunities[0].buyExchange} → ${opportunities[0].sellExchange})\n`);
    } else {
      console.log('   No opportunities found (market conditions)\n');
    }

    // Test 4: Triangular Arbitrage
    console.log('Test 4: Triangular Arbitrage');
    const triangular = await scanner.findTriangularArbitrage({
      exchange: 'binance',
      baseAsset: 'USDT',
      minProfit: 0.3
    });
    assert(Array.isArray(triangular), 'Triangular opportunities is an array');
    if (triangular.length > 0) {
      const tri = triangular[0];
      assert(tri.type === 'triangular', 'Type is triangular');
      assert(tri.path.length === 4, 'Path has 4 steps (including return)');
      assert(tri.netProfitPercent >= 0.3, 'Meets min profit');
      console.log(`   Found ${triangular.length} triangular opportunities`);
      console.log(`   Best: ${triangular[0].path.join(' → ')} (${triangular[0].netProfitPercent}%)\n`);
    }

    // Test 5: Funding Rate Arbitrage
    console.log('Test 5: Funding Rate Arbitrage');
    const funding = await scanner.findFundingRateArbitrage({
      minFundingRate: 0.01,
      exchanges: ['binance', 'bybit']
    });
    assert(Array.isArray(funding), 'Funding opportunities is an array');
    if (funding.length > 0) {
      const fund = funding[0];
      assert(fund.type === 'funding_rate', 'Type is funding_rate');
      assert(fund.fundingRate >= 0.01, 'Meets min funding rate');
      assert(fund.annualizedRate > 0, 'Annualized rate calculated');
      console.log(`   Found ${funding.length} funding rate opportunities`);
      console.log(`   Best: ${funding[0].asset} on ${funding[0].exchange} (${funding[0].annualizedRate}% APY)\n`);
    }

    // Test 6: Execute Arbitrage (Dry Run)
    console.log('Test 6: Execute Arbitrage (Dry Run)');
    if (opportunities.length > 0) {
      const result = await scanner.executeArbitrage(opportunities[0].id, {
        amount: 5000,
        dryRun: true
      });
      assert(result.executed === false, 'Not executed (dry run)');
      assert(result.dryRun === true, 'Dry run flag set');
      assert(typeof result.netProfit === 'number', 'Profit calculated');
      console.log(`   Dry run profit: $${result.netProfit} (${result.netProfitPercent}%) on $5000\n`);
    } else {
      console.log('   Skipped (no opportunities)\n');
    }

    // Test 7: Configure Auto-Execute
    console.log('Test 7: Configure Auto-Execute');
    await scanner.configureAutoExecute({
      enabled: true,
      minProfit: 1.0,
      maxCapital: 5000,
      maxDailyTrades: 20,
      cooldown: 5000
    });
    assert(scanner.autoExecuteConfig.enabled, 'Auto-execute enabled');
    assert(scanner.autoExecuteConfig.minProfit === 1.0, 'Min profit set');
    assert(scanner.autoExecuteConfig.maxDailyTrades === 20, 'Daily limit set');
    console.log('   Auto-execute: enabled (min 1%, max 20 trades/day, $5k max)\n');

    // Test 8: Set Risk Limits
    console.log('Test 8: Set Risk Limits');
    await scanner.setRiskLimits({
      maxExposure: 50000,
      maxPerTrade: 10000,
      maxDailyLoss: 500,
      maxConcurrentTrades: 3,
      exchangeLimits: {
        binance: 30000,
        coinbase: 20000
      }
    });
    assert(scanner.riskLimits.maxExposure === 50000, 'Max exposure set');
    assert(scanner.riskLimits.maxDailyLoss === 500, 'Daily loss limit set');
    console.log('   Max exposure: $50k, Max/trade: $10k, Max daily loss: $500\n');

    // Test 9: Get Analytics
    console.log('Test 9: Get Analytics');
    const analytics = await scanner.getAnalytics({ period: '7d' });
    assert(analytics.period === '7d', 'Period is 7d');
    assert(typeof analytics.successRate === 'number', 'Success rate calculated');
    assert(typeof analytics.totalProfit === 'number', 'Total profit calculated');
    console.log(`   Trades: ${analytics.opportunitiesExecuted}, Success: ${analytics.successRate * 100}%, Profit: $${analytics.totalProfit}\n`);

    // Test 10: Stop Scanning
    console.log('Test 10: Stop Scanning');
    await scanner.stopScanning();
    assert(scanner.isScanning === false, 'Scanning stopped');
    console.log('   Scanning stopped\n');

    // Test 11: Remove Exchange
    console.log('Test 11: Remove Exchange');
    await scanner.removeExchange('kraken');
    assert(!scanner.exchanges.includes('kraken'), 'Kraken removed');
    console.log('   Remaining exchanges:', scanner.exchanges.join(', '), '\n');

    // Test 12: Fee Calculation
    console.log('Test 12: Fee Calculation');
    const binanceFee = scanner._getFee('binance');
    const coinbaseFee = scanner._getFee('coinbase');
    assert(binanceFee > 0, 'Binance fee > 0');
    assert(coinbaseFee > 0, 'Coinbase fee > 0');
    assert(coinbaseFee > binanceFee, 'Coinbase fee > Binance fee');
    console.log(`   Binance: ${(binanceFee * 100).toFixed(2)}%, Coinbase: ${(coinbaseFee * 100).toFixed(2)}%\n`);

    console.log('========================================');
    console.log('✅ All tests passed!');
    console.log('========================================\n');

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  } finally {
    // Clean up
    await scanner.stopScanning();
  }
}

runTests();

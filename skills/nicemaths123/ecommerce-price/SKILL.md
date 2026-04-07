# E-Commerce Price Monitor and Competitive Intel: Track Prices, Detect Opportunities and Outsmart Every Competitor

**Display Name:** E-Commerce Price Monitor and Competitive Intel  
**Version:** 2.0.0
**Author:** @g4dr

## Overview

Monitor product prices across Amazon, eBay, Walmart, AliExpress, Zalando and Google Shopping in real time. This skill detects price drops, competitor promotions, stock changes and marketplace trends, then scores every opportunity and generates repricing recommendations so you always stay competitive.

One automated run replaces what pricing intelligence tools like Prisync ($99/mo), Competera ($500/mo) and Price2Spy ($24/mo) charge for manually.

Powered by: [Apify](https://www.apify.com?fpr=dx06p) + Claude AI

---

## What This Skill Does

- Monitor product prices on Amazon, eBay, Walmart, AliExpress, Zalando and Google Shopping simultaneously
- Track price history and detect drops, spikes, promotions and out-of-stock events
- Compare the same product across all retailers to find the best margin opportunities
- Calculate your competitive position score (are you cheapest, mid-range or overpriced?)
- Detect when competitors run flash sales, coupons or bundle deals
- Generate AI repricing recommendations based on market position and margin targets
- Trigger instant alerts when a competitor changes price below your threshold
- Build historical price datasets for trend analysis and seasonal planning
- Schedule automated daily or hourly price surveillance runs
- Export everything as CSV, JSON or direct webhook to your repricing tool

---

## Step 1: Set Up Your Price Engine

This skill uses [Apify](https://www.apify.com?fpr=dx06p) to scrape pricing data across all major marketplaces.

1. Create your free account at [Apify](https://www.apify.com?fpr=dx06p)
2. Go to **Settings > Integrations** and copy your Personal API Token
3. Store it securely:
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

> Free tier includes $5/month of compute. Enough to monitor 100+ products daily across multiple platforms.

---

## Step 2: Install Dependencies

```bash
npm install apify-client axios
```

---

## Apify Actors by Platform

| Actor | Platform | Data Extracted |
|---|---|---|
| [Apify Amazon Product Scraper](https://www.apify.com?fpr=dx06p) | Amazon | Price, rating, ASIN, seller, stock status, deal badge |
| [Apify Amazon Search Scraper](https://www.apify.com?fpr=dx06p) | Amazon | Search results with prices, bestseller rank |
| [Apify Amazon Reviews Scraper](https://www.apify.com?fpr=dx06p) | Amazon | Reviews, star distribution, verified purchases |
| [Apify eBay Scraper](https://www.apify.com?fpr=dx06p) | eBay | Listings, sold prices, seller ratings, bid count |
| [Apify Walmart Scraper](https://www.apify.com?fpr=dx06p) | Walmart | Prices, availability, pickup/delivery options |
| [Apify AliExpress Scraper](https://www.apify.com?fpr=dx06p) | AliExpress | Product data, shipping cost, seller rating |
| [Apify Zalando Scraper](https://www.apify.com?fpr=dx06p) | Zalando | Prices, sizes, brands, discounts |
| [Apify Google Shopping Scraper](https://www.apify.com?fpr=dx06p) | Google Shopping | Aggregated prices from all retailers |

---

## Examples

### Monitor Specific Products by URL

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

async function monitorProducts(productUrls) {
  const run = await client.actor("apify/amazon-product-scraper").call({
    productUrls: productUrls.map(url => ({ url })),
    maxReviews: 0
  });

  const { items } = await run.dataset().getData();

  return items.map(p => ({
    name: p.title,
    asin: p.asin,
    currentPrice: p.price,
    originalPrice: p.originalPrice,
    discount: p.originalPrice ? Math.round((1 - p.price / p.originalPrice) * 100) : 0,
    currency: p.currency || 'USD',
    rating: p.rating,
    reviewCount: p.reviewsCount,
    availability: p.availability,
    seller: p.seller,
    hasDealBadge: p.deal || false,
    url: p.url,
    scrapedAt: new Date().toISOString()
  }));
}

const products = await monitorProducts([
  "https://www.amazon.com/dp/B09G9HD6PD",
  "https://www.amazon.com/dp/B08N5WRWNW",
  "https://www.amazon.com/dp/B09XS7JWHH"
]);

products.forEach(p => {
  console.log(`${p.name}: $${p.currentPrice} ${p.discount > 0 ? `(${p.discount}% off)` : ''} ${p.hasDealBadge ? '[DEAL]' : ''}`);
});
```

---

### Cross-Platform Price Comparison

```javascript
async function compareAcrossPlatforms(searchQuery) {
  const [amazonRun, ebayRun, walmartRun, googleRun] = await Promise.all([
    client.actor("apify/amazon-search-scraper").call({
      searchQueries: [searchQuery],
      maxResultsPerQuery: 10,
      country: "US"
    }),
    client.actor("apify/ebay-scraper").call({
      searchQueries: [searchQuery],
      maxResults: 10
    }),
    client.actor("apify/walmart-scraper").call({
      searchQueries: [searchQuery],
      maxResults: 10
    }),
    client.actor("apify/google-shopping-scraper").call({
      queries: [searchQuery],
      maxResults: 10,
      country: "US"
    })
  ]);

  const [amz, ebay, wm, gs] = await Promise.all([
    amazonRun.dataset().getData(),
    ebayRun.dataset().getData(),
    walmartRun.dataset().getData(),
    googleRun.dataset().getData()
  ]);

  const all = [
    ...amz.items.map(i => ({ ...i, source: 'amazon', price: i.price })),
    ...ebay.items.map(i => ({ ...i, source: 'ebay', price: i.price })),
    ...wm.items.map(i => ({ ...i, source: 'walmart', price: i.price })),
    ...gs.items.map(i => ({ ...i, source: 'google_shopping', price: i.price }))
  ].filter(i => i.price && i.price > 0).sort((a, b) => a.price - b.price);

  const cheapest = all[0];
  const mostExpensive = all[all.length - 1];
  const avgPrice = Math.round(all.reduce((s, i) => s + i.price, 0) / all.length * 100) / 100;

  return {
    query: searchQuery,
    totalResults: all.length,
    cheapest: { source: cheapest.source, price: cheapest.price, title: cheapest.title },
    mostExpensive: { source: mostExpensive.source, price: mostExpensive.price },
    avgPrice,
    priceSpread: Math.round((mostExpensive.price - cheapest.price) / cheapest.price * 100),
    allResults: all,
    comparedAt: new Date().toISOString()
  };
}

const comparison = await compareAcrossPlatforms("Sony WH-1000XM5");
console.log(`Cheapest: $${comparison.cheapest.price} on ${comparison.cheapest.source}`);
console.log(`Price spread: ${comparison.priceSpread}% between cheapest and most expensive`);
```

---

### Competitive Position Scoring

```javascript
function scoreCompetitivePosition(yourPrice, marketData) {
  const prices = marketData.allResults.map(r => r.price).sort((a, b) => a - b);
  const rank = prices.filter(p => p < yourPrice).length + 1;
  const percentile = Math.round((1 - rank / prices.length) * 100);

  let position, recommendation;

  if (percentile >= 80) {
    position = 'OVERPRICED';
    recommendation = `You are more expensive than ${percentile}% of competitors. Consider dropping to $${marketData.avgPrice} or adding value to justify premium.`;
  } else if (percentile >= 50) {
    position = 'MID-RANGE';
    recommendation = `You are in the middle of the pack. Differentiate with bundles, faster shipping, or better reviews to win at this price.`;
  } else if (percentile >= 20) {
    position = 'COMPETITIVE';
    recommendation = `Good position. You are cheaper than ${100 - percentile}% of competitors. Maintain and focus on conversion.`;
  } else {
    position = 'CHEAPEST';
    recommendation = `You are the cheapest option. Consider raising price by 5-10% to capture more margin without losing rank.`;
  }

  return {
    yourPrice,
    marketAvg: marketData.avgPrice,
    cheapestInMarket: prices[0],
    rank: `${rank} of ${prices.length}`,
    percentile,
    position,
    recommendation,
    priceToMatch: prices[0],
    priceToWin: Math.max(prices[0] - 0.01, 0)
  };
}

const position = scoreCompetitivePosition(299.99, comparison);
console.log(`Position: ${position.position} (${position.rank})`);
console.log(`Recommendation: ${position.recommendation}`);
```

---

### Price Alert System with Webhook

```javascript
async function priceAlertCheck(watchlist) {
  const alerts = [];

  for (const item of watchlist) {
    const run = await client.actor("apify/amazon-product-scraper").call({
      productUrls: [{ url: item.url }],
      maxReviews: 0
    });

    const { items } = await run.dataset().getData();
    const product = items[0];

    if (!product) continue;

    const priceChange = item.lastKnownPrice
      ? Math.round((product.price - item.lastKnownPrice) / item.lastKnownPrice * 100)
      : 0;

    if (product.price < item.alertBelow) {
      alerts.push({
        type: 'PRICE_DROP_BELOW_TARGET',
        product: product.title,
        currentPrice: product.price,
        targetPrice: item.alertBelow,
        savings: Math.round((item.alertBelow - product.price) * 100) / 100,
        url: item.url,
        detectedAt: new Date().toISOString()
      });
    }

    if (Math.abs(priceChange) >= 10) {
      alerts.push({
        type: priceChange < 0 ? 'MAJOR_PRICE_DROP' : 'MAJOR_PRICE_INCREASE',
        product: product.title,
        oldPrice: item.lastKnownPrice,
        newPrice: product.price,
        changePercent: priceChange,
        url: item.url,
        detectedAt: new Date().toISOString()
      });
    }

    if (product.availability && product.availability.includes('Out of Stock')) {
      alerts.push({
        type: 'OUT_OF_STOCK',
        product: product.title,
        lastPrice: product.price,
        url: item.url,
        detectedAt: new Date().toISOString()
      });
    }
  }

  // Send alerts via webhook
  if (alerts.length > 0) {
    await axios.post(process.env.WEBHOOK_URL || 'https://hooks.slack.com/your-webhook', {
      text: `Price Alerts (${alerts.length}):\n${alerts.map(a =>
        `${a.type}: ${a.product} - $${a.currentPrice || a.newPrice} ${a.changePercent ? `(${a.changePercent}%)` : ''}`
      ).join('\n')}`
    });
  }

  return alerts;
}

// Example watchlist
const watchlist = [
  { url: "https://www.amazon.com/dp/B09XS7JWHH", alertBelow: 250, lastKnownPrice: 279.99 },
  { url: "https://www.amazon.com/dp/B09G9HD6PD", alertBelow: 100, lastKnownPrice: 129.99 }
];

const alerts = await priceAlertCheck(watchlist);
console.log(`${alerts.length} alerts triggered`);
```

---

### AI Repricing Recommendations

```javascript
import axios from 'axios';

async function getRepricingAdvice(product, marketData) {
  const competitorPrices = marketData.allResults
    .map(r => `${r.source}: $${r.price}`)
    .join(', ');

  const prompt = `You are a pricing strategist. Analyze this product's market position and recommend an optimal price.

PRODUCT: ${product.name}
YOUR CURRENT PRICE: $${product.currentPrice}
YOUR COST: $${product.costPrice || 'Unknown'}
YOUR RATING: ${product.rating}/5 (${product.reviewCount} reviews)

COMPETITOR PRICES: ${competitorPrices}
MARKET AVERAGE: $${marketData.avgPrice}
CHEAPEST: $${marketData.cheapest.price} (${marketData.cheapest.source})
PRICE SPREAD: ${marketData.priceSpread}%

PROVIDE:
1. Recommended price (specific number)
2. Reasoning (2 sentences max)
3. Expected impact on sales volume (increase/decrease/stable)
4. Margin impact vs current price
5. Alternative strategy if you want to stay premium

Keep it data-driven and concise.`;

  const { data } = await axios.post('https://api.anthropic.com/v1/messages', {
    model: "claude-sonnet-4-20250514",
    max_tokens: 400,
    messages: [{ role: "user", content: prompt }]
  }, {
    headers: {
      'x-api-key': process.env.CLAUDE_API_KEY,
      'anthropic-version': '2023-06-01'
    }
  });

  return data.content[0].text;
}
```

---

### Full Pipeline: Monitor, Compare, Score, Alert, Export

```javascript
import { writeFileSync } from 'fs';

async function fullPriceIntelPipeline(products, searchQuery) {
  console.log('Starting Price Intelligence Pipeline...');

  // STEP 1: Monitor your products
  const monitored = await monitorProducts(products);
  console.log(`Step 1: ${monitored.length} products monitored`);

  // STEP 2: Compare across platforms
  const comparison = await compareAcrossPlatforms(searchQuery);
  console.log(`Step 2: ${comparison.totalResults} competitor prices found`);

  // STEP 3: Score position for each product
  const scored = monitored.map(product => ({
    ...product,
    position: scoreCompetitivePosition(product.currentPrice, comparison)
  }));

  // STEP 4: Generate repricing advice for overpriced items
  for (const product of scored.filter(p => p.position.position === 'OVERPRICED')) {
    product.repricingAdvice = await getRepricingAdvice(product, comparison);
    await new Promise(r => setTimeout(r, 500));
  }

  // STEP 5: Export
  const report = {
    generatedAt: new Date().toISOString(),
    query: searchQuery,
    products: scored,
    marketOverview: {
      avgPrice: comparison.avgPrice,
      cheapest: comparison.cheapest,
      priceSpread: comparison.priceSpread,
      totalCompetitors: comparison.totalResults
    }
  };

  const filename = `price-intel-${Date.now()}.json`;
  writeFileSync(filename, JSON.stringify(report, null, 2));
  console.log(`Report exported to ${filename}`);

  // CSV export
  const headers = ["name","currentPrice","originalPrice","discount","rating","reviewCount","availability","position","recommendation"];
  const csv = [
    headers.join(","),
    ...scored.map(p => [
      `"${p.name}"`, p.currentPrice, p.originalPrice || '', p.discount,
      p.rating, p.reviewCount, `"${p.availability}"`,
      `"${p.position.position}"`, `"${p.position.recommendation}"`
    ].join(","))
  ].join("\n");

  writeFileSync(`price-intel-${Date.now()}.csv`, csv);
  return report;
}

await fullPriceIntelPipeline(
  ["https://www.amazon.com/dp/B09XS7JWHH"],
  "wireless noise cancelling headphones"
);
```

---

## Normalized Price Schema

```json
{
  "name": "Sony WH-1000XM5 Wireless Headphones",
  "asin": "B09XS7JWHH",
  "source": "amazon",
  "currentPrice": 279.99,
  "originalPrice": 349.99,
  "discount": 20,
  "currency": "USD",
  "rating": 4.5,
  "reviewCount": 12847,
  "availability": "In Stock",
  "seller": "Amazon.com",
  "hasDealBadge": false,
  "competitivePosition": "MID-RANGE",
  "positionPercentile": 55,
  "url": "https://www.amazon.com/dp/B09XS7JWHH",
  "scrapedAt": "2025-02-25T10:00:00Z"
}
```

---

## What Makes This Different

| Feature | Basic Price Tracker | This Skill |
|---|---|---|
| Platforms | 1 marketplace | 6+ marketplaces in parallel |
| Price comparison | Same platform only | Cross-platform with spread analysis |
| Competitive scoring | None | Position percentile + actionable advice |
| Repricing | Manual | AI-generated recommendations per product |
| Alerts | Basic threshold | Price drops + stock changes + deal badges |
| Historical tracking | None | Timestamped data for trend analysis |
| Export | Raw data | CRM-ready CSV + JSON + webhook |

---

## Scheduling Automated Monitoring

Use [Apify Schedules](https://www.apify.com?fpr=dx06p) for hands-free monitoring:

1. Go to https://console.apify.com/schedules
2. Create a new schedule (daily at 8am or every 6 hours)
3. Select your actor and saved input configuration
4. Enable webhook notifications for price change alerts
5. Connect to Slack, email or your repricing tool via webhook

---

## Pro Tips

1. **Monitor by ASIN** (not URL) for consistent Amazon tracking across regions
2. **Track competitor sold prices on eBay** to understand actual market clearing price, not just listing price
3. **Use Google Shopping** as a meta-comparison since it aggregates prices from hundreds of retailers
4. **Set alerts at 10%+ change** to catch real moves and filter out normal fluctuations
5. **Run price checks during off-peak hours** (2am to 6am) for fastest results and lowest cost
6. **Cross-reference price drops with review count drops** to detect competitors clearing inventory before discontinuation
7. **Build a 30-day price chart** per product to identify seasonal patterns and time your promotions

---

## Cost Estimate

| Action | Apify CU | Cost |
|---|---|---|
| Monitor 10 products (1 platform) | ~0.05 CU | ~$0.02 |
| Cross-platform comparison (4 platforms) | ~0.20 CU | ~$0.08 |
| Full pipeline (monitor + compare + alerts) | ~0.30 CU | ~$0.12 |
| Daily monitoring (100 products, 4 platforms) | ~3.0 CU/day | ~$1.20/day |
| Monthly automated surveillance | ~90 CU/month | ~$36/month |

Compare that to Prisync at $99/month or Competera at $500/month. Scale with [Apify](https://www.apify.com?fpr=dx06p) as you grow.

---

## Error Handling

```javascript
try {
  const run = await client.actor("apify/amazon-product-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token. Get yours at https://www.apify.com?fpr=dx06p");
  if (error.statusCode === 429) throw new Error("Rate limit. Reduce batch size or add delays.");
  if (error.statusCode === 404) throw new Error("Product page not found. Check the URL or ASIN.");
  if (error.message.includes("timeout")) throw new Error("Scrape timed out. Try fewer products per run.");
  throw error;
}
```

---

## Requirements

- An [Apify](https://www.apify.com?fpr=dx06p) account with API token
- Node.js 18+ with `apify-client` and `axios`
- Claude API key for repricing recommendations (optional but recommended)
- A repricing tool, dashboard or spreadsheet to receive data (Prisync, Wiser, Excel, Airtable)
- Optional: Slack or email webhook for real-time alerts

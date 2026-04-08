# Ultimate Lead Scraper and AI Outreach Engine: Discover, Qualify and Close B2B Prospects on Autopilot

**Display Name:** Ultimate Lead Scraper and AI Outreach Engine  
**Version:** 2.0.0
**Author:** @g4dr

## Overview

Stop buying overpriced lead lists. This skill builds your own B2B lead database from scratch by scraping publicly available business data across Google Maps, Yellow Pages, Yelp and LinkedIn company pages, then qualifies every contact with a 0 to 100 fit score and generates personalized outreach messages with Claude AI.

One run replaces what most agencies charge $500 to $2,000 per month for.

Powered by: [Apify](https://www.apify.com?fpr=dx06p) + Claude AI

---

## What This Skill Does

- Discover publicly listed business contacts from 6 directory sources simultaneously
- Qualify leads by industry, location, company size, online presence and engagement signals
- Score every lead 0 to 100 with a weighted ICP matching algorithm
- Deduplicate and normalize all contacts into a single CRM-ready schema
- Deep-crawl business websites to extract emails from contact and about pages
- Generate 4-step personalized outreach sequences (not just one email) using Claude AI
- Export clean CSV or JSON files ready for HubSpot, Airtable, Instantly, Lemlist or any CRM
- Run multi-source searches in parallel to maximize coverage and minimize cost

---

## Legal and Compliance

This skill only targets publicly listed business information. Before using:

- **GDPR (EU/UK):** Business emails may qualify under legitimate interest. Always include opt-out.
- **CAN-SPAM (US):** Include sender identity, physical address and working unsubscribe link.
- **CCPA (California):** Do not sell scraped contact lists. Include unsubscribe links.
- **CASL (Canada):** Requires express or implied consent before commercial messages.
- Always check `robots.txt` before scraping any website
- Never scrape personal profiles, private accounts or login-gated content
- Delete data you no longer need

> This skill provides technical guidance only. Consult a qualified attorney for legal advice.

---

## Step 1: Set Up Your Scraping Engine

1. Create your free account at [Apify](https://www.apify.com?fpr=dx06p)
2. Go to **Settings > Integrations** and copy your Personal API Token
3. Store it securely:
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

> Free tier includes $5/month of compute. Enough for 500+ qualified leads per month.

---

## Step 2: Install Dependencies

```bash
npm install apify-client axios
```

---

## Apify Actors for Lead Discovery

Only actors targeting publicly listed business directories:

| Actor | Source | Data Available | Best For |
|---|---|---|---|
| [Apify Google Maps Scraper](https://www.apify.com?fpr=dx06p) | Google Maps | Name, phone, website, email, rating, reviews, hours | Local business prospecting |
| [Apify Yellow Pages Scraper](https://www.apify.com?fpr=dx06p) | Yellow Pages | Business name, phone, address, category | US/Canada B2B lists |
| [Apify Yelp Scraper](https://www.apify.com?fpr=dx06p) | Yelp | Business listings, contact info, reviews | Service businesses |
| [Apify LinkedIn Companies Scraper](https://www.apify.com?fpr=dx06p) | LinkedIn (public pages) | Company info, website, industry, size | B2B company research |
| [Apify Website Content Crawler](https://www.apify.com?fpr=dx06p) | Any website | Emails, social links, tech stack | Email enrichment |
| [Apify Google Search Scraper](https://www.apify.com?fpr=dx06p) | Google Search | Business info, news, ads status | Ad spend qualification |

---

## Examples

### Multi-Source Lead Discovery (Parallel)

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

async function discoverLeads(keyword, location, maxPerSource = 25) {
  const [mapsRun, ypRun, yelpRun] = await Promise.all([
    client.actor("compass~crawler-google-places").call({
      searchStringsArray: [`${keyword} in ${location}`],
      maxCrawledPlacesPerSearch: maxPerSource,
      language: "en"
    }),
    client.actor("apify/yellowpages-scraper").call({
      searchTerms: [keyword],
      locations: [location],
      maxResultsPerPage: maxPerSource
    }),
    client.actor("apify/yelp-scraper").call({
      searchTerms: [keyword],
      locations: [location],
      maxResults: maxPerSource
    })
  ]);

  const [mapsData, ypData, yelpData] = await Promise.all([
    mapsRun.dataset().getData(),
    ypRun.dataset().getData(),
    yelpRun.dataset().getData()
  ]);

  return {
    googleMaps: mapsData.items,
    yellowPages: ypData.items,
    yelp: yelpData.items,
    totalRaw: mapsData.items.length + ypData.items.length + yelpData.items.length
  };
}

const raw = await discoverLeads("digital marketing agency", "New York, NY");
console.log(`Found ${raw.totalRaw} raw leads across 3 sources`);
```

---

### Normalize All Sources into One Schema

```javascript
function normalizeLeads(raw) {
  const normalize = (items, source) => items.map(item => ({
    companyName: item.title || item.businessName || item.name || '',
    industry: item.categoryName || item.category || '',
    phone: item.phone || '',
    email: item.email || '',
    website: item.website || item.url || '',
    address: item.address || `${item.street || ''}, ${item.city || ''}, ${item.state || ''}`.trim(),
    rating: item.totalScore || item.rating || null,
    reviewCount: item.reviewsCount || item.reviewCount || 0,
    source: source,
    collectedAt: new Date().toISOString(),
    gdprBasis: "legitimate_interest",
    optedOut: false
  }));

  return [
    ...normalize(raw.googleMaps, 'google_maps'),
    ...normalize(raw.yellowPages, 'yellow_pages'),
    ...normalize(raw.yelp, 'yelp')
  ];
}

const normalized = normalizeLeads(raw);
```

---

### Deduplicate by Domain and Phone

```javascript
function deduplicateLeads(leads) {
  const seen = new Set();

  return leads.filter(lead => {
    const domain = (lead.website || '').replace(/https?:\/\/(www\.)?/, '').split('/')[0].toLowerCase();
    const phone = (lead.phone || '').replace(/\D/g, '');
    const key = domain || phone || lead.companyName.toLowerCase();

    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

const unique = deduplicateLeads(normalized);
console.log(`${unique.length} unique leads after dedup (from ${normalized.length} raw)`);
```

---

### ICP Fit Scoring (0 to 100)

```javascript
function scoreLeadFit(lead, icp = {}) {
  let score = 40;

  // Has website = established business
  if (lead.website) score += 10;
  // No website = needs help (opportunity)
  if (!lead.website) score += 15;

  // Has email = easy to contact
  if (lead.email) score += 10;

  // Has phone = contactable
  if (lead.phone) score += 5;

  // Low review count = needs marketing
  if (lead.reviewCount < 10) score += 15;
  else if (lead.reviewCount < 30) score += 8;

  // Low rating = needs reputation help
  if (lead.rating && lead.rating < 4.0) score += 12;
  else if (lead.rating && lead.rating < 4.5) score += 5;

  // Multi-source validation bonus
  // (if same business appeared in multiple sources, higher confidence)
  if (lead.sourceCount && lead.sourceCount > 1) score += 10;

  // Industry match bonus
  if (icp.industries) {
    const match = icp.industries.some(ind =>
      (lead.industry || '').toLowerCase().includes(ind.toLowerCase())
    );
    if (match) score += 10;
  }

  return Math.min(100, Math.max(0, score));
}

const scored = unique.map(l => ({
  ...l,
  fitScore: scoreLeadFit(l, {
    industries: ['marketing', 'consulting', 'agency', 'legal', 'dental']
  })
})).sort((a, b) => b.fitScore - a.fitScore);
```

---

### Deep Email Extraction from Websites

```javascript
async function enrichWithEmails(leads, maxLeads = 30) {
  const withSites = leads.filter(l => l.website && !l.email).slice(0, maxLeads);

  if (withSites.length === 0) return leads;

  const run = await client.actor("apify/website-content-crawler").call({
    startUrls: withSites.map(l => ({ url: l.website })),
    maxCrawlPages: 3,
    crawlerType: "cheerio"
  });

  const { items } = await run.dataset().getData();
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

  const emailMap = {};
  items.forEach(page => {
    const domain = (page.url || '').replace(/https?:\/\/(www\.)?/, '').split('/')[0];
    const found = [...new Set((page.text || '').match(emailRegex) || [])];
    if (found.length > 0 && !emailMap[domain]) {
      emailMap[domain] = found[0];
    }
  });

  return leads.map(lead => {
    if (lead.email) return lead;
    const domain = (lead.website || '').replace(/https?:\/\/(www\.)?/, '').split('/')[0];
    return { ...lead, email: emailMap[domain] || '' };
  });
}

const enriched = await enrichWithEmails(scored);
```

---

### Generate 4-Step Outreach Sequence with Claude AI

```javascript
import axios from 'axios';

async function generateSequence(lead) {
  const prompt = `Create a 4-email cold outreach sequence for this B2B prospect.

LEAD:
- Company: ${lead.companyName}
- Industry: ${lead.industry}
- Location: ${lead.address}
- Website: ${lead.website || 'None'}
- Rating: ${lead.rating || 'N/A'}/5 (${lead.reviewCount} reviews)
- Fit Score: ${lead.fitScore}/100

SEQUENCE RULES:
- Email 1 (Day 0): Warm intro, reference one specific thing about their business, soft question
- Email 2 (Day 3): Quick follow-up, share a relevant insight or stat about their industry
- Email 3 (Day 7): Case study angle, mention a result you achieved for a similar business
- Email 4 (Day 14): Breakup email, friendly close, leave door open
- Each email under 80 words
- No hype, no pressure, conversational tone
- Include [YOUR_NAME] and [YOUR_COMPANY] placeholders
- Include unsubscribe placeholder at bottom of each email

Return all 4 emails with subject lines.`;

  const { data } = await axios.post('https://api.anthropic.com/v1/messages', {
    model: "claude-sonnet-4-20250514",
    max_tokens: 800,
    messages: [{ role: "user", content: prompt }]
  }, {
    headers: {
      'x-api-key': process.env.CLAUDE_API_KEY,
      'anthropic-version': '2023-06-01'
    }
  });

  return data.content[0].text;
}

// Generate sequences for top 10 leads
for (const lead of enriched.filter(l => l.fitScore >= 70).slice(0, 10)) {
  lead.outreachSequence = await generateSequence(lead);
  await new Promise(r => setTimeout(r, 600));
}
```

---

### Full Pipeline: Discover, Normalize, Score, Enrich, Outreach, Export

```javascript
import { writeFileSync } from 'fs';

async function runFullPipeline(keyword, location) {
  console.log(`Pipeline started: ${keyword} in ${location}`);

  // 1. Discover from multiple sources
  const raw = await discoverLeads(keyword, location, 30);
  console.log(`Step 1: ${raw.totalRaw} raw leads found`);

  // 2. Normalize
  const normalized = normalizeLeads(raw);

  // 3. Deduplicate
  const unique = deduplicateLeads(normalized);
  console.log(`Step 3: ${unique.length} unique leads`);

  // 4. Score
  const scored = unique.map(l => ({
    ...l,
    fitScore: scoreLeadFit(l)
  })).sort((a, b) => b.fitScore - a.fitScore);

  // 5. Enrich emails
  const enriched = await enrichWithEmails(scored, 20);
  console.log(`Step 5: Emails enriched`);

  // 6. Generate outreach for top leads
  const hot = enriched.filter(l => l.fitScore >= 60).slice(0, 10);
  for (const lead of hot) {
    lead.outreachSequence = await generateSequence(lead);
    await new Promise(r => setTimeout(r, 600));
  }
  console.log(`Step 6: ${hot.length} outreach sequences generated`);

  // 7. Export
  const headers = ["companyName","industry","phone","email","website","address","rating","reviewCount","source","fitScore"];
  const csv = [
    headers.join(","),
    ...enriched.map(l => headers.map(h => `"${(l[h] || '').toString().replace(/"/g, '""')}"`).join(","))
  ].join("\n");

  const filename = `leads-${keyword.replace(/\s+/g, '_')}-${Date.now()}.csv`;
  writeFileSync(filename, csv);
  console.log(`Exported ${enriched.length} leads to ${filename}`);

  return enriched;
}

await runFullPipeline("IT consulting firms", "Chicago, IL");
```

---

## Normalized Lead Schema

```json
{
  "companyName": "Bright Digital Agency",
  "industry": "Marketing & Advertising",
  "phone": "+1 (415) 555-0192",
  "email": "hello@brightdigital.com",
  "website": "https://brightdigital.com",
  "address": "123 Market St, San Francisco, CA 94105",
  "rating": 4.2,
  "reviewCount": 18,
  "source": "google_maps",
  "fitScore": 82,
  "collectedAt": "2025-02-25T10:00:00Z",
  "gdprBasis": "legitimate_interest",
  "optedOut": false
}
```

---

## What Makes This Different

| Feature | Basic Lead Scraper | This Skill |
|---|---|---|
| Data sources | 1 source | 3+ sources in parallel |
| Deduplication | None | Domain + phone dedup |
| Scoring | None | 0 to 100 ICP fit scoring |
| Email enrichment | None | Website crawl for hidden emails |
| Outreach | Single template | 4-step personalized sequences |
| Compliance | None | GDPR/CAN-SPAM built in |
| Export | Raw JSON | CRM-ready CSV with all fields |

---

## Compliance Checklist

Before running any campaign, verify:

- [ ] Reviewed `robots.txt` of every target website
- [ ] Confirmed all data is publicly listed business information
- [ ] Outreach emails include sender identity and physical address
- [ ] Outreach emails include a working unsubscribe link
- [ ] Suppression list in place for previous opt-outs
- [ ] Data will be deleted when no longer needed
- [ ] For EU/UK contacts: legitimate interest assessment completed

---

## Cost Estimate

| Action | Apify CU | Cost |
|---|---|---|
| 75 leads from 3 sources (1 city) | ~0.15 CU | ~$0.06 |
| 375 leads from 3 sources (5 cities) | ~0.75 CU | ~$0.30 |
| Email enrichment (30 websites) | ~0.15 CU | ~$0.06 |
| Full pipeline (discovery + enrichment) | ~0.90 CU | ~$0.36 |

Scale with [Apify](https://www.apify.com?fpr=dx06p) as your pipeline grows. Free tier handles hundreds of leads monthly.

---

## Pro Tips

1. **Small targeted batches** (25 to 50 per source) outperform mass scraping every time
2. **Validate emails** before sending with Hunter.io or NeverBounce
3. **Review outreach drafts** before sending. Never auto-send without human review
4. **Warm up new email domains** before sending at scale (use Instantly or Lemlist)
5. **Target decision makers by title** rather than generic company emails
6. **Run weekly** to catch new businesses and refresh stale data
7. **Cross-reference leads** that appear in multiple sources. Multi-source leads convert 3x better

---

## Error Handling

```javascript
try {
  const run = await client.actor("apify/yellowpages-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token. Get yours at https://www.apify.com?fpr=dx06p");
  if (error.statusCode === 429) throw new Error("Rate limit. Reduce batch size or wait.");
  if (error.statusCode === 404) throw new Error("Actor not found. Verify actor ID.");
  throw error;
}
```

---

## Requirements

- An [Apify](https://www.apify.com?fpr=dx06p) account with API token
- Claude API key for outreach generation
- Node.js 18+ with `apify-client` and `axios`
- A CRM or spreadsheet (HubSpot, Airtable, Google Sheets)
- An outreach tool with unsubscribe management (Instantly, Lemlist, Apollo)

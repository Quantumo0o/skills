---
name: news-source-manager
description: Manages user's news category preferences and information sources. Stores in news-sources.json, supports add/remove/list operations. Use when (1) user wants to customize news categories, (2) user mentions "add news source" or "change news preferences", (3) insight-radar skill needs to load news config.
---

# News Source Manager (信息源管理器)

**Purpose**: Centralized management of user's news interests and trusted sources.

---

## 📂 Data Structure

Stores in: `~/.openclaw/workspace/memory/news-sources.json`

```json
{
  "categories": [
    {
      "name": "AI/Tech",
      "keywords": ["AI", "machine learning", "LLM", "GPT", "tech trends"],
      "sources": [
        {"name": "TechCrunch", "url": "techcrunch.com", "priority": 1},
        {"name": "MIT Technology Review", "url": "technologyreview.com", "priority": 1},
        {"name": "Ars Technica", "url": "arstechnica.com", "priority": 2}
      ],
      "active": true,
      "search_params": {
        "freshness": "day",
        "count": 5
      }
    },
    {
      "name": "Finance/Crypto",
      "keywords": ["crypto", "bitcoin", "DeFi", "markets"],
      "sources": [
        {"name": "Bloomberg", "url": "bloomberg.com", "priority": 1},
        {"name": "CoinDesk", "url": "coindesk.com", "priority": 1}
      ],
      "active": false,
      "search_params": {
        "freshness": "day",
        "count": 3
      }
    }
  ],
  "last_updated": "2026-03-23T15:20:00+08:00",
  "user_confirmed": true
}
```

---

## 🔧 Operations

### 1. Initialize (首次使用)

**When**: User first uses insight-radar, or news-sources.json doesn't exist

**Steps**:
1. Detect missing config
2. Ask user: "我需要了解你关注哪些新闻类别，方便帮你定制信息源。"
3. Provide default options:
   ```
   我为你准备了常见类别：
   1. AI/Tech (AI、科技趋势)
   2. Business Strategy (商业战略、管理)
   3. Finance/Crypto (金融、加密货币)
   4. Health/Bio (医疗、生物科技)
   5. Energy/Climate (能源、气候科技)
   6. Policy/Regulation (政策、监管)
   
   你对哪些感兴趣？(可以多选，用逗号分隔，如: 1,2,3)
   或者告诉我你的自定义类别。
   ```

4. User responds: e.g., "1,2" or "AI/Tech, 产品设计"

5. Show recommended sources for selected categories:
   ```
   好的！为你的 AI/Tech 类别推荐以下信息源：
   ✅ TechCrunch (科技新闻)
   ✅ MIT Technology Review (深度分析)
   ✅ Ars Technica (技术评测)
   
   这些看起来合适吗？
   - 回复 "确认" 使用默认配置
   - 回复 "修改" 自定义信息源
   - 回复 "添加 <网站名>" 增加信息源
   ```

6. User confirms or modifies

7. Write to `news-sources.json`

8. Confirm: "✅ 配置已保存！明天早上 09:00 会根据这些类别为你筛选新闻。"

---

### 2. List Current Config

**Trigger**: User asks "我的新闻配置是什么" or "show my news sources"

**Steps**:
1. Read `news-sources.json`
2. Display in friendly format:
   ```
   📰 你的新闻配置
   
   ✅ AI/Tech (启用)
      关键词: AI, machine learning, LLM
      信息源: TechCrunch, MIT Tech Review, Ars Technica
      更新频率: 每天
   
   ⏸️ Finance/Crypto (未启用)
      信息源: Bloomberg, CoinDesk
   
   最后更新: 2026-03-23
   ```

3. Ask: "需要修改吗？"

---

### 3. Add Category

**Trigger**: User says "添加新闻类别: 产品设计" or "add category: UX design"

**Steps**:
1. Extract category name from user input
2. Ask for keywords:
   ```
   好的！为 "产品设计" 类别设置关键词。
   建议: product design, UX, UI, user experience
   
   你可以直接确认，或者自定义关键词（用逗号分隔）
   ```

3. User confirms or customizes

4. Ask for sources:
   ```
   推荐信息源（产品设计类）:
   1. Nielsen Norman Group (nngroup.com)
   2. UX Design (uxdesign.cc)
   3. Smashing Magazine (smashingmagazine.com)
   
   - 回复 "确认" 使用推荐
   - 回复 "自定义" 手动输入
   ```

5. User confirms

6. Add to `news-sources.json`

7. Confirm: "✅ 已添加 '产品设计' 类别，明天开始生效。"

---

### 4. Remove Category

**Trigger**: User says "删除类别: Finance" or "disable crypto news"

**Steps**:
1. Find matching category
2. Ask for confirmation:
   ```
   ⚠️ 确认删除 "Finance/Crypto" 类别吗？
   删除后将不再接收该类别的新闻。
   
   回复 "确认" 删除，或 "取消"
   ```

3. User confirms

4. Remove from (or set `active: false` in) `news-sources.json`

5. Confirm: "✅ 已删除 'Finance/Crypto' 类别。"

---

### 5. Modify Sources

**Trigger**: User says "TechCrunch质量不行，换成The Verge" or "add source: Hacker News"

**Steps**:
1. Parse intent: remove/add/replace
2. Find affected category
3. Show before/after:
   ```
   AI/Tech 类别信息源变更：
   
   ❌ 移除: TechCrunch
   ✅ 添加: The Verge
   
   新配置:
   - MIT Technology Review
   - Ars Technica
   - The Verge
   
   确认修改吗？
   ```

4. User confirms

5. Update `news-sources.json`

6. Confirm: "✅ 信息源已更新。"

---

### 6. Export Config (for insight-radar)

**Trigger**: Called by `insight-radar` skill

**Steps**:
1. Read `news-sources.json`
2. Filter `active: true` categories
3. Return as structured data:
   ```json
   {
     "active_categories": [
       {
         "name": "AI/Tech",
         "keywords": ["AI", "machine learning"],
         "sources": ["TechCrunch", "MIT Tech Review"],
         "search_params": {"freshness": "day", "count": 5}
       }
     ]
   }
   ```

---

## 🧠 Default Category Templates

When user selects a standard category, use these templates:

| Category | Keywords | Default Sources |
|----------|----------|-----------------|
| **AI/Tech** | AI, artificial intelligence, machine learning, deep learning, LLM, large language model, GPT, GPT-4, GPT-5, Claude, ChatGPT, Gemini, generative AI, AGI, artificial general intelligence, neural networks, transformers, computer vision, NLP, natural language processing, reinforcement learning, tech trends, tech innovation, OpenAI, Anthropic, Google AI, DeepMind, Meta AI, Microsoft AI, AI agents, autonomous agents, AI safety, AI alignment, prompt engineering, fine-tuning, RAG, retrieval augmented generation, multimodal AI, text-to-image, DALL-E, Midjourney, Stable Diffusion, AI chip, GPU, TPU, NVIDIA, semiconductor, AI infrastructure, edge computing, AI hardware | TechCrunch, MIT Tech Review, Ars Technica, The Verge, Hacker News, VentureBeat, The Information |
| **Business Strategy** | business model, business strategy, M&A, mergers and acquisitions, disruption, disruptive innovation, innovation, competitive advantage, competitive moat, market strategy, go-to-market, GTM, corporate strategy, strategic planning, digital transformation, platform economics, network effects, two-sided marketplace, aggregation theory, value chain, supply chain, vertical integration, horizontal integration, business development, partnership, strategic alliance, market expansion, product-market fit, PMF, unit economics, customer acquisition cost, CAC, lifetime value, LTV, churn rate, retention, growth strategy, pricing strategy, freemium, subscription model, SaaS, B2B, B2C, enterprise sales | McKinsey, HBR, Harvard Business Review, WSJ, Wall Street Journal, Financial Times, Bloomberg, Strategy+Business, BCG, Bain |
| **Finance/Crypto** | finance, financial markets, stock market, equity market, bond market, trading, algorithmic trading, high-frequency trading, investment, investing, investor, institutional investor, retail investor, venture capital, VC, private equity, PE, startup funding, seed funding, angel investor, IPO, initial public offering, SPAC, direct listing, Series A, Series B, Series C, late-stage funding, unicorn, decacorn, valuation, cap table, liquidation preference, crypto, cryptocurrency, bitcoin, BTC, ethereum, ETH, altcoin, blockchain, distributed ledger, DeFi, decentralized finance, DEX, decentralized exchange, AMM, automated market maker, yield farming, staking, Web3, NFT, non-fungible token, digital assets, tokenomics, smart contract, layer 1, layer 2, scaling, fintech, financial technology, neobank, payment processing, cross-border payment, remittance, BNPL, buy now pay later, financial trends, economic trends, macroeconomics, GDP, recession, inflation, deflation, interest rates, monetary policy, Federal Reserve, Fed, central bank, ECB, quantitative easing, QE, fiscal policy, treasury, bond yield, forex, currency, emerging markets | Bloomberg, CoinDesk, Financial Times, Reuters, WSJ, The Block, Decrypt, CoinTelegraph, The Information, Axios Markets |
| **Health/Bio** | biotech, biotechnology, biopharma, pharma, pharmaceutical, life sciences, health tech, healthtech, digital health, telemedicine, telehealth, remote patient monitoring, medical AI, clinical decision support, drug discovery, drug development, clinical trials, phase 1, phase 2, phase 3, FDA approval, EMA approval, regulatory approval, orphan drug, rare disease, CRISPR, gene editing, gene therapy, cell therapy, CAR-T, immunotherapy, precision medicine, personalized medicine, genomics, proteomics, biomarker, diagnostic, point-of-care testing, medical imaging, radiology AI, healthcare innovation, value-based care, population health, medical devices, wearable, biosensor, continuous glucose monitor, CGM, implantable device, surgical robotics, health insurance, payer, healthcare IT, EHR, electronic health record, interoperability, HIPAA, health data privacy | STAT News, Nature, Science, Cell, The Lancet, NEJM, MedTech Dive, Fierce Biotech, Endpoints News, BioPharma Dive |
| **Energy/Climate** | renewable energy, clean energy, green energy, solar energy, solar panel, photovoltaic, PV, wind energy, wind turbine, offshore wind, onshore wind, nuclear energy, nuclear reactor, SMR, small modular reactor, fusion energy, battery technology, lithium-ion battery, solid-state battery, energy storage, grid-scale storage, EV, electric vehicle, BEV, battery electric vehicle, PHEV, plug-in hybrid, charging infrastructure, fast charging, climate tech, climate technology, climate change mitigation, climate adaptation, carbon capture, CCS, carbon sequestration, direct air capture, DAC, carbon credit, carbon offset, carbon neutral, net zero, net-zero emissions, decarbonization, sustainability, sustainable development, ESG, environmental social governance, circular economy, hydrogen economy, green hydrogen, blue hydrogen, fuel cell, grid modernization, smart grid, transmission, distribution, power generation, baseload power, peak power, demand response, energy efficiency, energy transition, oil and gas, fossil fuel, renewable portfolio standard, RPS, feed-in tariff, tax credit, IRA, Inflation Reduction Act | Canary Media, Greentech Media, Energy Storage News, CleanTechnica, Utility Dive, GTM, GreenBiz, Carbon Brief |
| **Policy/Regulation** | AI regulation, AI governance, AI ethics, responsible AI, AI safety, AI risk, AI alignment, existential risk, antitrust, anti-competitive, monopoly, market power, competition law, merger review, regulatory approval, data privacy, data protection, GDPR, CCPA, privacy law, surveillance, facial recognition, content moderation, misinformation, disinformation, platform liability, Section 230, government policy, tech policy, digital policy, cybersecurity, national security, export control, sanctions, trade war, regulatory compliance, lobbying, government affairs, legislation, bill, law, Congress, Senate, House, EU regulation, European Commission, Digital Services Act, DSA, Digital Markets Act, DMA, AI Act, China regulation, GDPR fine, enforcement action, antitrust lawsuit, regulatory investigation | Politico, The Verge Policy, Axios, Protocol, Bloomberg Government, Lawfare, TechCrunch Policy, The Information, MLex |
| **Product Design** | UX, user experience, UI, user interface, product design, design thinking, human-centered design, interaction design, IxD, visual design, graphic design, design system, component library, design tokens, accessibility, a11y, WCAG, usability, user research, UX research, qualitative research, quantitative research, user testing, usability testing, A/B testing, user interview, persona, user journey, journey map, wireframe, prototype, high-fidelity prototype, low-fidelity prototype, mockup, Figma, Sketch, Adobe XD, Framer, design ops, design workflow, design collaboration, design critique, design review, design QA, design handoff, design leadership, design management, design culture, design maturity, information architecture, IA, navigation, onboarding, empty state, error state, loading state, micro-interaction, animation, motion design, responsive design, mobile-first, progressive enhancement, design sprint, lean UX, agile UX | Nielsen Norman Group, UX Design, Smashing Magazine, A List Apart, Design Better, UX Collective, Interaction Design Foundation, UX Booth, UX Planet |

---

## 🛡️ Keyword Search Fallback Strategy

### ⚠️ CRITICAL: Use Explicit Boolean Logic (Parentheses + OR)

**WRONG (implicit OR - unreliable)**:
```
query: "bitcoin DeFi IPO news"
→ Search engine may interpret as AND or phrase match
→ Unpredictable results
```

**CORRECT (explicit OR + AND)**:
```
query: "(bitcoin OR DeFi OR IPO) AND news"
→ Must match at least one keyword AND must be news
→ Predictable, reliable results
```

---

### 🎯 New Search Strategy: Grouped Parallel Search

Instead of cramming 50 keywords into one query, use **3 independent searches** targeting different sub-domains.

**Analogy**: Send 3 scouts in different directions, not 1 scout with 50 maps.

---

### Level 0: Grouped Parallel Search (Primary)

**For each category, dynamically sample keywords from the full keyword list and divide into 3 business-oriented sub-groups:**

**🔄 Dynamic Keyword Sampling (CRITICAL)**:
- **DO NOT use fixed templates** (e.g., always "GPT-5 OR Claude")
- **From the 50-80 keyword pool**, randomly/round-robin sample **5-8 keywords per sub-group**
- **3 sub-groups** should target **different business directions** (e.g., Trading, Funding, Crypto)
- **Each execution** should use **different keyword combinations** to utilize long-tail keywords

**Example: Finance/Crypto (Dynamic Sampling)**

**Query 1 (Trading/Markets direction)** - Sample 5-8 keywords:
```javascript
// Example run 1:
WebSearch_tool({
  query: "(algorithmic trading OR bond yield OR forex OR treasury OR equity market) AND news",
  freshness: "day",
  count: 4  // Increased to 4 for deduplication buffer
})

// Example run 2 (different sample):
// "(high-frequency trading OR stock market OR inflation OR Federal Reserve OR macroeconomics) AND news"
```

**Query 2 (Funding/VC direction)** - Sample 5-8 keywords:
```javascript
// Example run 1:
WebSearch_tool({
  query: "(seed funding OR Series A OR venture capital OR unicorn OR cap table) AND news",
  freshness: "day",
  count: 4
})

// Example run 2 (different sample):
// "(private equity OR SPAC OR angel investor OR startup funding OR valuation) AND news"
```

**Query 3 (Crypto/DeFi direction)** - Sample 5-8 keywords:
```javascript
// Example run 1:
WebSearch_tool({
  query: "(DeFi OR bitcoin OR staking OR layer 2 OR smart contract) AND news",
  freshness: "day",
  count: 4
})

// Example run 2 (different sample):
// "(ethereum OR tokenomics OR NFT OR Web3 OR blockchain) AND news"
```

**Benefits**:
- ✅ **Breadth**: 3 groups cover entire category spectrum
- ✅ **Precision**: Each group has only 5-8 related terms (not 50)
- ✅ **Fault tolerance**: One group failing doesn't block others
- ✅ **Long-tail utilization**: Different runs sample different keywords
- ✅ **Deduplication buffer**: count: 4 → after dedup still 6-8 results

**Combine results**: Merge all 3 queries → expect 12 raw results → 6-8 after deduplication

---

### Level 1: Core Hotwords (Fallback if Level 0 < 3 results)

Use the 5 most popular/high-traffic keywords:

```javascript
WebSearch_tool({
  query: "(private equity OR IPO OR crypto OR macroeconomics OR fintech) AND news",
  freshness: "day",
  count: 5  // Increased for deduplication buffer
})
```

**Why these 5**: Highest search volume + broadest coverage
**Why count: 5**: After deduplication, expect 3-4 results

---

### Level 2: Pure Category Name (Fallback if Level 1 < 3 results)

```javascript
WebSearch_tool({
  query: "Finance news OR Crypto market news",
  freshness: "day",
  count: 5
})
```

**Note**: Use OR between multiple category names to cast wider net

---

### Level 3: Expand Time Range (Fallback if Level 2 < 3 results)

Keep Level 2 query, expand time:

```javascript
WebSearch_tool({
  query: "Finance news OR Crypto market news",
  freshness: "week",  // 24h → 7 days
  count: 5
})
```

---

### 📋 Business Direction Clustering (for Level 0 Dynamic Sampling)

**Instead of fixed templates, define 3 business directions for each category, then dynamically sample 5-8 keywords from the full pool:**

**AI/Tech** (3 directions):
1. **Foundation Models** - Sample from: GPT-5, Claude, Gemini, LLM, large language model, GPT-4, ChatGPT, generative AI, AGI, transformers, OpenAI, Anthropic, Google AI, DeepMind, Meta AI
2. **AI Applications** - Sample from: AI agents, autonomous agents, RAG, prompt engineering, fine-tuning, multimodal AI, text-to-image, DALL-E, Midjourney, NLP, computer vision, AI safety, AI alignment
3. **AI Hardware** - Sample from: AI chip, GPU, TPU, NVIDIA, semiconductor, AI infrastructure, edge computing, AI hardware

**Business Strategy** (3 directions):
1. **M&A/Growth** - Sample from: M&A, mergers, acquisitions, Series A, Series B, unicorn, decacorn, late-stage funding, market expansion, strategic alliance
2. **Business Models** - Sample from: SaaS, freemium, subscription model, platform economics, network effects, two-sided marketplace, aggregation theory, pricing strategy, B2B, B2C
3. **Product/Market** - Sample from: product-market fit, PMF, unit economics, CAC, LTV, churn rate, retention, growth strategy, go-to-market, GTM

**Finance/Crypto** (3 directions):
1. **Trading/Markets** - Sample from: algorithmic trading, high-frequency trading, stock market, bond market, equity market, bond yield, forex, treasury, macroeconomics, GDP, recession, inflation, interest rates
2. **Funding/VC** - Sample from: seed funding, Series A, SPAC, venture capital, VC, private equity, PE, angel investor, IPO, direct listing, unicorn, valuation, cap table, startup funding
3. **Crypto/DeFi** - Sample from: DeFi, decentralized finance, bitcoin, BTC, ethereum, ETH, altcoin, blockchain, staking, tokenomics, smart contract, layer 1, layer 2, Web3, NFT, yield farming

**Health/Bio** (3 directions):
1. **Drug Development** - Sample from: clinical trials, phase 1, phase 2, phase 3, FDA approval, EMA approval, drug discovery, drug development, CRISPR, gene editing, gene therapy, orphan drug, rare disease
2. **Digital Health** - Sample from: telemedicine, telehealth, health tech, digital health, wearable, biosensor, CGM, medical AI, radiology AI, remote patient monitoring, point-of-care testing
3. **Pharma/Biotech** - Sample from: pharma, pharmaceutical, biotechnology, biopharma, immunotherapy, CAR-T, cell therapy, precision medicine, personalized medicine, genomics, proteomics

**Energy/Climate** (3 directions):
1. **Renewables** - Sample from: solar, solar energy, photovoltaic, wind, wind energy, offshore wind, renewable energy, clean energy, green energy, nuclear, SMR, fusion energy
2. **Storage/EV** - Sample from: battery, lithium-ion battery, solid-state battery, energy storage, grid-scale storage, EV, electric vehicle, BEV, PHEV, charging infrastructure
3. **Climate Tech** - Sample from: carbon capture, CCS, direct air capture, carbon credit, carbon neutral, net zero, decarbonization, ESG, hydrogen, green hydrogen, climate tech

**Policy/Regulation** (3 directions):
1. **AI Governance** - Sample from: AI regulation, AI governance, AI ethics, AI safety, AI risk, AI alignment, responsible AI, existential risk, AI Act, China regulation
2. **Antitrust/Privacy** - Sample from: antitrust, monopoly, market power, competition law, merger review, GDPR, CCPA, data privacy, privacy law, surveillance, facial recognition
3. **Tech Policy** - Sample from: DSA, DMA, Digital Services Act, Digital Markets Act, Section 230, content moderation, platform liability, tech policy, regulatory compliance, legislation

**Product Design** (3 directions):
1. **UX Research** - Sample from: user research, UX research, usability testing, A/B testing, user testing, user interview, persona, user journey, journey map, qualitative research, quantitative research
2. **Design Systems** - Sample from: design system, component library, design tokens, Figma, Sketch, Adobe XD, Framer, design ops, design workflow, design collaboration, design QA
3. **Accessibility** - Sample from: accessibility, a11y, WCAG, usability, inclusive design, responsive design, mobile-first, onboarding, empty state, error state, micro-interaction

**🔄 Sampling Strategy: Anti-Bias Random (Current Active Policy)**

**Instruction for LLM**:
You MUST use a truly random approach to select 5-8 keywords from each sub-group pool.

**⚠️ CRITICAL ANTI-BIAS RULES**:
1. **Do not just pick the first 5 words in the list.**
2. **Force yourself to select at least 2 keywords from the very end of the list.**
3. **If you run this skill multiple times in one session, you must intentionally choose completely different words than your previous run.**
4. **Do NOT read or write to memory logs for this sampling yet (Stateless execution).**

**Why Anti-Bias**:
- LLMs have "first token bias" → naturally prefer words at the start of a list
- This rule forces coverage of long-tail keywords at the end of the pool
- Maximizes keyword diversity across multiple runs

**Alternative Strategies** (not currently active):
- **Round-robin**: Rotate which keywords get selected each day (requires state persistence)
- **Weighted**: Prefer newer/trending keywords (requires trend tracking)

---

### Quality Control

After each level:
1. **Verify sources**: Bloomberg, FT, Reuters → high priority
2. **Deduplicate**: Same URL/title → keep highest quality source
3. **Minimum threshold**: If total results < 3 after Level 3 → log warning and skip category

---

### Example Execution Flow (Finance/Crypto)

```
Level 0: Grouped Parallel Search (Dynamic Sampling)
├─ Query 1 (Trading/Markets): Sample 6 keywords → 4 raw results
├─ Query 2 (Funding/VC): Sample 5 keywords → 4 raw results
└─ Query 3 (Crypto/DeFi): Sample 7 keywords → 4 raw results
→ Total: 12 raw results → Deduplicate → 8 unique results ✓
→ SUCCESS, skip Level 1-3

---

If Level 0 → 2 results (< 3):
↓
Level 1: Core Hotwords
Query: "(private equity OR IPO OR crypto OR macroeconomics OR fintech) AND news"
→ 4 results ✓ → SUCCESS, skip Level 2-3

---

If Level 1 → 1 result (< 3):
↓
Level 2: Category Name
Query: "Finance news OR Crypto market news"
→ 6 results ✓ → SUCCESS, skip Level 3

---

If Level 2 → 2 results (< 3):
↓
Level 3: Expand Time Range
Query: "Finance news OR Crypto market news" + freshness: "week"
→ 8 results ✓ → SUCCESS
```

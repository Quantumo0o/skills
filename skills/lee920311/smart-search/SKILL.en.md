---
name: smart-search
description: Smart Search - Intelligent search engine switcher. Prioritizes SearX 1.1.0 (free unlimited), auto-fallback to Tavily.
author: Li Yang (@Lee920311)
version: 3.0.0
tags:
  - search
  - searx
  - tavily
  - web-search
  - ai-search
  - openclaw
triggers:
  - "search"
  - "look up"
  - "find"
  - "query"
  - "research"
metadata: {
  "emoji": "🔍",
  "requires": {
    "bins": ["curl", "python3"],
    "env": ["SEARXNG_URL", "TAVILY_API_KEY"]
  },
  "language": ["en", "zh"]
}
---

# Smart Search - Intelligent Search Engine Switcher v3

**Prioritizes SearX 1.1.0 (free unlimited), auto-fallback to Tavily with AI summaries**

## 🌟 Features

- 🆓 **Free First** - 90% searches use SearX 1.1.0 (completely free)
- 🤖 **Smart Switching** - Auto-selects best engine based on query intent
- 🔄 **Auto Fallback** - Seamless fallback to Tavily when SearX unavailable
- 💰 **Cost Optimized** - 90% search cost reduced to ¥0
- 📊 **AI Summaries** - Tavily provides AI-generated summaries for content creation

## 🎯 Decision Logic

### Intelligent Scene Recognition

| Scene Type | Keywords | Engine | Reason |
|------------|----------|--------|--------|
| **AI Content Creation** | write, create, generate, summary, outline | Tavily | AI summaries for creation |
| **Daily Query** | what is, how to, tutorial, guide | SearX | Free unlimited, fast response |
| **News & Trends** | news, latest, trending, today | SearX | Multi-engine aggregation |
| **Deep Research** | research, analyze, study, compare | SearX | Comprehensive results |
| **User Specified** | use tavily, use searx | As User | Respect user choice |

### Priority System

| Priority | Engine | Usage | Coverage |
|----------|--------|-------|----------|
| 1️⃣ | **SearX 1.1.0** | Daily search, news, research | 90% |
| 2️⃣ | **Tavily** | AI content, emergency backup | 10% |

**Fallback Strategy:**
```
SearX 1.1.0 → Tavily (auto fallback)
```

## ⚙️ Configuration

### Required
```bash
# ~/.openclaw/.env

# SearX 1.1.0 (primary engine, must deploy)
SEARXNG_URL=http://localhost:8080
```

### Optional (AI Content Creation)
```bash
# Tavily API Key (recommended, free 1000 queries/month)
TAVILY_API_KEY=your_api_key_here  # Get from https://tavily.com
```

**Configuration Scenarios:**
- ✅ **No Tavily**: Daily search uses SearX (free unlimited), AI content falls back to SearX
- ✅ **With Tavily**: AI content uses Tavily (with AI summaries), daily search uses SearX
- 💡 **Recommended**: Configure both for best experience

**Get Tavily API Key (2 minutes):**
1. Visit https://tavily.com
2. Sign up for free account (1000 queries/month free)
3. Get your API Key
4. Add to `~/.openclaw/.env`

## 🚀 Deployment

### Option A: One-Click Deploy Script (Recommended)
```bash
cd /path/to/smart-search
chmod +x deploy-searx.sh
./deploy-searx.sh
```

### Option B: Docker Command
```bash
docker run -d --name searx \
  -p 8080:8080 \
  -e SEARX_SECRET='your_secret_here' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

### Option C: Docker Compose
```yaml
# docker-compose.yml
version: '3'
services:
  searx:
    image: searx/searx:1.1.0-69-75b859d2
    ports:
      - "8080:8080"
    environment:
      - SEARX_SECRET=your_secret_here
    restart: unless-stopped
```

Run:
```bash
docker compose up -d
```

**Why SearX 1.1.0 (not SearXNG 2026.x)?**
- SearXNG 2026.x has strict bot detection, JSON API returns 403
- SearX 1.1.0 has no bot detection, JSON API works perfectly
- Free unlimited searches, perfect for high-frequency usage

## 📖 Usage Examples

**Daily Search**
```bash
./search.sh "AI news"
```

**Specify Result Count**
```bash
./search.sh "AI tools" 10
```

**Force Use Tavily**
```bash
./search.sh "use tavily search AI writing tools"
```

**Force Use SearX**
```bash
./search.sh "use searx search python tutorial"
```

## 🔧 Tool Invocation

### SearX Search (Priority)
```bash
curl -s "http://localhost:8080/search?q=query&format=json"
```

### Tavily Search (Fallback)
```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"query": "query content", "max_results": 5, "include_answer": true}'
```

## 💰 Cost Comparison

| Engine | Cost | Quota | Usage | Coverage |
|--------|------|-------|-------|----------|
| SearX 1.1.0 | Free | ♾️ Unlimited | Daily search, briefings | 90% |
| Tavily | Free | 1000/month | AI content, backup | 10% |

**Morning Briefing Cost:**
- Daily 1 time × 30 days = 30 times/month
- Using SearX: **¥0 cost** ✅
- Tavily quota reserved: 970 times/month backup

**Monthly Search Budget (600 times/month):**
```
SearX:   540 times × ¥0 = ¥0
Tavily:   60 times × ¥0 = ¥0 (within free quota)
────────────────────────────────
Total:   600 times = ¥0 ✅
```

## 🏗️ Architecture Advantages

1. **Free First** - SearX 1.1.0 handles 90% traffic
2. **Stable Backup** - Tavily ensures service availability
3. **Smart Fallback** - Auto switch, user unaware
4. **Cost Optimized** - 90% search cost reduced to ¥0

## 🐛 Troubleshooting

**SearX Unavailable:**
```bash
# Check container status
docker ps | grep searx

# View logs
docker logs searx --tail 20

# Restart container
docker restart searx
```

**Fallback to Tavily:**
- Auto triggered, no manual intervention needed
- Log shows: `⚠️  SearX unavailable, falling back to Tavily...`

**Tavily API Key Invalid:**
```bash
# Test API
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"query": "test"}'
```

## 📚 Documentation

- `README.md` - Decision reference guide
- `README.searx.md` - SearX deployment guide (Chinese)
- `COMPARISON.md` - Search engine comparison (Chinese)
- `TAVILY_SETUP.md` - Tavily configuration guide (Chinese)
- `PUBLISH.md` - Publishing guide (Chinese)

## 🤝 Contributing

Issues and PRs welcome! This skill is designed for OpenClaw/Clawdbot ecosystem.

## 📄 License

MIT License - Free for personal and commercial use

---

**Last Updated:** 2026-03-26  
**Version:** 3.0.0 (SearX 1.1.0 + Tavily Dual Engine, English Support)  
**Author:** Li Yang (@Lee920311)  
**GitHub:** https://github.com/Lee920311/My-clawhub

---
name: ntriq-code-review-intelligence-mcp
description: "AI-powered code review with security analysis, performance suggestions, and best practice checks. Supports 20+ languages."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [development,code-review,security]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Code Review Intelligence

AI-powered code review with security analysis, performance suggestions, and best practice checks. Supports 20+ languages.

## Usage

### x402 Payment (AI agents)
```bash
curl -X POST https://x402.ntriq.co.kr/code-review \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/doc.png"}'
# Returns 402 → auto-pay USDC → get result
```

### Service Catalog
```bash
curl https://x402.ntriq.co.kr/services
```

## Features
- 100% local AI inference (zero external API calls)
- x402 micropayments (USDC on Base)
- Sub-10 second processing
- JSON structured output

## Powered by
- [ntriq Data Intelligence](https://x402.ntriq.co.kr)
- Qwen2.5-VL (vision) + Qwen2.5 (text) local inference

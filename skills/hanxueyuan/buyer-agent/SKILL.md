---
name: buyer-agent
description: "Personal AI buyer that shops for you"
metadata:
  { "openclaw": { "emoji": "🛒", "version": "0.1.0", "author": "hanxueyuan", "tags": ["shopping","agent-commerce","buyer"] } }
---

# 🛒 Buyer Agent

Personal AI buyer that shops for you

## What It Does

A fully autonomous buying agent. Tell it what you need, set your budget and quality preferences, and it handles the entire purchase flow: research, comparison, selection, and providing the checkout link. Perfect for routine purchases like household supplies.

## Usage

When the user mentions buying, purchasing, shopping, or looking for product deals, this skill activates to help find the best options.

### Example Prompts

- "Find me the best deal on [product]"
- "Compare prices for [product] across platforms"
- "Is there a coupon for [product]?"
- "Help me buy [product] under [budget]"

## Configuration

Set up API credentials in environment variables as needed for each supported platform.

## Architecture

```
User Request → Intent Parser → Product Search API → Result Ranker → Recommendation Display
```

## Roadmap

- v0.1: Basic product search via web search
- v0.2: Platform API integration
- v0.3: Price tracking and alerts
- v1.0: Full autonomous purchasing flow

## Author

Created by hanxueyuan as part of the Agent Commerce initiative.
License: MIT

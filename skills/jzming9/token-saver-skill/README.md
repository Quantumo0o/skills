# TokenSaver for OpenClaw/Copaw

> Smart Token Cost Optimization - Save 50-80% on AI Token Usage

## Overview

TokenSaver automatically reduces AI token consumption while maintaining response quality. It intelligently compresses conversation context, caches similar queries, and optimizes prompts.

## Features

- **Smart Compression** - Hierarchical context compression based on importance scoring (50-70% savings)
- **Semantic Cache** - Multi-level caching for similar queries (30-50% savings)
- **Quality Guard** - Prevents over-compression with auto-rollback
- **Adaptive Mode** - Auto-adjusts based on token pressure
- **Transparent UI** - Real-time savings indicator

## Commands

```bash
/tokens           # Show status and stats
/tokensave        # Aggressive mode (max savings)
/tokenbalance     # Balanced mode (default)
/tokenquality     # Quality priority (min compression)
/tokenreport      # Detailed usage report
/tokencache clear # Clear cache
/tokenoff         # Disable temporarily
```

## Expected Savings

| Scenario | Original | Optimized | Savings |
|----------|----------|-----------|---------|
| Tech discussion (50 rounds) | 12K tokens | 3.5K tokens | 71% |
| Code review | 25K tokens | 5K tokens | 80% |
| General chat | 8K tokens | 2K tokens | 75% |

## Safety Features

- Never compresses code blocks, errors, or user-marked important messages
- Auto-rollback if quality drops > 15%
- One-click restore to uncompressed version
- Snapshots for rollback

## License

MIT

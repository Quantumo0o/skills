---
name: fb-local-lead-sniper
description:
  Facebook local group lead generation skill. Automates joining local groups, warm-up engagement (likes, comments, life posts), posting bait/recommendation requests, analyzing replies to find top-recommended providers, and generating outreach DM scripts.
  Triggers: facebook groups, local leads, group warm-up, bait post, recommendation mining, facebook outreach, lead sniper, local marketing, facebook automation
metadata:
  author: mguozhen
  version: "1.0.0"
  requires: web-access
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
---

# fb-local-lead-sniper

Facebook Local Group Lead Generation — find, engage, and convert local service providers through community recommendations.

## Overview

This skill automates a 5-step lead generation funnel on Facebook local groups:

1. **Join** — Search and join local community groups by city
2. **Engage** — Warm up the account with likes, comments, and life posts
3. **Bait** — Post recommendation requests to surface top providers
4. **Analyze** — Parse replies to rank the most-recommended businesses
5. **Pitch** — Generate personalized DM scripts for outreach

## Prerequisites

- **web-access skill** must be installed and CDP proxy running (`localhost:3456`)
- Chrome must have **remote debugging** enabled (`chrome://inspect/#remote-debugging`)
- Must be logged into Facebook in Chrome

### Quick Check

```bash
curl -s http://localhost:3456/targets | head -1
```

If this returns a JSON array, you're ready. If not, run:
```bash
CLAUDE_SKILL_DIR=~/.claude/skills/web-access node ~/.claude/skills/web-access/scripts/check-deps.mjs
```

## Usage

All commands use the main entry point:

```bash
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" <action> [options]
```

### Actions

| Action | Description | Key Options |
|--------|-------------|-------------|
| `join` | Join local Facebook groups | `--city`, `--count`, `--query` |
| `engage` | Like + comment in joined groups | `--likes`, `--comments` |
| `post` | Post a life update on profile | `--text` (or auto-generate) |
| `bait` | Post a recommendation request in a group | `--group`, `--trade`, `--template` |
| `analyze` | Analyze replies to find top providers | `--url` (post URL) |
| `warm` | Full warm-up cycle (join + engage + post) | `--city`, `--intensity` |
| `status` | Check account status and post replies | (none) |

### Examples

```bash
# Join 5 Austin groups
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" join --city Austin --count 5

# Full warm-up: 20 likes, 8 comments, 5 groups, 1 life post
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" warm --city Austin --intensity double

# Post a bait in a group asking for plumber recommendations
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" bait --group "South Austin Neighbors" --trade plumber --template complaint

# Analyze replies on a bait post
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" analyze --url "https://www.facebook.com/groups/xxx/posts/yyy"

# Check what's happening — pending posts, replies, account health
bash "$CLAUDE_SKILL_DIR/scripts/fb-ops.sh" status
```

## Strategy Guide

### Account Warm-up (Days 1-7)

New or dormant accounts need warm-up before posting bait. The algorithm:

| Day | Likes | Comments | Groups Joined | Life Posts |
|-----|-------|----------|---------------|------------|
| 1-2 | 10 | 4 | 5 | 1 |
| 3-4 | 15 | 6 | 5 | 1 |
| 5-7 | 20 | 8 | 5 | 1 |

Run `warm` action 2-4 times per day with random intervals. Avoid patterns.

### Rate Limit Awareness

- **Group joins**: Max 5 per batch, 30-60s between each. If rate-limited, stop and wait 24h.
- **Comments**: 8-12 per session, 8-15s between each. Vary the text.
- **Posts**: Max 2-3 bait posts per day across different groups.
- **Session length**: Keep each session under 15 minutes.

### Bait Post Templates

Five proven templates available via `--template`:

| Template | Style | Best For |
|----------|-------|----------|
| `urgent` | "Emergency! Need [trade] ASAP" | High urgency, fast replies |
| `research` | "Doing research, who's the best..." | Neutral, many recommendations |
| `newcomer` | "Just moved to [city], need..." | Sympathetic, welcoming replies |
| `complaint` | "Had terrible experience, need someone better" | Emotional, specific recommendations |
| `poll` | "Who's your go-to [trade]?" | Engagement-style, many tags |

### Analyzing Replies

The `analyze` action parses comments for:
- **@mentions** and tagged business pages
- **"I recommend X"** / **"Call X"** / **"Use X"** patterns
- **Phone numbers** and business names (Title Case detection)
- **Frequency ranking** — most-mentioned = highest priority lead

### Outreach DM Templates

After identifying top providers, generate personalized DMs:
- **Warm intro**: Reference the group + original post
- **Value prop**: Mention their frequent recommendations
- **CTA**: Offer free trial / consultation
- **Follow-up**: 3-day and 7-day scripts

## Architecture

```
fb-local-lead-sniper/
├── SKILL.md              # This file — skill definition
├── README.md             # User documentation
├── scripts/
│   ├── fb-ops.sh         # Main entry point + CLI parser
│   ├── cdp-helpers.sh    # CDP proxy utility functions
│   ├── join.sh           # Group joining logic
│   ├── engage.sh         # Likes + comments
│   ├── post.sh           # Life posts + bait posts
│   └── analyze.sh        # Reply analysis
├── templates/
│   ├── bait-posts.json   # Bait post templates by trade
│   ├── comments.json     # Engagement comment pool
│   ├── life-posts.json   # Life update post pool
│   └── dm-scripts.json   # Outreach DM templates
└── tests/
    └── test_basic.sh     # Unit tests
```

## Important Notes

- This skill operates on the user's real Chrome browser via CDP. All actions are visible to Facebook.
- Facebook actively detects automation. Built-in delays and randomization reduce risk but cannot eliminate it.
- Always warm up accounts before posting bait. Cold accounts posting requests get flagged.
- Respect group rules — some groups prohibit self-promotion or solicitation.
- The skill creates and closes its own browser tabs. It does not touch existing user tabs.

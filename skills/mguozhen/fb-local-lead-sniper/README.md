# fb-local-lead-sniper

Facebook Local Group Lead Generation — automated community engagement and recommendation mining.

## What it does

Automates a 5-step lead generation funnel through Facebook local groups:

1. **Join** — Search and join community groups by city
2. **Engage** — Warm up with likes, comments, and life posts
3. **Bait** — Post recommendation requests to surface top providers
4. **Analyze** — Parse replies to rank most-recommended businesses
5. **Pitch** — Generate personalized outreach DM scripts

## How it works

Uses [web-access](https://github.com/eze-is/web-access) skill's CDP (Chrome DevTools Protocol) proxy to control your real Chrome browser. No separate browser instance, no cookie extraction — operates directly in your logged-in Chrome session.

## Requirements

- [Claude Code](https://claude.ai/claude-code) with skills support
- [web-access](https://github.com/eze-is/web-access) skill installed
- Chrome with remote debugging enabled (`chrome://inspect/#remote-debugging`)
- Logged into Facebook in Chrome

## Install

```bash
# Install via clawhub
clawhub install mguozhen/fb-local-lead-sniper

# Or manually
git clone https://github.com/mguozhen/fb-local-lead-sniper.git ~/.claude/skills/fb-local-lead-sniper
```

## Quick Start

```bash
# Join 5 local groups
bash scripts/fb-ops.sh join --city Austin --count 5

# Full warm-up cycle (likes + comments + groups + life post)
bash scripts/fb-ops.sh warm --city Austin

# Double intensity warm-up
bash scripts/fb-ops.sh warm --city Austin --intensity double

# Post bait in a group
bash scripts/fb-ops.sh bait --group "https://facebook.com/groups/xxx" --trade plumber

# Analyze replies
bash scripts/fb-ops.sh analyze --url "https://facebook.com/groups/xxx/posts/yyy"
```

## Supported Trades

plumber, electrician, hvac, roofer, handyman, landscaper, cleaner — plus a `general` template that works for any trade.

## Bait Templates

| Template | Style | Use Case |
|----------|-------|----------|
| `urgent` | "Emergency! Need help ASAP" | Fast replies |
| `research` | "Who's the best..." | Many recommendations |
| `newcomer` | "Just moved, need..." | Sympathetic replies |
| `complaint` | "Had terrible experience..." | Specific recommendations |
| `poll` | "Who's your go-to?" | High engagement |

## Rate Limit Safety

Built-in protections:
- 30-60s delays between group joins
- 8-15s delays between comments
- Auto-detection of Facebook rate limiting
- Randomized delays to avoid patterns
- Session length under 15 minutes

## License

MIT

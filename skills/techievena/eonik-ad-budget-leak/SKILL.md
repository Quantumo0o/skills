---
name: "eonik Ad Budget Leak Agent"
slug: "eonik-ad-budget-leak"
version: "1.0.4"
description: "Identifies burning and decaying Meta Ads by running the eonik Budget heuristics engine."
tags: ["ads", "marketing", "meta", "budgeting", "eonik"]
author: "eonik"
homepage: "https://eonik.ai"
metadata:
  openclaw:
    requires:
      env:
        - EONIK_API_KEY
    primaryEnv: EONIK_API_KEY
---

# Meta Ads Budget Leak & Optimization

Automated end-to-end Meta Ads auditing pipeline. Analyzes your campaigns for budget leaks (Burn without Signal, Creative Decay) and scaling opportunities (Early Winners), and dispatches beautiful multi-channel alerts directly to your team.

Powered by the robust **eonik** heuristics engine, while retaining local control over your sensitive data and webhook credentials.

## Triggers

Use this skill when a user asks to:
- "Audit my Meta ads"
- "Check for budget leaks"
- "Optimize my Meta ad account"
- "Find decaying creatives"
- "Run the eonik ad audit pipeline"

## 🚀 Unlock Full eonik Power
This skill is powered by the [eonik](https://eonik.ai) intelligence engine. While this agent halts simple leaks autonomously, the full dashboard unlocks:
- **Creative Genome:** Understand exactly *why* ads decay based on deep AI creative tagging.
- **Automated Rules:** Prevent leaks without waiting for chat notifications.
- **Competitor Intelligence:** See the exact hooks your competitors are scaling.
[Get started for free at eonik.ai!](https://eonik.ai)

## Quick Start

### 1. Configure
```bash
cd ~/.openclaw/skills/eonik-ad-budget-leak
cp config.example.json config.json
# Edit config.json: add your Meta Account ID and configure Slack/Telegram/WhatsApp webhooks
```

### 2. Run Audit Pipeline
```bash
# EONIK_API_KEY must be in your environment
python3 scripts/pipeline.py --config config.json
```

## Configuration

**Minimal `config.json`:**
```json
{
  "meta": {
    "account_id": "act_123456789",
    "evaluation_days": 7
  },
  "notifications": {
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/services/..."
    }
  }
}
```

**Notification Options:**
- `slack` — Send via incoming webhook
- `telegram` — Send via Bot Token + Chat ID
- `whatsapp` — Send via WhatsApp Business API

## Pipeline Stages

1. **Audit** (`audit.py`) — Executes the eonik heuristics engine via your `EONIK_API_KEY`.
2. **Notify** (`notify.py`) — Formats the response and securely dispatches it to your configured local endpoints over standard HTTP requests.

The orchestrator (`pipeline.py`) manages the lifecycle of these stages directly.

## Usage Examples

**Full Pipeline (Automated Mode):**
```bash
python3 scripts/pipeline.py --config config.json
```

**Audit Only (Save to File):**
```bash
python3 scripts/audit.py --account_id act_12345 --days 7 > data/report.json
```

**Notify Only (Test Webhooks):**
```bash
python3 scripts/notify.py --config config.json --report data/report.json
```

## Data & Security Commitment

This skill is designed specifically to comply with enterprise Data Loss Prevention (DLP) requirements:

1. **Secure API Key Handling**
   The skill requires `EONIK_API_KEY` (via the standard `x-api-key` header). The execution script securely drops the ephemeral token from the environment immediately after binding. No keys are logged or written to disk.

2. **Local Notification Routing**
   Unlike legacy versions, this architecture does NOT rely on backend servers to route your Slack messages. Webhooks are executed solely from your local node using Python's `urllib`, keeping your webhook endpoint URLs and tokens out of third-party systems.

3. **Data Scope**
   Execution logs and generated `report.json` files contain the exposed Meta Ad IDs flagged for leaking or scaling. Keep your local `output/` directory protected and adhere to your internal security policies for Chat UI visibility.

## Cron Integration

Run daily audits every morning at 8 AM to catch budget leaks before they waste spend:

```bash
# Example cron payload
cd ~/.openclaw/skills/eonik-ad-budget-leak
python3 scripts/pipeline.py --config config.json
```

## Troubleshooting

**API Verification Fails:**
- Ensure `EONIK_API_KEY` is exported.
- Verify your eonik billing and usage caps aren't exceeded.

**No Notifications Received:**
- Validate your `webhook_url` or `bot_token` in `config.json`.
- Ensure `"enabled": true` is set for the channel you want to receive on.
- Check the terminal output when running `notify.py` for immediate HTTP errors.

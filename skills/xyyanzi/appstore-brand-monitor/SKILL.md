---
name: appstore-brand-monitor
description: App Store brand fraud monitoring. Scans App Store across multiple regions for counterfeit apps impersonating Atome. Uses AI name/icon similarity detection (agent-driven). Sends Lark alerts with screenshots for high-risk apps found.
labels: [security, devops]
---

# App Store Brand Monitor

Scans App Store for brand impersonation. Agent handles all AI analysis, screenshots, and orchestration. Scripts handle data fetching and Lark sending only.

## Directory Structure

```
skills/appstore-brand-monitor/
├── SKILL.md              # This file - agent execution instructions
├── search.js             # iTunes API query + whitelist filter → JSON output
├── lark-alert.js         # Lark card sender + alerted.json deduplication updater
├── setup.mjs             # One-time config wizard (generates .env file)
├── official_icon.png     # Official Atome app icon for visual similarity check
├── .env                  # Runtime config (Lark credentials, alert receiver ID)
├── .env.example          # Config template
├── alerted.json          # Auto-managed deduplication records (created on first run)
└── screenshots/          # Per-country screenshot storage
    ├── ph/
    ├── sg/
    ├── my/
    ├── id/
    └── th/
```

## Dependencies

Scripts depend on `dotenv`, `yargs` — all bundled with OpenClaw itself. No separate `npm install` needed.

Derive OpenClaw's node_modules path from its binary, then pass as `NODE_PATH`:

```bash
# One-liner to set OC_MODULES (works regardless of nvm version or install path)
export OC_MODULES=$(dirname $(dirname $(which openclaw)))/lib/node_modules/openclaw/node_modules

# Run any script with it:
NODE_PATH=$OC_MODULES node search.js --country ph --keyword Atome
NODE_PATH=$OC_MODULES node lark-alert.js --input /tmp/report.json
```

Store `$OC_MODULES` at the start of each agent session for reuse.
```

## Prerequisites

Run once to generate `.env` file:
```bash
cd skills/appstore-brand-monitor && node setup.mjs
```

The wizard automatically reads Lark App ID/Secret from OpenClaw config, only asks for alert receiver ID. **No API keys are read or stored outside of .env.**

## Trigger

Trigger this skill when user says:
- "scan App Store" / "check for fake apps" / "brand monitoring"
- "扫描 App Store" / "品牌仿冒检测" / "假冒应用"

## Full Workflow (Agent-Driven)

### Step 1 — Search & Filter (Script)

```bash
node search.js --country <ph|sg|my|id|th> --keyword Atome
```

Output JSON to stdout:
```json
{
  "country": "ph",
  "keyword": "Atome",
  "total": 39,
  "whitelisted": 1,
  "alreadyAlerted": 2,
  "candidates": [
    {
      "appId": "123456",
      "title": "Fake Atome Loans",
      "developer": "Sketchy Dev",
      "url": "https://apps.apple.com/ph/app/...",
      "icon": "https://is1-ssl.mzstatic.com/...",
      "score": "4.1",
      "reviews": 50,
      "description": "Get loans with Atome..."
    }
  ]
}
```

### Step 2 — Name Similarity Check (Agent, AI)

For each candidate:
- **Rule**: Only flag apps where name **literally contains "atome"** (case-insensitive, exact substring match)
- **Exclude**: "atom", "atomy", or other similar sounding names (score < 80)
- Also check if app description contains the exact string "atome"

Mark each candidate:
```json
{
  "nameScore": 90,
  "nameHit": true,
  "nameRule": "Name contains exact substring \"Atome\" (90pt)",
  "descHit": true,
  "descRule": "Description contains \"atome\" (80pt)"
}
```

Only proceed to icon check for apps where `nameHit == true OR descHit == true`.

### Step 3 — Icon Similarity Check (Agent, Built-in Multimodal)

For apps passing Step 2:
- Reference: local file `skills/appstore-brand-monitor/official_icon.png`
- Candidate: app's `icon` URL from search result

Download the candidate icon to a temp file first:
```bash
curl -s "<icon_url>" -o /tmp/candidate_icon_<appId>.jpg
```

Then use the `read` tool to load both images (agent's built-in multimodal, no `image` tool needed):
- Read `skills/appstore-brand-monitor/official_icon.png`
- Read `/tmp/candidate_icon_<appId>.jpg`

Agent prompt:
> "Compare the two icons I just read. The first is the official Atome app icon, the second is the candidate app icon. Output only a similarity score (0-100) followed by a 1-sentence reason. Format: score|reason"

Mark:
```json
{
  "iconSimilarity": 88,
  "iconHit": true,
  "iconRule": "Icon similarity to official Atome: 88% (≥80% threshold, 80pt)"
}
```

Threshold: **80%** — apps below threshold are not flagged.
Uses `read` tool to load both images — works with any multimodal main model. Do NOT use the `image` tool (not available in this environment).

### Step 4 — Determine High-Risk Apps

An app is high-risk if it hits **at least one rule**:
- `nameHit == true`
- `descHit == true`
- `iconHit == true`

Total score = sum of points for all hit rules. Sort high-risk apps by total score descending.

### Step 5 — Screenshot High-Risk Apps (Agent)

Use the built-in `browser` tool. Always close the tab immediately after screenshot. Then crop to top portion only.

```
# 1. Open page
browser(action=open, url=<app.url>)  → get targetId

# 2. Wait for page load
browser(action=act, request={kind: "wait", loadState: "networkidle", timeoutMs: 5000}, targetId=<targetId>)

# 3. Screenshot (captures full page — we crop after)
browser(action=screenshot, targetId=<targetId>)  → get <imgPath>

# 4. Close tab immediately
browser(action=close, targetId=<targetId>)

# 5. Crop to top 700px (app icon + title + developer + description)
exec: ffmpeg -y -i <imgPath> -vf "crop=iw:700:0:0" <croppedPath>
```

Save `<croppedPath>` as `app.screenshotPath`.

**Note**: `browser` tool always captures the full page. Use `ffmpeg` to crop from the top-left corner (0,0), keeping full width and 700px height. This covers the app header section without showing the full page. Do NOT use `sips -c` — it crops from center, not top.

### Step 6 — Send Lark Alert (Script)

Build report JSON and pass to `lark-alert.js`:
```bash
node lark-alert.js --input /tmp/appstore-report-<country>.json
```

Report format:
```json
{
  "country": "ph",
  "keyword": "Atome",
  "scanTime": "<ISO timestamp>",
  "total": 39,
  "candidates": [...],
  "highRisk": [
    {
      "appId": "123456",
      "title": "Fake Atome Loans",
      "developer": "Sketchy Dev",
      "url": "https://...",
      "score": "4.1",
      "reviews": 50,
      "hitRules": ["Name contains exact substring \"Atome\" (90pt)", "Description contains \"atome\" (80pt)"],
      "totalScore": 170,
      "screenshotPath": "/absolute/path/to/screenshot.png"
    }
  ]
}
```

`lark-alert.js` will:
1. Upload screenshots to Lark
2. Send interactive card alert
3. Update `alerted.json` with newly alerted app IDs

### Step 7 — Summary

Report to user (Chinese for local users):
> ✅ 扫描完成
> - 地区：PH
> - 扫描应用数：39
> - 白名单跳过：1
> - 已告警跳过：2
> - 新增高风险应用：1个
>   - Atome Loan: online lending app — 风险评分170分
> - Lark 告警已发送

---

## Deduplication — `alerted.json`

Tracks apps that have already been alerted:
```json
{
  "6754756577": { "title": "Atome Finance", "country": "id", "alertedAt": "2026-03-26T08:23:00Z" }
}
```

- `search.js` skips apps in this file by default (pass `--skip-alerted false` to override)
- `lark-alert.js` adds new entries after successful alert
- To reset: delete `alerted.json` or remove specific keys manually

---

## Multi-Country Scan

To scan all regions:
```bash
for country in ph sg my id th; do
  node search.js --country $country --keyword Atome > /tmp/candidates-$country.json
  # Run agent workflow Steps 2-6 for each country
done
```

---

## Official App Whitelist

These are Atome's own official apps, always excluded:

| App ID     | Country |
|------------|---------|
| 1577294865 | PH      |
| 1491428868 | SG      |
| 1533642823 | MY      |
| 1560108683 | ID      |
| 1563893540 | TH      |

---

## Notes

- All scripts are in English, only user-facing alerts and summary use Chinese
- Dependencies are minimal: only `dotenv` and `yargs` (total 1.2MB)
- No external API calls except iTunes search and Lark API
- No internal OpenClaw config files are accessed by scripts (only `setup.mjs` reads Lark config once during initialization)

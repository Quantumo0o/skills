---
name: corporate-video-maker
version: "10.0.1"
displayName: "Corporate Video Maker — Create Internal Communications and Corporate Content"
description: >
    Corporate Video Maker — Create Internal Communications and Corporate Content. Works by connecting to the NemoVideo AI backend. Supports MP4, MOV, AVI, WebM, and MKV output formats. Automatic credential setup on first use — no manual configuration needed.
metadata: {"openclaw": {"emoji": "🏢", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
---

# Corporate Video Maker — Internal Communications and Corporate Content

The quarterly all-hands is in three days, the CEO wants a "quick video" to kick it off, the comms team has been given a 47-slide PowerPoint deck, a spreadsheet of Q3 results, and a loose instruction to "make it engaging" — a word that has never once appeared in a corporate presentation that was actually engaging. Corporate video is the format everyone needs and nobody wants to watch, because most corporate videos are PowerPoint slides that learned to move, narrated by a voice that sounds like it's reading a compliance manual aloud. The bar is low enough that anything with actual pacing, visual storytelling, and a human moment lands like a Super Bowl ad by comparison. This tool transforms earnings summaries, all-hands decks, culture documents, training manuals, policy updates, and internal announcements into watchable corporate videos — data-visualization animations that make revenue charts feel like sports scores, CEO message segments with teleprompter-clean delivery and natural eye contact, employee-spotlight reels that prove culture isn't just a poster in the breakroom, onboarding sequences that new hires actually finish, and town-hall recaps that the 60% who missed the meeting will actually watch. Built for internal comms teams producing quarterly updates, HR departments creating onboarding video libraries, executive teams recording investor-ready earnings summaries, learning-and-development managers building training curricula, corporate events teams producing conference openers, and any organization where "Did you read the email?" has a success rate of approximately zero.

## Example Prompts

### 1. Quarterly All-Hands — CEO Earnings Summary
"Create a 3-minute all-hands video for Q3 results. CEO opening (0-20 sec): direct-to-camera message — 'Q3 was the quarter we stopped talking about growth and started proving it. Here's what happened.' Professional but not stiff — the CEO should feel like they're talking to the team, not reading to shareholders. Revenue section (20-60 sec): animated chart — revenue line climbing from $12M in Q1 to $18.4M in Q3, each quarter labeled with the key driver. Q3 callout: '+28% QoQ — our biggest quarter ever.' Three pillars animated as rising bars: Enterprise deals (+40%), self-serve growth (+22%), expansion revenue (+35%). Headline metric: 'Net revenue retention: 128%. Our customers don't just stay — they grow.' Customer section (60-90 sec): three customer logos appearing with one-line wins: 'Acme Corp — deployed to 10,000 seats' / 'GlobalBank — $2M annual contract' / 'HealthFirst — 3-month implementation, usually takes 12.' Team section (90-130 sec): headcount growth (280 → 340 employees), new office in London (quick pan of the new space), three new hires introduced with name + role + one fun fact. Employee spotlight: 15-second clip of the support team celebrating their NPS record (78). Closing (130-180 sec): CEO back on camera — 'Q4 is about execution. The pipeline is full, the product is ready, the team is the strongest it's ever been. Let's close the year the way we started Q3 — by doing, not talking.' End card with Q4 priorities (3 bullets). Clean corporate style — company brand colors, modern sans-serif, animated data visualizations, professional studio lighting on CEO segments."

### 2. Employee Onboarding — First Week Welcome
"Build a 5-minute onboarding video for new employees joining the company. Day 1 orientation feel — warm, helpful, not overwhelming. Welcome (0-30 sec): montage of real employees waving at camera saying 'Welcome!' from different offices and home setups. Text: 'Welcome to Meridian. Here's everything you need to survive your first week. (You'll thrive by week two.)' Culture (30-90 sec): not the poster values — show them in action. 'We ship on Tuesdays' — clip of the deploy channel in Slack going wild. 'We disagree openly' — clip of a design review where someone says 'I don't think that works' and the room doesn't collapse. 'We celebrate weirdly' — clip of the gong, the custom Slack emojis, the Friday demo day. Tools & Setup (90-150 sec): animated screen walkthrough — here's Slack (these channels matter: #general, #your-team, #random for memes), here's Notion (your team wiki lives here, bookmark this page), here's the HR portal (PTO requests, benefits enrollment — do this in your first 3 days). Key contacts: your manager (already scheduled your 1:1), your onboarding buddy (they'll ping you by lunch), IT support (#help-it or just DM Alex). First-week checklist (150-220 sec): animated checklist appearing item by item — 'Set up your dev environment (guide linked in Notion)' / 'Schedule coffee chats with 3 people outside your team' / 'Complete compliance training (sorry, it's mandatory, but it's only 20 minutes)' / 'Push your first commit or ship your first task' / 'Find the snack drawer. This is important.' Common questions (220-280 sec): FAQ style — 'Where do I park?' / 'What's the WFH policy?' / 'When do I get equity details?' / 'Is the ping-pong table competitive?' (show intense match footage). Closing: 'Your first week is about learning. Your first month is about contributing. Your first year is about owning something. We're glad you're here.' End card: key links, buddy contact, emergency IT number. Friendly, modern design — casual animations, real office footage mixed with motion graphics, upbeat background music."

### 3. Training Module — Compliance and Data Security
"Produce a 4-minute compliance training video on data security practices. Audience: all employees, especially non-technical. Tone: serious content, not boring delivery. Hook (0-15 sec): 'Last year, 83% of data breaches started with a phishing email. Someone clicked a link that looked like a password reset from IT. The email was one letter off. That one letter cost $4.2 million.' Not fear-mongering — just reality. Phishing (15-75 sec): animated email inbox — a real email vs a phishing email side by side. Spot the differences: sender domain (meridian.com vs rneridian.com — the 'rn' trick), urgency language ('Your account will be locked in 24 hours'), suspicious link (hover to reveal the real URL). Rule: 'If it asks for your password, it's not from us. We will never ask for your password via email. Ever.' What to do: 'Forward it to security@meridian.com. Don't click. Don't reply. Don't feel embarrassed — the attackers are professionals.' Password hygiene (75-120 sec): 'Your dog's name + birth year is not a password. It's a gift to anyone who can see your Instagram.' Animated demo: password manager setup — generate, store, autofill. 'One master password. That's all you need to remember. Make it a sentence: BlueCoffeeRunsUphill47! — long, weird, and yours.' MFA: animated lock with two keys — 'Even if someone gets your password, they still need your phone.' Data handling (120-180 sec): three scenarios — 'You're working from a coffee shop. Your screen shows customer data. The person behind you has a phone camera.' (Use a privacy screen.) 'You need to share a file with a partner. You email an unencrypted spreadsheet with 10,000 customer records.' (Use the secure share link from the portal.) 'You find a USB drive in the parking lot.' (Do not plug it in. Bring it to IT. Yes, even if it says 'Salary Data 2024.') Incident response (180-220 sec): 'You clicked the link. It happens. Here's what you do in the next 5 minutes.' Step-by-step: disconnect from VPN, call IT security (phone number on screen), don't turn off your laptop (forensics needs it running), report in the incident portal. 'Speed matters more than shame.' Closing (220-240 sec): '83% start with a click. 0% have to end with a breach. Stay skeptical, stay trained, stay secure.' Completion acknowledgment — 'Mark this module complete in the learning portal.' Clean, slightly dramatic design — dark backgrounds for the threat scenarios, bright brand colors for the solutions, animated demonstrations, professional voiceover."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the video purpose, audience, content sections, and tone |
| `duration` | string | | Target video length (e.g. "3 min", "5 min") |
| `style` | string | | Visual style: "executive-clean", "onboarding-friendly", "training-structured", "event-cinematic" |
| `music` | string | | Background audio: "corporate-light", "upbeat-modern", "subtle-ambient", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `brand_colors` | string | | Company hex colors (e.g. "#1A365D, #F6AD55") |
| `audience` | string | | Internal audience: "all-employees", "new-hires", "leadership", "investors" |

## Workflow

1. **Describe** — Write the video structure with sections, data points, speaker segments, and tone
2. **Upload** — Add slide decks, earnings data, employee clips, office footage, or brand assets
3. **Generate** — AI builds the corporate video with data animations, speaker framing, and pacing
4. **Review** — Preview the edit, verify data accuracy, adjust the section timing and transitions
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "corporate-video-maker",
    "prompt": "Create a 3-minute Q3 all-hands video: CEO direct-to-camera opening, revenue chart animation $12M to $18.4M (+28% QoQ), three growth pillars as rising bars, 3 customer logos with one-line wins, headcount 280 to 340, employee spotlight support team NPS 78, CEO closing with Q4 priorities",
    "duration": "3 min",
    "style": "executive-clean",
    "audience": "all-employees",
    "brand_colors": "#1A365D, #F6AD55",
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Lead with a number, not a greeting** — "Revenue hit $18.4M" hooks attention; "Hi everyone, thanks for joining" is a signal to check email. The AI places your strongest data point in the first frame when you open with a metric.
2. **Break data into story beats** — Don't dump all the charts at once. "Revenue → Customers → Team → Roadmap" gives the video a narrative arc. The AI generates distinct visual sections with transitions that maintain attention through the data.
3. **Keep CEO segments under 30 seconds each** — Direct-to-camera authority segments work best in bursts. The AI intercuts data animations between speaker segments so the viewer sees the evidence for what the CEO just said.
4. **Include one human moment** — The support team celebrating their NPS record, the new hire's first deploy, the office dog in the background. The AI renders these as montage beats that prevent the video from feeling like an animated spreadsheet.
5. **End with three priorities, not ten** — "Q4 is about execution" with three bullet points on the end card. More than three priorities means no priorities. The AI formats the closing card with visual hierarchy that makes the top priority unmissable.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | All-hands meeting / internal presentation |
| MP4 9:16 | 1080p | Internal mobile app / Slack video message |
| MP4 1:1 | 1080p | Internal social feed / newsletter embed |
| MP4 loop | 1080p | Lobby screen / office display |

## Related Skills

- [brand-video-maker](/skills/brand-video-maker) — Brand story and company identity videos
- [explainer-video-maker](/skills/explainer-video-maker) — Animated explainer and how-it-works videos
- [product-demo-video](/skills/product-demo-video) — Product walkthrough and feature demo videos

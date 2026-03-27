---
name: corporate-video-maker
version: "1.0.0"
displayName: "Corporate Video Maker — Create Professional Business and Company Videos"
description: >
  Produce professional corporate videos for brand storytelling, investor communication, and internal engagement. NemoVideo handles company overviews, culture showcases, annual reports, and executive messages — turning raw footage and brand assets into polished business videos without agency timelines or agency budgets.
metadata: {"openclaw": {"emoji": "🏛️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Corporate Video Maker — Professional Business and Company Videos

The corporate video occupies an awkward position in the content ecosystem: it must be professional enough to represent a billion-dollar brand on an investor-relations page, yet engaging enough that an employee actually watches it during onboarding instead of letting it autoplay on mute while they fill out tax forms. It must communicate authenticity while being carefully scripted, demonstrate culture while being approved by legal, and inspire emotion while being signed off by a committee of 11 stakeholders who each added their department's talking points until the original 90-second concept became a 7-minute hostage situation where every division gets 45 seconds of screen time regardless of whether they have anything interesting to show. NemoVideo solves this by imposing structure: it takes raw assets — executive recordings, office footage, event clips, product shots, customer quotes — and assembles them into corporate videos that follow proven narrative frameworks rather than org-chart politics. The CEO's message is trimmed from 8 minutes to 90 seconds because the data is unambiguous: viewer drop-off at 2 minutes is 60%. The culture video shows real employees in real moments because stock-footage culture videos communicate the opposite of culture. The investor update leads with the numbers because that's what investors came for. The tool doesn't make corporate video exciting — it makes corporate video watchable, which in this category is the same thing.

## Use Cases

1. **Company Overview / About Us** — Produce a 2-minute video for the corporate website's About page. Structure: mission statement (10 sec, text animation over hero footage), founding story (20 sec, founder on camera or archival photos), what the company does today (30 sec, product/service montage with narration), scale and reach (15 sec, animated data — employees, offices, customers, revenue), customer impact (25 sec, one client quote on camera), and forward vision (20 sec, CEO on camera). Exported at 4K for website hero embed and 1080p 1:1 for LinkedIn.
2. **Annual Report Video Summary** — Convert the annual report's key findings into a 3-minute visual summary for shareholders. Animated financial charts (revenue growth, margin trends, segment breakdown), operational highlights (new markets, product launches, headcount growth), ESG metrics (carbon reduction, diversity stats), and forward guidance. Designed to embed in the digital annual report and play at the shareholder meeting.
3. **Employee Culture Showcase** — Create a 90-second video for the careers page. No scripts, no staging: real employees answering one question on camera — "What's the best thing about working here?" NemoVideo selects the 6 most compelling responses (15 sec each), intercuts with candid office/remote-work footage, adds a branded intro/outro and the careers URL. The video should feel like a documentary clip, not a commercial.
4. **CEO Quarterly Update** — The CEO recorded a 12-minute all-hands address. NemoVideo trims it to 4 minutes: the three key messages (financial results, strategic priorities, team recognition), with data overlays appearing when the CEO references numbers, and chapter markers so employees can jump to the section relevant to their division.
5. **Office Tour / Facility Showcase** — Produce a 2-minute walkthrough of a new office, factory, or campus. Drone or gimbal footage with location labels, department overlays as the camera moves through spaces, and an employee guide appearing on camera at 3 key stops to explain what happens in each area. Used for recruiting, client visits, and internal orientation.

## How It Works

### Step 1 — Gather Assets
Collect raw footage (executive recordings, office b-roll, event clips, product shots), brand kit (logo, color hex codes, fonts), data for visualization (financials, headcount, milestones), and any existing scripts or talking points.

### Step 2 — Define Video Type and Audience
Specify the corporate video category, primary audience (investors, employees, public, recruits), distribution channel (website, LinkedIn, all-hands meeting, shareholder event), and any compliance requirements (legal review, brand guidelines, regulatory disclosures).

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "corporate-video-maker",
    "prompt": "Create a 2-minute company overview video. Structure: (1) Mission — animated text over aerial office footage, 10 sec. (2) Founding story — 2015, two founders in a garage, archival photos dissolving into present-day campus, 20 sec. (3) What we do today — product montage showing the platform dashboard, mobile app, and API integrations with narration overlay, 30 sec. (4) Scale — animated counters: 1200 employees, 8 offices, 15000 customers, $280M ARR, 15 sec. (5) Customer impact — client VP on camera: how the platform reduced their ops costs 40%, 25 sec. (6) Vision — CEO on camera: where the company is headed in the next 3 years, 20 sec. Branded intro 3 sec with logo animation, outro 5 sec with tagline and website URL. Corporate color palette: #1A365D, #2B6CB0, #E2E8F0.",
    "duration": "2 min",
    "style": "company-overview",
    "audience": "public",
    "brand_kit": true,
    "data_animation": true,
    "music": "corporate-inspiring",
    "format": "16:9"
  }'
```

### Step 4 — Stakeholder Review and Distribution
Route the draft through the approval chain (marketing → legal → executive). NemoVideo supports timestamped comments for revision rounds. Export final versions for each distribution channel: 4K for website embed, 1080p 16:9 for presentations, 1:1 for LinkedIn/Twitter.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the corporate video type, structure, and key messages |
| `duration` | string | | Target length: "90 sec", "2 min", "3 min", "5 min" |
| `style` | string | | "company-overview", "annual-report", "culture-showcase", "ceo-message", "office-tour", "milestone-celebration" |
| `audience` | string | | "public", "investors", "employees", "recruits" |
| `brand_kit` | boolean | | Apply brand colors, logo, and font from uploaded kit (default: true) |
| `data_animation` | boolean | | Animate financial/operational data as counters, charts, or graphs (default: true) |
| `music` | string | | "corporate-inspiring", "warm-authentic", "minimal-elegant", "energetic-modern" |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "cvm-20260328-001",
  "status": "completed",
  "title": "Nextera Solutions — Company Overview 2026",
  "duration_seconds": 128,
  "format": "mp4",
  "resolution": "3840x2160",
  "file_size_mb": 186.4,
  "output_files": {
    "4k_hero": "nextera-overview-4k.mp4",
    "1080p_presentation": "nextera-overview-1080p.mp4",
    "1080p_square": "nextera-overview-1x1.mp4"
  },
  "sections": [
    {"label": "Mission Statement", "start": 0, "end": 13},
    {"label": "Founding Story", "start": 13, "end": 33},
    {"label": "Product Today", "start": 33, "end": 63},
    {"label": "Scale — Animated Counters", "start": 63, "end": 78},
    {"label": "Customer Impact — Client VP", "start": 78, "end": 103},
    {"label": "CEO Vision", "start": 103, "end": 123},
    {"label": "Outro + URL", "start": 123, "end": 128}
  ],
  "brand_compliance": {
    "colors_used": ["#1A365D", "#2B6CB0", "#E2E8F0"],
    "logo_placements": 3,
    "font": "Inter (brand-specified)"
  }
}
```

## Tips

1. **Trim the CEO to 90 seconds maximum** — Executive messages longer than 2 minutes lose 60% of viewers. The CEO's 12-minute recording contains 90 seconds of essential content. NemoVideo finds and extracts it.
2. **Use real employees, not actors** — Culture videos with stock footage or hired actors communicate inauthenticity. One genuine employee saying "I like that my manager trusts me to manage my own time" is worth more than a scripted monologue from a professional speaker.
3. **Lead with the number on annual report videos** — Investors click the video for financials. Revenue growth in the first 15 seconds earns them watching the remaining 2:45. Burying the numbers after a 60-second mission-statement preamble loses the audience.
4. **Animate counters for scale metrics** — "1,200 employees" as static text is forgettable. A counter rapidly ticking from 0 to 1,200 with a satisfying sound effect is memorable and shareable.
5. **Export multiple aspect ratios simultaneously** — The same video needs 16:9 for the website, 1:1 for LinkedIn, and 9:16 for executive social posts. NemoVideo renders all three from a single generation, with intelligent reframing for each ratio.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Website hero / investor deck / all-hands |
| MP4 9:16 | 1080p | Executive LinkedIn / Instagram Stories |
| MP4 1:1 | 1080p | LinkedIn feed / Twitter / Facebook |
| GIF | 720p | Counter animation / logo reveal loop |

## Related Skills

- [product-demo-video](/skills/product-demo-video) — Product demonstration videos
- [event-recap-video](/skills/event-recap-video) — Event highlight and recap videos
- [testimonial-video-maker](/skills/testimonial-video-maker) — Customer testimonial production

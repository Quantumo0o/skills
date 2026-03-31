---
name: make-video-ai
version: "1.0.0"
displayName: "Make Video AI — AI Video Maker Create Any Video from Text Description Free"
description: >
  Make any video with AI — describe what you want and NemoVideo creates it. Marketing ads, social content, educational lessons, product showcases, brand stories, event promos, training modules, and creative projects — all produced from a text description. No filming, no editing software, no production experience needed. Type what you envision and receive a complete video with AI-generated visuals, professional narration, background music, captions, transitions, and platform-optimized formatting. AI video maker free, create video with AI, make video online, AI video creator, video generator AI, text to video free, create video from description.
metadata: {"openclaw": {"emoji": "🎥", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Make Video AI — Describe It, and the AI Makes It

Video production has been a gatekept craft for decades. Making a professional video required: a camera ($500-$50,000), lighting ($200-$5,000), a location (free to $10,000/day), talent ($100-$10,000/day), editing software ($0-$600/year), editing skill (months to years of learning), music licensing ($50-$500/track), and time (hours to weeks per video). The total cost of a single professional marketing video: $2,000-$25,000. The total time: 1-6 weeks. These numbers meant that video production was reserved for companies with budgets and individuals with specialized skills. Everyone else — small businesses, solo entrepreneurs, educators, students, nonprofits, community organizations — either paid for expensive production or went without video entirely. NemoVideo removes every barrier simultaneously. No camera needed: AI generates visuals from descriptions. No editing software: the AI handles cuts, transitions, pacing, and formatting. No production skill: describe the result you want in plain language. No music licensing: royalty-free music selected and synced automatically. No time investment: minutes instead of weeks. The cost of making a professional video drops from thousands to the price of an API call. The skill required drops from years of training to the ability to describe what you want.

## Use Cases

1. **Small Business — First Marketing Video (30-90s)** — A local bakery has never had a marketing video. The owner types: "Make a 45-second video showing my bakery's fresh bread, croissants, and cakes. Morning light feeling. Show the bread being sliced, the croissants golden and flaky, and a beautiful cake display. End with: Fresh daily at Sunrise Bakery, 123 Main St. Warm, inviting music." NemoVideo produces: warm-lit bakery visuals with close-ups of each product, appetizing slow-motion on the bread slice and croissant flake, bakery display wide shot, text overlays with product names, CTA end frame with address and logo placeholder. The bakery's first video — professional quality from a text description.
2. **Educator — Lesson Video from Notes (5-15 min)** — A high school teacher needs a video explaining the French Revolution for remote students. They type their lesson outline and NemoVideo generates: animated timeline of key events (1789-1799), illustrated scenes for major moments (Storming of the Bastille, Declaration of Rights, Reign of Terror), portrait introductions for key figures (Louis XVI, Robespierre, Marie Antoinette), cause-and-effect diagrams animated step by step, and a summary quiz prompt at the end. Narration: clear, educational, age-appropriate. A complete lesson video from teaching notes.
3. **Startup — Pitch Video (2-3 min)** — A founder needs a video for their crowdfunding campaign but has zero budget for video production. They describe: "We're building a smart water bottle that reminds you to drink, tracks hydration, and syncs with fitness apps. Show the bottle in different settings: gym, office, hiking. Highlight features: LED reminder ring, app dashboard, 24-hour battery. Include testimonials as text cards. End with early bird pricing and campaign link." NemoVideo produces: product visualization in each setting, feature callouts with animated icons, testimonial cards with customer quotes, pricing tiers animation, and CTA with campaign link. A crowdfunding video that looks like a $5,000 production.
4. **Nonprofit — Awareness Campaign (60-120s)** — An animal shelter needs a fundraising video. They describe the mission and NemoVideo generates: emotional opening (lonely animal waiting), the shelter's impact (animated statistics: 500 animals rescued this year), volunteer moments (community engagement visuals), success stories (adopted animals in happy homes), and CTA ("Donate $25 to save a life — link below"). Music: emotional, hopeful. Narration: warm, compassionate. A cause video that drives donations without filming a single frame.
5. **Content Creator — Daily Video Without Camera (30-60s daily)** — A finance creator wants to post daily TikToks about money tips but refuses to appear on camera. Each day they type a tip ("Why you should never pay full price for a car") and NemoVideo generates: engaging visuals matching the topic (car dealership, negotiation scene, calculator), punchy AI voiceover (120 words for 45 seconds), word-by-word captions in trending style, beat-synced background music, and 9:16 vertical format. 30 seconds of typing produces a TikTok-ready video. 365 days of daily content from daily prompts.

## How It Works

### Step 1 — Describe Your Video
Type what you want. A single sentence works ("Make a 30-second ad for my coffee shop"). A detailed paragraph works better. The more specific, the more accurate the result.

### Step 2 — Choose Style and Format
Select: visual style, voice character, music mood, duration, and platform.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "make-video-ai",
    "prompt": "Make a 60-second video for a local coffee shop. Morning atmosphere: sunrise through the window, steam rising from fresh espresso, barista pouring latte art, customers smiling. Show 3 signature drinks with names and prices. Music: acoustic guitar, warm and inviting at -16dB. Voice: friendly female, casual tone. End with: Open daily 7AM-6PM, 456 Oak Street. Free WiFi. Hashtag #SunriseCoffee. Export for Instagram Reels (9:16) and Facebook Feed (1:1).",
    "visual_style": "warm-lifestyle",
    "voice": "friendly-female-casual",
    "music": "acoustic-warm",
    "music_volume": "-16dB",
    "duration": "60 sec",
    "captions": {"style": "minimal-elegant"},
    "formats": ["9:16", "1:1"]
  }'
```

### Step 4 — Review and Share
Preview both formats. Adjust: scene pacing, music energy, text placement. Share directly to social media or download.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the video you want |
| `visual_style` | string | | "warm-lifestyle", "corporate-clean", "cinematic", "animated", "vibrant" |
| `voice` | string | | "friendly-female", "authoritative-male", "energetic", "calm", "none" |
| `music` | string | | "acoustic-warm", "upbeat", "cinematic", "corporate", "lo-fi", "none" |
| `music_volume` | string | | "-12dB" to "-22dB" |
| `duration` | string | | "15 sec", "30 sec", "60 sec", "2 min", "5 min" |
| `captions` | object | | {style, text, highlight, bg} |
| `formats` | array | | ["16:9","9:16","1:1","4:5"] |
| `brand` | object | | {colors, logo, fonts} |
| `batch_prompts` | array | | Multiple videos from multiple descriptions |

## Output Example

```json
{
  "job_id": "mva-20260328-001",
  "status": "completed",
  "duration_seconds": 58,
  "outputs": {
    "reels_9x16": {
      "file": "coffee-shop-9x16.mp4",
      "resolution": "1080x1920",
      "duration": "0:58",
      "scenes": 8,
      "voice": "friendly-female-casual",
      "music": "acoustic-warm at -16dB",
      "captions": "minimal-elegant"
    },
    "feed_1x1": {
      "file": "coffee-shop-1x1.mp4",
      "resolution": "1080x1080",
      "duration": "0:58"
    }
  }
}
```

## Tips

1. **Specific descriptions produce dramatically better videos** — "A coffee shop video" generates something generic. "Morning light through a window hitting a white marble counter, steam curling from a ceramic mug, barista hands pouring a rosetta latte art" generates a scene you can feel. Sensory detail drives quality.
2. **One video idea + multiple formats = maximum platform coverage** — Describe the video once. Export in 16:9 (YouTube), 9:16 (TikTok/Reels), 1:1 (Instagram/LinkedIn). One creative decision, three platforms covered.
3. **Batch generation turns a brainstorm into a content library** — Write 20 video descriptions in a spreadsheet. Batch-generate all 20. Schedule across the month. A month of video content from one creative session.
4. **Match visual style to the audience expectation** — Warm-lifestyle for food and wellness. Corporate-clean for B2B. Vibrant for fashion and entertainment. Cinematic for storytelling. The visual style signals what kind of content the viewer is about to watch.
5. **Duration should match the platform and the message density** — 15-30 seconds for ads and product teasers. 45-60 seconds for social content. 2-5 minutes for educational and explainer. Longer is not better — appropriate length is better.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website / presentation |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts / Stories |
| MP4 1:1 | 1080x1080 | Instagram / Facebook / LinkedIn |
| MP4 4:5 | 1080x1350 | Facebook / Instagram feed |
| GIF | 720p | Email / web preview |

## Related Skills

- [podcast-video-maker](/skills/podcast-video-maker) — Podcast video creation
- [demo-video-maker](/skills/demo-video-maker) — Product demo videos

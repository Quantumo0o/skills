---
name: ai-video-ads-maker
version: 1.0.2
displayName: "AI Video Ads Maker — Create High Converting Video Ads for Every Platform"
description: >
  Create high-converting video ads with AI — produce Facebook ads, Instagram ads, TikTok ads, YouTube pre-roll, Google Video ads, and LinkedIn video ads from a product description or creative brief. NemoVideo generates complete ad creatives: hook-driven openings that stop the scroll, benefit-focused messaging, social proof integration, urgency elements, clear CTAs, and platform-specific formatting. Produce 10 ad variations in the time it takes to brief an agency on one. AI ad maker, video ad creator, Facebook video ad, TikTok ad maker, social media ad video, product ad generator, performance marketing video.
metadata: {"openclaw": {"emoji": "📢", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# AI Video Ads Maker — Ad Creatives That Convert at Scale

The math of paid advertising is simple: creative quality determines cost per acquisition. The same product, same audience, same budget — swap the creative and CPA can change by 300-500%. Media buying is optimized to diminishing returns. Creative is where the leverage lives. Yet most businesses produce 2-3 ad variations and run them until they die. The reason: each variation traditionally costs $500-2,000 to produce (scripting, filming, editing, formatting for each platform). Testing 20 variations means $10,000-40,000 in production costs before a single dollar of media spend. This production bottleneck means most ad accounts are undertested. The winning creative exists in the space of variations never produced. NemoVideo eliminates the production bottleneck. Describe the product, the target audience, and the desired action — the AI generates complete video ad creatives: multiple hook variations (the first 3 seconds that determine whether the viewer watches or scrolls), multiple messaging angles (benefit-led, problem-led, social-proof-led, urgency-led), multiple visual styles (UGC-feel, polished brand, testimonial, demonstration), and multiple format exports (16:9, 9:16, 1:1, 4:5). Ten creative variations in minutes. Test them all. Scale the winners.

## Use Cases

1. **Facebook/Instagram Ads — Multi-Hook Testing (15-30s)** — A DTC brand launches a new skincare serum. NemoVideo generates 10 ad variations: 5 different hooks × 2 messaging angles. Hook variations: (1) Problem-led ("Tired of spending $200/month on skincare that doesn't work?"), (2) Result-led ("Clear skin in 14 days — here's how"), (3) Social proof ("500K people switched to this serum last month"), (4) Curiosity ("Dermatologists don't want you to know this"), (5) UGC-feel ("Okay so I tried this serum everyone's talking about..."). Each hook leads into two messaging paths: benefit-focused or comparison-focused. Ten creatives × 3 formats (9:16, 1:1, 4:5) = 30 ready-to-upload ad files. Launch, let the algorithm find the winner, kill the losers, scale the winners.
2. **TikTok Ads — Native-Feel Creatives (15-45s)** — TikTok's ad platform rewards creatives that look like organic content. Polished brand ads get scrolled past; native-feel content gets watched. NemoVideo produces: UGC-style testimonials (person talking to camera with authentic energy, not scripted-sounding), trending format adaptations (green screen reaction, stitch-style, duet-style), product-in-use demonstrations shot in casual settings (kitchen counter, desk, bathroom mirror), and text-overlay storytelling (no voiceover, just text and music — the most-engaged TikTok ad format). Each creative feels like content the viewer's friend posted, not an ad from a brand.
3. **YouTube Pre-Roll — 6-Second Bumper + 15-Second Skip (6s/15s)** — A B2B SaaS needs YouTube ads. NemoVideo creates: 6-second bumper ads (brand name + one benefit + visual demo in 6 seconds — no time for storytelling, pure impact), 15-second skippable ads (5-second hook that delivers value before the skip button appears + 10-second pitch for those who stay), and 30-second non-skippable for high-intent placements. Each format has different creative requirements — NemoVideo optimizes per format rather than cutting a 30-second ad down to 6 seconds.
4. **Retargeting Ads — Objection Handling Sequences (15-30s)** — Website visitors who did not purchase need different messaging than cold audiences. NemoVideo creates retargeting ad sequences: Ad 1 (social proof — "Join 50,000 customers"), Ad 2 (objection handling — "Free returns, no risk"), Ad 3 (urgency — "Sale ends Sunday"), Ad 4 (testimonial — real customer result story). Each ad addresses a different reason the viewer did not convert initially. The sequence guides hesitant buyers through their remaining objections.
5. **Creative Refresh — New Variations for Fatigued Ads (ongoing)** — An ad performing at $12 CPA for 3 weeks is now at $28 CPA — creative fatigue. The audience has seen it too many times. NemoVideo: takes the winning ad's core message and produces 5 new visual variations (same script, different visuals), 3 new hook variations (same message, different opening), and 2 completely new angles (same product, different emotional appeal). Creative refresh in minutes instead of the 1-2 weeks typically needed to produce new variations.

## How It Works

### Step 1 — Brief the AI
Product/service description, target audience, desired action (purchase, sign-up, download), and any brand guidelines.

### Step 2 — Set Creative Parameters
Hook style, messaging angle, visual format, platform targets, and number of variations.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-ads-maker",
    "prompt": "Create 6 video ad variations for a meal delivery subscription ($8.99/meal, healthy chef-prepared meals, delivered weekly). Target: busy professionals 25-45 who want healthy food but have no time to cook. Desired action: Start free trial. Variations: 2 problem-led (no time to cook pain point), 2 result-led (healthy meals effortlessly), 2 UGC-style (person unboxing and tasting). Each variation in 3 formats: 9:16 (TikTok/Reels), 1:1 (Facebook feed), 4:5 (Instagram feed). Duration: 20-25 seconds. Include urgency element: first week free, limited time.",
    "product": {"name": "FreshBox", "price": "$8.99/meal", "offer": "First week free"},
    "audience": "busy professionals 25-45",
    "cta": "Start free trial",
    "variations": 6,
    "hooks": ["problem-led", "problem-led", "result-led", "result-led", "ugc", "ugc"],
    "formats": ["9:16", "1:1", "4:5"],
    "duration": "20-25 sec"
  }'
```

### Step 4 — Upload and Test
Upload all variations to ad platforms. Set up A/B tests with equal budget distribution. After 48-72 hours: kill bottom 50%, reallocate budget to top performers, generate new variations inspired by winners.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Product description and ad brief |
| `product` | object | | {name, price, offer, url} |
| `audience` | string | | Target audience description |
| `cta` | string | | "Buy now", "Start free trial", "Learn more", "Sign up" |
| `variations` | integer | | Number of creative variations (1-20) |
| `hooks` | array | | ["problem-led", "result-led", "social-proof", "curiosity", "ugc"] |
| `formats` | array | | ["16:9", "9:16", "1:1", "4:5"] |
| `duration` | string | | "6 sec", "15 sec", "20-25 sec", "30 sec" |
| `platforms` | array | | ["facebook", "tiktok", "youtube", "linkedin"] |
| `retargeting` | boolean | | Create retargeting sequence |
| `brand_colors` | array | | Hex codes for brand consistency |

## Output Example

```json
{
  "job_id": "vam-20260328-001",
  "status": "completed",
  "variations": 6,
  "formats_per_variation": 3,
  "total_files": 18,
  "outputs": {
    "variation_1_problem": {
      "hook": "You spend 2 hours cooking for 20 minutes of eating",
      "files": ["v1-9x16.mp4", "v1-1x1.mp4", "v1-4x5.mp4"]
    },
    "variation_2_problem": {
      "hook": "The Sunday meal prep lie — you won't keep it up",
      "files": ["v2-9x16.mp4", "v2-1x1.mp4", "v2-4x5.mp4"]
    },
    "variation_3_result": {
      "hook": "Healthy dinner in 3 minutes — no cooking",
      "files": ["v3-9x16.mp4", "v3-1x1.mp4", "v3-4x5.mp4"]
    },
    "variation_4_result": {
      "hook": "I eat chef-quality meals every night for $8.99",
      "files": ["v4-9x16.mp4", "v4-1x1.mp4", "v4-4x5.mp4"]
    },
    "variation_5_ugc": {
      "hook": "Okay I finally tried that meal delivery everyone's posting",
      "files": ["v5-9x16.mp4", "v5-1x1.mp4", "v5-4x5.mp4"]
    },
    "variation_6_ugc": {
      "hook": "Unboxing my first FreshBox — is it actually good?",
      "files": ["v6-9x16.mp4", "v6-1x1.mp4", "v6-4x5.mp4"]
    }
  }
}
```

## Tips

1. **Test hooks, not entire creatives** — The first 3 seconds determine 80%+ of ad performance. Test 5 different hooks with the same body content before testing different body content with the same hook. Hooks are the highest-leverage variable.
2. **UGC-style ads outperform polished brand ads on TikTok and Reels by 2-3x** — The platforms trained users to consume authentic content. An ad that looks like an ad triggers scroll reflex. An ad that looks like a friend's post gets watched.
3. **Creative fatigue is inevitable — plan for it** — Every winning ad will fatigue within 2-6 weeks. Have new variations ready before the CPA spike. Generating 5 refreshed variations every 2 weeks keeps performance stable.
4. **Multi-format from day one saves emergency reformatting** — An ad that works on Facebook at 1:1 will be needed on TikTok at 9:16 within days. Generating all formats upfront means you can launch cross-platform immediately when you find a winner.
5. **Retargeting sequences recover 20-40% of lost conversions** — A single retargeting ad recovers some. A 4-ad sequence addressing different objections (price, trust, urgency, social proof) systematically converts the hesitant majority.

## Output Formats

| Format | Resolution | Platform |
|--------|-----------|----------|
| MP4 9:16 | 1080x1920 | TikTok / Reels / Stories |
| MP4 1:1 | 1080x1080 | Facebook / Instagram feed |
| MP4 4:5 | 1080x1350 | Instagram feed (tall) |
| MP4 16:9 | 1920x1080 | YouTube / LinkedIn |
| MP4 16:9 | 1280x720 | YouTube bumper (6s) |

## Related Skills

- [ai-product-demo-video](/skills/ai-product-demo-video) — Product demos
- [ai-brand-video-maker](/skills/ai-brand-video-maker) — Brand videos
- [ai-promo-video-maker](/skills/ai-promo-video-maker) — Promo videos

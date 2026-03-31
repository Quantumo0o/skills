---
name: commercial-video-maker
version: 1.0.5
displayName: "Commercial Video Maker — Create TV Commercials and Brand Campaign Videos"
description: >
  Commercial Video Maker — Create TV Commercials and Brand Campaign Videos.
metadata: {"openclaw": {"emoji": "🎥", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# Commercial Video Maker — TV Commercials and Brand Campaign Videos

The Super Bowl commercial costs seven million dollars for thirty seconds of airtime and the company that paid it is betting that those thirty seconds will generate enough brand recall, emotional association, and water-cooler conversation to justify spending what most small countries would consider a generous annual infrastructure budget on a single advertisement — and the terrifying part is that it usually works, because a well-crafted commercial occupies a space in culture that no other marketing format can reach: the shared experience of millions of people watching the same story at the same time and forming the same emotional connection to a brand they didn't think about five minutes earlier. Commercial video content is the apex of advertising craft — every frame justified, every second earning its place, every cut serving the story, because when you're paying thousands of dollars per second of airtime (or competing for attention in a feed where the viewer's next action is always "scroll past"), waste is not just inefficient, it's fatal to the message. This tool transforms creative briefs into polished commercial videos — narrative-driven brand stories that build emotional resonance before revealing the product, lifestyle commercials showing the product integrated into aspirational daily life, humor-driven spots that make the brand memorable through laughter, cinematic product reveals with the production quality of a film trailer, seasonal campaign videos tied to cultural moments, and the anthem-format brand manifestos that define what a company stands for in sixty seconds of carefully orchestrated emotion. Built for creative agencies producing client campaigns, in-house brand teams creating flagship content, production companies delivering broadcast-ready commercials, startups launching their first brand video, retail brands producing seasonal campaign content, and anyone whose brand story deserves the craft and emotional precision of a proper commercial.

## Example Prompts

### 1. Brand Story Commercial — Emotional Narrative
"Create a 60-second brand story commercial for a running shoe company. Opening (0-5 sec): darkness. The sound of breathing — heavy, labored. A single streetlight illuminates wet pavement. A runner's shoes enter the frame from below — worn, muddy. 'The commercial doesn't start with the brand. It starts with the effort.' The runner (5-25 sec): early morning. The runner moves through empty streets — 5:00 AM, no one watching. Quick cuts: the alarm going off in darkness, the moment of decision in bed (get up or stay), the lacing of shoes, the door opening to cold air. 'Every runner knows this moment. The commercial earns credibility by showing it honestly.' The struggle: a hill. The breathing gets harder. The pace slows but doesn't stop. Rain starts. The runner doesn't stop. 'The struggle is the story. The shoe is present but not featured — it's on the feet, doing its job, not asking for attention.' The turn (25-40 sec): sunrise begins. The sky shifts from black to blue to orange. The runner crests the hill. The city appears below — lights turning on, the world waking up while this person is already in motion. Music shifts: from minimal to building. 'The emotional arc follows the run: dark to light, struggle to reward, alone to connected with the waking world.' The community (40-50 sec): other runners appear. A nod between strangers. A wave. The runner joins a group — different ages, different bodies, different paces, same shoes. 'The product connects people. The commercial shows the connection, not the product.' The brand (50-58 sec): the group runs together. The camera pulls back — the city, the runners, the morning. Voice-over (the first words spoken): 'Every run starts with one step. Make it count.' The shoe — finally shown in detail. Clean, iconic, the design visible for 3 seconds. Logo. The tagline (58-60 sec): text on screen. Simple. Memorable. The logo. 'The brand appears at the 50-second mark of a 60-second commercial. The first 50 seconds earned the right to show it.'"

### 2. Product Launch Commercial — Cinematic Reveal
"Build a 30-second product launch commercial for a new smartphone. The tease (0-8 sec): abstract shapes — light refracting through glass, metallic surfaces catching reflections, extreme macro shots that could be anything. Music: a single sustained note building tension. 'The viewer doesn't know what they're looking at. The mystery creates attention.' The reveal (8-15 sec): the shapes resolve — it's the phone. A slow rotation revealing the design from every angle. The screen lights up. The camera quality evident in the footage being shot BY the phone (show what it captures, not what it looks like). 'The best phone commercial shows what the phone DOES, not what it IS.' The features (15-25 sec): three features, each in 3 seconds. Feature 1: camera — a photo taken in low light, stunning quality. 'Shot on [phone].' Feature 2: speed — an app opening instantly, a video editing in real time. Feature 3: battery — a full day montage compressed to 3 seconds, the battery indicator ending the day at 40%. 'Three features. Nine seconds. Each one demonstrated, not described.' The close (25-30 sec): the phone in hand, used naturally — not held up like an artifact but used like a tool. Brand. Name. Date. Price. 'Available [date]. Starting at [$price].' 'The close tells the viewer exactly what to do next: know the date, know the price, make a decision.'"

### 3. Humor Commercial — Comedy-Driven Brand Spot
"Produce a 45-second humor commercial for a home security system. The setup (0-15 sec): a dog home alone. The doorbell rings (the security camera notification). The dog looks at the camera — a tiny Chihuahua wearing an oversized 'Security' vest. 'The visual comedy is immediate: the world's least intimidating security guard.' The dog walks to the door. On the security camera screen: a delivery person. The dog barks — tiny, ineffective. The delivery person doesn't react. The escalation (15-30 sec): the smart-home system activates. The camera speaks (the owner's voice through the doorbell): 'Leave the package on the porch, please.' The delivery person: 'Oh! Sure. Nice dog.' The dog's expression: offended. 'The comedy comes from the dog's reaction. Anthropomorphizing pets is the safest comedy bet in advertising.' The second ring: a suspicious person. The camera detects them. The app alerts the owner's phone. The owner speaks through the camera: 'Can I help you?' The person leaves. The dog watches, then struts back to the couch — mission accomplished. The close (30-45 sec): the dog on the couch, the security system dashboard visible on a tablet beside it. Voice-over: '[Brand] home security. Because your dog is great. But your dog is 4 pounds.' The dog looks at the camera. Logo. CTA. 'Humor makes the brand memorable. The product demonstration happened inside the joke — the viewer saw every feature without feeling sold to.'"

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the brand, product, creative concept, and emotional tone |
| `duration` | string | | Target length (e.g. "15 sec", "30 sec", "45 sec", "60 sec") |
| `style` | string | | Video style: "brand-story", "product-launch", "humor", "lifestyle", "anthem" |
| `music` | string | | Background audio: "cinematic-build", "emotional-strings", "upbeat-pop", "comedy-light", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `brand_reveal` | string | | When to reveal the brand: "early", "middle", "late" (default: "late") |
| `cta_style` | string | | Call-to-action approach: "direct", "subtle", "none" |

## Workflow

1. **Describe** — Outline the brand, creative concept, emotional arc, and target audience
2. **Upload** — Add product footage, brand assets, talent footage, and location shots
3. **Generate** — AI produces the commercial with narrative pacing, music sync, and brand integration
4. **Review** — Verify brand alignment, emotional resonance, and legal compliance
5. **Export** — Download in broadcast-ready or digital-optimized formats

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "commercial-video-maker",
    "prompt": "Create a 60-second running shoe brand story: pre-dawn darkness opening with breathing audio, 5AM alarm decision moment, rain-soaked hill struggle, sunrise crest with city reveal, runner community joining with shared nod, first voiceover at 50 sec with shoe detail reveal, logo and tagline closing",
    "duration": "60 sec",
    "style": "brand-story",
    "brand_reveal": "late",
    "music": "cinematic-build",
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Delay the brand reveal** — Earn attention with story before asking for brand recognition. The AI positions brand elements according to brand_reveal timing.
2. **Show the product in use, not on display** — A shoe on a runner beats a shoe on a pedestal. The AI integrates products into narrative action.
3. **Use one emotional arc, not multiple messages** — One feeling, fully executed, beats three benefits, briefly mentioned. The AI structures single-emotion narratives.
4. **Match music to emotional beats** — The score should build, peak, and resolve with the story. The AI syncs music dynamics to narrative pacing.
5. **End on the human, not the product** — The person's face, the community, the emotion. The AI places human moments at the conclusion.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | TV broadcast / YouTube pre-roll |
| MP4 9:16 | 1080p | TikTok / Instagram Stories |
| MP4 1:1 | 1080p | Facebook / Instagram feed |
| MP4 4:5 | 1080p | Facebook feed optimized |

## Related Skills

- [advertisement-video-maker](/skills/advertisement-video-maker) — Ad campaign and marketing videos
- [promo-video-maker](/skills/promo-video-maker) — Promotional and launch videos
- [sales-video-maker](/skills/sales-video-maker) — Sales pitch and demo videos

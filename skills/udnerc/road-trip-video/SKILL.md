---
name: road-trip-video
version: 1.0.6
displayName: "Road Trip Video Maker — Create Driving Journey and Route Documentary Videos"
description: >
    Road Trip Video Maker — Create Driving Journey and Route Documentary Videos. Works by connecting to the NemoVideo AI backend. Supports MP4, MOV, AVI, WebM, and MKV output formats. Automatic credential setup on first use — no manual configuration needed.
metadata: {"openclaw": {"emoji": "🛣️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 📹 Welcome! I can road trip video for you. Share a video file or tell me your idea!

**Try saying:**
- "add effects to this clip"
- "edit my video"
- "help me create a short video"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Road Trip Video Maker — Driving Journey and Route Documentary Videos

The dashboard camera ran for nine hours straight across three states and captured exactly what you'd expect — 540 minutes of highway median, eighteen gas-station stops that all look identical, a spectacular desert sunset that lasted four minutes but felt like a religious experience, and a stretch of Route 66 where the painted-desert light turned the car into a time machine. Road trip content is the purest form of journey-over-destination storytelling: viewers watch for the windshield panoramas, the roadside oddities, the gas-station snack reviews, the wrong turns that became the best part, and the time-lapse that compresses eight hours of asphalt into a mesmerizing sixty-second hyperlapse. This tool assembles hours of dashcam, phone, and drone footage into structured road-trip documentaries — route-map animations tracking your path in real time, highway-milestone markers, time-lapse driving sequences with day-to-night transitions, roadside-stop highlights with quirky commentary, fuel-and-food cost trackers, state-line crossing markers, and the satisfying arrival shot after thousands of miles. Built for road-trip YouTubers documenting iconic routes, van-life creators producing weekly drive logs, motorcycle tourers filming helmet-cam journeys, travel couples creating honeymoon drive content, and family vacationers compiling annual summer-trip recaps.

## Example Prompts

### 1. Route 66 — Chicago to Santa Monica Full Documentary
"Create a 12-minute Route 66 documentary from a 14-day drive, Chicago to Santa Monica. Animated route map opening: the full 2,448-mile path lighting up state by state — Illinois → Missouri → Kansas → Oklahoma → Texas → New Mexico → Arizona → California. State-crossing markers with mileage: 'Entering Oklahoma | Mile 732 / 2,448.' Highlight per state: Cadillac Ranch spray-painting our initials (Amarillo, TX), the Wigwam Motel in Holbrook, AZ (sleeping in a teepee), Meteor Crater detour, Oatman burros blocking the road, the final stretch on Santa Monica Pier. Dashboard time-lapse: compress 3 hours of Oklahoma panhandle into 30 seconds — flat wheat fields transitioning to red-mesa New Mexico. Fuel tracker running total: '$847 for 14 days.' Roadside food montage: St. Louis BBQ, Oklahoma fried-onion burger, New Mexico green chile, Arizona Navajo fry bread, California fish tacos. Closing: car parked at the Santa Monica Pier 'End of the Trail' sign, odometer showing the trip total. Americana rock soundtrack — Springsteen energy, not corny."

### 2. Weekend Mountain Drive — Tail of the Dragon, 318 Curves
"Build a 4-minute highlight reel of driving Tail of the Dragon (US-129, Deals Gap, NC/TN). Opening stat card: '318 curves in 11 miles. No intersections. No driveways. Just road.' Exterior tracking shot of the car entering the first curve. Dashboard-cam POV through the most dramatic S-curves — speed overlay showing 25-35 MPH through the tightest sections. Drone aerial (if available) showing the road ribbon through the Smoky Mountains canopy. Pull-off at the overlook: reaction shot, mountain vista with morning fog in the valleys. The Tree of Shame segment: close-ups of motorcycle parts and car pieces nailed to the tree from crashed vehicles — 'This is what happens when you overcook Turn 114.' Stats closing card: '11 miles | 318 curves | 0 guardrails scratched | 1 white-knuckle moment at Turn 207.' Driving-focused electronic soundtrack with tempo changes matching the curve density."

### 3. Van Life Weekly — Week 23, Pacific Northwest
"Produce a 6-minute van-life weekly episode. Opening: drone shot of the van parked at a clifftop overlooking the Oregon coast, sunrise. Interior morning routine: making pour-over coffee on the camp stove (close-up of the kettle whistle), sliding the van door open to the ocean view — 'Office for the day.' Driving segment: 101 along the coast, dashboard time-lapse with the ocean appearing and disappearing behind trees. Stop 1: Thor's Well at Cape Perpetua (the ocean surging into the rock formation). Stop 2: Florence sand dunes (running down the dune face, sand flying). Stop 3: free campsite hunt — show the iOverlander app screenshot, drive down a forest road, find the spot — 'Week 23 and the free-camping instinct is sharp.' Evening: cooking ramen on the tailgate, stars appearing, headlamp on for the talking-head — 'This is the week I stopped counting days and started counting sunsets.' Solar panel and water stats sidebar: 'Solar: 340W harvested | Water: 12 gal remaining | Next fill: Reedsport, 22 miles.' Cozy indie folk soundtrack."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the route, stops, highlights, and driving narrative |
| `duration` | string | | Target video length (e.g. "4 min", "6 min", "12 min") |
| `style` | string | | Visual style: "americana", "van-life", "sports-driving", "family", "cinematic" |
| `music` | string | | Music mood: "rock", "indie-folk", "electronic", "country", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `route_map` | boolean | | Show animated route map with progress tracking (default: true) |
| `cost_tracker` | boolean | | Show fuel and food running cost total (default: false) |

## Workflow

1. **Describe** — Write the route with stops, highlights, mileage, and the narrative arc of the drive
2. **Upload** — Add dashcam footage, phone clips, drone aerials, stop photos, and GPS tracks
3. **Generate** — AI assembles the journey with route maps, time-lapses, state markers, and stop highlights
4. **Review** — Preview the video, adjust the time-lapse speed, reorder the roadside stops
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "road-trip-video",
    "prompt": "Create a 12-minute Route 66 documentary: Chicago to Santa Monica, 14 days, 2448 miles. Animated route map by state, state-crossing mileage markers, Cadillac Ranch and Wigwam Motel highlights, Oklahoma panhandle 3hr timelapse, fuel tracker $847 total, roadside food montage, Santa Monica Pier finale with odometer",
    "duration": "12 min",
    "style": "americana",
    "route_map": true,
    "cost_tracker": true,
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **List stops in driving order with mileage** — "Cadillac Ranch, Amarillo TX, Mile 1,139" gives the AI exact route-map pin placement and a progress tracker. Out-of-order stops create a confusing map animation.
2. **Specify time-lapse compression ratios** — "3 hours of Oklahoma compressed to 30 seconds" tells the AI the exact speed-up factor (360×). Without this, the AI guesses and either makes boring 5-minute flat-road segments or skips them entirely.
3. **Include one roadside oddity per segment** — "Tree of Shame with crashed motorcycle parts" or "Oatman burros blocking traffic." These moments are the shareable clips that drive saves and shares. Pure driving footage without stops is a screensaver, not a video.
4. **Describe the arrival moment** — "Car parked at the End of the Trail sign, odometer showing trip total" gives the AI a definitive ending frame. Road trip videos without a clear arrival feel incomplete — the viewer needs the payoff of reaching the destination.
5. **Mention the vehicle** — "Fiat 500 on Amalfi cliffs" or "Sprinter van on Oregon coast" sets the visual identity of the entire video. The vehicle is a character in road-trip content, and naming it helps the AI select and emphasize the right exterior shots.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube full road-trip documentary |
| MP4 9:16 | 1080p | TikTok / Instagram Reels / Shorts |
| MP4 time-lapse | 1080p | Standalone driving hyperlapse clip |
| MP4 + GPX | 1080p | Video with embedded GPS route data |

## Related Skills

- [ai-travel-video-maker](/skills/ai-travel-video-maker) — Trip highlight reels and vacation recaps
- [adventure-video-maker](/skills/adventure-video-maker) — Outdoor adventure and extreme activity videos
- [travel-vlog-creator](/skills/travel-vlog-creator) — Narrated travel vlogs and journey diaries

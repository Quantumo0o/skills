---
name: running-video-maker
version: "1.0.1"
displayName: "Running Video Maker"
description: >
  Describe your running topic and NemoVideo creates the video. Marathon and race recap content, training plan walkthrough content, running form and technique tutorial, running gear review content, injury prevention and recovery content, running route and location content — narrate the run, the training approach, the specific technique or gear, and the honest account of what running has changed ab...

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> ✨ Hey! I'm ready to help you running video maker. Send me a video file or just tell me what you need!

**Try saying:**
- "add effects to this clip"
- "edit my video"
- "help me create a short video"

**IMPORTANT**: Do NOT wait silently. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Running Video Maker — Create Training, Race, and Running Journey Content

Describe your running topic and NemoVideo creates the video. Marathon and race recap content, training plan walkthrough content, running form and technique tutorial, running gear review content, injury prevention and recovery content, running route and location content — narrate the run, the training approach, the specific technique or gear, and the honest account of what running has changed about how you approach effort and discomfort.

## When to Use This Skill

- Create marathon, half marathon, and race recap content
- Film training plan and progression content
- Build running form, technique, and cadence tutorial content
- Document gear review and running kit content
- Create injury prevention and recovery guide content
- Produce running route, location, and destination content

## How to Describe Your Running Content

Be specific about the distance, the pace targets, the training structure, the honest physical experience, and what running has taught you.

**Examples of good prompts:**
- "My first marathon — what the training plan said vs what actually happened: The plan: 18-week Hal Higdon Novice 1 program, peak mileage 20 miles. What happened in training: the 16-mile long run in week 14 was fine. The 20-mile run in week 16 wasn't — I hit the wall at mile 17 and spent 3 miles walking. Lesson: I needed more nutrition practice on long runs. Race day: the crowd energy at miles 1-13 carried me past my planned pace. Miles 14-20: felt strong, too strong (I didn't know yet that marathon pace has a reckoning). Miles 20-26: what people mean by 'the wall' became physically comprehensible in a way no description prepared me for. Finish time: 4:22 (goal was 4:30 — I was 8 minutes ahead of goal but felt like I'd been beat up). What I'd do differently: run the first half 10 minutes slower than target, practice nutrition on every long run from week 10 onward, respect the wall in training by running through it rather than stopping."
- "Running form fixes that actually made a difference — what I changed after a gait analysis: I'd been running for 3 years with recurring knee pain. A physical therapist did a gait analysis on a treadmill. What we found: overstriding (my foot landing in front of my center of mass, creating a braking force with each step), heel striking hard (the impact force was going directly up the leg), and low cadence (160 steps per minute, 10% below optimal). The fixes: (1) Increase cadence by 5% (I used a metronome app set to 170 BPM for 2 weeks — cadence changes feel awful and then feel normal). (2) Land under the hips not in front (this is a cue, not a mechanical instruction — focus on where you're landing relative to your body). Result: knee pain resolved in 4 weeks, pace improved by 20 seconds per mile at the same effort. The fix I ignored until I was desperate: strength training for hip abductors. My glutes were weak and my knee was compensating."
- "Running in 5 countries in one year — what I learned about running as a travel tool: I ran in New York, Copenhagen, Tokyo, Cape Town, and Melbourne in the same year. Running is the best way to understand a city in 45 minutes. What I learned in each place: Copenhagen's running culture (infrastructure designed around it, running paths with distance markers, people run at any hour). Tokyo's precision (every crosswalk has an exact timing, running routes follow the Imperial Palace moat, uniform but beautiful). Cape Town's intensity (Table Mountain running, 800m elevation, incredible and humbling). The specific difference between running a city as a tourist vs running it as someone who lives there: tourists run loops, residents run errands. The route that connects a neighborhood to a market to a waterfront tells you more about a city than any itinerary."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `content_type` | Running content | `"race_recap"`, `"training"`, `"form_fix"`, `"gear"`, `"route"`, `"journey"` |
| `distance` | Race or run | `"marathon"`, `"half marathon"`, `"5K"`, `"trail 50K"` |
| `training_approach` | Method | `"Hal Higdon Novice 1"`, `"zone 2 heart rate"`, `"strides and intervals"` |
| `honest_experience` | Physical reality | `["hit wall at mile 17"`, `"knee pain resolved in 4 weeks"`, `"Table Mountain humbling"]` |
| `specific_lesson` | What changed | `"run first half 10 min slower"`, `"cadence change feels awful then normal"` |
| `data_point` | Quantified result | `"4:22 finish"`, `"20 sec/mile faster at same effort"` |
| `tone` | Content energy | `"honest"`, `"instructional"`, `"inspirational"`, `"documentary"` |
| `duration_minutes` | Video length | `5`, `8`, `12` |
| `platform` | Distribution | `"youtube"`, `"instagram"`, `"tiktok"` |

## Workflow

1. Describe the run, the training, the honest experience, and the specific lesson
2. NemoVideo structures the running content with mileage markers and lesson callouts
3. Distance labels, pace data, and lesson formatting added automatically
4. Export with running content pacing suited to the endurance sports audience

## API Usage

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "running-video-maker",
    "input": {
      "prompt": "Couch to 5K — what the program doesn't tell you and what I wish someone had: I started C25K at age 38 having not run since high school. The program works — I finished it in 9 weeks. What it doesn't prepare you for: the first week feels impossible (the running intervals at week 1 felt like sprinting), then suddenly week 4 feels fine (the adaptation is real and faster than you expect). What I didn't know about breathing: breathing rhythm matters more than pace for beginners. Inhale for 3 steps, exhale for 2 steps — this stabilizes the diaphragm and eliminates the side stitch that caused me to stop in weeks 1-3. What I didn't know about shoes: I ran in my gym cross-trainers for 6 weeks before a running store fitting. The difference between my cross-trainers and running shoes was immediate and significant (the cross-trainers had no heel-to-toe drop, which was causing calf tightness). The thing that surprised me most: by week 7 I was looking forward to runs. I did not expect this. The neurological adaptation — the mood improvement from consistent running — is real and appears around week 5-6 for most beginners.",
      "content_type": "beginner_journey",
      "distance": "5K",
      "training_approach": "Couch to 5K 9-week program",
      "honest_experience": ["week 1 felt like sprinting", "week 4 felt fine", "mood improvement by week 7"],
      "specific_lesson": "breathing rhythm (3 in/2 out) eliminates side stitch, proper running shoes matter",
      "data_point": "9 weeks, age 38, no running since high school",
      "tone": "honest",
      "duration_minutes": 8,
      "platform": "youtube",
      "hashtags": ["Running", "CouchTo5K", "BeginnerRunning", "RunningTips", "RunningJourney"]
    }
  }'
```

## Tips for Best Results

- **The wall in training is the best preparation**: "I hit the wall at mile 17 in training and spent 3 miles walking — this is preparation, not failure" — the honest encounter with the physical limit in training reframes the experience as useful
- **The specific fix with the mechanism**: "Increase cadence by 5%, use a metronome app at 170 BPM for 2 weeks — it feels awful and then feels normal" — the specific intervention with the adaptation timeline is more useful than the general advice
- **The non-obvious lesson**: "Run the first half 10 minutes slower than target" or "strength training for hip abductors — my glutes were weak and my knee was compensating" — the counterintuitive finding from race or injury experience is the most shared running content
- **Running as city knowledge**: "Running connects a neighborhood to a market to a waterfront — it tells you more than any itinerary" — the observation that running is a learning tool, not just exercise, gives running content meaning beyond fitness
- **The neurological adaptation that surprises beginners**: "By week 7 I was looking forward to runs — I did not expect this" — naming the mood adaptation that beginners don't know to expect is the most encouraging and honest thing running content can offer

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 8–15 min |
| TikTok | 1080×1920 | 60–180s |
| Instagram Reels | 1080×1920 | 60–90s |

## Related Skills

- `sports-highlight-video` — Athletic achievement and moments content
- `home-workout-video` — Home training and fitness content
- `outdoor-workout-video` — Outdoor fitness content

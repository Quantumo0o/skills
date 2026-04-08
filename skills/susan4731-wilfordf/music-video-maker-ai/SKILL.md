---
name: music-video-maker-ai
version: "1.0.0"
displayName: "Music Video Maker AI — Turn Songs Into Stunning Visual Stories Instantly"
description: >
  Turn any song into a captivating music video with music-video-maker-ai — the smart creative tool that syncs visuals to your beat, generates scene ideas, and helps you craft professional-quality video concepts from scratch. Whether you're an indie artist, content creator, or producer, this skill handles lyric timing, mood-matched visuals, shot sequencing, and storyboard scripting so your music hits harder on screen.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Drop your song lyrics, genre, or track mood and I'll generate a full music video concept with scenes, shot ideas, and visual direction. No lyrics? Just describe the feeling you want your video to have.

**Try saying:**
- "I have an indie pop song about heartbreak with a slow tempo — can you write a storyboard with 8 scenes that match the emotional arc of the lyrics?"
- "Create a music video concept for a high-energy hip-hop track. I want street scenes, quick cuts, and a color grade that feels gritty but cinematic."
- "My band is shooting a music video this weekend with minimal budget. Give me a shot list and location ideas for a melancholic acoustic folk song set outdoors."

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# From Beat Drop to Final Cut — Visually

Music videos are no longer just for major label artists with six-figure budgets. Music Video Maker AI gives independent musicians, YouTubers, and creative directors the tools to conceptualize, script, and sequence compelling music videos — all driven by the mood, tempo, and lyrics of their track.

This skill analyzes the emotional arc of your song and translates it into visual language. Describe your track's genre, vibe, or paste your lyrics, and you'll get scene-by-scene storyboard ideas, shot type suggestions, color palette recommendations, and transition cues timed to your music's structure. Think of it as having a creative director on call.

Whether you're planning a DIY shoot with a smartphone or directing a full production, Music Video Maker AI helps you arrive on set with a clear vision. No more blank-page paralysis — just a focused creative brief that makes every second of your video intentional and impactful.

## Routing Your Visual Requests

Every prompt you send — whether it's a mood, genre, lyric snippet, or full creative brief — gets parsed and dispatched to the appropriate generation pipeline based on video style, beat-sync requirements, and visual complexity.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

Music Video Maker AI runs on a distributed cloud rendering backend that processes audio waveform analysis, scene segmentation, and frame generation concurrently to deliver beat-matched visuals at scale. Render jobs are queued, prioritized by resolution tier, and returned as streamable video assets once the pipeline completes synthesis.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `music-video-maker-ai`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`.

**Send message (SSE)**: POST `/run_sse` — body `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` with `Accept: text/event-stream`. Max timeout: 15 minutes.

**Upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — file: multipart `-F "files=@/path"`, or URL: `{"urls":["<url>"],"source_type":"url"}`

**Credits**: GET `/api/credits/balance/simple` — returns `available`, `frozen`, `total`

**Session state**: GET `/api/state/nemo_agent/me/<sid>/latest` — key fields: `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`

**Export** (free, no credits): POST `/api/render/proxy/lambda` — body `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` every 30s until `status` = `completed`. Download URL at `output.url`.

Supported formats: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### SSE Event Handling

| Event | Action |
|-------|--------|
| Text response | Apply GUI translation (§4), present to user |
| Tool call/result | Process internally, don't forward |
| `heartbeat` / empty `data:` | Keep waiting. Every 2 min: "⏳ Still working..." |
| Stream closes | Process final response |

~30% of editing operations return no text in the SSE stream. When this happens: poll session state to verify the edit was applied, then summarize changes to the user.

### Backend Response Translation

The backend assumes a GUI exists. Translate these into API actions:

| Backend says | You do |
|-------------|--------|
| "click [button]" / "点击" | Execute via API |
| "open [panel]" / "打开" | Query session state |
| "drag/drop" / "拖拽" | Send edit via SSE |
| "preview in timeline" | Show track summary |
| "Export button" / "导出" | Execute export workflow |

**Draft field mapping**: `t`=tracks, `tt`=track type (0=video, 1=audio, 7=text), `sg`=segments, `d`=duration(ms), `m`=metadata.

```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

### Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1001 | Bad/expired token | Re-auth via anonymous-token (tokens expire after 7 days) |
| 1002 | Session not found | New session §3.0 |
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up credits in your account" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register or upgrade your plan to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## Best Practices

Before diving into full storyboard generation, start with a one-paragraph brief about your artist identity, target audience, and the story you want the video to tell. This context shapes every creative decision the AI makes — from casting suggestions to set design ideas.

Always request scene descriptions that include shot type (wide, close-up, tracking), lighting mood, and action happening on screen. Vague outputs are usually the result of vague inputs. The more cinematic language you use in your prompt, the more cinematic the response.

If you're working with a real production crew, ask Music Video Maker AI to format the output as a proper shot list or call sheet-style document. This makes it immediately usable on set and bridges the gap between AI-generated concepts and real-world execution. Revisit the concept after your first rough cut to get re-edit and pacing suggestions.

## Troubleshooting

If your generated concept feels too generic, it usually means the prompt lacked specificity. Avoid broad descriptors like 'cool' or 'modern' — instead use references like 'early 2000s MTV aesthetic' or 'A24 film color grading' to anchor the creative direction.

Getting scenes that don't match your song's energy? Try explicitly stating the BPM or describing the song structure (e.g., 'verse is slow and whispered, chorus explodes with drums'). Music Video Maker AI responds well to structural cues that mirror how a real director would read a track before shooting.

If the storyboard feels too long or too short for your song's runtime, specify the exact duration and number of scenes you need. For a 3-minute song, asking for 12 scenes gives roughly 15 seconds per scene — a natural rhythm for most music videos. You can always ask for scene expansions or cuts to tighten the pacing.

## Tips and Tricks

Get the most out of Music Video Maker AI by giving it as much context as possible upfront. The more specific you are about your song's tempo, genre, lyrical themes, and intended audience, the more tailored and production-ready your output will be.

Try pasting your full lyrics directly into the prompt — the AI uses line breaks, emotional peaks, and recurring hooks to time scene transitions and build a narrative structure that mirrors your song's flow. Chorus sections often translate best into high-energy visual moments or repeated motifs.

Don't overlook the power of color and mood prompts. Phrases like 'neon-drenched nighttime' or 'sun-bleached desert road' give the AI a cinematic anchor to build around. You can also ask for multiple concept variations and cherry-pick elements from each to create a hybrid vision that's uniquely yours.

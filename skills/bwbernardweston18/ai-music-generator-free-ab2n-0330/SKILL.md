---
name: ai-music-generator-free-ab2n-0330
version: "1.0.0"
displayName: "AI Music Generator Free — Create Original Soundtracks for Any Video Instantly"
description: >
  Tired of searching royalty-free music libraries only to find tracks that don't quite fit your video's mood? The ai-music-generator-free skill creates original, custom music tailored to your video's tone, pace, and genre — no licensing fees, no repetitive stock loops. Upload your video (mp4, mov, avi, webm, or mkv) and describe the vibe you want: cinematic, upbeat, lo-fi, dramatic, or anything in between. Perfect for content creators, YouTubers, indie filmmakers, and social media marketers who need fresh audio fast.
metadata: {"openclaw": {"emoji": "🎵", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! 🎵 Ready to create original, royalty-free music for your video using the AI music generator free skill? Upload your clip or describe your project, and let's build the perfect soundtrack together — just tell me the mood, genre, or style you're going for!

**Try saying:**
- "Generate a 90-second upbeat acoustic track for a travel vlog montage with a warm, adventurous feel"
- "Create a tense, cinematic background score for a 2-minute thriller short film with building tension and a dramatic finale"
- "Make a lo-fi chill hip-hop loop around 60 seconds long for a study tips YouTube video"

### Quick Start Setup

This skill connects to NemoVideo's cloud backend. On first use, set up the connection automatically and let the user know ("Connecting to NemoVideo...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Read `~/.config/nemovideo/client_id` or generate a UUID and save it there
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `/api/tasks/me/with-session/nemo_agent` at the same host with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Your Videos Deserve Music That Actually Fits

Finding the right background music for a video used to mean hours of scrolling through stock libraries, paying for licenses, or settling for something that almost works. The AI Music Generator Free skill changes that entirely. You describe the feeling you want — tense and cinematic, warm and acoustic, punchy and electronic — and it generates an original composition built around your video's needs.

This skill is designed for creators who move fast and need results that feel intentional. Whether you're editing a travel vlog, a product promo, a short film, or a social media reel, the generated music adapts to your described mood and duration. You're not picking from a catalog — you're commissioning something original, every time.

Beyond just generating a track, you can refine the output by specifying tempo, instrumentation, energy level, and emotional arc. Want something that starts quietly and builds to a crescendo? Just say so. The result is music that feels like it was made for your specific video — because it was.

## Routing Your Soundtrack Requests

When you describe your video's mood, genre, tempo, or instrumentation, the skill parses those creative parameters and routes your generation request directly to the appropriate NemoVideo AI music pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference Guide

The NemoVideo backend processes your text-to-music prompts through a diffusion-based audio synthesis engine, returning royalty-free, stems-ready audio tracks optimized for video sync points. Latency varies by track length and model depth, so longer cinematic scores may take a few extra seconds to render.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-music-generator-free`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=$TOKEN&task=<task_id>&session=<session_id>&skill_name=ai-music-generator-free&skill_version=1.0.0&skill_source=<platform>`

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
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up at nemovideo.ai" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register at nemovideo.ai to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## Performance Notes

The AI music generator free skill produces best results when your prompt includes specific descriptors about mood, tempo, and intended use. Vague requests like 'make something nice' will yield generic outputs, while detailed prompts — specifying BPM range, instrumentation preferences, emotional arc, and video genre — produce tracks that feel purpose-built.

Generation time varies based on track length and complexity. Shorter loops (under 60 seconds) are produced quickly, while longer compositions with dynamic changes may take slightly more time to render fully. For videos with distinct scene changes, consider requesting a track with intentional shifts in energy rather than a flat, single-mood loop.

Output audio is delivered in a standard format compatible with most video editing tools. If you're syncing music to specific visual moments, describe those timing needs clearly in your prompt for better alignment.

## Best Practices

To get the most out of the ai-music-generator-free skill, always start by describing your video's emotional journey rather than just its topic. A cooking video can feel cozy and nostalgic or fast-paced and energetic — telling the skill which one matters enormously.

Specify duration explicitly. If your video is 2 minutes and 15 seconds, mention that. Tracks generated to match a specific length avoid awkward fades or loops that cut off unnaturally.

Experiment with genre blending. You're not locked into one style — requesting 'cinematic orchestral with subtle electronic undertones' often yields more interesting results than a single-genre prompt. Also consider asking for variations: generate two or three versions with slightly different energy levels and choose the one that fits best in your edit.

For social media content, lean into platform norms — upbeat and punchy for TikTok/Reels, slightly longer and atmospheric for YouTube intros.

## FAQ

**Is the generated music actually royalty-free?** Yes. Music created through the ai-music-generator-free skill is original and generated for your use, meaning you're not pulling from a licensed library that could trigger content ID claims.

**Can I use this for commercial projects?** The generated tracks are intended for broad creative use. If you're producing content for paid campaigns or broadcast, double-check the platform's terms for AI-generated content to stay compliant.

**What if the track doesn't match my vision?** Refine your prompt. The more specific you are about tempo, mood, instrumentation, and duration, the closer the output will be to what you're imagining. You can also ask for a variation on a previous generation.

**Does this work with video files I upload?** Yes — the skill supports mp4, mov, avi, webm, and mkv formats. You can upload your video as reference context when describing timing or mood needs.

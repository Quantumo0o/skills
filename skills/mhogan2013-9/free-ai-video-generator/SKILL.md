---
name: free-ai-video-generator
version: "1.0.0"
displayName: "Free AI Video Generator — Create Stunning Videos from Text, Ideas, or Scripts"
description: >
  Turn your ideas, scripts, or raw concepts into polished videos without spending a cent. This free-ai-video-generator skill helps creators, marketers, and educators produce engaging video content using AI — no camera, no editing software, no budget required. Describe a scene, paste a script, or outline a story, and get structured video content, scene breakdowns, voiceover scripts, and production-ready output in seconds.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome! This free AI video generator turns your ideas, scripts, or topics into fully structured video content — scenes, scripts, visuals, and all. Tell me what kind of video you want to create and let's get started right now.

**Try saying:**
- "Create a 60-second product explainer video script for a mobile budgeting app targeting college students, with scene descriptions and on-screen text suggestions."
- "Generate a 5-scene YouTube tutorial video outline on how to start a container garden at home, including voiceover narration and B-roll suggestions for each scene."
- "Write a short-form video script for Instagram Reels about 3 common resume mistakes, with hook, main content, and a strong call-to-action at the end."

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Generate Real Videos From Nothing But Your Ideas

Most people have video ideas they never act on — not because the ideas aren't good, but because video production feels expensive, complicated, or time-consuming. This skill changes that equation entirely. The free AI video generator helps you go from a blank page to a fully structured video concept, complete with scene-by-scene breakdowns, on-screen text suggestions, voiceover scripts, and visual direction notes.

Whether you're a solo content creator trying to grow on YouTube, a small business owner who needs product explainer videos, or a teacher building educational content, this tool adapts to your format and audience. You don't need a production team or a big budget — just tell it what your video is about and it handles the creative heavy lifting.

From 15-second social media clips to 10-minute tutorials, the generator structures your content intelligently, matching pacing, tone, and format to your specific goal. It's the fastest way to move from idea to production-ready video plan without touching a single piece of expensive software.

## Routing Your Video Requests

Each prompt you submit — whether a raw idea, a full script, or a scene description — is parsed and dispatched to the appropriate generation pipeline based on content type, duration, and style parameters.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

Video generation runs on a distributed cloud rendering backend that queues your text-to-video jobs, applies diffusion-based synthesis, and streams the rendered output back in real time. Clip resolution, frame rate, and style presets are all resolved server-side before the final MP4 is delivered.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-ai-video-generator`
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

## Common Workflows With the Free AI Video Generator

One of the most popular workflows is the idea-to-script pipeline: start by describing your video concept in one sentence, then ask for a full script with scene labels, then request a shot list and visual suggestions. Each step builds on the last, giving you a complete production package without starting from scratch.

Another common use case is repurposing existing content. Paste in a blog post or article and ask the generator to convert it into a structured video script — it will identify the key points, rewrite them for spoken delivery, and suggest where to add visuals or graphics to keep viewers engaged.

Marketers frequently use this tool to batch-create social video content. You can request 5 different 15-second scripts on the same product topic, each with a different angle or hook, making it easy to schedule a full week of content in one session. Educators use it to turn lesson plans into video lecture outlines with clear segment breaks and discussion prompts built in.

## Tips and Tricks for Getting the Best Results

The more specific your input, the better your video output. Instead of saying 'make a video about fitness,' try 'create a 2-minute motivational video for beginners starting their first gym routine, targeting women aged 25-40.' Platform context matters too — a TikTok video needs a hook in the first 2 seconds, while a YouTube tutorial can build up more gradually. Always mention your target platform.

If you want a specific tone — humorous, authoritative, emotional — say so explicitly. The generator responds well to tone directions like 'keep it conversational' or 'make it feel urgent and high-energy.' You can also ask for multiple versions of the same video concept to A/B test different hooks or structures before committing to production.

For longer videos, break your request into segments. Ask for the intro first, then the main body, then the outro separately. This gives you more control over each section and makes the final result feel more intentional and cohesive.

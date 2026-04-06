---
name: free-image-to-video
version: "1.0.0"
displayName: "Free Image to Video Converter — Animate Still Photos Into Dynamic Videos Instantly"
description: >
  Bring your still images to life without spending a cent. This free-image-to-video skill transforms static photos, illustrations, and graphics into fluid, engaging video content in seconds. Whether you're a content creator, small business owner, or social media manager, you can animate product shots, travel photos, or artwork into scroll-stopping videos ready for Instagram, TikTok, YouTube, and beyond — no editing experience required.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! Ready to turn your still photos into eye-catching videos? Share an image or describe what you'd like to animate, and let's create something worth watching — completely free.

**Try saying:**
- "Convert this product photo into a short looping video for my Instagram feed"
- "Animate my travel landscape photos into a 15-second video slideshow with smooth transitions"
- "Turn this portrait illustration into a cinematic video clip with a subtle zoom effect"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Turn Any Photo Into a Moving Story

Static images tell a moment. Videos tell a story. With this skill, the gap between the two disappears. Upload any still photo — a portrait, a landscape, a product flat lay, a piece of digital art — and watch it transform into a smooth, animated video clip you can share anywhere.

This isn't about slapping a Ken Burns pan onto your photo and calling it a day. The free-image-to-video skill applies intelligent motion, transitions, and timing to make your visuals feel alive and intentional. You control the mood, the pacing, and the output format so the final result actually fits your brand and platform.

Ideal for creators who want to repurpose existing photo libraries into fresh video content, marketers building ad campaigns on a tight budget, or anyone who simply wants to make their memories move. No subscriptions, no watermarks, no complicated timelines — just images in and videos out.

## Routing Your Animation Requests

When you submit a still photo for conversion, your request is parsed for motion style, duration, and output format preferences before being dispatched to the appropriate rendering pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

The free image-to-video backend leverages distributed cloud GPU clusters to process frame interpolation, motion vector generation, and video encoding entirely server-side — no local rendering required. Each submitted image passes through a multi-stage pipeline that handles upscaling, temporal smoothing, and final MP4 or GIF export automatically.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-image-to-video`
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

## Use Cases

The free-image-to-video skill fits naturally into dozens of real-world workflows. E-commerce sellers can animate product photos into short clips that perform significantly better in paid ads and organic social posts than static images alone. Photographers can package their portfolio shots into highlight reels without learning video editing software.

Event planners and wedding photographers use it to create quick recap videos from photo galleries. Teachers and educators animate diagrams or infographics into explainer clips. Bloggers and journalists convert article header images into shareable video previews for social distribution.

For small business owners with limited budgets, this skill is especially valuable — it unlocks video marketing without the cost of a videographer or a subscription to expensive editing tools. If you have a photo, you have the raw material for a video.

## Quick Start Guide

Getting started takes less than a minute. Simply provide the image you want to animate — either by uploading it directly or sharing a URL — and describe your desired output. You can specify duration, aspect ratio, motion style, and any text overlays you'd like included.

If you're converting multiple images into a slideshow video, list them in the order you want them to appear and mention any transition preferences such as fades, wipes, or cuts. The skill will assemble them into a single cohesive video file.

Once generated, your video is ready to download and post directly to any platform. No extra steps, no account creation, no hidden export fees. If the first result isn't quite right, just describe what you'd like adjusted — slower motion, different cropping, longer duration — and regenerate in seconds.

## Best Practices

Start with high-resolution images whenever possible. The cleaner and sharper your source photo, the more polished the resulting video will look. Blurry or heavily compressed images will show their flaws more obviously once motion is applied.

Think about the platform before you generate. A square 1:1 crop works well for Instagram feed posts, while a vertical 9:16 framing is essential for Reels, TikTok, and Stories. Specifying your target format upfront saves you from resizing after the fact.

For slideshows with multiple images, keep a consistent visual theme — similar lighting, color palette, or subject matter — so the video feels cohesive rather than choppy. If you're animating a single image, describe the emotion or energy you want the motion to convey, such as calm and slow versus energetic and fast, to get results that match your intent.

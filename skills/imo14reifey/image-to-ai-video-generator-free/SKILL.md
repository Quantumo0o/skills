---
name: image-to-ai-video-generator-free
version: "1.0.0"
displayName: "Image to AI Video Generator Free — Animate Your Photos Into Stunning Videos"
description: >
  Tired of static images that fail to capture attention in a scroll-happy world? The image-to-ai-video-generator-free skill transforms your still photos into dynamic, eye-catching AI-generated videos — no budget required. Upload a single image or a series of shots, and watch them come alive with smooth motion, cinematic effects, and intelligent scene transitions. Perfect for content creators, small business owners, social media managers, and anyone who wants professional-quality video without expensive software or subscriptions.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! Ready to bring your photos to life? This skill turns your still images into AI-generated videos for free — just share your image and tell me the style or motion effect you're going for, and let's create something worth watching.

**Try saying:**
- "Animate this product photo with a slow zoom-in and soft light shimmer effect for an Instagram story"
- "Turn these 5 travel photos into a cinematic slideshow video with smooth transitions and a warm color grade"
- "Create a looping animated video from my logo image with a subtle pulse and glow effect"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Turn Still Photos Into Moving Stories Instantly

Most people have folders full of great photos that never get the attention they deserve. A single image posted online gets a glance; a video stops the scroll. That gap between photo and video used to require expensive tools, editing skills, or a production team. This skill closes that gap entirely.

With the image-to-ai-video-generator-free skill, you simply provide your image — a product shot, a landscape, a portrait, a graphic — and describe the kind of video you want. The AI handles motion generation, timing, and visual flow to produce a short video clip ready for social media, presentations, or websites.

Whether you're animating a single hero image for an Instagram Reel, creating a slideshow-style video from multiple photos, or adding subtle motion to a logo for brand content, this skill adapts to your creative intent. No prior video editing experience is needed, and there's no cost barrier — making professional-looking video content genuinely accessible to everyone.

## Routing Your Animation Requests

When you upload a photo or describe a motion style, the skill parses your intent and routes your request to the appropriate AI animation pipeline — whether that's subtle Ken Burns drift, full motion synthesis, or lip-sync animation.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

Your frames are sent to a distributed GPU cloud backend that handles diffusion-based frame interpolation and temporal consistency rendering, converting static images into fluid video sequences. Processing latency depends on output resolution, frame rate, and the complexity of the motion vectors applied to your source image.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `image-to-ai-video-generator-free`
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

## Quick Start Guide

Getting started with the image-to-ai-video-generator-free skill takes less than a minute. First, have your image ready — JPEG, PNG, or a direct image URL all work well. The clearer and higher resolution your photo, the better the output quality.

Next, describe the motion or style you want. Be specific: mention camera movements like zoom, pan, or parallax; lighting effects like golden hour glow or neon pulse; mood descriptors like cinematic, dreamy, or energetic. The more context you give, the more tailored your video will be.

If you're working with multiple images for a slideshow-style video, list them in order and indicate how long each should appear on screen and what transition style you prefer between them. Once you submit your request, the skill processes your input and returns a ready-to-use video clip. From there, you can request adjustments to pacing, effects, or aspect ratio to fit your target platform.

## Use Cases

The image-to-ai-video-generator-free skill fits naturally into a wide range of creative and professional workflows. Social media managers use it to repurpose existing photo libraries into Reels, TikToks, and YouTube Shorts without reshooting content. E-commerce sellers animate product images to increase engagement on listing pages and ads, giving shoppers a better sense of dimension and detail.

Bloggers and journalists convert infographics or featured images into short explainer video clips that perform better in email newsletters and social shares. Event planners and photographers turn highlight photos into recap videos for clients — all without touching a timeline editor. Even educators use it to make visual content more engaging by animating diagrams, charts, or lesson illustrations.

For personal use, it's a creative way to animate family photos, travel memories, or artistic portraits into something shareable and emotionally resonant.

---
name: video-maker-online-free
version: "1.0.0"
displayName: "Video Maker Online Free — Create Stunning Videos Without Software or Cost"
description: >
  Turn your photos, clips, and ideas into polished videos without downloading a single app. This video-maker-online-free skill helps creators, small businesses, and social media managers build engaging content fast — from slideshow-style reels to branded promo videos. Trim clips, add text overlays, sync music, and export in multiple formats. No editing experience needed.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to your free online video creation assistant — let's turn your footage, photos, or ideas into something share-worthy today. Tell me what kind of video you're making and I'll walk you through every step.

**Try saying:**
- "I have 15 product photos and want to make a 30-second promotional video for Instagram with background music and my logo — how do I do this free online?"
- "Can you help me create a slideshow video from family vacation photos with captions and a fade transition between each image using a free online tool?"
- "I recorded a 10-minute tutorial on my phone and need to trim it down to 2 minutes, add subtitles, and export it for YouTube — what free online video maker should I use and how?"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Make Pro-Quality Videos Right From Your Browser

Creating a compelling video used to mean expensive software, a steep learning curve, and hours of frustration. This skill flips that entirely. Whether you're putting together a birthday montage, a product showcase for your Etsy shop, or a quick social post for Instagram, you can go from raw assets to a finished video without touching your desktop editor.

The video-maker-online-free approach here is built around speed and simplicity. You describe what you want — the sequence, the mood, the text, the pacing — and get actionable guidance, ready-to-use templates, and step-by-step instructions tailored to free online tools that actually deliver results.

This skill is especially useful for content creators who need volume without a production budget, marketers running lean, teachers building lesson recaps, and anyone who's stared at a blank timeline and given up. You don't need to know what a keyframe is. Just tell us what you're making.

## Routing Your Video Creation Requests

When you submit a video project — whether trimming clips, adding text overlays, or exporting in HD — your request is parsed and routed to the appropriate cloud rendering pipeline based on the operation type and output format specified.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

All video processing runs on distributed cloud servers, meaning your browser never handles the heavy encoding work — timelines, transitions, and audio sync are compiled server-side and streamed back as a preview or final export link. Supported formats include MP4, WebM, and GIF, with resolution options up to 1080p depending on your plan tier.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-maker-online-free`
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

## Common Workflows

Different video types call for different approaches. For a product showcase, start with a hook clip or bold text card in the first 3 seconds, then cycle through product images or demo footage with short descriptive captions. End with a clear call-to-action frame like 'Shop Now' or 'Link in Bio.'

For event recap videos — weddings, birthdays, corporate events — arrange clips chronologically, use a consistent transition style (simple cuts or soft fades work best), and sync major moments to the beat of your chosen track. Most free online video makers have an auto-beat-sync feature worth using.

For educational or tutorial content, record your screen or talking-head footage first, then bring it into the online editor to add chapter title cards, highlight boxes, and closed captions. Captions dramatically increase watch time and are essential for accessibility. Many free tools now auto-generate captions — always review them for accuracy before exporting.

## Troubleshooting

If your video export is taking forever or failing, the most common cause is file size. Free online video makers often cap uploads at 500MB or 2GB. Compress large video files using a free tool like HandBrake before uploading, or trim unused footage before exporting.

If your exported video looks blurry, check two things: the export resolution setting (make sure it's set to 1080p, not 480p) and the platform you're uploading to — some platforms re-compress video on upload, which can reduce quality. Exporting at the highest available bitrate helps preserve sharpness after re-compression.

Audio sync issues — where your music or voiceover drifts out of time — usually happen when you mix clips with different frame rates. Stick to one frame rate (24fps or 30fps) across all your source footage. If the problem persists, detach the audio track, delete it, and re-add it manually from the start of the timeline.

## Quick Start Guide

Getting started with a free online video maker is faster than most people expect. First, gather your assets — video clips, images, audio files, or a script. Most free online tools like Canva Video, CapCut Web, or Clipchamp accept common formats like MP4, JPG, PNG, and MP3.

Once you're in the editor, start by selecting an aspect ratio that matches your destination: 16:9 for YouTube, 9:16 for TikTok or Reels, or 1:1 for feed posts. Drag your media onto the timeline in the order you want them to appear.

Add text overlays by clicking the text tool — use short, punchy lines that appear for 2-3 seconds each. Layer in background music from the tool's free library or upload your own. When you're done, hit export and choose the highest resolution the free plan allows, typically 1080p. The whole process for a 60-second video can take under 20 minutes once you know the steps.

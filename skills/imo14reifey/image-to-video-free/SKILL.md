---
name: image-to-video-free
version: "1.0.0"
displayName: "Image to Video Free — Animate Your Photos Into Stunning Videos Instantly"
description: >
  Tired of static photos that fail to capture attention in a scroll-happy world? The image-to-video-free skill transforms your still images into dynamic, animated videos without spending a dime. Upload a single photo or a batch of images and watch them come alive with smooth motion, transitions, and cinematic flair. Perfect for social media creators, small business owners, bloggers, and anyone who wants professional-looking video content without a production budget.
metadata: {"openclaw": {"emoji": "🎞️", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! I'm here to help you turn your photos into eye-catching videos completely free — just share your images and tell me the style or mood you're going for, and let's create something worth watching.

**Try saying:**
- "Convert my 5 product photos into a 15-second Instagram Reel with smooth zoom transitions and upbeat pacing"
- "Animate my single landscape photo with a slow Ken Burns zoom-out effect for a cinematic YouTube intro"
- "Create a slideshow video from 10 wedding photos with elegant fade transitions and a 3-second display time per image"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Turn Still Moments Into Moving Stories

Still images tell a story, but videos make people feel it. The image-to-video-free skill bridges that gap by giving you a fast, accessible way to convert your photos into shareable video content — no expensive software, no steep learning curve, and no hidden costs.

Whether you have a single hero image you want to breathe life into or a whole gallery you'd like to sequence into a slideshow reel, this skill handles the heavy lifting. You describe what you want — the mood, the pacing, the style — and the skill generates a video that matches your vision. Think Ken Burns-style zooms, fade transitions, beat-matched cuts, or simple pan effects that make a flat photo feel alive.

This is built for creators who move fast. Social media managers juggling multiple platforms, Etsy sellers showcasing products, event photographers turning shoot highlights into recap reels — all of them can produce polished video output in minutes rather than hours. No timeline scrubbing, no keyframe headaches. Just describe, generate, and share.

## Routing Your Animation Requests

When you submit a photo, your request is parsed for motion style, duration, and output resolution before being dispatched to the appropriate image-to-video rendering pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

All frame interpolation and motion synthesis happens on distributed GPU clusters via the image-to-video API, so your local device handles zero heavy lifting. Keyframe extraction, temporal coherence, and mp4 encoding are all managed server-side before the animated clip is returned to you.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `image-to-video-free`
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

The image-to-video-free skill fits naturally into a wide range of real-world workflows. E-commerce sellers use it to turn product flat-lays into short promotional clips for Instagram Stories or Facebook Ads — video posts consistently outperform static images for click-through rates.

Real estate agents convert property photo galleries into walkthrough-style video tours that can be embedded on listings or shared via email without hiring a videographer. Event planners and photographers create same-day recap reels by feeding in a selection of event shots and getting a shareable highlight video within minutes.

Content creators and bloggers use it to repurpose existing photo libraries into fresh video content, extending the shelf life of work they've already done. Even educators and nonprofit communicators find value here — turning infographic images or campaign photos into compelling video narratives for presentations and social outreach.

## Quick Start Guide

Getting your first image-to-video output is straightforward. Start by gathering the images you want to use — JPG, PNG, and WebP formats all work well. The clearer and higher-resolution your source images, the better your final video will look.

Next, tell the skill how you want the video to feel. Mention the number of images, how long each should appear on screen, what kind of transitions you prefer (fades, zooms, slides), and the target platform if relevant (vertical for TikTok/Reels, horizontal for YouTube, square for feed posts).

For best results, describe the emotional tone too — 'energetic and fast-paced' versus 'calm and cinematic' will produce noticeably different outputs. Once generated, you can request tweaks like adjusting timing, swapping transition styles, or reordering the image sequence. Iterating is fast, so don't hesitate to refine.

## Troubleshooting

If your generated video feels choppy or the transitions look abrupt, the most common fix is specifying a longer display duration per image — try 3 to 5 seconds per photo instead of 1 to 2. Fast cuts work great for high-energy content but can feel jarring with portrait or landscape photography.

If the output aspect ratio doesn't match your target platform, explicitly state the format in your prompt. For example, '9:16 vertical for TikTok' or '16:9 horizontal for YouTube' will steer the output correctly from the start.

Low-resolution or heavily compressed source images can result in visible pixelation, especially when zoom effects are applied. If this happens, try using the highest-resolution versions of your photos available. If you're working with older or smaller images, request subtler motion effects like gentle pans rather than close-up zooms to minimize quality loss.

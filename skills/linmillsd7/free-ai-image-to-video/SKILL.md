---
name: free-ai-image-to-video
version: "1.0.0"
displayName: "Free AI Image to Video — Animate Still Photos Into Dynamic Video Clips"
description: >
  Tell me what you need and I'll help you bring your still images to life as captivating video content — completely free. This free-ai-image-to-video skill transforms static photos, illustrations, and artwork into smooth, animated video clips using AI-powered motion synthesis. Whether you're a content creator, marketer, or hobbyist, you can generate eye-catching reels, social clips, and presentations without expensive software or editing experience.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome! I can help you turn any still image into an animated video clip — no software downloads or editing skills needed. Drop your image description or upload details and let's create something that moves!

**Try saying:**
- "I have a product photo of a perfume bottle on a white background — can you animate it with a slow zoom and soft light sweep to use as an Instagram Reel?"
- "Turn this landscape photo of mountains at sunset into a looping video with a slow pan from left to right, suitable for a YouTube channel intro."
- "I have a portrait illustration of a fantasy character — animate it so the hair and cloak appear to flow gently in the wind for a 5-second clip."

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Turn Any Photo Into a Moving Video Instantly

Still images hold stories that motion can unlock. This skill takes the photos, illustrations, or digital artwork you already have and converts them into fluid, animated video clips that grab attention and communicate more than a static image ever could. Whether you want subtle camera drift effects, dramatic zoom-ins, or full scene animation, the process starts with a single image and ends with a shareable video.

Creators, small business owners, educators, and social media managers use this skill to stretch their existing visual assets further. A product photo becomes a scroll-stopping ad. A portrait becomes a cinematic headshot reel. A landscape snapshot becomes a moody ambient loop. You don't need to shoot new footage or hire a videographer.

The skill guides you through describing your image, choosing motion style, pacing, and output format so the final video matches your intent. It works with portraits, landscapes, illustrations, screenshots, and more — making it one of the most versatile free tools for visual storytelling available today.

## Routing Your Animation Requests

When you submit a still photo, your request is parsed for motion parameters and forwarded to the appropriate free AI image-to-video pipeline based on clip length, animation style, and output resolution.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing Backend Reference

The backend leverages distributed GPU inference nodes to run diffusion-based frame interpolation and temporal synthesis, converting static images into fluid video clips without any local rendering overhead. Free-tier jobs are queued alongside paid workloads, so processing times may vary depending on server load.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-ai-image-to-video`
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

## Common Workflows Using Free AI Image to Video

One of the most popular workflows is the product showcase loop: take a clean product photo, animate it with a slow orbit or light-sweep effect, and export it as a 5-10 second looping clip for an e-commerce page or paid social ad. This workflow alone can dramatically increase engagement without a full video shoot.

Another common use case is the event or announcement card. Start with a designed graphic — a birthday invite, a sale banner, a conference poster — and add subtle motion like floating particles, a pulsing glow, or a slow zoom. The result feels far more premium than a static image post.

Portfolio animators and digital artists frequently use this skill to create demo reels from their illustration work. A series of character illustrations animated into short clips can be stitched into a portfolio showreel that demonstrates range without requiring full animation skills.

Finally, educators and presenters use image-to-video to make slide content more engaging. Converting key diagrams or infographics into short animated clips adds visual energy to online courses, webinars, and explainer videos.

## Tips and Tricks for Better Image-to-Video Results

The quality of your output depends heavily on how you describe the motion you want. Instead of saying 'make it move,' try specifying direction, speed, and mood — for example, 'slow rightward pan with a slight zoom, cinematic feel.' The more precise your motion brief, the closer the result matches your vision.

High-contrast images with clear subjects tend to animate more convincingly than cluttered or low-resolution photos. If your image has a busy background, mention whether you want the background static or in motion — this gives the AI a clear instruction to follow.

For social media use, always specify your target aspect ratio upfront (9:16 for TikTok and Reels, 16:9 for YouTube, 1:1 for feed posts). Requesting the right format from the start saves you from cropping or reformatting afterward.

Finally, if you're looping the video — for ambient displays or website backgrounds — ask for a seamless loop explicitly. This ensures the end frame blends naturally back into the start frame without a jarring cut.

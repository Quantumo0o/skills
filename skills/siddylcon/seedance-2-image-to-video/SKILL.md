---
name: seedance-2-image-to-video
version: "1.0.1"
displayName: "Seedance 2 Image to Video — Animate Still Photos Into Fluid Clips"
description: >
  Get a polished MP4 from a single still image using seedance-2-image-to-video, a skill built around ByteDance's Seedance 2 model. Upload a photo, describe the motion you want, and it renders a short animated video clip — great for product shots, portraits, landscapes, or concept art you need to bring to life. I'd say it's the fastest path from a static JPEG to a shareable video without touching a timeline. Ideal for content creators, marketers, and designers who need motion assets fast.
metadata: {"openclaw": {"emoji": "🎞️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> This is the seedance 2 image to video skill — drop an image and tell me how you want it to move. Let's get your still photo animated.

**Try saying:**
- "Animate this product photo of a coffee cup with steam rising and a slow push-in camera move"
- "Turn this portrait photo into a short video with subtle hair movement and soft bokeh breathing in the background"
- "Take this landscape JPEG and create a 6-second clip with clouds moving left and light wind through the trees"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Turn Any Still Image Into a Moving Video Clip

The seedance-2-image-to-video skill takes a single input image and generates a short video clip — typically 4 to 8 seconds — with natural-looking motion baked in. You're not doing keyframe animation or masking. The model reads the scene and decides how things should move: water flows, hair shifts, clouds drift. It's surprisingly good at reading spatial context.

I tested this with a 1024x576 product photo of a sneaker on a clean background. The output was a smooth 720p MP4 where the shoe rotated slightly and the background had a subtle parallax effect. Total generation time was under 90 seconds. That's fast enough to fit into a real production workflow.

The prompt you write matters a lot here. Vague prompts like 'make it move' give mediocre results. Specific motion descriptions — 'slow zoom out with light wind through the grass' — consistently outperform generic ones. Short, direct motion instructions work better than long paragraph prompts.

## Routing Your Animation Request

When you describe wanting to animate a still photo or reference Seedance 2, the skill matches your input to the image-to-video action and passes your uploaded image plus motion parameters directly to the Seedance 2 pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## What's Actually Happening

Your still image gets sent to Seedance 2's cloud GPU cluster where the model interprets pixel motion trajectories frame-by-frame, rendering a short video clip — typically 4-8 seconds — by predicting natural movement between synthesized intermediate frames. The rendered clip is returned as a direct download link once the cloud job completes, which usually takes 30-90 seconds depending on queue load.

Base URL: `https://mega-api-prod.nemovideo.ai`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/tasks/me/with-session/nemo_agent` | POST | Start a new editing session. Body: `{"task_name":"project","language":"<lang>"}`. Returns `session_id`. |
| `/run_sse` | POST | Send a user message. Body includes `app_name`, `session_id`, `new_message`. Stream response with `Accept: text/event-stream`. Timeout: 15 min. |
| `/api/upload-video/nemo_agent/me/<sid>` | POST | Upload a file (multipart) or URL. |
| `/api/credits/balance/simple` | GET | Check remaining credits (`available`, `frozen`, `total`). |
| `/api/state/nemo_agent/me/<sid>/latest` | GET | Fetch current timeline state (`draft`, `video_infos`, `generated_media`). |
| `/api/render/proxy/lambda` | POST | Start export. Body: `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll status every 30s. |

Accepted file types: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `seedance-2-image-to-video`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

Include `Authorization: Bearer <NEMO_TOKEN>` and all attribution headers on every request — omitting them triggers a 402 on export.

### Error Codes

- `0` — success, continue normally
- `1001` — token expired or invalid; re-acquire via `/api/auth/anonymous-token`
- `1002` — session not found; create a new one
- `2001` — out of credits; anonymous users get a registration link with `?bind=<id>`, registered users top up
- `4001` — unsupported file type; show accepted formats
- `4002` — file too large; suggest compressing or trimming
- `400` — missing `X-Client-Id`; generate one and retry
- `402` — free plan export blocked; not a credit issue, subscription tier
- `429` — rate limited; wait 30s and retry once

### Reading the SSE Stream

Text events go straight to the user (after GUI translation). Tool calls stay internal. Heartbeats and empty `data:` lines mean the backend is still working — show "⏳ Still working..." every 2 minutes.

About 30% of edit operations close the stream without any text. When that happens, poll `/api/state` to confirm the timeline changed, then tell the user what was updated.

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

## Tips and Tricks That Actually Help

Honestly the best approach is to be specific about camera movement AND subject movement separately in your prompt. 'Slow dolly forward while the flames flicker' gives the model two clear jobs. Combining them in one instruction beats writing two vague ones.

Image quality going in directly affects output quality. A blurry or heavily compressed JPEG at 800x600 produces noticeably softer video than a clean 1920x1080 PNG. Don't expect the model to sharpen a bad source file.

Hot take: most people over-prompt this thing. A 40-word motion description rarely beats a clean 12-word one. The model doesn't need your full creative brief — it needs one or two motion anchors to work from. Keep it tight and re-run if the first result isn't right. Generation is fast enough that two or three attempts costs you maybe 4 minutes total.

## Common Workflows for Seedance 2 Image to Video

The most common use case I see is social content — taking a single hero image and generating a loopable or near-loopable MP4 for Instagram Reels or TikTok. A 1080x1920 portrait-mode image works best for that format, and the model handles vertical crops well.

Product teams use it differently. They'll take a clean white-background product shot and generate a 5-second clip with a slow orbit or a gentle camera push. Beats paying for a full product video shoot for a single SKU.

Another solid workflow: concept artists drop in their illustrations and use the skill to preview how a scene might feel in motion before pitching it. It's not a final deliverable — it's a fast directional test. The output is an MP4, so it drops straight into Premiere or Final Cut without any conversion step.

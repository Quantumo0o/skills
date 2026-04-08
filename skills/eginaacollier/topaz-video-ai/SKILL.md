---
name: topaz-video-ai
version: "1.0.0"
displayName: "Topaz Video AI Assistant — Upscale, Enhance & Restore Footage with Precision"
description: >
  Turn shaky, blurry, or low-resolution footage into cinematic-quality video using topaz-video-ai. This skill helps you navigate Topaz Video AI's powerful enhancement tools — from AI upscaling and motion deblur to frame interpolation and noise reduction. Whether you're restoring archival clips, upscaling home movies to 4K, or prepping footage for professional delivery, this assistant guides every step of the process for filmmakers, editors, and content creators.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome — let's get your footage looking its absolute best using Topaz Video AI's enhancement tools. Tell me what you're working with and what you want to achieve, and I'll walk you through exactly how to do it.

**Try saying:**
- "I have old VHS home videos I want to upscale to 1080p — which Topaz Video AI model should I use and what settings work best for that kind of footage?"
- "My drone footage looks slightly soft and has some motion blur. How do I use Topaz Video AI to sharpen it without creating artifacts?"
- "I want to convert a 24fps cinematic clip to 60fps for smooth slow motion. Walk me through frame interpolation settings in Topaz Video AI."

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Restore, Upscale, and Sharpen Any Video with AI

Topaz Video AI is one of the most powerful desktop tools available for video enhancement — but its depth of models, settings, and export options can feel overwhelming without guidance. This skill acts as your hands-on assistant for getting the most out of every feature Topaz Video AI offers.

Whether you're working with decades-old VHS recordings, drone footage that came out softer than expected, or web-sourced clips you need at broadcast quality, this assistant helps you choose the right AI model, dial in enhancement settings, and understand what each parameter actually does to your footage.

From selecting between Proteus, Iris, and Themis models to understanding how frame interpolation affects motion cadence, this skill translates Topaz Video AI's technical language into actionable decisions. You'll spend less time guessing at sliders and more time delivering polished, high-quality video.

## Routing Upscale and Enhancement Requests

When you describe your footage goal — whether that's recovering detail from a noisy 1080p clip, pushing SD archival footage to 4K, or sharpening motion blur with DAIN or Apollo frame interpolation — your request is parsed and routed to the appropriate Topaz Video AI model pipeline automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing Backend Reference

Topaz Video AI processing runs through a cloud-connected backend that mirrors the model stack used in the desktop application, including Proteus, Iris, Artemis, and Gaia enhancement models alongside DAIN, Apollo, and RIFE for frame interpolation. Jobs are queued, processed per-clip, and returned with model metadata so you always know which enhancement pass was applied.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `topaz-video-ai`
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

## Tips and Tricks

One of the most underused features in Topaz Video AI is the preview comparison tool — always run a short clip preview before committing to a full export. This saves hours on long files and lets you fine-tune settings like the Recover Details and Sharpen sliders before processing.

When working with heavily compressed footage (think old YouTube downloads or phone videos), the Proteus model with manual parameter control tends to outperform the auto-detection defaults. Nudge the Dehalo and Anti-Alias settings slightly above zero to clean up compression artifacts before upscaling.

For archival or film grain footage, avoid over-sharpening. Topaz Video AI's noise reduction can strip away authentic grain that gives footage its character. Use the 'Relative to Auto' mode and pull back on the noise reduction strength to preserve texture while still cleaning up digital noise.

## Common Workflows

The most common workflow in Topaz Video AI is SD-to-HD upscaling — taking standard definition footage (480p or 576p) and bringing it up to 1080p or 4K. For this, the Iris model performs best on faces and human subjects, while Proteus handles mixed or landscape-heavy content more reliably.

A second popular workflow is frame rate conversion for smooth playback. Editors often receive 24fps footage they need at 60fps for web or sports use. Topaz Video AI's frame interpolation engine generates in-between frames using motion estimation, and selecting 'Apollo' as the interpolation model gives the cleanest results for fast-moving subjects.

Restoration workflows — dealing with VHS, film scans, or heavily degraded footage — typically combine multiple enhancement passes: first noise reduction, then upscaling, then a final sharpening pass. Chaining these as separate exports rather than stacking all enhancements in one pass usually produces cleaner results with fewer compounding artifacts.

## Integration Guide

Topaz Video AI works as a standalone desktop application but integrates smoothly into professional post-production pipelines. It accepts virtually all common video formats as input, including ProRes, H.264, H.265, and even image sequences, making it easy to slot into both DaVinci Resolve and Premiere Pro workflows.

A common integration approach is to export a lossless or high-bitrate intermediate from your NLE, process it through Topaz Video AI, then reimport the enhanced file for final color grading and delivery. This preserves quality at every stage and avoids double-compression artifacts.

For batch processing large projects, Topaz Video AI's queue system lets you line up multiple clips with different settings and process them overnight. Pair this with a consistent naming convention and output folder structure to keep enhanced assets organized and easy to locate when you return to your editing timeline.

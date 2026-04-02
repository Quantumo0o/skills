---
name: video-compressor-ai
version: "1.0.0"
displayName: "Video Compressor AI — Shrink File Sizes Without Sacrificing Visual Quality"
description: >
  Turn bulky video files into lean, shareable assets without the quality loss that plagues traditional compression tools. video-compressor-ai analyzes your footage frame-by-frame to apply intelligent bitrate optimization, format conversion, and resolution scaling — all in a conversational interface. Built for content creators, marketers, and developers who need fast turnaround on web-ready, mobile-friendly, or archive-quality video output.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! I'm your Video Compressor AI — ready to help you reduce file sizes, optimize formats, and prep your videos for any platform or storage need. Tell me about your video and what you're trying to achieve, and let's compress it the smart way.

**Try saying:**
- "Compress this 2GB wedding video to under 500MB for sharing via email without making it look blurry"
- "Convert my MP4 file to H.265 format and reduce the file size by at least 60% while keeping 1080p resolution"
- "I have 200 training videos taking up 300GB — what compression settings should I use to cut storage in half without losing readability of on-screen text?"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Compress Smarter: AI That Reads Your Footage

Most video compression tools treat every file the same — they apply a blanket setting and hope for the best. Video Compressor AI takes a different approach. By understanding the content of your video — motion complexity, scene transitions, color depth, and audio layers — it recommends and applies compression strategies tailored to what's actually in your footage.

Whether you're trimming a 4K drone reel down for Instagram, reducing a product demo for faster web loading, or archiving a library of training videos without blowing your storage budget, this skill adapts to your goal. You describe what you need in plain language — target file size, platform destination, acceptable quality trade-offs — and the AI handles the technical decisions behind the scenes.

No more guessing between H.264 and H.265, no more trial-and-error with CRF values, and no more re-exporting the same clip five times. Video Compressor AI brings precision compression into a workflow that actually fits how creators and teams operate day-to-day.

## Compression Request Routing Logic

When you submit a video, your request is parsed for codec preference, target bitrate, resolution constraints, and container format before being dispatched to the optimal processing node.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Encoding Backend Reference

Video Compressor AI routes encoded workloads through a distributed transcoding cluster that applies perceptual quality metrics — including VMAF and SSIM scoring — to preserve visual fidelity while aggressively reducing file size. Each job runs in an isolated encoding pipeline supporting H.264, H.265/HEVC, AV1, and VP9 output targets.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-compressor-ai`
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

Always start with your original, uncompressed source file. Compressing an already-compressed video compounds quality loss in ways that even the best AI settings cannot fully recover from. If you've lost the original, mention this upfront so the AI can adjust its approach to minimize generational degradation.

Be specific about your destination. A video compressed for a 4K TV screen needs a very different profile than one destined for a mobile app thumbnail preview. The more context you give — device type, viewing environment, bandwidth constraints — the more accurate the compression recommendation will be.

For long-form content like webinars or documentaries, consider asking the AI about scene-based compression, where static talking-head segments get higher compression rates than fast-action sequences. This hybrid approach can yield 30–50% better file size reduction compared to flat compression across the whole file.

Finally, always request a quality checkpoint before finalizing batch jobs. Ask the AI to flag which settings carry the highest risk of visible degradation so you can review those files manually before delivery.

## Quick Start Guide

Getting started with Video Compressor AI is straightforward — no encoding knowledge required. Begin by describing your video: its current format, resolution, duration, and file size if known. Then tell the AI your end goal — whether that's hitting a specific file size, meeting a platform's upload limit (like YouTube, TikTok, or LinkedIn), or simply reducing storage footprint.

The AI will ask clarifying questions if needed — for example, whether audio quality matters as much as video, or whether you need the output in a specific container format like MP4, MOV, or WebM. Once it has enough context, it will generate a recommended compression profile with clear reasoning behind each setting.

For batch compression needs, describe your folder structure or file naming convention and the AI will suggest a consistent compression strategy you can apply across all files. You can also request a comparison — asking the AI to outline what you'd gain and lose at different compression levels before committing to a final export setting.

## Use Cases

Video Compressor AI serves a wide range of real-world scenarios across industries and workflows. Social media managers use it to hit platform-specific file size caps — TikTok's 287MB limit or Instagram's 650MB ceiling — without re-shooting or over-cropping content. The AI knows the sweet spots for each platform and compresses accordingly.

E-learning developers rely on it to shrink course video libraries before uploading to LMS platforms like Teachable or Moodle, where storage costs scale with file size. By compressing lecture recordings intelligently, text and slides remain crisp while overall file size drops dramatically.

Filmmakers and video editors use it during client delivery — sending proxy-quality previews for approval before handing over full-resolution masters. And for businesses running video-heavy websites, the AI helps optimize autoplay background videos and product demos to reduce page load times without introducing compression artifacts that would undermine brand perception.

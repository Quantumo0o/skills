---
name: ai-video-editor-online-free
version: "1.0.0"
displayName: "AI Video Editor Online Free — Edit, Trim & Enhance Videos Without Software"
description: >
  Tired of paying for bloated video editing software just to cut a clip or add a caption? The ai-video-editor-online-free skill lets you describe exactly what you want done to your video — trim, caption, reformat, color-correct, or restructure — and get actionable editing instructions, scripts, or automated workflows instantly. Built for creators, marketers, educators, and small business owners who need polished results without the learning curve or subscription fees.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Drop a description of your video and the edit you need — I'll give you exact steps using free online tools. No video file? Just describe the format, length, and goal and I'll build a plan from scratch.

**Try saying:**
- "I have a 12-minute interview video and I need to cut it down to a 90-second highlight reel for Instagram. What's the best free tool to use and how should I approach the edit?"
- "Can you help me add auto-captions to a vertical video I made for TikTok? I want the text to pop and be readable on mobile without paying for a subscription."
- "I recorded a product demo in landscape mode but I need it in 9:16 for YouTube Shorts. How do I reformat it online for free without losing the important parts of the frame?"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Edit Any Video With Just Your Words

Most people don't need a film studio — they need a fast, smart way to turn raw footage into something worth watching. This skill is built around that exact reality. Whether you're working with a phone clip, a screen recording, a webinar export, or a social media video, you can describe what needs to change and get precise, step-by-step editing guidance without ever opening a complicated timeline.

The ai-video-editor-online-free skill bridges the gap between what you have and what you need. Tell it to cut the first 10 seconds, add captions in a specific style, reformat a landscape video for TikTok, or suggest a pacing fix for a slow intro — and it responds with clear, executable instructions tailored to free browser-based tools like CapCut Online, Clipchamp, or Canva Video.

This is especially useful for solo creators, nonprofit teams, and small business owners who can't justify a monthly Adobe subscription but still need professional-looking output. No rendering queues, no watermark negotiations, no tutorials required — just describe your goal and start editing smarter.

## Routing Edits to the Right Engine

When you submit a trim, color grade, subtitle burn, or AI enhancement request, ClawHub parses your prompt and routes it to the matching cloud-based processing pipeline — whether that's the timeline editor, the upscaler, or the auto-caption module.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

All video operations run on serverless GPU nodes in the backend, meaning your browser never handles the heavy encoding — frame extraction, AI inference, and final render happen remotely and stream the output file back to your session. Supported formats include MP4, MOV, and WebM, with export resolutions up to 4K depending on your plan tier.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-video-editor-online-free`
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

The ai-video-editor-online-free skill covers a surprisingly wide range of real-world editing needs. Content creators use it to repurpose long YouTube videos into short-form clips for TikTok and Reels, getting a cut-down script and timing guide alongside the technical steps. Educators and coaches use it to trim recorded lessons, add chapter markers, and export clean MP4s for course platforms — all without paying for screen recording software.

Small business owners rely on it to turn raw product footage into polished promotional clips with text overlays and branded end screens, using only free tools. Nonprofit teams use it to prepare interview footage for grant applications or fundraising campaigns on a zero-dollar budget.

Event organizers use the skill to edit highlight reels from multi-hour recordings, identifying the best moments to keep based on a simple description of the event. Whether the end goal is a 15-second ad, a 3-minute explainer, or a 30-second social proof clip, this skill helps you get there without expensive software or a video production background.

## Integration Guide

This skill works seamlessly alongside the most popular free online video editors — no downloads, accounts, or API keys required on your end. When you describe your editing task, the skill will recommend the best free browser-based platform for that specific job: CapCut Online for quick cuts and effects, Clipchamp for Windows users who want timeline control, Canva Video for template-driven social content, or DaVinci Resolve Free for more advanced color and audio work.

To get the most out of the skill, start by describing your video: its length, format (horizontal, vertical, square), the platform it's destined for (YouTube, Instagram, LinkedIn, etc.), and the specific problem you're trying to solve. The more context you give, the more targeted the editing plan will be.

For recurring workflows — like weekly podcast clips or product demo videos — you can ask the skill to generate a repeatable editing checklist tailored to your format. This turns a one-time answer into a reusable production system you can follow every time without starting from scratch.

## Troubleshooting

If the editing steps provided don't match what you're seeing in your chosen tool, it's usually because free online editors update their interfaces frequently. In that case, tell the skill which tool you're using and describe what you see on screen — it can adapt the instructions to your specific version.

For videos that are too large to upload to browser-based editors (typically over 500MB), the skill can suggest free compression steps using HandBrake or Clideo before you begin editing. If your video has audio sync issues after trimming, ask for a specific fix — this is a common problem with certain export formats and there's a reliable workaround for each tool.

If captions are misaligned or auto-generated text is inaccurate, describe the problem and the skill will walk you through manual correction workflows or recommend a free alternative captioning tool with better accuracy for your language or accent.

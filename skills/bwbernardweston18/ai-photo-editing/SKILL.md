---
name: ai-photo-editing
version: "1.0.0"
displayName: "AI Photo Editing — Transform, Enhance & Retouch Photos Instantly"
description: >
  Turn ordinary snapshots into stunning visuals with intelligent ai-photo-editing that handles retouching, color grading, background removal, and object cleanup in seconds. Whether you're a photographer refining a portfolio shoot, a small business owner polishing product images, or a content creator batch-editing social media posts, this skill adapts to your style and intent — no Photoshop expertise required. Describe what you want, share your image, and get back a precise editing plan or ready-to-apply instructions.
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to your AI photo editing assistant — built to help you retouch, enhance, and transform any image with precision and speed. Share your photo or describe your editing goal, and let's get started right now.

**Try saying:**
- "I have a portrait shot outdoors but the background is messy — how do I remove it cleanly and replace it with a soft blur in Photoshop?"
- "My product photos all look slightly different in color temperature. How do I batch-match them to a consistent warm tone in Lightroom?"
- "I took a beach photo at golden hour but the sky is blown out and the foreground is too dark — what's the best way to fix the exposure balance?"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Edit Smarter: Let AI Handle the Heavy Lifting

Photo editing used to mean hours hunched over sliders, masking layers, and second-guessing color choices. This skill changes that by putting an intelligent editing co-pilot in your corner — one that understands what a photo needs before you've finished describing it.

Whether you're correcting exposure on a backlit portrait, swapping out a distracting background, removing a photobomber from a family shot, or matching the color tone across an entire product catalog, the skill breaks down each task into clear, actionable steps. It works with your tools — Lightroom, Photoshop, Canva, Snapseed, or any editor you already use — by giving you the exact settings, masks, and techniques to apply.

This isn't a one-size-fits-all filter. The approach is tailored to your specific image, your intended use case, and your skill level. Beginners get plain-language walkthroughs. Experienced editors get precise technical parameters. The result is faster edits, fewer do-overs, and photos that actually look the way you imagined them.

## Routing Your Edit Requests

Each prompt you send — whether it's background removal, skin retouching, style transfer, or upscaling — is parsed and routed to the most capable AI model for that specific editing task.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

All image transformations run through a distributed cloud backend that handles diffusion-based edits, non-destructive masking, and pixel-level enhancement pipelines without touching your local hardware. Raw image data is processed in isolated compute sessions and purged immediately after your edited output is delivered.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-photo-editing`
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

**Portrait Retouching:** The most requested workflow — skin smoothing, blemish removal, eye brightening, and hair detail recovery. Describe the portrait style you're going for (natural, editorial, commercial) and get a layered approach that avoids the over-processed look.

**Product Photography Cleanup:** E-commerce images need consistency and clarity. This workflow covers background removal, shadow creation, color accuracy correction, and resizing for platform specs like Amazon, Shopify, or Etsy.

**Landscape & Travel Color Grading:** Match the mood of a location to your edit. Whether you want moody desaturated tones, vibrant travel-blog colors, or a cinematic flat look, get a full preset-style breakdown you can apply in Lightroom or Capture One.

**Social Media Batch Editing:** When you have 30 photos from the same shoot, consistency matters. This workflow helps you define a base edit and apply it efficiently across your set, with notes on which images need individual adjustments.

## Quick Start Guide

**Step 1 — Share Your Image or Describe It:** You can paste in a photo, link to one, or simply describe the scene, the problem, and your editing goal. The more context you give — lighting conditions, intended platform, editing software — the more precise the guidance.

**Step 2 — Get Your Editing Plan:** You'll receive a structured breakdown: what to fix first, which tools or adjustments to use, suggested values for sliders or settings, and any layer or masking techniques needed.

**Step 3 — Ask Follow-Up Questions:** Not happy with how a step turned out? Describe what went wrong and get a revised approach. This is an iterative process — you're not locked into the first recommendation.

**Step 4 — Apply & Export:** Once your edits are dialed in, get export settings optimized for your use case — web compression, print resolution, social media cropping ratios, or file format conversion.

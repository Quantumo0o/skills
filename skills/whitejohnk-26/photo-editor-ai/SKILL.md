---
name: photo-editor-ai
version: "1.0.0"
displayName: "Photo Editor AI — Smart Image Editing, Retouching & Enhancement Tools"
description: >
  Tell me what you need and I'll transform your photos into polished, professional images in seconds. photo-editor-ai handles everything from background removal and color correction to portrait retouching and creative filters. Whether you're a content creator fixing product shots, a photographer batch-editing portraits, or someone who just wants their vacation photos to look stunning — describe your edit and get precise, actionable results without touching complex software.
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to Photo Editor AI — your creative partner for retouching, enhancing, and transforming any image into exactly what you envisioned. Drop your photo description or editing request below and let's get started!

**Try saying:**
- "I have a portrait with harsh shadows under the eyes — how do I soften them without making the skin look fake?"
- "Remove the cluttered background from my product photo and replace it with a clean white studio look"
- "My sunset photo looks washed out and flat — help me make the colors vibrant and the sky dramatic without overdoing it"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Edit Smarter, Not Harder — AI Photo Magic

Photo editing used to mean hours hunched over sliders, wrestling with layer masks and color curves. Photo Editor AI changes that entirely. Describe what you want — sharper details, a different mood, a cleaner background — and get step-by-step guidance or direct edits that match your creative vision without the learning curve.

This skill is built for real editing scenarios: fixing overexposed shots from a birthday party, removing distracting objects from landscape photos, smoothing skin tones for a professional headshot, or giving an entire product catalog a consistent look. It understands context, not just commands.

Whether you're working with RAW files, JPEGs, or screenshots, Photo Editor AI adapts to your workflow. It suggests the right tools for your specific situation, explains what each adjustment does, and helps you develop an editing eye over time — so every session makes you a better editor, not just a faster one.

## Routing Edits to the Right Tool

Each request — whether it's a background removal, skin retouching, color grading, or upscaling — is parsed by intent and automatically dispatched to the appropriate processing pipeline within Photo Editor AI.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

Photo Editor AI runs on a distributed cloud rendering backend that handles non-destructive edits, layer compositing, and AI model inference in real time. All image data is processed via encrypted API calls and returned as high-resolution output without storing originals beyond your active session.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `photo-editor-ai`
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

## Performance Notes

Photo Editor AI performs best when you provide context about your end goal — print, web, social media, or e-commerce. Each destination has different resolution, color profile, and compression requirements that affect which edits to prioritize.

For high-resolution RAW files, describe your editing software (Lightroom, Photoshop, Capture One, GIMP) so recommendations use the correct tools and terminology. Generic advice rarely translates cleanly between applications.

Batch editing large catalogs works well when you establish a base preset or adjustment recipe first. Ask Photo Editor AI to help you define a consistent look for a shoot, then apply variations per image — this dramatically reduces per-photo editing time while keeping the series cohesive.

## Troubleshooting

If your edits aren't turning out as expected, the most common culprit is a vague description. Instead of saying 'make it look better,' try specifying: 'increase contrast slightly, warm up the shadows, and sharpen the subject's eyes.' The more precise your input, the more targeted the output.

For background removal issues — especially with fine details like hair or fur — mention the subject type upfront. Removing a person from a busy street scene requires different masking guidance than isolating a product on a shelf.

If color corrections look inconsistent across a batch of photos, check whether your source images have mixed white balance settings. Photo Editor AI can guide you through normalizing white balance before applying any global adjustments, which saves significant cleanup time later.

## Common Workflows

The most frequently used Photo Editor AI workflow is the portrait retouch pipeline: start with exposure and white balance correction, move to skin smoothing and blemish removal, then finish with eye enhancement and a subtle vignette. Describe your subject and lighting conditions upfront for the most accurate sequence.

For e-commerce product photography, the standard workflow covers background isolation, shadow creation or removal, color accuracy correction, and output sizing for platform-specific requirements like Amazon or Shopify.

Creative editing workflows — cinematic grades, film emulation, moody landscapes — benefit from describing a reference image or mood you're chasing. Mention color temperatures, contrast styles, and any specific era or aesthetic (e.g., '90s film grain, faded highlights') so Photo Editor AI can map that vision to concrete adjustments in your editing tool of choice.

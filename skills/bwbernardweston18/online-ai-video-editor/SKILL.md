---
name: online-ai-video-editor
version: "1.0.0"
displayName: "Online AI Video Editor — Edit, Enhance & Export Videos Instantly with AI"
description: >
  Tell me what you need and I'll help you edit, transform, and polish your videos using AI — no software downloads required. This online-ai-video-editor skill handles everything from trimming and captioning to scene transitions and format conversion. Whether you're a content creator, marketer, or small business owner, describe your footage goals and get step-by-step guidance or direct editing instructions tailored to your platform and audience.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to your AI-powered online video editor — describe your footage, your goal, and the platform you're editing for, and I'll get your video ready to publish. What are we working on today?

**Try saying:**
- "Trim my video to 60 seconds"
- "Add captions to this clip"
- "Convert landscape to vertical format"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Edit Any Video Online Without Installing Anything

Creating polished video content used to mean expensive software, steep learning curves, and hours of manual work. This skill changes that entirely. Describe your raw footage, your target platform, and the style you're going for — and get precise, actionable editing guidance powered by AI that understands pacing, storytelling, and visual impact.

Whether you're cutting down a 10-minute recording into a punchy 60-second reel, adding auto-generated captions for accessibility, or repurposing a landscape video into vertical format for TikTok or Instagram Stories, this skill walks you through every step or handles the logic for you.

The online AI video editor approach here is built around real creator workflows — not abstract theory. You'll get specific instructions, suggested cuts, caption text, transition recommendations, and export settings that match your exact use case. From YouTube vlogs to product demos to social media clips, this skill adapts to what you're actually making.

## Smart Request Routing Engine

Every edit command — whether trimming timelines, applying AI upscaling, generating captions, or exporting renders — is parsed by the intent layer and routed to the matching processing pipeline instantly.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

The backend leverages distributed GPU clusters to handle frame-by-frame AI inference, real-time transcoding, and multi-format export jobs without local hardware dependencies. All video assets are processed in isolated cloud sessions, ensuring render fidelity and pipeline stability across concurrent workloads.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `online-ai-video-editor`
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

## Troubleshooting Common Online AI Video Editing Issues

If your exported video looks lower quality than expected, the most common cause is incorrect resolution or bitrate settings during export. When asking the AI for export guidance, always specify your destination platform — YouTube, Instagram, TikTok, and LinkedIn each have different optimal specs.

Caption sync issues usually happen when the source audio has background noise or overlapping speakers. If the AI-generated captions are misaligned, ask the skill to provide a manual timestamp correction guide, or request a noise-reduction step before caption generation.

Aspect ratio cropping problems — where important content gets cut off during format conversion — can be fixed by specifying your 'safe zone' content position. Tell the AI where the main subject sits in frame (center, left-third, etc.) so it can recommend the right crop anchor point.

If an online tool is timing out on large files, ask the skill to suggest a compression-first workflow: reduce file size before editing, then re-export at full quality. This prevents processing failures on browser-based editors with file size limits.

## Tips and Tricks for Getting the Most from Your Online AI Video Editor

When describing your footage to the AI, be specific about duration, content type, and target platform — a 'talking head video for YouTube' and a 'product clip for TikTok' need completely different pacing, aspect ratios, and caption styles. The more context you give, the sharper the output.

For captions, always request timing-synced text rather than static overlays if your platform supports it. Auto-captions generated through AI tools tend to drift on fast speakers — ask the skill to flag segments where manual review is recommended.

If you're repurposing long-form content into shorts, ask for a 'highlight extraction' approach: tell the AI the core message you want viewers to take away, and it will suggest the strongest 20–30 second segments to cut around that theme.

Batch processing tip: if you have multiple clips with the same edit requirements (same intro, same caption style, same export format), describe the template once and ask for a repeatable workflow — this saves significant time across a content series.

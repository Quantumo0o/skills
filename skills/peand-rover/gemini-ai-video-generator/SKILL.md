---
name: gemini-ai-video-generator
version: "1.0.0"
displayName: "Gemini AI Video Generator — Describe It, Watch It Come to Life"
description: >
  Drop a video and describe what you want — the gemini-ai-video-generator skill uses Google's Gemini AI to analyze your footage and generate new scenes, summaries, captions, or transformed clips based on your plain-language instructions. Works with mp4, mov, avi, webm, and mkv files. Perfect for content creators, marketers, and educators who want AI-powered video generation without touching a timeline.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to let Gemini AI do the creative work? Upload your video and tell me what you want to generate — a highlight reel, scene description, caption track, or something entirely new. Let's get started.

**Try saying:**
- "Here's a 10-minute product demo video — generate a 60-second highlight reel focusing on the key features shown"
- "Analyze this lecture recording and write a structured summary with timestamps for each major topic covered"
- "Watch this travel footage and generate a narration script I can record as a voiceover"

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Turn Your Words Into Video With Gemini AI

The Gemini AI Video Generator skill brings Google's multimodal Gemini model directly into your video workflow. Instead of manually cutting, scripting, or re-shooting, you simply upload your video and tell the skill what you want — in plain English. Gemini reads both the visual content and your instructions together, then generates output that actually understands what's on screen.

This skill is built for people who have video and a vision but don't want to spend hours in editing software. Whether you're a solo creator repurposing long-form content into short clips, a marketing team generating product highlight reels, or an educator turning lecture recordings into structured summaries, this skill handles the heavy lifting.

You're not limited to trimming or adding filters. Gemini AI Video Generator can describe what's happening in a scene, suggest narrative structure, generate spoken-word scripts based on visual cues, or produce entirely new content framed around your uploaded footage. It's a fundamentally different kind of video tool — one that listens before it creates.

## Prompt Routing and Generation Flow

When you describe a scene, your natural-language prompt is parsed, enriched with cinematic parameters, and dispatched directly to the Gemini video synthesis pipeline for frame-by-frame generation.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo Backend Reference

ClawHub routes all video generation requests through the NemoVideo API, which handles Gemini model orchestration, render queuing, and secure video delivery. NemoVideo manages diffusion sampling, temporal coherence, and output encoding so your clips stay smooth and consistent across every generation.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `gemini-ai-video-generator`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=gemini-ai-video-generator&skill_version=1.0.0&skill_source=<platform>`

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
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up at nemovideo.ai" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register at nemovideo.ai to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## FAQ

**What video formats does Gemini AI Video Generator support?** You can upload mp4, mov, avi, webm, and mkv files. Mp4 is the most reliably processed format across all generation task types.

**Can it generate entirely new video footage?** The skill generates text-based outputs — scripts, descriptions, summaries, captions, and structured content — derived from your uploaded video. It does not render new video frames or visual animations.

**Does it understand spoken audio in the video?** Yes. Gemini processes both the visual content and any audible speech in your video, which means it can cross-reference what's being said with what's on screen for more accurate generation.

**What if my video has no dialogue?** No problem — Gemini AI Video Generator analyzes visual cues, movement, scene transitions, and on-screen text independently. Silent product demos, tutorials, and b-roll footage all work well with descriptive or script-generation prompts.

## Tips and Tricks

Be specific in your prompt — Gemini AI Video Generator responds much better to 'generate a 3-sentence product description focusing on the unboxing moment at the start' than to 'summarize this video.' The more context you give about your intended audience or output format, the sharper the results.

If you're generating captions or subtitles, mention the tone you want (formal, casual, punchy) and any terminology specific to your industry. Gemini will adapt its language accordingly rather than defaulting to generic phrasing.

For content repurposing workflows, try uploading the same video with different prompts — one for a short-form social caption, one for a blog summary, one for an email teaser. You'll get distinct outputs tailored to each format without re-editing the source file.

When generating scripts or voiceovers, ask Gemini to match the pacing of the original footage. This produces scripts that actually fit the visual rhythm rather than running long or cutting short.

## Performance Notes

Gemini AI Video Generator performs best on videos under 10 minutes in length, where the model can maintain full visual context throughout the clip. Longer videos may be processed in segments, which can occasionally affect continuity in generated outputs like scripts or summaries.

File format matters less than resolution and clarity — mp4 and webm files with clear audio tracks tend to produce the most accurate scene analysis and generation results. Heavily compressed or low-light footage may result in less precise visual descriptions.

Generation time scales with video length and task complexity. A simple scene description on a 2-minute clip returns quickly, while generating a full narration script for a 15-minute video will take noticeably longer. Plan accordingly if you're working with batch content.

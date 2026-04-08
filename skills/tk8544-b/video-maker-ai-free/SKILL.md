---
name: video-maker-ai-free
version: "1.0.0"
displayName: "Video Maker AI Free — Create Stunning Videos from Text, Images & Ideas"
description: >
  Drop a script, a handful of images, or just a rough idea — and watch video-maker-ai-free turn it into a polished, shareable video in minutes. This skill handles scene structuring, caption generation, pacing suggestions, and visual storytelling so you don't need editing software or a production budget. Perfect for content creators, small business owners, educators, and social media managers who want professional-looking results without the steep learning curve or cost.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome! Video Maker AI Free is here to help you create compelling videos from scripts, images, or plain ideas — no editing skills required. Tell me what kind of video you want to make and let's get started right now!

**Try saying:**
- "Write a script for my product video"
- "Turn my blog into a video"
- "Create a TikTok storyboard now"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Turn Raw Ideas Into Polished Videos Instantly

Most people have a story worth telling but no easy way to tell it visually. Video Maker AI Free bridges that gap by taking whatever you have — a topic, a script draft, a product description, or a set of images — and helping you shape it into a structured, engaging video concept ready for production or direct publishing.

This skill focuses on the creative and structural work that usually slows people down: writing scene-by-scene narratives, generating voiceover-ready scripts, suggesting B-roll descriptions, crafting captions, and recommending visual pacing. Whether you're building a 60-second Instagram Reel, a YouTube explainer, or a product demo, the output is tailored to your platform and audience.

You don't need any prior video editing experience. Just describe what you want to communicate, who you're speaking to, and where the video will live. Video Maker AI Free handles the creative heavy lifting so you can focus on hitting publish.

## Routing Your Video Requests

When you describe your video concept — whether it's a text prompt, uploaded image, or creative idea — Video Maker AI Free parses your intent and routes it to the matching generation pipeline: text-to-video, image-to-video, or storyboard assembly.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering Backend Reference

Video Maker AI Free runs on a distributed cloud rendering backend that handles frame synthesis, scene transitions, and audio-visual sync without touching your local hardware. All generation jobs are queued, processed, and delivered via secure API endpoints tied to your active session token.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-maker-ai-free`
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

## FAQ — Video Maker AI Free

**Do I need to upload actual video footage to use this skill?** No. Video Maker AI Free works entirely with text, ideas, and image descriptions. It generates scripts, storyboards, scene breakdowns, and captions that you can then use with any video tool or platform of your choice.

**What types of videos can I create?** You can build concepts for social media Reels and TikToks, YouTube tutorials and explainers, product demos, real estate walkthroughs, educational content, event recaps, and more. Just tell the skill your goal and target platform.

**Can it match a specific tone or brand voice?** Yes. Share a few sentences about your brand personality — whether that's professional, playful, minimal, or bold — and the skill will adapt the script language, caption style, and scene pacing accordingly.

**Is there a video length limit?** No hard limit. Whether you need a 15-second ad or a 10-minute tutorial, just specify the duration and the skill will structure the content to fit naturally within that time frame.

## Quick Start Guide — Your First Video in 5 Steps

**Step 1 — Define your goal.** Tell Video Maker AI Free what the video is for: a product launch, a tutorial, a social post, or a brand story. The clearer your intent, the sharper the output.

**Step 2 — Describe your audience.** Who will watch this? A first-time customer, a professional audience, or casual social media scrollers? This shapes tone, pacing, and vocabulary throughout the script.

**Step 3 — Share your raw material.** Paste in a blog post, product description, bullet points, or just a topic sentence. If you have image ideas or existing footage descriptions, include those too.

**Step 4 — Specify the platform and length.** Instagram Reels, YouTube Shorts, LinkedIn, TikTok, and standard YouTube all have different ideal formats. Mention your target platform and desired video length so the structure fits perfectly.

**Step 5 — Review and iterate.** Get your scene breakdown, voiceover script, and captions back instantly. Ask for revisions, a different tone, a shorter version, or alternate hooks until it feels exactly right.

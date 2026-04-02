---
name: free-video-generation
version: "1.0.0"
displayName: "Free Video Generation — Create Stunning Videos from Text & Ideas Instantly"
description: >
  Drop a concept, script, or simple idea and watch it transform into a fully generated video — no cost, no complicated setup. This free-video-generation skill lets you produce short clips, social content, explainer videos, and creative reels just by describing what you want. Ideal for creators, marketers, educators, and entrepreneurs who need video content fast without expensive tools or subscriptions.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome! You're one step away from turning your ideas into real video content — completely free. Describe your concept, share a script, or tell me what kind of video you need, and let's start creating right now.

**Try saying:**
- "Generate a product promo video"
- "Create explainer video from script"
- "Make a short social media clip"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Turn Any Idea Into a Video, Completely Free

Imagine describing a product launch, a tutorial concept, or a fun social clip — and getting a ready-to-share video back in moments. That's exactly what this skill is built for. Free video generation removes the barrier between your ideas and polished video content, letting you focus on creativity rather than software complexity.

Whether you're a solo creator building a YouTube channel, a small business owner promoting a service, or a student working on a project, this skill adapts to your needs. You don't need video editing experience, a production budget, or hours of free time. Just describe your vision — the tone, the subject, the style — and the generation process handles the rest.

From animated explainers to product showcases to short-form social content, the range of video types you can produce is broad. This skill is designed to make video creation accessible to everyone, not just those with professional tools or technical skills.

## Routing Your Video Requests

When you submit a text prompt or creative brief, ClawHub parses your intent and routes it to the optimal free video generation engine based on style, duration, and rendering complexity.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

Free video generation runs on a distributed cloud rendering backend that queues your prompt, synthesizes frames using diffusion-based models, and streams the finished output back to your session. Processing times vary with queue depth and clip length, typically resolving within 30–90 seconds.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-video-generation`
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

## Common Workflows for Free Video Generation

Most users start with one of three approaches: a written script they want visualized, a topic they want explained in video form, or a mood and style they want captured without a specific script. Each workflow leads to a generated video, but the path differs slightly.

For script-based generation, paste your narration or dialogue and specify the visual style — minimalist, cinematic, animated, or documentary. The skill maps your words to matching visuals and pacing. For topic-based generation, simply name the subject and target audience. The skill structures the content, selects a narrative flow, and generates accordingly.

For mood-driven videos — common in social media and brand content — describe the feeling you want viewers to have, the color palette, and the energy level. Upbeat and colorful for a fitness brand, calm and minimal for a wellness product. These cues shape everything from scene transitions to text overlays, giving you a video that feels intentional and on-brand without manual editing.

## Integration Guide for Free Video Generation

This skill fits naturally into content pipelines where speed and volume matter. If you're managing a social media calendar, you can batch-generate video drafts for the week by submitting multiple prompts in sequence — one per platform format if needed, such as vertical for Reels or square for feed posts.

For teams using content management workflows, generated videos can be exported and dropped directly into scheduling tools like Buffer or Later. The skill outputs are designed to be publish-ready or minimally editable, so your post-production step stays lightweight.

Educators and course creators can integrate this skill into lesson planning by generating short video summaries for each module topic. Submit your lesson outline and let the skill produce a companion video that reinforces key concepts visually. This works especially well for asynchronous learning environments where engagement depends on varied content formats.

If you're running ad campaigns on a tight budget, use this skill to rapidly prototype video ad concepts before committing to professional production — test messaging and visuals cheaply before scaling.

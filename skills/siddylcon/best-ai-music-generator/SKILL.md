---
name: best-ai-music-generator
version: "1.0.0"
displayName: "Best AI Music Generator — Create Original Tracks for Any Mood or Project"
description: >
  Tired of searching royalty-free libraries only to find the same overused tracks? The best-ai-music-generator skill on ClawHub lets you describe the music you need and instantly generate original compositions tailored to your exact mood, tempo, and style. Whether you're scoring a short film, backing a podcast, or soundtracking social content, this skill produces unique audio that fits your creative vision. Supports mp4/mov/avi/webm/mkv video uploads for sync previews.
metadata: {"openclaw": {"emoji": "🎵", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm your AI music composer — ready to generate original tracks tailored to your exact mood, style, and project needs using the best-ai-music-generator skill. Tell me what you're working on and let's create something that sounds exactly right.

**Try saying:**
- "Generate a 90-second upbeat electronic track with a driving beat for a fitness promo video"
- "Create a melancholic acoustic guitar piece with light piano, suitable for a travel documentary outro"
- "Make a tense, cinematic orchestral loop around 60 BPM for a suspense scene in a short film"

### Getting Connected

Before handling any user request, establish a connection to the NemoVideo backend. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Ensure a client identifier exists at `~/.config/nemovideo/client_id` (create one as a UUID if needed)
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Your Personal Composer, Available Anytime

Finding the right music for a project used to mean hours of browsing stock libraries, paying per-track licensing fees, or hiring a composer. The Best AI Music Generator skill changes that entirely — you describe what you want, and it builds something original around your brief.

Whether you need a tense cinematic underscore, an upbeat lo-fi loop for a study video, or a gentle acoustic piece for a wedding slideshow, this skill interprets your creative direction and generates music that genuinely fits. You can specify genre, energy level, instrumentation, tempo, and emotional tone in plain language — no music theory knowledge required.

This skill is built for content creators, video editors, podcasters, game developers, and anyone who needs custom audio without the complexity or cost of traditional music production. The result is a track that feels intentional and crafted, not randomly assembled — giving your project a professional sonic identity from the very first listen.

## Routing Your Music Generation Requests

When you describe a mood, genre, tempo, or instrumentation, your prompt is parsed and routed to the optimal generation pipeline based on track length, style complexity, and whether you need stems, loops, or a full composition.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Music Reference

The NemoVideo backend processes your music generation requests by translating natural-language prompts into structured audio synthesis parameters — handling BPM mapping, key signatures, and timbre modeling under the hood. Latency varies with track duration and polyphonic complexity, so longer cinematic pieces take more render time than short ambient loops.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `best-ai-music-generator`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=$TOKEN&task=<task_id>&session=<session_id>&skill_name=best-ai-music-generator&skill_version=1.0.0&skill_source=<platform>`

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

## Tips and Tricks

The more specific your prompt, the better your result. Instead of saying 'make something happy,' try 'create a bright, bouncy ukulele track at 120 BPM with hand claps, suitable for a children's educational video.' Naming a reference mood, a decade, or even a film genre gives the generator useful creative anchors.

If you're generating music to sync with a video, upload your clip alongside your prompt. Describing the pacing of key moments — like 'the beat should drop at the 30-second mark' — helps align the musical energy with your visual cuts.

Don't be afraid to iterate. Generate a first version, then refine with follow-up prompts like 'make it slightly slower' or 'add more bass presence in the low end.' Treating it like a conversation with a composer consistently produces better results than a single broad request.

For looping background music, mention that explicitly — the generator can structure tracks with clean loop points so they repeat seamlessly in presentations or apps.

## Performance Notes

Generation time varies depending on track length and complexity. Short loops under 60 seconds typically render quickly, while longer full-length compositions with layered instrumentation may take additional processing time. Keeping initial requests under 3 minutes is recommended for fastest turnaround.

Highly complex prompts requesting multiple distinct sections — like a track with a quiet intro, building middle, and explosive finale — will take longer than a single-mood piece. If speed matters, generate sections individually and combine them in your editing workflow.

Audio output quality is optimized for standard video and podcast production use. For projects requiring broadcast-grade mastering or specific technical audio specs, plan to run the generated track through a dedicated mastering tool as a final step. The skill focuses on creative composition, not post-production processing.

Uploaded video files in mp4/mov/avi/webm/mkv formats are used for reference and sync previewing only — they are not altered or re-exported by this skill.

---
name: news-anchor-video
version: "1.0.0"
displayName: "News Anchor Video Creator — Generate Professional Broadcast-Style News Videos"
description: >
  Tired of spending hours trying to produce polished, broadcast-quality news anchor videos from scratch? The news-anchor-video skill automates the creation of professional presenter-style news segments — complete with scripted delivery, teleprompter-ready formatting, and studio-look visuals. Ideal for content creators, media teams, marketers, and educators who want authoritative news-style video content without a production crew.
metadata: {"openclaw": {"emoji": "📰", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to your news anchor video studio — let's turn your story into a broadcast-ready segment that looks like it belongs on the evening news. Share your topic, script, or article link and I'll get started right away.

**Try saying:**
- "Write a news anchor video script"
- "Make a broadcast-style news segment"
- "Format my article as news video"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Your Personal News Studio, Ready in Minutes

Creating a convincing news anchor video used to mean booking a studio, hiring talent, writing a broadcast script, and editing hours of footage. This skill collapses that entire pipeline into a single, guided workflow — so you can go from a topic or article to a finished news-style segment faster than ever.

The news-anchor-video skill is built around the specific conventions of broadcast journalism: clear scripting with proper news cadence, on-screen lower-third style formatting, confident presenter framing, and the kind of visual authority audiences associate with professional news channels. Whether you're producing internal company updates, educational explainers, or branded media content, the output feels credible and polished.

Target users include social media managers who want news-format hooks, educators building current-events lessons, PR teams creating press-release-style video content, and indie creators who want a high-trust aesthetic for their channel. No prior video production experience is required — just bring your story, and the skill handles the structure.

## Routing Your Broadcast Requests

Each request — whether generating a teleprompter script, selecting an anchor avatar, or rendering a final broadcast segment — is parsed and routed to the appropriate pipeline stage based on intent and asset type.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

News anchor video generation runs through a cloud-based rendering backend that handles avatar lip-sync, chroma key compositing, and broadcast-grade encoding in real time. All API calls are authenticated per session and return a signed media URL upon successful render completion.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `news-anchor-video`
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

## Troubleshooting

If your generated news anchor video script sounds stiff or overly formal, try specifying a tone modifier in your prompt — phrases like 'conversational broadcast tone' or 'local news warmth' give the output more natural delivery rhythm compared to the default neutral anchor style.

If the segment is running too long when read aloud, ask for a tighter edit targeting a specific word count. A 90-second segment at average broadcast pace sits around 225–250 words — use that as your benchmark and request a trim accordingly.

For users finding that visual direction notes are too generic, provide context about your actual production setup: whether you're using an AI avatar tool, filming a real presenter, or creating a motion-graphic-only video. The skill will tailor on-screen cues and b-roll suggestions to match your actual production method rather than a generic studio assumption.

## Common Workflows

The most frequent use case is converting a written article or press release into a news anchor video script with visual direction notes. Paste your source text, specify the desired segment length, and the skill will restructure it into broadcast format with intro hook, body delivery, and sign-off.

Another popular workflow is generating a series of recurring news-style updates — for example, weekly company performance summaries or monthly industry roundups delivered in a consistent anchor format. Users define a template once and reuse it with fresh data each cycle.

Educators frequently use this skill to produce current-events segments for classroom use. By inputting a news article and specifying a grade level, they receive an age-appropriate anchor script with suggested on-screen text overlays and discussion prompts built into the segment structure.

Marketing teams also use the news anchor video format to lend credibility to product announcements, framing launches as 'breaking news' stories with all the visual and scripting conventions that implies.

## Performance Notes

News anchor video segments perform best when the input content is focused on a single, clearly defined story angle. Vague or overly broad topics — like 'cover everything about AI' — tend to produce scripts that feel unfocused or run too long for a standard segment format.

For optimal output, aim to provide a headline, 2-3 key facts or talking points, and a preferred tone (breaking news urgency vs. feature-story warmth vs. investigative gravity). Segments in the 45–90 second range consistently produce the most broadcast-authentic results.

If you're generating video for a specific platform — LinkedIn, YouTube, Instagram Reels — mention it upfront. The pacing, script length, and visual cue suggestions will be adjusted to match that platform's viewer expectations and format constraints.

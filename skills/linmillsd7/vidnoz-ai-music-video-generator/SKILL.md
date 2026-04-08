---
name: vidnoz-ai-music-video-generator
version: "1.0.0"
displayName: "Vidnoz AI Music Video Generator — Sync Footage to Music Automatically"
description: >
  Turn raw clips and audio tracks into polished, beat-synced music videos without manual editing. The vidnoz-ai-music-video-generator skill automates scene transitions, visual effects, and rhythm alignment so your footage moves with the music. Ideal for content creators, marketers, and musicians who want professional-looking results fast. Upload your media, choose a style, and let AI handle the rest.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome! You've got footage and a track — let's turn them into something worth sharing. Tell me what you're working with and I'll help you build a beat-synced music video using Vidnoz AI right now.

**Try saying:**
- "Sync my clips to this track"
- "Create a 30-second music reel"
- "Match cuts to beat drops"

### Automatic Setup

On first interaction, connect to the processing API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Generate a UUID as client identifier, then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry).

**Session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Create Beat-Synced Music Videos in Minutes

Making a music video used to mean hours in a timeline editor, manually cutting clips to match every beat drop and melody shift. The Vidnoz AI Music Video Generator changes that entirely. By analyzing both your footage and your audio track simultaneously, it identifies rhythm patterns, tempo changes, and emotional peaks — then assembles your clips to match them naturally.

This skill gives you direct access to that automation layer. You can describe the style you want, specify the mood, select transition types, or let the AI make creative decisions based on your source material. Whether you're producing a lyric video, a brand reel, a wedding highlight, or a social media clip, the output is timed, coherent, and visually engaging.

The tool is designed for people who want quality results without needing professional editing experience. You bring the footage and the song — the AI brings the timing, the cuts, and the visual flow. It's a practical shortcut from raw media to shareable video.

## Routing Clips and Beat Requests

When you submit a footage upload or music sync request, ClawHub parses your intent and routes it to the appropriate Vidnoz AI pipeline — whether that's beat detection, auto-cut sequencing, or transition styling.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Vidnoz Cloud Processing Reference

Vidnoz AI handles all music-to-video synchronization server-side, using its beat-matching engine to analyze BPM, waveform peaks, and rhythm patterns before applying automated cuts and transitions to your footage. Your rendered music video is processed entirely in the cloud, so local hardware specs have no impact on export quality or sync accuracy.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `vidnoz-ai-music-video-generator`
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

The vidnoz-ai-music-video-generator performs best when your audio track has a clear, consistent tempo or identifiable beat markers. Songs with strong percussion or defined drops give the AI more anchor points for cut alignment, resulting in tighter sync.

For footage, shorter clips (3–10 seconds each) tend to produce more dynamic results than long uncut takes. The more variety in your source material — different angles, movement speeds, and lighting — the more visually interesting the final edit will be.

If you're working with a track that has a slow tempo or ambient structure, specify a 'mood-based' rather than 'beat-based' sync mode. This tells the AI to prioritize emotional pacing over strict rhythmic cuts, which suits cinematic and documentary-style videos far better.

## Common Workflows

Most users approach the vidnoz-ai-music-video-generator with one of three workflows. The first is the full-auto approach: upload footage and audio, let the AI select clip order, transition style, and beat alignment without manual input. This works well for social content where speed matters more than precise creative control.

The second workflow is style-guided generation. Here you describe a visual mood — cinematic, energetic, minimal, nostalgic — and the AI applies matching effects, color treatment, and cut pacing to your material. This is popular for brand videos and music artist content.

The third workflow is segment-specific editing: you lock certain scenes to specific timestamps in the song and let the AI fill the gaps. This gives you creative checkpoints while still automating the bulk of the assembly. It's the preferred method for wedding films and narrative-driven reels where specific moments must hit on cue.

## Use Cases

The vidnoz-ai-music-video-generator fits a wide range of real-world content needs. Musicians and bands use it to produce lyric videos and visual albums without hiring a video editor. The AI handles the timing and aesthetics while the artist focuses on the creative direction.

Social media managers use it to turn product footage into scroll-stopping reels timed to trending audio, dramatically cutting production time per post. E-commerce brands find it especially useful for seasonal campaigns where multiple product videos need to be produced quickly.

Event videographers — particularly in weddings and corporate productions — rely on it to deliver highlight reels the same day as the event. And independent content creators on YouTube and TikTok use it to add a professional polish to vlogs and travel content without investing in expensive software or editing skills.

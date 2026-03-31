---
name: video-reverser
version: "1.0.6"
displayName: "Video Reverser - Reverse and Rewind Video Clips with AI"
description: "Reverse any video clip instantly — upload a video and get a smooth reversed version perfect for creative effects and artistic content. Supports full reversal, partial segment reversal, slow-motion reverse, and boomerang-style loops. Supports mp4, mov, avi, webm, mkv."
  Video reverser that plays video clips in reverse through AI chat. Upload any video
  and the AI creates a smooth reversed version â perfect for creative effects, satisfying
  rewind moments, and artistic content. Handles full video reversal, partial segment
  reversal (reverse only a specific section), reverse with speed changes (slow-mo
  reverse for dramatic effect), and boomerang-style forward-then-reverse loops. Create
  satisfying reverse videos of pouring, breaking, falling, or building. Combine reverse
  segments with forward playback for creative storytelling: "play forward to 0:05 then
  reverse back to start." Works for TikTok reverse trends, Instagram Reels effects,
  and creative video projects. Adjust audio during reverse â keep original, mute, or
  add new music. Export as MP4. Supports mp4, mov, avi, webm, mkv.
metadata: {"openclaw": {"emoji": "ð¬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🎵 Welcome! I can video reverser for you. Share a video file or tell me your idea!

**Try saying:**
- "add effects to this clip"
- "edit my video"
- "help me create a short video"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.

# Video Reverser - Play It Backwards

## 1. Role & Environment

You are an OpenClaw agent acting as the **interface layer** between the user and NemoVideo's backend AI Agent. The backend handles video generation/editing but assumes a GUI exists. Your job:

1. **Relay** user requests to the backend via SSE
2. **Intercept** backend responses â replace GUI references with API actions
3. **Supplement** â handle export/render, credits, file delivery directly
4. **Translate** â present results in user's language with clear status

### Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `NEMO_TOKEN` | No | Auto-generated on first use |
| `NEMO_API_URL` | No | `https://mega-api-prod.nemovideo.ai` |
| `NEMO_WEB_URL` | No | `https://nemovideo.com` |
| `NEMO_CLIENT_ID` | No | Auto-generated UUID, persisted to `~/.config/nemovideo/client_id` |
| `SKILL_SOURCE` | No | Auto-detected from install path |

If `NEMO_TOKEN` is not set:
```bash
CLIENT_ID="${NEMO_CLIENT_ID:-$(cat ~/.config/nemovideo/client_id 2>/dev/null)}"
if [ -z "$CLIENT_ID" ]; then
  CLIENT_ID=$(uuidgen 2>/dev/null || echo "client-$(date +%s)-$RANDOM")
  mkdir -p ~/.config/nemovideo && echo "$CLIENT_ID" > ~/.config/nemovideo/client_id
fi
curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
```
Save `token` as `NEMO_TOKEN`. Expires after 7 days; re-request with same `X-Client-Id`.

## 2. Request Router

| User says... | Action | Skip SSE? |
|-------------|--------|-----------|
| "export" / "download" / "send me the video" | Export | Yes |
| "credits" / "balance" | Credits | Yes |
| "status" / "show tracks" | State | Yes |
| "upload" / user sends file | Upload | Yes |
| Everything else | SSE | No |

## 3. Core Flows

`$API` = `${NEMO_API_URL:-https://mega-api-prod.nemovideo.ai}`, `$TOKEN` = `${NEMO_TOKEN}`, `$WEB` = `${NEMO_WEB_URL:-https://nemovideo.com}`.

All API requests MUST include:
```
X-Skill-Source: $SKILL_NAME
X-Skill-Version: $SKILL_VERSION
X-Skill-Platform: $SKILL_SOURCE
```

### 3.0 Create Session
```bash
curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"task_name":"project","language":"<lang>"}'
```
Save `session_id`, `task_id`.

### 3.1 Send Message via SSE
```bash
curl -s -X POST "https://mega-api-prod.nemovideo.ai/run_sse" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" --max-time 900 \
  -d '{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}'
```

### 3.2 Upload
**File**: `curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/upload-video/nemo_agent/me/<sid>" -H "Authorization: Bearer $TOKEN" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -F "files=@/path/to/file"`

**URL**: same endpoint, `-d '{"urls":["<url>"],"source_type":"url"}'`

Supported: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### 3.3 Credits
```bash
curl -s "https://mega-api-prod.nemovideo.ai/api/credits/balance/simple" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```

### 3.4 Query State
```bash
curl -s "https://mega-api-prod.nemovideo.ai/api/state/nemo_agent/me/<sid>/latest" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```

### 3.5 Export
```bash
curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/render/proxy/lambda" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}'
```
Poll `GET https://mega-api-prod.nemovideo.ai/api/render/proxy/lambda/<id>` every 30s.

### 3.6 Disconnect Recovery
Wait 30s, query state. After 5 unchanged polls, report failure.

## 4. GUI Translation

| Backend says | You do |
|-------------|--------|
| "click Export" | Render + deliver |
| "open timeline" | Show state |
| "drag/drop" | Send edit via SSE |
| "check account" | Show credits |

## 6. Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1001 | Token expired | Re-auth |
| 1002 | Session gone | New session |
| 2001 | No credits | Show registration URL |
| 4001 | Unsupported file | Show formats |
| 402 | Export restricted | "Register at nemovideo.ai" |
| 429 | Rate limited | Wait 30s, retry |

## 7. Limitations

- Aspect ratio change after generation requires regeneration
- YouTube/Spotify music URLs not supported; built-in library available
- Photo editing not supported; slideshow creation available
- Local files must be sent in chat or provided as URL


## 5. Reverse Tips

**Partial reverse**: "Reverse from 0:05 to 0:10" keeps the rest playing forward normally.

**Boomerang**: "Make a boomerang loop" creates forward-then-reverse seamless loops.

**Speed**: "Slow-mo reverse" combines slowdown with reversal for dramatic effect.

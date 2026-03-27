---
name: screen-recorder-free
version: "1.0.0"
displayName: "Free Screen Recorder — Capture, Edit & Export Instantly"
description: >
  screen-recorder-free is a ClawHub skill that lets you capture, trim, annotate, and export screen recordings without installing any software. Record browser tabs, app windows, or your full desktop, then describe edits in plain language — crop a region, cut dead air, add captions, or change playback speed. Ideal for tutorial creators, support teams, and remote workers. Exports to mp4, mov, avi, webm, and mkv.
metadata: {"openclaw": {"emoji": "🖥️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# Record Your Screen, Edit It By Just Talking

Most screen recorders stop at the recording itself — leaving you to hunt down a separate editor, learn its timeline, and export through a maze of settings. The screen-recorder-free skill collapses that entire workflow into a single conversation. You capture your screen, describe what you want changed, and the skill handles the rest.

Under the hood, the OpenClaw agent interprets your natural-language instructions and maps them onto precise video operations — whether that means silencing a fumbled sentence, zooming into a specific UI element mid-recording, or stitching two clips together with a clean cut. The agent understands context across your session, so you can say 'remove the part where I switched tabs by mistake' and it knows exactly which segment you mean.

This approach is especially useful for people who record frequently but aren't video editors — customer support reps building knowledge-base walkthroughs, developers documenting bugs, or educators producing quick how-to clips. No timeline scrubbing, no keyframe panels. Just describe the result you want, and the skill produces a polished file ready to share or embed. Final recordings export in mp4, mov, avi, webm, or mkv to fit any platform requirement.

### Environment Variables

| Variable | Required | Default |
|----------|----------|--------|
| `NEMO_TOKEN` | No | Auto-generated (100 free credits, expires in 7 days, revocable via Settings → API Tokens) |
| `NEMO_API_URL` | No | `https://mega-api-prod.nemovideo.ai` |
| `NEMO_WEB_URL` | No | `https://nemovideo.com` |
| `NEMO_CLIENT_ID` | No | Auto-generated UUID, persisted to `~/.config/nemovideo/client_id` (UUID only, no secrets) |
| `SKILL_SOURCE` | No | Auto-detected from install path, fallback `unknown` |

If `NEMO_TOKEN` is not set, get one (requires `X-Client-Id` header):
```bash
# Generate or read persisted Client-Id
CLIENT_ID="${NEMO_CLIENT_ID:-$(cat ~/.config/nemovideo/client_id 2>/dev/null)}"
if [ -z "$CLIENT_ID" ]; then
  CLIENT_ID=$(uuidgen 2>/dev/null || echo "client-$(date +%s)-$RANDOM")
  mkdir -p ~/.config/nemovideo && echo "$CLIENT_ID" > ~/.config/nemovideo/client_id
fi
curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
# → {"code":0,"data":{"token":"nmv_usr_xxx","credits":100,...}}
```
Save `token` as `NEMO_TOKEN`, `CLIENT_ID` as `NEMO_CLIENT_ID`. Anonymous: 1 token per client per 7 days; token expires in 7 days and can be revoked at any time via **Settings → API Tokens** on nemovideo.com. If your token expires, request a new one with the same `X-Client-Id`.

**Local persistence:** This skill writes `~/.config/nemovideo/client_id` to persist the Client-Id across sessions. This avoids generating a new ID on every request, which would hit the per-IP rate limit quickly (default 10 tokens per 7 days per IP). The file contains only a UUID — no credentials are stored locally.

## 2. Routing Incoming Requests

Use the table below to determine which endpoint handles each type of incoming request.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## 3. Primary Operational Flows

$API = `${NEMO_API_URL:-https://mega-api-prod.nemovideo.ai}`, $TOKEN = `${NEMO_TOKEN}`, $WEB = `${NEMO_WEB_URL:-https://nemovideo.com}`.

Skill attribution variables — do NOT hardcode:
- `$SKILL_NAME` = this file's YAML frontmatter `name`
- `$SKILL_VERSION` = this file's YAML frontmatter `version`
- `$SKILL_SOURCE` = detect at runtime using the first match:
  1. Env `SKILL_SOURCE` if set
  2. If this file's path contains a known platform directory (e.g. `~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`)
  3. Fallback: `unknown`

**CRITICAL**: ALL API requests (including render/export/upload/state/credits) MUST include these headers. Missing them will cause export to fail with 402.
```
X-Skill-Source: $SKILL_NAME
X-Skill-Version: $SKILL_VERSION
X-Skill-Platform: $SKILL_SOURCE
```

### 3.0 Initialize a Session
```bash
curl -s -X POST "$API/api/tasks/me/with-session/nemo_agent" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"task_name":"project","language":"<lang>"}'
# → {"code":0,"data":{"task_id":"...","session_id":"..."}}
```
Before any other action can take place, a session must be established. Every subsequent request depends on the session identifier returned at this stage.

**Open in browser**: After creating a session, give the user a link to view/edit the task in NemoVideo:
`$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

### 3.1 Deliver a Message Over SSE
```bash
curl -s -X POST "$API/run_sse" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" --max-time 900 \
  -d '{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}'
```
All conversational messages to the backend are transmitted through a Server-Sent Events channel.

#### SSE Handling

| Event | Action |
|-------|--------|
| Text response | Apply GUI translation (§4), present to user |
| Tool call/result | Wait silently, don't forward |
| `heartbeat` / empty `data:` | Keep waiting. Every 2 min: "⏳ Still working..." |
| Stream closes | Process final response |

Typical durations: text 5-15s, video generation 100-300s, editing 10-30s.

**Timeout**: 10 min heartbeats-only → assume timeout. **Never re-send** during generation (duplicates + double-charge).

Ignore trailing "I encountered a temporary issue" if prior responses were normal.

#### Silent Response Fallback (CRITICAL)

Approximately 30% of edit operations return no text in the response. When this occurs: first, check the HTTP status code to confirm the request succeeded; second, poll the session state endpoint to retrieve the current operation status; third, surface a status update to the user rather than treating the empty response as a failure.

**Two-stage generation**: After raw video is produced, the backend automatically triggers a second processing stage that appends background music and a title sequence. Be aware of both stages when tracking job completion — the final deliverable is not ready until stage two has finished.

### 3.2 Handling File Uploads

**File upload**: `curl -s -X POST "$API/api/upload-video/nemo_agent/me/<sid>" -H "Authorization: Bearer $TOKEN" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -F "files=@/path/to/file"`

**URL upload**: `curl -s -X POST "$API/api/upload-video/nemo_agent/me/<sid>" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -d '{"urls":["<url>"],"source_type":"url"}'`

Use **me** in the path; backend resolves user from token.

Supported: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

The upload endpoint accepts media files that will be used as source material within the current session.

### 3.3 Checking Available Credits
```bash
curl -s "$API/api/credits/balance/simple" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
# → {"code":0,"data":{"available":XXX,"frozen":XX,"total":XXX}}
```
Query the credits endpoint to verify the user has a sufficient balance before initiating any operation that consumes credits.

### 3.4 Retrieving Current Session State
```bash
curl -s "$API/api/state/nemo_agent/me/<sid>/latest" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```
Use **me** for user in path; backend resolves from token.
Key fields: `data.state.draft`, `data.state.video_infos`, `data.state.canvas_config`, `data.state.generated_media`.

**Draft field mapping**: `t`=tracks, `tt`=track type (0=video, 1=audio, 7=text), `sg`=segments, `d`=duration(ms), `m`=metadata.

**Draft ready for export** when `draft.t` exists with at least one track with non-empty `sg`.

**Track summary format**:
```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

### 3.5 Exporting and Delivering the Final Output

**Export does NOT cost credits.** Only generation/editing consumes credits.

Exporting a finished video does not deduct any credits from the user's balance. The export flow proceeds as follows: (a) confirm the job has reached a completed state; (b) call the export endpoint with the session identifier; (c) await the download URL in the response; (d) verify the URL is reachable before presenting it to the user; (e) deliver the link along with the filename and format details.

**b)** Submit: `curl -s -X POST "$API/api/render/proxy/lambda" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -d '{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}'`

Note: `sessionId` is **camelCase** (exception). On failure → new `id`, retry once.

**c)** Poll (every 30s, max 10 polls): `curl -s "$API/api/render/proxy/lambda/<id>" -H "Authorization: Bearer $TOKEN" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"`

Status at top-level `status`: pending → processing → completed / failed. Download URL at `output.url`.

**d)** Download from `output.url` → send to user. Fallback: `$API/api/render/proxy/<id>/download`.

**e)** When delivering the video, **always also give the task detail link**: `$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

Progress messages: start "⏳ Rendering ~30s" → "⏳ 50%" → "✅ Video ready!" + file + **task detail link**.

### 3.6 Recovering from an SSE Disconnection

When an SSE connection drops, follow these steps: (1) detect the disconnection event and pause any pending UI updates; (2) wait a short back-off interval before attempting to reconnect; (3) re-establish the SSE connection using the existing session identifier — do not create a new session; (4) once reconnected, poll the state endpoint to reconcile any events that may have been missed during the outage; (5) resume normal message handling and inform the user if the interruption affected a running operation.

## 4. Translating GUI Elements for the Backend

The backend operates under the assumption that a graphical interface is present — never forward raw GUI instructions or UI component references directly to it.

| Backend says | You do |
|-------------|--------|
| "click [button]" / "点击" | Execute via API |
| "open [panel]" / "打开" | Show state via §3.4 |
| "drag/drop" / "拖拽" | Send edit via SSE |
| "preview in timeline" | Show track summary |
| "Export button" / "导出" | Execute §3.5 |
| "check account/billing" | Check §3.3 |

**Keep** content descriptions. **Strip** GUI actions.

## 5. Recommended Interaction Patterns

• Always confirm a session is active before dispatching any request to the backend.
• When a response body is empty, rely on state polling rather than assuming an error has occurred.
• Present progress indicators to the user during both processing stages of video generation.
• Validate credit availability ahead of any credit-consuming action to avoid unnecessary failures.
• After an SSE reconnect, reconcile missed events via the state endpoint before resuming user-facing updates.

## 6. Known Limitations

• A single session cannot be shared across multiple concurrent users.
• Silent responses are expected behavior for a subset of edit operations and should not be treated as errors.
• Background music and title injection occur automatically server-side and cannot be suppressed through the API.
• Export URLs are time-limited and should be delivered to the user promptly after retrieval.
• Credit balances are read-only through the API; top-ups must be handled outside this integration.

## 7. Error Handling Reference

The table below maps common error codes to their causes and the recommended remediation steps.
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

**Common**: no video → generate first; render fail → retry new `id`; SSE timeout → §3.6; silent edit → §3.1 fallback.

## 8. Version Information and Token Scopes

Before going live, confirm the API version in use matches the version this skill was built and validated against. Token scopes must include permissions for session management, messaging, file upload, export, and credits retrieval — requests made with tokens missing any required scope will be rejected with an authorization error.

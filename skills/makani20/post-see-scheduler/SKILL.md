---
name: post-see-post-scheduling-skill
description: Turn your OpenClaw into an autonomous social media manager using the Post See API. Use when scheduling, posting, or managing content across Instagram, LinkedIn, X, Facebook, Threads, Bluesky, Pinterest, YouTube, Mastodon, Discord, and other networks Post See supports.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - POST_SEE_API_KEY
      bins:
        - ffmpeg
    primaryEnv: POST_SEE_API_KEY
    homepage: https://api.post-see.com/
---

# Social Media Assistant (via Post See / post-see.com)

Autonomously manage social scheduling and publishing through the **[Post See REST API](https://api.post-see.com/)**.

**Canonical spec:** download or reference [`https://api.post-see.com/openapi.yaml`](https://api.post-see.com/openapi.yaml) (same host as the docs).

**Bundled helpers (optional):** this package includes `prompts/generate-post.txt`, `prompts/schedule-post.txt`, `skill.json`, and Node CLIs under `actions/*.js` (Node 18+). The runtime instructions below are sufficient without executing those files.

## Setup

1. Create a Post See account at [post-see.com](https://post-see.com).
2. Connect your social accounts and link them into a **workspace**.
3. Enable API access and create an API key (`pk_live_…` as shown in the API docs “Try it”).
4. Store your API key in workspace `.env`:

   ```
   POST_SEE_API_KEY=pk_live_xxxxx
   ```

5. Optional: save the OpenAPI document locally for offline reference:

   ```
   curl -sS https://api.post-see.com/openapi.yaml -o post-see-openapi.yaml
   ```

6. **ffmpeg** — used when you work from **local** video files (extract a frame to read on-screen text before writing captions). Post See accepts **public HTTPS URLs** in `media_urls`; host files on your storage/CDN first.

## Auth

All requests use a Bearer token:

```
Authorization: Bearer <POST_SEE_API_KEY>
Content-Type: application/json
```

**Base URL:** `https://api.post-see.com/api/v1`

## Responses

- **Success:** `{ "data": …, "meta": { "api_version": "1.0", … } }`
- **Error:** `{ "error": { "code", "message", "details?" }, "meta": … }` — branch on `error.code` (e.g. `unauthorized`, `workspace_forbidden`, `post_locked`, `validation_error`).

## Workspace scope

Pass **`workspace_id`** as a query parameter (or **`X-Workspace-Id`** where supported). Resolve membership before trusting any id. **Roles:** `readonly` can read; creating/updating/deleting posts requires `collaborator`, `admin`, or `owner`.

Optional: `timezone` query or **`X-Timezone`** (IANA) for schedule display or naive local times.

## Platform slugs (`platform` field)

Documented today (lowercase; **treat as opaque** — new values may appear): `bluesky`, `discord`, `facebook`, `instagram`, `linkedin`, `mastodon`, `pinterest`, `threads`, `x`, `youtube`. **X uses `x`, not `twitter`.** Always match the `platform` string returned from `GET /social-accounts` for the chosen connection.

**Immediate publish on create** (`POST /posts`, per OpenAPI): **`linkedin`**, **`facebook`**, **`instagram`**, **`x`**, **`pinterest`**, **`bluesky`**, **`threads`**. Others (e.g. **`youtube`**, **`mastodon`**, **`discord`**) support **drafts** and **scheduled** posts via `scheduled_at` / worker — do not assume synchronous publish in the create response.

## Core workflow

### 1. List workspaces (get `workspace_id`)

```
GET /workspaces
```

Use `data.workspaces[]` → `id`, `name`, `myRole`.

### 2. Get linked social accounts

```
GET /social-accounts?workspace_id=<workspace_id>
```

Returns `data.connections[]` with `id` (**use as `connection_id`**), `platform`, `platform_username`, `is_connected`, `needs_reauth`, and for Pinterest optionally `default_pin_destination_link`. **OAuth tokens are never returned.** If `needs_reauth` is true, the user must reconnect in the product before publish will succeed.

### 3. List and inspect posts

```
GET /posts?workspace_id=<id>&status=<draft|scheduled|published|fail>&platform=<slug>&page=1&limit=20
GET /posts/{id}
```

### 4. Create post

```
POST /posts
```

**Required:** `workspace_id`.

**Typical JSON body:**

```json
{
  "workspace_id": 7,
  "connection_id": 42,
  "platform": "instagram",
  "text": "Caption and #hashtags",
  "caption": "Optional alias for text",
  "scheduled_at": "2026-04-01T14:00:00Z",
  "media_urls": ["https://cdn.example.com/asset.jpg"]
}
```

- Omit `scheduled_at` / `date_time` for **drafts**.
- **`media_urls`:** public **HTTPS** URLs only (upload to your storage first).
- **Pinterest:** `board_id` or `boardId`; optional default outbound URL may exist on the connection.
- **YouTube:** `post_title`, **`youtube_options`** (object, default `{}`) for product-specific hints (privacy, category, shorts vs long-form, etc.).
- **All platforms:** **`platform_options`** (object, default `{}`) for forward-compatible flags (visibility, audience, etc.).

Deprecated: `social_account_ids` — prefer **`connection_id`**.

**201** may include `data.publish_results` when immediate publish was attempted.

### 5. Update or delete posts

```
PUT /posts/{id}
DELETE /posts/{id}
```

Use **`PUT`**, not PATCH. **409** `post_locked` if the post is published or cannot be changed.

### 6. Check publish results

```
GET /post-results?workspace_id=<id>&post_id=<optional>&page=1&limit=20
GET /post-results/{id}
```

Inspect `data.results[]`: `status` (`pending` | `success` | `fail`), `external_post_url`, nested `error` (e.g. `publish_failed`).

### 7. Current user (optional)

```
GET /me
PATCH /me
```

## Team / workspace admin (optional)

Routes under `/workspaces/...` (members, invitations, transfer) are **destructive or role-sensitive**. Use only when the user explicitly asks; see OpenAPI for `owner` vs `admin` requirements.

## Recommended workflow for video content

1. Store videos in a local folder.
2. Extract a frame with ffmpeg to read any text overlays:

   ```
   ffmpeg -i video.mp4 -ss 00:00:04 -frames:v 1 frame.jpg -y
   ```

3. Write caption from content + hashtags; upload media to HTTPS storage and copy URLs.
4. `POST /posts` with `media_urls`, `connection_id`, `platform`, and schedule (or draft).
5. Move posted assets to a `posted/` subfolder to avoid duplicates.
6. After the scheduled time, `GET /post-results?post_id=...` to confirm `status` and `external_post_url`.

## Tips

- Resolve **`workspace_id`** and **`connection_id`** before every create/update; guessing ids causes `403` or empty lists.
- Stagger posts across the day for better reach when scheduling manually.
- Keep hashtags focused (roughly 4–5 where appropriate for the network).
- Re-fetch `openapi.yaml` when integrating — new fields and platforms appear there first.
- Use a **test workspace** and non-production accounts before automating brands you care about.

## Safety

Use a **least-privilege** API key; revoke from the dashboard if leaked. This skill implies the agent may read `.env`, workspace files, and **public** media URLs you provide — avoid sensitive paths and shared/synced folders you do not trust. If you do not want autonomous posting, require human confirmation before `POST /posts` or restrict agent autonomy in your OpenClaw config.

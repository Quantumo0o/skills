# Post See — social scheduling skill (ClawHub)

Instruction and tooling for agents that call the **[Post See REST API](https://api.post-see.com/)** (`https://api.post-see.com/api/v1`). The **authoritative contract** is always [`openapi.yaml`](https://api.post-see.com/openapi.yaml) on the same host.

## ClawHub manifest (`skill.json`)

Required fields for this bundle:

| Field | Value |
|--------|--------|
| `name` | `post-see-post-scheduling-skill` |
| `description` | `Schedule and publish posts across multiple social platforms using AI.` |
| `entry` | `prompts/generate-post.txt` — primary agent instructions |
| `actions` | Array of relative paths to platform CLI scripts (`actions/<slug>.js`), same order as API slugs: bluesky → youtube |

Secondary workflow prompt: `prompts/schedule-post.txt` (also listed under `prompts.schedule` in `skill.json`).

### ClawHub listing (same idea as [Post Bridge on ClawHub](https://clawhub.ai/jackfriks/post-bridge-social-manager))

The public **skills page** is driven mainly by **`SKILL.md`**: title + body preview, and **runtime** from YAML **`metadata.openclaw`** (`requires.env`, `requires.bins`, `primaryEnv`). Put your “hero” workflow in `SKILL.md`; use `skill.json` for extra tooling metadata your stack reads. Published skills on ClawHub are **MIT-0** ([skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)).

## Supported platform slugs

These are the **documented** `social_connections.platform` / `posts.platform` values today (lowercase). **New slugs may appear** — treat `platform` as an opaque string; never hard-code an exhaustive enum in production without checking the live spec.

| Slug | Notes |
|------|--------|
| `bluesky` | Publish-now supported on create (see below). |
| `discord` | Drafts / scheduling via worker; not in immediate publish-now set. |
| `facebook` | Publish-now supported on create. |
| `instagram` | Publish-now supported on create. |
| `linkedin` | Publish-now supported on create. |
| `mastodon` | Drafts / scheduling; not in immediate publish-now set. |
| `pinterest` | Publish-now supported on create; use `board_id` / `boardId`; connections may expose `default_pin_destination_link`. |
| `threads` | Publish-now supported on create. |
| `x` | **X (Twitter)** — slug is `x`, not `twitter`. Publish-now supported on create. |
| `youtube` | Drafts / scheduling; use `post_title`, `youtube_options` JSON as needed. |

**Immediate publish on `POST /posts`** (per OpenAPI): only **`linkedin`**, **`facebook`**, **`instagram`**, **`x`**, **`pinterest`**, **`bluesky`**, and **`threads`**. Other platforms (e.g. **`youtube`**, **`mastodon`**, **`discord`**) are still valid for **drafts** and **scheduled** posts (`scheduled_at` / `date_time` + worker).

## Setup

1. [Post See](https://post-see.com) account; connect networks; link profiles into a **workspace**.
2. API key (`pk_live_…` in docs “Try it”).
3. Env:

   ```bash
   export POST_SEE_API_KEY=pk_live_xxxxx
   # optional defaults for agents:
   export POST_SEE_WORKSPACE_ID=7
   export POST_SEE_TIMEZONE=Europe/London   # IANA; sent as query/header where supported
   ```

## Authentication

```http
Authorization: Bearer <POST_SEE_API_KEY>
Content-Type: application/json
```

Base URL: **`https://api.post-see.com/api/v1`**

## Response envelope

- **Success:** `{ "data": …, "meta": { "api_version": "1.0", … } }`
- **Error:** `{ "error": { "code", "message", "details?" }, "meta": … }` — branch on `error.code` (`unauthorized`, `workspace_forbidden`, `post_locked`, `validation_error`, …).

## Workspace scope

Pass **`workspace_id`** as a query parameter on relevant routes (or **`X-Workspace-Id`** where the implementation supports it). The server checks **workspace membership**; never assume a client-supplied workspace id is safe without that check (see API description in OpenAPI).

**Roles (workspace):** `readonly` may read lists/details; **create / update / delete posts** needs `collaborator`, `admin`, or `owner`.

## Core HTTP workflow

### 1) Workspaces

```http
GET /workspaces
```

Use `data.workspaces[]` → `id`, `name`, `myRole`, etc.

### 2) Linked social accounts

```http
GET /social-accounts?workspace_id=<id>
```

`data.connections[]`: `id` (this is **`connection_id`** on posts), `platform`, `platform_username`, `is_connected`, `needs_reauth`, optional **`default_pin_destination_link`** (Pinterest). **OAuth tokens are not returned.**

Match the user’s requested account by **`platform` + `platform_username`** (or `id` if they know it).

### 3) Posts — list / get

```http
GET /posts?workspace_id=<id>&status=<draft|scheduled|published|fail>&platform=<slug>&page=1&limit=20
GET /posts/{id}
```

Optional **`timezone`** query or **`X-Timezone`** header for schedule display formatting.

### 4) Create post

```http
POST /posts
```

**Required:** `workspace_id`.

**Typical body fields** (see `PostCreateRequest` in OpenAPI):

- `connection_id` — required when targeting a specific linked account for publish/schedule (optional for some drafts).
- `platform` — lowercase slug; **must match** the connection and the network you intend.
- `text` / `caption` — body copy (max length in schema).
- `scheduled_at` or `date_time` — ISO 8601; omit for drafts.
- `status` — maps to post lifecycle (e.g. draft / scheduled); use spec + “Try it” for publish-now behavior on supported platforms.
- `media_urls` — array of **public HTTPS** URLs.
- `hashtags`, `image_url`, `video_url`, `link`, `alt_text`, `location`, `tags` — as supported.
- **Pinterest:** `board_id` or `boardId`.
- **Video:** `video_thumbnail_url`, `post_title` where relevant.
- **YouTube:** `youtube_options` (object, defaults `{}`) — shorts/long-form hints, privacy, category, etc. per product.
- **All platforms:** `platform_options` (object, defaults `{}`) — forward-compatible flags (visibility, audience, cross-post, etc.).

Deprecated: `social_account_ids` — use **`connection_id`**; if both are sent they must match.

**201** response may include `data.publish_results` when immediate publish was attempted.

### 5) Update / delete

```http
PUT /posts/{id}
DELETE /posts/{id}
```

**`PUT` only** (not PATCH). Published or in-flight posts may return **`409`** with `post_locked`.

### 6) Publish results

```http
GET /post-results?workspace_id=<id>&post_id=<optional>&page=1&limit=20
GET /post-results/{id}
```

`data.results[]`: `status` (`pending` | `success` | `fail`), `external_post_url`, optional nested `error` (e.g. `publish_failed`).

### 7) Profile (optional)

```http
GET /me
PATCH /me
```

Caller-only profile fields.

## Team / workspace admin (optional)

Routes under `/workspaces/...` (members, invitations, transfer, leave) are **destructive or role-sensitive**. Use only when the user explicitly asks; read OpenAPI for required roles (`owner` vs `admin`).

## Actions (Node 18+)

Shared client: `actions/post-see-client.js`. One CLI entry per platform slug, e.g.:

```bash
cd skill
POST_SEE_API_KEY=pk_live_... node actions/x.js list-workspaces
POST_SEE_API_KEY=pk_live_... node actions/instagram.js list-connections 7
POST_SEE_API_KEY=pk_live_... node actions/linkedin.js create 7 42 '{"text":"Hello","scheduled_at":"2026-04-01T12:00:00Z"}'
```

Commands: `help`, `list-workspaces`, `list-connections`, `list-posts`, `post-results`, `create`. See `node actions/<slug>.js help`.

## Prompts

- `prompts/generate-post.txt` — copy and constraints **per platform**.
- `prompts/schedule-post.txt` — API preflight and create/update/results.

## Optional: local video → caption

Host media at a public URL for `media_urls`. If you use local files, **ffmpeg** can extract a frame to read on-screen text (optional):

```bash
ffmpeg -i video.mp4 -ss 00:00:04 -frames:v 1 frame.jpg -y
```

## Safety

Least-privilege API keys; test workspace first; revoke leaked keys; do not commit `.env`; be aware agents may read workspace files and call upload URLs you provide.

## Package for ClawHub

Do **not** put `.git` in the upload (ClawHub rejects non-text paths such as `.git/config`, `.git/HEAD`, `.git/description`). This repo includes **`.clawhubignore`** so `clawhub publish` / `clawhub sync` skips `.git/`.

**Preferred** (tracked files only — never bundles `.git`):

```bash
cd /path/to/post-see-post-scheduling-skill
git archive --format=zip -o post-see-scheduling-skill.zip HEAD
```

**Plain zip** (exclude Git metadata):

```bash
cd /path/to/post-see-post-scheduling-skill
zip -r post-see-scheduling-skill.zip . -x ".git/*" -x "**/.git/*"
```

Upload the zip so **`skill.json`** and **`SKILL.md`** sit at the root of the archive.

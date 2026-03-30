---
name: clawmart-upload
description: Upload your current OpenClaw configuration to the ClawMart marketplace
version: 1.4.0
triggers:
  - "upload to clawmart"
  - "share my config on clawmart"
  - "publish to clawmart"
  - "upload my pack"
---

# ClawMart Upload Skill

You are helping the user upload their OpenClaw configuration to the ClawMart marketplace. Follow these steps exactly and in order.

## Configuration

- ClawMart API base URL: `https://clawmart-gray.vercel.app`
- Config file: `~/.openclaw/clawmart-config.json`
- API endpoint: `POST {base_url}/api/packs`

---

## Step 1: Check API Token

Read `~/.openclaw/clawmart-config.json`. If the file does not exist or `token` is empty:

Tell the user:
> You need a ClawMart API Token to upload. Please visit https://clawmart-gray.vercel.app/dashboard/tokens to generate one, then paste it here.

Once the user provides a token (format: `cm_` followed by hex characters), save it:

```json
{
  "token": "<user_provided_token>",
  "base_url": "https://clawmart-gray.vercel.app"
}
```

Write this to `~/.openclaw/clawmart-config.json`.

---

## Step 2: Scan Workspace Files

Scan `~/.openclaw/workspace/` for OpenClaw configuration files. Do **not** scan the current working directory — the workspace is the canonical location for all OpenClaw configs. OpenClaw supports two naming conventions — match **either** format:

| Default format (no prefix) | Prefixed format | Type |
|---------------------------|-----------------|------|
| `SOUL.md` | `*.soul.md` | SOUL |
| `AGENTS.md` | `*.agents.md` | AGENTS |
| `BOOT.md` | `*.boot.md` | BOOT |
| `HEARTBEAT.md` | `*.heartbeat.md` | HEARTBEAT |
| `MEMORY.md` | `memory_*.json` or `memory-*.json` | MEMORY |
| `IDENTITY.md` | — | IDENTITY |
| `TOOLS.md` | — | TOOLS |
| `USER.md` | — | USER |
| `BOOTSTRAP.md` | — | BOOTSTRAP |
| `skills/*.skill.md` or `skills/*/SKILL.md` | — | LOCAL SKILLS |

**Exclude** any file named `clawmart-upload.skill.md` or `clawmart-install.skill.md` from the list.

If both a default-format and a prefixed-format file exist for the same type (e.g., `SOUL.md` AND `claude.soul.md`), include both and note the duplication to the user.

### Skill Classification

Within `~/.openclaw/workspace/skills/`, check each skill subfolder:

- **Has `_meta.json`** → installed from clawhub (external skill). Read `_meta.json` for `slug`, `version`, and `ownerId`. These are recorded as metadata only — file contents are **not** included in the zip.
- **No `_meta.json`** → user-authored skill. Include the full `SKILL.md` file content in the zip under `skills/`.

Do **not** scan any other directories (not `~/.claude/`, not `~/.claude/plugins/`, not the current working directory).

Show the user a summary:

```
Found the following OpenClaw configuration files:

SOUL:          SOUL.md
AGENTS:        AGENTS.md
IDENTITY:      IDENTITY.md
HEARTBEAT:     HEARTBEAT.md
MEMORY:        MEMORY.md
TOOLS:         TOOLS.md
USER:          USER.md
LOCAL SKILLS (user-authored, will be included):
  - skills/my-workflow/SKILL.md
CLAWHUB SKILLS (installed, metadata only):
  - clawmart-upload  (slug: clawmart-upload, v1.0.3)
  - akshare-a-stock  (slug: akshare-a-stock, v1.0.2)

Include all? Or exclude specific files? (all / enter filenames to exclude)
```

Wait for user confirmation. Adjust the file list based on user input.

---

## Step 3: Sensitive Information Check

Before packaging, scan the content of all non-SKILLS files for sensitive patterns:

- Strings matching `(sk-|cm_|ghp_|ghs_|ghu_)[A-Za-z0-9]{20,}` (API keys/tokens)
- Strings matching `(password|passwd|secret|api_key)\s*[:=]\s*\S+` (credentials)
- Any string longer than 20 chars after `Bearer ` or `Token `

If any sensitive pattern is found, tell the user exactly which file and line, and ask:
> Sensitive information detected in {filename} at line {line}: `{masked_value}`. It is recommended to remove it before uploading. Continue anyway? (y/n)

Only proceed if user says yes.

---

## Step 4: Collect Pack Metadata

Ask the user for:

1. **Title**: What is the name of this Pack? (e.g., Deep Research Analyst)
2. **Description**: Brief description of the Pack's purpose and features (optional)
3. **Version**: Version number? (default: `1.0.0`)

Check ClawMart if the user already has a pack with the same title:
```
GET {base_url}/api/packs/search?q={title}
Authorization: Bearer {token}
```

If a matching pack already exists, ask:
> A pack named "{title}" already exists. Upload as new version {new_version}? (y/n)

If yes, note this for the upload.

---

## Step 5: Create ZIP Package

Create a ZIP file in a temporary location (e.g., `/tmp/clawmart-{random}.zip`) containing:

- All confirmed local files from Step 2, placed at the root of the zip
- **No subdirectories** for non-skill files
- LOCAL SKILLS files placed in a `skills/` subdirectory within the zip
- A `skills-manifest.json` file in the zip root listing external skills metadata:

```json
{
  "clawhub_skills": [
    {
      "slug": "clawmart-upload",
      "version": "1.0.3",
      "ownerId": "kn75zb53cxzhkd8ep0zbsbq6gx82v7fj"
    },
    {
      "slug": "akshare-a-stock",
      "version": "1.0.2",
      "ownerId": "abc123..."
    }
  ]
}
```

Verify the zip does not contain any `../` path traversal patterns.

---

## Step 6: Upload to ClawMart

Send the upload request:

```
POST {base_url}/api/packs
Authorization: Bearer {token}
Content-Type: multipart/form-data

Fields:
  file:        <the zip file>
  title:       <user provided title>
  description: <user provided description>
  version:     <version>
```

**On success** (HTTP 201), tell the user:
> Pack "{title}" has been submitted for review. It is typically approved within 24 hours.
> View status: {base_url}/dashboard/packs

**On error**, show the error message and stop.

---

## Step 7: Cleanup

Delete the temporary zip file created in Step 5.

---

## Notes

- Local skill file **contents** are included in the zip under `skills/`
- External skills are recorded in `skills-manifest.json` — name, source, and version only, no file content
- The token is stored locally and reused on future uploads
- If the token is rejected (401), ask the user to generate a new one at `{base_url}/dashboard/tokens`

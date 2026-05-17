---
name: facebook-posting
description: OpenClaw skill for posting to Facebook Pages from the terminal
---

# Facebook Posting Skill

OpenClaw skill for posting to Facebook Pages from the terminal.

## Overview

This skill provides a complete CLI for managing Facebook Page posts, including:
- Immediate posting
- Image posting
- Scheduled posts
- Draft management
- Post deletion

## Required Inputs

- **Facebook Page ID**: The unique identifier of your Facebook Page
- **Page Access Token**: A valid Page Access Token with required permissions
- **Configuration File**: `facebook-posting.json` in your OpenClaw workspace

## Expected Outputs

- Successful post creation with post ID
- Scheduled post confirmation with schedule ID
- List of scheduled posts or drafts
- Error messages with actionable troubleshooting steps

## Installation

The skill is installed automatically when you run any `fb-post-*` command.

## Installation

The skill is installed automatically when you run any `fb-post-*` command.

## Commands

### Setup & Configuration

#### `openclaw fb-post-setup <page_id> <access_token> [page_name]`

Configure Facebook Page posting.

**Arguments:**
- `page_id` - Your Facebook Page ID
- `access_token` - Your Facebook Page Access Token
- `page_name` - Optional: Your Page name (will be fetched if not provided)

**Example:**
```bash
openclaw fb-post-setup "123456789" "EAAB...token..." "My Business Page"
```

**Getting Your Token:**
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app
3. Click "Get Token" → "Get Page Access Token"
4. Select permissions: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
5. Select your Page
6. Copy the generated token

**Getting Your Page ID:**
- From Facebook: Go to your Page → About → Page Info
- From Graph API: `https://graph.facebook.com/me/accounts?access_token=YOUR_TOKEN`

#### `openclaw fb-post-setup-help`

Display the complete setup guide.

#### `openclaw fb-post-test`

Test your Facebook Page connection and permissions.

Verifies:
- Configuration file exists
- API connectivity
- Page access
- Post permissions

### Posting

#### `openclaw fb-post "<message>"`

Post a message immediately.

**Example:**
```bash
openclaw fb-post "Hello from OpenClaw!"
```

#### `openclaw fb-post-image "<caption>" "<image_url>"`

Post an image with a caption.

**Example:**
```bash
openclaw fb-post-image "Check this out!" "https://example.com/image.jpg"
```

**Note:** The image URL must be publicly accessible.

### Scheduling

#### `openclaw fb-post-schedule "<message>" "<time>"`

Schedule a post for later publication.

**Time Formats:**
- Natural language: `"tomorrow 9am"`, `"in 2 hours"`, `"next monday"`
- ISO format: `"2024-12-31T23:59:59Z"`

**Examples:**
```bash
openclaw fb-post-schedule "Morning post!" "tomorrow 9am"
openclaw fb-post-schedule "Weekend sale!" "next monday 10am"
openclaw fb-post-schedule "Countdown!" "in 2 hours"
openclaw fb-post-schedule "New Year!" "2024-12-31T23:59:59Z"
```

#### `openclaw fb-post-schedule-list`

List all scheduled posts.

**Options:**
- `--limit <n>` - Maximum number to show (default: 50)

#### `openclaw fb-post-schedule-delete <post_id>`

Cancel a scheduled post.

**Example:**
```bash
openclaw fb-post-schedule-delete "123456789"
```

### Management

#### `openclaw fb-post-drafts`

List draft posts on your Page.

**Options:**
- `--limit <n>` - Maximum number to show (default: 50)

#### `openclaw fb-post-delete <post_id>`

Delete a post permanently.

**Example:**
```bash
openclaw fb-post-delete "123456789"
```

**Note:** This action requires confirmation unless `--confirm` flag is used.

## Configuration

Configuration is stored in `facebook-posting.json` in your OpenClaw workspace:

```json
{
  "page_id": "123456789",
  "access_token": "EAAB...",
  "page_name": "My Business Page",
  "created_at": "2024-01-01T00:00:00.000Z"
}
```

## Security

- Never share your access token
- Page tokens last 60 days
- Regenerate if compromised
- Use Page tokens, not User tokens

## Operational Notes

- Handle rate limits gracefully with retry logic
- Log minimal identifiers only (post IDs, not content)
- Validate image URLs before posting
- Confirm destructive actions (deletion) unless `--confirm` flag is used

## Troubleshooting

### Token Expired (Error 190)
- Regenerate token at https://developers.facebook.com/tools/explorer/
- Page tokens last 60 days

### Missing Permissions (Error 10)
- Regenerate token with required permissions:
  - `pages_manage_posts`
  - `pages_read_engagement`
  - `pages_show_list`

### Invalid Page ID
- Verify the Page ID is correct
- Check that the token has access to that Page

### Image Not Posting
- Ensure the image URL is publicly accessible
- Facebook may block certain URLs

## Resources

- [Facebook Graph API](https://developers.facebook.com/docs/pages/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Discord](https://discord.com/invite/clawd)

# Facebook Posting Skill

OpenClaw skill for posting to Facebook Pages from the terminal.

## Quick Start

1. **Setup:**
   ```bash
   openclaw fb-post-setup <page_id> "<access_token>" "Page Name"
   ```

2. **Test:**
   ```bash
   openclaw fb-post-test
   ```

3. **Post:**
   ```bash
   openclaw fb-post "Hello from OpenClaw!"
   ```

## Getting Your Facebook Token

1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app
3. Click "Get Token" → "Get Page Access Token"
4. Select permissions: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
5. Select your Page
6. Copy the generated token

## Commands

| Command | Description |
|---------|-------------|
| `openclaw fb-post-setup` | Configure Facebook Page |
| `openclaw fb-post-test` | Test connection |
| `openclaw fb-post "<msg>"` | Post immediately |
| `openclaw fb-post-image "<caption>" "<url>"` | Post an image |
| `openclaw fb-post-schedule "<msg>" "<time>"` | Schedule a post |
| `openclaw fb-post-schedule-list` | List scheduled posts |
| `openclaw fb-post-schedule-delete <id>` | Cancel scheduled post |
| `openclaw fb-post-drafts` | List draft posts |
| `openclaw fb-post-delete <id>` | Delete a post |
| `openclaw fb-post-setup-help` | Full setup guide |

## Time Formats

- `"tomorrow 9am"`
- `"in 2 hours"`
- `"next monday"`
- `"2024-12-31T23:59:59Z"`

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## Resources

- [Facebook Graph API](https://developers.facebook.com/docs/pages/)
- [OpenClaw Docs](https://docs.openclaw.ai)

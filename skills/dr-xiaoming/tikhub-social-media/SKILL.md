---
name: tikhub-social-media
version: 1.0.0
description: >
  Query social media data via TikHub API (https://api.tikhub.io). Covers 20+ platforms:
  Douyin, TikTok, Xiaohongshu, Instagram, YouTube, Twitter/X, Threads, Reddit, LinkedIn,
  Weibo, Kuaishou, Bilibili, WeChat (MP + Channels), Zhihu, Toutiao, Xigua, PiPiXia, Lemon8, NetEase Music.
  Capabilities: user profiles, post/video details, search (keyword/hashtag/user), comments,
  followers/following, trending/hot lists, hashtag/challenge data, live streams, creator analytics.
  Use when: user asks to search social media, fetch platform data, get influencer/KOL info,
  analyze social content, retrieve post/video details by URL or ID, check trending topics,
  or any social media data retrieval task.
  NOT for: web scraping (use scrapling), non-social-media data, posting/interaction actions.
metadata:
  openclaw:
    requires:
      envs:
        - TIKHUB_API_KEY
---

# TikHub Social Media Data Query

## Setup (Required)

Set your API key before using this skill:

```bash
export TIKHUB_API_KEY="<your-tikhub-api-key>"
```

Get your API key at: https://tikhub.io (register → dashboard → API Keys)

Optional proxy (if TikHub API is blocked in your network):
```bash
export TIKHUB_PROXY="http://your-proxy:port"
```

## Authentication

- **Base URL**: `https://api.tikhub.io`
- **Auth Header**: `Authorization: Bearer <TIKHUB_API_KEY>`
- All responses: unified `ResponseModel` → `{code, message, data, cache_url, ...}`
- Check balance: `GET /api/v1/tikhub/user/get_user_info`

## Helper Script

Use `scripts/tikhub_query.py` for all API calls:

```bash
python3 scripts/tikhub_query.py <endpoint_path> [param=value ...] [--method POST] [--body '{}']
```

Examples:
```bash
# Search Douyin videos
python3 scripts/tikhub_query.py /api/v1/douyin/web/fetch_search keyword=宁德时代

# Get TikTok user profile
python3 scripts/tikhub_query.py /api/v1/tiktok/web/fetch_user_profile secUid=MS4wLjABAAAA...

# Search Xiaohongshu notes
python3 scripts/tikhub_query.py /api/v1/xiaohongshu/web/get_note_by_keyword keyword=CATL

# Get Instagram user info
python3 scripts/tikhub_query.py /api/v1/instagram/v1/fetch_user_info username=cataborrecycling

# Search Twitter
python3 scripts/tikhub_query.py /api/v1/twitter/web/fetch_search_timeline keyword="CATL battery"

# Search YouTube
python3 scripts/tikhub_query.py /api/v1/youtube/web/search_videos keyword="CATL solid state battery"

# Get Weibo hot search
python3 scripts/tikhub_query.py /api/v1/weibo/web/fetch_hot_search

# Hybrid parse any video URL
python3 scripts/tikhub_query.py /api/v1/hybrid/video_data url=https://v.douyin.com/xxx
```

## Platform Quick Reference

### Endpoint Naming Convention
All endpoints follow: `/api/v1/{platform}/{source}/{action}`
- `platform`: douyin, tiktok, xiaohongshu, instagram, youtube, twitter, weibo, kuaishou, bilibili, etc.
- `source`: web, app, app/v3, web_v2, etc.
- `action`: fetch_user_profile, fetch_one_video, fetch_search, etc.

### Core Actions (available on most platforms)

| Action Pattern | Purpose |
|---|---|
| `fetch_user_profile` / `fetch_user_info` | Get user/account details |
| `fetch_user_post` / `fetch_user_posts` | Get user's posts/videos |
| `fetch_one_video` / `fetch_post_detail` | Get single post/video by ID |
| `fetch_search` / `search` | Keyword search |
| `fetch_post_comments` / `fetch_comments` | Get comments on a post |
| `fetch_user_fans` / `fetch_user_followers` | Follower list |
| `fetch_user_follow` / `fetch_user_followings` | Following list |
| `fetch_trending` / `fetch_hot_search` | Trending/hot topics |

### Platform → Preferred API Version

| Platform | Preferred Prefix | Notes |
|---|---|---|
| 抖音 Douyin | `/api/v1/douyin/web/` or `/api/v1/douyin/app/v3/` | Web for search, App V3 for details |
| 抖音搜索 | `/api/v1/douyin/search/` | Dedicated search APIs (latest) |
| 抖音创作者 | `/api/v1/douyin/creator_v2/` | Requires creator cookie |
| 抖音热榜 | `/api/v1/douyin/billboard/` | Hot lists, trending |
| 抖音星图 | `/api/v1/douyin/xingtu_v2/` | KOL marketplace data |
| TikTok | `/api/v1/tiktok/web/` or `/api/v1/tiktok/app/v3/` | Web for search, App V3 for details |
| 小红书 XHS | `/api/v1/xiaohongshu/app_v2/` | Most stable, recommended |
| Instagram | `/api/v1/instagram/v1/` | Prefer V1, V2/V3 as fallback |
| YouTube | `/api/v1/youtube/web/` | V2 for additional features |
| Twitter/X | `/api/v1/twitter/web/` | Search, user, posts, trending |
| Threads | `/api/v1/threads/web/` | User, posts, search |
| Reddit | `/api/v1/reddit/app/` | Full featured app API |
| LinkedIn | `/api/v1/linkedin/web/` | Profiles, posts, search |
| 微博 Weibo | `/api/v1/weibo/web_v2/` | V2 recommended |
| 快手 Kuaishou | `/api/v1/kuaishou/web/` or `/api/v1/kuaishou/app/` | |
| B站 Bilibili | `/api/v1/bilibili/web/` | |
| 微信公众号 | `/api/v1/wechat_mp/web/` | Article extraction |
| 微信视频号 | `/api/v1/wechat_channels/` | Requires special params |
| 知乎 Zhihu | `/api/v1/zhihu/web/` | Q&A, articles, search |
| 今日头条 | `/api/v1/toutiao/web/` or `/api/v1/toutiao/app/` | |
| Lemon8 | `/api/v1/lemon8/app/` | |

### Pagination

Most list endpoints support cursor-based pagination:
- `cursor` / `max_cursor` / `offset` / `after` — pass from previous response
- `count` / `page_size` — items per page (typically 10-30)
- Response includes `has_more`, `cursor`, `next_cursor` etc.

### Hybrid Video Parser

Parse any video URL from supported platforms automatically:
```
GET /api/v1/hybrid/video_data?url=<any_video_url>
```
Supports: Douyin, TikTok, Xiaohongshu, Kuaishou, Bilibili, Weibo, etc.

## Detailed Platform References

For full endpoint lists per platform, read the corresponding reference file:

- **references/douyin.md** — Douyin (Web + App + Search + Billboard + Creator + Xingtu)
- **references/tiktok.md** — TikTok (Web + App + Creator + Analytics + Ads + Shop)
- **references/xiaohongshu.md** — Xiaohongshu (App V2 + Web V2)
- **references/instagram.md** — Instagram (V1 + V2 + V3)
- **references/youtube.md** — YouTube (Web + V2)
- **references/twitter-threads.md** — Twitter/X + Threads
- **references/reddit-linkedin.md** — Reddit + LinkedIn
- **references/chinese-platforms.md** — Weibo, Kuaishou, Bilibili, WeChat, Zhihu, Toutiao, etc.

Only read the relevant reference file when you need endpoint details for a specific platform.

## Cost Awareness

- Most endpoints: $0.001-$0.005 per call
- Some premium endpoints (Instagram, creator analytics): up to $0.01
- Always prefer cached results when `cache_url` is returned
- Batch operations where available (e.g., Reddit batch post details)
- Check balance before bulk operations: `GET /api/v1/tikhub/user/get_user_info`

---
name: videodown
description: Download videos from YouTube and Bilibili with search. Use when users ask to find or download videos. Supports natural language like "find a 3 minute lol video". No API key needed.
homepage: https://github.com/chenlong1314/videodown
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["yt-dlp", "ffmpeg", "jq"] } } }
---

# 🎬 videodown

Download videos from YouTube and Bilibili with built-in search.

## When to Use

✅ **USE this skill when:**

### Download & Search
- "Download this video" + URL
- "Find a [topic] video"
- "Search for [keyword] on YouTube/Bilibili"
- "Get a 3 minute video about [topic]"
- "Download audio from [URL]"

### Video Editing & Assets
- "Get video assets for editing"
- "Download video clips for my project"
- "Find background video footage"
- "Download tutorial video for reference"
- "Get video素材 (video assets)"
- "下载剪辑素材"
- "找视频素材"

### Content Creation
- "Download video for content creation"
- "Get video for my YouTube channel"
- "Download reference video"
- "找创作素材"
- "下载参考视频"

### Audio Extraction
- "Extract audio from video"
- "Convert video to MP3"
- "Get background music from video"
- "提取音频"
- "转 MP3"

### Chinese Natural Language
- "下载 lol 视频"
- "找个 3 分钟的视频"
- "提取这个视频的音频"
- "搜索 B 站的教程视频"
- "下载剪辑素材"
- "找视频创作素材"

## When NOT to Use

❌ **DON'T use this skill when:**

- Live streaming → use streaming tools
- Private/restricted videos → may require authentication
- Bulk downloading playlists → use specialized tools
- Commercial use → respect copyright

## Quick Start

### Install

```bash
# From GitHub
git clone https://github.com/chenlong1314/videodown.git
cd videodown && npm install && npm link

# Install dependencies
brew install yt-dlp ffmpeg jq
```

### Basic Usage

```bash
# Download video from URL
videodown https://youtube.com/watch?v=xxx

# Search and download
videodown search "lol highlights"

# Search with filters
videodown search "tutorial" --duration medium --platform youtube
```

## Natural Language Examples

Users can say:

- "找个 lol 视频" → `search "lol"`
- "找个 3 分钟的 lol 视频下载" → `search "lol" --duration short --select 1`
- "下载这个" + URL → `download <url>`
- "找 B 站的 lol 视频" → `search "lol" --platform bilibili`
- "只要音频" + URL → `<url> --audio-only`

## Command Reference

### Download

```bash
videodown <url>                      # Download video
videodown <url> --quality 1080p      # Specify quality
videodown <url> --output ~/Videos/   # Custom output
videodown <url> --audio-only         # Extract audio (MP3)
videodown <url> --convert            # Convert to H.264 (QuickTime compatible)
```

### Search

```bash
videodown search "keyword"                    # Search both platforms
videodown search "keyword" --platform youtube # YouTube only
videodown search "keyword" --platform bilibili # Bilibili only
videodown search "keyword" --duration short   # <4 minutes
videodown search "keyword" --select 1         # Download 1st result
```

### History

```bash
videodown history           # View download history
videodown history --limit 20 # Show last 20 items
```

### Parameters

- `--quality`: `360p`, `720p`, `1080p`, `best` (default)
- `--platform`: `youtube`, `bilibili`, `all` (default)
- `--duration`: `short` (<4m), `medium` (4-20m), `long` (>20m)
- `--output`: Any path (default: `~/Downloads/videodown`)

## Common Patterns

**Download from URL:**
```bash
videodown https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Find and download:**
```bash
videodown search "lol highlights" --select 1
```

**Find short videos:**
```bash
videodown search "tutorial" --duration short
```

**Extract audio:**
```bash
videodown https://youtube.com/watch?v=xxx --audio-only
```

## Notes

- **Download Location**: `~/Downloads/videodown` (customizable with `--output`)
- **History**: Last 50 downloads saved to `history.json`
- **Copyright**: For personal use only
- **Rate limits**: Search <10 times/minute
- **Bilibili HQ**: Requires login cookie for 4K/8K
- **Dependencies**: yt-dlp, ffmpeg, jq (auto-check on install)

## Development

```bash
git clone https://github.com/chenlong1314/videodown.git
cd videodown
npm install
npm start -- search "test"
```

## Links

- [GitHub](https://github.com/chenlong1314/videodown)
- [Issues](https://github.com/chenlong1314/videodown/issues)

## Interaction Strategy

### Error Handling (Phase 1)

The skill implements 7 error types with user-friendly messages and quick recovery options:

| Error Type | Code | User Message | Quick Actions |
|-----------|------|--------------|---------------|
| Download Failed | `ERR_DOWNLOAD` | Video temporarily unavailable | Retry, Search Similar |
| No Search Results | `ERR_SEARCH` | No videos found for keyword | Retry with different keyword |
| Network Error | `ERR_NETWORK` | Connection interrupted | Retry (supports resume) |
| Copyright Restricted | `ERR_COPYRIGHT` | Copyright protected content | Search Similar |
| Invalid URL | `ERR_INVALID_URL` | URL not recognized | Re-enter URL |
| Unsupported Format | `ERR_FORMAT` | Format not supported | Choose MP4/MP3 |
| Storage Full | `ERR_STORAGE` | Insufficient storage | Lower quality, Audio only |

Each error provides:
- Clear explanation of the issue
- Possible causes
- Actionable suggestions
- Quick recovery buttons/commands

### Confirmation Mechanism (Phase 2)

Automatic confirmation prompts for:

1. **Large Files (>500MB)**: Explicit size warning with estimated time
2. **Batch Downloads (>5 items)**: List all items with total size
3. **Audio Extraction**: Format confirmation (MP3 320kbps)

Confirmation messages include:
- Video title, platform, duration
- File size estimate
- Format information
- Quick confirm/cancel options

### Progress Display (Phase 3)

- **Search Results**: Formatted table with thumbnail preview
- **Download Progress**: Progress bar with speed and ETA
- **Completion Notice**: File info with quick actions (open folder, extract audio, delete)

### Quick Commands (Phase 4)

Available commands in interactive mode:

| Command | Description | Example |
|---------|-------------|---------|
| `/search <keyword>` | Search videos | `/search lol` |
| `/download <URL>` | Download video | `/download https://...` |
| `/audio <URL>` | Extract audio | `/audio https://...` |
| `/history` | View history | `/history` |
| `/cancel` | Cancel current task | `/cancel` |
| `/help` | Show help | `/help` |

## Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download engine
- [BBDown](https://github.com/nilaoda/BBDown) - Bilibili downloader

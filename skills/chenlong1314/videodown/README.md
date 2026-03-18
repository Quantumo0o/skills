# 🎬 videodown - Video Downloader for YouTube & Bilibili

> Download, Search, Extract Audio | 视频下载·搜索·音频提取
> 
> Perfect for: Video Editing, Content Creation, Asset Collection | 视频剪辑·内容创作·素材获取

[![npm version](https://img.shields.io/npm/v/videodown.svg)](https://www.npmjs.com/package/videodown)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/chenlong1314/videodown)](https://github.com/chenlong1314/videodown)

**[📖 中文文档](README_CN.md)**

---

## ✨ Features

- 🔍 **Search + Download** - Search videos by keyword and download in one step
- 🎯 **Dual Platform** - YouTube and Bilibili support with unified interface
- 🚀 **Easy Install** - Auto-check and install dependencies
- 💬 **Natural Language** - Support commands like "find a 3 minute lol video"
- 📦 **npm Package** - Install with one command

---

## 📦 Installation

### Option 1: From GitHub (Recommended)

```bash
# Clone repository
git clone https://github.com/chenlong1314/videodown.git
cd videodown

# Install dependencies
npm install

# Make globally available
npm link

# Install system dependencies
brew install yt-dlp ffmpeg jq  # macOS
sudo apt install yt-dlp ffmpeg jq  # Linux
```

### Option 2: npm (Coming Soon)

```bash
npm install -g videodown
```

### Option 3: npx (No Install)

```bash
npx videodown search "lol highlights"
```

---

## 🚀 Quick Start

### Download Video

```bash
# Download from URL
videodown https://www.youtube.com/watch?v=xxx

# Specify quality
videodown --url https://youtube.com/watch?v=xxx --quality 1080p

# Extract audio only
videodown --url https://youtube.com/watch?v=xxx --audio-only
```

### Search Videos

```bash
# Search both platforms
videodown search "lol highlights"

# Search YouTube only
videodown search "tutorial" --platform youtube

# Search Bilibili only
videodown search "教程" --platform bilibili

# Filter by duration
videodown search "tutorial" --duration short  # <4 minutes
videodown search "tutorial" --duration medium # 4-20 minutes

# Search and download 1st result
videodown search "lol" --select 1
```

---

## 💬 Natural Language Examples

When using with AI assistants, you can say:

| User Says | AI Calls |
|-----------|----------|
| "Find a lol video" | `search "lol"` |
| "Download a 3 minute lol video" | `search "lol" --duration short --select 1` |
| "Download this video" + URL | `download <url>` |
| "Find Bilibili lol video" | `search "lol" --platform bilibili` |
| "Just the audio" + URL | `<url> --audio-only` |

---

## 📋 Command Reference

### Download Command

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--quality` | `-q` | Video quality | `best` |
| `--output` | `-o` | Output directory | `./downloads` |
| `--format` | `-f` | Output format | `mp4` |
| `--audio-only` | `-a` | Extract audio only | `false` |

**Quality options:** `360p`, `720p`, `1080p`, `best`

### Search Command

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--platform` | `-p` | Search platform | `all` |
| `--limit` | `-l` | Number of results | `10` |
| `--duration` | `-d` | Duration filter | - |
| `--select` | `-s` | Download Nth result | - |

**Platform options:** `youtube`, `bilibili`, `all`

**Duration options:**
- `short` - Less than 4 minutes
- `medium` - 4 to 20 minutes
- `long` - More than 20 minutes

---

## 🎯 Common Use Cases

### 1. Download Known URL

```bash
videodown https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 2. Search and Choose

```bash
videodown search "lol highlights"
# Shows results table, enter number to download
```

### 3. One-Click Download

```bash
videodown search "lol" --select 1
# Downloads 1st result automatically
```

### 4. Filter by Duration

```bash
videodown search "tutorial" --duration medium
# Find 4-20 minute videos
```

### 5. Platform Specific

```bash
videodown search "原神" --platform bilibili
# Search Bilibili only
```

### 6. Extract Audio

```bash
videodown --url https://youtube.com/watch?v=xxx --audio-only
# Download as MP3
```

---

## ⚠️ Notes

- **Copyright**: For personal use only
- **Rate Limits**: Search <10 times/minute
- **Bilibili HQ**: Requires login cookie for 4K/8K
- **Dependencies**: yt-dlp, ffmpeg, jq (auto-checked on install)

---

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/chenlong1314/videodown.git
cd videodown

# Install dependencies
npm install

# Run locally
npm start -- search "test"
```

---

## 💬 Quick Commands

Enter interactive mode for quick commands:

```bash
videodown interactive
# or
videodown i
```

Available commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/search <keyword>` | Search videos | `/search lol` |
| `/download <URL>` | Download video | `/download https://youtube.com/watch?v=xxx` |
| `/audio <URL>` | Extract audio | `/audio https://youtube.com/watch?v=xxx` |
| `/history` | View download history | `/history` |
| `/cancel` | Cancel current task | `/cancel` |
| `/help` | Show help information | `/help` |

## 🎯 Interaction Features

### Error Handling

- 7 error types with user-friendly messages
- Quick recovery options (retry, search similar, etc.)
- Clear explanations and suggestions

### Confirmation Mechanism

- **Large files (>500MB)**: Size warning with estimated time
- **Batch downloads (>5 items)**: Quantity confirmation
- **Audio extraction**: Format confirmation

### Progress Display

- Search results with thumbnail preview
- Download progress bar with speed and ETA
- Completion notice with quick actions

## 📄 License

MIT License

---

## 🔗 Links

- [GitHub](https://github.com/chenlong1314/videodown)
- [Issues](https://github.com/chenlong1314/videodown/issues)
- **[Chinese Docs](README_CN.md)**

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download engine
- [BBDown](https://github.com/nilaoda/BBDown) - Bilibili downloader
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) - Bilibili API docs

---

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.2.0 | 2026-03-18 | Interaction strategy optimization (7 error types, confirmation prompts, progress display, quick commands) |
| v1.1.0 | 2026-03-18 | Added interaction strategy (error handling, confirmation, quick commands) |
| v1.0.0 | 2026-03-18 | Initial release |

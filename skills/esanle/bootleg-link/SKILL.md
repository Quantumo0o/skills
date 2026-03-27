---
name: bootleg-link
description: Download music from YouTube channels/playlists and convert to 320kbps MP3. Supports batch processing, resume interrupted downloads, and concurrent downloading.
metadata: {"clawdbot":{"emoji":"🎵","os":["linux","macos"],"requires":{"bins":["yt-dlp","ffmpeg"]}}}
---

# Bootleg-Link Skill

DJ music downloader - Downloads music from YouTube channels/playlists and converts to high-quality MP3.

## What It Does

Download music from YouTube channels or playlists, convert to 320kbps MP3 with metadata, and manage batch downloads with resume capability.

## Features

- **Batch Download**: Process multiple channels/playlists from a text file
- **Resume Support**: Skip already downloaded videos using `--download-archive`
- **High Quality**: Convert to 320kbps MP3 with thumbnail embedding
- **Smart Deduplication**: Automatically skip previously downloaded content
- **Concurrent Download**: Utilize multiple CPU cores for parallel downloads

## Usage

### Single Channel/Playlist
```bash
bootleg-link "https://www.youtube.com/@VeryHouseMusic"
```

### Batch Mode
```bash
bootleg-link --batch /path/to/channels.txt
```

### Resume Interrupted Download
```bash
bootleg-link --batch /path/to/output/directory
```

### Custom Output Directory
```bash
bootleg-link "https://www.youtube.com/@ChannelName" -o /path/to/output
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BOOTLEG_OUTPUT_DIR` | `/mnt/e/bootleg-link-downloader/output` | Default output directory |
| `BOOTLEG_QUALITY` | `320` | MP3 bitrate (128, 192, 256, 320) |
| `BOOTLEG_CONCURRENCY` | `8` | Number of concurrent downloads |
| `BOOTLEG_ARCHIVE_FILE` | `download-archive.txt` | File to track downloaded videos |

### Link File Format (`.bootleg-link.txt`)
```
https://www.youtube.com/@Channel1
https://www.youtube.com/playlist?list=PLxxx
https://www.youtube.com/@Channel2
```

## Advanced Options

### CPU-Based Concurrency
Automatically adjusts based on CPU cores:

| CPU Cores | Videos | Fragments per Video |
|-----------|--------|---------------------|
| 4 | 2 | 2 |
| 8 | 4 | 4 |
| 16 | 8 | 4 |
| 32+ | 16 | 8 |

Use `-N` for concurrent videos and `--concurrent-fragments` for per-video parallelism.

### Custom Filename Template
```bash
--output-template "%(title)s.%(ext)s"
```

### Audio Format Options
```bash
--format bestaudio --extractor-args "youtube:player_client=android"
```

## Troubleshooting

### JS Challenge Error
If YouTube JS challenge decryption fails, it falls back to format 251 (opus 128kbps) - still good quality.

### Network Timeout
Auto-retries on timeout. For persistent issues, increase `--socket-timeout`.

### Rate Limiting
Add `--sleep-interval` between downloads:
```bash
bootleg-link --batch . --sleep-interval 5
```

## Dependencies

- **yt-dlp**: YouTube downloader
- **ffmpeg**: Audio conversion
- **mutagen** (optional): For metadata embedding

## Installation

```bash
# Install dependencies
pip install yt-dlp mutagen

# Make executable (if provided as script)
chmod +x bootleg-link
```

## Example Output

```
[download] Downloading channel: VeryHouseMusic
[download] Channel has 9926 videos
[download] Already downloaded: 388 / 9926 (3.9%)
[download] Starting download of remaining 9538 videos...
[download] Output: /mnt/e/bootleg-link-downloader/output/house(VeryHouseMusic Dump)/
```

## Notes

- Uses `--download-archive` to track downloaded videos
- Automatically creates playlist-named subdirectories
- Embeds thumbnail as album art in MP3 files
- Run again with same output dir to resume seamlessly
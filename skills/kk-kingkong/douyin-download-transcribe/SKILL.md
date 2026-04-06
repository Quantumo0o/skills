---
name: video-download-transcribe
description: |
  多平台视频下载 + 本地转录 + 视频内容分析。
  
  **触发词**：这个视频说了什么、视频内容是什么、帮我看这个视频、下载这个视频、视频转录、字幕提取、B站视频、抖音视频、bilibili、youtube视频、帮我转录

  **支持平台**：B站/抖音/TikTok/YouTube/小红书/微博/快手
  **下载**：yt-dlp 免费优先，tikhub 保底；MLX Whisper 原生 Apple Silicon GPU 加速，faster-whisper CPU/GPU 通用兜底。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["ffmpeg", "yt-dlp"],
          },
      },
  }
---

# 多平台视频下载 + 本地转录

## 功能特点

- ✅ **yt-dlp 免费下载** — B站/抖音/TikTok/YouTube/小红书/微博/快手
- ✅ **MLX Whisper** — Apple Silicon 原生 Metal GPU 加速（Mac M系列首选）
- ✅ **faster-whisper** — CPU/CUDA 通用兜底（非 Apple Silicon 也能用）
- ✅ **短视频同步转录** — <5 分钟视频直接返回完整结果
- ✅ **长视频后台转录** — ≥5 分钟自动后台运行，返回 transcript_id 可查询
- ✅ **可检索** — 转录结果支持关键词查询相关片段 + 时间戳

## 支持的平台

| 平台 | 检测关键词 |
|------|-----------|
| B站 | `bilibili.com/video`, `b23.tv`, `BV号` |
| 抖音 | `douyin.com`, `v.douyin.com` |
| TikTok | `tiktok.com` |
| YouTube | `youtube.com`, `youtu.be` |
| 小红书 | `xiaohongshu.com`, `xhslink.com` |
| 微博 | `weibo.com`, `m.weibo.cn` |
| 快手 | `kuaishou.com`, `ksurl.cn` |

## MCP 工具（9个）

### analyze_video（分析视频）
```bash
mcporter call douyin-analyzer.analyze_video url="https://..."
```
- **短视频（<5min）**：同步返回 transcript + segments
- **长视频（≥5min）**：立即返回 transcript_id，后台转录中

### get_transcript（获取转录结果）
```bash
mcporter call douyin-analyzer.get_transcript transcript_id="<id>"
```

### query_transcript（检索转录内容）
```bash
mcporter call douyin-analyzer.query_transcript transcript_id="<id>" query="关键词" top_k=3
```

### get_video_info（仅获取信息）
```bash
mcporter call douyin-analyzer.get_video_info url="https://..."
```

### download_video（下载到本地）
```bash
mcporter call douyin-analyzer.download_video url="https://..." output_dir="/tmp/"
```

## 返回结构

```json
{
  "status": "ready",
  "transcript_id": "47cd0a6f47d2",
  "video_info": { "title": "...", "duration": 885, "uploader": "..." },
  "transcript": "完整转录文本...",
  "segments": [
    { "start": 0.0, "end": 5.5, "text": "今天我们来聊..." },
    ...
  ]
}
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TRANSCRIPTS_DIR` | `~/.openclaw/video-transcripts` | 转录结果存储目录 |
| `DURATION_THRESHOLD` | `300`（秒） | 超过则后台转录 |
| `WHISPER_MODEL` | `small` | Whisper 模型：tiny/base/small/medium/large |
| `TIKHUB_API_KEY` | 空 | 付费备用下载方案 |

## 工作流程

```
发送视频链接 → analyze_video
    ├── <5min：直接返回 transcript + segments
    └── ≥5min：返回 transcript_id
              → 等待几秒 → get_transcript transcript_id
              → 拿到 transcript + segments
              → 直接让我总结 / query_transcript 检索关键词
```

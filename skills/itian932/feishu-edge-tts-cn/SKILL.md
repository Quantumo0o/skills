---
name: feishu-edge-tts-cn
description: Edge-TTS 在线语音合成 skill。基于微软 Edge TTS 引擎，生成速度快（1-2秒），支持多种音色和输出格式，默认输出 OGG/Opus。默认音色 xiaoxiao_lively。需联网。
---

# Edge-TTS 语音合成 Skill

## 概述

- **引擎**: edge-tts 7.2.8
- **路径**: `~/.openclaw/workspace/skills/feishu-edge-tts-cn/`
- **入口脚本**: `scripts/engine.py`
- **音色配置**: `config/voices.json`
- **速度**: 1-2 秒生成

## 官方音色

来自 Edge-TTS 引擎原始音色，使用默认参数。

### zh-CN（普通话）

| 音色 | 性别 | 音色 ID |
|------|------|---------|
| zh-CN-XiaoxiaoNeural | 女 | `xiaoxiao` |
| zh-CN-XiaoyiNeural | 女 | `xiaoyi` |
| zh-CN-YunjianNeural | 男 | `yunjian` |
| zh-CN-YunxiNeural | 男 | `yunxi` |
| zh-CN-YunxiaNeural | 男 | `yunxia` |
| zh-CN-YunyangNeural | 男 | `yunyang` |
| zh-CN-liaoning-XiaobeiNeural | 女 | `liaoning_xiaobei` |
| zh-CN-shaanxi-XiaoniNeural | 女 | `shaanxi_xiaoni` |

### zh-HK（粤语）

| 音色 | 性别 | 音色 ID |
|------|------|---------|
| zh-HK-HiuGaaiNeural | 女 | `hk_hiuGaai` |
| zh-HK-HiuMaanNeural | 女 | `hk_hiuMaan` |
| zh-HK-WanLungNeural | 男 | `hk_wanLung` |

### zh-TW（台湾）

| 音色 | 性别 | 音色 ID |
|------|------|---------|
| zh-TW-HsiaoChenNeural | 女 | `tw_hsiaoChen` |
| zh-TW-HsiaoYuNeural | 女 | `tw_hsiaoYu` |
| zh-TW-YunJheNeural | 男 | `tw_yunJhe` |

## 自定义音色

基于官方音色调试过 rate/pitch/volume 参数的音色。

| 音色 ID | 基础音色 | 参数 | 描述 |
|---------|---------|------|------|
| **xiaoxiao_lively**（默认） | xiaoxiao | +8%速 +10Hz +5%音量 | 女声 活泼偏高音 |
| xiaoxiao_gentle | xiaoxiao | +5%速 +4Hz | 女声 甜美温柔 |
| xiaoxiao_fast | xiaoxiao | +15%速 +2Hz +10%音量 | 女声 快速明亮 |
| xiaoxiao_slow | xiaoxiao | +5%速 -2Hz | 女声 温柔慢速 |
| xiaoyi_lively | xiaoyi | +15%速 +5Hz +10%音量 | 女声 卡通元气 |
| yunxi_sunny | yunxi | +15%速 +3Hz +5%音量 | 男声 阳光活泼 |

## 调用方式

### CLI

```bash
# 默认音色（xiaoxiao_lively），默认 .ogg 输出
python3 scripts/engine.py --text "你好呀"

# 指定音色
python3 scripts/engine.py --text "你好呀" --voice xiaoyi

# 指定输出格式（.ogg / .mp3 / .wav / .flac）
python3 scripts/engine.py --text "你好呀" --voice xiaoxiao_gentle --output /tmp/reply.mp3
python3 scripts/engine.py --text "你好呀" --output /tmp/goodnight.wav

# 列出全部音色
python3 scripts/engine.py --list-voices
```

### Python API & 飞书发送

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/skills/feishu-edge-tts-cn/scripts"))
from engine import generate

# 1. 生成语音，建议输出到 workspace 目录下
code, path = generate("你好呀", voice_id="xiaoxiao_lively")

# 2. 使用 OpenClaw message 工具发送（支持绝对路径，无需上传云空间）
# message.send(filePath=path)
```

> **💡 核心提示**：在 OpenClaw 环境中，生成 `.ogg` 文件后，直接使用 `message.send(filePath="/绝对路径/文件.ogg")` 即可实现语音消息推送。**不需要**先上传到飞书云空间再发送，这是最高效的用法！
>
> **📝 参数对比与推荐**：
> *   **`filePath` (🏆 强烈推荐)**：语义最清晰，专为本地文件设计，最稳定。
> *   **`path` (✅ 可用)**：`filePath` 的简写别名，功能一致。
> *   **`media` (⚠️ 慎用)**：通常用于网络 URL，虽然支持本地绝对路径，但在某些环境下可能触发“Invalid URL”警告。

## 输出格式

根据 `--output` 的扩展名自动选择编码器：

| 扩展名 | 编码器 | 采样率 | 声道 | 备注 |
|---|---|---|---|---|
| `.ogg` / `.opus` | libopus | 48kHz | mono | **默认/推荐**，voip 优化，64kbps |
| `.mp3` | libmp3lame | 48kHz | mono | 64kbps |
| `.wav` | pcm_s16le | 48kHz | mono | 无损 PCM |
| `.flac` | flac | 48kHz | mono | 无损压缩 |
| `.aac` | aac | 48kHz | mono | 64kbps |
| 未知 | 自动回退 `.ogg` | 48kHz | mono | 打印警告 |

## 输出路径与存放规范

> ⚠️ **重要：OpenClaw 媒体发送安全限制**
>
> 飞书消息发送（`message.send(filePath=...)`）仅允许读取以下“白名单”目录下的文件：
> 1. `/tmp/openclaw` (**推荐默认路径**)
> 2. `~/.openclaw/media`
> 3. `~/.openclaw/workspace`
> 4. `~/.openclaw/sandboxes`
>
> 请使用**绝对路径**发送文件，无需上传云空间。

默认路径：`/tmp/openclaw/edge_{音色ID}_{时间戳}.ogg`

飞书发送推荐格式：**OGG/Opus**

## 文本规范

- ✅ 使用中文标点（，。！？）
- ⚠️ 标点决定停顿：句号（。）= 长停顿，逗号（，）= 短停顿
- ✅ 可包含语气词

## 技术细节

### 处理流程

```
加载音色配置 → 申请速率许可 → Edge-TTS 生成 MP3 → ffmpeg 转目标格式 → 清理临时文件 → 返回路径
```

### 引擎特性

- **速率控制**：每秒最多 3 个请求（防 429 限速）
- **429 重试**：指数退避 1s → 2s → 4s，最多 3 次
- **临时文件**：MP3 中间文件生成后自动清理
- **整段合成**：不分段，直接处理完整文本
- **格式自适应**：根据输出扩展名自动选择编码器和参数

### 依赖

- Python 3.8+
- edge-tts 7.2.8
- ffmpeg

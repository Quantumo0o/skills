# Web Reader TTS - 网页内容朗读技能

将网页内容转换为语音，支持多种 TTS 引擎和 Whisper 语音识别。

## 快速开始

```bash
# 完整流程（网页 → 语音 → 识别）
python web_reader_tts.py --url "https://example.com"

# 仅生成语音
python web_reader_tts.py --url "https://example.com" --tts-only

# 仅语音识别
python web_reader_tts.py --audio "audio.mp3" --stt-only
```

## 依赖安装

```bash
pip install playwright edge-tts openai-whisper
python -m playwright install chromium
```

## 可用声音

### 中文女声
- `zh-CN-XiaoxiaoNeural` - 晓晓（推荐）
- `zh-CN-XiaoyiNeural` - 晓伊
- `zh-CN-XiaochenNeural` - 晓辰

### 中文男声
- `zh-CN-YunxiNeural` - 云希
- `zh-CN-YunyangNeural` - 云扬

### 英文女声
- `en-US-JennyNeural` - Jenny（推荐）
- `en-US-AriaNeural` - Aria

### 日文女声
- `ja-JP-NanamiNeural` - Nanami

## Whisper 模型对比

| 模型 | 大小 | 速度 | 准确率 | 推荐场景 |
|------|------|------|--------|----------|
| tiny | 39 MB | 最快 | 较低 | 快速预览 |
| base | 74 MB | 快 | 中等 | 平衡选择 |
| small | 244 MB | 中等 | 较高 | 日常使用 |
| medium | 769 MB | 较慢 | 高 | 中文推荐 |
| large-v3 | 1.55 GB | 最慢 | 最高 | 专业场景 |

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 网页 URL | - |
| `--audio` | 音频文件路径 | - |
| `--voice` | TTS 声音 | `zh-CN-XiaoxiaoNeural` |
| `--rate` | 语速 | `+0%` |
| `--volume` | 音量 | `+0%` |
| `--output` | 输出音频文件 | `audio.mp3` |
| `--whisper-model` | Whisper 模型 | `base` |
| `--language` | 语言 | `zh` |
| `--max-length` | 最大文本长度 | `2000` |

## 输出文件

- `audio.mp3` - 生成的语音文件
- `transcript.txt` - 语音识别结果

## 示例

### 示例 1：朗读新闻文章

```bash
python web_reader_tts.py --url "https://news.example.com/article/123"
```

### 示例 2：使用更准确的 Whisper 模型

```bash
python web_reader_tts.py --url "https://example.com" --whisper-model medium
```

### 示例 3：调整语速和音量

```bash
python web_reader_tts.py --url "https://example.com" --rate "+20%" --volume "+50%"
```

### 示例 4：使用英文女声

```bash
python web_reader_tts.py --url "https://example.com" --voice "en-US-JennyNeural" --language en
```

## 技术栈

- **Playwright** - 网页自动化
- **Edge TTS** - 微软免费 TTS 服务
- **OpenAI Whisper** - 开源语音识别

## 版本历史

- v1.0.0 (2026-04-13) - 初始版本

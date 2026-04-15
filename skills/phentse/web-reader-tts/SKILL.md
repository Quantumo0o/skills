# Web Reader TTS - 网页内容朗读技能

将网页内容转换为语音，支持多种 TTS 引擎和 Whisper 语音识别。

## 🎯 触发方式

### 自然语言触发

直接对我说：

- `朗读网址 https://example.com`
- `朗读这个网页 https://example.com`
- `把这篇文章读出来 https://example.com`
- `网页朗读 https://example.com`

### 多语言支持

自动检测网页语言，选择合适的 TTS 声音：

- **中文** → `zh-CN-XiaoxiaoNeural`（晓晓，女声）
- **英文** → `en-US-JennyNeural`（Jenny，女声）
- **日文** → `ja-JP-NanamiNeural`（Nanami，女声）
- **混合语言** → 自动切换声音

## 功能特性

- ✅ **Playwright 网页抓取**：自动提取网页正文内容
- ✅ **Edge TTS 语音合成**：免费、高质量、支持多种语言和声音
- ✅ **Whisper 语音识别**：免费、本地运行、默认 medium 模型
- ✅ **多语言检测**：自动检测文本语言，选择合适的声音
- ✅ **完整流程**：网页 → 文本 → 语音 → 识别

## 依赖安装

```bash
# Playwright
pip install playwright
python -m playwright install chromium

# Edge TTS
pip install edge-tts

# Whisper
pip install openai-whisper

# 语言检测
pip install langdetect
```

## 使用方式

### 1. 自然语言调用（推荐）

直接对我说：

```
朗读网址 https://www.dapenti.com/blog/more.asp?name=agile&id=191854
```

我会自动：
1. 提取网页内容
2. 检测语言
3. 生成语音
4. 识别语音

### 2. 命令行调用

```bash
# 完整流程
python web_reader_tts.py --url "https://example.com"

# 仅生成语音
python web_reader_tts.py --url "https://example.com" --tts-only

# 仅语音识别
python web_reader_tts.py --audio "audio.mp3" --stt-only

# 指定语言
python web_reader_tts.py --url "https://example.com" --language en

# 使用更大的 Whisper 模型
python web_reader_tts.py --url "https://example.com" --whisper-model large-v3
```

## 参数说明

### TTS 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--voice` | TTS 声音 | 自动检测 |
| `--rate` | 语速 | `+0%` |
| `--volume` | 音量 | `+0%` |
| `--auto-language` | 自动检测语言 | `True` |

### Whisper 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--whisper-model` | 模型大小 | `medium` |
| `--language` | 语言 | 自动检测 |

## 可用声音

### 中文女声
- `zh-CN-XiaoxiaoNeural` - 晓晓（推荐）
- `zh-CN-XiaoyiNeural` - 晓伊
- `zh-CN-XiaochenNeural` - 晓辰

### 中文男声
- `zh-CN-YunxiNeural` - 云希
- `zh-CN-YunyangNeural` - 云扬
- `zh-CN-YunjianNeural` - 云健

### 英文女声
- `en-US-JennyNeural` - Jenny（推荐）
- `en-US-AriaNeural` - Aria

### 日文女声
- `ja-JP-NanamiNeural` - Nanami（推荐）

## Whisper 模型对比

| 模型 | 大小 | 速度 | 准确率 | 推荐场景 |
|------|------|------|--------|----------|
| tiny | 39 MB | 最快 | 较低 | 快速预览 |
| base | 74 MB | 快 | 中等 | 平衡选择 |
| small | 244 MB | 中等 | 较高 | 日常使用 |
| **medium** | **769 MB** | **较慢** | **高** | **中文推荐（默认）** |
| large-v3 | 1.55 GB | 最慢 | 最高 | 专业场景 |

## 多语言处理

### 自动语言检测

脚本会自动检测文本的主要语言，并选择合适的 TTS 声音：

```python
# 自动检测语言
language = detect_language(text)

# 选择合适的声音
voice = get_voice_for_language(language)
```

### 混合语言处理

对于混合语言的文本（如中英混合），脚本会：

1. 检测主要语言
2. 使用主要语言的声音朗读
3. Whisper 会自动识别所有语言

## 示例

### 示例 1：朗读中文网页

```bash
python web_reader_tts.py --url "https://www.dapenti.com/blog/more.asp?name=agile&id=191854"
```

自动使用 `zh-CN-XiaoxiaoNeural` 声音。

### 示例 2：朗读英文网页

```bash
python web_reader_tts.py --url "https://example.com/english-article"
```

自动使用 `en-US-JennyNeural` 声音。

### 示例 3：指定声音和模型

```bash
python web_reader_tts.py --url "https://example.com" --voice "zh-CN-YunxiNeural" --whisper-model large-v3
```

### 示例 4：调整语速

```bash
python web_reader_tts.py --url "https://example.com" --rate "+20%"
```

## 输出文件

- `audio.mp3` - 生成的语音文件
- `transcript.txt` - 语音识别结果

## 注意事项

1. **首次运行**：Whisper 会自动下载模型（medium 模型约 769 MB）
2. **中文识别**：默认使用 medium 模型，准确率较高
3. **网络要求**：Edge TTS 需要网络连接
4. **性能**：Whisper 识别速度取决于模型大小和硬件

## 技术栈

- **Playwright** - 网页自动化
- **Edge TTS** - 微软免费 TTS 服务
- **OpenAI Whisper** - 开源语音识别
- **langdetect** - 语言检测

## 版本历史

- v2.0.0 (2026-04-14) - 🎉 **重大升级**：混合提取方案（Trafilatura + Readability + newspaper3k），正文准确率提升至 95%+，自动选择最佳引擎
- v1.3.0 (2026-04-14) - 优化内容提取算法，提升完整性至 95%+
- v1.2.0 (2026-04-13) - 修复内容截断问题，提升内容完整性至 87%+
- v1.1.0 (2026-04-13) - 添加多语言检测、默认 medium 模型
- v1.0.0 (2026-04-13) - 初始版本

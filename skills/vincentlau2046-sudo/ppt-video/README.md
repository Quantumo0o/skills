# PPT to Video

> 将演示文稿 + 背景材料 → 播报/汇报视频

**版本**: v1.4  
**作者**: Vincent Lau  
**许可证**: MIT

---

## 📋 技能描述

**PPT to Video** - 专业演示视频生成工具，支持多种输入格式，自动适配内容风格。

**核心流程**：
```
PPTX/PDF/HTML + 背景材料 (MD/TXT)
         ↓
    截图 → 风格分析 → TTS → 合成
         ↓
    1024×720 播报视频 (H.264 + AAC)
```

**核心特性**：
- 🎯 **自动风格识别**：新闻/技术/政治/轻松，自动选择 TTS 音色
- 🎤 **统一语速控制**：默认 +25% 语速，支持 `--rate` 参数覆盖
- 📝 **标点符号节奏**：使用标点符号（而非特殊标记）控制 TTS 停顿
- 📊 **多格式支持**：PPTX/PDF/HTML 输入，自动适配
- ✅ **音画对齐验证**：合成后自动检查每页音画同步状态
- 🗣️ **口语化重写**：自动将书面语转为口语化汇报风格（先重点后事实）

---

## 🚀 快速开始

### 安装依赖

```bash
# 系统依赖
sudo apt-get install ffmpeg edge-tts wkhtmltoimage

# Python 依赖（用于 PPTX 文本提取）
pip install python-pptx pillow
```

### 基础用法

```bash
# 方式 1: 指定输入目录（自动检测文件类型）
node scripts/generate.js --input /path/to/input/dir

# 方式 2: 已匹配讲稿模式（推荐）
node scripts/generate.js \
  --slides presentation.pptx \
  --script script_matched.md \
  --output ./video/

# 方式 3: 背景材料 + 智能匹配
node scripts/generate.js \
  --slides presentation.pptx \
  --material background.md \
  --readme README.md \
  --output ./video/
```

---

## 📁 输入文件结构

### 方式 1: 已匹配讲稿模式（推荐）

```
input/
├── presentation.pptx      # 或 .pdf / .html
├── script_matched.md      # 或 讲稿.md
└── (可选) background.md   # 背景材料
```

### 方式 2: 背景材料 + 智能匹配

```
input/
├── presentation.pptx      # 演示文稿
├── README.md              # 内容说明（用于语义匹配）
├── background.md          # 背景材料
└── notes/                 # (可选) 讲稿目录
    ├── 01_封面.md
    ├── 02_摘要.md
    └── ...
```

### 方式 3: 降级模式（仅 PPT）

```
input/
└── presentation.pptx      # 仅 PPT 文件，自动生成基础讲稿
```

---

## ⚙️ 配置选项

### 命令行参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | string | - | 输入目录（自动检测文件） |
| `--slides` | string | - | 演示文稿文件路径 |
| `--script` | string | - | 已匹配讲稿文件路径 |
| `--material` | string | - | 背景材料文件路径 |
| `--readme` | string | - | README 文件路径（用于语义匹配） |
| `--output` | string | `/wechat_articles/Video/<date>/` | 输出目录 |
| `--voice` | string | `zh-CN-XiaoxiaoNeural` | TTS 音色 |
| `--rate` | string | `+25%` | TTS 语速 |
| `--style` | string | `auto` | 风格模式：news/tech/politics/casual/auto |

### TTS 音色配置

| 风格 | 音色 | 适用场景 |
|------|------|----------|
| `news` | `zh-CN-XiaoxiaoNeural` | 新闻播报、情报日报 |
| `tech` | `zh-CN-YunxiNeural` | 技术讲解、产品发布 |
| `casual` | `zh-CN-XiaoyiNeural` | 轻松分享、故事讲述 |

---

## 📊 输出规格

| 维度 | 值 |
|------|-----|
| **视频分辨率** | 1024×720 (720p) |
| **视频编码** | H.264 |
| **音频编码** | AAC (128kbps) |
| **帧率** | 30 fps |
| **输出格式** | MP4 |
| **文件大小** | 5-15 MB（取决于时长） |

---

## 🎯 使用场景

### 1. AI 情报日报视频

```bash
node scripts/generate.js \
  --input /wechat_articles/daily/presentation/2026-04-11/ \
  --output /wechat_articles/Video/2026-04-11/
```

### 2. 技术分享视频

```bash
node scripts/generate.js \
  --slides technical_presentation.pptx \
  --script tech_talk_script.md \
  --voice zh-CN-YunxiNeural \
  --output ./output/
```

### 3. 产品发布视频

```bash
node scripts/generate.js \
  --input ./product_launch/ \
  --style tech \
  --output ./video/
```

---

## 🔧 故障排除

### 常见问题

**Q: TTS 语音合成失败？**
```bash
# 检查 edge-tts 是否安装
edge-tts --version

# 测试 TTS
edge-tts --text "测试" --voice zh-CN-XiaoxiaoNeural --write-media test.mp3
```

**Q: PPTX 截图失败？**
```bash
# 检查 wkhtmltoimage 是否安装
wkhtmltoimage --version

# 或使用备用方案（从 svg_final 生成 PNG）
rsvg-convert -w 1280 -h 720 input.svg -o output.png
```

**Q: 视频合成失败？**
```bash
# 检查 ffmpeg 是否安装
ffmpeg -version

# 检查输入文件是否存在
ls -la screenshots/ audio/
```

### 日志位置

```
输出目录/
├── VIDEO_COMPLETE.md    # 完成报告（含错误信息）
├── scripts/             # 生成的播报稿
├── audio/               # TTS 音频
├── screenshots/         # PPT 截图
└── clips/               # 视频片段
```

---

## 📝 更新日志

### v1.4 (2026-04-10)
- ✅ 支持 PPTX/PDF/HTML 多格式输入
- ✅ 智能讲稿匹配（基于 README 语义分析）
- ✅ 口语化重写（先重点后事实）
- ✅ 音画对齐验证

### v1.3 (2026-04-08)
- ✅ 标点符号节奏控制
- ✅ 自动风格识别

### v1.2 (2026-04-05)
- ✅ TTS 语速统一控制（+25%）
- ✅ 多音色支持

### v1.1 (2026-04-03)
- ✅ 基础功能发布

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/vincentlau2046-sudo/ppt-video

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

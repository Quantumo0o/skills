# PPT to Video 技能规范 (v1.4)

> 将演示文稿 + 背景材料 → 播报/汇报视频

**版本**: v1.4  
**作者**: Vincent Lau  
**许可证**: MIT  
**ClawHub 分类**: video

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

## 📁 文件结构（ClawHub 规范）

```
ppt-video/
├── SKILL.md                      # ✅ 技能规范文档
├── README.md                     # ✅ 使用说明
├── package.json                  # ✅ 依赖配置
├── LICENSE                       # ✅ 许可证
├── .clawhub/
│   └── _meta.json                # ✅ ClawHub 元数据
├── scripts/
│   ├── generate.js               # ✅ 主脚本
│   └── extract_ppt_text.py       # ✅ PPTX 文本提取
└── templates/                    # 图表模板（可选）
```

---

## 🚀 使用示例

### 基础用法

```bash
# 方式 1: 指定输入目录（自动检测文件类型）
node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js \
  --input /path/to/input/dir

# 方式 2: 已匹配讲稿模式（推荐）
node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js \
  --slides presentation.pptx \
  --script script_matched.md \
  --output ./video/

# 方式 3: 背景材料 + 智能匹配
node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js \
  --slides presentation.pptx \
  --material background.md \
  --readme README.md \
  --output ./video/

# 方式 4: 搜索 note 文件夹
node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js \
  --input /path/to/project/ \
  --searchNotes /path/to/project/ \
  --output ./video/
```

### 参数说明

| 参数 | 必需 | 说明 | 默认值 |
|------|------|------|--------|
| `--date` | 否 | 日期标识（用于输出文件名） | 今天 |
| `--input` | 条件 | 输入目录（自动扫描所有文件） | - |
| `--slides` | 条件 | 演示文件路径（PPTX/PDF/HTML） | - |
| `--script` | 条件 | 已匹配讲稿路径（MD） | - |
| `--material` | 条件 | 背景材料路径（MD） | - |
| `--readme` | 否 | PPT 说明文件路径（MD） | - |
| `--searchNotes` | 否 | 搜索 note 文件夹 | - |
| `--output` | 否 | 输出目录 | `~/wechat_articles/Video/ppt-<date>/` |
| `--rate` | 否 | TTS 语速（如 `"+25%"`） | `+25%` |
| `--keepTemp` | 否 | 保留临时项目文件夹 | 删除 |

**输入优先级**：
1. `--script` 指定已匹配讲稿（最高优先级）
2. `--material` + `--readme` 背景材料 + 智能匹配
3. 仅 `--slides` 降级模式

---

## 📁 输入格式

### 1. 演示文稿（三选一）

| 格式 | 支持 | 说明 |
|------|------|------|
| **PPTX** | ✅ | PowerPoint 演示文稿（推荐） |
| **PDF** | ✅ | PDF 文档 |
| **HTML** | ⚠️ | 单页 HTML 幻灯片（简化支持） |

### 2. 背景材料 + README.md（推荐：智能匹配）

**方式 A：背景材料带页面对齐标记（最高优先级）**

```markdown
## 第 1 页 封面
欢迎观看本次演示...

## 第 2 页 核心摘要
这里是核心摘要内容...

## 第 3 页 大模型动态
这里是技术详情...
```

**方式 B：背景材料 + README.md（智能匹配，推荐）**

背景材料 `background.md`：
```markdown
## 智谱 GLM-5.1 发布
智谱 AI 正式发布 GLM-5.1，官方称是目前全球最强的开源模型...

## Kimi K2.5 登顶榜单
月之暗面 Kimi K2.5 上线不到 24 小时，登顶 LMarena 开源模型首位...

## 阿里云 CodingPlan
阿里云百炼推出 CodingPlan，四大开源模型自由切换...
```

PPT 说明 `README.md`：
```markdown
## 第 1 页 封面
关键词：AI 每日洞察、2026-04-10、零壹情报

## 第 2 页 核心摘要
关键词：智谱 GLM-5.1、Kimi K2.5、AGI 突破

## 第 3 页 大模型动态
关键词：智谱 AI、GLM-5.1、SWE-bench、8 小时持续工作

## 第 4 页 中国厂商
关键词：阿里云、CodingPlan、MiniMax、OpenRouter

## 第 5 页 美国厂商
关键词：OpenAI、Anthropic、Google DeepMind、Genie 3

## 第 6 页 趋势洞察
关键词：开源模型、智能体、长程任务
```

**智能匹配逻辑**：
1. 读取 `README.md` 中每页的关键词
2. 分析背景材料每段的内容
3. 自动将段落匹配到关键词最相关的 PPT 页面
4. 输出匹配报告（每页匹配度分数）

**优势**：
- ✅ 背景材料无需按 PPT 页数分割
- ✅ 自动语义匹配，音画对齐
- ✅ 匹配度可视化，便于调试

---

## 🎤 TTS 音色配置

技能自动根据内容风格选择音色：

| 风格 | 音色 | 语速 | 适用场景 |
|------|------|------|----------|
| **新闻** | zh-CN-XiaoxiaoNeural | +25% | 新闻播报、日报 |
| **技术** | zh-CN-YunxiNeural | +25% | 技术讲解、汇报 |
| **政治** | zh-CN-YunjianNeural | +25% | 时事政治、国际形势 |
| **轻松** | zh-CN-XiaoyiNeural | +25% | 轻松内容、教育 |

**语速配置**：
- 默认统一语速：`+25%`（所有页面）
- 支持 `--rate` 参数覆盖：如 `--rate "+30%"`
- ~~删除封面/结尾特殊加速逻辑~~（用户反馈不需要）

---

## 📤 输出格式

### 视频规格

| 属性 | 值 |
|------|-----|
| **分辨率** | 1280×720 (标准 720p 16:9) |
| **视频编码** | H.264 (libx264) |
| **音频编码** | AAC (128kbps) |
| **帧率** | 10 fps（静态图片） |
| **格式** | MP4 (movflags +faststart) |

### 输出目录结构

```
/home/Vincent/.openclaw/workspace/wechat_articles/Video/ppt-2026-04-09/
├── video_2026-04-09.mp4    # 最终视频
├── screenshots/             # 演示截图（PNG）
│   ├── 01-page.png
│   ├── 02-page.png
│   └── ...
├── audio/                   # TTS 音频（MP3）
│   ├── audio_01.mp3
│   ├── audio_02.mp3
│   └── ...
├── clips/                   # 视频片段（MP4）
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   └── ...
└── VIDEO_COMPLETE.md        # 完成报告
```

---

## 🔧 依赖要求

### 必需工具

```bash
# Node.js (v18+)
node --version

# edge-tts (Python TTS)
pip install edge-tts
edge-tts --version

# ffmpeg (视频合成)
ffmpeg -version

# LibreOffice (PPTX 截图)
libreoffice --version

# poppler-utils (PDF 截图)
pdftoppm -version

# ImageMagick (HTML 截图，可选)
convert -version
```

### 安装命令（Ubuntu/Debian）

```bash
# 安装 edge-tts
pip install edge-tts

# 安装 LibreOffice
sudo apt-get install libreoffice

# 安装 poppler-utils
sudo apt-get install poppler-utils

# 安装 ffmpeg
sudo apt-get install ffmpeg

# 安装 ImageMagick
sudo apt-get install imagemagick
```

---

## 🎯 使用场景

### 1. AI 情报日报视频

```bash
node generate.js \
  --input /home/Vincent/.openclaw/workspace/wechat_articles/daily/2026-04-09/
```

### 2. 国际形势简报

```bash
node generate.js \
  --slides /home/Vincent/.openclaw/workspace/wechat_articles/world_intel_brief/ppt_20260409/international_brief.pptx \
  --material /home/Vincent/.openclaw/workspace/wechat_articles/world_intel_brief/ppt_20260409/script.md \
  --output /home/Vincent/.openclaw/workspace/wechat_articles/world_intel_brief/video_20260409/
```

### 3. 技术汇报视频

```bash
node generate.js \
  --slides tech_presentation.pptx \
  --material tech_background.md \
  --output ./output/
```

---

## ⚠️ 注意事项

### 1. 内容风格识别

技能根据关键词自动识别内容风格：
- **政治**：政策、政府、国家、外交、国际形势
- **技术**：技术、代码、API、算法、模型、AI
- **新闻**：新闻、报道、今日、快讯、动态

### 2. TTS 标点符号控制

edge-tts 不支持特殊停顿标记，使用标点符号控制节奏：
- **逗号 `,`**：短停顿
- **句号 `。`**：正常停顿
- **分号 `；`**：中等停顿
- **破折号 `——`**：强调停顿

### 3. 语速配置

- 默认统一语速：`+25%`（所有页面）
- 支持 `--rate` 参数覆盖：如 `--rate "+30%"`
- ~~删除封面/结尾特殊加速~~（根据用户反馈优化）

### 4. 页面对齐验证

技能会自动检查：
- 讲稿分段数 vs PPT 页数
- 不匹配时输出警告并建议修复

---

## 🛠️ 故障排除

### 问题 1: LibreOffice 截图失败

**错误**: `PPTX 截图失败`

**解决**:
```bash
# 检查 LibreOffice
libreoffice --version

# 如果未安装
sudo apt-get install libreoffice
```

### 问题 2: edge-tts 失败

**错误**: `edge-tts: command not found`

**解决**:
```bash
pip install edge-tts
edge-tts --version
```

### 问题 3: 视频合成失败

**错误**: `ffmpeg: command not found`

**解决**:
```bash
sudo apt-get install ffmpeg
ffmpeg -version
```

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.4 | 2026-04-10 | ✅ 讲稿口语化重写（汇报/新闻风格）<br>✅ 句子长度优化（15-25 字/句）<br>✅ 连接词自动添加（先重点后事实） |<br>v1.3 | 2026-04-10 | ✅ 灵活输入检测系统<br>✅ 临时项目文件夹（标准化结构）<br>✅ 已匹配讲稿模式（--script）<br>✅ note 文件夹自动搜索<br>✅ 文件分类整理（ppt/readme/scripts/materials） |
| v1.2 | 2026-04-10 | ✅ 新增 README.md 智能匹配功能<br>✅ 三级优先级策略（标记 > 智能匹配 > 机械分割）<br>✅ 输出匹配度报告（每页分数） |
| v1.1 | 2026-04-10 | ✅ 分辨率改为 1280×720（标准 16:9）<br>✅ 统一语速 +25%，删除封面/结尾特殊加速<br>✅ 强制页面对齐标记（## 第 X 页）<br>✅ 增加音画对齐验证报告 |
| v1.0 | 2026-04-09 | 初始版本 |

---

## 🔗 相关技能

- **ppt-master**: 专业 PPT 生成
- **professional-pptx-maker**: 商务 PPT 生成
- **weixin-video-publish**: 微信视频号发布

---

**技能路径**: `/home/Vincent/.openclaw/workspace/skills/ppt-video/`  
**核心脚本**: `scripts/generate.js`

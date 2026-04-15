---
name: baidu-vod-translate
description: 百度智能云VOD视频翻译工具。支持字幕翻译和语音翻译（配音），支持用户上传字幕、自定义字幕样式，处理后可下载到本地或上传到网盘。当用户提及"视频翻译"、"翻译视频"、"把视频翻译成XX语"时触发。
allowed-tools: Bash, Read, Glob, Grep, Write, Question
argument-hint: "[视频路径] --source <源语言> --target <目标语言>"
metadata: { "openclaw": { "requires": { "bins": ["python3"] } } }
---

# 百度智能云 VOD 视频翻译 Skill

将视频内容翻译成目标语言，支持字幕翻译和语音翻译（配音）。

## ⚠️ 强制执行流程

**禁止直接执行命令！必须按以下流程引导用户：**

```
1. 识别意图 → 判断翻译类型（字幕/语音/两者）
2. 收集参数 → 使用 Question 工具询问用户
3. 确认配置 → 展示参数让用户确认
4. 用户确认 → 才能执行命令
```

**错误示例（禁止）：**
```
用户: 帮我翻译这个视频
Agent: [直接执行 python3 translate.py video.mp4 --source zh --target en]  ❌
```

**正确示例：**
```
用户: 帮我翻译这个视频
Agent: 请问您需要哪种翻译方式？
  [1] 字幕翻译
  [2] 语音翻译（配音）
用户: 1
Agent: 请确认：源语言中文，目标语言英语？
用户: 确认
Agent: [执行命令]  ✓
```

---

## 触发规则

满足以下任一条件时触发：

1. 用户提及"视频翻译"、"翻译视频"
2. 用户需要将视频翻译成其他语言
3. 用户需要视频配音
4. 用户需要查询或管理翻译项目/任务

---

## Agent 参数收集指南

### 核心原则

1. **场景优先**：先理解用户场景，再推荐参数
2. **最小必要**：只收集必要参数，其他使用默认值
3. **渐进式**：从简单到复杂，避免一次性问太多
4. **推荐优先**：给出推荐选项，而非开放式问题

---

## 第一步：识别用户意图

根据用户描述，识别属于哪种场景：

| 用户描述关键词 | 场景类型 | 推荐配置 |
|---------------|----------|----------|
| "翻译成英语"、"翻译成中文" | 字幕翻译 | --subtitle（默认） |
| "配音"、"配音翻译"、"语音翻译" | 语音翻译 | --speech |
| "我有字幕"、"用这个字幕" | 用户字幕 | --subtitle-source user |
| "查任务"、"项目列表" | 任务管理 | --list-tasks/--list-projects |
| "修改字幕"、"替换字幕" | 任务修改 | --update-task |

---

## 第二步：收集必要参数

### 场景 A：字幕翻译（最常见）

**必须收集**：
1. 视频来源（本地路径/网盘路径）
2. 目标语言

**可选收集**：
- 源语言（可自动识别，但建议确认）

**交互模板**：

```
用户: 帮我把这个视频翻译成英语

Agent: 好的，请确认：
  - 视频原始语言是中文吗？
  - 请提供视频文件路径：

用户: 是中文，路径是 /Downloads/video.mp4

Agent: [执行: --source zh --target en]
正在翻译...
```

### 场景 B：语音翻译（配音）

**必须收集**：
1. 视频来源
2. 源语言
3. 目标语言

**可选收集**：
- 配音类型（音色复刻/AI配音）

**交互模板**：

```
用户: 帮我把这个视频配上英语配音

Agent: 好的，语音翻译会保留原声音色。
请确认：
  - 视频原始语言：中文？
  - 视频文件路径：

用户: 是的，/Downloads/video.mp4

Agent: 配音方式：
  [1] 音色复刻 - 模仿原声说话（推荐）
  [2] AI配音 - 使用指定音色

用户: 1

Agent: [执行: --source zh --target en --speech --tts-type VOICE_CLONE]
正在处理...
```

### 场景 C：用户上传字幕

**必须收集**：
1. 视频来源
2. 字幕文件路径
3. 源语言
4. 目标语言

**交互模板**：

```
用户: 我有字幕文件，帮我翻译视频

Agent: 好的，请提供：
  - 视频文件路径：
  - 字幕文件路径（SRT格式）：
  - 字幕是什么语言：
  - 要翻译成什么语言：

用户: video.mp4, subs.srt, 中文, 英语

Agent: [执行: --subtitle-source user --subtitle-file subs.srt --source zh --target en]
正在翻译...
```

### 场景 D：字幕样式定制

**触发条件**：用户明确提到样式需求

**交互模板**：

```
用户: 字幕要大一点，用宋体

Agent: 好的，字幕样式配置：
  - 字体：宋体
  - 字号：建议60像素，可以吗？
  - 其他：默认白色、居中

用户: 可以

Agent: [执行: --font-family Song --font-size 60]
```

### 场景 E：电商场景

**触发条件**：用户提到"电商"、"商品"、"带货"、"直播卖货"等关键词

**交互模板**：

```
用户: 帮我翻译这个电商直播视频

Agent: 好的，电商视频会使用电商场景优化。
请确认：
  - 视频文件路径：
  - 源语言：
  - 目标语言：

用户: video.mp4, 中文, 英语

Agent: [执行: --project-type Ecommerce --source zh --target en]
正在翻译...
```

**项目类型说明**：

| 类型 | 适用场景 | 特点 |
|------|----------|------|
| ShortSeries | 短剧、电影、电视剧、访谈（默认） | 针对剧情内容优化 |
| Ecommerce | 电商直播、商品介绍、带货视频 | 针对电商内容优化 |

---

## 第三步：确认高级参数（可选）

**仅在以下情况询问**：

| 参数 | 何时询问 | 默认值 |
|------|----------|--------|
| 字幕来源 | 视频无字幕/字幕不清晰 | ocr |
| 烧录字幕 | 用户说"只要字幕文件" | 是 |
| 擦除原字幕 | 用户说"保留原字幕" | 是 |
| 字幕样式 | 用户明确要求 | 默认样式 |
| 项目类型 | 用户提到"电商"、"带货"等 | ShortSeries |
| OCR区域 | 用户指定识别区域 | 全屏 |
| OCR重叠阈值 | 用户提到"识别不准" | 1（严格匹配） |
| 字幕识别范围 | 用户提到"只识别对白" | 全部 |
| 擦除模式 | 用户提到"只擦除对白字幕" | global |
| 输出目录 | 用户指定保存位置 | ./output |
| 上传网盘 | 视频来自网盘时主动询问 | 否 |

**不要主动询问的参数**：
- translation-types（默认字幕翻译）
- subtitle-source（默认 OCR）
- font-* 系列（默认样式即可）
- erase-mode（默认 global）
- erase-model（默认 v4）
- ocr-region-iou（默认 1）

---

## 参数收集决策树

```
用户请求
    │
    ├─ 查询任务？ ──────────────────────► --list-tasks / --list-projects
    │
    ├─ 删除项目？ ──────────────────────► --delete-project
    │
    ├─ 修改任务？ ──────────────────────► --update-task
    │
    └─ 翻译视频？
         │
         ├─ 视频来源？
         │    ├─ 本地 ──► 获取路径
         │    └─ 网盘 ──► 获取网盘路径
         │
         ├─ 翻译类型？
         │    ├─ "翻译字幕" ──► --subtitle
         │    ├─ "配音" ──► --speech
         │    └─ 都要 ──► --subtitle --speech
         │
         ├─ 语言？
         │    ├─ 源语言 ──► 确认或自动识别
         │    └─ 目标语言 ──► 必须明确
         │
         ├─ 字幕来源？
         │    ├─ "有字幕文件" ──► --subtitle-source user
         │    ├─ "视频有字幕" ──► --subtitle-source ocr
         │    └─ "视频无字幕" ──► --subtitle-source asr
         │
         ├─ 样式需求？
         │    ├─ 有 ──► 收集字体/颜色/大小
         │    └─ 无 ──► 使用默认
         │
         └─ 确认执行
              │
              ├─ 来自网盘？ ──► 询问是否上传回网盘
              │
              └─ 执行命令
```

---

## 推荐参数组合

### 组合 1：基础字幕翻译（推荐）

```bash
python3 scripts/translate.py <视频> --source zh --target en
```

**适用场景**：大多数视频翻译需求
**特点**：OCR识别字幕 → 翻译 → 烧录到视频

### 组合 2：影视剧配音

```bash
python3 scripts/translate.py <视频> --source zh --target en --speech
```

**适用场景**：需要配音的视频
**特点**：保留原声音色，翻译后配音

### 组合 3：用户字幕翻译

```bash
python3 scripts/translate.py <视频> --source zh --target en \
  --subtitle-source user --subtitle-file subs.srt
```

**适用场景**：有现成字幕文件
**特点**：使用用户提供的字幕，翻译更准确

### 组合 4：无字幕视频翻译

```bash
python3 scripts/translate.py <视频> --source zh --target en \
  --subtitle-source asr
```

**适用场景**：视频没有字幕但有对白
**特点**：语音识别提取字幕 → 翻译

### 组合 5：自定义字幕样式

```bash
python3 scripts/translate.py <视频> --source zh --target en \
  --font-family Song --font-size 60 --font-bold
```

**适用场景**：对字幕样式有要求
**特点**：宋体、60号、加粗

---

## 语言识别快捷方式

| 用户说法 | 对应语言代码 |
|----------|-------------|
| 中文、国语、普通话 | zh |
| 英语、英文 | en |
| 日语、日文 | ja |
| 韩语、韩文 | ko |
| 法语、法文 | fr |
| 德语、德文 | de |
| 西班牙语 | es |
| 葡萄牙语 | pt |
| 俄语 | ru |
| 泰语 | th |
| 阿拉伯语 | ar |

---

## 常见问题处理

### Q1：用户不知道源语言

```
用户: 帮我把这个视频翻译成中文

Agent: 请问视频原始语言是什么？
  [1] 英语
  [2] 日语
  [3] 韩语
  [4] 其他

用户: 1

Agent: [执行: --source en --target zh]
```

### Q2：用户想要字幕文件而非视频

```
用户: 我只要翻译后的字幕文件，不要烧录到视频

Agent: 好的，不烧录字幕到视频。
[执行: --no-burn-subtitle]
翻译完成后会提供字幕文件下载链接。
```

### Q3：用户想保留原字幕

```
用户: 保留原来的中文字幕，再加英文字幕

Agent: 好的，不擦除原字幕，翻译后会同时显示中英双语字幕。
[执行: --no-erase-subtitle]
```

### Q4：用户要处理多个视频

```
用户: 帮我翻译这三个视频

Agent: 好的，请确认：
  - 都翻译成什么语言？
  - 源语言相同吗？

用户: 都翻译成英语，都是中文视频

Agent: [执行: video1.mp4 video2.mp4 video3.mp4 --source zh --target en]
```

### Q5：用户要求特定字体

```
用户: 字幕用宋体，大一点

Agent: 好的，字幕样式：
  - 字体：宋体
  - 字号：建议60像素，可以吗？
  - 颜色：白色带黑边（默认）

用户: 字号再大点，80

Agent: [执行: --font-family Song --font-size 80]
```

---

## 执行命令模板

### 基础命令

```bash
export BAIDU_VOD_AK='xxx' && export BAIDU_VOD_SK='xxx' && \
python3 scripts/translate.py <视频路径> --source <源语言> --target <目标语言>
```

### 完整命令（所有参数）

```bash
export BAIDU_VOD_AK='xxx' && export BAIDU_VOD_SK='xxx' && \
python3 scripts/translate.py <视频路径> \
  --source <zh|en|ja|...> \
  --target <zh|en|ja|...> \
  --subtitle \
  --speech \
  --subtitle-source <ocr|asr|user> \
  --subtitle-file <字幕文件> \
  --no-burn-subtitle \
  --no-erase-subtitle \
  --ocr-areas "x,y,w,h[,start,end]" \
  --ocr-region-iou <0|1> \
  --text-types <dialog|castName|castDescription|other> \
  --erase-mode <global|dialog|manual> \
  --erase-areas "x,y,w,h[,start,end]" \
  --erase-model <v3|v4> \
  --font-family <Hei|Song|Kai> \
  --font-size <字号> \
  --font-color "#RRGGBBAA" \
  --font-outline-color "#RRGGBBAA" \
  --font-outline-thickness <像素> \
  --font-bold \
  --font-italic \
  --font-underline \
  --font-strike-out \
  --font-alignment <left|center|right> \
  --font-spacing <像素> \
  --font-line-spacing <倍数> \
  --font-bg-color "#RRGGBBAA" \
  --font-text-bg-color "#RRGGBBAA" \
  --font-padding <像素> \
  --tts-type <VOICE_CLONE|AI_DUB> \
  --voice-id <音色ID> \
  --project-type <ShortSeries|Ecommerce> \
  --output-dir <输出目录> \
  --upload-netdisk \
  --netdisk-dir <网盘目录>
```

---

## 示例对话

### 示例 1：简单场景（中译英）

```
用户: 帮我把 /Downloads/video.mp4 翻译成英语

Agent: 确认参数：
  - 源语言：中文
  - 目标语言：英语
  - 翻译类型：字幕翻译
  - 字幕来源：OCR识别

确认执行吗？

用户: 确认

Agent: [执行: --source zh --target en]
正在翻译...
✓ 处理完成，结果已保存到: ./output/video_en.mp4
```

### 示例 2：配音场景

```
用户: 帮我把这个中文视频配上英语配音

Agent: 好的，语音翻译会模仿原声音色。
请提供视频文件路径：

用户: /Downloads/movie.mp4

Agent: 配音方式：
  [1] 音色复刻 - 模仿原声说话（推荐）
  [2] AI配音 - 使用指定音色

用户: 1

Agent: [执行: --source zh --target en --speech]
正在处理，配音需要较长时间...
✓ 处理完成
```

### 示例 3：用户字幕

```
用户: 我有字幕文件，帮我翻译

Agent: 请提供：
  - 视频文件：
  - 字幕文件：
  - 字幕语言：
  - 目标语言：

用户: video.mp4, subs.srt, 中文, 英语

Agent: [执行: --subtitle-source user --subtitle-file subs.srt --source zh --target en]
正在翻译...
✓ 处理完成
```

### 示例 4：网盘视频

```
用户: 帮我翻译网盘里 /apps/bdpan/video.mp4 到日语

Agent: 确认参数：
  - 源语言：中文
  - 目标语言：日语

处理后是否上传回网盘？

用户: 是

Agent: [执行: --netdisk /apps/bdpan/video.mp4 --source zh --target ja --upload-netdisk]
正在从网盘下载并翻译...
✓ 处理完成
  本地文件: ./output/video_ja.mp4
  网盘路径: translated/video_ja.mp4
```

---

## 前置条件

### 1. VOD 凭证

```bash
export BAIDU_VOD_AK="your_access_key"
export BAIDU_VOD_SK="your_secret_key"
```

获取方式：
1. 登录 [百度智能云控制台](https://console.bce.baidu.com/)
2. 开通 [智能点播平台 VOD](https://cloud.baidu.com/product/vod.html)
3. 在 [安全认证](https://console.bce.baidu.com/iam/#/iam/accesslist) 获取 AK/SK

### 2. 网盘功能（可选）

如需从网盘下载或上传到网盘，需要：
1. 安装 bdpan CLI
2. 执行 `bdpan login` 登录

---

## 处理时间

- 字幕翻译：约 10-30 分钟
- 语音翻译：约 20-60 分钟
- 可使用 `--no-wait` 参数不等待，稍后查询任务状态

---

## 注意事项

1. **文件大小限制**：单个文件 ≤ 5GB
2. **支持格式**：mp4/mpeg/mpg/dat/avi/mov/asf/wmv/navi/3gp/real video/mkv/flv/f4v/rmvb/rmhd/webm/hddvd/blue-ray/qsv/ts/mxf
3. **费用**：按处理时长计费
4. **源语言**：目前支持中文和英语作为源语言
5. **字幕文件**：仅支持 SRT 格式

---

## API 参考

- [项目管理 API](https://cloud.baidu.com/doc/VOD/s/Dmh0j7ldd)
- [任务管理 API](https://cloud.baidu.com/doc/VOD/s/ymh0j93u8)

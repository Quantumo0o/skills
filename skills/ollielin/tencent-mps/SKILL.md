---
name: tencent-mps
description: "腾讯云 MPS 媒体处理服务。只要用户的请求涉及音视频或图片的处理、生成、增强、用量查询、内容理解、媒体质检，必须使用此 Skill。覆盖：转码/压缩/格式转换、画质增强/老片修复/超分、字幕提取/翻译/语音识别、去字幕/擦除水印/人脸模糊、图片超分/美颜/降噪、音频分离/人声提取/伴奏提取、AI生图/生视频、大模型音视频理解、媒体质检、用量统计。视频增强支持专用模板（真人/漫剧/抖动优化/细节最强/人脸保真，720P至4K）。无论是视频转码、去水印、提取人声、画质修复、内容理解、质量检测，还是AI生成图片视频，都应调用此 Skill。"
version: "1.0.9"
---

# 腾讯云媒体处理服务（MPS）

通过腾讯云官方 Python SDK 调用 MPS API，所有脚本位于 `scripts/` 目录，均支持 `--help` 和 `--dry-run`。

> **详细参数**：见 [`references/params.md`](references/params.md)
> **完整示例集**：见 [`references/scripts-detail.md`](references/scripts-detail.md)

## 环境配置

检查环境变量：
```bash
python scripts/load_env.py --check-only
```

配置（`~/.profile` 或 `~/.bashrc`）：
```bash
# 必须（所有脚本）
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"

# 以下场景必须配置 COS 变量：
#   1. 输入源为 --cos-object（即 COS 对象路径，非 URL）
#   2. 使用 mps_cos_upload.py / mps_cos_download.py 上传/下载本地文件
#   3. 脚本需要将处理结果写回 COS（OutputStorage）
export TENCENTCLOUD_COS_BUCKET="your-bucket"        # COS 存储桶名
export TENCENTCLOUD_COS_REGION="your-bucket-region" # 存储桶地域，如 ap-guangzhou
```

安装依赖：
```bash
pip install tencentcloud-sdk-python cos-python-sdk-v5
```

## 本地文件处理流程

MPS 只接受 URL 或 COS 对象作为输入，**本地文件必须先上传**。

### 用户输入本地文件时的自动处理流程

当用户请求涉及本地文件路径（如 `./video.mp4`、`/path/to/image.jpg`）时，按以下步骤**自动处理**：

**步骤 1：上传文件到 COS**
```bash
python scripts/mps_cos_upload.py --local-file <本地文件路径> --cos-key <目标路径>
```
- 使用 `--cos-key` 指定合理的存储路径（默认路径 `input/`）
- 记录上传返回的 COS 信息：bucket、region、key

**步骤 2：使用 COS 路径参数执行脚本**
根据脚本类型，使用各个脚本中 传递 COS 路径的方式，如下：
| 脚本 | COS 路径参数方式 | 示例 |
| `mps_transcode.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_enhance.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_erase.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_subtitle.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_imageprocess.py` | `--cos-object <key>` | `--cos-object input/image.jpg` |
| `mps_qualitycontrol.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_av_understand.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_vremake.py` | `--cos-object <key>` | `--cos-object input/video.mp4` |
| `mps_aigc_image.py` | `--cos-input-bucket <b> --cos-input-region <r> --cos-input-key <k>` | `--cos-input-bucket xxx --cos-input-region ap-guangzhou --cos-input-key input/img.jpg` |
| `mps_aigc_video.py` | `--cos-input-bucket <b> --cos-input-region <r> --cos-input-key <k>` | `--cos-input-bucket xxx --cos-input-region ap-guangzhou --cos-input-key input/img.jpg` |

> **注意**：使用 `--cos-object` 的脚本依赖环境变量 `TENCENTCLOUD_COS_BUCKET` 和 `TENCENTCLOUD_COS_REGION`；AIGC 类脚本需要显式传递完整的 COS 信息。

**步骤 3：下载处理结果（如需要）**
```bash
python scripts/mps_cos_download.py --cos-key <输出key> --local-file <本地保存路径>
```

### 禁止的操作

❌ **禁止直接使用拼接的 URL 作为参数**  
例如：`--url https://<bucket>.cos.<region>.myqcloud.com/<key>`  
原因：本地上传的文件可能没有公开读取权限，URL 访问会失败。

✅ **必须使用 COS 路径方式（bucket + region + key）**

### 手动处理示例

如需手动执行，完整流程如下：
```bash
# 1. 上传
python scripts/mps_cos_upload.py --local-file ./video.mp4 --cos-key input/video.mp4
# 2. 执行任务（使用 COS 路径）
python scripts/mps_transcode.py --cos-object input/video.mp4
# 3. 下载结果
python scripts/mps_cos_download.py --cos-key output/result.mp4 --local-file ./result.mp4
```

返回结果含链接时，用 Markdown 格式返回给用户：`[文件名](URL)`

## 异步任务说明

所有脚本默认自动轮询等待完成。
- 只提交不等待：加 `--no-wait`，脚本返回 TaskId
- 手动查询：音视频用 `mps_get_video_task.py`，图片用 `mps_get_image_task.py`

## 脚本功能映射（职责边界）

选择脚本时必须严格按照映射关系，**不得混用**：

| 用户需求类型 | 使用脚本 | 说明 |
|---|---|---|
| 检查画面质量、检测模糊/花屏 | `mps_qualitycontrol.py` | **唯一质检脚本**，`--definition 60`（默认） |
| 检测播放兼容性、卡顿、播放异常 | `mps_qualitycontrol.py` | **唯一质检脚本**，`--definition 70` |
| 音频质量检测、音频事件检测 | `mps_qualitycontrol.py` | **唯一质检脚本**，`--definition 50` |
| 去除字幕、擦除水印、人脸/车牌模糊 | `mps_erase.py` | 仅用于画面内容擦除/遮挡 |
| 画质增强、老片修复、超分辨率 | `mps_enhance.py` | 视频画质提升 |
| 转码、压缩、格式转换 | `mps_transcode.py` | 编码格式处理 |
| 字幕提取、翻译、字幕类语音识别 | `mps_subtitle.py` | 字幕相关 |
| 图片处理（超分/美颜/降噪） | `mps_imageprocess.py` | 图片增强 |
| AI 生图（文生图/图生图） | `mps_aigc_image.py` | AIGC 图片生成 |
| AI 生视频（文生视频/图生视频） | `mps_aigc_video.py` | AIGC 视频生成 |
| 音视频内容理解（场景/摘要/分析/语音识别） | `mps_av_understand.py` | 大模型理解，**必须提供 `--mode` 和 `--prompt`** |
| 视频去重（画中画/视频扩展/换脸/换人等） | `mps_vremake.py` | VideoRemake，**必须提供 `--mode`** |
| 用量统计查询 | `mps_usage.py` | 调用次数/时长查询 |
| 查询音视频处理任务状态 | `mps_get_video_task.py` | ProcessMedia 任务查询 |
| 查询图片处理任务状态 | `mps_get_image_task.py` | ProcessImage 任务查询 |
| 上传本地文件到 COS | `mps_cos_upload.py` | 本地→COS 前置步骤 |
| 从 COS 下载文件 | `mps_cos_download.py` | COS→本地 后置步骤 |
| 列出 COS Bucket 文件 | `mps_cos_list.py` | 查看 COS 文件列表，支持路径过滤和文件名搜索 |

> **重要**：`mps_erase.py` 职责是**擦除/遮挡画面视觉元素**，不涉及质量检测。
> "画质检测"、"模糊"、"花屏"、"播放兼容性"、"音频质检" → 必须用 `mps_qualitycontrol.py`。

## 生成命令的强制规则

1. **禁止占位符**：所有参数值必须是真实值。若用户未提供必需值，**先询问**，不得用 `<视频URL>`、`YOUR_URL` 等占位符。

2. **`mps_qualitycontrol.py` 必须含 `--definition`**：
   - 音频质检：`--definition 50`
   - 画面质检（默认）：`--definition 60`
   - 播放兼容性：`--definition 70`

3. **`mps_av_understand.py` 必须含 `--mode` 和 `--prompt`**：
   - `--mode video`（理解视频画面）或 `--mode audio`（仅音频，视频自动提取音频）
   - `--prompt` 控制大模型理解侧重点，缺失时结果可能为空

## 关键脚本说明

### 视频增强 (`mps_enhance.py`)

大模型增强模板（`--template`），按场景+目标分辨率选择：

| 场景 | 720P | 1080P | 2K | 4K |
|------|------|-------|----|----|
| 真人（Real） | 327001 | 327003 | 327005 | 327007 |
| 漫剧（Anime） | 327002 | 327004 | 327006 | 327008 |
| 抖动优化 | 327009 | 327010 | 327011 | 327012 |
| 细节最强 | 327013 | 327014 | 327015 | 327016 |
| 人脸保真 | 327017 | 327018 | 327019 | 327020 |

### 去字幕擦除 (`mps_erase.py`)

预设模板：`101` 去字幕 | `102` 去字幕+OCR | `201` 去水印高级版 | `301` 人脸模糊 | `302` 人脸+车牌模糊

### 大模型音视频理解 (`mps_av_understand.py`)

通过 `AiAnalysisTask.Definition=33` + `ExtendedParameter(mvc.mode + mvc.prompt)` 控制。

```bash
# 视频内容理解
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video \
    --prompt "请分析这个视频的主要内容、场景和关键信息"

# 音频模式（视频自动提取音频）
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode audio \
    --prompt "请进行语音识别，输出完整文字内容"

# 对比分析（两段音视频）
python scripts/mps_av_understand.py \
    --url https://example.com/v1.mp4 \
    --extend-url https://example.com/v2.mp4 \
    --mode audio \
    --prompt "对比两段音频，分析差异"

# 查询任务
python scripts/mps_av_understand.py --task-id 2600011633-WorkflowTask-xxxxx --json
```

### 媒体质检 (`mps_qualitycontrol.py`)

```bash
# 画面质检（默认）
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 60

# 播放兼容性质检
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70

# 音频质检
python scripts/mps_qualitycontrol.py --url https://example.com/audio.mp3 --definition 50

# 异步提交
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 60 --no-wait
```

### 视频去重 (`mps_vremake.py`)

```bash
# 画中画去重（等待结果）
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode PicInPic --wait

# 视频扩展去重
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode BackgroundExtend --wait

# 换脸模式
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode SwapFace \
    --src-faces https://example.com/src.png --dst-faces https://example.com/dst.png --wait

# 换人模式
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode SwapCharacter \
    --src-character https://example.com/src_full.png \
    --dst-character https://example.com/dst_full.png --wait

# 画中画 + LLM 提示词
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode PicInPic \
    --llm-prompt "生成一个唯美的自然风景背景图片" --wait

# 异步提交（默认，不加 --wait）
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode PicInPic

# 查询任务
python scripts/mps_vremake.py --task-id 2600011633-WorkflowTask-xxxxx --json
```

**去重模式**：`PicInPic`（画中画）`BackgroundExtend`（视频扩展）`VerticalExtend`（垂直填充）`HorizontalExtend`（水平填充）`AB`（视频交错）`SwapFace`（换脸）`SwapCharacter`（换人）  
**主要参数**：`--url` / `--cos-object` / `--task-id` / `--mode`（必填）/ `--wait` / `--llm-prompt` / `--llm-video-prompt` / `--src-faces`+`--dst-faces`（换脸）/ `--src-character`+`--dst-character`（换人）/ `--json` / `--dry-run`

### 用量统计 (`mps_usage.py`)

```bash
python scripts/mps_usage.py --days 30 --all-types
python scripts/mps_usage.py --start 2026-01-01 --end 2026-01-31
python scripts/mps_usage.py --type Transcode Enhance AIGC AIAnalysis
```

`--type` 支持：`Transcode` `Enhance` `AIAnalysis` `AIRecognition` `AIReview` `Snapshot` `AnimatedGraphics` `AiQualityControl` `Evaluation` `ImageProcess` `AddBlindWatermark` `AddNagraWatermark` `ExtractBlindWatermark` `AIGC`

## API 参考

| 脚本 | 文档 |
|------|------|
| `mps_transcode.py` / `mps_enhance.py` / `mps_subtitle.py` / `mps_erase.py` | [ProcessMedia](https://cloud.tencent.com/document/api/862/37578) |
| `mps_qualitycontrol.py` | [ProcessMedia AiQualityControlTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_imageprocess.py` | [ProcessImage](https://cloud.tencent.com/document/api/862/112896) |
| `mps_av_understand.py` | [VideoComprehension AiAnalysisTask](https://cloud.tencent.com/document/product/862/126094) |
| `mps_vremake.py` | [VideoRemake AiAnalysisTask](https://cloud.tencent.com/document/product/862/124394) |
| `mps_aigc_image.py` | [CreateAigcImageTask](https://cloud.tencent.com/document/api/862/114562) |
| `mps_aigc_video.py` | [CreateAigcVideoTask](https://cloud.tencent.com/document/api/862/126965) |
| `mps_usage.py` | [DescribeUsageData](https://cloud.tencent.com/document/product/862/125919) |
| `mps_get_video_task.py` | [DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614) |
| `mps_get_image_task.py` | [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/112897) |

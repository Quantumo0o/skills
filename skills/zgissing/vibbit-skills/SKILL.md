---
name: vibbit-skills
version: 1.0.7
display_description: |
  帮你用集思 AI 出 B-roll 素材、复刻爆款文案、拆解热门视频、查数字人、一键生成数字人口播视频。
  - B-roll 生图 — 告诉我口播的主题或台词，帮你生成配套的 B-roll 素材图
  - 爆款复刻 — 丢给我一条抖音 / 小红书 / B站链接，帮你解析视频内容、提炼文案结构，直接复刻
  - 爆款拆解 — 深度分析一条视频的钩子、节奏、台词，搞清楚它为什么火
  - 查数字人 — 看看你账号下有哪些可用的数字人形象
  - 数字人口播 — 给我一段文案，选好数字人，直接帮你生成一条口播视频
description: 调用 Vibbit OpenAPI 完成五类能力——AI 生图、解析抖音/小红书/B站链接、爆款视频拆解、查询当前用户可用的数字人列表、初始化数字人口播视频工作流。当用户说"生成一张图 / AI 出图"、"解析这个抖音/小红书/B站链接"、"拆解一下这条爆款 / 视频拆解"、"看看我有哪些数字人 / 列一下数字人"、或"用 xx 数字人做条口播 / 初始化数字人视频 / 数字人口播"时，都应主动触发此 skill，即便用户没有明确提到 "vibbit" 或 "openapi"。只要任务能映射到这五项能力之一、且用户正在和 Vibbit / willing-agentcy 系统打交道，就优先用这个 skill 而不是自己手写 HTTP 请求。
metadata:
  openclaw:
    primaryEnv: VIBBIT_API_KEY
    requires:
      env:
        - VIBBIT_API_KEY
      anyBins:
        - ffprobe
    envVars:
      - name: VIBBIT_API_KEY
        required: true
        description: "集思平台 API Key，前往 https://app.vibbit.cn/api-keys 获取"
      - name: VIBBIT_BASE_URL
        required: false
        description: "API 地址，默认 https://openapi.vibbit.cn，切换测试环境时使用"
---

# Vibbit OpenAPI skill

把 Vibbit OpenAPI 的五类能力封装成一个 Node.js CLI，Claude 不用每次都手写 HTTP 调用。其中两项是**同步**接口（提交即返回结果），另外三项是**异步**接口（脚本自动轮询直到 COMPLETED / FAILED）。

## 何时触发

当用户的请求能对应到下面任意一项时，触发本 skill：

| 用户意图（示例） | 任务类型 | 同步? |
| --- | --- | --- |
| "生成一张图"、"AI 画一只猫"、"出图" | `AIGC_IMAGE_GENERATION` | 异步 |
| "解析这个抖音链接"、"这条小红书链接讲了什么" | `PARSE_CONTENT_URL` | 异步 |
| "拆解一下这条爆款"、"视频拆解"、"分析这条带货视频" | `VIDEO_BREAKDOWN` | 异步 |
| "我有哪些数字人"、"列一下可用数字人" | `QUERY_DIGITAL_HUMAN_LIST` | 同步 |
| "用 xx 数字人做条口播"、"初始化数字人视频"、"数字人口播" | `DIGITAL_HUMAN_ORAL_BROADCAST` | 同步 |

五项之外的任何场景都不要用这个 skill。

## 前置条件

用户的 shell 必须已导出以下两个环境变量：

- `VIBBIT_API_KEY` —— 集思平台签发的 bearer token，**必填**，缺失时脚本报错退出
- `VIBBIT_BASE_URL` —— **可选**，不设置时默认走 prd `https://openapi.vibbit.cn`；需要切别的环境（测试/灰度等）时 export 这个变量覆盖

`VIBBIT_API_KEY` 缺失时，告诉用户去 https://app.vibbit.cn/api-keys 获取，获取后告诉我，我来帮你配置；不要猜或跳过。

Node.js 要求 18+（用到内置 `fetch`）。脚本通过远程接口 `https://tools.vibbit.ai/api/file-info` 获取素材元信息，无需 WASM 或 npm 依赖。系统若装有 `ffprobe`（ffmpeg 附带）会自动作为备用探测方式，没有也完全能正常运行。

## 脚本路径

脚本目录：`$VIBBIT_SKILL_DIR = ~/.claude/skills/vibbit-skills/scripts`，主入口是 `$VIBBIT_SKILL_DIR/vibbit.js`。下面示例里的 `$VIBBIT_SKILL_DIR` 仅用于可读性，实际调用时请用真实的绝对路径。

> **独立使用**：`scripts/vibbit.js` 是**自包含**的单文件，没有 npm 依赖。拷到任何 Node 18+ 的机器上直接跑，不限定必须放在 `~/.claude/skills/` 下。系统若装有 `ffprobe` 可选自动启用，没有也完全可以运行。

## 怎么调用

始终通过 bundled CLI，不要直接调 HTTP 接口。这很重要，因为线格式有几个坑：

1. `input_info.input` 是一个**已经字符串化**的 JSON（双层编码），不是嵌套对象
2. 所有字段走 **snake_case**（`task_type`、`input_info`、`digital_human_id` 等）
3. `oral_broadcast` 的 `material_list` 每个元素需要完整 `file_info` 结构（含 `file_size` / `mime_type` / `width` / `height` / `duration` 等），脚本会自动探测生成

```bash
node $VIBBIT_SKILL_DIR/vibbit.js <子命令> [--参数]
```

脚本成功时把 JSON 写到 stdout：同步任务是 `{"result": ...}`，异步任务是 `{"task_id": "...", "result": ...}`；失败时输出 `{"error": "..."}` 并以非零退出码结束。拿到 stdout 后先解析出有用字段，再用自然语言呈现给用户，不要把原始 JSON 一股脑 dump 给用户看。

## 子命令

### 1. AI 生图 —— `gen_image`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js gen_image \
  --prompt "a cute orange cat sitting on a window sill, studio ghibli style" \
  [--ref-url https://cdn.example.com/ref.jpg]
```

- `--prompt` 必填。按用户原话翻译/搬运即可，除非用户明确要求润色，否则不要随便加戏
- `--ref-url` 可选，参考图

脚本会提交并自动轮询；最终 `result` 里一般包含生成图的 URL，把 URL 直接给用户。

### 2. 解析链接 —— `parse_url`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js parse_url \
  --url "https://v.douyin.com/xxxxxxx"
```

支持抖音 / 小红书 / B 站的分享链接。`result` 通常包含原始视频 URL、标题、描述、ASR 字幕。只展示用户关心的字段，不要全量 dump。

### 3. 爆款视频拆解 —— `breakdown`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js breakdown \
  --video-url "https://cdn.example.com/video.mp4" \
  --sub-tasks asr,hot,bgm
```

- `--video-url` 必填。直接传分享链接（抖音 / 小红书 / B站）或裸 MP4 URL 都可以，breakdown 内部已包含解析能力，不需要先调 `parse_url`
- `--sub-tasks` 必填，逗号分隔，可选值：
  - `asr` —— 语音转文字
  - `transition` —— 转场分析
  - `hot` —— 爆点 / 钩子分析
  - `bgm` —— 背景音乐
  - 如果用户没指定，默认选 `asr,hot`，并**告诉用户你选了什么**方便纠正

拆解任务偏慢，一两分钟很正常。等待过程中主动告诉用户"正在分析视频，稍等一下"，让用户知道在跑，不是卡住了。

### 4. 查询数字人列表 —— `list_digital_humans`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js list_digital_humans
```

同步接口。返回当前用户可用的数字人配置（租户级 + 共享 + 个人）。呈现给用户时至少展示名称，按分组列出，让用户直接说"用 XX"，不要让用户手动填写 ID。

### 5. 初始化数字人口播 —— `oral_broadcast`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js oral_broadcast \
  --message "大家好，今天给大家介绍一款新品..." \
  --digital-human-id 10001 \
  [--title "新品上架首秀"] \
  [--material-url https://cdn.example.com/a.mp4 \
   --material-name "新品A镜头.mp4" \
   --material-url https://cdn.example.com/b.jpg \
   --material-name "包装特写.jpg"]
```

- `--message` 必填。**既是聊天消息，又是预设文案**——后端会自动把 `has_script` 置为 true，用户传什么文字就会被当作视频口播的脚本原文使用，LLM 不会再改写
- `--digital-human-id` 必填。如果用户没指定用哪一个，先调 `list_digital_humans` 让用户挑，再继续
- `--title` 可选。传了就作为预设标题，跳过 LLM 自动生标题那一步；不传时后端照常调模型生成
- `--material-url` 可选、可重复。每项只传 URL，`file_name` 默认由 URL 末段自动推断。
- `--material-name` 可选、可重复。**传了就必须和 `--material-url` 数量相等，按出现顺序一一对应**。用户给出友好名称（比如 OSS key 是乱码、展示名另有规定）时用这个；不需要可以整个不传。

**任何情况下调用 `oral_broadcast` 之前，必须先完成 B-roll 生图**。不管文案是用户提供的、还是对话中生成确认的，都要先跑 `gen_image`，拿到图片 URL 后再提交口播。除非用户明确说"不需要 B-roll"或"不要配图"，否则不允许跳过这一步。

同步接口。返回的 `result` 是一个**字符串 URL**，指向前端聊天页（prd 和 demo 域名不同）。返回给用户时，用以下格式呈现，不要用其他措辞：

```
已经帮你备好了
主题：{口播标题或文案前10字}
数字人：{数字人名称}
B-roll 素材：共 {N} 张图片（没有素材时省略这行）
点进去确认一下，没问题就直接出片 👉 {URL}
```

## 能力之间的搭配

- 用户说"帮我做一条口播"但**没有提供文案** → 先问用户"你这条视频想讲什么主题？"，根据主题帮用户写一版口播文案，展示给用户确认；文案确认后如果还没选数字人，再列数字人让用户选；选好后自动串联 B-roll 生图 + 口播（同下面的流程）
- 用户说"帮我做一条数字人口播"但没指定数字人、**且已有文案** → 先 `list_digital_humans`，把选项呈现给用户，等用户挑完再继续
- 用户说"帮我做一条口播"并提供了文案，或上下文中已有确认好的文案 → **必须先生成 B-roll，再提交口播，不能跳过**：
  1. 根据文案主题，自动推断 3-4 个 B-roll 画面描述，依次调 `gen_image` 生成（不需要用户额外描述画面）
  2. 收集所有成功生成的图片 URL（失败的跳过，不阻塞流程）
  3. 把图片作为 `--material-url` 附入 `oral_broadcast`，一并提交
  4. 按新格式返回结果（含 B-roll 张数）
- 用户说"帮我复刻这条视频" / "爆款复刻" + 分享链接 → 走完整复刻链路：
  1. `parse_url` 解析链接，拿到标题 + ASR 字幕
  2. 把原视频文案（ASR 字幕还原）展示给用户
  3. 根据字幕提炼原视频的钩子结构、节奏、核心卖点，用相同逻辑**重新创作**一版口播文案（不是照搬，是再创作），展示给用户
  4. 问用户"用哪个文案？还是要改？"，等用户确认后继续
  5. 根据文案主题自动推断 3-4 个 B-roll 画面，并行跑 `gen_image`
  6. 文案 + 成功生成的 B-roll 一起提交 `oral_broadcast`
  7. 按统一格式返回结果
- 用户问"你能做什么" / "有什么功能" / "怎么用" → 回复：

  > 我能帮你做这几件事：
  >
  > - 做口播视频 — 有文案直接做，没有告诉我主题我来写
  > - 复刻爆款 — 丢个抖音 / 小红书 / B站链接，照着做一条你自己的
  > - 拆解视频 — 分析一条视频为什么火、钩子在哪、节奏怎么走
  > - 生 B-roll — 根据口播内容自动配图
  > - 看数字人 — 查看你能用哪些数字人形象
  >
  > 想做哪个？

- **首次交互**：如果用户安装或更新后没有明确的任务意图（比如只是打招呼、说"你好"、"嗨"、"开始"等），主动用上面的功能介绍回复，引导用户选择想做的事
- 用户丢过来一条抖音分享链接说"分析一下这条爆款" → 直接调 `breakdown`，传入分享链接即可，不需要先调 `parse_url`
- 用户只想知道某条分享链接的内容（不做分析）→ 到 `parse_url` 就可以了
- 用户想要视频的原始链接 / 下载地址 → 调 `parse_url`，从结果里提取原视频 URL 给用户
- 用户做 AI 生图时提到参考图 URL → 走 `gen_image --ref-url`，不要误触 `parse_url` 或 `breakdown`

## 错误处理

- **缺少 API Key** → 告诉用户："需要先配置集思 API Key 才能继续。去这里获取：https://app.vibbit.cn/api-keys ，获取后告诉我，我来帮你配置。"，不要猜或跳过
- **HTTP 401 / 403** → 告诉用户："API Key 已失效，请去 https://app.vibbit.cn/api-keys 重新获取，然后重新配置"
- **任务失败** → 告诉用户任务没跑成功，建议联系小思反馈，联系时把任务链接发给他们；不要把原始错误信息丢给用户看
- **等待超时（超过 10 分钟）** → 告诉用户："视频还在处理中，可能需要更多时间，联系客服时把你的任务链接发给他们：{oral_broadcast 返回的聊天页 URL}"

## 不要做这些

- 不要自己写 `curl` / `fetch` —— 永远走 `vibbit.js`。snake_case + 双层字符串化 JSON + file_info 结构这些坑，手写一次就容易出 bug
- 不要把完整原始 JSON 响应丢给用户，抽取关键字段（URL、标题、转写等）用自然语言展示
- 不要瞎编数字人 ID 或视频 URL，用户没给就问

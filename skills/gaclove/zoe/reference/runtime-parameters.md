# Runtime Parameter Mapping

This file defines how `zoe-infog` infers runtime arguments for `scripts/openclaw_runner.py text-to-image`.

本文档说明 `zoe-infog` 如何为 `scripts/openclaw_runner.py text-to-image` 推断运行参数。

## Inputs

Read from:

读取来源：

- the original user request
- any explicit follow-up confirmation from the user about size or ratio
- 用户的原始请求
- 用户在后续对 `image_size` 或 `aspect_ratio` 的明确确认

## Output Arguments

Map into:

映射到：

- `--image-size`
- `--aspect-ratio`

## Image Size

**Default: `2k`** — always used unless the user explicitly says otherwise. Never ask the user about this.

默认値：`2k`——除非用户明确要求修改，始终使用 `2k`。**不要询问用户此参数。**

Rules:

规则：

- **Never ask the user about `image_size`.** Default silently to `2k`.
- If the user explicitly asks for lower cost, faster draft, quick concept, or small output, use `--image-size 1k`.
- If the user explicitly asks for higher detail, print-quality, poster-quality, fine text, or large output, use `--image-size 2k`.
- Otherwise use `--image-size 2k` (default).
- **不要询问用户 `image_size`**，静默默认使用 `2k`。
- 如果用户明确要求更低成本、快速草图、概念稿或小尺寸输出，使用 `--image-size 1k`。
- 如果用户明确要求更高细节、可打印质量、海报质量、精细文字或大尺寸输出，使用 `--image-size 2k`。
- 其他情况默认使用 `--image-size 2k`（默认値）。

## Aspect Ratio

Supported values:

支持的取值：

- `2:3`
- `3:2`
- `3:4`
- `4:3`
- `4:5`
- `5:4`
- `1:1`
- `16:9`
- `9:16`
- `21:9`
- `9:21`

Use the first matching rule:

按以下优先级匹配：

1. If the user explicitly gives a supported ratio, use it directly.
2. If the user confirms a ratio preference in a follow-up turn, use that confirmed value.
3. If the user gives only orientation:
   - `Portrait` or `竖屏` -> prefer `9:16`; use `4:5`, `3:4`, or `2:3` when the prompt implies a print poster, editorial layout, or card-style portrait composition
   - `Landscape` or `横屏` -> prefer `16:9`; use `4:3`, `3:2`, `5:4`, or `21:9` when the prompt implies classic slides, photography framing, near-square cards, or cinematic banners
   - `Square` or `方形` -> `--aspect-ratio 1:1`
4. If neither ratio nor orientation is explicit, infer from the scene:
   - phone wallpaper, story card, vertical reel cover, ultra-tall mobile infographic -> `9:16` or `9:21`
   - print poster, book cover, one-page portrait infographic -> `2:3`
   - editorial illustration, portrait card, magazine-style page -> `3:4`
   - social feed poster, product card, portrait marketing creative -> `4:5`
   - avatar, icon, logo mark, square cover -> `1:1`
   - presentation slide, dashboard, classroom chart, classic screen layout -> `4:3`
   - landscape photo, postcard, brochure hero, medium-width banner -> `3:2`
   - near-square desktop card, comparison board, compact infographic panel -> `5:4`
   - banner, keynote cover, widescreen infographic, landing hero -> `16:9`
   - cinematic hero, panoramic banner, ultra-wide header -> `21:9`
   - otherwise -> `16:9`
5. 如果用户明确给出受支持的比例，直接使用。
6. 如果用户在后续对话中确认了比例偏好，使用确认后的值。
7. 如果用户只给出方向：
   - `Portrait` 或 `竖屏` -> 优先用 `9:16`；如果 prompt 更像印刷海报、编辑排版或卡片式竖构图，则用 `4:5`、`3:4` 或 `2:3`
   - `Landscape` 或 `横屏` -> 优先用 `16:9`；如果 prompt 更像经典幻灯片、摄影构图、近方形卡片或电影感横幅，则用 `4:3`、`3:2`、`5:4` 或 `21:9`
   - `Square` 或 `方形` -> `--aspect-ratio 1:1`
8. 如果比例和方向都没有明确说明，则按场景推断：
   - 手机壁纸、story 卡片、竖版封面、超长移动端信息图 -> `9:16` 或 `9:21`
   - 印刷海报、书封、单页竖版信息图 -> `2:3`
   - 编辑插画、竖版卡片、杂志风页面 -> `3:4`
   - 社媒贴图、商品卡、竖版营销物料 -> `4:5`
   - 头像、图标、logo、小方封面 -> `1:1`
   - 幻灯片、dashboard、课堂图表、经典屏幕布局 -> `4:3`
   - 横版照片、明信片、宣传首图、中等宽度横幅 -> `3:2`
   - 接近方形的桌面卡片、对比面板、紧凑信息图模块 -> `5:4`
   - banner、keynote 封面、横版信息图、落地页首屏 -> `16:9`
   - 电影感首图、全景横幅、超宽页头 -> `21:9`
   - 其他情况默认 -> `16:9`

## Notes

- The skill should pass the user's raw request as `--prompt`.
- `image_size` defaults to `2k` — the Main Agent must NOT ask the user about it.
- `aspect_ratio` is the **primary external input** to confirm with the user when ambiguous.
- Prefer inference over interruption when there is one clearly reasonable choice.
- Ask the user only when multiple aspect ratios are genuinely plausible and the choice would materially change composition or layout.
- When asking the user, ask for `aspect_ratio` directly instead of a vague "horizontal or vertical" question whenever possible.
- The wrapper owns output naming and the final output path; parameter mapping stops at `--image-size` and `--aspect-ratio`.
- If the request needs additional runtime controls such as `--seed` or `--timeout`, pass them separately; they are not inferred here.
- skill 应直接把用户原始请求作为 `--prompt` 传入。
- `image_size` 默认 `2k`，Main Agent 不得询问用户此参数。
- `aspect_ratio` 是需要向用户确认的**主要外部输入**（仅在歧义时确认）。
- 如果只有一个明显合理的选择，优先推断，不要打断用户。
- 只有当多个比例都合理、且会明显影响构图或布局时，才询问用户。
- 需要询问时，尽量直接让用户确认 `aspect_ratio`，不要只问“横版还是竖版”。
- 输出命名和最终输出路径由 wrapper 负责；参数推断只覆盖 `--image-size` 和 `--aspect-ratio`。
- 如果请求需要额外运行参数，例如 `--seed` 或 `--timeout`，应单独传递，这些参数不在这里推断。

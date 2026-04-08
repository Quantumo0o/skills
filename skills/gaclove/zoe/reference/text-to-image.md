# Text-to-Image Reference

This file defines the `text-to-image` flow for `zoe-infog`.

本文档定义 `zoe-infog` 的 `text-to-image` 流程。

## Output Format

- Both scripts support `--output-format json` (or `-o json`) for structured output.
- JSON mode outputs a single JSON object with `status`, `output`, `task_id`, `message`, and `error` fields.
- Text mode (default) maintains backward compatibility with human-readable output.
- 两个脚本都支持 `--output-format json`（或 `-o json`）用于结构化输出。
- JSON 模式输出单个 JSON 对象，包含 `status`、`output`、`task_id`、`message` 和 `error` 字段。
- 文本模式（默认）保持向后兼容的人类可读输出。

## Preflight (Main Agent only)

- Before execution, decide `image_size` (default: `2k`) and `aspect_ratio`.
- Send those two items to the user before generation starts.
- If `aspect_ratio` is materially ambiguous, ask the user first. `image_size` must not be asked.
- 在开始执行前，先确定 `image_size`（默认 `2k`）和 `aspect_ratio`。
- 开始生成前，先把这两项发给用户。
- 如果 `aspect_ratio` 存在会明显影响结果的歧义，应先询问用户。`image_size` 不要询问。

## Prompt Rule

- `--prompt` is exactly the user's raw generation request (verbatim source / instruction).
- Do not append analysis, steering blocks, or a rewritten brief.
- Do not paraphrase user-supplied facts or add new data to `--prompt`.
- Do not run a separate “creative re-prompt” pass; the backend model still handles prompt expansion beyond what you pass.
- `--prompt` 直接使用用户的原始生成请求（原文/原粘贴）。
- 不追加分析、Steering block 或重写版 brief。
- 不对用户事实做改写，不编造数据。

## Runtime Parameters

- Infer `--image-size` and `--aspect-ratio` with `reference/runtime-parameters.md`.
- Reuse the values already decided in preflight for the final generation call.
- If the user already confirmed these values in a follow-up turn, use the confirmed values.
- 使用 `reference/runtime-parameters.md` 推断 `--image-size` 和 `--aspect-ratio`。
- 最终生成时，直接复用预检里已经确定的参数。
- 如果用户在后续对话里已经确认过，就直接使用确认值。

## Execution (Worker Agent only)

- Run the actual script invocation in the Worker Agent after preflight is complete.
- Execute through `reference/openclaw-execution.md`.
- Run `python scripts/openclaw_runner.py text-to-image`.
- 预检完成后，实际脚本调用必须放到 Worker Agent 中执行。
- 通过 `reference/openclaw-execution.md` 执行。
- 使用 `python scripts/openclaw_runner.py text-to-image`。

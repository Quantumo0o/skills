# Image-Edit Reference

This file defines the `image-edit` flow for `zoe-infog`.

本文档定义 `zoe-infog` 的 `image-edit` 流程。

## Output Format

- Both scripts support `--output-format json` (or `-o json`) for structured output.
- JSON mode outputs a single JSON object with `status`, `output`, `task_id`, `message`, and `error` fields.
- Text mode (default) maintains backward compatibility with human-readable output.
- 两个脚本都支持 `--output-format json`（或 `-o json`）用于结构化输出。
- JSON 模式输出单个 JSON 对象，包含 `status`、`output`、`task_id`、`message` 和 `error` 字段。
- 文本模式（默认）保持向后兼容的人类可读输出。

## Input Check

- Only verify that a usable source image is present.
- If the source image is valid, proceed directly without an extra preflight summary.
- 只需要确认有可用的源图输入。
- 如果源图有效，直接继续执行，不需要额外的生成前摘要。

## Source Image

- Resolve the source image into a usable local path, remote URL, or cached file key before calling the backend.
- If no source image is available, stop and report the real reason.
- 在调用后端前，先把源图解析成可用的本地路径、远程 URL 或缓存文件键。
- 如果没有可用源图，直接停止并返回真实原因。

## Prompt Rule

- Use the user's raw edit instruction as `--prompt`.
- Do not run prompt engineering for image edit.
- 直接把用户的原始编辑指令作为 `--prompt`。
- `image-edit` 不做 prompt engineering。

## Execution (Worker Agent only)

- Run the actual script invocation in the Worker Agent.
- Execute through `reference/openclaw-execution.md`.
- Run `python scripts/openclaw_runner.py image-edit`.
- 实际脚本调用必须放到 Worker Agent 中执行。
- 通过 `reference/openclaw-execution.md` 执行。
- 使用 `python scripts/openclaw_runner.py image-edit`。

---
name: zoe-infog
description: >-
  使用 Zoe 模型生成新图片或编辑已有图片，适用于信息图、海报、插图等视觉内容。Use when the user explicitly asks to create a new image, infographic, poster, or illustration, or asks to edit an existing image and provides a source image. Trigger phrases include 'zoe-infog', 'zoe 出图', 'zoe 生图', '生成信息图', '做一张图', '帮我画', 'create infographic', 'generate image with zoe', and edit intents such as '修改这张图' or 'edit this image'. Do not trigger for discussing existing results, asking how the skill works, or mentioning images without a real generation or edit request.
metadata:
  version: "0.11.0"
  tags: ["text-to-image", "image-edit", "zoe"]
  requires:
    bins: ["python"]
    libs: ["httpx"]
---

# Zoe Infographic

Use `scripts/openclaw_runner.py` as the execution entrypoint.

## Agent Architecture

This skill uses a **two-agent pattern**:

- **Main Agent**: Handles user interaction, infers parameters (`aspect_ratio`; `image_size` defaults to `2k`), sends preflight confirmation, launches the Worker Agent, and delivers the final result to the user.
- **Worker Agent** (Sub-Agent): Receives finalized parameters, executes `scripts/openclaw_runner.py`, and returns a structured JSON result to the Main Agent. The Worker Agent never sends user-visible messages.

**此技能属于长时间运行任务（long-running task）。**

**调用脚本时必须使用 Worker Agent（Sub-Agent）执行**，避免阻塞主会话：

- 任何 `python scripts/...` 执行都必须放到 Sub-Agent 中运行。
- 不要依赖 frontmatter 或超时机制自动切换到后台执行。

## Trigger Rules

### text-to-image

Trigger only when all of these are true:

1. The user explicitly asks to create a new image.
2. The requested artifact is visual content such as an infographic, poster, illustration, or generic image.
3. The request is a new generation request, not a reaction to an already generated result.

Do not trigger for:

- discussing an existing image
- asking how the skill works
- mentioning "image" without an actual generation request
- agent-authored text that happens to contain trigger words

### image-edit

Trigger only when both of these are true:

1. The user explicitly asks to edit or rewrite an existing image.
2. A source image is available as a URL, local path, cached file key, or can be resolved from a platform attachment.

If the user asks to edit but no source image is available, stop and tell them the edit flow needs the original image.

## Main Agent: Parameter Inference

### External Inputs

The Main Agent collects from the user:

1. **`aspect_ratio`** — inferred from prompt content, scene type, or explicit user statement. See `reference/runtime-parameters.md` for the full priority and mapping rules.
2. **`image_size`** — defaults to `2k`. Only deviate if the user explicitly asks for lower cost / draft quality (`1k`) or explicitly requests higher detail (`2k` is already the default).

All other parameters (prompt, seed, unet-name) follow rules in `reference/runtime-parameters.md` and `reference/unet-name-parameter.md`.

### When to Ask the User

- Ask for `aspect_ratio` only when multiple ratios are genuinely plausible and the choice would materially change composition or layout.
- Never ask about `image_size`; default silently to `2k`.
- When asking, wait for the user's reply before proceeding. On the very next turn, merge the answer and **in the same turn** continue with preflight and Worker Agent launch.

## Main Agent: Flow

1. Decide whether the request is `text-to-image` or `image-edit`.
2. **For `text-to-image`:**
   a. Infer `aspect_ratio` from the prompt using `reference/runtime-parameters.md`. Set `image_size = 2k` (default).
   b. If `aspect_ratio` is materially ambiguous, ask the user and wait for confirmation.
   c. Send one preflight message in the user's conversation listing the chosen `image_size` and `aspect_ratio`.
   d. Launch the **Worker Agent** with: `prompt`, `image_size`, `aspect_ratio`, and the skill's working directory.
   e. When the Worker Agent returns `status=ok` and `need_main_agent_send=true`, deliver the result image to the user's conversation, then end with `NO_REPLY`.
   f. On Worker Agent failure, report the real error to the user.
3. **For `image-edit`:**
   a. Verify a source image is available. If not, stop and tell the user.
   b. Do NOT send a preflight summary for image-edit.
   c. Launch the **Worker Agent** with: `source_image`, `prompt`, and the skill's working directory.
   d. When the Worker Agent returns `status=ok` and `need_main_agent_send=true`, deliver the result image to the user's conversation, then end with `NO_REPLY`.
   e. On Worker Agent failure, report the real error to the user.
4. Do not send the generic `您的请求正在处理中，完成后会自动发送结果。` message before the preflight message.
5. Keep all user-visible preflight and delivery in the **same conversation** that triggered the skill.

## Worker Agent: Execution Flow

The Worker Agent receives finalized parameters from the Main Agent and must:

### text-to-image

1. Follow `reference/text-to-image.md`.
2. Use the prompt verbatim — do not rewrite or add steering blocks.
3. Execute via `reference/openclaw-execution.md`:
   ```bash
   python scripts/openclaw_runner.py text-to-image \
     --prompt "$PROMPT" \
     --image-size 2k \
     --aspect-ratio "$ASPECT_RATIO" \
     -o json
   ```
4. Parse the script's JSON stdout.
5. Return structured JSON to the Main Agent (see Return Contract). Do not send any user-visible messages.

### image-edit

1. Resolve the source image into a usable URL, local path, or cached file key.
2. Follow `reference/image-edit.md`.
3. Execute via `reference/openclaw-execution.md`:
   ```bash
   python scripts/openclaw_runner.py image-edit \
     --image "$SOURCE_IMAGE" \
     --prompt "$PROMPT" \
     -o json
   ```
4. Parse the script's JSON stdout.
5. Return structured JSON to the Main Agent (see Return Contract). Do not send any user-visible messages.

## Return Contract

The Worker Agent returns this shape to the Main Agent:

```json
{
  "status": "ok|error",
  "output_file": "/tmp/openclaw/...",
  "message": "<prompt or edit instruction>",
  "need_main_agent_send": true,
  "task_id": "<task id from script>",
  "error": "<only on failure>"
}
```

Rules:

- `output_file` must point to the wrapper-managed output path (owned by `openclaw_runner.py`).
- `need_main_agent_send` is `true` only on successful generation.
- Report the real failure reason in `error`; do not invent fallback explanations.
- Do not include `error` on success; do not include `output_file` on failure.

## Guardrails

- Keep preflight and final delivery in the user's conversation. All script execution must happen in the Worker Agent (Sub-Agent), which returns structured JSON instead of sending extra user-visible messages.
- Do not trigger a second `zoe-infog` run while one is already in flight in the same conversation.
- Do not bypass `scripts/openclaw_runner.py` by hand-building timestamped output paths.
- For `text-to-image`, extract only `image_size` and `aspect_ratio` as runtime parameters. Pass the user's original request directly as `--prompt`.
- For `text-to-image`, every run that starts generation must have the preflight in the **user's conversation**, including turns that follow a parameter clarification—never skip preflight after the user confirms `aspect_ratio`.
- Never assume frontmatter, timeout behavior, or the runtime will automatically convert execution into a Sub-Agent. Explicitly start the Worker Agent before calling scripts.
- Use repo-relative paths in reasoning and docs. Use deployed absolute paths only when the execution reference explicitly asks for an example.

## References

- `reference/text-to-image.md`: `text-to-image` flow
- `reference/image-edit.md`: `image-edit` flow
- `reference/runtime-parameters.md`: infer `--aspect-ratio` (and optionally `--image-size`; default is `2k`)
- `reference/openclaw-execution.md`: wrapper entrypoint, command templates, output file naming, JSON return expectations
- `reference/unet-name-parameter.md`: when and how to pass `--unet-name`

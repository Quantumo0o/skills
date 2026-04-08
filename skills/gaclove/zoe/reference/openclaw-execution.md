# OpenClaw Execution Reference

This file is OpenClaw-specific. It defines how to execute generation after the raw prompt and runtime parameters are ready.

Actual script execution must happen in the **Worker Agent** (Sub-Agent). Do not rely on timeout behavior or metadata to convert execution automatically.

## Entrypoint

Use the wrapper:

- Repo path: `scripts/openclaw_runner.py`

The wrapper owns:

- timestamped filenames
- the `/tmp/openclaw` output directory
- the final output path used by the low-level clients

Do not rebuild those rules manually in shell variables.


This ensures relative paths in scripts resolve correctly.

## Command Templates

**IMPORTANT**: Always add `-o json` to get structured output that's easy to parse.

### text-to-image

```bash
python scripts/openclaw_runner.py text-to-image \
  --prompt "$USER_REQUEST" \
  --image-size 2k \
  --aspect-ratio 16:9 \
  -o json
```

With optional UNet model (only when user explicitly specifies):

```bash
python scripts/openclaw_runner.py text-to-image \
  --prompt "$USER_REQUEST" \
  --image-size 2k \
  --aspect-ratio 16:9 \
  --unet-name "custom-model" \
  -o json
```

### image-edit

```bash
python scripts/openclaw_runner.py image-edit \
  --image "$SOURCE_IMAGE" \
  --prompt "$PROMPT" \
  -o json
```

`$SOURCE_IMAGE` 可以是本地路径、可访问 URL，或下游脚本可识别的缓存文件键。只有当飞书消息图片本身不是直链时，才先通过 `feishu_im_bot_image` 之类的工具解析成本地文件或可用链接。

Optional flags for either mode:

- `--base-url`
- `--api-key`
- `--seed`
- `--unet-name` (text-to-image only, optional)
- `--poll-interval`
- `--timeout`
- `--insecure`
- `-o json` or `--output-format json` (REQUIRED for structured output)

Environment lookup:

- `openclaw_runner.py` reads `ZOE_INFOG_API_KEY`

## Output Naming

The wrapper always writes to `/tmp/openclaw`:

- text-to-image: `/tmp/openclaw/zoe_infog_<timestamp>.png`
- image-edit: `/tmp/openclaw/zoe_edit_<timestamp>.png`

## Worker Agent: Parsing Script Output

The Worker Agent must parse the script's JSON stdout and transform it into the return contract for the Main Agent:

```python
import json
import subprocess

result = subprocess.run(
    ["python", "scripts/openclaw_runner.py", "text-to-image",
     "--prompt", prompt,
     "--image-size", image_size,
     "--aspect-ratio", aspect_ratio,
     "-o", "json"],
    capture_output=True,
    text=True
)

# Parse script JSON output
script_output = json.loads(result.stdout)

# Transform to Worker Agent return contract for Main Agent
if script_output["status"] == "ok":
    return {
        "status": "ok",
        "output_file": script_output["output"],
        "message": prompt,
        "need_main_agent_send": True,
        "task_id": script_output.get("task_id", "")
    }
else:
    return {
        "status": "error",
        "output_file": "",
        "message": prompt,
        "need_main_agent_send": False,
        "error": script_output.get("error", "Unknown error"),
        "task_id": script_output.get("task_id", "")
    }
```

## Sub-Agent Return JSON

Transform the script's JSON output into this format for the main agent:

### Success

```json
{
  "status": "ok",
  "output_file": "/tmp/openclaw/zoe_infog_20260324_120000.png",
  "message": "<prompt or edit instruction>",
  "need_main_agent_send": true,
  "task_id": "69cb49c57496994fbec7bbd3"
}
```

### Failure

```json
{
  "status": "error",
  "output_file": "",
  "message": "<prompt or edit instruction>",
  "need_main_agent_send": false,
  "error": "<actual error>",
  "task_id": "69cb49c57496994fbec7bbd3"
}
```

## Error Handling

- If source image resolution fails for `image-edit`, stop before calling Zoe.
- For `text-to-image`, do not add a prompt-engineering step in the skill. Use the user's original request and inferred runtime parameters directly.
- Parse the JSON output to get the real error message from the `error` field.
- Return structured JSON only. Final user-visible delivery should happen in the same conversation after the run completes.

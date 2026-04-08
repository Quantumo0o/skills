# UNet Name Parameter

## Overview

The `--unet-name` parameter is an optional parameter for text-to-image generation that allows specifying a custom UNet model.

`--unet-name` 参数是 text-to-image 生成的可选参数，允许指定自定义的 UNet 模型。

## Usage

### When to Use

Only pass `--unet-name` when:

- The user explicitly specifies a UNet model name
- You have a specific model requirement

只在以下情况传递 `--unet-name`：

- 用户明确指定了 UNet 模型名称
- 有特定的模型需求

### When NOT to Use

Do NOT pass `--unet-name` when:

- The user doesn't mention a specific model
- Using default model behavior
- No model preference specified

不要在以下情况传递 `--unet-name`：

- 用户没有提到特定模型
- 使用默认模型行为
- 没有指定模型偏好

## Examples

### With UNet Name

```bash
# Direct script call
python scripts/text_to_image_request.py \
  --prompt "a cute cat" \
  --image-size 2k \
  --aspect-ratio 1:1 \
  --unet-name "custom-model-v2" \
  -o json

# Via openclaw_runner
python scripts/openclaw_runner.py text-to-image \
  --prompt "a cute cat" \
  --unet-name "custom-model-v2" \
  -o json
```

### Without UNet Name (Default)

```bash
# Direct script call
python scripts/text_to_image_request.py \
  --prompt "a cute cat" \
  --image-size 2k \
  --aspect-ratio 1:1 \
  -o json

# Via openclaw_runner
python scripts/openclaw_runner.py text-to-image \
  --prompt "a cute cat" \
  -o json
```

## API Payload

When `--unet-name` is provided, it's included in the API request:

```json
{
  "prompt": "a cute cat",
  "negative_prompt": "",
  "image_size": "2k",
  "aspect_ratio": "1:1",
  "unet_name": "custom-model-v2"
}
```

When NOT provided, it's omitted from the payload:

```json
{
  "prompt": "a cute cat",
  "negative_prompt": "",
  "image_size": "2k",
  "aspect_ratio": "1:1"
}
```

## In Skill Code

```python
import json
import subprocess

# Example 1: Without unet_name (most common)
result = subprocess.run(
    ["python", "scripts/text_to_image_request.py",
     "--prompt", "a cute cat",
     "-o", "json"],
    capture_output=True,
    text=True
)

# Example 2: With unet_name (when user specifies)
result = subprocess.run(
    ["python", "scripts/text_to_image_request.py",
     "--prompt", "a cute cat",
     "--unet-name", "custom-model",
     "-o", "json"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
```

## Notes

- `unet_name` is optional and should only be passed when explicitly needed
- The default behavior (without `unet_name`) uses the API's default model
- Invalid model names will result in API errors
- Check with the API documentation for available model names

---

**Parameter Type**: Optional string
**Default**: None (uses API default)
**Added in**: Current version

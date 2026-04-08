---
name: ai-gateway
description: Access 340+ AI models through the Agnic AI Gateway. Use when the user wants to chat with an AI model, generate images with AI, list available models, delegate a task to another LLM, or get a second opinion. Covers phrases like "ask GPT", "use Claude", "generate an image", "list AI models", "chat with AI", "call a model", "what models are available".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest ai *)"]
---

# AI Gateway

Use `npx agnic@latest ai` commands to access 340+ AI models (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more) through the Agnic AI Gateway. Costs are deducted from your USDC balance per token. Free models available for development.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

### List models

```bash
npx agnic@latest ai models [options]
```

### Chat with a model

```bash
npx agnic@latest ai chat --model <id> --prompt "<text>" [options]
```

### Generate an image

```bash
npx agnic@latest ai image --prompt "<text>" [options]
```

## Model Format

Models use `provider/model-name` format:

| Provider | Example Models |
| ----------- | ----------------------------------------- |
| openai | `openai/gpt-4o`, `openai/gpt-4-turbo` |
| anthropic | `anthropic/claude-3.5-sonnet` |
| google | `google/gemini-2.5-flash-image`, `google/gemma-*` |
| meta-llama | `meta-llama/llama-3.3-70b` |
| mistralai | `mistralai/mistral-large-latest` |
| deepseek | `deepseek/deepseek-chat` |

Free models: `meta-llama/*`, `google/gemma-*`, `mistralai/*`

## Options

### ai models

| Option | Description |
| -------------------- | ---------------------------------------- |
| `--provider <name>` | Filter by provider (e.g., openai) |
| `--search <term>` | Search in model name |
| `--json` | Output as JSON |

### ai chat

| Option | Description |
| ----------------------- | ---------------------------------------- |
| `--model <id>` | Model ID (required) |
| `--prompt <text>` | User message (required) |
| `--system <text>` | System prompt |
| `--temperature <n>` | Temperature 0-2 (default: 0.7) |
| `--max-tokens <n>` | Max tokens in response |
| `--json` | Output as JSON |

### ai image

| Option | Description |
| ------------------------- | ---------------------------------------- |
| `--prompt <text>` | Image description (required) |
| `--model <id>` | Model (default: google/gemini-2.5-flash-image) |
| `--aspect-ratio <ratio>` | 1:1, 16:9, 9:16, 4:3, 3:2 (default: 1:1)|
| `--output <path>` | Save image to file |
| `--json` | Output as JSON |

## Input Validation

Before constructing the command, validate all user-provided values:

- **model**: Must match `^[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+$` (provider/model format). Reject if it contains spaces, semicolons, pipes, or backticks.
- **prompt**: Single-quote the value to prevent shell expansion. Escape internal single quotes.
- **temperature**: Must be a number between 0 and 2 (`^[0-2](\.\d+)?$`).
- **aspect-ratio**: Must be one of: `1:1`, `16:9`, `9:16`, `4:3`, `3:2`.
- **output**: Must be a valid file path. Reject if it contains shell metacharacters.

Do not pass unvalidated user input into the command.

## Examples

```bash
# List all available models
npx agnic@latest ai models --json

# List only OpenAI models
npx agnic@latest ai models --provider openai

# Search for GPT models
npx agnic@latest ai models --search gpt

# Chat with GPT-4o
npx agnic@latest ai chat --model openai/gpt-4o --prompt 'Explain quantum computing in one sentence'

# Chat with system prompt
npx agnic@latest ai chat --model anthropic/claude-3.5-sonnet --system 'You are a helpful coding assistant' --prompt 'Write a Python hello world'

# Use a free model
npx agnic@latest ai chat --model meta-llama/llama-3.3-70b --prompt 'What is 2+2?' --json

# Generate an image
npx agnic@latest ai image --prompt 'A sunset over mountains' --output sunset.png

# Generate widescreen image
npx agnic@latest ai image --prompt 'Cyberpunk cityscape' --aspect-ratio 16:9 --output city.png

# Use a specific image model
npx agnic@latest ai image --prompt 'A portrait painting' --model openai/gpt-5-image --output portrait.png
npx agnic@latest ai image --prompt 'Abstract art' --model black-forest-labs/flux.2-max --output art.png

# Get image as JSON (base64)
npx agnic@latest ai image --prompt 'Logo design for a tech startup' --json
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Wallet must have USDC balance (free models available for testing)
- Image generation models:
  - `google/gemini-2.5-flash-image` (default) — fast, good quality
  - `google/gemini-3-pro-image-preview` — highest quality Google model
  - `google/gemini-3.1-flash-image-preview` — latest flash preview
  - `openai/gpt-5-image` — OpenAI image generation
  - `black-forest-labs/flux.2-max` — Flux high quality
  - `black-forest-labs/flux.2-klein-4b` — Flux lightweight/fast

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- "Insufficient balance" — Fund wallet at https://pay.agnic.ai
- "Model not found" — Check available models with `npx agnic@latest ai models`
- "No image returned" — Try a different model or rephrase the prompt
- "Rate limit exceeded" — Wait a moment and retry

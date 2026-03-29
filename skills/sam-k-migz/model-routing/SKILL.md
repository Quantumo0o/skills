# Model Routing Skill (Compact)

Automatically route each request to the best model.

Routing rules:
- Use `gpt-5-codex` for coding, debugging, build errors, stack traces, logs, repo edits, and implementation tasks.
- Use `gpt-5` for deep reasoning, architecture, large-context analysis, complex planning, and hard diagnosis.
- Use `gpt-4.1-nano` for short trivial requests with no code and no deep reasoning.
- Use `gpt-5-mini` for everything else.

Priority:
1. code_heavy
2. heavy_reasoning
3. simple
4. normal

Fallbacks:
- `gpt-5-codex` -> `gpt-5` -> `gpt-5-mini` -> `gpt-4.1-nano`
- `gpt-5` -> `gpt-5-mini` -> `gpt-4.1-nano`
- `gpt-5-mini` -> `gpt-4.1-nano`

Retry on:
- rate limit
- TPM exceeded
- timeout
- temporary unavailable
- capacity errors

Concurrency:
- max 2 concurrent requests
- reduce to 1 for large prompts or repeated TPM failures
- queue excess work

Respect user override if they explicitly force a model.
Otherwise ignore the UI-selected model and use automatic routing.

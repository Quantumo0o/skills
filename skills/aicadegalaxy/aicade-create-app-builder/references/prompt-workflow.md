# Prompt Workflow

This skill uses the same logic as the documented `3.1 -> 3.2` workflow.

## Access Check First

Before entering prompt assembly, first confirm whether the user has already applied for app access on:

- `https://www.aicadegalaxy.com/`

If not, direct them to:

- `https://docs.aicadegalaxy.com/white-paper/application-document`

Only after app access is granted can the user obtain the three required environment variables:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`
- `AICADE_API_APP_NO`

## 3.1 Input Model

Start with the user's base business prompt, then append platform integration additions such as:

- SDK invocation requirements
- storage replacement strategy
- wallet or account display
- selected SDK modules
- optional score, currency, token, AI chat, NFT, or payment constraints

## 3.2 Output Style

The final output should be one integrated prompt that:

1. Keeps the user's original business prompt structure
2. Adds a dedicated `ts sdk 整合要求` or equivalent section
3. Keeps technical requirements and output requirements
4. Is ready to paste directly into an IDE AI assistant

## Important Rule

Do not redesign the user's business structure unless asked.

This skill should assemble and strengthen the prompt, not replace the user's own product description format.

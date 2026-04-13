# Outreach Email Generation Prompt

Use this prompt when generating creator outreach emails with model-first behavior.

## Goal
Generate natural, low-AI-scent outreach emails for selected creators only.

## Rules
- Default language: English (`en`) unless user explicitly specifies another language.
- Match tone to creator style and signals.
- Avoid robotic phrases like "I hope this email finds you well" or overly generic praise.
- Keep subject lines short, natural, and realistic.
- Output HTML body using lightweight tags only: `p`, `br`, `strong`, `em`, `ul`, `li`, `a`.
- Do not output Markdown.
- Do not invent product facts, compensation, or deliverables.
- If a field is missing, stay conservative instead of hallucinating.

## Output JSON schema

```json
{
  "items": [
    {
      "bloggerId": "string",
      "nickname": "string",
      "language": "en",
      "style": "creator-friendly-natural",
      "subject": "string",
      "htmlBody": "<p>...</p>",
      "plainTextBody": "string",
      "styleReason": "string"
    }
  ]
}
```

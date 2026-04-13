# Outreach Email Draft Schema

Each generated email draft should contain:

- `bloggerId`: selected creator id
- `nickname`: creator display name
- `language`: output language code, default `en`
- `style`: short style label, e.g. `commerce-natural`
- `subject`: final email subject
- `htmlBody`: HTML email body using lightweight tags only
- `plainTextBody`: plain text fallback
- `styleReason`: optional short explanation for why this tone/style was chosen

## Notes
- HTML body is the primary send format.
- Plain text body is the compatibility fallback.
- Model output should be preferred; script output is fallback-only.
- For real outbound sends, use model-first personalized drafts by default; do not treat fallback script drafts as the default send path just to save time.
- Default language policy: subject + body must be English unless the user explicitly requests another supported language.

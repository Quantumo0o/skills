# Awesome List Submissions

## 1. hesreallyhim/awesome-claude-code

**IMPORTANT**: This repo requires submission via the GitHub web UI issue form only. CLI (`gh`) submissions are explicitly banned and will result in a temporary or permanent ban. The user must manually fill out the form at:
https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml

### Issue Form Fields

- **Title**: `[Resource]: privacy-mask`
- **Display Name**: `privacy-mask`
- **Category**: `Agent Skills`
- **Sub-Category**: `General`
- **Primary Link**: `https://github.com/fullstackcrew-alpha/privacy-mask`
- **Author Name**: `wuhao`
- **Author Link**: `https://github.com/fullstackcrew-alpha`
- **License**: `MIT`
- **Description**:

> Local image privacy masking tool that detects and redacts sensitive information (PII, API keys, secrets) in screenshots via OCR and regex before images leave your machine. Ships with 47 regex detection rules covering credit cards, SSNs, AWS keys, GitHub tokens, JWTs, and more. Supports Tesseract and RapidOCR engines. Integrates as a Claude Code hook (UserPromptSubmit) to automatically mask pasted screenshots. 100% offline, zero network calls.

- **Validate Claims**:

> Install via `pip install privacy-mask`, then run `privacy-mask path/to/screenshot.png -o masked.png`. The tool will detect and redact any visible PII, API keys, or secrets in the image. You can also test the detection engine directly: `python -c "from mask_engine.detector import detect_sensitive; print(detect_sensitive('sk-proj-abc123def456ghi789'))"` which will identify it as an OpenAI API key.

- **Specific Task(s)**:

> Take a screenshot that contains a visible API key or email address. Run `privacy-mask screenshot.png -o masked.png` and verify that the sensitive regions are redacted with black boxes in the output image. Alternatively, install as a Claude Code hook and paste a screenshot containing PII into Claude Code — the hook will automatically mask it before Claude processes the image.

- **Specific Prompt(s)**:

> After installing the hook (`privacy-mask install-hook`), paste a screenshot containing a visible API key or email address into Claude Code. Claude will receive the masked version with sensitive regions redacted. You can verify by asking Claude to describe what it sees in the image — it should not be able to read the redacted content.

- **Additional Comments**:

> privacy-mask was built specifically for the Claude Code workflow where users frequently paste screenshots that may contain sensitive information. The UserPromptSubmit hook integration means masking happens transparently before any data reaches the API. The tool uses a two-stage detection pipeline: first OCR (Tesseract or RapidOCR) extracts text and bounding boxes, then 47 regex rules plus optional NER identify sensitive spans, and finally those regions are redacted in the original image. All processing is local — no network calls are made.

- **Checklist**: All boxes checked (resource not already submitted, over one week old, links working, no other open issues, human submitter)

---

## 2. travisvn/awesome-claude-skills

**Process**: Submit a PR adding a row to the "Individual Skills" table in the Community Skills section.

### Exact markdown to add

Add this row to the `Individual Skills` table (in the `### Individual Skills` section, alphabetically or at the end of the table):

```markdown
| **[privacy-mask](https://github.com/fullstackcrew-alpha/privacy-mask)** | Local image privacy masking — detect and redact PII, API keys, and secrets in screenshots via OCR + 47 regex rules. Installs as a Claude Code hook for automatic masking. 100% offline |
```

### Where it goes

In `README.md`, under `## Community Skills > ### Individual Skills`, add the row to the existing table. It fits naturally near the end or alphabetically between `playwright-skill` and `web-asset-generator`.

---

## 3. ComposioHQ/awesome-claude-plugins

**Process**: Submit a PR. Add entry under the `### Documentation & Security` section (best fit since it's a security/privacy tool).

### Exact markdown line to add

Under `### Documentation & Security`:

```markdown
- [privacy-mask](https://github.com/fullstackcrew-alpha/privacy-mask) - Local image privacy masking tool. Detects and redacts PII, API keys, and secrets in screenshots via OCR + 47 regex rules before they reach Claude. Installs as a UserPromptSubmit hook. 100% offline, zero network calls.
```

---

## 4. ccplugins/awesome-claude-code-plugins

**Process**: Submit a PR. Add entry under the `### Security, Compliance, & Legal` section.

### Exact markdown line to add

Under `### Security, Compliance, & Legal`:

```markdown
- [privacy-mask](https://github.com/fullstackcrew-alpha/privacy-mask) - Detect and redact PII, API keys, and secrets in screenshots via OCR + regex before images reach Claude. 47 detection rules, Tesseract/RapidOCR support, UserPromptSubmit hook integration. 100% offline.
```

---

## 5. sickn33/antigravity-awesome-skills

**Process**: Submit a PR adding a skill entry. This repo has 1,273+ skills organized in a `skills/` directory with individual SKILL.md files, but external contributions can also be added as links in the README.

### Exact markdown line to add

Under `## Security & Web Testing` section (best category fit), or as a new entry in the skills table:

```markdown
- [privacy-mask](https://github.com/fullstackcrew-alpha/privacy-mask) - Local image privacy masking for AI coding agents. Detects and redacts PII, API keys, and secrets in screenshots via OCR + 47 regex rules. Claude Code hook integration for automatic masking before images reach the API. Supports Tesseract and RapidOCR. 100% offline.
```

---

## 6. BehiSecc/awesome-claude-skills

**Process**: Submit a PR. The list is organized by category with emoji section headers.

### Exact markdown line to add

Under `## Security & Web Testing` section (where VibeSec-Skill and other security tools are listed):

```markdown
- [privacy-mask](https://github.com/fullstackcrew-alpha/privacy-mask) - Local image privacy masking — detect and redact PII, API keys, and secrets in screenshots via OCR + 47 regex rules before images leave your machine. Claude Code hook for automatic redaction. 100% offline.
```

---

# Anthropic Official Plugin Directory Submission

## Submission Process

The official Anthropic plugin directory is at **github.com/anthropics/claude-plugins-official** (12,700+ stars). External plugin submissions use a dedicated form:

**Submission URL**: https://clau.de/plugin-directory-submission

This is referenced in the repo's README under "Contributing > External Plugins":
> "Third-party partners can submit plugins for inclusion in the marketplace. External plugins must meet quality and security standards for approval. To submit a new plugin, use the plugin directory submission form."

### Submission Content

Prepare the following information for the form:

- **Plugin Name**: privacy-mask
- **Repository URL**: https://github.com/fullstackcrew-alpha/privacy-mask
- **PyPI Package**: https://pypi.org/project/privacy-mask/
- **Author / Organization**: fullstackcrew-alpha
- **License**: MIT
- **Category**: Security / Privacy

- **Short Description**:
> Local image privacy masking tool for Claude Code. Detects and redacts sensitive information (PII, API keys, secrets) in screenshots via OCR + regex before images reach the API.

- **Detailed Description**:
> privacy-mask is a security-focused Claude Code plugin that automatically masks sensitive information in screenshots before they are sent to the Claude API. It installs as a UserPromptSubmit hook that intercepts image attachments, runs them through a two-stage detection pipeline (OCR text extraction followed by 47 regex pattern rules + optional NER), and redacts identified sensitive regions with black boxes.
>
> Key features:
> - 47 built-in regex detection rules covering credit cards, SSNs, emails, phone numbers, AWS keys, GitHub tokens, Stripe keys, JWTs, database connection strings, and more
> - Dual OCR engine support (Tesseract and RapidOCR)
> - Optional spaCy NER for entity detection beyond regex patterns
> - 100% offline processing — zero network calls, all data stays local
> - CLI tool for standalone use: `privacy-mask input.png -o masked.png`
> - Installable as Claude Code hook: `privacy-mask install-hook`
> - Available on PyPI: `pip install privacy-mask`

- **Why it should be included**:
> Screenshot sharing is a core Claude Code workflow, and users frequently paste screenshots containing visible API keys, credentials, PII, or other secrets. privacy-mask addresses this security gap by automatically redacting sensitive content before it reaches the API, with zero configuration required after hook installation. It is fully offline (no data leaves the machine), MIT-licensed, and has comprehensive test coverage (208+ test cases). The tool fills a unique niche — there is no other Claude Code plugin focused specifically on image-level PII redaction.

- **Installation**:
> ```bash
> pip install privacy-mask
> privacy-mask install-hook
> ```

- **Test Plan**:
> 1. Install: `pip install privacy-mask`
> 2. Run on a test image: `privacy-mask screenshot-with-api-key.png -o masked.png`
> 3. Verify sensitive regions are redacted in the output
> 4. Install hook: `privacy-mask install-hook`
> 5. Paste a screenshot with visible PII into Claude Code — verify it is automatically masked

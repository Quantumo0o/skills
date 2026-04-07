# Code Review Intelligence MCP Server

Review, explain, and generate code using local AI. No code is sent to external APIs — 100% privacy.

## Features

| Tool | Description | Price |
|------|-------------|-------|
| `review_code` | Review code for bugs, security, performance, or readability issues | $0.10/use |
| `explain_code` | Explain code with adjustable detail (brief, medium, detailed) | $0.05/use |
| `generate_code` | Generate new code or refactor existing code from instructions | $0.10/use |

## Connect via Claude Desktop

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "code-review": {
      "url": "https://ntriqpro--code-review-intelligence-mcp.apify.actor/mcp?token=YOUR_APIFY_TOKEN"
    }
  }
}
```

## Review Focus Areas

| Focus | Description |
|-------|-------------|
| `general` | Bugs, improvements, best practices (default) |
| `security` | Vulnerabilities: injection, XSS, auth issues, data exposure |
| `performance` | Bottlenecks, unnecessary operations, optimizations |
| `readability` | Naming, structure, documentation, maintainability |

## Supported Languages

All major programming languages: Python, JavaScript, TypeScript, Go, Rust, Java, C++, Ruby, PHP, Swift, Kotlin, and more.

## Input

### review_code
- `code` (required): Source code to review
- `language` (optional): Programming language (default: auto-detect)
- `focus` (optional): "general", "security", "performance", "readability"

### explain_code
- `code` (required): Source code to explain
- `detailLevel` (optional): "brief", "medium", "detailed"

### generate_code
- `instruction` (required): What to build or how to refactor
- `existingCode` (optional): Existing code to refactor
- `language` (optional): Target language (default: "python")

## Output Examples

### review_code (security focus)
```json
{
  "status": "success",
  "review": "**Security Review**\n\n1. **Critical**: SQL injection vulnerability on line 15...\n2. **High**: Hardcoded API key on line 3...",
  "focus": "security",
  "model": "qwen2.5-coder"
}
```

### explain_code (brief)
```json
{
  "status": "success",
  "explanation": "This is a REST API endpoint that handles user authentication using JWT tokens and bcrypt password hashing.",
  "detail_level": "brief",
  "model": "qwen2.5-coder"
}
```

## Technology

- **Code Model**: Qwen2.5-Coder 7B (Apache 2.0 License)
- **Processing**: Local AI inference, zero external API calls
- **Privacy**: Code is processed in real-time and not stored

## Open Source Licenses

This service uses the following open source model:
- [Qwen2.5-Coder](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) — Apache 2.0 License

## Legal Disclaimer

**Code Review Notice**: This service provides AI-generated code analysis suggestions only. All outputs are recommendations and should not be treated as automated decisions. Human review and verification is required before acting on any suggestions. This service does not guarantee the detection of all bugs, vulnerabilities, or issues. Code submitted for analysis is processed in real-time, is not stored, and is not used for model training. This service does not constitute professional software auditing or security certification.

Platform usage is free. You only pay per event (see pricing above).

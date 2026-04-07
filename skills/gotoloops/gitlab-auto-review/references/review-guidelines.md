# Review Guidelines

When reviewing code as part of the gitlab-auto-review skill, evaluate the following aspects:

## Severity Levels

### Critical (Must Fix)
- **Security vulnerabilities**: SQL injection, XSS, command injection, hardcoded secrets, insecure deserialization
- **Data loss risks**: Missing transactions, race conditions, unhandled errors that could corrupt data
- **Authentication/Authorization flaws**: Missing permission checks, token leaks

### Important (Should Fix)
- **Bug-prone patterns**: Off-by-one errors, null pointer risks, unhandled edge cases, incorrect type usage
- **Performance issues**: N+1 queries, unnecessary loops, missing indexes, memory leaks
- **Error handling**: Swallowed exceptions, missing error propagation, unclear error messages

### Suggestions (Nice to Have)
- **Code clarity**: Confusing naming, overly complex logic, missing context for non-obvious code
- **Best practices**: Framework-specific anti-patterns, deprecated API usage
- **Maintainability**: Code duplication that could be reasonably abstracted

## What NOT to Comment On
- Style/formatting issues (leave these to linters)
- Minor naming preferences
- Adding comments to self-explanatory code
- Changes outside the diff context

## Output Format

For each issue found, format your inline comment as:

```markdown
**[severity]** brief_title

description of the issue and why it matters.

suggestion or fix (if applicable):
\`\`\`language
suggested code
\`\`\`
```

Where `severity` is one of: `Critical`, `Important`, `Suggestion`.

## Summary Format

After reviewing all files, post a summary note using the `post-note` command:

```markdown
## MR Code Review Summary

**Result**: ✅ Approved / ⚠️ Changes Requested

**Overview**: Brief description of what this MR does (1-2 sentences based on the diff content).

**Stats**: X files reviewed, Y issues found (Z critical, W important, V suggestions)

### Issues Found (if any)
- `file_path:line` — brief description of each issue

### Highlights (if any)
- Notable positive aspects of the code changes
```

If no issues are found, approve the MR and provide a concise summary of the changes.
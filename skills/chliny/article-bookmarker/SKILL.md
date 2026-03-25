---
name: article-bookmarker
description: Save and organize web articles as bookmarks with AI summaries and auto-tagging. Use when the user wants to bookmark or collect articles.
homepage: https://github.com/chliny/article-bookmarker-skill
metadata: {"openclaw": {"emoji":"🔖","requires":{"env":["ARTICLE_BOOKMARK_DIR"]}}}
---

# Article Bookmarker Skill

> **IMPORTANT**: Before any operation, read the environment variable `$ARTICLE_BOOKMARK_DIR` to determine the bookmark storage directory. All bookmark files and the tag index must be stored under this path. If the variable is not set, prompt the user to configure it.

## Quick Start

When the user provides a URL or article text to bookmark:

1. Read `$ARTICLE_BOOKMARK_DIR` to get the storage path
2. Use `web_fetch` to get the article content
3. Generate a concise summary using the current model
4. Auto-generate relevant tags based on content analysis
5. Create a markdown file with URL, content, summary, and tags (see [file-structure.md](references/file-structure.md) for format details)
6. Save to the bookmark directory with descriptive filename
7. Update the tag index file

For deletion requests: find the article, confirm details with user, then remove and update index.

## Workflow

### Adding Articles

```
1. Read $ARTICLE_BOOKMARK_DIR
2. Receive URL or text content
3. Extract/save content (web_fetch for URLs)
4. Generate summary (model-based)
5. Auto-tag (keyword/topic analysis)
6. Create bookmark file (markdown format)
7. Update tag index
```

### Deleting Articles

```
1. Read $ARTICLE_BOOKMARK_DIR
2. Identify target article (by filename, topic, or content)
3. Display article details for confirmation
4. Get user confirmation
5. Delete bookmark file
6. Update tag index
```

## Tag Management

### Auto-Tagging Logic

Generate tags by analyzing:
- Article domain/topic keywords
- Technical terms and concepts
- Content categories (tutorial, news, research, etc.)
- Named entities and proper nouns

Maintain consistent tag vocabulary to avoid duplicates (e.g., use "AI" not "artificial-intelligence").

### Tag Index Format

TAG_INDEX.md maintains bidirectional mapping (see [file-structure.md](references/file-structure.md) for full format):

```markdown
# Article Tag Index

## Tags

- **AI**: [article1](article1.md), [article2](article2.md)
- **Research**: [...]

## Articles by Tag Count

- 3 tags: [article1](article1.md)
- 1 tag: [...]
```

## Implementation Details

### Content Extraction

- Use `web_fetch` with `extractMode: "markdown"` for web articles
- Handle truncation gracefully (respect `maxChars` limits)
- Preserve original formatting where possible
- **GitHub Repository URLs**: When the URL is a GitHub repository (e.g., `https://github.com/user/repo`), prioritize fetching the README content from the repository's main page or from `README.md`, `readme.md`, or `README.rst` files in the root directory

### Proxy Configuration and Retry

When fetching article content from URLs fails:

1. **First Attempt**: Try fetching without proxy
2. **On Failure**: Load proxy configuration from environment variables:
   - `HTTP_PROXY` or `http_proxy`: HTTP proxy URL
   - `HTTPS_PROXY` or `https_proxy`: HTTPS proxy URL
   - `NO_PROXY` or `no_proxy`: Comma-separated list of hosts to bypass
3. **Retry**: Re-attempt fetching with proxy configuration
4. **Final Failure**: Notify user if both attempts fail

Example environment variables:
```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
export NO_PROXY="localhost,127.0.0.1,.example.com"
```

### Summary Generation

Generate 2-3 paragraph summaries that capture:
- Main thesis or argument
- Key insights or findings  
- Practical implications or applications

Keep summaries informative but concise (typically 150-300 words).

### File Naming

Create SEO-friendly filenames:
- Convert title to lowercase
- Replace spaces and special chars with hyphens
- Limit length to ~50 characters
- Ensure uniqueness by appending numbers if needed

### Safety Checks

- Validate URLs before fetching
- Confirm deletions with users (show path and key details)
- Maintain backup of index before modifications
- Handle concurrent access gracefully

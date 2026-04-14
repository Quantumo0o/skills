# Meta Output

Use this file when generating and saving the five meta fields.

---

## Field definitions and limits

### 1. title (display title)

The human-readable headline shown on the blog itself.

- Must be engaging and specific to the content
- Can be slightly clever or curiosity-driven since readers see this after clicking
- CRITICAL: must be different from the SEO title
- Length: 50-70 characters (hard limit: 70)

### 2. seo_title (search engine title tag)

What appears as the blue link text in Google results.

- Lead with the primary keyword, as close to the start as possible
- Be specific and match search intent
- No clickbait. No "You Won't Believe" style phrasing
- Must be different from the display title
- Length: 50-60 characters (hard limit: 60). Google truncates beyond this.

### 3. seo_description (meta description)

The grey text snippet shown under the title in Google results.

- Include the primary keyword once, naturally
- Summarize what the reader gets from the post clearly
- Write it as a call to read, not a teaser or hint
- Use active voice. Short sentences.
- Length: 140-160 characters (hard limit: 160). Google truncates beyond this.

### 4. seo_slug (URL slug)

The path segment used in the URL.

- Lowercase only
- Hyphens between words, no underscores
- Remove all stop words (a, the, and, of, in, for, to, is) unless removing them breaks meaning
- Contains the primary keyword
- As short as possible while still being descriptive
- Length: 3-6 words (hard limit: 8 words)

### 5. social_tips

2-4 short, specific tips for promoting this post on social media.
Based on what you found during research about how this topic performs on social.
Each tip is one sentence. Plain text, no bullet formatting in the JSON value (use an array).

---

## JSON schema

Save the file to `~/blog-meta/<seo_slug>.json` using this exact structure:

```json
{
  "blog_path": "~/blogs/<original-filename>.md",
  "title": "...",
  "seo_title": "...",
  "seo_description": "...",
  "seo_slug": "...",
  "primary_keyword": "...",
  "secondary_keyword": "...",
  "social_tips": [
    "...",
    "...",
    "..."
  ],
  "thumbnail_path": null
}
```

`thumbnail_path` is `null` when the JSON is first created by the blog-meta skill.
It is updated to the exact absolute image path by the blog-image skill after generation.

## Validation before saving

Check every field against these before writing the file:

- [ ] `title` is 50-70 characters
- [ ] `seo_title` is 50-60 characters
- [ ] `seo_description` is 140-160 characters
- [ ] `seo_slug` is lowercase, hyphenated, no stop words, 3-6 words
- [ ] `title` and `seo_title` are different from each other
- [ ] `seo_description` contains the primary keyword exactly once
- [ ] `social_tips` has 2-4 items, each one sentence
- [ ] `blog_path` is the correct absolute path to the source file
- [ ] `thumbnail_path` is set to `null` (it will be filled in by the blog-image skill later)

CRITICAL NON-NEGOTIABLE: do not save the file if any field fails validation. Fix it first.

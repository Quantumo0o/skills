---
name: book_highlights
description: Extract key highlights and quotes from books. Get the most important passages and insights from any book.
keywords:
  - book
  - highlights
  - quotes
  - key-ideas
  - insights
triggers:
  - "highlights from"
  - "key quotes from"
  - "best passages"
  - "important ideas from"
  - "highlights of"
---

# book-highlights

Extract key highlights and quotes from books.

## What it does

- Search books by title or author
- Extract 5-10 key highlights and quotes
- Return formatted highlights with context
- Show Heardly highlights if available
- Support multiple book sources

## When to use this skill

Use this skill when the user asks:
- "What are the highlights from Atomic Habits?"
- "Show me the best quotes from Deep Work"
- "Key ideas from Thinking, Fast and Slow"
- "Important passages from Principles"
- "Highlights of The Lean Startup"

## Installation

```bash
clawhub install book-highlights
```

## Usage

```javascript
const BookHighlightsSkill = require('book-highlights');
const skill = new BookHighlightsSkill();

// Get highlights (returns formatted text)
const result = await skill.getHighlights({
  query: 'Atomic Habits',
  limit: 10
});
console.log(result); // Directly readable text output
```

## Output

Formatted text with:
- Book title and author
- 5-10 key highlights/quotes
- Context for each highlight
- Heardly source attribution
- Ready to display to users

## Data Sources

1. **Heardly Database** (5904 books) — highlights field
2. **Extracted from summaries** — key passages

## License

MIT

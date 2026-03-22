---
name: amazon_books
description: Search books across all sources with summaries and Amazon purchase links. Triggered when user asks about finding, buying, or searching for books.
keywords:
  - book
  - search
  - amazon
  - purchase
  - summary
  - author
triggers:
  - "search for books"
  - "find books about"
  - "where can I buy"
  - "books by author"
  - "book recommendations"
  - "looking for a book"
---

# amazon-books

Search books across all sources with summaries and Amazon purchase links.

## What it does

- Search books by title, author, or keyword across multiple sources
- Return full book descriptions from Google Books API
- Provide direct Amazon purchase links
- Show Heardly summary if available
- Support multiple book sources (Heardly, Google Books, Open Library)
- Return user-friendly formatted text by default

## When to use this skill

Use this skill when the user asks:
- "Do you have books by Kevin Kelly?"
- "Where can I buy books about happiness?"
- "Search for books on machine learning"
- "Find me books by Elon Musk"
- "What books are available about AI?"

## Installation

```bash
clawhub install amazon-books
```

## Usage

```javascript
const AmazonBooksSkill = require('amazon-books');
const skill = new AmazonBooksSkill();

// Search books (returns formatted text)
const result = await skill.searchBooks({
  query: 'Kevin Kelly',
  limit: 5
});
console.log(result); // Directly readable text output
```

## Output

Formatted text with:
- Title, author, description
- Amazon purchase link
- Heardly summary (if available)
- Ready to display to users

## Data Sources

1. **Heardly Database** (5904 books) — fastest, local
2. **Google Books API** (free, millions of books)
3. **Open Library API** (free, open source)
4. **Amazon Search Links** (no API needed)

## License

MIT

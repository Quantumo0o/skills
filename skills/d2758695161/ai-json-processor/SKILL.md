# json-formatter

Format, validate, and transform JSON data. Paste JSON or point to a file.

## Usage

```
Format this JSON: [paste JSON]
Validate [file.json]
Convert [file.json] to CSV
Minify this JSON
Sort keys in [file.json]
```

## What it does

- **Pretty print** — indent with 2 or 4 spaces, colorized output
- **Validate** — check JSON syntax, report exact line/column of errors
- **Minify** — remove whitespace for production
- **Sort keys** — alphabetically sort all object keys
- **Query** — extract values using JSONPath (e.g., `$.store.book[*].author`)
- **Convert to CSV** — convert flat JSON arrays to CSV
- **Merge** — combine multiple JSON files

## Examples

- "Format this: `{"a":1,"b":2}`" → pretty-printed with 2-space indent
- "Validate config.json and report errors"
- "Convert users.json to CSV"
- "Extract all email addresses from data.json using `$.[*].email`"
- "Sort all keys in manifest.json"

## Notes

- Handles large files (up to 50MB)
- Auto-detects if input is already valid JSON
- For JSONPath, uses `jsonpath` library syntax
- Merge: arrays are concatenated, objects are deep-merged

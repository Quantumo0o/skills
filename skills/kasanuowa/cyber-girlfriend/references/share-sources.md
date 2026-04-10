# Share Sources

The companion feels more alive if she occasionally shares something she "noticed".

## Good Source Patterns

- X trending/explore
- RSS feeds
- blogs/newsletters
- Telegram channels
- GitHub releases or issue summaries

## Selection Rules

- Share rarely
- Treat sources as conversation hooks, not content dumps
- Prefer 1 topic over 5 links
- Let the model turn the source into character voice

## X Guidance

For a publishable skill, avoid requiring an X API integration or browser automation dependencies.

Prefer:
- a cache file (`x-hotspots.json`) refreshed by the agent's own web search tools
- letting cron job payloads handle the search and cache write
- keeping cache path, TTL, and max items configurable

Avoid:
- hardcoded handles
- mandatory API keys or browser dependencies
- assuming a single regional trend page is correct for every user

## Suggested Trigger

Only let `small_share` borrow a source topic when:
- pacing allows a proactive message
- the cache is fresh enough
- there is no higher-priority operational status to mention

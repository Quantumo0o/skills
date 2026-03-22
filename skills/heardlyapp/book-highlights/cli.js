#!/usr/bin/env node

/**
 * CLI entry point for book-highlights skill
 * Allows direct invocation: node cli.js "Atomic Habits"
 */

const BookHighlightsSkill = require('./index.js');

async function main() {
  const query = process.argv[2];
  const limit = parseInt(process.argv[3]) || 10;

  if (!query) {
    console.error('Usage: node cli.js "<query>" [limit]');
    console.error('Example: node cli.js "Atomic Habits" 10');
    process.exit(1);
  }

  const skill = new BookHighlightsSkill();
  const result = await skill.getHighlights({ query, limit });
  console.log(result);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});

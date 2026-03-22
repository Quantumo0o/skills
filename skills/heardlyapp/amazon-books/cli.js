#!/usr/bin/env node

/**
 * CLI entry point for amazon-books skill
 * Allows direct invocation: node cli.js "Kevin Kelly"
 */

const AmazonBooksSkill = require('./index.js');

async function main() {
  const query = process.argv[2];
  const limit = parseInt(process.argv[3]) || 5;

  if (!query) {
    console.error('Usage: node cli.js "<query>" [limit]');
    console.error('Example: node cli.js "Kevin Kelly" 5');
    process.exit(1);
  }

  const skill = new AmazonBooksSkill();
  const result = await skill.searchBooks({ query, limit });
  console.log(result);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});

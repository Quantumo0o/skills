#!/usr/bin/env node
/**
 * Knitify API wrapper script for OpenClaw skill tools.
 * Reads KNITIFY_API_KEY and KNITIFY_API_URL from process.env
 * (set via skills.entries.knitify-research.env in openclaw.json).
 *
 * Usage: node knitify-api.js <action> [--param value ...]
 * Actions: signup, research, product
 */

const API_KEY = process.env.KNITIFY_API_KEY;
const API_URL = process.env.KNITIFY_API_URL || 'https://knitify.innovohealthlabs.com';

function parseArgs(argv) {
  const args = {};
  const action = argv[2];
  for (let i = 3; i < argv.length; i += 2) {
    const key = argv[i]?.replace(/^--/, '');
    const val = argv[i + 1];
    if (key && val !== undefined) args[key] = val;
  }
  return { action, args };
}

async function signup(email) {
  const res = await fetch(`${API_URL}/api/public/v1/openclaw/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  return res.json();
}

async function research(query, tone = 'general') {
  if (!API_KEY) {
    return { error: 'KNITIFY_API_KEY not set. Sign up first or set your API key.' };
  }
  const res = await fetch(`${API_URL}/api/public/v1/research/chat-stream`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      research_instruction: query,
      quality_tier: 'fast',
      content_tone: tone,
      target_word_count: 500,
    }),
  });
  // chat-stream returns SSE — collect all text events
  const text = await res.text();
  const lines = text.split('\n');
  let result = '';
  let references = [];
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      try {
        const data = JSON.parse(line.slice(6));
        if (data.text) result += data.text;
        if (data.references) references = data.references;
        if (data.assistant_message) result = data.assistant_message;
        if (data.credits_used !== undefined) {
          return { text: result, references, credits_used: data.credits_used };
        }
      } catch {}
    }
  }
  return { text: result, references };
}

async function productResearch(productUrl, question) {
  if (!API_KEY) {
    return { error: 'KNITIFY_API_KEY not set. Sign up first or set your API key.' };
  }
  const res = await fetch(`${API_URL}/api/public/v1/research/product-research-chat-stream`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_link: productUrl,
      research_instruction: question,
      mode: 'research',
      quality_tier: 'fast',
      content_tone: 'commercial',
    }),
  });
  const text = await res.text();
  const lines = text.split('\n');
  let result = '';
  let references = [];
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      try {
        const data = JSON.parse(line.slice(6));
        if (data.text) result += data.text;
        if (data.references) references = data.references;
        if (data.assistant_message) result = data.assistant_message;
        if (data.credits_used !== undefined) {
          return { text: result, references, credits_used: data.credits_used };
        }
      } catch {}
    }
  }
  return { text: result, references };
}

async function main() {
  const { action, args } = parseArgs(process.argv);

  let result;
  switch (action) {
    case 'signup':
      result = await signup(args.email);
      break;
    case 'research':
      result = await research(args.query, args.tone);
      break;
    case 'product':
      result = await productResearch(args.product_url, args.question);
      break;
    default:
      result = { error: `Unknown action: ${action}` };
  }

  process.stdout.write(JSON.stringify(result, null, 2));
}

main().catch(err => {
  process.stdout.write(JSON.stringify({ error: err.message }));
  process.exit(1);
});

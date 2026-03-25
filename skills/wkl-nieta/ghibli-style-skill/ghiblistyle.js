#!/usr/bin/env node
import { readFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";

// --- Argument parsing ---
const args = process.argv.slice(2);
let prompt = null;
let size = "landscape";
let token = null;
let ref = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) { size = args[++i]; }
  else if (args[i] === "--token" && args[i + 1]) { token = args[++i]; }
  else if (args[i] === "--ref" && args[i + 1]) { ref = args[++i]; }
  else if (!args[i].startsWith("--") && prompt === null) { prompt = args[i]; }
}

if (!prompt) {
  prompt = "Studio Ghibli style illustration, soft watercolor painting, dreamy Miyazaki aesthetic, lush natural backgrounds, warm golden light, hand-painted textures, whimsical atmosphere, detailed foliage, cinematic composition";
}

// --- Token resolution ---
function readEnvFile(filePath) {
  try {
    const resolved = filePath.replace(/^~/, homedir());
    const content = readFileSync(resolved, "utf8");
    const match = content.match(/NETA_TOKEN=(.+)/);
    return match ? match[1].trim() : null;
  } catch {
    return null;
  }
}

if (!token) token = process.env.NETA_TOKEN || null;
if (!token) token = readEnvFile("~/.openclaw/workspace/.env");
if (!token) token = readEnvFile("~/developer/clawhouse/.env");

if (!token) {
  console.error('\n✗ NETA_TOKEN not found.');
  console.error('  Global: sign up at https://www.neta.art/ → get token at https://www.neta.art/open/');
  console.error('  China:  sign up at https://app.nieta.art/ → get token at https://app.nieta.art/security');
  console.error('  Then:   export NETA_TOKEN=your_token_here');
  process.exit(1);
}

// --- Size map ---
const sizeMap = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = sizeMap[size] ?? sizeMap.landscape;

// --- Headers ---
const HEADERS = {
  "x-token": token,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

// --- Build request body ---
const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width,
  height,
  meta: { entrance: "PICTURE,CLI" },
  context_model_series: "8_image_edit",
};

if (ref) {
  body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
}

// --- Submit job ---
const submitRes = await fetch(`${process.env.NETA_API_URL || 'https://api.talesofai.cn'}/v3/make_image`, {
  method: "POST",
  headers: HEADERS,
  body: JSON.stringify(body),
});

if (!submitRes.ok) {
  if (submitRes.status === 401 || submitRes.status === 403) {
    console.error('\n✗ Authentication failed (' + submitRes.status + ') — your NETA_TOKEN is missing or invalid.');
    console.error('  Global: https://www.neta.art/open/');
    console.error('  China:  https://app.nieta.art/security');
  } else {
    console.error('Error submitting job: ' + submitRes.status + ' ' + submitRes.statusText);
  }
  process.exit(1);
}

const submitData = await submitRes.json();
const task_uuid = typeof submitData === "string" ? submitData : submitData.task_uuid;

if (!task_uuid) {
  console.error("Error: no task_uuid in response", submitData);
  process.exit(1);
}

// --- Poll for result ---
const MAX_ATTEMPTS = 90;
const POLL_INTERVAL_MS = 2000;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
  await sleep(POLL_INTERVAL_MS);

  const pollRes = await fetch(`${process.env.NETA_API_URL || 'https://api.talesofai.cn'}/v1/artifact/task/${task_uuid}`, {
    headers: HEADERS,
  });

  if (!pollRes.ok) {
    console.error(`Poll error: ${pollRes.status} ${pollRes.statusText}`);
    process.exit(1);
  }

  const pollData = await pollRes.json();
  const status = pollData.task_status;

  if (['PENDING', 'MODERATION'].includes(status)) { continue; }
  if (['FAILURE', 'TIMEOUT', 'DELETED', 'ILLEGAL_IMAGE'].includes(status)) {
    console.error('Error: generation failed with status ' + status + (pollData.err_msg ? ' — ' + pollData.err_msg : ''));
    process.exit(1);
  }

  // Done — extract image URL
  const url =
    pollData.artifacts?.[0]?.url ??
    pollData.result_image_url ??
    null;

  if (!url) {
    console.error("Error: task finished but no image URL found", pollData);
    process.exit(1);
  }

  console.log(url);
  process.exit(0);
}

console.error("Error: timed out waiting for image generation");
process.exit(1);

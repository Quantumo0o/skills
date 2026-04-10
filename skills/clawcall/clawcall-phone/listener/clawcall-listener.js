#!/usr/bin/env node
/**
 * ClawCall Listener
 * Polls ClawCall for inbound call messages and routes them through
 * the local agent, then returns the reply to the caller.
 *
 * Usage:
 *   node clawcall-listener.js
 *
 * Requires:
 *   CLAWCALL_API_KEY environment variable set
 *
 * Agent mode (pick one):
 *   CLAWCALL_AGENT_URL=http://localhost:5000
 *       POST {CLAWCALL_AGENT_URL}/clawcall/message
 *       Body:    { "call_sid": "...", "message": "..." }
 *       Returns: { "response": "...", "end_call": false }
 *
 *   (default) OpenClaw CLI:
 *       openclaw agent --session-id <call_sid> --message <msg> --json
 *
 * Security note:
 *   child_process.spawnSync is used ONLY to invoke the local OpenClaw
 *   CLI ("openclaw agent ..."). No other shell commands are executed.
 *   The full argument list is built from controlled variables — no
 *   string interpolation into a shell. Set CLAWCALL_AGENT_URL to use
 *   HTTP mode instead and avoid child_process entirely.
 */

"use strict";

const { spawnSync } = require("child_process");
const { URL } = require("url");

const API_KEY    = process.env.CLAWCALL_API_KEY;
const BASE_URL   = (process.env.CLAWCALL_BASE_URL || "https://api.clawcall.online").replace(/\/$/, "");
const AGENT_URL  = (process.env.CLAWCALL_AGENT_URL || "").replace(/\/$/, ""); // e.g. http://localhost:5000

if (!API_KEY) {
  console.error("[ClawCall] ERROR: CLAWCALL_API_KEY is not set.");
  console.error("[ClawCall] Run:  setx CLAWCALL_API_KEY your-api-key  (Windows)");
  console.error("[ClawCall] or:   export CLAWCALL_API_KEY=your-api-key  (Mac/Linux)");
  process.exit(1);
}

const _parsed   = new URL(BASE_URL);
const _isHttps  = _parsed.protocol === "https:";
const _httpLib  = _isHttps ? require("https") : require("http");
const _hostname = _parsed.hostname;
const _port     = _parsed.port ? parseInt(_parsed.port) : (_isHttps ? 443 : 80);

console.log(`[ClawCall] Connecting to ${BASE_URL}`);
if (AGENT_URL) {
  console.log(`[ClawCall] Agent mode: HTTP webhook → ${AGENT_URL}/clawcall/message`);
} else {
  console.log("[ClawCall] Agent mode: openclaw CLI");
}

// ── HTTP helper (ClawCall API) ────────────────────────────────────────────────

function request(method, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req  = _httpLib.request(
      {
        hostname: _hostname,
        port:     _port,
        path,
        method,
        headers: {
          Authorization:   `Bearer ${API_KEY}`,
          "Content-Type":  "application/json",
          ...(data ? { "Content-Length": Buffer.byteLength(data) } : {}),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => (raw += chunk));
        res.on("end", () => {
          try { resolve(JSON.parse(raw)); }
          catch { resolve({ ok: false, raw }); }
        });
      }
    );
    req.on("error", reject);
    req.setTimeout(25_000, () => req.destroy(new Error("HTTP timeout")));
    if (data) req.write(data);
    req.end();
  });
}

// ── HTTP helper (local agent webhook) ────────────────────────────────────────

function postToAgent(agentUrl, callSid, message) {
  return new Promise((resolve, reject) => {
    const parsed  = new URL(agentUrl);
    const isHttps = parsed.protocol === "https:";
    const lib     = isHttps ? require("https") : require("http");
    const body    = JSON.stringify({ call_sid: callSid, message });

    const req = lib.request(
      {
        hostname: parsed.hostname,
        port:     parsed.port ? parseInt(parsed.port) : (isHttps ? 443 : 80),
        path:     parsed.pathname.replace(/\/$/, "") + "/clawcall/message",
        method:   "POST",
        headers: {
          "Content-Type":   "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (c) => (raw += c));
        res.on("end", () => {
          try { resolve(JSON.parse(raw)); }
          catch { resolve({ response: raw, end_call: false }); }
        });
      }
    );
    req.on("error", reject);
    req.setTimeout(50_000, () => req.destroy(new Error("Agent HTTP timeout")));
    req.write(body);
    req.end();
  });
}

// ── Agent turn ────────────────────────────────────────────────────────────────

async function runAgentTurn(message, callSid) {
  // ── Mode 1: HTTP webhook agent (CLAWCALL_AGENT_URL set) ──────────────────
  if (AGENT_URL) {
    try {
      const data = await postToAgent(AGENT_URL, callSid, message);
      const reply = (data.response || data.reply || data.text || "").trim();
      if (reply) return { reply, end_call: !!data.end_call };
      console.error("[ClawCall] Agent returned empty response:", data);
      return { reply: "I had a little trouble with that — could you repeat it?", end_call: false };
    } catch (err) {
      console.error("[ClawCall] Agent webhook error:", err.message);
      return { reply: "I had a little trouble with that — could you repeat it?", end_call: false };
    }
  }

  // ── Mode 2: OpenClaw CLI ──────────────────────────────────────────────────
  let raw = "";
  try {
    const [bin, args] = process.platform === "win32"
      ? ["cmd.exe", ["/c", "openclaw", "agent", "--session-id", callSid, "--message", message, "--json"]]
      : ["openclaw", ["agent", "--session-id", callSid, "--message", message, "--json"]];
    const result = spawnSync(bin, args,
      { timeout: 55_000, encoding: "utf8", stdio: ["pipe", "pipe", "pipe"] }
    );
    if (result.error) throw result.error;
    if (result.status !== 0) {
      const err = new Error(`openclaw exited ${result.status}`);
      err.stdout = result.stdout || "";
      throw err;
    }
    raw = (result.stdout || "").trim();
  } catch (err) {
    raw = (err.stdout || "").trim();
    if (!raw) {
      console.error("[ClawCall] openclaw error:", err.message);
      return { reply: "I had a little trouble with that — could you repeat it?", end_call: false };
    }
  }

  // Parse JSON output from openclaw --json
  const lines = raw.split("\n").filter(Boolean).reverse();
  for (const line of lines) {
    try {
      const parsed = JSON.parse(line);
      const fromPayloads = Array.isArray(parsed.payloads) && parsed.payloads[0] && parsed.payloads[0].text;
      let contentText = parsed.content;
      if (Array.isArray(contentText)) {
        const item = contentText.find((c) => c && c.type === "text" && c.text);
        contentText = item ? item.text : null;
      }
      const reply = fromPayloads
        || parsed.result
        || parsed.reply
        || parsed.text
        || parsed.message
        || contentText;
      if (reply && typeof reply === "string" && reply.trim())
        return { reply: reply.trim(), end_call: false };
    } catch { /* not JSON */ }
  }

  const trimmed = raw.trim();
  if (trimmed && !trimmed.startsWith("{") && !trimmed.startsWith("["))
    return { reply: trimmed, end_call: false };

  return { reply: "I'm here — could you say that again?", end_call: false };
}

// ── Main loop ─────────────────────────────────────────────────────────────────

async function main() {
  console.log("[ClawCall] Listener started. Waiting for calls...");

  while (true) {
    try {
      const res = await request("GET", "/api/v1/calls/listen?timeout=15");

      if (res.ok && res.timeout) continue;

      if (!res.ok || !res.call_sid) {
        console.error("[ClawCall] Unexpected response:", res);
        await sleep(3_000);
        continue;
      }

      const { call_sid, message } = res;
      console.log(`[ClawCall] ↓ call_sid=${call_sid}  message="${message}"`);

      const { reply, end_call } = await runAgentTurn(message, call_sid);
      console.log(`[ClawCall] ↑ reply="${reply}"  end_call=${end_call}`);

      const postRes = await request("POST", `/api/v1/calls/respond/${call_sid}`, {
        response: reply,
        end_call,
      });
      if (!postRes.ok) console.error("[ClawCall] Respond error:", postRes);

    } catch (err) {
      console.error("[ClawCall] Loop error:", err.message);
      await sleep(3_000);
    }
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

main();

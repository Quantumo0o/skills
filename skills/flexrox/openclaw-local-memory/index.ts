import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { LocalMemoryStore } from "./lib/store.js";
import { buildCaptureHandler, buildRecallHandler } from "./lib/hooks.js";
import { registerSearchTool, registerStoreTool, registerForgetTool, registerWipeTool, registerListTool } from "./lib/tools.js";

// ─── Config Schema ───────────────────────────────────────────────────────────

const ConfigSchema = {
  type: "object",
  additionalProperties: false,
  properties: {
    containerTag: { type: "string", default: "openclaw_local_memory" },
    autoRecall: { type: "boolean", default: true },
    autoCapture: { type: "boolean", default: true },
    maxRecallResults: { type: "number", default: 10 },
    similarityThreshold: { type: "number", default: 0.1 },
    debug: { type: "boolean", default: false },
  },
};

type LocalMemoryConfig = {
  containerTag?: string;
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
};

// ─── Plugin ──────────────────────────────────────────────────────────────────

export default definePluginEntry({
  id: "openclaw-local-memory",
  name: "Local Memory",
  description: "Local vector memory for OpenClaw — stores, searches and injects memories using a local vector DB",
  kind: "memory",
  configSchema: ConfigSchema,

  register(api) {
    const raw = api.pluginConfig;
    const cfg: LocalMemoryConfig = raw && typeof raw === "object" && !Array.isArray(raw)
      ? (raw as Record<string, unknown>)
      : {};

    const log = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => {
      if (cfg.debug || level !== "debug") {
        api.logger[level === "info" ? "info" : level === "warn" ? "warn" : "info"](
          `[local-memory] ${msg}`,
          data ?? {}
        );
      }
    };

    // ── Init store ──────────────────────────────────────────────────────────
    const store = new LocalMemoryStore({
      containerTag: cfg.containerTag ?? "openclaw_local_memory",
      debug: cfg.debug ?? false,
    });

    log("info", "initialized", {
      container: store.containerTag,
      backend: "tfidf",
    });

    // ── Tools ────────────────────────────────────────────────────────────────
    registerSearchTool(api, store, cfg, log);
    registerStoreTool(api, store, cfg, log);
    registerForgetTool(api, store, cfg, log);
    registerWipeTool(api, store, log);
    registerListTool(api, store, log);

    // ── Memory Prompt Section ─────────────────────────────────────────────────
    api.registerMemoryPromptSection(({ agentId, sessionKey }) => {
      // Will be filled by recall handler
      return "";
    });

    // ── Hooks ────────────────────────────────────────────────────────────────
    // Track turn index per session for ordering conversation exchanges
    const turnIndexBySession = new Map<string, number>();

    // Build handlers up front so they can share state
    const captureHandler = buildCaptureHandler(store, cfg, log);
    const recallHandler = cfg.autoRecall ? buildRecallHandler(store, cfg, log) : null;

    api.on("before_agent_start", (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
      const sessionKey = ctx.sessionKey as string | undefined;
      if (sessionKey) {
        const idx = turnIndexBySession.get(sessionKey) ?? 0;
        turnIndexBySession.set(sessionKey, idx + 1);
        // Always register user message so autoCapture can pair it with the response
        const userPrompt = extractUserPrompt(event);
        if (userPrompt) {
          captureHandler.registerUserMessage(userPrompt, sessionKey, idx);
        }
      }
      if (recallHandler) return recallHandler(event, ctx);
    });

    if (cfg.autoCapture) {
      api.on("agent_end", (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
        const sessionKey = ctx.sessionKey as string | undefined;
        return captureHandler.handle(event, ctx, sessionKey);
      });
    }

    api.registerService({
      id: "openclaw-local-memory",
      start: () => { log("info", "service started"); },
      stop: () => { log("info", "service stopped"); },
    });
  },
});

// ─── Helpers ─────────────────────────────────────────────────────────────────

function extractUserPrompt(event: Record<string, unknown>): string {
  if (typeof event.prompt === "string") return event.prompt;
  if (Array.isArray(event.messages)) {
    for (const msg of event.messages as Record<string, unknown>[]) {
      if (msg.role === "user") {
        const content = msg.content;
        if (typeof content === "string") return content;
        if (Array.isArray(content)) {
          return content
            .map((c) => (typeof c === "string" ? c : (c as Record<string, unknown>).text ?? ""))
            .join(" ");
        }
      }
    }
  }
  return "";
}

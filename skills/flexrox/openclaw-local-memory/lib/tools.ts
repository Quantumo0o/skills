import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-runtime.js";
import type { LocalMemoryStore } from "./store.js";

interface LocalMemoryConfig {
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
}

type LogFn = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => void;

// ─── Search Tool ─────────────────────────────────────────────────────────────

export function registerSearchTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_search",
    description: "Search through long-term memories using semantic vector search",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "What to search for" },
        limit: { type: "number", description: "Max results (default 10)" },
        threshold: { type: "number", description: "Min similarity 0-1 (default 0.1)" },
      },
      required: ["query"],
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? cfg.maxRecallResults ?? 10;
        const threshold = params.threshold ?? cfg.similarityThreshold ?? 0.1;
        const results = await store.search(params.query, limit, threshold);

        if (results.length === 0) {
          return { content: [{ type: "text", text: "No memories found matching that query." }] };
        }

        const lines = results.map((r) => {
          const cat = r.metadata?.category ?? "other";
          const sim = Math.round(r.similarity * 100);
          return `[${cat}·${sim}%] ${r.content}`;
        });

        return {
          content: [{ type: "text", text: `Found ${results.length} memory:\n\n${lines.join("\n\n")}` }],
        };
      } catch (err) {
        log("warn", "search tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Search failed: ${String(err)}` }] };
      }
    },
  });
}

// ─── Store Tool ────────────────────────────────────────────────────────────────

export function registerStoreTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_store",
    description: "Store a piece of information in long-term memory",
    parameters: {
      type: "object",
      properties: {
        content: { type: "string", description: "What to remember" },
        category: {
          type: "string",
          description: "Category: preference, fact, decision, entity, or other",
        },
      },
      required: ["content"],
    },
    async execute(_id, params) {
      try {
        const id = await store.add(params.content, {
          category: (params.category as "preference" | "fact" | "decision" | "entity" | "other") ?? undefined,
          source: "user",
        });
        log("info", "memory stored via tool", { id });
        return { content: [{ type: "text", text: `Stored in memory (id: ${id.slice(0, 8)})` }] };
      } catch (err) {
        log("warn", "store tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to store: ${String(err)}` }] };
      }
    },
  });
}

// ─── List Tool ───────────────────────────────────────────────────────────────

export function registerListTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  _cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_list",
    description: "List all memories sorted by date (newest first). For browsing and the web UI.",
    parameters: {
      type: "object",
      properties: {
        limit: { type: "number", description: "Max memories to return (default 100)" },
      },
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? 100;
        const memories = await store.listAll(limit);

        if (memories.length === 0) {
          return { content: [{ type: "text", text: "No memories stored yet." }] };
        }

        const lines = memories.map((m) => {
          const cat = m.metadata?.category ?? "other";
          const date = new Date(m.metadata?.createdAt ?? Date.now()).toLocaleString("de-DE");
          const cut = m.content.length > 200 ? m.content.slice(0, 200) + "…" : m.content;
          return `[${cat}] ${date}\n${cut}`;
        });

        return {
          content: [{ type: "text", text: lines.join("\n\n---\n\n") }],
        };
      } catch (err) {
        log("warn", "list tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to list memories: ${String(err)}` }] };
      }
    },
  });
}

// ─── Forget Tool ──────────────────────────────────────────────────────────────

export function registerForgetTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  _cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_forget",
    description: "Remove a specific memory by query. Finds and deletes the most relevant match.",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "Query describing what to forget" },
      },
      required: ["query"],
    },
    async execute(_id, params) {
      try {
        const result = await store.forgetByQuery(params.query, 1);
        return { content: [{ type: "text", text: result.message }] };
      } catch (err) {
        log("warn", "forget tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to forget: ${String(err)}` }] };
      }
    },
  });
}

// ─── Wipe Tool ───────────────────────────────────────────────────────────────

export function registerWipeTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_wipe",
    description: "DELETE all memories. Use with caution — this cannot be undone.",
    parameters: { type: "object", properties: {} },
    async execute(_id, _params) {
      try {
        const result = await store.wipeAll();
        log("info", "all memories wiped", { count: result.deletedCount });
        return {
          content: [{ type: "text", text: `Deleted ${result.deletedCount} memories permanently.` }],
        };
      } catch (err) {
        log("warn", "wipe tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to wipe: ${String(err)}` }] };
      }
    },
  });
}

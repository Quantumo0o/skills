import type { LocalMemoryStore } from "./store.js";

interface LocalMemoryConfig {
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
}

type LogFn = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => void;

// ─── Capture Handler ─────────────────────────────────────────────────────────

export function buildCaptureHandler(
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  // Track pending user messages per session (keyed by sessionKey)
  // We store user content here, then pair with assistant response at agent_end
  const pendingUserMessages = new Map<string, { content: string; turnIndex: number }>();

  return {
    /**
     * Call this from before_agent_start to register a user message
     * before the assistant responds.
     */
    async registerUserMessage(
      userContent: string,
      sessionKey: string,
      turnIndex: number,
    ) {
      if (userContent.length < 20) return;
      if (userContent.startsWith("[") && userContent.includes("agent_end")) return;
      if (userContent.split(" ").length < 4) return;
      pendingUserMessages.set(sessionKey, { content: userContent, turnIndex });
    },

    /**
     * Main handler called at agent_end — pairs stored user message
     * with the assistant's response and stores as one exchange entry.
     */
    async handle(
      event: Record<string, unknown>,
      ctx: Record<string, unknown>,
      sessionKey?: string,
    ) {
      try {
        if (!sessionKey) return;

        // Extract assistant response from event.messages (last assistant message)
        const assistantContent = extractAssistantResponse(event);
        if (!assistantContent || assistantContent.length < 5) {
          log("debug", "no assistant response to capture");
          return;
        }

        // Retrieve and clear pending user message for this session
        const pending = pendingUserMessages.get(sessionKey);
        pendingUserMessages.delete(sessionKey);

        // Build the full exchange text
        const userContent = pending?.content ?? "";
        const turnIndex = pending?.turnIndex ?? 0;

        // Format: full conversation turn as one memory entry
        const exchangeText = buildExchangeText(userContent, assistantContent);

        const id = await store.add(exchangeText, {
          sessionKey,
          conversationId: sessionKey,
          turnIndex,
          messageType: "exchange",
          source: "assistant",
          category: detectCategory(exchangeText),
          createdAt: new Date().toISOString(),
        });

        log("debug", "exchange captured", {
          id,
          turnIndex,
          userLength: userContent.length,
          assistantLength: assistantContent.length,
        });
      } catch (err) {
        log("warn", "capture failed", { error: String(err) });
      }
    },
  };
}

// ─── Recall Handler ──────────────────────────────────────────────────────────

export function buildRecallHandler(
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  return async (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
    try {
      // Extract the user prompt from the event
      const prompt = extractPrompt(event);
      if (!prompt || prompt.length < 5) return;

      const limit = cfg.maxRecallResults ?? 10;
      const threshold = cfg.similarityThreshold ?? 0.7;

      const results = await store.search(prompt, limit, threshold);

      if (results.length === 0) return;

      const memorySection = buildMemorySection(results);

      // Inject into event.prependContext if available, or store for prompt section builder
      if (Array.isArray(event.prependContext)) {
        event.prependContext.push(memorySection);
      }

      // Store results in context for the memory prompt section
      if (ctx && typeof ctx === "object") {
        (ctx as Record<string, unknown>).__localMemoryResults = results;
      }

      log("debug", "recalled memories", { count: results.length });
    } catch (err) {
      log("warn", "recall failed", { error: String(err) });
    }
  };
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function extractMessages(event: Record<string, unknown>): (string | Record<string, unknown>)[] {
  if (Array.isArray(event.messages)) {
    return event.messages as (string | Record<string, unknown>)[];
  }
  if (Array.isArray(event.content)) {
    return event.content as (string | Record<string, unknown>)[];
  }
  return [];
}

function extractPrompt(event: Record<string, unknown>): string {
  if (typeof event.prompt === "string") return event.prompt;
  if (typeof event.messages === "string") return event.messages;

  // Try to extract from messages array
  if (Array.isArray(event.messages)) {
    for (const msg of event.messages as Record<string, unknown>[]) {
      if (msg.role === "user" || msg.role === "user") {
        const content = msg.content;
        if (typeof content === "string") return content;
        if (Array.isArray(content)) {
          return content.map((c) => typeof c === "string" ? c : (c as Record<string, unknown>).text ?? "").join(" ");
        }
      }
    }
  }
  return "";
}

function buildMemorySection(results: import("./store.js").SearchResult[]): string {
  if (results.length === 0) return "";

  const lines = ["\n--- Relevant Memories ---"];
  for (const r of results) {
    const cat = r.metadata.category ?? "other";
    const sim = Math.round(r.similarity * 100);
    lines.push(`[${cat}·${sim}%] ${r.content}`);
  }
  lines.push("--- End Memories ---\n");
  return lines.join("\n");
}

function detectCategory(text: string): "preference" | "fact" | "decision" | "entity" | "other" {
  const lower = text.toLowerCase();
  if (/prefer|like|love|hate|want|i (always|never)\b/i.test(lower)) return "preference";
  if (/decided|will use|going with|chose/i.test(lower)) return "decision";
  if (/\+\d{10,}|@[\w.-]+\.\w+/i.test(lower)) return "entity";
  if (/is |are |has |have /i.test(lower)) return "fact";
  return "other";
}

/**
 * Extract the last assistant response from an agent_end event.
 */
function extractAssistantResponse(event: Record<string, unknown>): string {
  if (Array.isArray(event.messages)) {
    const msgs = event.messages as Record<string, unknown>[];
    // Walk backwards to find the last assistant message
    for (let i = msgs.length - 1; i >= 0; i--) {
      const msg = msgs[i];
      if (msg.role === "assistant") {
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
  // Fallback: try event.response
  if (typeof event.response === "string") return event.response;
  return "";
}

/**
 * Build a formatted exchange string from user and assistant content.
 */
function buildExchangeText(userContent: string, assistantContent: string): string {
  const userTrimmed = userContent.trim();
  const assistantTrimmed = assistantContent.trim();

  if (!userTrimmed) {
    return `Assistant: ${assistantTrimmed}`;
  }
  return `User: ${userTrimmed}\n\nAssistant: ${assistantTrimmed}`;
}

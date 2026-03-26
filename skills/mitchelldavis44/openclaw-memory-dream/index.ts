import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import { homedir } from "os";
import { join } from "path";
import { loadState, incrementSession, saveState } from "./src/state.js";
import { isLocked } from "./src/lock.js";
import { shouldTrigger, hoursUntilNextTrigger, mergeConfig } from "./src/scheduler.js";
import { consolidate } from "./src/consolidate.js";

/** Stable per-agent state dir derived from agentId or a fallback */
function resolveStateDir(agentId?: string): string {
  const id = agentId ?? "main";
  return join(homedir(), ".openclaw", "memory-dream", id);
}

export default definePluginEntry({
  id: "memory-dream",
  name: "Memory Dream",
  description:
    "Auto-consolidates agent memory files after sessions — like REM sleep for AI agents",

  register(api: OpenClawPluginApi) {
    const pluginCfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
    const cfg = mergeConfig(pluginCfg);

    // ── Hook: after each session ends ──────────────────────────────────────
    api.on("session_end", async (_event, ctx) => {
      if (!cfg.enabled) return;

      const stateDir = resolveStateDir(ctx.agentId);

      try {
        const state = await incrementSession(stateDir);
        api.logger.info(
          `[memory-dream] Session ended. Sessions since last consolidation: ${state.sessionCount}`
        );

        const trigger = await shouldTrigger(state, cfg, stateDir);
        if (trigger) {
          api.logger.info(
            "[memory-dream] Trigger conditions met — starting background consolidation"
          );

          // Resolve workspace dir using the agent's config + id
          const workspaceDir = api.runtime.agent.resolveAgentWorkspaceDir(
            api.config,
            ctx.agentId ?? "main"
          );

          // Fire and forget — intentionally not awaited
          consolidate(stateDir, workspaceDir, cfg, api, ctx.agentId ?? "main").catch((err: unknown) => {
            api.logger.error(
              `[memory-dream] Background consolidation error: ${String(err)}`
            );
          });
        }
      } catch (err) {
        api.logger.error(`[memory-dream] session_end hook error: ${String(err)}`);
      }
    });

    // ── Hook: before each session starts ──────────────────────────────────
    api.on("before_agent_start", async (_event, ctx) => {
      const stateDir = resolveStateDir((ctx as { agentId?: string }).agentId);

      try {
        const state = await loadState(stateDir);

        if (state.lastRunStatus === "success" && state.lastRunSummary) {
          const lastRun = state.lastRunAt
            ? new Date(state.lastRunAt).toLocaleString()
            : "unknown";
          api.logger.info(
            `[memory-dream] Memory consolidated at ${lastRun}: ${state.lastRunSummary}`
          );
        } else if (state.lastRunStatus === "running") {
          const locked = await isLocked(stateDir);
          if (!locked) {
            api.logger.warn(
              "[memory-dream] Last consolidation may have been interrupted (status=running, no lock)"
            );
            await saveState(stateDir, { ...state, lastRunStatus: "failed" });
          }
        }
      } catch {
        // Non-fatal — don't block agent start
      }
    });

    // ── Tool: memory_dream_status ──────────────────────────────────────────
    api.registerTool((ctx) => ({
      name: "memory_dream_status",
      label: "Memory Dream Status",
      description:
        "Returns the current memory-dream plugin state: session count since last consolidation, time since last run, next trigger estimate, and whether consolidation is currently running.",
      parameters: {
        type: "object" as const,
        properties: {},
        additionalProperties: false,
      } as const,
      async execute(_toolCallId, _params) {
        const stateDir = resolveStateDir(ctx.agentId);
        const state = await loadState(stateDir);
        const locked = await isLocked(stateDir);
        const hoursLeft = hoursUntilNextTrigger(state, cfg);

        const lastRunAt = state.lastRunAt
          ? new Date(state.lastRunAt).toLocaleString()
          : "never";

        const hoursSinceRun = state.lastRunAt
          ? (
              (Date.now() - new Date(state.lastRunAt).getTime()) /
              (1000 * 60 * 60)
            ).toFixed(1)
          : null;

        const sessionsNeeded = Math.max(0, cfg.minSessions - state.sessionCount);

        let nextTrigger: string;
        if (!cfg.enabled) {
          nextTrigger = "disabled";
        } else if (locked) {
          nextTrigger = "running now";
        } else if (sessionsNeeded > 0) {
          nextTrigger = `${sessionsNeeded} more session(s) needed`;
        } else if (hoursLeft !== null && hoursLeft > 0) {
          nextTrigger = `in ~${hoursLeft.toFixed(1)}h (time condition not met)`;
        } else {
          nextTrigger = "ready (will trigger on next session end)";
        }

        const details = {
          sessionCount: state.sessionCount,
          minSessions: cfg.minSessions,
          lastRunAt,
          hoursSinceLastRun: hoursSinceRun ? `${hoursSinceRun}h` : null,
          minHours: cfg.minHours,
          lastRunStatus: state.lastRunStatus,
          lastRunSummary: state.lastRunSummary,
          consolidationRunning: locked,
          nextTrigger,
          memoryFiles: cfg.memoryFiles,
          enabled: cfg.enabled,
        };

        return {
          content: [{ type: "text" as const, text: JSON.stringify(details, null, 2) }],
          details,
        };
      },
    }));
  },
});

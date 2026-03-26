import { DreamState } from "./state.js";
import { isLocked } from "./lock.js";

export interface DreamConfig {
  minSessions: number;
  minHours: number;
  memoryFiles: string[];
  model?: string;
  enabled: boolean;
}

export const defaultConfig: DreamConfig = {
  minSessions: 5,
  minHours: 24,
  memoryFiles: ["MEMORY.md"],
  enabled: true,
};

export async function shouldTrigger(
  state: DreamState,
  config: DreamConfig,
  agentDir: string
): Promise<boolean> {
  if (!config.enabled) {
    return false;
  }

  if (await isLocked(agentDir)) {
    return false;
  }

  if (state.sessionCount < config.minSessions) {
    return false;
  }

  if (state.lastRunAt !== null) {
    const lastRun = new Date(state.lastRunAt).getTime();
    const now = Date.now();
    const hoursSince = (now - lastRun) / (1000 * 60 * 60);
    if (hoursSince < config.minHours) {
      return false;
    }
  }

  return true;
}

export function mergeConfig(config: Record<string, unknown> = {}): DreamConfig {
  return {
    ...defaultConfig,
    ...(config as Partial<DreamConfig>),
    memoryFiles:
      Array.isArray(config.memoryFiles) && config.memoryFiles.length > 0
        ? (config.memoryFiles as string[])
        : defaultConfig.memoryFiles,
  };
}

export function hoursUntilNextTrigger(state: DreamState, config: DreamConfig): number | null {
  if (!config.enabled) return null;

  const sessionGap = Math.max(0, config.minSessions - state.sessionCount);

  if (state.lastRunAt === null) {
    return sessionGap > 0 ? null : 0;
  }

  const lastRun = new Date(state.lastRunAt).getTime();
  const hoursSince = (Date.now() - lastRun) / (1000 * 60 * 60);
  const hoursLeft = Math.max(0, config.minHours - hoursSince);

  // Both conditions must be met — return the larger blocker
  if (sessionGap > 0) return null; // session count unknown without rate info
  return hoursLeft;
}

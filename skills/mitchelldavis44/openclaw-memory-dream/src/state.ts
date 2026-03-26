import { readFile, writeFile, mkdir } from "fs/promises";
import { join } from "path";

async function ensureDir(dir: string): Promise<void> {
  await mkdir(dir, { recursive: true });
}

export interface DreamState {
  sessionCount: number;
  lastRunAt: string | null;
  lastRunStatus: "success" | "failed" | "running" | null;
  lastRunSummary: string | null;
}

const STATE_FILE = ".memory-dream-state.json";

const defaultState = (): DreamState => ({
  sessionCount: 0,
  lastRunAt: null,
  lastRunStatus: null,
  lastRunSummary: null,
});

export async function loadState(agentDir: string): Promise<DreamState> {
  const statePath = join(agentDir, STATE_FILE);
  try {
    const raw = await readFile(statePath, "utf-8");
    return { ...defaultState(), ...JSON.parse(raw) };
  } catch {
    return defaultState();
  }
}

export async function saveState(agentDir: string, state: DreamState): Promise<void> {
  await ensureDir(agentDir);
  const statePath = join(agentDir, STATE_FILE);
  await writeFile(statePath, JSON.stringify(state, null, 2), "utf-8");
}

export async function incrementSession(agentDir: string): Promise<DreamState> {
  const state = await loadState(agentDir);
  state.sessionCount += 1;
  await saveState(agentDir, state);
  return state;
}

export async function resetCounter(agentDir: string): Promise<DreamState> {
  const state = await loadState(agentDir);
  state.sessionCount = 0;
  state.lastRunAt = new Date().toISOString();
  await saveState(agentDir, state);
  return state;
}

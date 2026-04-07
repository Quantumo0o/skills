/**
 * singularity-forum - GitOps 模块
 * 为进化过程提供版本控制、stash 和 rollback 支持
 *
 * 功能：
 * - git stash 暂存改动
 * - git reset --hard 回滚
 * - 健康检查（工作区 clean/dirty 状态）
 * - 改动 diff 摘要
 */

import { execSync, exec } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 工作区根目录
const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');

// =============================================================================
// 工具函数
// =============================================================================

function git(args: string[], cwd = WORKSPACE): string {
  try {
    return execSync(`git ${args.join(' ')}`, {
      cwd,
      encoding: 'utf-8',
      timeout: 30000,
      windowsHide: true,
    }).trim();
  } catch (e: unknown) {
    const err = e as { status?: number; message?: string; stderr?: string };
    if (err.status !== 0) {
      throw new Error(`git ${args.join(' ')} failed (${err.status}): ${err.stderr || err.message || ''}`);
    }
    return err.stderr || '';
  }
}

function gitAsync(args: string[], cwd = WORKSPACE): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolve) => {
    exec(`git ${args.join(' ')}`, { cwd, encoding: 'utf-8', timeout: 30000, windowsHide: true }, (err, stdout, stderr) => {
      resolve({ stdout: (err ? (err as {stderr?:string}).stderr || '' : ''), stderr: (err ? (err as {stderr?:string}).stderr || '' : ''), code: (err ? (err as {code?:number}).code || 1 : 0) });
    });
  });
}

// =============================================================================
// 状态查询
// =============================================================================

export interface GitStatus {
  clean: boolean;
  branch: string;
  commit: string;
  staged: number;
  modified: number;
  untracked: number;
  behind: number;
  ahead: number;
}

export function getStatus(): GitStatus {
  try {
    const statusOut = git(['status', '--porcelain']);
    const branchOut = git(['branch', '--show-current']);
    const commitOut = git(['rev-parse', '--short', 'HEAD']);
    const tracking = git(['rev-list', '--left-right', '--count', '@{upstream}...HEAD']);

    const lines = statusOut.split('\n').filter(l => l.trim());
    let staged = 0, modified = 0, untracked = 0;
    for (const line of lines) {
      const st = line.slice(0, 2);
      if (st === '??') untracked++;
      else if (st === '  ') {}
      else {
        if (st[0] !== ' ' && st[0] !== '?') staged++;
        if (st[1] !== ' ' && st[1] !== '?') modified++;
      }
    }

    const [behind = '0', ahead = '0'] = tracking.split('\t');

    return {
      clean: staged === 0 && modified === 0 && untracked === 0,
      branch: branchOut,
      commit: commitOut,
      staged,
      modified,
      untracked,
      behind: parseInt(behind),
      ahead: parseInt(ahead),
    };
  } catch {
    return { clean: true, branch: 'unknown', commit: 'unknown', staged: 0, modified: 0, untracked: 0, behind: 0, ahead: 0 };
  }
}

export function isClean(): boolean {
  return getStatus().clean;
}

// =============================================================================
// 改动摘要
// =============================================================================

export interface ChangeSummary {
  files: string[];
  insertions: number;
  deletions: number;
  total: number;
}

export function getChangeSummary(): ChangeSummary {
  try {
    const out = git(['diff', '--stat', 'HEAD']);
    const lines = out.split('\n');
    let insertions = 0, deletions = 0, total = 0;
    for (const line of lines) {
      const m = line.match(/(\d+)\s+insertion/);
      if (m) insertions = parseInt(m[1]);
      const d = line.match(/(\d+)\s+deletion/);
      if (d) deletions = parseInt(d[1]);
    }
    const files = git(['diff', '--name-only', 'HEAD']).split('\n').filter(Boolean);
    total = insertions + deletions;
    return { files, insertions, deletions, total };
  } catch {
    return { files: [], insertions: 0, deletions: 0, total: 0 };
  }
}

// =============================================================================
// Stash 操作
// =============================================================================

export interface StashResult {
  success: boolean;
  stashRef?: string;
  message: string;
  files?: string[];
}

export function stash(message = 'evolver-auto-stash'): StashResult {
  const status = getStatus();
  if (status.clean) {
    return { success: true, message: 'Nothing to stash (working tree clean)', stashRef: undefined };
  }

  try {
    const files = git(['diff', '--name-only']).split('\n').filter(Boolean);
    git(['add', '-A']);
    const out = git(['stash', 'push', '-m', message]);
    const stashRef = out.match(/stash@\{\d+\}/)?.[0] || undefined;
    return { success: true, message: `Stashed ${files.length} file(s)`, stashRef, files };
  } catch (e: unknown) {
    const err = e as Error;
    return { success: false, message: 'Stash failed: ' + err.message };
  }
}

export function stashPop(): StashResult {
  try {
    git(['stash', 'pop']);
    return { success: true, message: 'Stash applied' };
  } catch (e: unknown) {
    const err = e as Error;
    return { success: false, message: 'Stash pop failed: ' + err.message };
  }
}

export function stashList(): string[] {
  try {
    const out = git(['stash', 'list']);
    return out.split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

// =============================================================================
// Rollback 操作
// =============================================================================

export type RollbackMode = 'hard' | 'stash' | 'none';

export interface RollbackResult {
  success: boolean;
  mode: RollbackMode;
  message: string;
  previousCommit?: string;
  currentCommit?: string;
  stashApplied?: boolean;
}

export function rollback(mode: RollbackMode = 'hard'): RollbackResult {
  const status = getStatus();
  const previousCommit = status.commit;

  if (!status.clean) {
    if (mode === 'hard') {
      // git reset --hard 会丢失未提交改动，先 stash
      git(['reset', '--hard', 'HEAD']);
      return {
        success: true,
        mode,
        message: 'Reset to HEAD (working tree was dirty, --hard discards changes)',
        previousCommit,
        currentCommit: getStatus().commit,
      };
    } else if (mode === 'stash') {
      const stashed = stash('rollback-backup');
      if (!stashed.success) {
        return { success: false, mode, message: 'Cannot rollback: stash failed and working tree is dirty' };
      }
    } else {
      // none 模式：不清工作区，直接 reset
    }
  }

  try {
    git(['reset', '--hard', 'HEAD~1']);
    return {
      success: true,
      mode,
      message: 'Rolled back one commit',
      previousCommit,
      currentCommit: getStatus().commit,
      stashApplied: mode === 'stash',
    };
  } catch (e: unknown) {
    const err = e as Error;
    return { success: false, mode, message: 'Rollback failed: ' + err.message };
  }
}

// =============================================================================
// 进化前准备（健康检查）
// =============================================================================

export interface HealthCheck {
  pass: boolean;
  checks: Array<{ name: string; pass: boolean; detail?: string }>;
  warnings: string[];
  errors: string[];
}

export function healthCheck(): HealthCheck {
  const checks: HealthCheck['checks'] = [];
  const warnings: string[] = [];
  const errors: string[] = [];

  // 1. Git 可用
  try {
    git(['--version']);
    checks.push({ name: 'git_available', pass: true });
  } catch {
    checks.push({ name: 'git_available', pass: false });
    errors.push('Git not available');
  }

  // 2. 工作区是 git 仓库
  try {
    const branch = git(['branch', '--show-current']);
    checks.push({ name: 'git_repo', pass: true, detail: 'branch=' + branch });
  } catch {
    checks.push({ name: 'git_repo', pass: false });
    errors.push('Workspace is not a git repository');
  }

  // 3. 最近一次 commit 不超过 7 天前
  try {
    const date = git(['log', '-1', '--format=%ci']);
    const commitTime = new Date(date).getTime();
    const ageDays = (Date.now() - commitTime) / (1000 * 60 * 60 * 24);
    checks.push({ name: 'recent_commit', pass: ageDays < 7, detail: `last commit ${ageDays.toFixed(1)} days ago` });
    if (ageDays > 7) warnings.push('No commits in over 7 days — consider committing before evolving');
  } catch {
    checks.push({ name: 'recent_commit', pass: false });
  }

  // 4. 无未解决的 stash
  const stashCount = stashList().length;
  checks.push({ name: 'no_stash_conflicts', pass: stashCount < 5, detail: `${stashCount} stash(es)` });
  if (stashCount >= 5) warnings.push(`${stashCount} stashes present — consider cleaning old ones`);

  // 5. 工作树状态
  const status = getStatus();
  checks.push({ name: 'working_tree', pass: status.clean, detail: status.clean ? 'clean' : `dirty (${status.modified} modified, ${status.untracked} untracked)` });
  if (!status.clean) warnings.push('Working tree has uncommitted changes — evolver may stash automatically');

  return {
    pass: errors.length === 0 && checks.every(c => c.pass),
    checks,
    warnings,
    errors,
  };
}

// =============================================================================
// 改动 Diff 预览（供 review 使用）
// =============================================================================

export function getDiff(files?: string[]): string {
  try {
    if (files && files.length > 0) {
      return git(['diff', ...files]);
    }
    return git(['diff', 'HEAD']);
  } catch {
    return '';
  }
}

export function getStagedDiff(): string {
  try {
    return git(['diff', '--cached']);
  } catch {
    return '';
  }
}

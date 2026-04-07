/**
 * singularity GEP GitOps
 * 安全 git 操作：rollback、diff 快照、关键文件保护
 *
 * 对标 capability-evolver/src/gep/gitOps.js
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { getRepoRoot } = require('./paths.cjs');

const DIFF_SNAPSHOT_MAX_CHARS = 8000;

// --- Critical protected files / paths ---
const CRITICAL_PROTECTED_PREFIXES = [
  'skills/feishu-',
  'skills/clawhub',
  'skills/git-sync',
  'skills/evolver',
];

const CRITICAL_PROTECTED_FILES = [
  'MEMORY.md', 'SOUL.md', 'IDENTITY.md', 'AGENTS.md',
  'USER.md', 'HEARTBEAT.md', 'TOOLS.md',
  'openclaw.json', '.env', 'package.json',
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function normalizeRelPath(relPath) {
  return String(relPath || '').replace(/\\/g, '/').replace(/^\.\/+/, '').trim();
}

function tryRunCmd(cmd, cwd, timeoutMs = 120000) {
  try {
    const out = execSync(cmd, {
      cwd,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: timeoutMs,
      windowsHide: true,
    });
    return { ok: true, out: String(out || ''), err: '' };
  } catch (e) {
    return {
      ok: false,
      out: e.stdout ? String(e.stdout) : '',
      err: e.stderr ? String(e.stderr) : e.message,
    };
  }
}

function countFileLines(absPath) {
  try {
    if (!fs.existsSync(absPath)) return 0;
    const buf = fs.readFileSync(absPath);
    if (!buf || buf.length === 0) return 0;
    let n = 1;
    for (let i = 0; i < buf.length; i++) if (buf[i] === 10) n++;
    return n;
  } catch { return 0; }
}

// ---------------------------------------------------------------------------
// Git status / diff
// ---------------------------------------------------------------------------

function isGitRepo(dir) {
  try {
    execSync('git rev-parse --git-dir', {
      cwd: dir, encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'], timeout: 5000,
    });
    return true;
  } catch { return false; }
}

function gitListChangedFiles(repoRoot) {
  const files = new Set();
  const cmds = [
    ['git diff --name-only', 60000],
    ['git diff --cached --name-only', 60000],
    ['git ls-files --others --exclude-standard', 60000],
  ];
  for (const [cmd, ms] of cmds) {
    const r = tryRunCmd(cmd, repoRoot, ms);
    if (r.ok) {
      for (const line of String(r.out).split('\n').map(l => l.trim()).filter(Boolean)) {
        files.add(line);
      }
    }
  }
  return Array.from(files);
}

function gitListUntrackedFiles(repoRoot) {
  const r = tryRunCmd('git ls-files --others --exclude-standard', repoRoot, 60000);
  if (!r.ok) return [];
  return String(r.out).split('\n').map(l => l.trim()).filter(Boolean);
}

function captureDiffSnapshot(repoRoot) {
  const parts = [];
  const unstaged = tryRunCmd('git diff', repoRoot, 30000);
  if (unstaged.ok && unstaged.out) parts.push(String(unstaged.out));
  const staged = tryRunCmd('git diff --cached', repoRoot, 30000);
  if (staged.ok && staged.out) parts.push(String(staged.out));
  let combined = parts.join('\n');
  if (combined.length > DIFF_SNAPSHOT_MAX_CHARS) {
    combined = combined.slice(0, DIFF_SNAPSHOT_MAX_CHARS) + '\n... [TRUNCATED]';
  }
  return combined || '';
}

// ---------------------------------------------------------------------------
// Critical path protection
// ---------------------------------------------------------------------------

function isCriticalProtectedPath(relPath) {
  const rel = normalizeRelPath(relPath);
  if (!rel) return false;
  for (const prefix of CRITICAL_PROTECTED_PREFIXES) {
    if (rel === prefix || rel.startsWith(prefix + '/')) return true;
  }
  for (const f of CRITICAL_PROTECTED_FILES) {
    if (rel === f) return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// Rollback
// ---------------------------------------------------------------------------

/**
 * 回滚工作区到 HEAD
 * mode: 'hard' | 'stash' | 'none'
 */
function rollbackTracked(repoRoot, mode = 'hard') {
  const safeMode = String(mode || 'hard').toLowerCase();
  if (safeMode === 'none') {
    console.log('[GitOps] Rollback skipped (mode=none)');
    return { ok: true, mode: 'none' };
  }
  if (safeMode === 'stash') {
    const stashRef = 'evo-rollback-' + Date.now();
    const r = tryRunCmd('git stash push -m "' + stashRef + '" --include-untracked', repoRoot, 60000);
    if (r.ok) {
      console.log('[GitOps] Stashed as "' + stashRef + '"');
      return { ok: true, mode: 'stash', ref: stashRef };
    }
    console.log('[GitOps] Stash failed, falling back to hard reset');
  }
  tryRunCmd('git restore --staged --worktree .', repoRoot, 60000);
  const r = tryRunCmd('git reset --hard', repoRoot, 60000);
  return { ok: r.ok, mode: 'hard' };
}

/**
 * 删除本次新增的非追踪文件
 */
function rollbackNewUntrackedFiles(repoRoot, baselineUntracked = []) {
  const baseline = new Set(baselineUntracked.map(String));
  const current = gitListUntrackedFiles(repoRoot);
  const toDelete = current.filter(f => !baseline.has(f));
  const skipped = [];
  const deleted = [];

  for (const rel of toDelete) {
    if (isCriticalProtectedPath(rel)) { skipped.push(rel); continue; }
    const abs = path.join(repoRoot, rel);
    const normRepo = path.resolve(repoRoot);
    const normAbs = path.resolve(abs);
    if (!normAbs.startsWith(normRepo + path.sep)) continue;
    try {
      if (fs.existsSync(normAbs) && fs.statSync(normAbs).isFile()) {
        fs.unlinkSync(normAbs);
        deleted.push(rel);
      }
    } catch (e) {
      console.warn('[GitOps] Unlink failed: ' + rel, e.message);
    }
  }

  // 清理空目录
  const dirsToCheck = new Set();
  for (const rel of deleted) {
    let dir = path.dirname(rel);
    while (dir && dir !== '.' && dir !== '/') {
      dirsToCheck.add(dir);
      dir = path.dirname(dir);
    }
  }
  const sortedDirs = dirsToCheck.size ? dirsToCheck : [];
  sortedDirs.sort((a, b) => b.length - a.length);
  const removedDirs = [];
  for (const rel of sortedDirs) {
    if (isCriticalProtectedPath(rel + '/')) continue;
    const dirAbs = path.join(repoRoot, rel);
    try {
      if (fs.readdirSync(dirAbs).length === 0) {
        fs.rmdirSync(dirAbs);
        removedDirs.push(rel);
      }
    } catch {}
  }

  return { deleted, skipped, removedDirs };
}

module.exports = {
  tryRunCmd,
  normalizeRelPath,
  countFileLines,
  isGitRepo,
  gitListChangedFiles,
  gitListUntrackedFiles,
  captureDiffSnapshot,
  DIFF_SNAPSHOT_MAX_CHARS,
  isCriticalProtectedPath,
  CRITICAL_PROTECTED_PREFIXES,
  CRITICAL_PROTECTED_FILES,
  rollbackTracked,
  rollbackNewUntrackedFiles,
};

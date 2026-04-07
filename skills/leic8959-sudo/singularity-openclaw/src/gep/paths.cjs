/**
 * singularity GEP Paths
 * 适配 singularity skill 目录结构的路径解析
 *
 * 目录布局（Desktop singularity）:
 *   C:\Users\29248\Desktop\singularity\    ← repoRoot
 *   C:\Users\29248\.openclaw\workspace\   ← workspace
 *   C:\Users\29248\.cache\singularity-forum\  ← cache
 */
const path = require('path');
const fs = require('fs');
const os = require('os');

function normalizeEnvPath(p) {
  return p ? path.normalize(p).replace(/\\/g, '/') : '';
}

// singularity skill 根目录（repoRoot）
function getRepoRoot() {
  if (process.env.SINGULARITY_REPO_ROOT) {
    return path.resolve(process.env.SINGULARITY_REPO_ROOT);
  }
  // 向上找 .git 或 package.json 所在目录
  let dir = __dirname;
  for (let i = 0; i < 4; i++) {
    const p = path.join(dir, '.git');
    if (fs.existsSync(p)) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  // 回退：桌面 singularity
  return path.join(os.homedir(), 'Desktop', 'singularity');
}

// OpenClaw workspace 根目录
function getWorkspaceRoot() {
  if (process.env.OPENCLAW_WORKSPACE) {
    return path.resolve(process.env.OPENCLAW_WORKSPACE);
  }
  return path.join(os.homedir(), '.openclaw', 'workspace');
}

// singularity 缓存目录
function getCacheDir() {
  if (process.env.SINGULARITY_CACHE_DIR) {
    return path.resolve(process.env.SINGULARITY_CACHE_DIR);
  }
  return path.join(os.homedir(), '.cache', 'singularity-forum');
}

// GEP 资产目录
function getGepAssetsDir() {
  return path.join(getCacheDir(), 'assets');
}

// memory 目录（OpenClaw workspace memory）
function getMemoryDir() {
  if (process.env.MEMORY_DIR) {
    return path.resolve(process.env.MEMORY_DIR);
  }
  return path.join(getWorkspaceRoot(), 'memory');
}

// evolution 目录
function getEvolutionDir() {
  return path.join(getMemoryDir(), 'evolution');
}

// 日志目录
function getLogsDir() {
  return path.join(getCacheDir(), 'logs');
}

function getEvolverLogPath() {
  return path.join(getLogsDir(), 'evolver.log');
}

module.exports = {
  getRepoRoot,
  getWorkspaceRoot,
  getCacheDir,
  getGepAssetsDir,
  getMemoryDir,
  getEvolutionDir,
  getLogsDir,
  getEvolverLogPath,
};

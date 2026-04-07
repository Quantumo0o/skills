/**
 * singularity GEP Session Reader
 * 读取 OpenClaw 实时 session 日志，提取信号
 *
 * 对标 capability-evolver evolve.js 里的 readRealSessionLog() + formatSessionLog()
 * 数据源：~/.openclaw/agents/{agent}/sessions/*.jsonl
 *
 * OpenClaw session JSONL 格式（每行一个条目）：
 *   { type: "message", id, message: { role: "user"|"assistant"|"tool", content: [...] } }
 *   { type: "tool_result", id, tool_result: { name, output } }
 *   { type: "annotation", ... }
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// --- Config ---
const AGENT_NAME = process.env.AGENT_NAME || 'main';
const SESSIONS_DIR = path.join(os.homedir(), '.openclaw', 'agents', AGENT_NAME, 'sessions');
const ACTIVE_WINDOW_MS = 24 * 60 * 60 * 1000; // 24h
const TARGET_BYTES = 120000;
const PER_SESSION_BYTES = 20000;

// --- Error patterns ---
const ERROR_PATTERNS = [
  /\[ERROR[\s\]]/i, /Error:/i, /Exception:/i, /\bFAIL\b/i,
  /Failed:\b/i, /"isError":\s*true/i, /"success"\s*:\s*false/i,
  /Error code:/i, /\berrno:\b/i, /ETIMEDOUT/i, /ECONNRESET/i,
  /Unauthorized/i, /401\b/, /403\b/, /rate.?limit/i, /429\b/,
  /SyntaxError/i, /TypeError/i, /ReferenceError/i, /RangeError/i,
  /ENOENT/i, /cannot find/i, /Module not found/i,
];

// --- Noise filters ---
const NOISE_PATTERNS = [
  /^heartbeat/i, /^HEARTBEAT/i, /^NO_REPLY$/i,
  /^(success|done|ok)$/i,
  /^[{}\[\]]$/,
];

// ============================================================================
// Raw reading
// ============================================================================

/**
 * 读取 session JSONL 文件最后 maxBytes 字节
 */
function readRecentLog(filePath, maxBytes = 20000) {
  try {
    if (!fs.existsSync(filePath)) return { raw: '', stat: null };
    const stat = fs.statSync(filePath);
    if (stat.size <= maxBytes) {
      return { raw: fs.readFileSync(filePath, 'utf-8'), stat };
    }
    // 从文件末尾读取，跳过可能不完整的行
    const fd = fs.openSync(filePath, 'r');
    const buf = Buffer.alloc(maxBytes);
    const bytesRead = fs.readSync(fd, buf, 0, maxBytes, stat.size - maxBytes);
    fs.closeSync(fd);
    const raw = buf.toString('utf-8', 0, bytesRead);
    // 跳过第一行（可能不完整）
    const firstNl = raw.indexOf('\n');
    return { raw: firstNl > 0 ? raw.slice(firstNl + 1) : raw, stat };
  } catch (e) {
    return { raw: '', stat: null };
  }
}

/**
 * 获取当前 agent 的 session 文件列表（按修改时间倒序）
 */
function getRecentSessionFiles() {
  if (!fs.existsSync(SESSIONS_DIR)) return [];
  const now = Date.now();
  try {
    return fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.lock') && !f.startsWith('evolver_hand_'))
      .map(f => {
        try {
          const st = fs.statSync(path.join(SESSIONS_DIR, f));
          return { name: f, time: st.mtime.getTime(), size: st.size };
        } catch { return null; }
      })
      .filter(f => f && (now - f.time) < ACTIVE_WINDOW_MS)
      .sort((a, b) => b.time - a.time);
  } catch { return []; }
}

// ============================================================================
// JSONL entry parsing
// ============================================================================

/**
 * 从 session entry 中提取纯文本
 */
function extractContent(entry) {
  try {
    // { type: "message", message: { role, content } }
    if (entry.type === 'message' && entry.message) {
      const msg = entry.message;
      const role = (msg.role || 'unknown').toUpperCase();
      let content = '';

      if (Array.isArray(msg.content)) {
        content = msg.content
          .map(c => {
            if (c.type === 'text') return c.text || '';
            if (c.type === 'toolCall') return `[TOOL: ${c.name || c.function?.name || '?'}]`;
            if (c.type === 'image') return '[IMAGE]';
            return '';
          })
          .join(' ');
      } else if (typeof msg.content === 'string') {
        content = msg.content;
      } else if (msg.content && typeof msg.content === 'object') {
        content = JSON.stringify(msg.content);
      }

      // LLM error
      if (msg.errorMessage) {
        const errMsg = typeof msg.errorMessage === 'string'
          ? msg.errorMessage
          : JSON.stringify(msg.errorMessage);
        content = `[LLM ERROR] ${errMsg.replace(/\n+/g, ' ').slice(0, 300)}`;
      }

      // Filter noise
      const trimmed = content.trim();
      if (!trimmed) return null;
      if (NOISE_PATTERNS.some(p => p.test(trimmed))) return null;

      return { role, content: trimmed.slice(0, 500) };
    }

    // { type: "tool_result", tool_result: { name, output } }
    if (entry.type === 'tool_result' || entry.tool_result) {
      const tr = entry.tool_result || entry;
      let output = '';
      if (tr.output) {
        output = typeof tr.output === 'string' ? tr.output : JSON.stringify(tr.output);
      } else {
        output = JSON.stringify(tr);
      }

      const trimmed = output.trim();
      if (!trimmed || trimmed === '{}' || trimmed === '""') return null;

      // Filter short success noise
      if (trimmed.length < 60 && /^(success|done|ok|✅)/i.test(trimmed)) return null;
      if (NOISE_PATTERNS.some(p => p.test(trimmed))) return null;

      return {
        role: 'TOOL',
        content: `[TOOL: ${tr.name || '?'}] ${trimmed.slice(0, 300)}`,
      };
    }

    // { type: "result", content: ... } (alternative format)
    if (entry.type === 'result' && entry.content) {
      const content = typeof entry.content === 'string'
        ? entry.content
        : JSON.stringify(entry.content);
      const trimmed = content.trim();
      if (!trimmed || trimmed.length < 20) return null;
      if (NOISE_PATTERNS.some(p => p.test(trimmed))) return null;
      return { role: 'RESULT', content: trimmed.slice(0, 300) };
    }

    return null;
  } catch (e) {
    return null;
  }
}

/**
 * 格式化 session 日志（人类可读）
 */
function formatSessionLog(rawJsonl) {
  const lines = rawJsonl.split('\n').filter(Boolean);
  const result = [];
  let lastLine = '';
  let repeatCount = 0;

  const flush = () => {
    if (repeatCount > 0) result.push(`   ... [Repeated ${repeatCount} times] ...`);
    repeatCount = 0;
  };

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const extracted = extractContent(entry);
      if (!extracted) continue;

      const entryLine = `**${extracted.role}**: ${extracted.content}`;

      if (entryLine === lastLine) {
        repeatCount++;
      } else {
        flush();
        result.push(entryLine);
        lastLine = entryLine;
      }
    } catch {}
  }
  flush();
  return result.join('\n');
}

// ============================================================================
// Signal extraction
// ============================================================================

function extractErrorsFromText(text) {
  const errors = [];
  for (const p of ERROR_PATTERNS) {
    if (p.test(text)) {
      errors.push(text.split('\n')[0].substring(0, 200));
    }
  }
  return errors;
}

function extractSignalsFromEntry(entry) {
  const extracted = extractContent(entry);
  if (!extracted) return [];
  const signals = [];

  // Error signals
  const errors = extractErrorsFromText(extracted.content);
  for (const err of errors) {
    signals.push({ signal: 'errsig:' + err.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 80), raw: err });
  }

  // Tool failure signals
  if (extracted.role === 'TOOL' && /\[TOOL:/.test(extracted.content)) {
    const failurePatterns = [
      { re: /timeout|timed_out|etimedout/i, signal: 'tool_timeout' },
      { re: /not found|enoent|module not found/i, signal: 'tool_not_found' },
      { re: /permission denied|access denied|eacces/i, signal: 'tool_permission_error' },
      { re: /rate limit|429/i, signal: 'tool_rate_limit' },
      { re: /error|failed|exception/i, signal: 'tool_error' },
    ];
    for (const p of failurePatterns) {
      if (p.re.test(extracted.content)) {
        signals.push({ signal: 'tool_failure:' + p.signal, raw: extracted.content.slice(0, 100) });
      }
    }
  }

  // User feedback signals
  if (extracted.role === 'USER') {
    const userPatterns = [
      { re: /wrong|incorrect|bad|error|bug/i, signal: 'user_error_report' },
      { re: /improve|better|should|could|fature/i, signal: 'user_improvement_request' },
      { re: /thank|great|awesome|nice/g, signal: 'positive_feedback' },
      { re: /stuck|loop|repeat|again|重复/i, signal: 'loop_detected' },
    ];
    for (const p of userPatterns) {
      if (p.re.test(extracted.content)) {
        signals.push({ signal: 'user_signal:' + p.signal, raw: extracted.content.slice(0, 100) });
      }
    }
  }

  return signals;
}

/**
 * 从 session 日志中提取所有信号
 */
function extractSignalsFromSessionLog(rawJsonl) {
  const lines = rawJsonl.split('\n').filter(Boolean);
  const signals = [];
  const seenSignals = new Set();

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const entrySignals = extractSignalsFromEntry(entry);
      for (const s of entrySignals) {
        if (!seenSignals.has(s.signal)) {
          seenSignals.add(s.signal);
          signals.push(s);
        }
      }
    } catch {}
  }
  return signals;
}

// ============================================================================
// Main API
// ============================================================================

/**
 * 读取最新 session 日志，返回格式化文本
 * @param {object} opts
 * @param {number} opts.maxSessions - 最多读取多少个 session 文件 (default 6)
 * @param {number} opts.maxBytes - 最多读取多少字节 (default 120000)
 * @returns {{ formatted: string, raw: string, files: string[], errors: string[] }}
 */
function readOpenClawSessions(opts = {}) {
  const maxSessions = Math.min(opts.maxSessions || 6, 20);
  const maxBytes = opts.maxBytes || TARGET_BYTES;
  const files = getRecentSessionFiles();

  if (!files.length) {
    return { formatted: '', raw: '', files: [], errors: [], signals: [] };
  }

  const sections = [];
  const allErrors = [];
  const allSignals = [];
  let totalBytes = 0;

  for (let i = 0; i < Math.min(files.length, maxSessions) && totalBytes < maxBytes; i++) {
    const f = files[i];
    const fp = path.join(SESSIONS_DIR, f.name);
    const { raw } = readRecentLog(fp, PER_SESSION_BYTES);

    if (!raw.trim()) continue;

    // 提取信号
    const fileSignals = extractSignalsFromSessionLog(raw);
    allSignals.push(...fileSignals);

    // 提取错误
    const rawLines = raw.split('\n');
    for (const line of rawLines) {
      try {
        const entry = JSON.parse(line);
        const extracted = extractContent(entry);
        if (extracted) {
          const errs = extractErrorsFromText(extracted.content);
          allErrors.push(...errs);
        }
      } catch {}
    }

    const formatted = formatSessionLog(raw);
    if (formatted.trim()) {
      sections.push(`--- SESSION (${f.name}) ---\n${formatted}`);
      totalBytes += formatted.length;
    }
  }

  return {
    formatted: sections.join('\n\n'),
    raw: sections.join('\n\n'),
    files: files.map(f => f.name),
    errors: allErrors,
    signals: allSignals,
  };
}

/**
 * 快速检查：有多少活跃 session 文件
 */
function getActiveSessionCount() {
  return getRecentSessionFiles().filter(f => !f.name.startsWith('evolver_hand_')).length;
}

/**
 * 检查是否有新的 session 数据（相比上次读取）
 */
function hasNewSessions(lastReadState) {
  const files = getRecentSessionFiles();
  if (!files.length) return false;
  if (!lastReadState) return true;
  for (const f of files) {
    const prev = lastReadState[f.name];
    if (!prev || f.time > prev) return true;
  }
  return false;
}

module.exports = {
  readOpenClawSessions,
  formatSessionLog,
  extractSignalsFromSessionLog,
  extractContent,
  extractErrorsFromText,
  getRecentSessionFiles,
  getActiveSessionCount,
  hasNewSessions,
  readRecentLog,
  ERROR_PATTERNS,
  SESSIONS_DIR,
};

#!/usr/bin/env node
/**
 * Qwen Chat Orchestrator — Puppeteer-based interaction with chat.qwen.ai
 * Adapted from ai-orchestrator (DeepSeek) for Qwen Chat
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Reuse diagnostics from ai-orchestrator, but keep Qwen-specific auth local.
const DIAG_DIR = path.resolve(__dirname, '../ai-orchestrator');
let Diagnostics;
let requireAuth;
try {
  ({ Diagnostics } = require(path.join(DIAG_DIR, 'diagnostics.js')));
} catch (e) {
  Diagnostics = class { start(){} succeed(){} fail(){} skip(){} printSummary(){} save(){} summary(){} finish(){} };
}
try {
  ({ requireAuth } = require(path.join(__dirname, 'auth-check.js')));
} catch (e) {
  requireAuth = async () => true;
}

// ═══ Configuration ═══════════════════════════════════════════════════════
const SCRIPT_DIR = path.dirname(process.argv[1]);
const BASE_DIR = path.resolve(SCRIPT_DIR);
const CONFIG_PATH = path.join(BASE_DIR, '.qwen.json');

const DEFAULT_CONFIG = {
  browserLaunchTimeout: 30000,
  answerTimeout: 600000,
  composerTimeout: 10000,
  navigationTimeout: 30000,
  idleTimeout: 15000,
  heartbeatInterval: 15000,
  domErrorIdleMs: 25000,
  shortAnswerStableMs: 300,
  minResponseLength: 50,
  maxContinueRounds: 30,
  deltaThreshold: 100,
  rateLimitMs: 5000,
  debugMode: false,
  logToFile: false,
  logPath: '.logs/qwen.log',
};

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const user = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return { ...DEFAULT_CONFIG, ...user };
    }
  } catch (e) {}
  return DEFAULT_CONFIG;
}

const CONFIG = loadConfig();
const TIMEOUT_ANSWER = CONFIG.answerTimeout;
const TIMEOUT_BROWSER = CONFIG.browserLaunchTimeout;
const MIN_RESPONSE = CONFIG.minResponseLength;

if (CONFIG.logToFile) {
  const logPath = path.resolve(BASE_DIR, CONFIG.logPath);
  try {
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    const origLog = console.log;
    console.log = (...args) => {
      const line = args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ');
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] ${line}\n`);
      origLog(...args);
    };
  } catch (e) {}
}

// ═══ CDP Interceptor state ═══════════════════════════════════════════════
var cdpInterceptor = null;

const argv = process.argv.slice(2);
const isVisible = argv.includes('--visible');
const waitForAuth = argv.includes('--wait');
const shouldClose = argv.includes('--close');
const endSession = argv.includes('--end-session');
const newChat = argv.includes('--new-chat');
const useDaemon = argv.includes('--daemon');
const dryRun = argv.includes('--dry-run');
const doSearch = argv.includes('--search');
const VERBOSE = argv.includes('--verbose');
const DEBUG = argv.includes('--debug');
const FILE_ARG_IDX = argv.indexOf('--file');
const FILE_PROMPT_PATH = FILE_ARG_IDX !== -1 ? argv[FILE_ARG_IDX + 1] : null;

// ═══ Auto-detect Chrome ══════════════════════════════════════════════════
let executablePath;
try {
  const bundled = require('puppeteer').executablePath();
  if (bundled && fs.existsSync(bundled)) executablePath = bundled;
} catch {}
if (!executablePath) {
  try {
    const w = require('child_process').execSync(
      'which chromium 2>/dev/null || which chromium-browser 2>/dev/null || which google-chrome 2>/dev/null || echo ""',
      { encoding: 'utf8' }
    ).trim();
    if (w && fs.existsSync(w)) executablePath = w;
  } catch {}
}

// ═══ Helpers ═════════════════════════════════════════════════════════════
function log(...a) { console.log(...a); }
function debugLog(...a) { if (VERBOSE || DEBUG) console.log(...a); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function ensureDirSync(d) { try { fs.mkdirSync(d, { recursive: true }); } catch {} }

// ═══ Qwen-specific constants ═════════════════════════════════════════════
const QWEN_URL = 'https://chat.qwen.ai/';
const QWEN_CHAT_RE = /^https:\/\/chat\.qwen\.ai\/c\//;

// Input/composer selectors — try the most specific first
const COMPOSER = [
  '#chat-input',
  'textarea#chat-input',
  'textarea[id*="chat-input" i]',
  'textarea[placeholder*="Message" i]',
  'textarea[placeholder*="Send a message" i]',
  'textarea[placeholder*="Ask" i]',
  'textarea[placeholder]',
  'textarea',
  'div[contenteditable="true"]',
  'div[role="textbox"]',
  'div[class*="composer" i]',
];

// Response selectors
const RESPONSE_SELECTORS = [
  'div[class*="markdown-body" i]',
  'div[class*="md-preview" i]',
  'div[class*="message-content" i]',
  'article',
  '.prose',
  '[class*="message"][class*="assistant"]',
  '[class*="message"][class*="ai"]',
];

// API patterns for CDP interception
const API_PATTERNS = [
  '/api/v1/chat/completions',
  '/api/v2/chat/completions',
  '/api/v2/chats',
  '/api/v1/generate',
  '/api/v2/messages',
  '/chat/completions',
  '/generate',
];

// ═══ Session & file management ═══════════════════════════════════════════
const SESSIONS_DIR = path.join(BASE_DIR, '.sessions');
const PROFILE_DIR = path.join(BASE_DIR, '.profile');
const DAEMON_ENDPOINT_FILE = path.join(BASE_DIR, '.daemon-ws-endpoint');
const SESSION_IDX = argv.indexOf('--session');
const sessionName = SESSION_IDX !== -1 ? (argv[SESSION_IDX + 1] || 'default') : null;

const question = FILE_PROMPT_PATH
  ? fs.readFileSync(FILE_PROMPT_PATH, 'utf8').trim()
  : argv.filter(a => !a.startsWith('--') && (SESSION_IDX === -1 || argv.indexOf(a) !== SESSION_IDX + 1)).join(' ');

let browser = null;
let qwenPage = null;
let browserLaunchedByUs = false;
let browserConnectionMode = 'local';

ensureDirSync(SESSIONS_DIR);
ensureDirSync(PROFILE_DIR);

function getSessionFile(name) { return path.join(SESSIONS_DIR, `${name}.json`); }
function loadSession(name) {
  try {
    const f = getSessionFile(name);
    if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  } catch {}
  return { name, messageCount: 0, created: null, lastUsed: null, chatUrl: null };
}
function saveSession(name, data) {
  try { fs.writeFileSync(getSessionFile(name), JSON.stringify(data, null, 2)); } catch {}
}
function deleteSession(name) { try { fs.unlinkSync(getSessionFile(name)); } catch {} }

// ═══ Profile lock cleanup ════════════════════════════════════════════════
async function killChromeProfile(profilePath) {
  try {
    const { execSync } = require('child_process');
    const pids = execSync(
      `ps aux | grep -i chrome | grep "${profilePath}" | grep -v grep | awk '{print $2}'`,
      { encoding: 'utf8' }
    ).split('\n').filter(p => p.trim());
    for (const pid of pids) {
      try { process.kill(pid.trim(), 'SIGKILL'); } catch {}
    }
    await sleep(1000);
    try { execSync('rm -rf /dev/shm/.com.google.Chrome.* 2>/dev/null || true'); } catch {}
    try { execSync('rm -rf /tmp/.com.google.Chrome.* 2>/dev/null || true'); } catch {}
  } catch {}
}

async function launchWithTimeout(options, timeoutMs = 30000) {
  const profileDir = options.userDataDir;
  if (profileDir && fs.existsSync(profileDir)) {
    for (const lock of ['SingletonLock', 'SingletonSocket', 'SingletonCookie']) {
      try { fs.unlinkSync(path.join(profileDir, lock)); } catch {}
    }
  }
  log(`🚀 Запуск браузера (timeout: ${timeoutMs}ms)...`);
  const p = puppeteer.launch(options);
  const t = new Promise((_, rj) => setTimeout(() => rj(new Error(`Launch timeout after ${timeoutMs}ms`)), timeoutMs));
  const b = await Promise.race([p, t]);
  log('✅ Браузер запущен');
  return b;
}

async function isBrowserAlive(ws) {
  try {
    const b = await puppeteer.connect({ browserWSEndpoint: ws, timeout: 5000 });
    const pgs = await b.pages();
    await b.disconnect();
    return pgs.length > 0;
  } catch { return false; }
}

async function connectToDaemon() {
  let ws = '';
  if (fs.existsSync(DAEMON_ENDPOINT_FILE)) {
    ws = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
  } else {
    try {
      const dp = getSessionFile('daemon');
      if (fs.existsSync(dp)) {
        const ds = JSON.parse(fs.readFileSync(dp, 'utf8'));
        if (ds?.browserWSEndpoint) {
          ws = ds.browserWSEndpoint.trim();
          try { fs.writeFileSync(DAEMON_ENDPOINT_FILE, ws); } catch {}
        }
      }
    } catch {}
  }
  if (!ws) throw new Error('Демон не запущен. Запусти: node qwen-daemon.js');
  log('🔗 Подключаюсь к демону...');
  try {
    const b = await puppeteer.connect({ browserWSEndpoint: ws, defaultViewport: null });
    browserConnectionMode = 'daemon';
    return b;
  } catch (e) {
    try { fs.unlinkSync(DAEMON_ENDPOINT_FILE); } catch {}
    throw new Error(`Демон недоступен: ${e.message}`);
  }
}

async function connectToExisting(session) {
  if (session?.wsEndpoint) {
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: session.wsEndpoint });
      browserConnectionMode = 'session';
      const pgs = await browser.pages();
      qwenPage = pgs.find(p => { try { return p.url().includes('qwen'); } catch { return false; } }) || pgs[0];
      if (qwenPage) { log('🔗 Подключились к существующему браузеру'); return true; }
    } catch { log('⚠️ Не удалось подключиться, запускаю новый'); }
  }
  return false;
}

async function cleanup() {
  try {
    if (browser) {
      if (browserLaunchedByUs) { await browser.close().catch(() => {}); }
      else { try { browser.disconnect(); } catch {} }
    }
  } finally { browser = null; qwenPage = null; }
}

async function disableAnimations(page) {
  await page.evaluate(() => {
    const s = document.createElement('style');
    s.textContent = '*,*::before,*::after{animation-duration:0s!important;transition-duration:0s!important}';
    document.head.appendChild(s);
  });
}

// ═══ Page ready ══════════════════════════════════════════════════════════
async function waitUntilReady(page, timeout = 45000) {
  const start = Date.now();
  let i = 0;
  while (Date.now() - start < timeout) {
    i++;
    try {
      const url = page.url();
      if (/auth|login|signin|signup/i.test(url)) {
        throw new Error('Требуется авторизация — запусти с --visible --wait');
      }
    } catch (e) {
      if (e.message && e.message.includes('авторизация')) throw e;
    }
    for (const sel of COMPOSER) {
      try {
        const el = await page.$(sel);
        if (el) {
          log(`✅ Composer: ${sel} (${i} checks, ${((Date.now()-start)/1000).toFixed(1)}s)`);
          return sel;
        }
      } catch {}
    }
    await sleep(i <= 3 ? 500 : 1000);
  }
  throw new Error(`Qwen not ready after ${timeout}ms`);
}

// ═══ CDP Interceptor for Qwen API ════════════════════════════════════════
async function setupQwenInterceptor(page) {
  const client = await page.target().createCDPSession();
  await client.send('Network.enable');

  let reqCounter = 0;
  let expectedIds = new Set();
  let windowOpen = false;
  let pendingResolve = null;
  let pendingTimer = null;
  let respState = { resolved: false, result: null };

  function parseQwenBody(raw) {
    if (!raw || typeof raw !== 'string') return { text: null, finished: false };
    const trimmed = raw.trim();
    if (!trimmed) return { text: null, finished: false };

    // Try SSE format
    if (trimmed.includes('data:') || trimmed.includes('event:')) {
      return parseQwenSSE(trimmed);
    }

    // Try JSON
    try {
      const obj = JSON.parse(trimmed);
      if (obj.choices?.[0]?.message?.content) return { text: obj.choices[0].message.content, finished: true };
      if (obj.choices?.[0]?.delta?.content) {
        const finished = obj.choices?.[0]?.delta?.status === 'finished' || obj.choices?.[0]?.finish_reason != null;
        return { text: obj.choices[0].delta.content, finished };
      }
      if (obj.output?.text) return { text: obj.output.text, finished: true };
      if (obj.text) return { text: obj.text, finished: true };
      if (obj.output) return { text: obj.output, finished: true };
      if (obj.data?.chat?.history?.messages) {
        const msgs = obj.data.chat.history.messages;
        if (msgs) {
          const last = Object.values(msgs).find(m => m.role === 'assistant');
          if (last?.content) return { text: last.content, finished: true };
          if (Array.isArray(last?.content_list)) {
            const answer = last.content_list.filter(x => x.phase === 'answer').map(x => x.content || '').join('');
            if (answer) return { text: answer, finished: true };
          }
        }
      }
      return { text: null, finished: false };
    } catch { return { text: null, finished: false }; }
  }

  function parseQwenSSE(raw) {
    let acc = '';
    let finished = false;
    for (const line of raw.split('\n')) {
      if (!line.startsWith('data:') || line.includes('[DONE]')) continue;
      const payload = line.slice(5).trim();
      if (!payload) continue;
      try {
        const obj = JSON.parse(payload);
        const delta = obj.choices?.[0]?.delta;
        const phase = delta?.phase;
        const status = delta?.status;
        const content = delta?.content;
        if (typeof content === 'string' && (phase === 'answer' || !phase)) {
          acc += content;
        }
        if (phase === 'answer' && status === 'finished') finished = true;

        const msg = obj.choices?.[0]?.message?.content;
        if (typeof msg === 'string' && !acc) acc = msg;
        if (obj.output?.text && !acc) acc = obj.output.text;
        if (obj.text && !acc) acc = obj.text;
      } catch {}
    }
    return { text: acc.length > 0 ? acc : null, finished };
  }

  client.on('Network.requestWillBeSent', (ev) => {
    const url = ev.request.url;
    const isCompletion = ev.request.method === 'POST' && /\/api\/v2\/chat\/completions(\?|$)/.test(url);
    if (isCompletion) {
      if (!windowOpen || respState.resolved) return;
      windowOpen = false;
      expectedIds.add(ev.requestId);
      debugLog(`[CDP] caught Qwen completion API: ${ev.requestId} ${url}`);
    }
  });

  client.on('Network.loadingFinished', async (ev) => {
    if (!expectedIds.has(ev.requestId) || respState.resolved) return;
    try {
      const resp = await client.send('Network.getResponseBody', { requestId: ev.requestId });
      let body = resp.body;
      if (resp.base64Encoded) body = Buffer.from(body, 'base64').toString('utf8');
      const parsed = parseQwenBody(body);
      const text = parsed?.text || null;
      debugLog(`[CDP] Body: ${body.length} chars, parsed: ${text ? text.length + ' chars' : 'null'}, finished: ${!!parsed?.finished}`);
      respState.resolved = true;
      respState.result = { raw: body, text, finished: !!parsed?.finished, format: text ? 'parsed' : 'raw' };
      if (pendingResolve) { const r = pendingResolve; pendingResolve = null; if (pendingTimer) clearTimeout(pendingTimer); r(respState.result); }
      expectedIds.delete(ev.requestId);
    } catch (err) {
      debugLog(`[CDP] Error: ${err.message}`);
      if (!respState.resolved) {
        respState.resolved = true;
        respState.result = { raw: null, text: null, format: 'failed', error: err.message };
        if (pendingResolve) { const r = pendingResolve; pendingResolve = null; r(respState.result); }
        expectedIds.delete(ev.requestId);
      }
    }
  });

  client.on('Network.loadingFailed', (ev) => {
    if (!expectedIds.has(ev.requestId) || respState.resolved) return;
    respState.resolved = true;
    respState.result = { raw: null, text: null, format: 'failed', error: 'network_failed' };
    if (pendingResolve) { const r = pendingResolve; pendingResolve = null; r(respState.result); }
    expectedIds.delete(ev.requestId);
  });

  function prepareForRequest() {
    pendingResolve = null;
    if (pendingTimer) clearTimeout(pendingTimer);
    respState = { resolved: false, result: null };
    reqCounter++;
    windowOpen = true;
    debugLog(`[CDP] Ready #${reqCounter}`);
    return reqCounter;
  }

  async function waitForResponse(timeoutMs = 120000) {
    if (respState.resolved && respState.result) {
      return respState.result;
    }
    return new Promise((resolve) => {
      pendingResolve = resolve;
      pendingTimer = setTimeout(() => {
        if (pendingResolve) { pendingResolve = null; resolve(null); }
      }, timeoutMs);
    });
  }

  function consumeResponse() {
    if (!respState.resolved || !respState.result) return null;
    const r = respState.result;
    respState = { resolved: false, result: null };
    pendingResolve = null;
    if (pendingTimer) clearTimeout(pendingTimer);
    pendingTimer = null;
    return r;
  }

  return { prepareForRequest, waitForResponse, consumeResponse };
}

// ═══ Send prompt ═════════════════════════════════════════════════════════
async function sendPrompt(page, composerSelector, prompt) {
  log(`📝 "${prompt.substring(0, 60)}${prompt.length > 60 ? '...' : ''}"`);
  if (cdpInterceptor) { cdpInterceptor.prepareForRequest(); }

  const el = await page.waitForSelector(composerSelector, { visible: true, timeout: 10000 });

  await el.evaluate((el, text) => {
    el.focus();
    if (el.isContentEditable || el.getAttribute('contenteditable') === 'true') {
      el.textContent = text;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (el instanceof HTMLTextAreaElement || el instanceof HTMLInputElement) {
      const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
      if (setter) setter.call(el, text); else el.value = text;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    } else {
      el.textContent = text;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
    // Enter to send
    const ev = { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true };
    el.dispatchEvent(new KeyboardEvent('keydown', ev));
    el.dispatchEvent(new KeyboardEvent('keypress', ev));
    el.dispatchEvent(new KeyboardEvent('keyup', ev));
    // Click send button
    for (const sel of ['#send-message-button', 'button[type="submit"]', '[data-testid="send"]', 'button[aria-label*="send" i]']) {
      const b = (el.closest('form') || document).querySelector(sel);
      if (b && b.offsetWidth > 0 && !b.disabled) { b.click(); return; }
    }
    const nb = el.parentElement?.querySelector('button, [role="button"]');
    if (nb && nb.offsetWidth > 0 && !nb.disabled) nb.click();
  }, prompt);

  await sleep(20);
}

// ═══ Enable web search ═══════════════════════════════════════════════════
async function enableWebSearch(page) {
  log('🔍 Активирую Web Search...');
  await page.evaluate(() => {
    const btn = document.querySelector('[class*="globe" i], button[aria-label*="search" i], [class*="search-toggle" i]');
    if (btn && btn.offsetWidth > 0 && !btn.disabled) btn.click();
  }).catch(() => {});
  await sleep(1000);
}

// ═══ Force thinking mode ═════════════════════════════════════════════════
async function ensureThinkingMode(page) {
  const readModeInfo = async () => {
    return page.evaluate(() => {
      const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
      const input = document.querySelector('.qwen-thinking-selector input[role="combobox"]');
      const trigger = document.querySelector('.qwen-thinking-selector .ant-select-selector, .qwen-thinking-selector');
      const rect = trigger ? trigger.getBoundingClientRect() : null;
      return {
        exists: !!label,
        current: label ? (label.textContent || '').trim() : '',
        expanded: input ? input.getAttribute('aria-expanded') : null,
        rect: rect ? { x: rect.x, y: rect.y, w: rect.width, h: rect.height } : null,
      };
    }).catch(() => ({ exists: false, current: '', expanded: null, rect: null }));
  };

  const modeInfo = await readModeInfo();
  if (!modeInfo.exists) {
    log('⚠️ Переключатель режима не найден — пропускаю выбор thinking');
    return false;
  }

  if (/размыш|мышлен|think|reason/i.test(modeInfo.current)) {
    log(`🧠 Режим уже установлен: ${modeInfo.current}`);
    return true;
  }

  log(`🧠 Переключаю режим: ${modeInfo.current || 'unknown'} -> thinking`);

  let opened = false;
  if (modeInfo.rect) {
    const x = modeInfo.rect.x + modeInfo.rect.w / 2;
    const y = modeInfo.rect.y + modeInfo.rect.h / 2;
    try {
      await page.mouse.move(x, y);
      await page.mouse.down();
      await sleep(80);
      await page.mouse.up();
      await sleep(250);
      const probe = await readModeInfo();
      opened = probe.expanded === 'true';
    } catch {}
  }

  const triggerSelectors = [
    '.qwen-thinking-selector .ant-select-selector',
    '.qwen-thinking-selector .qwen-select-thinking-label',
    '.qwen-thinking-selector input[role="combobox"]',
    '.qwen-thinking-selector',
  ];

  if (!opened) {
    for (const selector of triggerSelectors) {
      const handle = await page.$(selector).catch(() => null);
      if (!handle) continue;
      try {
        await handle.click({ delay: 50 });
        await sleep(200);
      } catch {}
      const probe = await readModeInfo();
      if (probe.expanded === 'true') {
        opened = true;
        break;
      }
    }
  }

  if (!opened) {
    log('⚠️ Не удалось раскрыть селектор режима');
    return false;
  }

  const pickedByText = await page.evaluate(() => {
    const matcher = /^(мышление|thinking)$/i;
    const fallbackMatcher = /(мышление|размыш|мышлен|think|thinking|reason)/i;
    const candidates = Array.from(document.querySelectorAll('[role="option"], .ant-select-item-option, .ant-select-dropdown .ant-select-item, .ant-select-dropdown li, .ant-select-dropdown div'));
    const visible = candidates.filter((el) => {
      const text = (el.innerText || el.textContent || '').trim();
      if (!text) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return !(s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0);
    });
    const option = visible.find((el) => matcher.test((el.innerText || el.textContent || '').trim()))
      || visible.find((el) => fallbackMatcher.test((el.innerText || el.textContent || '').trim()));
    if (!option) {
      return {
        ok: false,
        reason: 'no-thinking-option',
        visibleTexts: visible.slice(0, 20).map((el) => (el.innerText || el.textContent || '').trim()),
      };
    }
    const r = option.getBoundingClientRect();
    return {
      ok: true,
      text: (option.innerText || option.textContent || '').trim(),
      rect: { x: r.x, y: r.y, w: r.width, h: r.height },
    };
  }).catch((e) => ({ ok: false, reason: e.message }));

  if (pickedByText.ok && pickedByText.rect) {
    try {
      const x = pickedByText.rect.x + pickedByText.rect.w / 2;
      const y = pickedByText.rect.y + pickedByText.rect.h / 2;
      await page.mouse.move(x, y);
      await page.mouse.down();
      await sleep(60);
      await page.mouse.up();
      await sleep(350);
    } catch {}
  }

  if (!pickedByText.ok) {
    for (let i = 0; i < 6; i++) {
      await page.keyboard.press('ArrowDown').catch(() => {});
      await sleep(120);
      const probe = await readModeInfo();
      if (/мышление|размыш|мышлен|think|reason/i.test(probe.current)) {
        log(`🧠 Режим мышления включён: ${probe.current}`);
        return true;
      }
      await page.keyboard.press('Enter').catch(() => {});
      await sleep(250);
      const afterEnter = await readModeInfo();
      if (/мышление|размыш|мышлен|think|reason/i.test(afterEnter.current)) {
        log(`🧠 Режим мышления включён: ${afterEnter.current}`);
        return true;
      }
    }
  }

  await sleep(500);
  const finalLabel = await page.evaluate(() => {
    const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
    return label ? (label.textContent || '').trim() : '';
  }).catch(() => '');

  if (/мышление|размыш|мышлен|think|reason/i.test(finalLabel)) {
    try {
      await page.keyboard.press('Escape').catch(() => {});
      await sleep(120);
      await page.click('body').catch(() => {});
      await sleep(120);
    } catch {}
    log(`🧠 Режим мышления включён: ${finalLabel}`);
    return true;
  }

  log(`⚠️ Не удалось подтвердить thinking mode (после переключения: ${finalLabel || pickedByText.reason || 'unknown'})`);
  return false;
}

// ═══ New chat ════════════════════════════════════════════════════════════
async function startNewChat(page, force = false) {
  log('🆕 Начинаю новый чат...');
  try {
    const url = page.url();
    if (QWEN_CHAT_RE.test(url) && !newChat && !force) { log('🆕 Уже в чате — продолжаем'); return; }
  } catch {}

  const clicked = await page.evaluate(() => {
    const candidates = document.querySelectorAll('button, [role="button"], a, i');
    for (const el of candidates) {
      const text = (el.textContent || el.innerText || '').trim().toLowerCase();
      const aria = (el.getAttribute('aria-label') || '').toLowerCase();
      const cls = (el.className || '').toLowerCase();
      if (el.offsetWidth > 0 && (
        text.includes('new chat') || text.includes('новый чат') || text.includes('новый') ||
        aria.includes('new chat') || cls.includes('new-chat') || cls.includes('sidebar-new') ||
        cls.includes('plus') || cls.includes('icon-line-plus')
      )) {
        el.click();
        return text || aria || cls;
      }
    }
    return null;
  }).catch(() => null);

  if (clicked) {
    log(`🆕 New chat: "${clicked}"`);
    await sleep(1500);
  } else {
    log('📍 Переход на главную Qwen...');
    try { await page.goto(QWEN_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout }); }
    catch (e) { if (!String(e?.message || '').includes('ERR_ABORTED')) throw e; log('⚠️ Навигация прервана UI'); }
    await sleep(1500);
  }
}

// ═══ Extract answer from DOM ═════════════════════════════════════════════
async function extractAnswerFromDOM(page, minLen = 50) {
  return page.evaluate((minLen) => {
    // Try markdown-rendered content blocks
    const selectors = [
      'div[class*="markdown-body"]',
      'div[class*="md-preview"]',
      'div[class*="message-content"]',
      'article',
      '.prose',
    ];
    for (const sel of selectors) {
      const els = document.querySelectorAll(sel);
      for (let i = els.length - 1; i >= 0; i--) {
        const el = els[i];
        if (el.closest('.sidebar, nav, aside, .history')) continue;
        if (el.closest('textarea, [contenteditable], [role="textbox"]')) continue;
        const txt = el.innerText?.trim();
        if (txt && txt.length >= minLen) return txt.slice(0, 15000);
      }
    }
    // Fallback: get body text
    return null;
  }, minLen).catch(() => null);
}

// ═══ Wait for response ═══════════════════════════════════════════════════
async function waitForAnswer(page, timeout = TIMEOUT_ANSWER) {
  const start = Date.now();
  let idleSince = null;
  let lastText = '';
  let continueClicks = 0;

  async function clickContinueIfPresent() {
    const clicked = await page.evaluate(() => {
      const matcher = /continue|continue generating|продолж|продолжить генерацию|далее|more|read more/i;
      const all = Array.from(document.querySelectorAll('button, [role="button"], a, div, span'));
      const btn = all.find((el) => {
        const text = (el.innerText || el.textContent || '').trim();
        if (!text) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        if (s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0) return false;
        return matcher.test(text);
      });
      if (!btn) return { clicked: false };
      const text = (btn.innerText || btn.textContent || '').trim();
      const r = btn.getBoundingClientRect();
      btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
      btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
      btn.click();
      return { clicked: true, text };
    }).catch(() => ({ clicked: false }));
    return clicked;
  }

  while (Date.now() - start < timeout) {
    let networkFinished = false;
    try {
      if (cdpInterceptor) {
        let network = cdpInterceptor.consumeResponse ? cdpInterceptor.consumeResponse() : null;
        if (!network) {
          network = await cdpInterceptor.waitForResponse(250).catch(() => null);
          if (network && cdpInterceptor.consumeResponse) {
            const consumed = cdpInterceptor.consumeResponse();
            if (consumed) network = consumed;
          }
        }
        if (network?.text && network.text.length > lastText.length) {
          lastText = network.text;
          idleSince = null;
          debugLog(`🌐 Ответ из сети: ${lastText.length} символов`);
        }
        networkFinished = !!network?.finished;
      }
    } catch (e) { debugLog('Network check error:', e.message); }

    // DOM-based check
    try {
      const text = await extractAnswerFromDOM(page, MIN_RESPONSE);
      if (text && text.length > lastText.length) {
        lastText = text;
        idleSince = null;
        debugLog(`📝 Ответ: ${lastText.length} символов`);
      }

      const continueBtn = await clickContinueIfPresent();
      if (continueBtn.clicked) {
        continueClicks += 1;
        log(`🔁 Continue clicked (${continueClicks}): ${continueBtn.text}`);
        idleSince = null;
        await sleep(2000);
        continue;
      }

      if (lastText.length > 0) {
        if (networkFinished) {
          if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
          debugLog(`✅ Ответ готов по сети: ${lastText.length} символов`);
          return { text: lastText, source: 'network', complete: true, continueClicks };
        }

        if (idleSince === null) {
          idleSince = Date.now();
        } else if (Date.now() - idleSince > CONFIG.shortAnswerStableMs) {
          const isGenerating = await page.evaluate(() => {
            return !!(
              document.querySelector('[class*="stop" i]') ||
              document.querySelector('[class*="loading" i]') ||
              document.querySelector('i[class*="Stop" i]') ||
              document.querySelector('i[class*="loading"]') ||
              document.querySelector('[class*="generating" i]') ||
              document.querySelector('[class*="thinking" i]') ||
              document.body?.innerText?.includes('The chat is in progress!')
            );
          }).catch(() => false);

          if (!isGenerating) {
            if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
            debugLog(`✅ Ответ готов: ${lastText.length} символов`);
            return { text: lastText, source: lastText.length >= MIN_RESPONSE ? 'dom' : 'network', complete: true, continueClicks };
          } else {
            idleSince = null;
          }
        }
      }
    } catch (e) { debugLog('DOM check error:', e.message); }

    await sleep(500);
  }

  if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
  log('⏰ Таймаут ожидания ответа');
  return { text: lastText || null, source: lastText.length >= MIN_RESPONSE ? 'dom' : 'network', complete: false, continueClicks };
}

// ═══ Ensure browser ══════════════════════════════════════════════════════
async function ensureBrowser(session) {
  if (browser && qwenPage) {
    try { await qwenPage.url(); return qwenPage; }
    catch (e) { browser = null; qwenPage = null; }
  }

  // Try daemon
  if (useDaemon || (!isVisible && fs.existsSync(DAEMON_ENDPOINT_FILE))) {
    try {
      browser = await connectToDaemon();
      const pages = await browser.pages();
      qwenPage = pages.find(p => {
        try { return p.url().includes('qwen'); } catch { return false; }
      }) || pages[0];
      if (!qwenPage?.url?.().match(QWEN_CHAT_RE || /qwen/i)) {
        log('📍 Навигация на Qwen Chat...');
        await qwenPage.goto(QWEN_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
      }
      log(`🔗 Подключился к демону (URL: ${qwenPage.url().substring(0, 50)})`);
      return qwenPage;
    } catch (e) {
      if (useDaemon) throw new Error(`Демон недоступен: ${e.message}`);
      log(`⚠️ Демон недоступен: ${e.message}, запускаю локально`);
    }
  }

  // Try existing session
  if (session && await connectToExisting(session)) {
    return qwenPage;
  }

  // Launch new
  await cleanup();
  if (!session && shouldClose) await killChromeProfile(PROFILE_DIR);

  const launchOptions = {
    headless: isVisible ? false : 'new',
    userDataDir: PROFILE_DIR,
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--no-first-run', '--no-default-browser-check',
      '--disable-gpu', '--window-size=1280,800',
    ],
  };
  if (executablePath) launchOptions.executablePath = executablePath;

  browser = await launchWithTimeout(launchOptions, TIMEOUT_BROWSER);
  browserLaunchedByUs = true;
  browserConnectionMode = 'local';

  const pages = await browser.pages();
  qwenPage = pages[0] || await browser.newPage();
  await qwenPage.setUserAgent(
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  );
  await qwenPage.setViewport({ width: 1280, height: 800 });
  await qwenPage.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  if (session?.chatUrl && !newChat) {
    log(`📂 Открываю чат: ${session.chatUrl.substring(0, 60)}`);
    await qwenPage.goto(session.chatUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  } else {
    log('📍 Открываем Qwen Chat...');
    await qwenPage.goto(QWEN_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  }

  await disableAnimations(qwenPage);
  await sleep(150);

  if (isVisible && waitForAuth) {
    log('\n⚠️ Авторизуйтесь в Qwen и нажмите Enter...');
    if (process.stdin.isTTY) {
      await new Promise(r => { process.stdin.resume(); process.stdin.once('data', () => r()); });
    } else {
      await sleep(60000);
    }
  }

  if (session) {
    session.wsEndpoint = browser.wsEndpoint();
    session.chatUrl = qwenPage.url();
    saveSession(session.name, session);
  }

  return qwenPage;
}

// ═══ MAIN ════════════════════════════════════════════════════════════════
async function main() {
  let diag = null;

  try {
    // End session
    if (endSession && sessionName) {
      deleteSession(sessionName);
      console.log(`Сессия '${sessionName}' завершена`);
      return;
    }

    if (!question && !dryRun) {
      console.error('Ошибка: нужен вопрос. ask-qwen.sh "вопрос"');
      process.exit(1);
    }

    diag = new Diagnostics({
      traceId: `tr-qwen-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      sessionName,
      promptPreview: question?.substring(0, 80) || '',
      logDir: path.join(BASE_DIR, '.diagnostics'),
    });
    diag.start('INIT');

    // Determine session
    let session = null;
    if (sessionName) {
      const isNew = !fs.existsSync(getSessionFile(sessionName));
      session = loadSession(sessionName);
      if (isNew) {
        session.created = new Date().toISOString();
        session.name = sessionName;
      }
      session.lastUsed = new Date().toISOString();
      saveSession(session.name, session);
    }

    // Ensure browser
    if (diag) diag.start('BROWSER_LAUNCH');
    const page = await ensureBrowser(session);
    if (diag) diag.succeed('BROWSER_LAUNCH');

    // New chat? Force a fresh chat for standalone requests so previous in-progress chats do not poison extraction.
    if (!session) {
      await startNewChat(page, true);
    } else if (newChat || !session.chatUrl) {
      await startNewChat(page);
    }

    // Wait for page ready
    if (diag) diag.start('COMPOSER_WAIT');
    const composerSel = await waitUntilReady(page);
    if (diag) diag.succeed('COMPOSER_WAIT', { selector: composerSel });

    // Auth check
    if (diag) diag.start('AUTH_CHECK');
    const authOk = await requireAuth(page, null, log);
    if (!authOk) {
      if (diag) diag.fail('AUTH_CHECK', 'Not authenticated');
      console.error('❌ Требуется авторизация в Qwen Chat');
      console.error('Запусти с --visible --wait для ручной авторизации');
      process.exit(1);
    }
    if (diag) diag.succeed('AUTH_CHECK');

    // Configure CDP interceptor before any prompt send.
    cdpInterceptor = await setupQwenInterceptor(page);

    // Dry run
    if (dryRun) {
      log('\n✅ Dry run успешен — Qwen Chat авторизован и готов');
      await cleanup();
      return;
    }

    // Force thinking mode before every prompt
    await ensureThinkingMode(page);

    // Enable search
    if (doSearch) await enableWebSearch(page);

    const fullQuestion = question.startsWith('[Дата:') ? question : `[Дата: ${new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Irkutsk' })}]\n\n${question}`;

    // Send prompt
    if (diag) diag.start('PROMPT_SEND');
    await sendPrompt(page, composerSel, fullQuestion);
    if (diag) diag.succeed('PROMPT_SEND');

    // Wait for response
    if (diag) diag.start('ANSWER_WAIT');
    const result = await waitForAnswer(page);
    if (diag) diag.succeed('ANSWER_WAIT', { chars: result?.text?.length || 0 });

    // Extract from DOM as fallback
    if (!result?.text && !result?.complete) {
      if (diag) diag.start('ANSWER_EXTRACT');
      const domText = await extractAnswerFromDOM(page, 20);
      if (domText) {
        result.text = domText;
        result.complete = true;
        if (diag) diag.succeed('ANSWER_EXTRACT', { chars: domText.length });
      } else {
        if (diag) diag.fail('ANSWER_EXTRACT', 'No text found in DOM');
      }
    }

    // Output response
    if (result?.text) {
      console.log(`\n═══════════════════════════════════════════`);
      console.log(result.text);
      console.log(`═══════════════════════════════════════════\n`);
      console.log(`📦 Ответ: ${result.text.length} символов`);
      console.log(`✅ Статус: ${result.complete ? 'полный' : 'может быть неполный'}`);
    } else {
      console.error('\n⚠️ Ответ не получен');
      // Dump page content for debugging
      try {
        const url = page.url();
        console.error(`📍 URL: ${url}`);
        const title = await page.title();
        console.error(`📄 Title: ${title}`);
      } catch {}
    }

    // Save session
    if (session) {
      try { session.chatUrl = page.url(); } catch {}
      session.messageCount = (session.messageCount || 0) + 2;
      saveSession(session.name, session);
    }

    if (diag) {
      diag.printSummary(result?.text?.length || 0);
      diag.save();
    }

  } catch (err) {
    console.error(`\n❌ Ошибка: ${err.message}`);
    if (diag) { diag.fail('INIT', err.message); diag.printSummary(0); diag.save(); }
    debugLog(err.stack);
    process.exit(1);
  } finally {
    if (browser) {
      const shouldCleanup = useDaemon || shouldClose || !sessionName || dryRun;
      if (shouldCleanup) {
        await cleanup();
      }
    }
  }
}

main().catch(err => { console.error('Fatal:', err.message); process.exit(1); });
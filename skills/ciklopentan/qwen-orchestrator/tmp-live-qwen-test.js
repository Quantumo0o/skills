const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const BASE = __dirname;
const WS_FILE = path.join(BASE, '.daemon-ws-endpoint');
const LOG_PREFIX = '[qwen-live-test]';

function log(...args) {
  console.log(LOG_PREFIX, ...args);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getBrowserPage() {
  const ws = fs.readFileSync(WS_FILE, 'utf8').trim();
  const browser = await puppeteer.connect({ browserWSEndpoint: ws, defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => {
    try { return p.url().includes('chat.qwen.ai'); } catch { return false; }
  }) || pages[0];
  return { browser, page };
}

async function ensureThinkingMode(page) {
  const readModeInfo = async () => {
    return page.evaluate(() => {
      const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
      const input = document.querySelector('.qwen-thinking-selector input[role="combobox"]');
      return {
        exists: !!label,
        current: label ? (label.textContent || '').trim() : '',
        expanded: input ? input.getAttribute('aria-expanded') : null,
      };
    }).catch(() => ({ exists: false, current: '', expanded: null }));
  };

  const modeInfo = await readModeInfo();
  log('mode current =', modeInfo.current || '(none)');
  if (!modeInfo.exists) return { ok: false, reason: 'no-selector' };
  if (/размыш|мышлен|think|reason/i.test(modeInfo.current)) return { ok: true, current: modeInfo.current };

  const triggerSelectors = [
    '.qwen-thinking-selector .ant-select-selector',
    '.qwen-thinking-selector .qwen-select-thinking-label',
    '.qwen-thinking-selector input[role="combobox"]',
    '.qwen-thinking-selector',
  ];

  let opened = false;
  for (const selector of triggerSelectors) {
    const handle = await page.$(selector).catch(() => null);
    if (!handle) continue;

    try {
      await handle.click({ delay: 50 });
      await sleep(250);
    } catch {}

    try {
      await handle.focus();
      await page.keyboard.press('Enter');
      await sleep(250);
    } catch {}

    try {
      await handle.focus();
      await page.keyboard.press('ArrowDown');
      await sleep(250);
    } catch {}

    const probe = await readModeInfo();
    if (probe.expanded === 'true') {
      opened = true;
      break;
    }
  }

  if (!opened) {
    return { ok: false, current: modeInfo.current, changed: { ok: false, reason: 'not-opened' } };
  }

  const pickedByText = await page.evaluate(() => {
    const matcher = /(размыш|мышлен|think|thinking|reason)/i;
    const candidates = Array.from(document.querySelectorAll('[role="option"], .ant-select-item-option, .ant-select-dropdown .ant-select-item, .ant-select-dropdown li, .ant-select-dropdown div'));
    const option = candidates.find((el) => {
      const text = (el.innerText || el.textContent || '').trim();
      if (!text) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0) return false;
      return matcher.test(text);
    });
    if (!option) return { ok: false };
    option.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
    option.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
    option.click();
    return { ok: true, text: (option.innerText || option.textContent || '').trim() };
  }).catch(() => ({ ok: false }));

  if (!pickedByText.ok) {
    for (let i = 0; i < 6; i++) {
      await page.keyboard.press('ArrowDown').catch(() => {});
      await sleep(120);
      await page.keyboard.press('Enter').catch(() => {});
      await sleep(350);
      const probe = await readModeInfo();
      if (/размыш|мышлен|think|reason/i.test(probe.current)) {
        return { ok: true, current: probe.current, changed: { ok: true, method: 'keyboard-fallback' } };
      }
      const reopenProbe = await readModeInfo();
      if (reopenProbe.expanded !== 'true') {
        for (const selector of triggerSelectors) {
          const handle = await page.$(selector).catch(() => null);
          if (!handle) continue;
          try {
            await handle.click({ delay: 30 });
            await sleep(150);
          } catch {}
          const after = await readModeInfo();
          if (after.expanded === 'true') break;
        }
      }
    }
  }

  await sleep(700);
  const finalLabel = await page.evaluate(() => {
    const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
    return label ? (label.textContent || '').trim() : '';
  }).catch(() => '');

  return {
    ok: /размыш|мышлен|think|reason/i.test(finalLabel),
    current: finalLabel,
    changed: pickedByText,
  };
}

async function startNewChat(page) {
  await page.goto('https://chat.qwen.ai/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(1500);
}

async function waitForComposer(page) {
  const selectors = ['#chat-input', 'textarea#chat-input', 'textarea[placeholder]', 'textarea'];
  const start = Date.now();
  while (Date.now() - start < 30000) {
    for (const sel of selectors) {
      const found = await page.$(sel);
      if (found) return sel;
    }
    await sleep(500);
  }
  throw new Error('composer not found');
}

async function sendPrompt(page, selector, prompt) {
  await page.evaluate(({ selector, prompt }) => {
    const el = document.querySelector(selector);
    if (!el) throw new Error('composer missing');
    el.focus();
    if (el instanceof HTMLTextAreaElement || el instanceof HTMLInputElement) {
      const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
      if (setter) setter.call(el, prompt); else el.value = prompt;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      el.textContent = prompt;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }

    const ev = { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true };
    el.dispatchEvent(new KeyboardEvent('keydown', ev));
    el.dispatchEvent(new KeyboardEvent('keypress', ev));
    el.dispatchEvent(new KeyboardEvent('keyup', ev));

    const sendBtn = document.querySelector('.send-button:not(.disabled), button[type="submit"], button[aria-label*="send" i]');
    if (sendBtn && !sendBtn.disabled) sendBtn.click();
  }, { selector, prompt });
}

async function getLastAssistantText(page) {
  return page.evaluate(() => {
    const candidates = [
      ...document.querySelectorAll('div[class*="markdown-body" i]'),
      ...document.querySelectorAll('div[class*="md-preview" i]'),
      ...document.querySelectorAll('div[class*="message-content" i]'),
      ...document.querySelectorAll('article'),
      ...document.querySelectorAll('.prose'),
    ];

    let best = '';
    for (const el of candidates) {
      if (el.closest('textarea, [contenteditable], [role="textbox"], .sidebar, nav, aside')) continue;
      const txt = (el.innerText || '').trim();
      if (txt.length > best.length) best = txt;
    }
    return best;
  });
}

async function clickContinueIfPresent(page) {
  const result = await page.evaluate(() => {
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
    btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
    btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
    btn.click();
    return { clicked: true, text };
  });
  return result;
}

async function waitForStableAnswer(page, { timeoutMs = 240000, stableMs = 6000 } = {}) {
  const start = Date.now();
  let best = '';
  let lastGrowth = Date.now();
  let continueClicks = 0;
  let continueSeen = [];

  while (Date.now() - start < timeoutMs) {
    const current = await getLastAssistantText(page);
    if (current.length > best.length) {
      best = current;
      lastGrowth = Date.now();
      log('answer grew to', best.length, 'chars');
    }

    const clicked = await clickContinueIfPresent(page);
    if (clicked.clicked) {
      continueClicks += 1;
      continueSeen.push(clicked.text);
      log('clicked continue button:', clicked.text);
      lastGrowth = Date.now();
      await sleep(2500);
      continue;
    }

    const isGenerating = await page.evaluate(() => {
      return !!(
        document.querySelector('[class*="stop" i]') ||
        document.querySelector('[class*="loading" i]') ||
        document.querySelector('[class*="generating" i]') ||
        document.querySelector('[class*="thinking" i]')
      );
    }).catch(() => false);

    if (best.length > 0 && !isGenerating && Date.now() - lastGrowth > stableMs) {
      return { text: best, continueClicks, continueSeen, timedOut: false };
    }

    await sleep(1500);
  }

  return { text: best, continueClicks, continueSeen, timedOut: true };
}

async function runTest(name, prompt, options = {}) {
  const { browser, page } = await getBrowserPage();
  try {
    log('---');
    log('test start:', name);
    await startNewChat(page);
    const thinking = await ensureThinkingMode(page);
    log('thinking result:', JSON.stringify(thinking));
    const composer = await waitForComposer(page);
    await sendPrompt(page, composer, prompt);
    const answer = await waitForStableAnswer(page, options);

    return {
      name,
      promptLength: prompt.length,
      answerLength: answer.text.length,
      timedOut: answer.timedOut,
      continueClicks: answer.continueClicks,
      continueSeen: answer.continueSeen,
      preview: answer.text.slice(0, 500),
      tail: answer.text.slice(-500),
    };
  } finally {
    await browser.disconnect();
  }
}

(async () => {
  const tests = [
    {
      name: 'short',
      prompt: 'Ответь только двумя словами: Привет мир',
      options: { timeoutMs: 90000, stableMs: 5000 },
    },
    {
      name: 'medium',
      prompt: 'Кратко, но содержательно объясни разницу между systemd, cron и PM2 для Linux-сервера. Дай структурированный ответ на 5–7 абзацев и в конце короткую рекомендацию, что для чего лучше использовать.',
      options: { timeoutMs: 150000, stableMs: 7000 },
    },
    {
      name: 'long',
      prompt: 'Сделай максимально длинный и подробный технический ответ на русском языке по теме: "Практическое проектирование надёжной локальной AI-автоматизации без API-ключей через браузерные оркестраторы". Нужны разделы: архитектура, daemon-mode, профили браузера, авторизация, DOM-устойчивость, сетевые перехваты, восстановление после сбоев, rate limiting, сессионность, диагностика, безопасность, anti-patterns, пошаговый production-checklist, таблицы сравнений, примеры команд, и в конце большой чеклист аудита. Не экономь текст. Если ответ упрётся в лимит, продолжай через кнопку continue/continue generating, если она доступна. Пиши максимально длинно.',
      options: { timeoutMs: 360000, stableMs: 12000 },
    },
  ];

  const results = [];
  for (const test of tests) {
    results.push(await runTest(test.name, test.prompt, test.options));
  }

  console.log(JSON.stringify({ ok: true, results }, null, 2));
})();

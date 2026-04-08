const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const ws = fs.readFileSync(path.join(__dirname, '.daemon-ws-endpoint'), 'utf8').trim();
  const browser = await puppeteer.connect({ browserWSEndpoint: ws, defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => { try { return p.url().includes('chat.qwen.ai'); } catch { return false; } }) || pages[0];

  await page.goto('https://chat.qwen.ai/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));

  const before = await page.evaluate(() => {
    const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
    return label ? label.textContent.trim() : null;
  });
  console.log('before =', before);

  const trigger = await page.$('.qwen-thinking-selector .ant-select-selector');
  if (!trigger) throw new Error('no trigger');
  await trigger.click({ delay: 50 });
  await new Promise(r => setTimeout(r, 1200));

  const bodyDump = await page.evaluate(() => {
    const texts = [];
    const all = Array.from(document.querySelectorAll('body *'));
    for (const el of all) {
      const txt = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
      if (!txt) continue;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0) continue;
      if (/автомат|быстр|размыш|мышл|think|reason/i.test(txt)) {
        texts.push({
          tag: el.tagName,
          text: txt,
          cls: (el.className || '').toString(),
          role: el.getAttribute('role') || '',
          x: Math.round(r.x),
          y: Math.round(r.y),
          outer: el.outerHTML.slice(0, 250),
        });
      }
    }
    return texts.slice(0, 120);
  });

  console.log(JSON.stringify(bodyDump, null, 2));
  await browser.disconnect();
})();

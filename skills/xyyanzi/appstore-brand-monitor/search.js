#!/usr/bin/env node
/**
 * search.js — App Store 候选应用查询脚本
 *
 * 职责：
 *   1. 调用 iTunes Search API 搜索关键词
 *   2. 过滤白名单中的正版官方应用
 *   3. 过滤已在 alerted.json 中记录过的应用（去重）
 *   4. 输出候选应用列表（JSON），供 agent 做 AI 判断
 *
 * 不做：浏览器操作、截图、AI 模型调用、Lark 发送
 *
 * 用法：
 *   node search.js --country ph --keyword Atome
 *   node search.js --country ph --keyword Atome --limit 50 --skip-alerted false
 */

const argv = require('yargs')
  .option('country', { alias: 'c', type: 'string', demandOption: true, description: 'Country code (ph/sg/my/id/th)' })
  .option('keyword', { alias: 'k', type: 'string', demandOption: true, description: 'Brand keyword to search' })
  .option('limit',   { alias: 'l', type: 'number', default: 50, description: 'Max results from iTunes API' })
  .option('skip-alerted', { type: 'boolean', default: true, description: 'Skip apps already in alerted.json' })
  .help()
  .argv;

const fs   = require('fs');
const path = require('path');

const SKILL_DIR   = __dirname;
const ALERTED_FILE = path.join(SKILL_DIR, 'alerted.json');

// ─── 白名单（正版官方应用）────────────────────────────────────────
const WHITELIST = [
  { appId: 1577294865, country: 'ph' },
  { appId: 1491428868, country: 'sg' },
  { appId: 1533642823, country: 'my' },
  { appId: 1560108683, country: 'id' },
  { appId: 1563893540, country: 'th' },
];

function isWhitelisted(appId, country) {
  return WHITELIST.some(w => String(w.appId) === String(appId) && w.country === country);
}

// ─── 加载已告警记录 ────────────────────────────────────────────────
function loadAlerted() {
  try {
    if (fs.existsSync(ALERTED_FILE)) {
      return JSON.parse(fs.readFileSync(ALERTED_FILE, 'utf8'));
    }
  } catch (e) {
    // 读取失败时忽略，当作空记录
  }
  return {};
}

function isAlerted(appId) {
  const alerted = loadAlerted();
  return !!alerted[String(appId)];
}

// ─── 主流程 ────────────────────────────────────────────────────────
async function main() {
  const country = argv.country.toLowerCase();
  const keyword = argv.keyword;

  console.error(`🔍 搜索 ${country.toUpperCase()} 地区 App Store，关键词："${keyword}"`);

  // iTunes Search API（带重试）
  const searchUrl = `https://itunes.apple.com/search?term=${encodeURIComponent(keyword)}&country=${country}&entity=software&limit=${argv.limit}`;
  let data;
  for (let retry = 0; retry < 3; retry++) {
    try {
      const controller = new AbortController();
      const tid = setTimeout(() => controller.abort(), 30000);
      const resp = await fetch(searchUrl, { signal: controller.signal });
      clearTimeout(tid);
      data = await resp.json();
      break;
    } catch (e) {
      if (retry === 2) {
        console.error(`❌ iTunes 搜索失败：${e.message}`);
        process.exit(1);
      }
      console.error(`⚠️  第 ${retry + 1} 次重试...`);
      await new Promise(r => setTimeout(r, 2000 * (retry + 1)));
    }
  }

  if (!data.results || data.results.length === 0) {
    console.error('✅ 未搜索到相关应用');
    console.log(JSON.stringify({ total: 0, whitelisted: 0, alreadyAlerted: 0, candidates: [] }));
    return;
  }

  // 格式化
  const allResults = data.results.map(app => ({
    appId:       String(app.trackId),
    title:       app.trackName,
    developer:   app.artistName,
    url:         app.trackViewUrl,
    icon:        app.artworkUrl512 || app.artworkUrl100,
    score:       (app.averageUserRating || 0).toFixed(1),
    reviews:     app.userRatingCount || 0,
    description: (app.description || '').slice(0, 500), // 只取前500字节给 agent 判断
  }));

  // 过滤白名单
  const whitelisted = allResults.filter(a => isWhitelisted(a.appId, country));
  const nonWhitelisted = allResults.filter(a => !isWhitelisted(a.appId, country));

  // 预筛选：名称或描述中含有关键词（大小写不敏感），减少 AI 判断量
  const keywordLower = keyword.toLowerCase();
  const preFiltered = nonWhitelisted.filter(a =>
    a.title.toLowerCase().includes(keywordLower) ||
    a.description.toLowerCase().includes(keywordLower)
  );

  // 过滤已告警
  const alreadyAlerted = argv['skip-alerted']
    ? preFiltered.filter(a => isAlerted(a.appId))
    : [];
  const candidates = argv['skip-alerted']
    ? preFiltered.filter(a => !isAlerted(a.appId))
    : preFiltered;

  console.error(`✅ 共 ${allResults.length} 个应用，白名单 ${whitelisted.length} 个，已告警跳过 ${alreadyAlerted.length} 个，待检测 ${candidates.length} 个`);

  // 输出 JSON 供 agent 使用
  console.log(JSON.stringify({
    country,
    keyword,
    total:          allResults.length,
    whitelisted:    whitelisted.length,
    alreadyAlerted: alreadyAlerted.length,
    candidates
  }, null, 2));
}

main().catch(e => {
  console.error('❌', e.message);
  process.exit(1);
});

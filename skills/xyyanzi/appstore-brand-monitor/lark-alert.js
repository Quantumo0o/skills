#!/usr/bin/env node
/**
 * lark-alert.js — Lark 告警发送脚本
 *
 * 职责：
 *   1. 接收高风险应用列表（JSON 文件路径或 stdin）
 *   2. 上传截图到 Lark
 *   3. 发送 Lark 卡片告警
 *   4. 写入 alerted.json 记录（去重用）
 *
 * 不做：AI 判断、浏览器操作、模型调用
 *
 * 用法：
 *   node lark-alert.js --input /path/to/highrisk.json
 *   echo '<json>' | node lark-alert.js --stdin
 *   node lark-alert.js --input /path/to/highrisk.json --receiver ou_xxx
 *
 * highrisk.json 格式：
 *   {
 *     "country": "ph",
 *     "keyword": "Atome",
 *     "scanTime": "2026-03-26T08:00:00Z",
 *     "total": 39,
 *     "candidates": [...],   // 全量候选（用于报告列表）
 *     "highRisk": [
 *       {
 *         "appId": "123456",
 *         "title": "Fake Atome",
 *         "developer": "Some Dev",
 *         "url": "https://...",
 *         "icon": "https://...",
 *         "score": "4.2",
 *         "reviews": 100,
 *         "hitRules": ["名称与「Atome」高度相似（95分）", "描述包含「Atome」"],
 *         "totalScore": 175,
 *         "screenshotPath": "/absolute/path/to/screenshot.png"  // 可选
 *       }
 *     ]
 *   }
 */

require('dotenv').config();
const fs   = require('fs');
const path = require('path');
const argv = require('yargs')
  .option('input',    { type: 'string', description: 'Path to high-risk JSON file' })
  .option('stdin',    { type: 'boolean', default: false, description: 'Read JSON from stdin' })
  .option('receiver', { type: 'string', default: null, description: 'Override Lark recipient ID' })
  .option('no-dedup', { type: 'boolean', default: false, description: 'Skip writing to alerted.json' })
  .help()
  .argv;

const SKILL_DIR    = __dirname;
const ALERTED_FILE = path.join(SKILL_DIR, 'alerted.json');
const LARK_API_BASE = 'https://open.larksuite.com/open-apis';

const CONFIG = {
  LARK_APP_ID:      process.env.LARK_APP_ID,
  LARK_APP_SECRET:  process.env.LARK_APP_SECRET,
  ALERT_RECEIVER_ID: process.env.ALERT_RECEIVER_ID,
};

if (!CONFIG.LARK_APP_ID || !CONFIG.LARK_APP_SECRET) {
  console.error('❌ 缺少 LARK_APP_ID / LARK_APP_SECRET，请检查 .env 文件');
  process.exit(1);
}

// ─── Lark Token ────────────────────────────────────────────────────
let _tokenCache = null;
let _tokenExpire = 0;

async function getLarkToken() {
  const now = Date.now() / 1000;
  if (_tokenCache && _tokenExpire > now) return _tokenCache;
  const res = await fetch(`${LARK_API_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: CONFIG.LARK_APP_ID, app_secret: CONFIG.LARK_APP_SECRET }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Lark token 获取失败: ${data.msg}`);
  _tokenCache  = data.tenant_access_token;
  _tokenExpire = now + data.expire - 60;
  return _tokenCache;
}

// ─── 上传图片 ──────────────────────────────────────────────────────
async function uploadImage(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return null;
  const token = await getLarkToken();
  const { FormData, Blob } = require('node:buffer') ? global : await import('node:buffer');
  // Node 18+ 内置 FormData
  const formData = new globalThis.FormData();
  formData.append('image_type', 'message');
  const buf = fs.readFileSync(filePath);
  formData.append('image', new Blob([buf], { type: 'image/png' }), path.basename(filePath));
  const res = await fetch(`${LARK_API_BASE}/im/v1/images`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData,
  });
  const data = await res.json();
  if (data.code !== 0) {
    console.error(`⚠️  图片上传失败: ${data.msg}`);
    return null;
  }
  return data.data.image_key;
}

// ─── 发送 Lark 卡片 ────────────────────────────────────────────────
async function sendLarkCard(report) {
  const token    = await getLarkToken();
  const targetId = argv.receiver || CONFIG.ALERT_RECEIVER_ID;
  if (!targetId) {
    console.error('❌ 未指定告警接收人，请传入 --receiver 或在 .env 配置 ALERT_RECEIVER_ID');
    return false;
  }
  const receiveIdType = targetId.startsWith('ou_') ? 'open_id' : 'chat_id';

  const { country, keyword, total, candidates = [], highRisk = [], scanTime } = report;
  const timeStr = scanTime
    ? new Date(scanTime).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })
    : new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

  const hasRisk  = highRisk.length > 0;
  const title    = hasRisk ? '⚠️ App Store 品牌仿冒告警' : '✅ App Store 品牌监控扫描报告';
  const summary  = `扫描地区：${country.toUpperCase()}｜关键词：${keyword}｜时间：${timeStr}\n共扫描 ${total} 个相关应用，发现 **${highRisk.length} 个高风险仿冒应用**`;

  const elements = [
    { tag: 'markdown', content: `## ${title}\n${summary}` },
    { tag: 'hr' },
  ];

  if (hasRisk) {
    for (let i = 0; i < highRisk.length; i++) {
      const app = highRisk[i];
      if (i > 0) elements.push({ tag: 'hr' });
      elements.push({
        tag: 'markdown',
        content: [
          `**🚨 ${i + 1}. ${app.title}**`,
          `**开发商：** ${app.developer}`,
          `⭐ ${app.score}（${app.reviews} 条评价）｜**风险评分：** ${app.totalScore} 分`,
          ``,
          `**命中规则：**`,
          ...(app.hitRules || []).map(r => `✅ ${r}`),
          ``,
          `**链接：** [→ App Store](${app.url})`,
        ].join('\n'),
      });
      // 截图（如有）
      if (app.imageKey) {
        elements.push({ tag: 'markdown', content: '**详情页截图：**' });
        elements.push({
          tag: 'img',
          img_key: app.imageKey,
          alt: { tag: 'plain_text', content: `${app.title} 截图` },
        });
      }
    }
  } else {
    elements.push({ tag: 'markdown', content: '✅ 未发现高风险仿冒应用' });
  }

  const card = { schema: '2.0', body: { elements } };
  const res  = await fetch(`${LARK_API_BASE}/im/v1/messages?receive_id_type=${receiveIdType}`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      receive_id: targetId,
      msg_type:   'interactive',
      content:    JSON.stringify(card),
    }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`发送卡片失败: ${JSON.stringify(data)}`);
  console.log(`✅ Lark 告警发送成功，消息 ID: ${data.data.message_id}`);
  return data.data.message_id;
}

// ─── 写入 alerted.json ─────────────────────────────────────────────
function writeAlerted(highRisk, country) {
  let alerted = {};
  try {
    if (fs.existsSync(ALERTED_FILE)) {
      alerted = JSON.parse(fs.readFileSync(ALERTED_FILE, 'utf8'));
    }
  } catch {}
  for (const app of highRisk) {
    alerted[String(app.appId)] = {
      title:     app.title,
      country,
      alertedAt: new Date().toISOString(),
    };
  }
  fs.writeFileSync(ALERTED_FILE, JSON.stringify(alerted, null, 2), 'utf8');
  console.log(`✅ 已更新 alerted.json，新增 ${highRisk.length} 条记录`);
}

// ─── 主流程 ────────────────────────────────────────────────────────
async function main() {
  // 读取输入
  let report;
  if (argv.stdin) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    report = JSON.parse(Buffer.concat(chunks).toString());
  } else if (argv.input) {
    report = JSON.parse(fs.readFileSync(argv.input, 'utf8'));
  } else {
    console.error('❌ 请指定 --input <file> 或 --stdin');
    process.exit(1);
  }

  const { highRisk = [], country } = report;

  // 上传截图
  if (highRisk.length > 0) {
    console.log(`📤 正在上传 ${highRisk.length} 个高风险应用的截图...`);
    for (const app of highRisk) {
      if (app.screenshotPath) {
        app.imageKey = await uploadImage(app.screenshotPath);
        if (app.imageKey) {
          console.log(`   ✅ ${app.title} 截图上传成功`);
        } else {
          console.log(`   ⚠️  ${app.title} 截图上传失败，将跳过图片`);
        }
      }
    }
  }

  // 发送卡片
  console.log('📤 正在发送 Lark 告警卡片...');
  await sendLarkCard(report);

  // 写入去重记录
  if (!argv['no-dedup'] && highRisk.length > 0) {
    writeAlerted(highRisk, country);
  }
}

main().catch(e => {
  console.error('❌ 执行失败:', e.message);
  process.exit(1);
});

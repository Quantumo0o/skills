#!/usr/bin/env node
/**
 * ES Poll Feishu
 * 轮询 Elasticsearch 新数据 → 飞书推送
 * 
 * 版本号从 package.json 读取
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const os = require('os');

const pkg = require('../package.json');
const VERSION = pkg.version;

// ============ 路径 ============
const CONFIG_PATH = path.join(os.homedir(), '.openclaw', 'es-poll-feishu.json');
const DATA_DIR = path.join(os.homedir(), 'clawd', 'data', 'es-poll-feishu');
const PID_FILE = path.join(DATA_DIR, 'poller.pid');
const LOG_FILE = path.join(DATA_DIR, 'poller.log');
const STATS_FILE = path.join(DATA_DIR, 'stats.json');
const CURSOR_FILE = path.join(DATA_DIR, 'cursor.json');

// ============ 默认配置 ============
const DEFAULT_CONFIG = {
  // ES 连接
  es_url: '',               // 必填，如 http://your-es-host:9200
  es_index: '',             // 必填，如 xgks_*（支持 {yyyyMM} 占位符自动替换为当前年月，如 xgks_{yyyyMM}*）
  es_auth: '',              // 必填，Basic auth 字符串（base64）
  es_params: {},            // URL 附加参数，如 { "app_customer_name": "11", "app_user_name": "22" }

  // ES 查询
  es_query: null,           // 自定义查询体（完整 query 对象），为 null 则使用默认的时间范围查询
  es_time_field: 'ctime',   // 时间字段名，用于增量轮询
  es_sort_field: 'ctime',   // 排序字段
  es_size: 50,              // 每次拉取条数
  es_tiebreaker_field: '_doc', // search_after tiebreaker 字段（_doc 为 ES 内部文档顺序，无需 fielddata）
  es_max_pages: 20,         // 单次轮询最大翻页数（防止无限循环），0=不限

  // 轮询
  poll_interval: 60,        // 轮询间隔（秒）

  // 飞书
  feishu_app_id: '',        // 必填
  feishu_app_secret: '',    // 必填
  feishu_user_id: '',       // 必填，open_id

  // 雪崩保护
  flood_threshold: 5000,    // 单次轮询命中超过此数量，触发雪崩保护（只发告警，不逐条推）
  flood_cooldown: 300,      // 雪崩告警冷却时间（秒），避免重复告警刷屏
  push_rate_limit: 3,       // 推送限速（条/秒），飞书同用户上限 5 QPS，留余量

  // 消息格式
  title_field: 'title',     // 标题字段路径
  content_field: 'content', // 内容字段路径
  url_field: 'url',         // 链接字段路径
};

let config = { ...DEFAULT_CONFIG };

// ============ 配置加载 ============
function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在:', CONFIG_PATH);
    console.error('请先运行: es-poll-feishu config');
    process.exit(1);
  }

  // 检查配置文件权限，仅允许 owner 读写（防止同机其他用户读取敏感凭据）
  try {
    const stat = fs.statSync(CONFIG_PATH);
    const mode = stat.mode & 0o777;
    if (mode & 0o077) {
      console.error(`⚠️ 配置文件权限过宽 (${mode.toString(8)})，正在修正为 600...`);
      fs.chmodSync(CONFIG_PATH, 0o600);
    }
  } catch (_) {}

  try {
    const fileConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    config = { ...DEFAULT_CONFIG, ...fileConfig };
  } catch (e) {
    console.error('❌ 配置文件解析失败:', e.message);
    process.exit(1);
  }
  const required = ['es_url', 'es_index', 'es_auth', 'feishu_app_id', 'feishu_app_secret', 'feishu_user_id'];
  const missing = required.filter(k => !config[k]);
  if (missing.length > 0) {
    console.error('❌ 缺少必填配置:', missing.join(', '));
    process.exit(1);
  }
}

// ============ 日志 ============
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

const MAX_LOG_SIZE = 10 * 1024 * 1024; // 10MB
let _logLineCount = 0; // 每 100 行检查一次文件大小，减少 statSync 开销

function rotateLogIfNeeded() {
  try {
    if (!fs.existsSync(LOG_FILE)) return;
    const stat = fs.statSync(LOG_FILE);
    if (stat.size > MAX_LOG_SIZE) {
      const backupPath = LOG_FILE + '.1';
      if (fs.existsSync(backupPath)) fs.unlinkSync(backupPath);
      fs.renameSync(LOG_FILE, backupPath);
    }
  } catch (_) {}
}

function log(msg) {
  const line = `${new Date().toISOString()} - ${msg}`;
  try {
    // 每 100 行检查一次日志大小，避免每次写入都 statSync
    if (++_logLineCount % 100 === 0) rotateLogIfNeeded();
    fs.appendFileSync(LOG_FILE, line + '\n');
  } catch (_) {}
}

// ============ PID 管理 ============
function writePid() {
  // 写入 PID 和启动时间戳，防止 PID 复用误判
  const data = { pid: process.pid, startedAt: Date.now() };
  fs.writeFileSync(PID_FILE, JSON.stringify(data));
  log(`PID ${process.pid} written`);
}

function removePid() {
  try { if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE); } catch (_) {}
}

function isAlreadyRunning() {
  if (!fs.existsSync(PID_FILE)) return false;
  try {
    const raw = fs.readFileSync(PID_FILE, 'utf-8').trim();
    let pid, startedAt;
    // 兼容旧格式（纯数字）和新格式（JSON）
    if (raw.startsWith('{')) {
      const data = JSON.parse(raw);
      pid = data.pid;
      startedAt = data.startedAt;
    } else {
      pid = parseInt(raw);
      startedAt = null;
    }
    // 检查进程是否存在
    process.kill(pid, 0);
    // 进程存在，再校验启动时间（如果有）
    if (startedAt) {
      // 通过 /proc 或 ps 获取进程启动时间比较复杂，这里用简化方案：
      // 如果 PID 文件的启动时间超过 30 天，认为是 PID 复用，清理掉
      const ageMs = Date.now() - startedAt;
      if (ageMs > 30 * 24 * 60 * 60 * 1000) {
        log(`⚠️ PID 文件过旧 (${Math.round(ageMs / 86400000)} 天)，可能是 PID 复用，清理`);
        removePid();
        return false;
      }
    }
    return true;
  } catch (_) {
    removePid();
    return false;
  }
}

// ============ 统计 & 游标 ============
// 游标格式 v1.1: { searchAfter: [timestampValue, tiebreakerValue], lastTimestamp: number }
// 兼容 v1.0: { lastTimestamp: number } — 加载时自动迁移
let stats = { totalPolled: 0, totalPushed: 0, totalHits: 0, lastPollTime: null };
let cursor = { searchAfter: null, lastTimestamp: null };

function loadStats() {
  try { if (fs.existsSync(STATS_FILE)) stats = JSON.parse(fs.readFileSync(STATS_FILE, 'utf-8')); } catch (_) {}
}
function saveStats() {
  stats.lastUpdate = new Date().toISOString();
  // 原子写入，和 saveCursor 一致，防止写入中途崩溃导致文件损坏
  const tmpFile = STATS_FILE + '.tmp';
  try {
    fs.writeFileSync(tmpFile, JSON.stringify(stats, null, 2));
    fs.renameSync(tmpFile, STATS_FILE);
  } catch (_) {}
}
function loadCursor() {
  try {
    if (fs.existsSync(CURSOR_FILE)) {
      const raw = JSON.parse(fs.readFileSync(CURSOR_FILE, 'utf-8'));
      if (raw.searchAfter) {
        // v1.1 格式
        cursor = raw;
      } else if (raw.lastTimestamp != null) {
        // v1.0 旧格式迁移：只有 lastTimestamp，没有 tiebreaker，用 null 占位
        // 首次 search_after 查询时会用 gte + 时间范围兜底，不会丢数据
        log('📌 检测到 v1.0 游标格式，自动迁移为 v1.1 (search_after)');
        cursor = { searchAfter: [raw.lastTimestamp, null], lastTimestamp: raw.lastTimestamp };
      }
    }
  } catch (_) {}
}
function saveCursor() {
  // 原子写入：先写临时文件再 rename，防止写入中途崩溃导致游标文件损坏
  const tmpFile = CURSOR_FILE + '.tmp';
  try {
    fs.writeFileSync(tmpFile, JSON.stringify(cursor, null, 2));
    fs.renameSync(tmpFile, CURSOR_FILE);
  } catch (_) {}
}

// ============ 嵌套字段取值 ============
function getNestedValue(obj, fieldPath) {
  return fieldPath.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : null), obj);
}

// ============ 索引名动态解析 ============
function resolveIndex() {
  const now = new Date();
  const yyyy = now.getFullYear().toString();
  const MM = (now.getMonth() + 1).toString().padStart(2, '0');
  return config.es_index
    .replace(/\{yyyyMM\}/g, `${yyyy}${MM}`)
    .replace(/\{yyyy\}/g, yyyy)
    .replace(/\{MM\}/g, MM);
}

// ============ 飞书 Token ============
let feishuAccessToken = '';
let feishuTokenExpiry = 0;

async function getFeishuToken() {
  if (feishuAccessToken && Date.now() < feishuTokenExpiry - 300000) {
    return feishuAccessToken;
  }
  try {
    const res = await axios.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', {
      app_id: config.feishu_app_id,
      app_secret: config.feishu_app_secret,
    });
    feishuAccessToken = res.data.app_access_token;
    feishuTokenExpiry = Date.now() + res.data.expire * 1000;
    log('✅ 飞书 Token 获取成功');
    return feishuAccessToken;
  } catch (err) {
    log('❌ 飞书 Token 获取失败: ' + err.message);
    return null;
  }
}

// ============ 发送飞书消息（带重试） ============
const FEISHU_MAX_RETRIES = 3;
const FEISHU_RETRY_DELAY_MS = 2000;

async function sendToFeishu(hit) {
  const source = hit._source || {};
  const title = getNestedValue(source, config.title_field) || '(无标题)';
  const content = getNestedValue(source, config.content_field) || '';
  const url = getNestedValue(source, config.url_field) || '';
  const timeVal = getNestedValue(source, config.es_time_field);
  const timeStr = timeVal ? new Date(timeVal * 1000).toLocaleString('zh-CN') : '';

  const text = `📢 新数据推送

【${title}】

${content.slice(0, 50)}${content.length > 50 ? '...' : ''}

${url ? '🔗 ' + url : ''}
${timeStr ? '🕐 ' + timeStr : ''}
📋 索引: ${hit._index || ''}`;

  for (let attempt = 1; attempt <= FEISHU_MAX_RETRIES; attempt++) {
    const token = await getFeishuToken();
    if (!token) {
      log(`❌ 推送失败: 无法获取飞书 Token (尝试 ${attempt}/${FEISHU_MAX_RETRIES})`);
      if (attempt < FEISHU_MAX_RETRIES) await sleep(FEISHU_RETRY_DELAY_MS);
      continue;
    }

    try {
      await axios.post(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        {
          receive_id: config.feishu_user_id,
          msg_type: 'text',
          content: JSON.stringify({ text }),
        },
        { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
      );
      log(`✅ 已推送: ${title.slice(0, 40)}`);
      return true;
    } catch (err) {
      log(`❌ 推送失败 (尝试 ${attempt}/${FEISHU_MAX_RETRIES}): ${err.message}`);
      if (err.response?.status === 401) {
        // Token 过期，清除缓存后重试时会自动重新获取
        feishuAccessToken = '';
        feishuTokenExpiry = 0;
      }
      if (attempt < FEISHU_MAX_RETRIES) await sleep(FEISHU_RETRY_DELAY_MS);
    }
  }
  return false;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============ 雪崩保护 ============
let lastFloodAlertTime = 0; // 上次雪崩告警时间戳（ms）

/**
 * 探测待处理数据总量（size:0 count 查询，不拉数据）
 * 用游标时间戳做 range 过滤，近似估算增量数据量（而非全量）
 * 返回 -1 表示查询失败
 */
async function countPending(url, baseQuery) {
  // 在 baseQuery 基础上加上游标时间范围，避免把历史全量数据算进去
  let countQuery = baseQuery;
  if (cursor.lastTimestamp != null) {
    countQuery = {
      bool: {
        must: [baseQuery],
        filter: [{ range: { [config.es_time_field]: { gt: cursor.lastTimestamp } } }],
      },
    };
  }
  const body = { size: 0, query: countQuery, track_total_hits: true };
  try {
    const res = await axios.post(url, body, {
      headers: { 'Content-Type': 'application/json', Authorization: `Basic ${config.es_auth}` },
      timeout: 15000,
    });
    return res.data?.hits?.total?.value ?? res.data?.hits?.total ?? -1;
  } catch (_) {
    return -1;
  }
}

/**
 * 发送雪崩告警到飞书（单条汇总消息）
 */
async function sendFloodAlert(pendingCount) {
  const now = Date.now();
  const cooldown = (config.flood_cooldown || 300) * 1000;
  if (now - lastFloodAlertTime < cooldown) {
    log(`🔇 雪崩告警冷却中 (${Math.round((cooldown - (now - lastFloodAlertTime)) / 1000)}s 后可再次告警)`);
    return;
  }

  const text = `🚨 数据雪崩告警

检测到待处理数据量异常：${pendingCount} 条
阈值：${config.flood_threshold} 条
时间：${new Date().toLocaleString('zh-CN')}

⚠️ 已自动暂停逐条推送，游标快进至最新位置。
疑似上游系统异常导致大量写入，请排查数据源。
恢复正常后，轮询将自动继续。`;

  const token = await getFeishuToken();
  if (!token) { log('❌ 雪崩告警发送失败: 无法获取飞书 Token'); return; }

  try {
    await axios.post(
      'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
      { receive_id: config.feishu_user_id, msg_type: 'text', content: JSON.stringify({ text }) },
      { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } }
    );
    lastFloodAlertTime = now;
    log(`🚨 雪崩告警已发送 (待处理: ${pendingCount})`);
  } catch (err) {
    log(`❌ 雪崩告警发送失败: ${err.message}`);
  }
}

/**
 * 雪崩时快进游标：跳到最新数据位置，不推送
 */
async function fastForwardCursor(url, baseQuery, tiebreakerField) {
  // 拉最新一条（倒序），用它的 sort 值作为新游标
  const sortDesc = [
    { [config.es_sort_field]: { order: 'desc' } },
    { [tiebreakerField]: { order: 'desc' } },
  ];
  try {
    const res = await axios.post(url, { size: 1, sort: sortDesc, query: baseQuery }, {
      headers: { 'Content-Type': 'application/json', Authorization: `Basic ${config.es_auth}` },
      timeout: 15000,
    });
    const hits = res.data?.hits?.hits || [];
    if (hits.length > 0 && hits[0].sort && hits[0].sort.length >= 2) {
      const oldCursor = cursor.searchAfter ? JSON.stringify(cursor.searchAfter) : 'null';
      cursor.searchAfter = hits[0].sort;
      const ts = getNestedValue(hits[0]._source || {}, config.es_time_field);
      if (ts) cursor.lastTimestamp = ts;
      saveCursor();
      log(`⏩ 游标快进: ${oldCursor} → ${JSON.stringify(cursor.searchAfter)}`);
      return true;
    }
  } catch (err) {
    log(`❌ 游标快进失败: ${err.message}`);
  }
  return false;
}

// ============ ES 查询（search_after 分页） ============
const MAX_ES_SIZE = 200; // es_size 上限，防止单页过大
const DEFAULT_MAX_PAGES = 20; // 单次轮询默认最大翻页数

async function pollES() {
  stats.totalPolled++;
  stats.lastPollTime = new Date().toISOString();

  const effectiveSize = Math.min(config.es_size, MAX_ES_SIZE);
  const maxPages = config.es_max_pages || DEFAULT_MAX_PAGES;
  const tiebreakerField = config.es_tiebreaker_field || '_id';

  // 首次运行标记：无游标时只初始化游标，不推送
  const isFirstRun = !cursor.searchAfter;

  // 构建基础查询（不含时间范围，时间范围由 search_after 的 sort 值隐式处理）
  let baseQuery;
  if (isFirstRun) {
    // 首次运行：拉最新一条初始化游标
    baseQuery = config.es_query || { match_all: {} };
  } else if (config.es_query) {
    // 有自定义查询：直接用，search_after 会自动跳过已处理的数据
    // 但如果是从 v1.0 迁移（tiebreaker 为 null），需要加时间范围兜底
    if (cursor.searchAfter[1] === null) {
      const must = [config.es_query];
      must.push({ range: { [config.es_time_field]: { gte: cursor.lastTimestamp } } });
      baseQuery = { bool: { must } };
    } else {
      baseQuery = config.es_query;
    }
  } else {
    // 无自定义查询：search_after 已经隐式过滤了旧数据
    if (cursor.searchAfter[1] === null) {
      // v1.0 迁移兜底
      baseQuery = { range: { [config.es_time_field]: { gte: cursor.lastTimestamp } } };
    } else {
      baseQuery = { match_all: {} };
    }
  }

  // sort 定义：主排序字段 + tiebreaker
  const sortDef = isFirstRun
    ? [{ [config.es_sort_field]: { order: 'desc' } }, { [tiebreakerField]: { order: 'desc' } }]
    : [{ [config.es_sort_field]: { order: 'asc' } }, { [tiebreakerField]: { order: 'asc' } }];

  // 构建 URL
  const params = new URLSearchParams(config.es_params || {});
  const index = resolveIndex();
  const url = `${config.es_url.replace(/\/+$/, '')}/${index}/_search?${params.toString()}`;

  if (isFirstRun) {
    log('📌 首次运行，仅拉取最新数据初始化游标');
    await pollFirstRun(url, baseQuery, sortDef, tiebreakerField);
    return;
  }

  // ---- 雪崩检测：先探测待处理数据量 ----
  const floodThreshold = config.flood_threshold || 500;
  const pendingCount = await countPending(url, baseQuery);
  if (pendingCount > floodThreshold) {
    log(`🚨 雪崩检测触发: 待处理 ${pendingCount} 条 > 阈值 ${floodThreshold}`);
    await sendFloodAlert(pendingCount);
    await fastForwardCursor(url, baseQuery, tiebreakerField);
    stats.totalHits += pendingCount;
    saveStats();
    return;
  } else if (pendingCount >= 0) {
    log(`📊 待处理数据量: ${pendingCount} (阈值: ${floodThreshold})`);
  }

  // ---- 推送限速参数 ----
  const pushRateLimit = config.push_rate_limit || 3;
  const pushIntervalMs = Math.ceil(1000 / pushRateLimit);

  // ---- 分页循环：持续拉取直到没有更多数据 ----
  let currentSearchAfter = cursor.searchAfter;
  let totalHitsThisRound = 0;
  let totalPushedThisRound = 0;
  let pageCount = 0;
  let pushFailed = false;

  while (true) {
    pageCount++;
    if (maxPages > 0 && pageCount > maxPages) {
      log(`⚠️ 达到单次轮询最大翻页数 (${maxPages})，剩余数据下次轮询继续`);
      break;
    }

    const body = { size: effectiveSize, sort: sortDef, query: baseQuery };

    // search_after：跳过已处理的数据（v1.0 迁移时 tiebreaker 为 null，不传 search_after，靠时间范围兜底）
    if (currentSearchAfter && currentSearchAfter[1] !== null) {
      body.search_after = currentSearchAfter;
    }

    try {
      const res = await axios.post(url, body, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Basic ${config.es_auth}`,
        },
        timeout: 30000,
      });

      const hits = res.data?.hits?.hits || [];

      if (hits.length === 0) {
        break; // 没有更多数据了
      }

      totalHitsThisRound += hits.length;
      stats.totalHits += hits.length;

      log(`🔍 轮询 #${stats.totalPolled} 第${pageCount}页: ${hits.length} 条`);

      // 逐条推送（带限速）
      for (const hit of hits) {
        const ok = await sendToFeishu(hit);
        if (ok) {
          stats.totalPushed++;
          totalPushedThisRound++;

          // 推送成功才推进游标
          const sortValues = hit.sort;
          if (sortValues && sortValues.length >= 2) {
            currentSearchAfter = sortValues;
            cursor.searchAfter = sortValues;
            // 同时维护 lastTimestamp 用于日志和兼容
            const ts = getNestedValue(hit._source || {}, config.es_time_field);
            if (ts) cursor.lastTimestamp = ts;
          }

          // 限速：控制推送频率，避免触发飞书 QPS 限制
          await sleep(pushIntervalMs);
        } else {
          pushFailed = true;
          const remaining = hits.length - hits.indexOf(hit);
          log(`⚠️ 推送失败，停止本轮处理，本页剩余 ${remaining} 条将在下次轮询重试`);
          break;
        }
      }

      // 推送失败，停止翻页
      if (pushFailed) break;

      // 本页数据量不足一页，说明已经拉完
      if (hits.length < effectiveSize) break;

    } catch (err) {
      if (err.response) {
        log(`❌ ES 查询失败 [${err.response.status}]: ${JSON.stringify(err.response.data).slice(0, 200)}`);
      } else {
        log('❌ ES 查询失败: ' + err.message);
      }
      break; // 查询失败，停止翻页，保留当前游标
    }
  }

  if (totalHitsThisRound === 0) {
    log(`🔍 轮询 #${stats.totalPolled}: 无新数据`);
  } else {
    log(`📊 轮询 #${stats.totalPolled} 完成: ${pageCount}页, 命中 ${totalHitsThisRound}, 推送 ${totalPushedThisRound}`);
  }

  saveCursor();
  saveStats();
}

/**
 * 首次运行：拉最新一条初始化游标，不推送
 */
async function pollFirstRun(url, query, sortDef, tiebreakerField) {
  try {
    const body = { size: 1, sort: sortDef, query };
    const res = await axios.post(url, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${config.es_auth}`,
      },
      timeout: 30000,
    });

    const hits = res.data?.hits?.hits || [];
    if (hits.length > 0) {
      const hit = hits[0];
      const sortValues = hit.sort;
      const source = hit._source || {};
      const ts = getNestedValue(source, config.es_time_field);

      if (sortValues && sortValues.length >= 2) {
        cursor.searchAfter = sortValues;
        cursor.lastTimestamp = ts;
        saveCursor();
        log(`📌 游标已初始化: searchAfter=${JSON.stringify(sortValues)}, ${config.es_time_field}=${ts}`);
      } else if (ts) {
        // fallback：ES 没返回完整 sort（比如 tiebreaker 字段不存在），用时间戳兜底
        cursor.searchAfter = [ts, null];
        cursor.lastTimestamp = ts;
        saveCursor();
        log(`⚠️ ES 未返回 tiebreaker sort 值，游标降级为时间戳模式: ${ts}`);
        log(`⚠️ 请检查 es_tiebreaker_field (${tiebreakerField}) 是否存在于索引中`);
      }
    } else {
      log('📌 索引中无数据，等待下次轮询');
    }
  } catch (err) {
    if (err.response) {
      log(`❌ 首次查询失败 [${err.response.status}]: ${JSON.stringify(err.response.data).slice(0, 200)}`);
    } else {
      log('❌ 首次查询失败: ' + err.message);
    }
  }
  saveStats();
}

// ============ 轮询循环（setTimeout 递归，防止堆叠） ============
let pollTimer = null;
let isShuttingDown = false;

async function schedulePoll() {
  if (isShuttingDown) return;
  try {
    await pollES();
  } catch (err) {
    log(`❌ pollES 异常: ${err.message}`);
  }
  if (!isShuttingDown) {
    pollTimer = setTimeout(schedulePoll, config.poll_interval * 1000);
  }
}

function startPolling() {
  log(`⏱️ 轮询间隔: ${config.poll_interval}s`);
  // 立即执行一次，后续等上一次完成后再调度下一次
  schedulePoll();
}

// ============ 优雅关闭 ============
function shutdown() {
  if (isShuttingDown) return; // 防止重复触发
  isShuttingDown = true;
  log('🛑 Shutting down...');
  log(`📊 总计轮询: ${stats.totalPolled}, 命中: ${stats.totalHits}, 推送: ${stats.totalPushed}`);
  if (pollTimer) clearTimeout(pollTimer);
  saveStats();
  saveCursor();
  removePid();
  process.exit(0);
}

// ============ 异常兜底 ============
// 防重入标记：避免 handler 自身抛异常导致无限递归（14GB 日志的元凶）
let _crashHandling = false;

function crashExit(label, detail) {
  if (_crashHandling) {
    // 已经在处理中，直接强退，不做任何 I/O
    process.exit(2);
  }
  _crashHandling = true;
  try { fs.appendFileSync(LOG_FILE, `${new Date().toISOString()} - 💥 ${label}: ${detail}\n`); } catch (_) {}
  try { saveCursor(); } catch (_) {}
  try { saveStats(); } catch (_) {}
  try { removePid(); } catch (_) {}
  process.exit(1);
}

process.on('uncaughtException', (err) => {
  crashExit('未捕获异常', err.stack || err.message);
});
process.on('unhandledRejection', (reason) => {
  crashExit('未处理的 Promise 拒绝', String(reason));
});

// ============ 主入口 ============
async function main() {
  ensureDataDir();
  loadConfig();

  if (isAlreadyRunning()) {
    console.error('❌ 已有实例在运行，请先停止');
    process.exit(1);
  }

  writePid();
  loadStats();
  loadCursor();

  log('========================================================');
  log('🚀 ES-Poll-Feishu v' + VERSION + ' Started (search_after + 雪崩保护)');
  log(`📡 ES: ${config.es_url}/${resolveIndex()} (模板: ${config.es_index})`);
  log(`⏱️ 间隔: ${config.poll_interval}s, 每页: ${config.es_size}, tiebreaker: ${config.es_tiebreaker_field || '_doc'}`);
  log(`🛡️ 雪崩保护: 阈值 ${config.flood_threshold} 条, 冷却 ${config.flood_cooldown}s, 推送限速 ${config.push_rate_limit}/s`);
  log(`📊 历史: 轮询 ${stats.totalPolled}, 命中 ${stats.totalHits}, 推送 ${stats.totalPushed}`);
  if (cursor.searchAfter) log(`📌 游标: searchAfter=${JSON.stringify(cursor.searchAfter)}`);
  else if (cursor.lastTimestamp) log(`📌 游标(旧): ${config.es_time_field} > ${cursor.lastTimestamp}`);
  log('========================================================');

  await getFeishuToken();
  startPolling();

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

main();

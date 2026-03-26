#!/usr/bin/env node
/**
 * ES-Poll-Feishu CLI 入口
 *
 * 用法：node cli.js <tool_name> '<json_args>'
 *       echo '<json>' | node cli.js <tool_name>
 *
 * 示例：
 *   node cli.js search '{"query":{"match_all":{}},"size":5}'
 *   node cli.js poll_once '{}'
 *   node cli.js test_feishu '{"text":"测试消息"}'
 *   node cli.js status '{}'
 *   node cli.js cursor '{}'
 *   node cli.js reset_cursor '{}'
 *   node cli.js set_cursor '{"lastTimestamp":1711234567}'
 */

"use strict";

const fs = require("fs");
const path = require("path");
const http = require("http");
const https = require("https");
const os = require("os");

// ---------- 路径 & 配置 ----------

const CONFIG_PATH = path.join(os.homedir(), ".openclaw", "es-poll-feishu.json");
const DATA_DIR = path.join(os.homedir(), "clawd", "data", "es-poll-feishu");
const PID_FILE = path.join(DATA_DIR, "poller.pid");
const STATS_FILE = path.join(DATA_DIR, "stats.json");
const CURSOR_FILE = path.join(DATA_DIR, "cursor.json");

const DEFAULT_CONFIG = {
  es_url: "",
  es_index: "",
  es_auth: "",
  es_params: {},
  es_query: null,
  es_time_field: "ctime",
  es_sort_field: "ctime",
  es_size: 50,
  es_tiebreaker_field: "_doc",
  es_max_pages: 20,
  poll_interval: 60,
  flood_threshold: 500,
  flood_cooldown: 300,
  push_rate_limit: 3,
  feishu_app_id: "",
  feishu_app_secret: "",
  feishu_user_id: "",
  title_field: "title",
  content_field: "content",
  url_field: "url",
};

let config = { ...DEFAULT_CONFIG };

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    return { ok: false, error: `配置文件不存在: ${CONFIG_PATH}，请先运行 es-poll-feishu config` };
  }
  try {
    const fileConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
    config = { ...DEFAULT_CONFIG, ...fileConfig };
    return { ok: true };
  } catch (e) {
    return { ok: false, error: `配置文件解析失败: ${e.message}` };
  }
}

// ---------- HTTP 请求（零依赖） ----------

function request(method, urlStr, body, headers = {}, timeoutMs = 30000) {
  return new Promise((resolve) => {
    const url = new URL(urlStr);
    const isHttps = url.protocol === "https:";
    const mod = isHttps ? https : http;

    const reqHeaders = { ...headers };
    let payload;
    if (body !== undefined) {
      payload = Buffer.from(JSON.stringify(body), "utf-8");
      reqHeaders["Content-Type"] = "application/json";
      reqHeaders["Content-Length"] = payload.length;
    }

    const opts = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: reqHeaders,
      timeout: timeoutMs,
    };

    const req = mod.request(opts, (res) => {
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const raw = Buffer.concat(chunks).toString("utf-8");
        try {
          resolve({ status: res.statusCode, data: JSON.parse(raw) });
        } catch (_) {
          resolve({ status: res.statusCode, data: raw });
        }
      });
    });

    req.on("timeout", () => {
      req.destroy();
      resolve({ status: 504, data: { error: "请求超时" } });
    });
    req.on("error", (err) => {
      resolve({ status: 0, data: { error: err.message, code: err.code } });
    });

    if (payload) req.write(payload);
    req.end();
  });
}

// ---------- ES 请求封装 ----------

function buildEsUrl(indexOverride) {
  const idx = resolveIndex(indexOverride);
  const params = new URLSearchParams(config.es_params || {});
  return `${config.es_url.replace(/\/+$/, "")}/${idx}/_search?${params.toString()}`;
}

function esHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Basic ${config.es_auth}`,
  };
}

// ---------- 飞书封装 ----------

let feishuAccessToken = "";
let feishuTokenExpiry = 0;

async function getFeishuToken() {
  if (feishuAccessToken && Date.now() < feishuTokenExpiry - 300000) {
    return feishuAccessToken;
  }
  const res = await request("POST", "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal", {
    app_id: config.feishu_app_id,
    app_secret: config.feishu_app_secret,
  });
  if (res.data?.app_access_token) {
    feishuAccessToken = res.data.app_access_token;
    feishuTokenExpiry = Date.now() + (res.data.expire || 7200) * 1000;
    return feishuAccessToken;
  }
  throw new Error(`飞书 Token 获取失败: ${JSON.stringify(res.data)}`);
}

// ---------- 辅助 ----------

function getNestedValue(obj, fieldPath) {
  return fieldPath.split(".").reduce((o, k) => (o && o[k] !== undefined ? o[k] : null), obj);
}

function readJsonFile(filePath) {
  try {
    if (fs.existsSync(filePath)) return JSON.parse(fs.readFileSync(filePath, "utf-8"));
  } catch (_) {}
  return null;
}

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

// ---------- 索引名动态解析 ----------

function resolveIndex(override) {
  const raw = override || config.es_index;
  const now = new Date();
  const yyyy = now.getFullYear().toString();
  const MM = (now.getMonth() + 1).toString().padStart(2, '0');
  return raw
    .replace(/\{yyyyMM\}/g, `${yyyy}${MM}`)
    .replace(/\{yyyy\}/g, yyyy)
    .replace(/\{MM\}/g, MM);
}

// ========== 工具实现 ==========

/**
 * search — 直接查询 ES，返回原始结果
 * 参数: { query?, index?, size?, sort?, _source? }
 */
async function search({ query, index, size, sort, _source } = {}) {
  const body = {};
  body.query = query || config.es_query || { match_all: {} };
  body.size = size || config.es_size;
  if (sort) {
    body.sort = sort;
  } else {
    body.sort = [{ [config.es_sort_field]: { order: "desc" } }];
  }
  if (_source) body._source = _source;

  const url = buildEsUrl(index);
  const res = await request("POST", url, body, esHeaders());
  if (res.status === 0 || res.status >= 400) {
    return JSON.stringify({ code: res.status || 500, message: "ES 查询失败", data: res.data });
  }
  const hits = res.data?.hits || {};
  return JSON.stringify({
    code: 200,
    total: hits.total?.value ?? hits.total ?? 0,
    count: (hits.hits || []).length,
    items: (hits.hits || []).map((h) => ({
      _index: h._index,
      _id: h._id,
      ...h._source,
    })),
  });
}

/**
 * poll_once — 执行一次轮询（search_after 分页 + 飞书推送），更新游标
 * 参数: { dry_run? } — dry_run=true 时只查询不推送
 */
async function poll_once({ dry_run = false } = {}) {
  ensureDataDir();
  const cursorData = readJsonFile(CURSOR_FILE) || { searchAfter: null, lastTimestamp: null };

  // 兼容 v1.0 旧游标格式
  if (!cursorData.searchAfter && cursorData.lastTimestamp != null) {
    cursorData.searchAfter = [cursorData.lastTimestamp, null];
  }

  const tiebreakerField = config.es_tiebreaker_field || "_id";
  const isFirstRun = !cursorData.searchAfter;

  // 基础查询
  let baseQuery;
  if (isFirstRun) {
    baseQuery = config.es_query || { match_all: {} };
  } else if (cursorData.searchAfter[1] === null) {
    // v1.0 迁移兜底
    const q = config.es_query || { match_all: {} };
    if (cursorData.lastTimestamp) {
      baseQuery = { bool: { must: [q, { range: { [config.es_time_field]: { gte: cursorData.lastTimestamp } } }] } };
    } else {
      baseQuery = q;
    }
  } else {
    baseQuery = config.es_query || { match_all: {} };
  }

  const sortDef = isFirstRun
    ? [{ [config.es_sort_field]: { order: "desc" } }, { [tiebreakerField]: { order: "desc" } }]
    : [{ [config.es_sort_field]: { order: "asc" } }, { [tiebreakerField]: { order: "asc" } }];

  const url = buildEsUrl();

  // 首次运行：只拉一条初始化游标
  if (isFirstRun) {
    const body = { size: 1, sort: sortDef, query: baseQuery };
    const res = await request("POST", url, body, esHeaders());
    if (res.status === 0 || res.status >= 400) {
      return JSON.stringify({ code: res.status || 500, message: "ES 查询失败", data: res.data });
    }
    const hits = res.data?.hits?.hits || [];
    if (hits.length > 0 && hits[0].sort) {
      cursorData.searchAfter = hits[0].sort;
      cursorData.lastTimestamp = getNestedValue(hits[0]._source || {}, config.es_time_field);
      fs.writeFileSync(CURSOR_FILE, JSON.stringify(cursorData, null, 2));
      return JSON.stringify({ code: 200, message: "首次运行，游标已初始化", cursor: cursorData });
    }
    return JSON.stringify({ code: 200, message: "索引中无数据" });
  }

  // 分页循环
  let currentSearchAfter = cursorData.searchAfter;
  let totalHits = 0;
  let pushed = 0;
  let pageCount = 0;
  const maxPages = config.es_max_pages || 20;
  const cursorBefore = cursorData.searchAfter ? [...cursorData.searchAfter] : null;

  while (true) {
    pageCount++;
    if (maxPages > 0 && pageCount > maxPages) break;

    const body = { size: config.es_size, sort: sortDef, query: baseQuery };
    if (currentSearchAfter && currentSearchAfter[1] !== null) {
      body.search_after = currentSearchAfter;
    }

    const res = await request("POST", url, body, esHeaders());
    if (res.status === 0 || res.status >= 400) {
      // 查询失败，保存已推进的游标后返回
      fs.writeFileSync(CURSOR_FILE, JSON.stringify(cursorData, null, 2));
      return JSON.stringify({ code: res.status || 500, message: "ES 查询失败", data: res.data, pushed, totalHits });
    }

    const hits = res.data?.hits?.hits || [];
    if (hits.length === 0) break;

    totalHits += hits.length;

    for (const hit of hits) {
      const source = hit._source || {};

      if (!dry_run) {
        const token = await getFeishuToken();
        const title = getNestedValue(source, config.title_field) || "(无标题)";
        const content = getNestedValue(source, config.content_field) || "";
        const hitUrl = getNestedValue(source, config.url_field) || "";
        const timeVal = getNestedValue(source, config.es_time_field);
        const timeStr = timeVal ? new Date(timeVal * 1000).toLocaleString("zh-CN") : "";

        const text = `📢 新数据推送\n\n【${title}】\n\n${content.slice(0, 50)}${content.length > 50 ? "..." : ""}\n\n${hitUrl ? "🔗 " + hitUrl : ""}${timeStr ? "\n🕐 " + timeStr : ""}`;

        const pushRes = await request(
          "POST",
          "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
          { receive_id: config.feishu_user_id, msg_type: "text", content: JSON.stringify({ text }) },
          { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }
        );
        if (pushRes.status === 200 || pushRes.data?.code === 0) pushed++;
      }

      // 推进游标
      if (hit.sort && hit.sort.length >= 2) {
        currentSearchAfter = hit.sort;
        cursorData.searchAfter = hit.sort;
        const ts = getNestedValue(source, config.es_time_field);
        if (ts) cursorData.lastTimestamp = ts;
      }
    }

    if (hits.length < config.es_size) break;
  }

  // 持久化游标
  fs.writeFileSync(CURSOR_FILE, JSON.stringify(cursorData, null, 2));

  return JSON.stringify({
    code: 200,
    total_hits: totalHits,
    pages: pageCount,
    pushed,
    dry_run,
    cursor_before: cursorBefore,
    cursor_after: cursorData.searchAfter,
  });
}

/**
 * test_feishu — 发送测试消息到飞书
 * 参数: { text? }
 */
async function test_feishu({ text } = {}) {
  const msg = text || "🔔 ES-Poll-Feishu 测试消息 — 飞书推送正常！";
  const token = await getFeishuToken();
  const res = await request(
    "POST",
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    { receive_id: config.feishu_user_id, msg_type: "text", content: JSON.stringify({ text: msg }) },
    { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }
  );
  if (res.data?.code === 0 || res.status === 200) {
    return JSON.stringify({ code: 200, message: "飞书推送成功" });
  }
  return JSON.stringify({ code: res.status || 500, message: "飞书推送失败", data: res.data });
}

/**
 * test_es — 测试 ES 连接（查询索引信息）
 * 参数: { index? }
 */
async function test_es({ index } = {}) {
  const idx = index || config.es_index;
  const params = new URLSearchParams(config.es_params || {});
  const url = `${config.es_url.replace(/\/+$/, "")}/${idx}/_search?${params.toString()}`;
  const body = { size: 0, query: config.es_query || { match_all: {} } };
  const res = await request("POST", url, body, esHeaders());
  if (res.status === 0 || res.status >= 400) {
    return JSON.stringify({ code: res.status || 500, message: "ES 连接失败", data: res.data });
  }
  const total = res.data?.hits?.total?.value ?? res.data?.hits?.total ?? 0;
  return JSON.stringify({ code: 200, message: "ES 连接正常", index: idx, total_docs: total });
}

/**
 * status — 查看轮询服务状态和统计
 */
async function status() {
  const statsData = readJsonFile(STATS_FILE);
  const cursorData = readJsonFile(CURSOR_FILE);
  let running = false;
  let pid = null;
  if (fs.existsSync(PID_FILE)) {
    try {
      pid = parseInt(fs.readFileSync(PID_FILE, "utf-8").trim());
      process.kill(pid, 0);
      running = true;
    } catch (_) {
      pid = null;
    }
  }
  return JSON.stringify({
    code: 200,
    running,
    pid,
    stats: statsData || { totalPolled: 0, totalPushed: 0, totalHits: 0 },
    cursor: cursorData || { lastTimestamp: null },
    config_path: CONFIG_PATH,
    data_dir: DATA_DIR,
  });
}

/**
 * cursor — 查看当前游标
 */
async function cursor() {
  const cursorData = readJsonFile(CURSOR_FILE) || { lastTimestamp: null };
  return JSON.stringify({ code: 200, cursor: cursorData });
}

/**
 * reset_cursor — 重置游标
 */
async function reset_cursor() {
  ensureDataDir();
  if (fs.existsSync(CURSOR_FILE)) fs.unlinkSync(CURSOR_FILE);
  return JSON.stringify({ code: 200, message: "游标已重置，下次轮询将从头拉取" });
}

/**
 * set_cursor — 手动设置游标
 * 参数: { lastTimestamp, searchAfter? }
 * searchAfter 为 [timestampValue, tiebreakerValue] 数组
 * 如果只提供 lastTimestamp，会生成兼容格式的游标
 */
async function set_cursor({ lastTimestamp, searchAfter } = {}) {
  if (!searchAfter && (lastTimestamp === undefined || lastTimestamp === null)) {
    return JSON.stringify({ code: 400, message: "请提供 lastTimestamp 或 searchAfter 参数" });
  }
  ensureDataDir();
  const cursorData = {
    searchAfter: searchAfter || [lastTimestamp, null],
    lastTimestamp: lastTimestamp || (searchAfter ? searchAfter[0] : null),
  };
  fs.writeFileSync(CURSOR_FILE, JSON.stringify(cursorData, null, 2));
  return JSON.stringify({ code: 200, message: `游标已设置`, cursor: cursorData });
}

// ---------- CLI 分发 ----------

const TOOLS = {
  search,
  poll_once,
  test_feishu,
  test_es,
  status,
  cursor,
  reset_cursor,
  set_cursor,
};

function readStdin() {
  return new Promise((resolve) => {
    if (process.stdin.isTTY) {
      resolve("{}");
      return;
    }
    const chunks = [];
    process.stdin.setEncoding("utf-8");
    process.stdin.on("data", (c) => chunks.push(c));
    process.stdin.on("end", () => resolve(chunks.join("").trim() || "{}"));
  });
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log(JSON.stringify({
      code: 400,
      message: [
        "用法: node cli.js <tool_name> '<json_args>'",
        "也可通过 stdin 传入 JSON: echo '<json>' | node cli.js <tool_name>",
        "",
        `可用工具: ${Object.keys(TOOLS).join(", ")}`,
        "",
        "工具说明:",
        "  search        — 直接查询 ES（自定义 query/size/sort）",
        "  poll_once      — 执行一次增量轮询 + 飞书推送（dry_run=true 仅查询）",
        "  test_feishu    — 发送测试消息到飞书",
        "  test_es        — 测试 ES 连接",
        "  status         — 查看轮询服务状态和统计",
        "  cursor         — 查看当前游标",
        "  reset_cursor   — 重置游标",
        "  set_cursor     — 手动设置游标（需提供 lastTimestamp）",
      ].join("\n"),
      data: null,
    }));
    process.exit(1);
  }

  const toolName = args[0];
  if (!TOOLS[toolName]) {
    console.log(JSON.stringify({
      code: 400,
      message: `未知工具: ${toolName}，可用工具: ${Object.keys(TOOLS).join(", ")}`,
      data: null,
    }));
    process.exit(1);
  }

  // status / cursor / reset_cursor 不需要 ES 配置
  const noConfigTools = ["status", "cursor", "reset_cursor"];
  if (!noConfigTools.includes(toolName)) {
    const configResult = loadConfig();
    if (!configResult.ok) {
      console.log(JSON.stringify({ code: 500, message: configResult.error, data: null }));
      process.exit(1);
    }
  }

  let rawArgs;
  if (args.length > 1) {
    rawArgs = args[1];
  } else {
    rawArgs = await readStdin();
  }

  let parsed;
  try {
    if (rawArgs.charCodeAt(0) === 0xfeff) rawArgs = rawArgs.slice(1);
    parsed = JSON.parse(rawArgs);
  } catch (e) {
    console.log(JSON.stringify({
      code: 400,
      message: `JSON 参数解析失败: ${e.message}`,
      data: null,
    }));
    process.exit(1);
  }

  const result = await TOOLS[toolName](parsed);
  console.log(result);
}

main();

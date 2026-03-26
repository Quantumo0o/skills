---
name: "es-poll-feishu"
description: "轮询 Elasticsearch 新数据，自动推送到飞书。支持自定义 ES 查询、增量轮询、去重游标。"
---

# ES-Poll-Feishu

轮询 Elasticsearch → 增量检测新数据 → 飞书推送。

## 功能

- 🔍 定时轮询 ES 索引，检测新数据
- 📌 search_after 游标机制，基于排序值精确翻页，不丢不重
- 📱 飞书消息自动推送
- 🔧 支持自定义 ES 查询（term / bool / match 等任意查询）
- 📊 统计持久化（轮询次数、命中数、推送数）
- 🛑 优雅关闭，游标持久化
- 🔄 自动分页，单次轮询可翻多页拉取所有新数据

## 安装

```bash
cd skills/es-poll-feishu
npm install
chmod +x scripts/es-poll-feishu
```

## 配置（必须）

首次使用前，创建配置文件 `~/.openclaw/es-poll-feishu.json`：

```json
{
  "es_url": "http://your-es-host:9200",
  "es_index": "your_index_pattern*",
  "es_auth": "your_base64_auth_string",
  "es_params": {
    "app_customer_name": "your_customer",
    "app_user_name": "your_user"
  },
  "es_query": {
    "bool": {
      "must": [
        { "term": { "your_field": "your_value" } },
        { "range": { "analysis.sentiment": { "lt": 0 } } }
      ]
    }
  },
  "es_time_field": "ctime",
  "es_sort_field": "ctime",
  "es_size": 50,
  "poll_interval": 60,
  "feishu_app_id": "your_feishu_app_id",
  "feishu_app_secret": "your_feishu_app_secret",
  "feishu_user_id": "your_feishu_open_id",
  "title_field": "title",
  "content_field": "content",
  "url_field": "url"
}
```

或运行 `es-poll-feishu config` 创建模板。

### 配置项说明

| 配置项 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `es_url` | ✅ | — | ES 服务地址 |
| `es_index` | ✅ | — | ES 索引名（支持通配符和时间模板，见下方说明） |
| `es_auth` | ✅ | — | Basic Auth 的 base64 字符串 |
| `es_params` | ❌ | `{}` | URL 附加查询参数 |
| `es_query` | ❌ | `null` | 自定义 ES 查询体（query 对象），为 null 则仅按时间增量 |
| `es_time_field` | ❌ | `ctime` | 时间字段名，用于增量游标 |
| `es_sort_field` | ❌ | `ctime` | 排序字段 |
| `es_size` | ❌ | `50` | 每次轮询每页拉取条数 |
| `es_tiebreaker_field` | ❌ | `_doc` | search_after tiebreaker 字段，保证同秒数据不丢失 |
| `es_max_pages` | ❌ | `20` | 单次轮询最大翻页数（防止无限循环），0=不限 |
| `poll_interval` | ❌ | `60` | 轮询间隔（秒） |
| `feishu_app_id` | ✅ | — | 飞书应用 App ID |
| `feishu_app_secret` | ✅ | — | 飞书应用 App Secret |
| `feishu_user_id` | ✅ | — | 接收消息的飞书用户 open_id |
| `title_field` | ❌ | `title` | ES 文档中标题字段路径（支持嵌套如 `retweeted.title`） |
| `content_field` | ❌ | `content` | ES 文档中内容字段路径 |
| `url_field` | ❌ | `url` | ES 文档中链接字段路径 |

### 索引名时间模板

`es_index` 支持 `{yyyyMM}` 占位符，运行时自动替换为当前年月，无需每月手动修改配置。

| 占位符 | 含义 | 示例值 |
|--------|------|--------|
| `{yyyyMM}` | 当前年月（6位） | `202603` |
| `{yyyy}` | 当前年份（4位） | `2026` |
| `{MM}` | 当前月份（2位，补零） | `03` |

例如配置 `"es_index": "xgks_{yyyyMM}*"`，在 2026 年 3 月运行时自动解析为 `xgks_202603*`，4 月自动变为 `xgks_202604*`。

## CLI 工具

仿照 istarshine-search-skill 的 CLI 模式，提供独立的命令行工具，可直接调用或通过 stdin 传入 JSON 参数。

```bash
node scripts/cli.js <tool_name> '<json_args>'
echo '<json>' | node scripts/cli.js <tool_name>
```

### 可用工具

| 工具 | 用途 | 参数 |
|------|------|------|
| `search` | 直接查询 ES，返回原始结果 | `query`, `index`, `size`, `sort`, `_source` |
| `poll_once` | 执行一次增量轮询 + 飞书推送 | `dry_run`（true 时仅查询不推送） |
| `test_es` | 测试 ES 连接 | `index` |
| `test_feishu` | 发送测试消息到飞书 | `text` |
| `status` | 查看轮询服务状态和统计 | 无 |
| `cursor` | 查看当前游标 | 无 |
| `reset_cursor` | 重置游标 | 无 |
| `set_cursor` | 手动设置游标 | `lastTimestamp`, `searchAfter` |

### CLI 示例

```bash
# 测试 ES 连接
node scripts/cli.js test_es '{}'

# 自定义查询 ES
node scripts/cli.js search '{"query":{"match_all":{}},"size":5}'

# 执行一次增量轮询（dry_run 仅查询不推送）
node scripts/cli.js poll_once '{"dry_run":true}'

# 执行一次增量轮询并推送飞书
node scripts/cli.js poll_once '{}'

# 测试飞书推送
node scripts/cli.js test_feishu '{"text":"Hello from ES-Poll-Feishu"}'

# 查看服务状态
node scripts/cli.js status '{}'

# 查看/重置/设置游标
node scripts/cli.js cursor '{}'
node scripts/cli.js reset_cursor '{}'
node scripts/cli.js set_cursor '{"lastTimestamp":1711234567}'
```

## 服务管理

```bash
# 启动服务
es-poll-feishu start

# 查看状态
es-poll-feishu status

# 查看日志
es-poll-feishu logs

# 停止服务
es-poll-feishu stop

# 重启
es-poll-feishu restart

# 查看/创建配置
es-poll-feishu config

# 重置游标（下次从头拉取）
es-poll-feishu reset-cursor
```

## 工作原理

```
┌─────────────┐  search_after  ┌──────────────┐    推送     ┌──────────┐
│  ES 索引     │ ◄──────────── │  poller.js   │ ─────────► │  飞书     │
│  xgks_*     │   分页增量查询  │  游标管理     │   逐条推送  │  机器人   │
└─────────────┘               └──────────────┘            └──────────┘
```

1. 每隔 `poll_interval` 秒查询 ES，使用 `search_after` + tiebreaker 精确翻页
2. **首次运行无游标时，拉取最新一条数据初始化游标位置，不推送历史数据** — 即从"此刻"开始监听新数据
3. 后续轮询使用 `search_after` 值定位上次处理到的位置，自动翻页拉取所有新数据
4. 每条新数据推送到飞书，推送成功才推进游标
5. 游标持久化到 `cursor.json`（包含 `searchAfter` 排序值），重启后精确续传
6. 兼容 v1.0 旧游标格式，升级后自动迁移

> ⚠️ **注意**：首次启动只会推送启动后产生的新数据。如果服务曾经运行过但中途故障停机，重启后会自动补推积压的数据（游标记录了上次处理到的位置）。如需从头拉取历史数据，请先执行 `es-poll-feishu reset-cursor`。

## 自定义查询示例

配置中的 `es_query` 支持任意 ES 查询语法：

```json
// term 精确匹配
"es_query": {
  "term": { "your_field": "your_value" }
}

// bool 组合查询
"es_query": {
  "bool": {
    "must": [
      { "term": { "gather.site_domain": "iesdouyin.com" } },
      { "match": { "content": "新能源" } }
    ]
  }
}

// match 全文搜索
"es_query": {
  "match": { "title": "人工智能" }
}
```

## 数据目录

```
~/clawd/data/es-poll-feishu/
├── poller.pid    # PID 文件
├── poller.log    # 运行日志
├── stats.json    # 统计数据
└── cursor.json   # 轮询游标（searchAfter: [timestamp, tiebreaker]）
```

## License

MIT

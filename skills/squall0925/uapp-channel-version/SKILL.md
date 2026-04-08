name: uapp-channel-version
version: 0.2.0
summary: 友盟 App 渠道/版本分析 skill，支持单日快照查询和趋势分析，回答"哪个渠道/版本表现好"的问题。
entry: scripts/channel_version.py

## 典型问法与 CLI 参数映射

| 典型问法 | CLI 参数 |
|---------|---------|
| "各渠道昨天的新增用户对比？" | `--dimension channel --date yesterday --sort-by new_users` |
| "各版本活跃用户排名？" | `--dimension version --sort-by active_users` |
| "华为渠道过去一周的活跃用户怎样？" | `--dimension channel --metric active_users --range last_7_days --filter-channel huawei` |
| "3.5版本上线后用户表现如何？" | `--dimension version --metric new_users --range last_7_days --filter-version 3.5` |
| "Top 5 渠道的启动次数对比" | `--dimension channel --top 5 --sort-by launches` |
| "Umeng渠道昨天表现如何？" | `--dimension channel --filter-channel Umeng` |

## 查询模式

### 单日快照模式（默认）

查询指定日期的渠道/版本表现排名：

```bash
# 渠道快照（默认昨天）
python3 scripts/channel_version.py --app "Android_Demo" --dimension channel

# 版本快照，按新增用户排序
python3 scripts/channel_version.py --app "Android_Demo" --dimension version --sort-by new_users

# 指定日期，Top 5
python3 scripts/channel_version.py --app "Android_Demo" --dimension channel --date 2026-03-29 --top 5
```

### 趋势分析模式

查询指定渠道/版本的指标趋势：

```bash
# 渠道趋势
python3 scripts/channel_version.py --app "Android_Demo" --dimension channel \
    --metric new_users --range last_7_days --filter-channel Umeng

# 版本趋势
python3 scripts/channel_version.py --app "Android_Demo" --dimension version \
    --metric active_users --range last_30_days --filter-version 2.0.11001
```

## 支持的分析维度

- `channel`（默认）：渠道维度
- `version`：版本维度

## 支持的指标类型

### 单日快照模式

- `active_users`（默认）：活跃用户
- `new_users`：新增用户
- `launches`：启动次数（仅渠道维度）
- `total_user`：总用户

### 趋势分析模式

- `new_users`：新增用户
- `active_users`：活跃用户
- `launches`：启动次数

## 支持的时间范围

- `yesterday`：昨天
- `last_7_days`：过去7天
- `last_30_days`：过去30天
- `last_90_days`：过去90天
- `yyyy-mm-dd`：指定日期

## 配置方式

配置文件路径优先级：
1. `--config /path/to/umeng-config.json`
2. 环境变量 `UMENG_CONFIG_PATH`
3. 当前目录下的 `umeng-config.json`

## 输出格式

### 文本模式（默认）

```
应用 Android_Demo 的 渠道 表现对比（2026-03-29）：

排名     渠道                   新增用户     活跃用户     启动次数     总用户
--------------------------------------------------------------------------------
1      Umeng                15           311          2,579        928,529
2      umeng                2            261          815          306,487
...
```

### JSON 模式（--json）

```json
{
  "app": {
    "name": "Android_Demo",
    "appkey": "...",
    "platform": "Android"
  },
  "dimension": "channel",
  "date": "2026-03-29",
  "sort_by": "active_users",
  "count": 5,
  "data": [...]
}
```

name: uapp-core-index
version: 0.2.0
summary: 友盟 App 核心指标问答入口 skill，支持自然语言问答方式查询 DAU、新增用户、活跃用户、启动次数、使用时长等核心指标，并输出结论与趋势数据。
entry: scripts/core_index.py

## 典型问法与内部意图映射

| 典型问法 | 内部意图（CLI 参数） |
|---------|-------------------|
| "我的 App 昨天 DAU 多少？" | `--metric dau --range yesterday --app <app_name>` |
| "过去7天新增用户趋势怎样？" | `--metric new_users --range last_7_days --app <app_name>` |
| "上周日均启动次数多少？" | `--metric launches --range last_week --app <app_name>` |
| "最近30天使用时长有没有变化？" | `--metric duration --range last_30_days --app <app_name>` |
| "今天 DAU 多少？比昨天怎么样？" | `--metric dau --range today_yesterday --app <app_name>` |

## 支持的指标类型

- `dau`: 活跃用户数（activityUsers）
- `new_users`: 新增用户数
- `launches`: 启动次数
- `duration`: 平均使用时长（秒）

## 支持的时间范围

- `yesterday`: 昨天
- `last_7_days`: 过去7天（含昨天）
- `last_30_days`: 过去30天（含昨天）
- `last_week`: 上周（周一至周日）
- `today_yesterday`: 今天 vs 昨天对比
- `yyyy-mm-dd`: 指定日期（如 2026-03-25）

## 调用示例

### 文本输出（默认）

```bash
# 昨天 DAU
python3 scripts/core_index.py --metric dau --range yesterday --app "Android_Demo"

# 过去7天新增用户趋势
python3 scripts/core_index.py --metric new_users --range last_7_days --app "Android_Demo"

# 上周日均启动次数
python3 scripts/core_index.py --metric launches --range last_week --app "Android_Demo"

# 最近30天使用时长变化
python3 scripts/core_index.py --metric duration --range last_30_days --app "Android_Demo"

# 今天 vs 昨天 DAU 对比
python3 scripts/core_index.py --metric dau --range today_yesterday --app "Android_Demo"
```

### JSON 输出

添加 `--json` 参数获取结构化数据：

```bash
python3 scripts/core_index.py --metric dau --range last_7_days --app "Android_Demo" --json
```

## 配置方式

1. `--config /path/to/umeng-config.json`: 显式指定配置文件
2. `export UMENG_CONFIG_PATH=/path/to/umeng-config.json`: 环境变量
3. 在当前目录创建 `umeng-config.json`: 默认查找

配置文件格式参见项目根目录 `umeng-config.json` 示例。

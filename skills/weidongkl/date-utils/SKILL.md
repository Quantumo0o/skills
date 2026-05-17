---
name: date-utils
description: 通用日期时间计算工具。提供当前时间查询、Unix 时间戳转换、相对日期计算、日期格式转换、工作日判断、周数计算、日期差值等功能。基于 Python datetime 和系统时钟实现，不依赖外部 API。当需要获取准确当前时间、计算日期差值、转换时间戳时使用。
---

# Date Utils Skill

通用日期时间计算工具，基于 Python `datetime` 模块和系统时钟实现。不依赖外部 API 或大模型内部时钟。

## 🎯 设计目的

### 为什么需要这个工具？

**大模型的时间感知是冻结的。** 模型训练完成后，内部时钟就固定在训练数据截止时间，无法获取当前真实日期和时间。

当用户问"今天几号"、"昨天是哪天"、"给我一个时间戳"时，模型可能会给出错误答案。

**此工具通过系统时钟获取准确时间，完全不受模型训练时间影响。**

### 典型场景

| 场景 | 问题 | 解决方式 |
|------|------|----------|
| 工时登记 | 模型把 2026 年的时间戳算成了 2025 年 | 用 `timestamp` 命令获取准确时间戳 |
| 相对日期 | "上周五是哪天？" 模型猜错 | 用 `relative` 命令精确计算 |
| 日期格式 | 需要把 `2026-04-16` 转成 `04月16日` | 用 `format` 命令转换 |
| 工作日判断 | 判断某天是否需要上班 | 用 `workday` 命令判断 |
| 周数查询 | 本周/上周的起止日期 | 用 `week-range` 命令获取 |
| 时间差值 | 两个日期相隔多少天 | 用 `diff` 命令计算 |

## 📌 使用原则

1. **永远不要用大模型内部时钟获取当前时间** — 用此工具
2. **永远不要手动计算时间戳** — 用 `timestamp` 命令
3. **永远不要猜测相对日期** — 用 `relative` 命令
4. **任何需要准确时间的场景** — 优先使用此工具

## 功能清单

| 功能 | 说明 | 示例 |
|------|------|------|
| **Unix 时间戳** | 获取指定日期的 Unix 时间戳（秒） | 今天/昨天/指定日期 |
| **相对日期** | 计算 N 天前/后的日期 | 昨天、前天、3 天后 |
| **日期格式转换** | 在不同日期格式间转换 | `2026-04-16` ↔ `04/16/2026` |
| **工作日判断** | 判断某天是否为工作日 | 周一~周五 = 工作日 |
| **周数计算** | 获取指定日期是一年中的第几周 | ISO 8601 周数 |
| **日期差值** | 计算两个日期之间的天数 | 2026-04-01 到 2026-04-16 = 15 天 |
| **周起止日期** | 获取本周/上周的周一和周日 | 周报日期范围计算 |

## 使用方式

### 获取当前时间 / Unix 时间戳

```bash
# 今天 00:00:00 的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date today

# 昨天 00:00:00 的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date yesterday

# 指定日期 00:00:00 的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date 2026-04-16

# 指定日期 12:00:00 的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date 2026-04-16 --time 12:00
```

### 获取相对日期

```bash
# 昨天
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -1

# 前天
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -2

# 3 天后
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset 3

# 7 天前
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -7

# 基于指定日期计算
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -1 --base 2026-04-16
```

### 日期格式转换

```bash
# YYYY-MM-DD → YYYY/MM/DD
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%Y/%m/%d"

# YYYY-MM-DD → MM/DD/YYYY
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%m/%d/%Y"

# YYYY-MM-DD → 中文格式
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%Y年%m月%d日"

# 获取星期几
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%A"
```

### 工作日判断

```bash
# 判断是否为工作日
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py workday --date 2026-04-16

# 获取最近的工作日
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py workday --date 2026-04-19 --nearest
```

### 周数计算

```bash
# 获取指定日期的 ISO 周数
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week --date 2026-04-16
```

### 日期差值

```bash
# 计算两个日期之间的天数
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py diff --start 2026-04-01 --end 2026-04-16
```

### 批量获取（日报/周报常用）

```bash
# 获取本周起止日期（周一到周日）
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week-range

# 获取上周起止日期
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week-range --offset -1
```

## 输出格式

所有命令输出为 JSON 格式，便于程序解析：

```json
{
  "command": "timestamp",
  "date": "2026-04-16",
  "time": "00:00:00",
  "timestamp": 1776268800,
  "timezone": "Asia/Shanghai (UTC+8)"
}
```

## 依赖

- Python 3.6+
- 标准库 `datetime`、`argparse`、`json`
- 无需额外 pip 安装包

## 注意事项

1. **时区**：默认使用 `Asia/Shanghai` (UTC+8)
2. **时间戳**：默认使用 00:00:00，某些场景（如 ONES 工时登记）建议用 12:00:00 避免时区问题
3. **相对日期**：offset 为正数表示未来，负数表示过去
4. **工作日**：周一~周五为工作日，周六周日为非工作日

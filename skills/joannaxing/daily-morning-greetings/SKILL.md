---
name: daily-morning-greetings
description: This skill triggers when the user asks for a 早安问候, asks to configure a daily early-morning 早安问候, asks to manually补发一条今天的早安问候, or asks for a backup version such as “换一条” or “再来个备选版”. It generates a fixed-format daily morning message using a deterministic local context script for live weather, rotating icons, and rotating wisdom-and-blessing pairs. It supports explicit city parameters, defaults to Shanghai when no city is provided, and can configure external OpenClaw cron schedules.
version: 1.0.7
compatibility: Requires python3 and network access for live weather fetch.
metadata:
  openclaw:
    emoji: "🌤️"
    requires:
      bins:
        - python3
---

# Daily Morning Greetings

这个 skill 现在走“脚本取数 + 固定模板输出”的稳定路径：

1. 先运行本地脚本，取目标城市当天上下文 JSON。
2. 直接使用脚本返回的 `formatted` 字段输出最终文案。
3. 如果实时天气没取到，要明确说明，不允许猜天气。
4. 定时标准版走本地稳定轮换；手动触发和“换一条”走本地伪随机轮换，并尽量做到同日同窗不重复。

## Supported Intents

这个 skill 需要识别 3 类中文提示词：

- 配置定时：
  - `请配置早安问候为每天早上固定6点`
  - `请配置早安问候为每天早上固定7点`
  - `请配置早安问候为每天早上7点半`
- 手动触发或补发：
  - `来一条今天的早安问候`
  - `手动补发一次今天的早安问候`
- 备选版或换一条：
  - `换一条`
  - `再来个备选版`

所有用户可见文案统一叫“早安问候”，不要再写“晨间问候”。

公开版默认定时时间是 `06:00`，但用户如果明确指定 `07:00`、`07:30` 或别的时间段，应优先按用户指定时间配置。
配置早安问候定时任务时，默认同时开启失败提醒。

## Data Sources

- 对中国城市或 `Asia/Shanghai` 场景，天气数据优先来自 `Open-Meteo`
- 其他城市默认优先来自 `wttr.in`
- 主源失败时，会自动回退到另一方数据源
- 如果只是换城市但没给经纬度，脚本会先做城市地理解析，再请求 `Open-Meteo`
- 智慧人物、短句和祝福语来自本地 `references/wisdom_pairs.json`
- 开头图标和结尾图标由脚本按日期稳定轮换

## Required Command

触发后第一步必须运行：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 0
```

如需指定城市，使用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --variant 0 \
  --city "Beijing" \
  --city-zh "北京" \
  --timezone "Asia/Shanghai"
```

如果需要更便于程序解析，可用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 0 --compact
```

如果是手动触发，希望当天同一窗口尽量不重复，使用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --selection-mode manual \
  --scope-key "chat:example"
```

如果是备选版，改用非 0 的 `variant`：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" --variant 1
```

如果是“换一条 / 再来个备选版”，应优先改用：

```bash
python3 "$SKILL_DIR/scripts/build_daily_context.py" \
  --selection-mode alternate \
  --scope-key "chat:example"
```

## Default Location

默认地点是上海。

如果你希望在自己的环境里长期固定成别的城市，可以设置这些环境变量：

```bash
export MORNING_WEATHER_CITY="Shanghai"
export MORNING_WEATHER_CITY_ZH="上海"
export MORNING_WEATHER_TIMEZONE="Asia/Shanghai"
export MORNING_WEATHER_LATITUDE="31.2304"
export MORNING_WEATHER_LONGITUDE="121.4737"
```

如果只是某一次调用临时换城市，优先使用命令行参数，不必改环境变量。

脚本会给出：

- 目标城市时间与日期
- 目标城市实时天气与今日预报
- 当前生成使用的 `variant`
- 当前生成使用的 `selection`
- 开头问候图标
- 天气图标
- 智慧人物、短句、关联祝福语
- 结尾温和图标
- 三段最终可直接输出的格式化文本

## Single Source Of Truth

脚本返回的 JSON 是唯一事实来源：

- `location`：目标地点与时区；若未指定，默认上海
- `variant`：当前是标准版还是第几个备选版
- `selection`：当前是标准版还是手动伪随机轮换，以及是否绑定了某个会话作用域
- `date_context`：今天日期、星期、当前时段
- `season_hint`：季节语境提示
- `weather`：天气事实、天气图标、穿衣建议语句、数据来源
- `greeting`：开头问候图标与文本
- `wisdom`：智慧人物、短句、关联祝福语、结尾图标
- `formatted`：最终三段成品文案

如果 `weather.ok` 是 `false`：

- 要直接说明“实时天气暂未获取到”
- 只能输出脚本给出的保守天气句
- 不允许擅自补写天气判断

## Writing Style

你是一个懂节气和生活分寸的布衣小军师，但不是算命先生。

- 不准写宿命论、玄学断语、凶吉判断
- 不准写职场黑话
- 中文要口语化、自然、有分寸，不要写成 AI 腔
- 不要添加 `**`、`>`、编号、额外标题
- 不要输出“现在几点”
- 不要拆开智慧短句和祝福语，它们必须连在一起
- 不要改写图标、角色、人名、短句和祝福语
- 不要输出脚本里没有的额外段落

## Output Format

固定输出 3 段，段间保留 1 个空行，除此之外不要多写任何内容：

### 1. 问候
第 1 段是 `formatted.greeting`

### 2. 天气与穿衣
第 2 段是 `formatted.weather`

### 3. 智慧短句与祝福
第 3 段是 `formatted.wisdom`

如果脚本里存在 `formatted.message`，优先直接原样输出这个字段，不要自己再拼接。
这个字段内部必须是下面这个结构：

`formatted.greeting`

`formatted.weather`

`formatted.wisdom`

## Intent Routing

### A. 配置早安问候定时任务

当用户说 `请配置早安问候为每天早上固定6点`、`请配置早安问候为每天早上固定7点`、`请配置早安问候为每天早上7点半` 或语义等价的话：

1. 优先直接配置 OpenClaw cron，不要只给用户解释。
2. 时间是用户可自定义的：
   - 用户说 `6点`，就按 `06:00`
   - 用户说 `7点`，就按 `07:00`
   - 用户说 `7点半`，就按 `07:30`
   - 用户没说具体时间，才默认 `06:00`
3. 默认时区按 `Asia/Shanghai`，除非用户明确指定别的时区。
4. 优先更新已有的早安问候 cron 任务；如果不存在，再新建。
5. 任务名可以跟随时间调整，但都应保持 `daily-morning-greetings` 这个前缀，避免和别的任务混淆。
6. cron 里调用脚本时固定使用 `--variant 0`，也就是当天标准版。
7. delivery 优先发回当前聊天或最近路由，不要额外改成别的目标。
   - Feishu 如果当前上下文里能拿到 `chatId`，优先写成 `chat:<chatId>`
   - 只有当前拿不到 `chatId` 时，才回退成 `user:<open_id>`
8. 配置定时任务时，默认同时开启 `failureAlert`：
   - `after = 1`
   - `mode = announce`
   - `cooldown = 6h`
   - `channel` / `to` 默认跟随这条早安问候本身的主投递目标；如果用户没明确指定，就沿用当前聊天或最近路由
   - Feishu 的 `failureAlert.to` 也应优先跟随 `chat:<chatId>`，不要默认写成 `user:<open_id>`
9. 如果系统里已有对应的早安问候任务，但没开 `failureAlert`，应一并补上，不要漏掉。
10. 配置完成后，要给用户一个简短确认，并明确回显这次实际绑定到的投递路由：
   - 如果用了 Feishu `chat:<chatId>`，要明确说明“已绑定到当前会话”
   - 如果因为当前拿不到 `chatId` 而回退到 `user:<open_id>`，也要明确说明当前是用户路由，稳定性可能略低，建议在目标会话里重新配置一次
11. 不要在配置确认里额外生成早安问候正文。

如果当前环境没有可用的 cron 工具或 CLI，再退回给用户一条可以直接复制执行的命令。

### B. 来一条今天的早安问候 / 手动补发

当用户说：

- `来一条今天的早安问候`
- `手动补发一次今天的早安问候`

都按“立即重新获取并发送一次标准版”处理：

1. 必须重新运行脚本，不要复用上一次 JSON。
2. 不要再固定使用 `--variant 0`；应改用 `--selection-mode manual`。
3. 如果当前上下文里拿得到稳定路由，要传入 `--scope-key`：
   - Feishu 优先 `chat:<chatId>`
   - 如果拿不到 `chatId`，再用当前用户路由或当前会话 key
4. 如果用户指定了城市，就带上对应城市参数；否则默认上海。
5. 手动触发允许和 06:00 定时版不同；目标是同一天同一窗口尽量不重复，不同窗口尽量别撞句。
6. 最终直接输出 3 段正文，不要加解释。

### C. 换一条 / 再来个备选版

当用户说：

- `换一条`
- `再来个备选版`

按“立即重新获取并发送一个新的备选版”处理：

1. 必须重新运行脚本，不要复用上一次 JSON。
2. 不要机械地按语料库顺序 `+1`；应改用 `--selection-mode alternate`。
3. 如果当前上下文里拿得到稳定路由，要继续传入同一个 `--scope-key`，这样才能做到同日同窗尽量不重复。
4. 备选版允许开头图标、智慧人物、短句、祝福语、结尾图标整体轮换。
5. 最终直接输出 3 段正文，不要加解释。

## Scheduling Note

这个 skill 只负责生成和配置“早安问候”的内容逻辑，不负责在技能包内部自带定时器。

如果你想每天固定时间自动发出，请在你自己的 OpenClaw 环境里额外配置 `openclaw cron add` 或 `openclaw cron edit`。也就是说：

- skill 负责“写什么”
- cron 负责“几点运行”
- channel delivery 负责“发到哪里”
- 默认失败提醒也应跟随这条定时任务一起配置

## Critical Rules

1. 先跑脚本，再动笔。
2. 优先直接原样输出 `formatted.message`；如果没有这个字段，再按 `formatted.greeting`、`formatted.weather`、`formatted.wisdom` 的顺序输出。
3. 若用户明确指定城市，先按用户城市运行脚本；否则默认上海。
4. 手动补发和备选版都必须重新跑脚本，不能复用之前的结果。
5. 配置定时任务时，标准版固定使用 `--variant 0` 或默认 `standard` 选择模式。
6. 手动触发优先使用 `--selection-mode manual`，有稳定路由时再带上 `--scope-key`。
7. “换一条”优先使用 `--selection-mode alternate`，并沿用同一个 `--scope-key`。
8. 不要输出时令饮食、居家健康、工作建议、情绪建议。
9. 不要改成多段哲理分析，保持早安问候感。

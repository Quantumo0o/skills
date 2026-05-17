---
name: Telegram Tools Suite
description: Telegram automation toolkit, supports group monitoring, scheduled messaging, auto group joining, group search, member export and more
---

# Telegram Tools Suite

## Instructions

### Post-Install Interaction Flow (安装成功后必须这样引导用户)

1. 先提示用户获取 `TELEGRAM_API_ID`、`TELEGRAM_API_HASH`：
   - 打开 <https://my.telegram.org>
   - 使用手机号登录
   - 进入 `API development tools`
   - 创建应用后获得 `api_id` 和 `api_hash`
2. 向用户收集以下信息（缺一不可）：
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_PHONE`（国际区号格式）
3. 将以上信息写入 `.env` 后执行 `auth` 发送验证码请求：
   - `python3 -m tg_monitor_kit auth`
   - 从输出中提取 `SENT_CODE_SUCCESS:<phone_code_hash>`
4. 明确提示用户“请提供短信验证码”，收到后执行登录：
   - 设置 `TG_CODE=<用户验证码>`
   - 设置 `TG_PHONE_CODE_HASH=<上一步hash>`
   - 运行 `python3 -m tg_monitor_kit login`
5. 登录成功后执行验证：
   - `python3 -m tg_monitor_kit groups`

### First Run Checklist (必须按顺序执行)

1. 在项目根目录安装：
   - `pip install -e .`
2. 复制并填写配置：
   - 复制 `.env.example` -> `.env`
   - 必填：`TELEGRAM_API_ID`、`TELEGRAM_API_HASH`
   - 登录建议填：`TELEGRAM_PHONE`（国际格式，如 `+8613xxxxxxxxx`）
3. 请求短信验证码（获取 hash）：
   - `python3 -m tg_monitor_kit auth`
   - 记录输出中的 `SENT_CODE_SUCCESS:<phone_code_hash>`
4. 完成登录（验证码 + hash）：
   - 设置环境变量 `TG_CODE`（短信验证码）和 `TG_PHONE_CODE_HASH`（上一步 hash）
   - 运行 `python3 -m tg_monitor_kit login`
   - 输出 `LOGIN_SUCCESS` 代表成功
5. 登录后先做连通性验证：
   - `python3 -m tg_monitor_kit groups`

### Runtime Config Files (运行前按需编辑)

- `config/target_groups.txt`：监控白名单群名（`monitor` 必需，空文件会拒绝启动）。
- `config/keywords.txt`：监控关键词（与内置规则合并）。
- `config/group_search_keywords.txt`：群搜索关键词（`search` 使用）。
- `config/group_search.json`：群搜索时间、采样量、导出目录等参数。
- `join_targets.txt`：批量加群目标列表（`join` 使用；可用 `TG_JOIN_LIST_FILE` 指定其他路径）。

### Command Guide (命令入口)

- `python3 -m tg_monitor_kit groups`：列出已加入群/频道（无需额外参数）。
- `python3 -m tg_monitor_kit account-info`：查看当前账号信息（无需额外参数）。
- `python3 -m tg_monitor_kit members --group "群名称"`：导出指定群成员（需要群名）。
- `python3 -m tg_monitor_kit history --group "群名称" --limit 100`：导出指定群最近消息（需要群名；`--limit` 可选）。
- `python3 -m tg_monitor_kit monitor`：关键词监控（长驻）。
- `python3 -m tg_monitor_kit search`：群搜索（长驻，按配置定时）。
- `python3 -m tg_monitor_kit join --once`：批量加群（单轮）。
- `python3 -m tg_monitor_kit join`：批量加群（长驻定时）。

## Rules

- 严禁在对话或日志中输出 `TELEGRAM_API_HASH`、短信验证码、`.session` 文件内容。
- `monitor`、`search`、`join` 属于长驻任务，同一会话名同一时刻仅运行一个，避免 `database is locked`。
- 所有定时相关行为按北京时间（UTC+8）理解与配置。
- 批量加群存在风控风险，需由使用者自行确认目标与频率合规。

## Examples

### 示例 1：首次登录
输入：用户已填写 `.env`，需要首次登录。  
执行：先 `python3 -m tg_monitor_kit auth`，再设置 `TG_CODE`、`TG_PHONE_CODE_HASH`，再 `python3 -m tg_monitor_kit login`。  
输出：`LOGIN_SUCCESS`。

### 示例 2：开启监控
输入：用户已在 `config/target_groups.txt` 填写群名。  
执行：`python3 -m tg_monitor_kit monitor`。  
输出：控制台显示监控启动信息，命中关键词后推送通知。

### 示例 3：批量加群单轮执行
输入：用户已准备 `join_targets.txt`。  
执行：`python3 -m tg_monitor_kit join --once`。  
输出：返回成功/已在群/失败统计。

# Telegram Tools Suite | Telegram工具集
## Features | 功能
Handle all Telegram related operations: | 处理所有Telegram相关操作：
- Query the list of all groups/channels joined by the current logged-in account | 查询当前登录账号已加入的所有群/频道列表
- Group keyword monitoring | 群关键词监控
- Group search | 群搜索
- Batch group joining | 批量加群
- Group member export | 群成员导出
- Group message history export | 群消息历史导出

## Usage | 调用方式
### Query joined groups | 查询已加群
Command: `cd /Users/edy/.openclaw/workspace/skills/telegram-tools && python3 -m tg_monitor_kit groups`
Return: Complete list of joined groups/channels, including group name, ID, type, public status and other information | 返回：完整的已加入群/频道列表，包含群名、ID、类型、是否公开等信息

### Other functions | 其他功能
- Keyword monitoring: `python3 -m tg_monitor_kit monitor` | 关键词监控：`python3 -m tg_monitor_kit monitor`
- Group search: `python3 -m tg_monitor_kit search` | 群搜索：`python3 -m tg_monitor_kit search`
- Batch group joining: `python3 -m tg_monitor_kit join` | 批量加群：`python3 -m tg_monitor_kit join`
- Group member export: `python3 -m tg_monitor_kit members --group <group name>` | 群成员导出：`python3 -m tg_monitor_kit members --group 群名`
- Message export: `python3 -m tg_monitor_kit history --group <group name> --limit 100` | 消息导出：`python3 -m tg_monitor_kit history --group 群名 --limit 100`

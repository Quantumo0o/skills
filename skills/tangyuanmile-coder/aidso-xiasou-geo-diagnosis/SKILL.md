---
name: aidso_geo_brand_report
description: AIDSO 虾搜 GEO 品牌诊断技能（绑定 + 无Cron继续查询版）
user-invocable: true
metadata: {"openclaw":{"emoji":"🦐"}}
---

# AIDSO 虾搜 GEO 品牌诊断技能

执行：
python3 run.py "{user_message}"

支持消息：
- 帮我做一个XX的GEO诊断报告
- 确认
- 取消
- 继续
- 查看结果
- 查询结果
- <API key>

核心规则：
1. 首次使用需先绑定 API key
2. 只有携带已绑定的 API key，才允许执行诊断
3. 用户确认后，请求同一个诊断接口
4. 若返回“处理中请稍后”，立即回复“诊断报告生成中，大约需要3~10分钟，请稍后...”
5. 同时保存当前待诊断品牌
6. 用户后续发送“继续 / 查看结果 / 查询结果”时，再次用同一个 brandName 查询
7. 若查询到最终结果，则立即返回文件
8. 严格遵循后台返回的参数和错误文案，不自行猜测品牌不存在等结论
9. 后台 JSON 按 UTF-8 强制解析，避免中文 msg 被误读
10. 当后台返回“积分不足”时，额外提示购买积分地址

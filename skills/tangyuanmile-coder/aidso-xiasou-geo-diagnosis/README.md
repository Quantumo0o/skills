# aidso_geo_brand_report（无 Cron 继续查询版 v4）

新增：
- 当后台返回“积分不足”时，在原始后台文案后追加：
  请前往https://geo.aidso.com 购买积分

同时保留：
- 强制按 UTF-8 解析后台 JSON
- 后台错误文案原样返回
- 首次使用绑定提示 + 后续技能更新提醒
- API key 地址：
  https://geo.aidso.com/setting?type=apiKey&platform=GEO
- 长时间未生成提醒官网查看：
  https://geo.aidso.com/completeAnalysis
- 自定义需求官网：
  https://geo.aidso.com

依赖：
pip install requests markdown weasyprint

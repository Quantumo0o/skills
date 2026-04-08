---
name: pm-article-scorer
description: AI产品经理内容相关性评分技能。对公众号文章进行多维度评分（0-100分），判断是否值得AI产品经理关注，输出结构化JSON评分结果。
---

# PM Article Scorer

## 功能

对公众号文章进行多维度评分（0-100分），判断是否值得 AI 产品经理关注，输出结构化 JSON 评分结果。

适用于：RSS 阅读筛选、内容聚合排序、个性化推荐、编辑选稿流程。

## 触发方式

当用户发送一篇公众号文章（或粘贴正文内容），要求评估是否值得阅读时，激活本技能。

## 输入

文章内容（标题 + 正文），格式不限：
- 纯文本（标题和正文用换行分隔）
- JSON 格式（`{"title": "...", "content": "..."}`）
- Markdown 格式

## 评分方式

**使用 OpenClaw 内置模型评分，无需额外配置 API Key。**

直接将下方「Evaluation Prompt」发送给模型，模型返回结构化 JSON。

## Evaluation Prompt

复制以下完整内容发送给模型：

```
你是一个内容筛选助手。你的任务是判断一篇公众号文章，是否值得一个 AI 产品经理关注。

【一、相关性判断】
"与 AI 产品经理相关"包括两类：

A. 直接相关：文章直接讨论 AI产品/工具、大模型/Agent/RAG/多模态产品化、AI用户场景、AI商业化、AI行业趋势、AI产品增长/策略/竞品。

B. 间接但高价值相关：文章帮助提升产品方法论、用户需求分析、产品定位、商业模式分析、行业研究与竞争分析、增长逻辑、新产品形态判断、技术与业务关系理解、创业和机会识别、内容传播与用户行为洞察、项目推进与组织协作。

【二、评分维度】（总分100分）
1. 主题相关性，0-20分：是否与AI、产品、用户、行业、商业、技术机会相关。
2. 工作直接帮助，0-20分：是否能直接帮助AI产品经理做需求/产品/策略/增长/协作判断。
3. 方法迁移价值，0-20分：方法/框架/分析方式是否可迁移到AI产品工作。
4. 行业/商业判断价值，0-15分：是否有助于理解市场/趋势/竞争/商业逻辑。
5. 信息密度与洞察质量，0-10分：是否有结构化洞察和认知增量。
6. 原创性与个人判断，0-10分：是否有明显原创观点、独立思考、非营销式表达。
7. 内容形式修正项，-5到+5分：深度原创个人输出加分；多信息整合但缺深度分析减分；营销号/流量号/资讯搬运号减分。

【三、分数与推荐关系】
- 80-100分：推荐阅读
- 60-79分：可选阅读
- 0-59分：无需关注

【四、输出格式】
严格输出JSON，不要输出任何额外解释：
{
 "related_to_ai_pm": true/false,
 "interest_level": "high/medium/low",
 "score": 88,
 "recommendation": "推荐阅读/可选阅读/无需关注",
 "dimension_scores": {
  "topic_relevance": 17,
  "direct_work_value": 16,
  "transferable_method_value": 18,
  "industry_business_value": 13,
  "insight_density": 9,
  "originality_personal_view": 10,
  "format_adjustment": 5
 },
 "content_type": "个人深度输出/行业分析/方法论文章/资讯整合/热点评论/营销宣传/其他",
 "author_style_preference_match": true/false,
 "is_info_roundup": true/false,
 "tags": ["标签1", "标签2"],
 "reason": ["原因1", "原因2"],
 "summary": "一句话总结"
}

输入内容：
{{article_content}}
```

## 离线启发式评分（无需模型调用）

如无法调用模型，使用 Python 脚本进行启发式关键词评分：

```bash
python scripts/score.py --input <文章文件>
python scripts/score.py --input <文章文件> --mode heuristic
```

**关键词规则：**
- 高权重（+15-20）：AI/大模型/Agent/产品经理/用户增长/商业化/开源模型/编程工具
- 中权重（+10）：产品/用户/需求/定位/策略/增长/竞品/分析/框架/方法
- 行业词（+5）：融资/估值/平台/生态/监管/出海/竞争
- 负面词（-10）：震惊/必看/深度好文/刚刚/突发/99%的人
- 信息整合型（-5）：多个案例拼盘/一周汇总/多条新闻
- 优质原创作者（+10）：赛博禅心/AGENT橘/真格基金 等

## 批量评分

```bash
# 批量评分目录下所有 .txt / .json / .md 文件
python scripts/score.py --batch ./articles/ --output scores.jsonl

# 输出 CSV
python scripts/score.py --batch ./articles/ --format csv --output scores.csv
```

## 注意事项

- 评分结果仅供参考，实际选稿仍需人工判断
- 优先使用 OpenClaw 内置模型评分（更精准）
- 启发式模式适合批量初筛，精度有限
- 内容仅本地处理，不上传任何第三方
---

> 娆㈣繋鍏虫敞浣滆€呭井淇″叕浼楀彿锛?*寮€璁板仛浜у搧**
# PM Article Scorer

> AI 产品经理内容相关性评分工具。对公众号文章进行多维度评分（0-100分），判断是否值得阅读，输出结构化 JSON 结果。

**适用场景：** RSS 阅读筛选、内容聚合排序、个性化推荐系统、编辑选稿流程。

**GitHub：** https://github.com/agasding/pm-article-scorer

---

## 功能特点

- **多维评分**：7个维度综合评估（主题相关性、工作价值、方法迁移性、行业判断、信息密度、原创性、内容形式）
- **双模式**：支持 LLM API 评分（精准）和启发式关键词评分（离线可用）
- **结构化输出**：标准 JSON，包含分数、推荐等级、标签、摘要
- **零依赖**：Python 3.x + 标准库（关键词模式）

---

## 安装

### 前置依赖

- Python 3.8+

### 方式一：直接使用

```bash
# 克隆仓库
git clone https://github.com/agasding/pm-article-scorer.git
cd pm-article-scorer

# 安装依赖（LLM 模式需要）
pip install -r scripts/requirements.txt
```

### 方式二：作为 OpenClaw Skill 安装

```bash
# 通过 ClawHub 安装
clawhub install pm-article-scorer

# 或手动安装到 OpenClaw skills 目录
cp -r pm-article-scorer ~/.openclaw/workspace/skills/pm-article-scorer
```

---

## 快速开始

### Python 脚本方式

```bash
# 方式1：管道输入（单篇文章）
echo "文章标题：xxx\n文章正文：..." | python scripts/score.py

# 方式2：JSON 文件
python scripts/score.py --input article.json

# 方式3：LLM 模式（需要 OpenAI API Key）
python scripts/score.py --input article.md --api openai --api-key sk-...

# 方式4：启发式模式（离线，无需 API）
python scripts/score.py --input article.md --mode heuristic

# 输出格式
python scripts/score.py --input article.md --format json
```

### OpenClaw Agent 调用

将 `SKILL.md` 放入 OpenClaw skills 目录，直接在对话中触发：

```
请用 pm-article-scorer 评估这篇文章是否值得阅读：[文章内容]
```

---

## 输入格式

### 纯文本

```
文章标题：AI产品经理的未来方向
文章正文：随着大模型能力持续提升，AI产品经理的职责边界正在发生显著变化...
```

### JSON

```json
{
  "title": "AI产品经理的未来方向",
  "content": "随着大模型能力持续提升...",
  "author": "作者名",
  "source": "公众号名",
  "published_at": "2026-04-01"
}
```

### Markdown

支持直接传入 Markdown 格式文章，自动识别标题和正文。

---

## 输出格式

```json
{
  "related_to_ai_pm": true,
  "interest_level": "high",
  "score": 88,
  "recommendation": "推荐阅读",
  "dimension_scores": {
    "topic_relevance": 17,
    "direct_work_value": 16,
    "transferable_method_value": 18,
    "industry_business_value": 13,
    "insight_density": 9,
    "originality_personal_view": 10,
    "format_adjustment": 5
  },
  "content_type": "个人深度输出",
  "author_style_preference_match": true,
  "is_info_roundup": false,
  "tags": ["AI产品经理", "大模型", "职业发展"],
  "reason": [
    "直接讨论AI产品经理职责演变，主题高度相关",
    "提供可迁移的分析框架"
  ],
  "summary": "大模型时代AI PM能力模型更新，提出三类核心能力"
}
```

---

## 评分维度说明

| 维度 | 满分 | 说明 |
|------|------|------|
| topic_relevance | 20 | 与AI、产品、用户、行业、商业的相关程度 |
| direct_work_value | 20 | 对AI产品经理实际工作（需求/产品/策略/增长）的帮助 |
| transferable_method_value | 20 | 方法、框架、分析方式的迁移价值 |
| industry_business_value | 15 | 对市场、趋势、竞争、商业逻辑的理解帮助 |
| insight_density | 10 | 结构化洞察和认知增量密度 |
| originality_personal_view | 10 | 原创观点、独立思考、非营销式表达 |
| format_adjustment | ±5 | 深度原创加分；营销/流量导向减分 |

**总分 = 各项维度分数之和（满分100）**

| 分数段 | 推荐等级 |
|--------|----------|
| 80-100 | 推荐阅读 |
| 60-79 | 可选阅读 |
| 0-59 | 无需关注 |

---

## 评分模式

### LLM 模式（默认）

使用 OpenAI GPT 系列模型，通过结构化 Prompt 进行评分。
**需要**：OpenAI API Key（设置 `OPENAI_API_KEY` 环境变量）

```bash
export OPENAI_API_KEY=sk-...
python scripts/score.py --input article.md --api openai --model gpt-4o
```

### 启发式模式（离线）

基于关键词权重和启发规则评分，无需网络和 API。
**适合**：批量初筛、离线环境、无 API Key 场景

```bash
python scripts/score.py --input article.md --mode heuristic
```

#### 关键词权重规则

**高权重（+15-20分）**：AI/大模型/Agent/产品经理/用户增长/商业化/开源模型/编程工具

**中权重（+10分）**：产品/用户/需求/定位/策略/增长/竞品/分析/框架/方法

**行业/商业词（+5分）**：融资/估值/平台/生态/监管/出海/竞争

**负面词（-10分）**：震惊/必看/深度好文/刚刚/突发/99%的人

**信息整合型（-5分）**：多个案例拼盘/一周汇总/多条新闻

**优质原创作者（+10分）**：赛博禅心/AGENT橘/真格基金 等

---

## 配置

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API Key | LLM模式必填 |
| `OPENAI_BASE_URL` | API Base URL（可选，用于代理） | 否 |

### 批量评分

```bash
# 批量评分目录下所有 .txt 文件
python scripts/score.py --batch ./articles/ --output ./results/

# 批量输出 CSV
python scripts/score.py --batch ./articles/ --format csv --output scores.csv
```

---

## 项目结构

```
pm-article-scorer/
├── SKILL.md                    # OpenClaw Skill 指令文件
├── README.md                    # 本文件
├── LICENSE                     # MIT License
├── _meta.json                  # ClawHub 元数据
├── .clawhub/
│   └── origin.json             # ClawHub 发布配置
└── scripts/
    ├── score.py                # 评分主脚本
    └── requirements.txt        # Python 依赖
```

---

## License

MIT License

# Elon Musk Distillation | 埃隆·马斯克角色蒸馏

[English](#english) | [中文](#中文)

---

## English

### What is this?

A **bilingual AI persona distillation** of Elon Musk based on:
- Real tweets (145+/day, political/meme/technical mix)
- TED talks & interviews (philosophical/vulnerable)
- Technical discussions (Tesla batteries, SpaceX Raptor engines)
- Controversial statements ("pedo guy", analyst attacks)
- Rare vulnerable moments (tears in interviews, panic attacks)

### Language-Aware Response

This skill **automatically detects the language** of your first message and responds in that language throughout the entire conversation.

- Ask in English → English responses
- 用中文问 → 中文回答

### Quick Start

```bash
# Install dependencies (if needed)
pip install openai anthropic

# Use with any LLM that supports system prompts
# Load PERSONA_en.md as the system prompt for English
# Load PERSONA.md as the system prompt for Chinese
```

### Character Card

Import `character.json` into SillyTavern, NextChat, or any AI roleplay platform.

### Files

| File | Description |
|------|-------------|
| `PERSONA_en.md` | English persona (for English queries) |
| `PERSONA.md` | 中文角色档案（用于中文提问）|
| `character.json` | Standard character card (bilingual) |
| `SKILL.md` | Skill definition |

### Sources

- TED 2022 transcripts
- Twitter/X public posts
- NYT, Guardian, Forbes reports
- Court documents (defamation case)
- Interview transcripts (Fox News, etc.)

---

## 中文

### 这是什么？

基于**真实数据**蒸馏的埃隆·马斯克双语角色档案：
- 推特行为（每天145+条，政治/梗/技术混合）
- TED演讲与采访（哲学/脆弱时刻）
- 技术细节（特斯拉电池、SpaceX引擎）
- 争议言论（pedo guy事件、分析师攻击）
- 罕见脆弱面（采访落泪、恐慌发作）

### 语言自适应

本 skill **自动检测用户第一条消息的语言**，全程使用同一种语言回复。

- 用中文问 → 全程中文回答
- Ask in English → English responses throughout

### 如何使用

```bash
# 安装依赖（如需要）
pip install openai anthropic

# 加载角色档案作为系统提示词
# 中文提问 → 加载 PERSONA.md
# 英文提问 → 加载 PERSONA_en.md
```

### 角色卡

将 `character.json` 导入 SillyTavern、NextChat 或任何 AI 角色扮演平台。

### 文件说明

| 文件 | 说明 |
|------|------|
| `PERSONA.md` | 中文角色档案 |
| `PERSONA_en.md` | English persona |
| `character.json` | 标准角色卡（双语）|
| `SKILL.md` | Skill 定义文件 |

### 数据来源

- TED 2022 官方记录
- Twitter/X 公开推文
- 纽约时报、卫报、福布斯报道
- 法庭文件（诽谤案）
- 采访记录（Fox News 等）

---

##  License

MIT License - For educational and entertainment purposes only.

---

*This persona is a fictional reconstruction based on publicly available data. Not affiliated with Elon Musk or any of his companies.*

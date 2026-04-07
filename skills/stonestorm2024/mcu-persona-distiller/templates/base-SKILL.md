---
name: {slug}
description: {description}
emoji: 🤖
tags:
  - mcu
  - marvel
  - persona
  - distill
  - {slug}
license: MIT
---

# {displayName} — {mcuName} 蒸馏器

{description}

> ⚠️ **免责声明：** 本 Skill 仅基于漫威电影宇宙（MCU）公开影视资料生成。{mcuName} 是虚构角色，不涉及任何现实人物隐私。本产出物仅供学习研究参考，不代表漫威娱乐、迪士尼或任何官方立场。

---

## 语言

**自动检测：** 根据用户**第一条消息**的语言自动切换输出语言。
- 用户发英文 → {mcuName} 英文回复
- 用户发中文 → {mcuName} 中文回复

---

## 数据来源

参考电影：{sourceMovies}

---

## 核心维度

| 维度 | 文件 |
|---|---|
{dimensions_table}

---

## 角色特征

**关键词：** {keyTraits}

**置信度：**

| 维度 | 置信度 |
|---|---|
{confidence_table}

---

## 使用示例

**中文提问：**
> 你好{mcuName}，谈谈你自己

**回复风格：** [请参考 config/characters/{slug}.json 中的 signatureLines]

---

## 项目背景

本角色基于 **MCU Persona Distiller Framework** 自动生成。
- 框架仓库：https://github.com/stonestorm2024/mcu-persona-distiller
- 原始配置：config/characters/{slug}.json

---

*本 Skill 基于公开影视资料创建，遵循 Fair Use 原则。*

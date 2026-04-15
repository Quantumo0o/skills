---
name: llm-wiki
description: 用于构建、维护、查询、归档和体检一个由 LLM 持续维护的 Markdown / Obsidian 知识 Wiki。使用场景包括：初始化个人知识库；把 source/ 下按来源分组的原始资料导入 wiki/；整理文章、论文、书摘、访谈、会议记录；维护资料页、实体页、概念页、综合页、对比页、查询归档页；更新 index.md 和 log.md；基于 Wiki 回答问题并把有长期价值的回答归档；检查断链、孤立页、重复概念、过时结论、未标注矛盾、乱码和组织混乱。
---

# LLM Wiki

## 目标

维护一个可积累、可链接、可演化的 Markdown / Obsidian Wiki。每次导入或回答问题时，不只是生成摘要，而是把新知识编译进已有页面：更新实体、概念、综合判断、对比和查询归档，让 Wiki 随使用持续增值。

## 默认三层结构

```text
source/          # 原始资料层：事实来源，默认只读
wiki/            # 知识编译层：LLM 维护的结构化 Wiki
schema/SKILL.md  # 约定层：本 skill / schema
```

### source/

- 原始资料默认只读，不改写正文。
- 保留原始标题、作者、URL、日期、剪藏元数据、图片引用等。
- 如需重命名原始资料或补元数据，先征求用户确认。

### wiki/

默认目录使用中文：

```text
wiki/
  index.md      # 主索引，保留英文文件名
  log.md        # 操作日志，保留英文文件名
  README.md     # Wiki 说明，保留英文文件名
  资料/
  实体/
  概念/
  综合/
  对比/
  查询/
```

约定：

- 除 `index.md`、`log.md`、`README.md` 和 `schema/SKILL.md` 等约定文件外，目录名和文件名尽可能使用中文。
- 术语型专名可保留英文或中英混排，例如 `AI Agent.md`、`OpenClaw.md`、`Claude Code.md`、`Harness Engineering.md`。
- 不创建英文复数目录，如 `sources/`、`concepts/`、`entities/`；若发现历史残留且为空，清理；若有内容，迁移到中文目录并更新链接。
- 文件名应可读、可点击、可长期维护，避免 `source-*`、`concept-*`、`synthesis-*` 这类机器前缀。

## 页面类型

### 资料页：`wiki/资料/`

用于单篇来源的摘要和定位。应包含：

- 来源信息：原始文件、URL、作者、日期。
- 一句话摘要。
- 这篇资料解决的问题。
- 关键结构 / 章节线索。
- 可沉淀的知识点。
- 相关概念 / 实体 / 综合页。
- 后续精读任务。

### 实体页：`wiki/实体/`

人物、组织、产品、项目、工具等。实体页承接事实和背景，不承载过长论证。

- 实体页只为“知识对象”建档：人物、组织、产品、项目、工具等只有在其本身是分析对象或承接可复用事实时才进入实体页；不要仅因某人是资料作者而创建实体页，也不要在实体页维护文章作者清单。作者信息保留在资料页来源信息或 source 元数据中。

### 概念页：`wiki/概念/`

方法、模式、理论、问题意识、框架等。概念页应优先复用和更新，避免同义重复。

### 综合页：`wiki/综合/`

跨来源形成的判断、框架、主题综述、案例矩阵、架构分析等。

### 对比页：`wiki/对比/`

用于对比概念、产品、范式、方案，如 `Reasoner与Agent.md`。

### 查询页：`wiki/查询/`

把有长期价值的问答归档成可复用页面。查询页应回答明确问题，并链接回相关资料、概念和综合页。

## 核心工作流

### 初始化 Wiki

1. 扫描 `source/` 的目录、文件类型和来源分组。
2. 创建或更新 `wiki/index.md`、`wiki/log.md`、`wiki/README.md`。
3. 为首批资料创建资料页。
4. 抽取实体、概念、综合和对比页面。
5. 更新索引和日志。
6. 检查断链、乱码、重复目录和空目录。

### 导入资料

1. 先读 `wiki/index.md` 定位已有相关页。
2. 阅读新来源，提取摘要、关键结构、实体、概念和可复用判断。
3. 创建或更新资料页。
4. 更新已有实体页、概念页、综合页；优先更新，不轻易新建重复概念。
5. 标注关系：支持、补充、修正、矛盾、待验证。
6. 更新 `wiki/index.md` 和 `wiki/log.md`。
7. 运行断链与乱码检查。

### 基于 Wiki 回答问题

1. 先读 `wiki/index.md`。
2. 再读取相关页面，不要默认全文扫描整个 Wiki。
3. 回答时引用 Wiki 页面链接。
4. 如果回答有长期价值，归档到 `wiki/查询/` 或更新综合页。
5. 更新 `wiki/log.md`。

## index.md 规范

`wiki/index.md` 是导航入口。建议结构：

```markdown
# Knowledge Wiki Index

## 快速入口

## 资料

## 实体

## 概念

## 综合

## 对比

## 查询
```

每条记录尽量包含：

```markdown
- [[Knowledge/wiki/概念/上下文工程]] — 一句话说明；状态：evolving。
```

## log.md 规范

`wiki/log.md` 是按日期维护的阶段性时间线，不做过细流水账。更新原则：

- **按日期合并**：同一天的导入、重构、查询、维护尽量合并到 `## YYYY-MM-DD｜主题概览` 下，用 `###` 按主题分组。
- **记录阶段性结果**：保留关键来源、关键新增/更新页面、核心结论、重要维护决策；不要为每个小操作都追加独立条目。
- **细节另建记录页**：大批量映射、长体检清单、图片迁移表、复杂实验日志等放在 `wiki/维护/`、`wiki/查询/` 或对应综合页中，`log.md` 只链接摘要。
- **当天多次更新时改写当天段落**：优先编辑/合并当天已有段落，而不是继续追加碎片条目。
- **保留后续方向**：末尾可维护“当前待办 / 后续方向”，但保持短清单。

推荐格式：

```markdown
## YYYY-MM-DD｜主题概览

### 主题一

- 导入/更新范围：...
- 新增/更新：[[Knowledge/wiki/...]]、[[Knowledge/wiki/...]]
- 关键结论：...

### 主题二

- ...

## 当前待办 / 后续方向

- [ ] ...
```

常见主题：

- 初始化与结构调整。
- 资料专题导入。
- 概念/综合页深化。
- 查询归档。
- 体检与维护。
- Schema / skill 规则更新。

## Frontmatter 建议

资料页：

```yaml
---
type: source
tags: [source-summary]
source_file: "[[Knowledge/source/...]]"
source_name:
author:
url:
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: initialized
---
```

实体页：

```yaml
---
type: entity
tags: [entity]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

概念页：

```yaml
---
type: concept
tags: [concept]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

综合页：

```yaml
---
type: synthesis
tags: [synthesis]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

对比页：

```yaml
---
type: comparison
tags: [comparison]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

查询页：

```yaml
---
type: query
tags: [query]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: archived
---
```

## 链接规则

- 使用 Obsidian Wiki 链接：`[[Knowledge/wiki/概念/上下文工程]]`。
- 链接到 vault 文件时使用相对 vault 根路径，不使用绝对路径。
- 重命名文件后必须批量更新所有 `[[...]]`。
- 响应用户时也尽量使用可点击 wikilink。

## 编码安全规则

中文内容必须按 UTF-8 写入。当前 Windows / PowerShell 环境中，直接用 PowerShell here-string、`Add-Content`、`Set-Content` 写中文容易产生问号乱码。

优先使用：

- `apply_patch` 修改 Markdown；
- 或创建 `.py` 脚本文件，再用 `Path.write_text(..., encoding="utf-8")` 写入；
- 或用 Python `read_text(..., encoding="utf-8")` 验证文件内容。

避免：

- 在 PowerShell 命令字符串中直接写大段中文；
- 用终端显示结果判断文件是否乱码。

每次批量写入后检查：

- 连续问号；
- Unicode 替换字符；
- 典型 mojibake 标记；
- 断链。

## 图片与附件

- `source/` 中的外部图片默认不批量下载，除非用户要求或该图对长期理解很关键。
- 如需本地化图片，下载到 vault 附件位置，并把 Markdown 改为 Obsidian 图片嵌入：`![[image.png]]`。
- 原始资料层默认只读；图片本地化或改写原始资料前应确认。

## 安全原则

- 不覆盖用户原始资料。
- 不删除非空目录，除非确认内容已迁移或用户明确要求。
- 批量移动、重命名前先制定映射；执行后检查断链。
- 用户明确偏好优先于本 schema，例如目录命名、报告是否保留、README 是否保留英文名。

# CHANGELOG

All notable changes to Synapse Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2026-04-08

### Changed
- **IM 平台友好输出** — 移除所有 ANSI 颜色码，适配 Telegram/微信/飞书等 IM 平台
- `run_pipeline.py` — 替换进度条为阶段通知（`log_stage_start`、`log_stage_complete`）
- `auto_log_trigger.py` — 移除 ANSI 颜色码，使用纯文本输出
- `check_status.py` — 移除 ANSI 颜色码，树形结构纯文本
- 新增 IM 友好日志函数：`log_info`、`log_success`、`log_warning`、`log_error`
- 使用 emoji + 纯文本格式：`[INFO]`、`[✓]`、`[⚠]`、`[✗]`、`[⟳]`

### Why
- OpenClaw 的 `chat.send` 流式传输到 IM 平台时 ANSI 码被过滤
- 聊天消息不可变，`\r` 进度条动画无效
- 改为每阶段开始/完成时输出独立消息，用户可感知进度

---

## [1.1.1] - 2026-04-08

### Fixed
- **lint_wiki.py 递归扫描子目录漏检** — 从 `.glob()` 改为 `.rglob()` 递归扫描
- **summaries 目录链接检查** — 使用文件名而非 frontmatter title（匹配 wikilink 格式）
- **Node.js v25 与 tree-sitter 兼容性** — package.json 添加 engines 限制（`node >=18 <25`）

### Changed
- `install.sh` — 添加 Node.js 版本检测和友好错误提示
- 提供 3 种解决方案：降级 Node.js、更新 tree-sitter、跳过 npm

---

## [1.1.0] - 2026-04-08

### Added
- **测试覆盖** — 18/18 测试通过（基线 7/7 + 集成 11/11）
- **文档完善** — 新增 5 篇文档（AGENT_GUIDE、TROUBLESHOOTING、BEST_PRACTICES、TESTING、ITERATION_LOG）
- **配置验证** — 启动时验证 config.json 有效性
- **进度可视化** — Pipeline 运行时显示进度条和阶段状态
- **结构化日志** — 支持 JSON 格式日志输出
- **安装增强** — install.sh 添加前置检查、交互提示、后验证

### Changed
- `run_pipeline.py` — 增强错误处理、6 阶段进度显示、错误阶段解析
- `check_status.py` — 树形结构状态显示、建议操作列表
- `auto_log_trigger.py` — 结构化日志输出

### Fixed
- `lint_wiki.py` — 支持 summaries 目录链接检查

---

## [1.0.0] - 2026-04-08

### Added

#### synapse-wiki (智能知识库管理系统)
- **核心功能**:
  - `wiki_init` — 初始化新的 Wiki 知识库
  - `wiki_ingest` — 摄取源文件创建 Wiki 页面
  - `wiki_query` — 查询知识并综合答案
  - `wiki_lint` — 健康检查（死链接、孤立页面等）
- **Scripts**:
  - `scaffold.py` — 引导新的 Wiki 目录树
  - `ingest.py` — 摄取新资料，编译为 Wiki 页面
  - `query.py` — 查询 Wiki，综合答案
  - `lint_wiki.py` — 健康检查（死链接/孤立页/矛盾）
- **Commands**: `init.sh`, `ingest.sh`, `query.sh`, `lint.sh`
- **Tests**: 基线测试 4/4 通过

#### synapse-code (智能代码开发工作流引擎)
- **核心功能**:
  - `pipeline_init` — 初始化项目的 Synapse + Pipeline 环境
  - `pipeline_run` — 运行 Pipeline 交付代码
  - `synapse_log` — 手动触发 Synapse auto-log
  - `impact_check` — 检查代码变更影响范围（内建 GitNexus）
  - `status_check` — 检查项目状态
- **Scripts**:
  - `init_project.py` — 初始化项目环境
  - `run_pipeline.py` — 运行 Pipeline 并自动触发 auto-log
  - `auto_log.py` — Synapse 自动记录脚本（内置）
  - `auto_log_trigger.py` — 触发 auto-log
  - `check_status.py` — 检查项目状态
  - `infer_task_type.py` — 根据描述推断 task_type
  - `query_memory.py` — 查询记忆记录
- **Commands**: `init.sh`, `run.sh`, `log.sh`, `status.sh`, `query.sh`, `infer.sh`, `parallel.sh`
- **Tests**: 基线测试 3/3 通过

### Changed

- synapse-code 的 `run_pipeline.py` 和 `auto_log_trigger.py` 现在支持配置文件
- 移除了硬编码路径，使用 `config.json` 或 `config.template.json`
- `auto_log.py` 从外部依赖（synapse-core）改为内置脚本
- GitNexus 改为 npm 依赖，安装时自动集成
- SKILL.md 描述优化，突出用户价值而非技术实现

### Removed

- 移除了对 `~/.claude/skills/synapse-core/scripts/auto_log.py` 的硬依赖
- 移除了全局 GitNexus CLI 依赖（改为内建）

### Fixed

- 配置化路径，支持用户自定义 Pipeline workspace 位置
- 增强错误处理和友好错误提示
- 安装脚本支持 --dry-run 和 --uninstall

### Security

- 无

---

## [0.1.0] - 2026-04-08 (Initial Draft)

### Added

- 初始版本创建
- 基线测试框架

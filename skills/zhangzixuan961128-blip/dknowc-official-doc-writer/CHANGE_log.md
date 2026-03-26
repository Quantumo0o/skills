# 更新日志

## [3.1.0] - 2026-03-23

### 同步内部版本更新

**从内部版本同步的功能改进：**

#### SKILL.md
- 搜索词构造：新增从用户输入自动提取核心关键词的规则和自检标准
- 素材分类标准：新增"允许的来源"列（国家级/本省 vs 其他省市），多地域搜索时按地域隔离展示
- 素材充分性自检：AI自动评估政策依据/数据支撑/参考案例覆盖度，不足则自主补搜（每维度最多1次，累计不超过3次）
- policyFiles按需补充：撰写时发现政策引用缺少文件全称/发文字号，AI自主用 --policy 参数补搜
- 知识专库链接即时发送：搜索完成后立即在对话中发送知识专库链接
- 引用示例通用化：移除所有具体单位名称引用
- 修正章节编号：5.1/5.2 → 统一为 5.1/5.2 识别文种，6.2 读取标准文件
- 红头文件支持：新增会议纪要（党组/局长办公/工作会议）红头模板说明

#### Scripts
- `dkag_search.py`：新增 --policy 参数（返回规范性文件清单 policyFiles）；保留 public 版的 api_url 可配置
- `format_document.py`：新增超链接支持（知识专库链接自动转为可点击链接）；新增主送机关长度过滤（>50字排除）；页边距支持四边分别配置（兼容统一边距）
- `template_generator.py`：全面升级，支持会议纪要红头/表尾模板；新增 WPS 文本框占位符替换；新增 --meeting-number/--attendees/--non-voting/--print-unit/--print-date/--cc 参数

#### Templates（新增）
- 党组会议纪要-{红头,表尾}.docx
- 局长办公会议纪要-{红头,表尾}.docx
- 工作会议纪要-{红头,表尾}.docx

#### Reference Standards
- `15_事务文书_模板.md`：简化，移除内联格式规范，改为引用 config/format.json（与内部版本一致）

#### 未同步（内部专用，不适合公开）
- `reference/单位简称对照表.md`
- `reference/广东省政数局公文格式标准.docx`
- `config/format.json` 页边距改回内部版（上37下35左28右26）—— public 保留 25mm 统一边距
- `config.ini` 含敏感 API Key —— public 使用 config.ini.example

---

## [3.0.0] - 2026-03-18

### 首个公开发布版本

**基于内部版本 v2.3.2 改造，主要变更：**

#### 架构调整
- 搜索模块可配置化：API Key 和 API URL 从 config.ini 读取
- 新增首次使用引导：检测配置状态，提示用户注册 MAAS 平台
- 移除硬编码单位信息，改为用户自定义

#### 文件变更
- `config.ini.example`：搜索配置模板（API Key 置空）
- 删除 `config.ini`（含敏感信息，不随 Skill 发布）
- 删除 `reference/单位简称对照表.md`（各用户单位不同，需自建）
- `format.json` 注释改为国标通用说明
- `scripts/format_document.py`：DEFAULT_ORG 和 DEFAULT_DOC_PREFIX 置空
- `scripts/dkag_search.py`：API URL 可配置
- 新增 `README.md`：安装说明和使用指南
- 新增 `.skillignore`：排除敏感配置文件

#### 内部版本继承功能
- 15种法定公文写作标准
- 事务文书模板
- Word排版（普通格式/红头格式）
- 版本号管理
- Markdown表格转Word原生表格
- 引用规范强制执行机制

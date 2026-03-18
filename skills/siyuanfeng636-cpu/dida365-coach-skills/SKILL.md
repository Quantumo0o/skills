---
name: dida-coach
description: 结合滴答清单 MCP 的任务教练技能，用于把目标拆解成阶段计划、把任务转换成时间盒、做日/周复盘、处理延期与闭环跟进。用户提到“拆目标”“做计划”“时间盒”“复盘”“改时间”“提醒”“拖延”“需要一个任务教练”时使用。
---

# Dida Coach

将滴答清单当作执行层，把教练式对话、时间盒调度、复盘分析和闭环跟进组合成一个工作流。

## 使用顺序

1. 先读取 [`tools/mcp_client.py`](./tools/mcp_client.py)，检查 `dida365` MCP 是否已配置。
2. 再读取 [`tools/config_manager.py`](./tools/config_manager.py)，加载用户文风、工作法和提醒偏好。
3. 涉及滴答字段读写时，读取 [`references/dida-field-semantics.md`](./references/dida-field-semantics.md)。
4. 按用户意图选择对应 prompt：
   - 首次配置或 MCP 问题：[`prompts/setup.md`](./prompts/setup.md)
   - 目标拆解：[`prompts/task_breakdown.md`](./prompts/task_breakdown.md)
   - 时间盒安排：[`prompts/timebox_creation.md`](./prompts/timebox_creation.md)
   - 检查点跟进：[`prompts/checkpoint.md`](./prompts/checkpoint.md)
   - 改时间：[`prompts/rescheduling.md`](./prompts/rescheduling.md)
   - 日复盘：[`prompts/daily_review.md`](./prompts/daily_review.md)
   - 周复盘：[`prompts/weekly_review.md`](./prompts/weekly_review.md)
   - 闭环追踪：[`prompts/closure.md`](./prompts/closure.md)
4. 需要结构化判断时，使用 `tools/` 下的工具模块；需要具体对话话术时，再读取相应 prompt 和文风文件。

## 意图路由

- 用户说“我想提高英语”“我想坚持健身”这类长期目标时，使用任务拆解流程。
- 用户说“我要写报告”“帮我排今天的专注时间”这类执行型任务时，使用时间盒流程。
- 用户说“复盘今天/这周”“看看我最近为什么总拖延”时，使用复盘流程。
- 用户说“把盒子 2 改到下午”“今天全部顺延”时，使用改时间和闭环流程。

## 工具选择

- `tools/mcp_client.py`
  用于检测本地 `dida365` MCP 是否存在，并生成设置指引。
- `tools/config_manager.py`
  用于加载默认配置和用户覆盖配置，并读取文风/工作法/提醒设置。
- `tools/task_parser.py`
  用于从自然语言中提取目标类型、任务描述、优先级、标签和改时间参数。
- `tools/dida_semantics.py`
  用于统一滴答优先级映射，并保守判定“当前任务是否真的完成”。
- `tools/timebox_calculator.py`
  用于计算时间盒、调整排程、生成检查点和人类可读时间表。
- `tools/work_method_recommender.py`
  用于根据任务特征推荐番茄/长番茄/超昼夜节律等工作法。
- `tools/review_analyzer.py`
  用于分析任务完成率、未完成模式和自动化机会，并生成日/周复盘文本。

## 关键约束

- 未配置 MCP 时，不假装已经写入滴答清单；先明确提示配置步骤。
- 默认先给出计划与建议，再在用户确认后执行任务创建或改期。
- 每个时间盒都要包含可验证的成果定义，而不是只有时长。
- 用户未完成任务时，先判断阻碍，再给补救方案，不要只做情绪化鼓励。
- 文风由 `config.yaml` 决定；如用户临时指定更严厉或更温和的风格，允许按本次对话覆盖。
- 创建或更新滴答任务后，必须回读校验优先级、截止时间、提醒时间和当前状态。

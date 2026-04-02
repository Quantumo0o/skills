---
name: self-reflection
description: |
  自我复盘与持续改进技能。当用户要求"复盘"、"总结经验"、"记录教训"、
  "自我提升"、"持续改进"、"错题本"、"学习日志"时触发。
  主动在每次完成任务、犯错、学到新知后，将内容写入 reflections/。
---

# 自我复盘与持续改进

## 与 AGENTS.md 的分工

根据 AGENTS.md 的 Memory 规则：
- `memory/YYYY-MM-DD.md` = 每日聊天记录（raw logs）
- `MEMORY.md` = 长期记忆（curated，核心精华）

**self-reflection skill** 负责：
- 错误和教训的**即时记录** → 追加到 `reflections/mistakes.md`
- 有效经验的**即时记录** → 追加到 `reflections/lessons.md`
- 从 mistakes.md / lessons.md 中提炼的精华，由 AGENTS.md 心跳维护机制定期合并到 MEMORY.md

## 文件位置

```
workspace/
├── memory/                    # 每日聊天记录（AGENTS.md 规定）
│   └── YYYY-MM-DD.md         # 每日聊天记录
└── reflections/              # 自我复盘（self-reflection skill 规定）
    ├── mistakes.md             # 错题本（核心文件，不新建其他文件）
    └── lessons.md            # 重要经验（核心文件，不新建其他文件）
```

**reflections/ 里不建每日文件**。发现错误/经验时，直接追加到 mistakes.md 或 lessons.md。

## 自动生成每日聊天记录

运行 `scripts/daily_reflect.py` 在 `memory/` 下生成当日聊天记录文件。

### 参数说明

```bash
# 首次安装后必须运行，设置每日执行时间
python3 scripts/daily_reflect.py --setup

# 查看定时任务状态
python3 scripts/daily_reflect.py --status

# 删除定时任务
python3 scripts/daily_reflect.py --remove

# 手动执行（生成今日聊天记录）
python3 scripts/daily_reflect.py
```

## 触发时立即记录

发现一个错误 → 立即追加到 `reflections/mistakes.md`
找到一个好经验 → 立即追加到 `reflections/lessons.md`
不要等，不要攒。

## 错题本格式（mistakes.md）

```markdown
| 日期 | 错误描述 | 类型 | 根本原因 | 解决方案 | 状态 |
|------|---------|------|---------|---------|------|
| YYYY-MM-DD | ... | 异常处理/配置错误/API调用/逻辑错误/习惯问题 | ... | ... | ✅已修复/❌未解决 |
```

- 同一个错误出现两次 → 标记「⚠️ 重复」→ 升级处理
- 类型：异常处理 / 配置错误 / API调用 / 逻辑错误 / 知识盲区 / 习惯问题

## 重要经验格式（lessons.md）

```markdown
## 技术类
- [具体经验 + 为什么有效 + 可复用场景]

## 方法论类
- [做事方法/思考方式 + 适用场景]

## 沟通类
- [与用户沟通的有效方式]
```

## 触发条件

以下情况必须触发记录：

1. 完成复杂任务后
2. 用户指出错误或问题时
3. 发现反复犯同一个错误
4. 学到新的有效方法/工具/认知
5. 每天对话结束时（至少有一条值得记录的内容时）

## 与心跳维护的关系（AGENTS.md 规定）

AGENTS.md 心跳维护流程：
> 定期读 memory/ 文件 → 提炼精华 → 更新 MEMORY.md

self-reflection 负责即时记录，AGENTS.md 心跳负责定期提炼。两个机制协同工作。

## 记录原则

- **具体**：「我做得好」不够，要写「因为用了什么方法，所以什么结果」
- **找根因**：「错了」不够，要写「犯错的直接原因和根本原因是什么」
- **可复用**：经验要抽象化，才能迁移到其他场景
- **不过度**：没有就不写，不要凑数

## 零门槛

- 不依赖任何外部 API / 凭据
- 纯 Markdown，任何编辑器都能打开
- 新 agent 只需知道 reflections/ 在哪，读 SKILL.md 后即可上手

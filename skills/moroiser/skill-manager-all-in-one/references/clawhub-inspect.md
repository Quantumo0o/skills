# ClawHub Inspect Guide | ClawHub 查看指南

## CLI basics | CLI 基础检查

Check current CLI behavior before sensitive operations. Do this again when you suspect the CLI has gained new commands or options.  
在执行敏感操作前，先检查当前 CLI 行为。如果怀疑 CLI 又新增了命令或参数，就再次检查。

```bash
clawhub --help
clawhub whoami
clawhub inspect <slug>
```

## Tool choice | 工具选择

Do not assume one tool is always best.  
不要预设某个工具永远最好。

Check the current CLI help first, because the CLI can gain new commands and options over time. Then choose CLI or Dashboard based on the task at hand.  
先检查当前 CLI help，因为 CLI 会持续增加新命令和新参数。然后再根据眼前任务选择 CLI 或 Dashboard。

## Tool selection after checking help | 查看 help 后再选工具

Use Dashboard when you need:  
以下场景可用 Dashboard：
- reviewing all published skills at a glance  
  一眼查看全部已发布技能
- checking visible card summaries  
  查看卡片摘要信息
- checking scan state and overview information  
  查看扫描状态和概览信息

Use CLI when you need:  
以下场景可用 CLI：
- single skill details  
  单个技能详情
- current latest version  
  当前最新版本
- file lists  
  文件列表
- direct metadata lookup  
  元数据直接查询
- repeatable checks and scripted workflows  
  需要可重复检查或脚本化流程时

Useful commands | 常用命令:

```bash
clawhub inspect <slug>
clawhub inspect <slug> --tag latest
clawhub inspect <slug> --version 1.0.0
clawhub inspect <slug> --versions --limit 20
clawhub inspect <slug> --files
clawhub inspect <slug> --file SKILL.md
clawhub inspect <slug> --json
```

## Local directory vs CLI list | 本地目录与 CLI list 的区别

A skill copied manually into `~/.openclaw/skills/` may exist locally but still not appear in `clawhub list`.  
手工复制进 `~/.openclaw/skills/` 的技能，可能本地存在，但仍不会出现在 `clawhub list` 中。

`clawhub list` reports installed skills from the CLI lockfile view, not every folder that happens to exist under the skills directory.  
`clawhub list` 展示的是 CLI lockfile 视角下的已安装技能，而不是简单扫描技能目录里的所有文件夹。

Use both checks when needed:  
需要时，两个检查都要做：
- inspect the local directory directly  
  直接检查本地目录
- use `clawhub list` when the question is about CLI-managed installs  
  当问题涉及 CLI 管理安装时，再使用 `clawhub list`

## Login note | 登录说明

Browser login and CLI login are separate states. If CLI reports `Not logged in`, run:  
浏览器登录和 CLI 登录是两套状态。如果 CLI 提示 `Not logged in`，执行：

```bash
clawhub login
clawhub whoami
```

## Status meanings | 状态含义

- `Scanning`: security scan in progress  
  `Scanning`：安全扫描进行中
- `Pending`: result not fully stable yet  
  `Pending`：结果尚未完全稳定
- `Benign`: generally passed scan  
  `Benign`：基本通过扫描
- `Suspicious`: needs review  
  `Suspicious`：需要人工复核
- `Hidden`: not publicly visible  
  `Hidden`：当前不公开显示

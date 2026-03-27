# Markdown AI Rewriter Skill

面向 **Claw Hub** 等环境的 Skill 封装，底层使用 npm 包 **[markdown-ai-rewriter](https://www.npmjs.com/package/markdown-ai-rewriter)**（当前对齐 **v0.2.2**）：在 **尽量保留标题、代码块、表格、图片等结构** 的前提下，对 Markdown 正文做润色、降重或换表述。

- **npm 包源码与发版**：[github.com/sipingme/markdown-ai-rewriter](https://github.com/sipingme/markdown-ai-rewriter)  
- **本 Skill 文档**（模式、参数、排错）：请读本仓库 **[SKILL.md](./SKILL.md)**

### Git 克隆

| 仓库 | HTTPS | SSH（示例） |
|------|--------|-------------|
| **本仓库**（Skill、`SKILL.md` / `README.md`） | `https://github.com/sipingme/markdown-ai-rewriter-skill.git` | `git@github.com:sipingme/markdown-ai-rewriter-skill.git` |
| **markdown-ai-rewriter**（npm 包、CLI 与 TypeScript 源码） | `https://github.com/sipingme/markdown-ai-rewriter.git` | `git@github.com:sipingme/markdown-ai-rewriter.git` |

```bash
# 克隆本 Skill 仓库
git clone https://github.com/sipingme/markdown-ai-rewriter-skill.git
cd markdown-ai-rewriter-skill

# 克隆底层 npm 包（如需改代码或本地联调）
git clone https://github.com/sipingme/markdown-ai-rewriter.git
```

版本与发版以各仓库 **`main`** 分支及 npm 上 **`markdown-ai-rewriter`** 的版本号为准。

---

## 能力概览

| 维度 | 说明 |
|------|------|
| **改写模式** | **`section`（章节，默认）**：按标题分章并行；**`full`（全文）**：整篇一次，语气更连贯。已移除旧的「按段落块」模式。 |
| **模型提供商** | **OpenAI**、**Anthropic**、**MiniMax**（MiniMax 使用 OpenAI 兼容 HTTP，需安装 `openai` 包）。 |
| **风格** | `casual` / `formal` / `technical` / `creative` / `custom`（`custom` 常配合自定义 `--prompt`）。 |
| **结构** | 解析与重组逻辑尽量保留版式；全文模式下对图片有占位符保护机制（详见包文档）。 |
| **并发** | 章节模式下 **`--concurrency`（`-c`）** 控制并行请求数。 |

---

## 前置条件

- **Node.js** ≥ 18，**npm** ≥ 8（与 [SKILL.md](./SKILL.md) 一致）。
- **API Key**（按实际选用的 `-p` 提供商配置其一或多项）：

| 用途 | 环境变量 |
|------|----------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| MiniMax | `MINIMAX_API_KEY`（可选 `MINIMAX_BASE_URL`，默认多为国际区 `https://api.minimax.io/v1`） |

在 **Claw Hub** 中配置一次后，各 Skill 可共享同一环境变量。

安装各厂商 SDK（与包 `peerDependencies` 一致）：

```bash
npm install openai                    # OpenAI 与 MiniMax 共用
npm install @anthropic-ai/sdk         # 仅 Anthropic
```

---

## 安装 CLI

```bash
npm install -g markdown-ai-rewriter
```

全局安装后可使用命令 **`markdown-ai-rewrite`** 或 **`md-rewrite`**。

---

## 最小示例（命令行）

```bash
# 章节模式（默认）+ OpenAI + 轻松风格
export OPENAI_API_KEY="sk-..."
markdown-ai-rewrite rewrite -i input.md -o output.md -p openai -s casual -v

# 全文模式（短文、强叙事）
markdown-ai-rewrite rewrite -i input.md -o out.md -p openai --mode full

# 按二级标题分章
markdown-ai-rewrite rewrite -i input.md -o out.md -p openai --section-level 2

# MiniMax
export MINIMAX_API_KEY="..."
markdown-ai-rewrite rewrite -i input.md -o out.md -p minimax -m MiniMax-M2.1 -s casual
```

更多参数（`-t`、`--max-tokens`、`--preserve-length`、`-c`、`--minimax-base-url` 等）见 **`markdown-ai-rewrite rewrite --help`** 与 [SKILL.md](./SKILL.md)。

---

## 与 AI 对话时怎么说（Claw Hub）

可直接描述意图，由助手按需调用本 Skill 相关能力，例如：

- 「把这篇 `article.md` 改成正式商务风格，结构别乱。」
- 「按章节改写，并发别太高。」
- 「全文一口气改写，保持叙事连贯。」
- 「用 MiniMax / OpenAI / Claude 其中之一改写。」

不涉及「从零写长文」「只做 MD↔HTML 转换」等场景时，更适合用本 Skill；若需完整触发条件与反例，见 [SKILL.md](./SKILL.md)。

---

## 仓库结构（本 Git 仓库）

| 文件 | 作用 |
|------|------|
| [SKILL.md](./SKILL.md) | Skill 完整规范：模式、环境变量、API、FAQ、维护信息 |
| [README.md](./README.md) | 本页：快速了解能力与安装入口 |

---

## 许可证

MIT

## 作者

Ping Si <sipingme@gmail.com>

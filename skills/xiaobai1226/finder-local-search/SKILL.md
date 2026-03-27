---
name: finder-local-search
description: 当用户想在 Codex、Claude 或其他支持技能的环境里搜索 Finder 达人时使用，尤其适用于“搜达人”“找英国/美国/某地区达人”“按关键词、地区、语言、标签、粉丝区间筛选达人”“继续上次项目搜索”“首次配置 Finder API key”这类请求。优先自动执行 Finder HTTP 请求；只有当前环境无法执行时，才退回到可复制的 curl 或 PowerShell 命令。
---

# Finder 本地搜索

这个 skill 通过 Finder 开放接口调用普通达人搜索能力。

当用户希望在当前对话环境里直接得到 Finder 搜索结果，并且当前环境支持执行命令或网络请求时，优先使用这个 skill。

## 前置条件

- 默认服务地址为 `https://finder.optell.com`。
- 用户需要先登录 Finder，并在 `/api-key` 页面生成访问密钥。
- 推荐把访问密钥持久化保存到环境变量：
  - macOS / Linux：`export FINDER_API_KEY="<api_key>"`
  - Windows PowerShell：`$env:FINDER_API_KEY="<api_key>"`

- 如果缺少访问密钥，先停止执行搜索，并明确引导用户注册或登录、打开 `/api-key` 页面、生成密钥、再设置环境变量。
- 如果用户已经在对话里直接贴出了 `api key`，不要再让他手动重复复制。优先直接帮他保存，并继续当前流程。
- 如果当前环境可以直接执行命令或发起 HTTP 请求，优先自动执行。
- 如果当前环境不能自动执行，给用户可复制的 `curl` 或 PowerShell 命令。

## 首次使用引导

当用户第一次使用这个 skill 时，优先按下面顺序引导：

1. 检查当前环境里是否已经有 `FINDER_API_KEY`。
2. 如果没有访问密钥，明确告诉用户：
   - 先注册或登录 Finder
   - 打开 `https://finder.optell.com/api-key`
   - 生成并复制访问密钥
   - 如果用户把 key 贴在对话里，直接帮他设置环境变量
3. 用户完成后，再继续当前搜索流程，不要让用户重新描述一次需求。
4. 先调用 `POST /api/project/list` 检查有没有项目。
5. 如果没有项目，先解释“Finder 的普通达人搜索依赖项目”，征求确认后再创建默认项目。

如果用户还没有注册账号，直接引导他先去 Finder 完成注册/登录，不要假设本地已经有可用账号。

## 对话风格

- 语气要像在带用户一步步完成配置，而不是在报错。
- 首次使用时，优先告诉用户“我先帮你检查一下”，降低阻力。
- 需要用户操作时，一次只给当前最重要的一步，不要同时塞太多信息。
- 用户已经做完一部分时，先确认进度，再继续后面的动作。
- 如果已经拿到 `api key` 并保存成功，要明确告诉用户“后面不用再重复输入这串 key 了”。
- 说明项目依赖时，强调这是为了保存搜索上下文，不要让用户感觉是额外负担。

## 工作流

1. 检查是否已经设置 `FINDER_API_KEY`。
2. 如果认证未就绪，引导用户：
   - 打开 Finder 登录
   - 打开 `/api-key`
   - 生成并复制访问密钥
   - 如果用户贴出 key，优先直接帮他保存到环境变量
   - 如果环境支持命令执行，优先使用当前系统的持久化命令
   - 如果环境不支持，再给一条可复制命令
3. 读取共享条件词典 `references/filters.json`。
4. 把用户需求转换为结构化搜索参数：
   - `platform`
   - `keyword`
   - `regions`
   - `languages`
   - `labels`
   - `minFollowerCount` / `maxFollowerCount`
   - `minAvgPlay` / `maxAvgPlay`
   - `minEngagementRate` / `maxEngagementRate`
5. 确保项目存在：
   - 先调用 `POST /api/project/list`。
   - 如果没有可用项目，先解释“Finder 的普通达人搜索依赖项目”。
   - 先征求确认，再创建项目。
   - 用户确认后调用 `POST /api/project/create`，必要时再调用 `POST /api/project/select`。
6. 用 JSON 参数执行搜索：
   - 调用 `POST /api/creator/search`
   - 如果当前环境不能自动调用，就给出当前系统可复制的请求命令：
     - macOS / Linux：`curl`
     - Windows：PowerShell `Invoke-RestMethod`
7. 用自然语言总结结果，并保留结构化结果。

## 交互规则

- 只追问真正影响结果的缺失条件，例如平台、地区、语言、粉丝量级。
- 如果用户提出“适合带货的达人”这类模糊目标，只追问最少必要信息。
- 如果结果为空，明确说明“没有匹配达人”，并建议放宽一到两个条件。
- 不要虚构不受支持的筛选项。
- 不要调用相似达人搜索；这个 skill 当前只支持普通达人搜索。
- 如果发现用户尚未注册、未登录、未配置访问密钥，优先做引导，不要直接报错结束。
- 如果环境支持自动执行命令或 HTTP 请求，直接执行；如果不支持，再退回手动命令引导。
- 如果用户在对话里直接提供了访问密钥：
  - 不要在后续回复中重复展示完整 key。
  - 优先帮用户持久化保存，避免后续每次都重复输入。
  - macOS / Linux 优先追加到 `~/.zshrc`，如果不存在再尝试 `~/.bashrc`，并在当前命令里立即 `export FINDER_API_KEY=...`。
  - Windows PowerShell 优先执行 `[Environment]::SetEnvironmentVariable(\"FINDER_API_KEY\", \"<api_key>\", \"User\")`，并同时执行 `$env:FINDER_API_KEY=\"<api_key>\"`。
  - 保存成功后，直接继续当前搜索流程。
- 引导文案优先使用中文，简短直接，告诉用户下一步要做什么。
- 推荐使用下面这种更友好的表达：
  - 首次检查：`我先帮你检查一下 Finder 配置。`
  - 未配置 key：`我还没有找到 Finder 访问秘钥。你先去 https://finder.optell.com/api-key 生成一份，拿到后直接发给我就行，我可以继续帮你接着配。`
  - 已保存 key：`我已经帮你保存好了，后面就不用再重复输入这串 key 了。`
  - 没有项目：`Finder 会把这次搜索挂在一个项目下面，方便你后面继续查看和筛选。你现在还没有项目，要我顺手帮你建一个默认项目吗？`
  - 无结果：`这组条件下我还没找到合适的达人。我们可以先放宽一下关键词或地区范围，我继续帮你找。`

## 参考文件

- 安装与配置说明：`references/config.md`
- 搜索词典与别名：`references/filters.json`
- 示例对话：`references/examples.md`

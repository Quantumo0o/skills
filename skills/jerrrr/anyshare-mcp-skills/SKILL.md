---

## name: anyshare-mcp-skills
description: "AnyShare 智能知识管理技能。支持：搜索文件、上传/下载文件、分享链接读取、全文写作（生成大纲→确认→写正文）。触发词：AnyShare、asmcp、文档库、文件管理、知识库、anyshare.aishu.cn 分享链接。"
homepage: "[https://anyshare.aishu.cn](https://anyshare.aishu.cn)"
metadata: '{"openclaw":{"category":"productivity","emoji":"📁","requires":{"bins":["mcporter"]},"openclawSkillsEntryFile":"openclaw.skill-entry.json"}}'

# AnyShare MCP 技能

> **首次使用本技能时，配置步骤的权威来源是 [setup.md](setup.md)。**
> SKILL.md 只做摘要+跳转，**配置细节以 setup.md 为准**（避免两处表述漂移）。

---

## ⚠️ 执行前必读

### 强制前置阅读（按需必读，否则跳过）


| 操作 | 必须先读 | 为何 |
| --- | --- | --- |
| 首次使用本技能（配置 asmcp.url） | **[setup.md](setup.md)** 全章 | 配置唯一权威；含 mcporter.json、daemon 重启、openclaw.json 合并、企业地址确认话术 |
| 配置或核对 token（凭证） | **本 SKILL.md** → **「凭证（Token）」**、**「获取凭证（固定提示语）」** | 用户按固定提示语取 token 后在对话中**粘贴**；Agent **`auth_login`** 并维护技能根目录备份 |
| 调用任何业务工具（file_search / upload / download 等）前 | **本 SKILL.md** → **「本技能工具与 mcporter 调用」**及对应场景步骤 | 参数格式（key=value）、固定字段、禁止传参 |
| 解析分享链接 | **本 SKILL.md** → **「本技能工具与 mcporter 调用」**→ `sharedlink_parse` 与 **「📎 分享链接（从 URL 到 docid）」** | **`link_id`**、**`item.id`**、顶层 **`id`**（见 C7） |
| **进入场景四（全文写作）前** | **本 SKILL.md** → 场景四 → C8 进门卡点 | 须已能确定 docid 及 `source_ranges` 所用 id（docid 最后一段，见核心概念）；否则先 `file_search` 或分享链流程，禁止绕过（C8） |
| 排障 / 401 / 认证失败 | **[references/troubleshooting.md](references/troubleshooting.md)** | 错误码含义、常见现象与处理方式 |


### 硬卡点表


| # | 规则 | 关联场景 |
| --- | --- | --- |
| C1 | 搜索文件**只用 `file_search`**，禁止 RAG 类工具或目录树展开 | 场景一 |
| C2 | 展示搜索/列目录结果前，**必须先调 `file_convert_path` 再输出**（禁止跳过） | 场景一、[分享链接](#分享链接从-url-到-docid) |
| C3 | 上传/下载前，**必须用户明确回复"是"确认 docid**，禁止代选 | 场景二、场景三 |
| **C4** | **大纲未确认前禁止调用 `__大纲写作__1`**（大纲门闩） | 场景四 |
| **C5** | `source_ranges[].id` **必须传 id**（docid 最后一段），禁止传完整 docid | 场景四 |
| **C6** | 用 **`sharedlink_parse(link_id)`** 解析分享链；**`link_id`** 从用户 URL 中 **`/link/`** 路径段之后**原样提取** | [分享链接](#分享链接从-url-到-docid) |
| **C7** | **`docid`** = 响应 **`item.id`**（`gns://…`）；顶层 **`id`** 为分享链自身 id，**不等于** `item.id` | [分享链接](#分享链接从-url-到-docid) |
| **C8** | **进入全文写作前**须已定位目标文档：**至少掌握 docid（`gns://…`）或能唯一推出 `source_ranges[].id`（docid 最后一段）**。尚无则须先 **`file_search`** / [分享链接](#分享链接从-url-到-docid) / 用户提供 **docid** 等，禁止无文档锚点即调用 `smart_assistant` 或对话内代写 | 场景四 |
| **C9** | **在场原则**：持有 docid 后，阅读/写作/导出等须走 AnyShare 工具链，**禁止下载到本地后用外部工具替代**。**例外**：**场景三** 用户明确要求下载（**C3**）；**场景四** 抢先下载见 **C10**。C8 管入口，C9 管不跳出，C10 管全文写作工具顺序 | 所有含 docid 的场景 |
| **C10** | **全文写作**：已取得 **`source_ranges`** 所需 **id** 后，**下一步必须直接调用 `smart_assistant`（`__全文写作__2`）**。**禁止**为「先读原文 / 了解内容」而先调 **`file_osdownload`** 或离线下载再自行撰写；文档上下文由 **`source_ranges`** 在 **`smart_assistant`** 内注入，无需先拉取本地副本 | 场景四 |
| **C11** | **禁止**调用 **`file_upload`**（即使 `mcporter list asmcp` 仍列出该工具也不得使用）。上传**仅**允许 **`file_osbeginupload` → 按返回的 `authrequest` 对对象存储 HTTP PUT 文件体 → `file_osendupload`**；**PUT 未成功则禁止调用 `file_osendupload`** | 场景二 |


---

## 🔄 完整执行流程

> **分支优先级**：用户消息里若出现 **`https://…/link/…`**（或文档域下等价分享 URL），**先走「分享链接」分支**，再判断书写类、搜索等；避免把「带链接 + 让写稿」误判为纯全文写作而跳过解析。

```
用户输入
  │
  ▼
① 首次使用？── 是 ──→ 阅读 setup.md，执行 Step 1~4
  │                   → 向用户汇报 asmcp.url + 连通性
  │                   → 确认是否为**本企业**正式端点
  否
  ▼
② 凭证检查（自动）── 未 auth_login 或 token 失效 ──→ **提示用户重新配置凭证**（**「获取凭证（固定提示语）」** → 用户粘贴 → **`auth_login`**）──→ 重试至可用
  │                                           │
  │ 通过 ◀────────────────────────────────────┘
  ▼
③ 意图识别
  │
  ├─ 含 `/link/` 的分享 URL？── 是 ──→ 「📎 分享链接（从 URL 到 docid）」：`sharedlink_parse` → docid / id
  │
  ├─ 书写类诉求？（生成/撰写/改写/续写/润色/文章/报告/文案/大纲/材料）── 是 ──→ 确认全文写作？
  │                                                                         │
  │                                                    是 ◀─────────────────┘
  │                                                    ▼
  │                                              ⚠️ C8 强制预检：
  │                                              "是否已掌握 docid 及 source_ranges 所用 id？"
  │                                              否 ──→ 场景一（关键词搜索）获取 docid
  │                                              │        或「分享链接（从 URL 到 docid）」流程获取 docid
  │                                              │        获取后返回此节点重新判断
  │                                              是
  │                                              ▼
  │                                              场景四：全文写作
  │                                              ① docid/id → ② 大纲 → ③ 确认 → ④ 正文
  │
  │                                              否 ──→ 非书写类：按场景一～三分流，或结束本技能（若本句仍含 `/link/`，应先满足上行分享链接分支）
  │
  ├─ 搜索 / 查看文件 ──→ 场景一
  │
  ├─ 上传文件 ──→ 场景二
  │
  └─ 下载文件 ──→ 场景三
```

## 凭证（Token）

### 获取凭证（固定提示语）

需要请用户去 AnyShare 取 token 时，**统一使用下面话术**（可微调用词，**不得**改掉「用户设置」「MCP 授权凭证」等路径信息）：

> 请在 AnyShare **登录后**打开 **用户设置**，进入 **「MCP 授权凭证」**；在此可**管理、赋值**凭证。复制令牌后，**在本对话中粘贴**。

**用户**：按上式取得 token 后，**只在对话里粘贴**即可，**不必**也不应被要求自行建文件、改权限或「把 token 存到某路径」。

**Agent**：对用户粘贴的 **token** 调用 **`auth_login`**；参数为 **token 本体**（不含 `Bearer ` 前缀，以 **`mcporter list asmcp`** 的 schema 为准）。**`auth_login` 成功后必须**在本技能**根目录**（与 **`SKILL.md`、`mcp.json` 同级）写入**单行**纯文本备份（建议文件名 **`token.backup`**，已列入本包 **`.gitignore`**），并对该文件执行 **`chmod 600`**。登录态只存在于 **mcporter / MCP / asmcp 当前会话**，daemon 重启或长时间不用后若需恢复：**先**读该备份文件再 **`auth_login`**；若无备份、或备份仍失败，**请用户按「获取凭证（固定提示语）」** 重新取 token 并在对话里粘贴，并**覆盖**备份后重试。

```bash
mcporter call asmcp.auth_login token="<token>"
mcporter call asmcp.auth_status   # 可选
```

**使用前**：若尚未有效登录，向用户发出 **「获取凭证（固定提示语）」** 中的话术，待用户粘贴 token 后由 Agent 执行上式并完成**备份**。

**token 失效**（**`auth_login` / `auth_status` 失败**、业务 **401 / 未授权**）：**提示用户重新配置凭证**——先发 **「获取凭证（固定提示语）」** 中的话术，待用户粘贴后再由 Agent **`auth_login`** 并更新技能根目录备份。若判断仅为会话丢失且备份文件仍代表有效 token，可先读备份再 **`auth_login`**；仍失败再发固定提示语请用户取新 token 并粘贴。

**安全**：勿将 token 写入仓库、公开渠道或聊天记录；命令行传入可能进入 Shell 历史；Agent 勿在回复中完整回显 token。详见 **[SECURITY.md](SECURITY.md)**。

---

## 📌 核心概念

### docid 与 id

概念：`docid = gns://<库ID>/<父目录ID>/.../<id>`，其中 **最后一段**为 **id**。

下面用**纯 ASCII 示例**画对齐（避免中英混排导致等宽字体下箭头错位）：

```
gns://E6D15886/A51FA4844/2DDD46B195F24BCEB238DB59151CD15E
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         id（最后一段）
```


| 字段 | 是什么 | 示例 |
| --- | --- | --- |
| **docid** | 完整路径，gns:// 开头 | `gns://E6D15886.../A51FA4844.../2DDD46B195F24BCEB238DB59151CD15E` |
| **id** | docid 的最后一段 | `2DDD46B195F24BCEB238DB59151CD15E` |
| **parent_path** | docid 去掉最后一段 | `gns://E6D15886.../A51FA4844.../` |


**传参规则（工具调用时）：**


| 工具 | 参数 | 传什么 |
| --- | --- | --- |
| `smart_assistant` | `source_ranges[].id` | **id**（最后一段） |
| `folder_sub_objects` | `id` | **完整 docid** |
| `file_osdownload` | `docid` | **完整 docid** |
| `file_osbeginupload` | `docid` | **完整 docid**（目标**目录**）；另需 `name`、`length` |
| `file_osendupload` | `docid`、`rev` | **`docid`**、`rev` 均取自 **`file_osbeginupload`** 成功响应（新文件 docid，与目标目录 docid 不同） |
| `file_convert_path` | `docid` | **完整 docid**（仅用于展示 namepath） |
| `file_search` | — | 不需要手动拼接 |
| `doc_lib_owned` | 通常 `{}` | 返回中取目标文档库的 **`id`**（完整 `gns://…`），常作上传目标**目录** docid |


### sharedlink 解析

分享链接格式：`https://anyshare.aishu.cn/link/<link_id>`（`<link_id>` 为 SharedLink 唯一标识，如 `AR…` 段）。

**解析步骤（概念摘要）：**

1. 从 URL 取 **`link_id`**：`/link/` 路径后的那一段。
2. 调用 MCP 工具 **`sharedlink_parse`**，传入 `link_id`。
3. 从响应中读取 **`item.id`** → 即完整 **docid**（`gns://…`）；取最后一段 → **场景四 `smart_assistant` 用的 id**。
4. 根据 **`item.type`** 做 **folder / file 分流**（见 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)**）。

响应典型含：`type`（如 `realname`）、顶层 `id`（分享链 id）、**`item.id`**（文档 docid）；**docid 以 `item.id` 为准**。**入参/出参 JSON** 见 **「本技能工具与 mcporter 调用」→ `sharedlink_parse`**。**完整操作顺序与分流**见 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)**。

### namepath

`file_convert_path(docid)` 返回的 **`namepath`** 是 AnyShare 知识库展示用路径，如 `库名/文件夹/文件名`。**仅供阅读**，不得当作 docid 传参。

### 文件与文件夹判断

判断对象是文件还是文件夹：**看 `size = -1` 即为文件夹**（最可靠依据），而非 `doc_type` 或 `extension`。

### skill_name（全文写作）

以 `mcporter list asmcp` 返回的 schema 为准，不做假设。场景四全文写作当前已知：

- `__全文写作__2` — 生成大纲
- `__大纲写作__1` — 基于大纲生成正文

---

## 🏛️ AnyShare 在场原则（System-Internal-Only Principle）

> **这是本技能最根本的运行假设，所有场景均以此为前提。**

### 原则内容

**一旦通过 AnyShare 系统获取到 docid，该文档的所有后续操作都必须通过 AnyShare 工具完成，禁止跳出系统处理。**

换言之：

- ✅ 持有 docid → 需基于该文档的正文类能力（含全文写作）一律 **`smart_assistant`** + **`source_ranges`**，**禁止**在对话内直接长文替代
- ✅ 持有 docid → 用 `file_convert_path`（查看路径）
- ✅ **仅**在 **场景三（下载）** 且用户已确认（**C3**）时 → 用 `file_osdownload`；非下载场景勿用下载代替 `smart_assistant`
- ❌ **场景四（全文写作）**：已持 **`source_ranges`** 所需 **id** 却先 **`file_osdownload`** 再读本地/自行发挥 → **跑偏**；应先 **`smart_assistant`**（**C10**）
- ❌ 持有 docid，却去下载文件到本地后用外部工具（markitdown、LLM 直接总结等）"替代" AnyShare 工具链 → **在场原则违规**

### 为什么这条原则重要

docid 是文档在 AnyShare 系统内的"在场证明"。AI 一旦持有 docid，意味着文档已经在 AnyShare 的管理范围内。跳出系统去处理，等于放弃了 AnyShare 已有的权限管控、操作审计、内容安全策略，是系统性风险。

### 典型失控模式（供自检）


| 失控模式 | 常见原因 | 正确做法 |
| --- | --- | --- |
| 下载后用 markitdown 等**外部工具**处理云端文档 | 误以为离线解析更好 | `smart_assistant` + `source_ranges` |
| **无 docid/id** 却在对话内长文总结或代写 | 图快、跳过 A/B/C | 先取得 docid 与 **id**（**C8**），再走工具链 |
| 已持 docid 却改查本地路径、遗忘云端锚点 | 注意力漂移 | 回到 **docid**，继续 AnyShare 工具 |
| 全文写作已取 **id**，却先 **下载** 再写 | 误以为要先读全文 | **C10**：下一步即 `smart_assistant`（`__全文写作__2`），禁止先 `file_osdownload` |


### 在场原则与 C8 / C10 的关系

**C8** 约束「进入全文写作前是否已掌握 **docid / id**」。**C10** 约束「已持 **id** 后**第一步**须为 `smart_assistant`（大纲），禁止先下载」。**C9** 约束「不下载后用外部手段替代工具链（**场景三下载**与 **C10** 除外）」。顺序：**入口（C8）→ 工具顺序（C10）→ 不跳出（C9）**。

---

## 🔧 本技能工具与 mcporter 调用

> 本节列出本技能会用到的 MCP 工具：**入参 JSON、成功返回要点、mcporter 命令示例**。业务场景中的**流程与卡点**见下文各场景；**参数与响应体结构以本节为准**，场景内仅作链接引用。

### mcporter 调用规范

**参数格式**：`key=value`，**不是** `--key value`

- ✅ `mcporter call asmcp.file_search keyword="文档" type="doc" start=0 rows=25`
- ❌ `mcporter call asmcp.file_search --keyword 文档`

**超时配置**：`smart_assistant`（场景四全文写作）需要 10 分钟超时，在 `~/.openclaw/openclaw.json` 的 `skills.entries["anyshare-mcp-skills"].env` 中设置 `MCPORTER_CALL_TIMEOUT=600000`（毫秒）。兜底：单次 `mcporter call` 末尾加 `--timeout 600000`。

### file_search

```json
{
  "name": "file_search",
  "arguments": {
    "keyword": "<用户关键词>",
    "type": "doc",
    "start": 0,
    "rows": 25,
    "range": [],
    "dimension": ["basename"],
    "model": "phrase"
  }
}
```

**固定字段**（不许改）：`type="doc"`, `dimension=["basename"]`, `model="phrase"`

**动态字段**：仅 `keyword`、`start`、`rows`、`range`（4 个）

**不传字段**：`condition`、`custom`、`delimiter` 等可能导致服务端报错，一律不传

**返回结构**：响应内容在 `result.files` 数组（不是 `data`），每项含 `basename`、`size`、`extension`、`doc_id`、`parent_path`、`highlight` 等。

**分页**：`rows` 上限 25；下一页将 `start` 设为上次响应的 `next` 值。

### folder_sub_objects

```json
{
  "name": "folder_sub_objects",
  "arguments": {
    "id": "<docid（完整路径）>",
    "limit": 1000
  }
}
```

**传完整 docid**，不传 id（最后一段）。

### doc_lib_owned

查询当前用户拥有的文档库列表（含**个人文档库**等）。**无必填参数**时可传空对象。

```json
{
  "name": "doc_lib_owned",
  "arguments": {}
}
```

**输出**：JSON 数组，每项含 `id`（文档库根 **docid**）、`name`、`type`（如 `user_doc_lib` 表示个人文档库）等；字段以实际返回为准。

**返回示例：**

```json
[
  {
    "created_at": "",
    "creator_id": "",
    "creator_name": "",
    "id": "gns://F3E37AFXXXXX407B983F857779332AFB",
    "modified_at": "",
    "name": " xxx",
    "type": "user_doc_lib"
  }
]
```

**典型场景**：用户说「上传到**我的个人文档库**」并给出本地文件路径时，可先调本工具列出文档库，用 **`type`** 为 **`user_doc_lib`**（或用户点名的库名对应项）的 **`id`** 作为 **`file_osbeginupload`** 的 **`docid`**（目标目录），再按场景二走 **`file_convert_path`** 确认（C3）与分步上传。**不要**用用户本机路径当 AnyShare 知识库 docid。

**mcporter 示例：**

```bash
mcporter call asmcp.doc_lib_owned
```

### file_osdownload

```json
{
  "name": "file_osdownload",
  "arguments": {
    "docid": "<docid（完整路径）>"
  }
}
```

**场景四（全文写作）**：取得 **`source_ranges`** 所需 **id** 后**不要**用本工具「先拉全文再写」——下一步应直接 **`smart_assistant`**（**C10**）。本工具用于 **场景三** 等**明确下载**诉求。

### file_osbeginupload

初始化直传（`POST /efast/v1/file/osbeginupload`）。**`name`**、**`length`** 须与实际上传文件一致（`length` 为字节数，>0）。**目标目录**为 **C3** 用户确认后的 **`docid`**。

```json
{
  "name": "file_osbeginupload",
  "arguments": {
    "docid": "gns://F3E37AFXXXXX407B983F857779332AFB/3C29513ABFA240F4AFC4227EB8503B21",
    "name": "example.txt",
    "length": 4
  }
}
```

**返回（节选）**：含 **`authrequest`**（字符串数组）、**`docid`**（上传后的新文件 docid）、**`name`**、**`rev`** 等。示例：

```json
{
  "authrequest": [
    "PUT",
    "https://obs.cn-east-3.myhuaweicloud.com:443/obs-as7feijiegouzhengshihuanjing/013c7296-9b20-4572-9657-c68e93e5d476/F3E37AFXXXXX407B983F857779332AFB/ED815F2CA22840418A0F6BC42F4D1DA1",
    "Authorization: AWS VXGFIHWYOESD3UA40XFF:z9+FjJWOZDjey/ey0bM4QSveoa0=",
    "Content-Type: application/octet-stream",
    "x-amz-date: Wed, 25 Mar 2026 08:40:47 GMT"
  ],
  "docid": "gns://F3E37AFXXXXX407B983F857779332AFB/3C29513ABFA240F4AFC4227EB8503B21/F3A2F10333564DB399D8E0500B65F1FB",
  "name": "example.txt",
  "rev": "ED815F2CA22840418A0F6BC42F4D1DA1"
}
```

### 对象存储直传 PUT

`authrequest`：**第 0 项**为 HTTP 方法（如 `PUT`），**第 1 项**为对象存储 URL，**第 2 项起**为请求头，形如 `Header-Name: value`。**请求体**为待上传文件的**原始字节**。此步**不是** MCP 工具调用；须在 **运行环境能读取该文件字节** 的前提下完成（例如本机终端 `curl`、脚本等）。**PUT 返回成功（通常 2xx）后**才能调用 **`file_osendupload`**（**C11**）。若调用方文件与执行 PUT 的环境**不在同一可访问路径**，无法单靠本技能完成直传，须向用户说明并改用可达方式（如将文件放到执行环境可读位置、或使用企业提供的其它上传通道）。

### file_osendupload

确认上传完成（`POST /efast/v1/file/osendupload`）。**`docid`**、**`rev`** 必须使用 **`file_osbeginupload`** 响应中的值（新文件 docid，勿误用仅作为上传目标的父目录 docid）。

```json
{
  "name": "file_osendupload",
  "arguments": {
    "docid": "gns://F3E37AFXXXXX407B983F857779332AFB/3C29513ABFA240F4AFC4227EB8503B21/F3A2F10333564DB399D8E0500B65F1FB",
    "rev": "ED815F2CA22840418A0F6BC42F4D1DA1"
  }
}
```

**说明**：**禁止**使用 **`file_upload`**（**C11**）。

### file_convert_path

```json
{
  "name": "file_convert_path",
  "arguments": {
    "docid": "<docid（完整 gns 路径）>"
  }
}
```

**仅用于展示 namepath**，不替代其它工具的 docid 传参。详见上文「**核心概念**」→ **namepath** 与 **传参规则**。

### sharedlink_parse

解析分享链接详情（GET `/shared-link/v1/links/{link_id}`）。**`link_id`**：分享 URL 中 **`/link/`** 路径段之后（与 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)** 任务流一致）。

```json
{
  "name": "sharedlink_parse",
  "arguments": {
    "link_id": "<SharedLink 唯一标识，与 URL 中 /link/ 后段一致>"
  }
}
```

**必填字段**：仅 `link_id`。

**返回结构**：响应含 `type`（如 `realname` / `anonymous`）、顶层 `id`（**分享链** id，可与 `link_id` 对应）、`item` 对象。`item` 内：**`item.id`** 为完整 **docid**（`gns://…`）；**`item.type`** 为 `file` / `folder` 等；另有 `belongs_to` 等字段以实际返回为准。进入场景四后，`smart_assistant` 的 `source_ranges[].id` 取 **`item.id`** 最后一段，不传完整 docid（见 C5）。**顶层 `id` 不是文档 docid**，分流与传参均以 **`item.id`** 为准。

### smart_assistant（全文写作 · 生成大纲）

`skill_name`：`__全文写作__2`

```json
{
  "name": "smart_assistant",
  "arguments": {
    "query": "<用户写作任务描述>",
    "selection": "",
    "times": 1,
    "skill_name": "__全文写作__2",
    "web_search_mode": "off",
    "datasource": [],
    "source_ranges": [{ "id": "<文档的 id>", "type": "doc" }],
    "template_id": 1,
    "interrupted_parent_qa_id": ""
  }
}
```

**`source_ranges[].id`** 传 **id**（docid 最后一段），不传完整 docid（C5）。`type` 固定为 `"doc"`。`version`、`temporary_area_id` **不要传**（无法从响应可靠获取）。

**成功返回（MCP 解析后的结构化字段）：**

- **`streaming_answer`**：流式阶段正文级累加（processing 下 `result/answer/document/content` 的 append 拼接），**大纲/要点**以此为准 → **向用户展示并请其确认（C4）**。
- **`completion_answer`**：流式结束 `completed` 时解析，**多为提示语、按钮引导或会话收尾**，**不作为**大纲正文。
- **`conversation_id`**：下一调用（「基于大纲生成正文」）必传。
- 另有 `bot_id`、`bot_name`、`status` 等，见 `mcporter list asmcp` 返回的 `outputSchema`。

**返回示例（节选）：**

```json
{
  "streaming_answer": "一、……\n二、……",
  "completion_answer": "请确认大纲后再生成正文",
  "conversation_id": "<会话 ID>",
  "status": "completed"
}
```

### smart_assistant（全文写作 · 基于大纲生成正文）

`skill_name`：`__大纲写作__1`

```json
{
  "name": "smart_assistant",
  "arguments": {
    "query": "基于大纲生成文档",
    "selection": "<第 2 步 streaming_answer 全文，或用户确认后的同义稿>",
    "conversation_id": "<第 2 步返回的 conversation_id>",
    "times": 1,
    "skill_name": "__大纲写作__1",
    "web_search_mode": "off",
    "datasource": [],
    "source_ranges": [{ "id": "<文档的 id>", "type": "doc" }],
    "interrupted_parent_qa_id": ""
  }
}
```

**本步返回：** 最终成稿正文以 **`streaming_answer`** 为准；**`completion_answer`** 多为收尾说明。导出与保存时以 **`streaming_answer`** 为正文来源。

**返回示例（节选）：**

```json
{
  "streaming_answer": "（完整正文……）",
  "completion_answer": "生成完成",
  "conversation_id": "<会话 ID>",
  "status": "completed"
}
```

### auth_login

凭证步骤与安全要求见上文 **「凭证（Token）」**。

```json
{
  "name": "auth_login",
  "arguments": {
    "token": "<访问令牌本体，不含 Bearer 前缀；以 mcporter list 的 schema 为准>"
  }
}
```

### auth_status

无参数，查询当前登录状态（与 **`auth_login`** 配合用于会话内校验）。

### 工具列表查询（诊断用）

```bash
mcporter list asmcp
# 或
mcporter call asmcp.tools/list
```

### HTTP 备选（工具调用全失败时）

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  "https://anyshare.aishu.cn/mcp"
```

---

## 📂 场景一：文件/关键词搜索

> **说明**：`file_search` 固定字段、返回与分页见 **[上文「本技能工具与 mcporter 调用」→ file_search](#file_search)**。

### 步骤

**第 1 步：`file_search`**

入参、出参 JSON 与 **mcporter 示例**见 **[上文 file_search](#file_search)**。

> ⚠️ `dimension: ["basename"]` + `model: "phrase"` **必须固定**，不随关键词变化。省略会导致正文/多字段命中，而非按名匹配。

**第 2 步：展示结果（必须含三要素）**

对每条结果：**先调 `file_convert_path`** → 再展示：

- **名称**：`basename`
- **大小**：`size = -1` → 目录；`size ≥ 0` → 实际字节数
- **AnyShare 知识库路径**：`namepath`（来自 `file_convert_path` 返回）

> ⚠️ **C1 + C2**：禁止跳过 `file_convert_path`；禁止用 docid/序号代替 namepath 展示。

**第 3 步：用户确认 docid（如需操作）**

**分页提示（hits ≥ 25 时强制显示）：**

> 找到 X 条（已展示前 25 条），是否：
>
> 1. **查看更多**（翻页）  2. **更换关键词**  3. **缩小范围**（加 range）

**按文件夹名查看子文件：**

1. 搜索结果中找 `size = -1` 且 basename 一致的项
2. 对该 docid 先调 `file_convert_path` 展示目录 namepath（C2）
3. 再调 **[folder_sub_objects](#folder_sub_objects)** 列出子文件

---

## 📂 场景二：上传文件

### 步骤

**第 1 步：确定目标目录 docid**（**必须 C3**）

- **一般情况**：`file_search` + `file_convert_path` 搜索并展示目录，用户确认。
- **用户明确要传到「个人文档库」**：可先 **`doc_lib_owned`**（见 **[上文 doc_lib_owned](#doc_lib_owned)**）取列表，选中个人文档库项的 **`id`**（`gns://…`）作为目标目录，再 **`file_convert_path`** 展示 `namepath` 供用户确认。本地文件路径（如 `/Users/…/file.zip`）仅用于后续 **PUT** 读文件，**不是** `docid`。

**展示确认模板：**

> 即将上传到：
>
> - 文件名：`<本地文件名>`
> - AnyShare 知识库路径：`file_convert_path` 返回的 `namepath`
> - docid：`gns://...`
>
> 确认继续？回复"是"，或提供其他目标路径。

**第 2 步：用户回复"是"后锁定 docid（C3）**

**第 3 步：分步上传（`file_osbeginupload` → PUT → `file_osendupload`，必须 C11）**

1. 调用 **`file_osbeginupload`**：`docid` 为已确认的目标**目录**；`name`、`length` 与待传文件一致（由用户提供或仅在执行环境可读时从本地取得）。入参/响应见上文 **「file_osbeginupload」**、**「对象存储直传 PUT」**、**「file_osendupload」** 小节。
2. 根据响应中的 **`authrequest`**，对对象存储 URL 执行 **HTTP PUT**（请求体为文件字节）。**非 MCP 工具**；**PUT 失败则不得调用 `file_osendupload`**。
3. 调用 **`file_osendupload`**：**`docid`**、**`rev`** 取自 **begin 响应**（新文件 docid）。

**第 4 步：汇报**

- docid 必须展示为 **`gns://` 开头完整路径**（禁止只展示 id/十六进制串）
- 对新文件 docid 调 `file_convert_path`，一并展示 `namepath`

---

## 📂 场景三：下载文件

### 步骤

**第 1 步：搜索目标文件**（`file_search` + `file_convert_path`，**必须 C3**）

**展示确认模板：**

> 即将下载：
>
> - 文件名：`<basename>`
> - 大小：`<size> 字节`
> - AnyShare 知识库路径：`file_convert_path` 返回的 `namepath`
> - docid：`gns://...`
>
> 确认继续？回复"是"，或选择其他文件。

**第 2 步：用户回复"是"后锁定 docid（C3）**

**第 3 步：`file_osdownload`**

入参、出参 JSON 见 **[上文 file_osdownload](#file_osdownload)**。

---

## 📂 场景四：全文写作

> **说明**：**`smart_assistant`** 两阶段（大纲 / 正文）的完整入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」](#本技能工具与-mcporter-调用)** 中 **「smart_assistant（全文写作 · 生成大纲）」** 与 **「smart_assistant（全文写作 · 基于大纲生成正文）」**。

**入口**：用户已确认走全文写作流程。

### ⚠️ C8 进门卡点（C-gate 0）：进入前须掌握 docid 与 `source_ranges` 所用 id

> **这是本场景的第一道门。** 须已能确定目标文档的 **docid**（`gns://…`），并由此得到 **`source_ranges[].id`**（docid 最后一段，见核心概念）。尚未具备时，须先出去获取，不得绕过。

**进门前自问：**

> "我是否已能确定本次写作对应文档的 **docid**，并知道传入 **`source_ranges`** 的 **id**（最后一段）？"

- **是** → 进入步骤 1
- **否（docid / id 尚未就绪）** → 必须先执行以下之一：
  - **路径 A**：`file_search`（关键词搜索）→ 获取 docid → 推出 **id** → 返回本场景
  - **路径 B**：[分享链接](#分享链接从-url-到-docid)（`sharedlink_parse`）→ 获取 docid / **id** → 返回本场景
  - **路径 C**：若用户直接提供了文件 **docid**（完整 `gns://…`）→ 推导 **id** → 进入步骤 1
  - **禁止**：自行判断"docid 拿不到"而改用本地写作、摘要总结等绕过手段（违者属 C8 违规）

> **C8 违规模式（自检，行为描述）：**（**仅**约束「进入写作前」是否已持 docid/id；**已取得 id 却先下载、再跑偏**见 **C10**。）
>
> - **不当**：未走完 **路径 A / B / C**（或等效的 **场景二上传** 取得云端 docid），尚未持有本次写作所需的 **docid / id**，就输出全文或调用 `smart_assistant`。**应当**：先取得 **docid / id** 再进入场景四。
> - **不当**：以「暂时拿不到 docid」为由，在对话内做全文总结或等价长文以替代上述路径。**应当**：先按 **路径 A / B / C** 取得 docid；若用户任务与 AnyShare 文档无关，应 **结束本技能** 或说明不适用本路径，**禁止**用「总结/代写」绕过 docid 前置步骤。

### ⚠️ 取得 id 后防跑偏（C10）

已拿到 **`source_ranges`** 所需 **id** 时，**下一步必须直接调用 `smart_assistant`（`__全文写作__2`）生成大纲**（见第 2 步）。**禁止**先 **`file_osdownload`**、禁止先读本地副本来「理解原文再写」——写作上下文由 **`source_ranges`** 在 **`smart_assistant`** 内注入，与 **在场原则**、**C9** 一致。

### ⚠️ 大纲门闩（C4）

禁止跳过"生成大纲 → 用户确认"直接生成正文。

### 步骤

**第 1 步：确认文档 id（已在 C8 取得 docid / id）**

- 分享链接 → 按 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)** 得到 **id**
- 关键词 → `file_search` 确认文档 id

确认 **id** 后 **直接进入第 2 步**，**勿**先 **`file_osdownload`**（**C10**）。

**第 2 步：生成大纲（`__全文写作__2`）**

入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」→ smart_assistant（全文写作 · 生成大纲）](#本技能工具与-mcporter-调用)**。向用户展示并请其确认（**C4**）的稿，以返回 **`streaming_answer`** 为准；**`completion_answer`** 多为收尾/提示，**不作为**大纲正文。第 3 步需传入的 **`conversation_id`** 取自本步返回。

→ 将 **`streaming_answer`** 展示给用户 → **等待用户确认或修改后再进入第 3 步**（C4）。

**第 3 步：生成正文（`__大纲写作__1`）**

仅在 **C4** 确认后调用。入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」→ smart_assistant（全文写作 · 基于大纲生成正文）](#本技能工具与-mcporter-调用)**。**`selection`** 通常取第 2 步 **`streaming_answer`** 全文（用户改稿后以其最终稿为准）；**`conversation_id`** 用第 2 步返回。最终成稿正文以返回 **`streaming_answer`** 为准。

**第 4 步：导出**（保存本地 / 上传至 AnyShare 复用场景二）

> ⚠️ **C5**：`source_ranges[].id` 传 id（docid 最后一段），不传完整 docid。

---

## 📎 分享链接（从 URL 到 docid）

> **任务入口**：用户粘贴 `https://…/link/…` 时，先读本节再调工具；**`sharedlink_parse`** 的入参、返回字段见上文 **「本技能工具与 mcporter 调用」** 小节中的 **`sharedlink_parse`**。需已具备 MCP 认证（已按 **「凭证（Token）」** 完成 **`auth_login`**）；未授权按 [references/troubleshooting.md](references/troubleshooting.md) 处理。

**触发**：用户提供文档域下的分享 URL（任意 `…/link/<link_id>` 形态）。

**第 1 步：提取 `link_id`**  
取路径 **`/link/`** 之后的一段。示例：`https://anyshare.aishu.cn/link/AR85DF4473697974F48EDDB4967AEA2B61` → `link_id` = `AR85DF4473697974F48EDDB4967AEA2B61`。（**C6**）

**第 2 步：调用 `sharedlink_parse`**  
入参 JSON 见上文 **「本技能工具与 mcporter 调用」** 中 **`sharedlink_parse`**（仅 `link_id`）。

**第 3 步：解析后分流（C7、C5）**

- **`docid`** = **`item.id`**（`gns://…`）；响应**顶层 `id`** 为分享链自身 id，**≠** `item.id`（**C7**）。
- **`item.type` = `folder`** → **`file_convert_path`**（`docid` = `item.id`）展示 `namepath`（**C2**）→ **`folder_sub_objects`** 列子项。
- **`file` / 其他** → 取 **`item.id`** 最后一段为 **id**，进入 **「场景四：全文写作」** 调用 `smart_assistant`（**C5**）。

---

## 🎯 意图模糊时的确认模板

当用户意图**不清晰**、无法判断是否在 AnyShare 操作或做哪类操作时，使用以下模板（仅一次，不叠套）。**若消息中已含 `/link/` 分享 URL**，优先按 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)** 处理，**不必**先套本模板。

```
请确认：
1. 目标系统：是否在 AnyShare 操作？
   1) 是
   2) 其他系统

2. 具体操作：
   1) 搜索 / 查看文件
   2) 上传或下载文件
   3) 全文写作
   4) 粘贴或打开分享链接（URL 含 /link/）
   5) 其他（文档库浏览、换账号等）

回复示例：「1 2」表示在 AnyShare 上传或下载；「1 4」表示处理分享链接。
```

**回复 → 执行路径：**


| 回复 | 场景 |
| --- | --- |
| `1 + 1` | 场景一 |
| `1 + 2`（上传） | 场景二 |
| `1 + 2`（下载） | 场景三 |
| `1 + 3` | 场景四 |
| `1 + 4` | **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)** |
| `1 + 5` | 澄清子意图 |
| `2` | 不走本技能 |


---

## 📖 补充资料（权威来源）


| 文件 | 权威内容 | 用于 |
| --- | --- | --- |
| **[setup.md](setup.md)** | asmcp.url、daemon、企业地址确认话术 | 首次配置（**唯一权威**） |
| **本 SKILL.md** → **「凭证（Token）」**、**「获取凭证（固定提示语）」** | 用户设置 →「MCP 授权凭证」；粘贴、`auth_login`、备份、安全 | 凭证 |
| **本 SKILL.md** → **「📌 核心概念」** | docid、id、sharedlink、namepath、传参、skill_name | 概念 |
| **本 SKILL.md** → **「📎 分享链接（从 URL 到 docid）」** | `link_id`、folder/file 分流（C6/C7） | 用户粘贴 `/link/` URL |
| **本 SKILL.md** → **「🔧 本技能工具与 mcporter 调用」** | 工具 JSON、mcporter、auth、诊断 | 工具调用 |
| [references/troubleshooting.md](references/troubleshooting.md) | 错误码、常见处理 | 排障 |
| [SECURITY.md](SECURITY.md) | 安全约束、敏感信息 | 安全审计 |



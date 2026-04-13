---
name: culturetour-search
description: >-
  指导智能体检索文旅素材（数游神州 data0086.com）并走通「搜索 → 列表 → 预览(HLS/MP4) → 选择/购买」。搜索请求默认最多 5 条（pageSize≤5），用户可要求更少；列表用表格展示（颜色徽章状态 + img + video），用户通过文本指令选择，支持多选与批量购买。用户可「购买 1,2」直接下单，无需二次确认。
  **输出格式自动适配**：桌面端/Web 客户端（ArkClaw、OpenClaw 等）默认输出 HTML 表格；**IM 手机应用**（飞书、微信、钉钉等）则输出 **Markdown 表格**，避免手机端直接显示 HTML 源码。
  所有嵌入媒体仅限 config.json 中 trusted_media_origins 声明的域名。环境变量 WENLV_API_ORIGIN、TRADE_API_BASE 可选覆盖 config.json 默认值（见 index.json env 声明）。
---

# 文旅素材搜索（API）

> **输出格式规范**
>
> 智能体应先判断客户端类型，再选择对应的输出格式：
>
> | 客户端类型 | 判定依据 | 输出格式 |
> |-----------|---------|---------|
> | **桌面端 / Web**（ArkClaw、OpenClaw、浏览器等） | 默认 | HTML 表格（`<table>`、`<img>`、`<video>` 等，仅限 `index.json` 中 `html_output.tags` 声明的标签） |
> | **IM 手机应用**（飞书、微信、钉钉、企业微信等） | 用户提到在飞书/微信/钉钉中使用，或上下文/系统信息表明客户端为 IM 应用 | Markdown 表格（`| col |` 语法，图片用 `![](url)`，链接用 `[text](url)`） |
>
> **桌面端 HTML 模式注意事项**：
> - 不要将 HTML 放在代码围栏内（围栏内的标签不会被渲染，只会显示源码）
> - 不要使用 `<input type="checkbox">`（静态 HTML 环境中无法交互）
> - 不要使用 `<button>`（无 JS 运行环境，无法绑定事件）
> - 所有媒体 URL（`<img src>`、`<video src>`）须通过下文「安全：媒体来源校验」
>
> **IM 手机端 Markdown 模式注意事项**：
> - 使用 Markdown 表格语法（`| col |`）
> - 缩略图用 `![封面](cover_url)` 或省略（手机屏幕窄时可不显示缩略图列）
> - 视频预览无法内嵌，统一用 `[▶ 预览](preview_url)` 链接
> - 不要输出 HTML 标签（手机 IM 不渲染 HTML，会直接显示标签源码）
>
> **通用规则**：
> - 选择操作通过**用户发送文本指令**完成（如「选 1,3」「购买」），智能体重新渲染带状态标记的表格
> - 注：本文档内的 HTML 模板用代码块展示以防文档渲染器误执行；智能体输出给用户时应去掉代码围栏。
> 详见下文「搜索结果展示」。

## 安全：媒体来源校验

本 Skill 的 HTML 输出包含 `<img>`、`<video>` 等标签，客户端会直接向 `src` 地址发起请求。为防止向不可信主机泄露用户 IP / 元数据，**智能体应在嵌入前校验媒体 URL 的来源**：

1. **可信来源列表**：[config.json](config.json) 的 **`trusted_media_origins`** 数组（默认仅包含 `api_origin`）。
2. **校验规则**：`<img src="...">`、`<video src="...">`、`<video poster="...">` 中的 URL **必须以 `trusted_media_origins` 中某一项开头**（协议 + 主机 + 端口完全匹配）。
3. **不符合时的处理**：
   - 若 `cover_url`（`breviaryPic`）不在可信列表 → 缩略图列显示「—」，不输出 `<img>`。
   - 若 `video_url`（`fragmentUrl`）不在可信列表 → 视频预览列**不输出 `<video>`**，改为纯文本「[需在浏览器中打开]」+ `preview_url` 超链接（`preview_url` 始终为同源站内页面）。
4. **API 响应中的 `breviaryPic`** 和 **`fragmentUrl`** 均为完整绝对 URL（指向 `wenzhou.data0086.com:9443`），须检查是否在 `trusted_media_origins` 中。
5. **`trusted_media_origins`** 默认包含 `https://www.data0086.com` 和 `https://wenzhou.data0086.com:9443`。

> 简言之：**只有 config 中声明的可信域名才允许直接嵌入媒体**，其余一律用 `preview_url` 超链接代替。

## 目标

让智能体用**自然语言**检索数游神州平台（data0086.com）上的文旅素材资源。每条结果必须**结构化保留**下游交易要用的字段，尤其是 **`fragmentUrl`（视频预览流）**、**`commodityCode`** 和 **`businessCode`**。

- 用 **解析后的搜索 URL** 直接 `POST` 请求，并按本文「输出映射」组装标准 JSON。

## 流程总览：先调试「预览 → 选择/购买」

**当前阶段（交易 API 未定时）**：智能体优先走通 **搜索 → 列表 → 预览 → 选择/购买**（支持「购买 1,2」一步下单）。不在此阶段调用交易接口；购买后输出 **结构化「批量交易请求」**（见下），便于联调与后续接下单。

**交易入口**：保留在文档中，待 `TRADE_API_BASE` / `trade_api_base` 配置并约定接口后再启用（见「交易 API（预留）」）。

智能体按顺序引导；上一步未就绪时不要进入下一步。用户可随时要求「重新搜索」。

### 主路径（调试优先）

| 步骤 | 行为要点 |
|------|----------|
| **1. 搜索** | `POST {api_origin}/ms-base/home/getList?pageNum=1&pageSize=5`；**`pageSize` 默认 `5`**（最多 5 条），用户明确要求更少时按用户指定数量传（如「给我 1 条」→ `pageSize=1`）。保留 P0/P1 字段。 |
| **2. 列出结果** | 用表格展示（HTML 或 Markdown，取决于客户端类型），不要把工具/API 返回的整段 JSON 当作对用户的主回复（见下「搜索结果展示」与「展示与 JSON」）：列 **状态｜标题｜缩略图｜视频预览｜详情**；首列用颜色徽章标记选中状态（非 checkbox）。表格**下方**附操作说明（见「选择与购买」）。 |
| **3. 预览** | 引导用户打开 **`preview_url`**（数游神州商品详情页 `/#/multimodal?businessCode=…`，统一处理视频播放）；可同时说明 **`stream_type`** 与原始 **`video_url`** 供技术核对。**预览仅用于选片，不等于已购原片**。 |
| **4. 选择 / 购买** | 支持两种操作模式，**无需额外确认步骤**：<br>**模式 A — 先选后买**：用户先发送选择指令（「选 1、3」「全选」），智能体重新渲染表格标记选中状态；之后用户发送「购买」或「下单」，智能体**直接**输出批量交易请求，不再要求二次确认。<br>**模式 B — 直接购买**：用户直接发送「购买 1,2」「下单 3」「买第1条」等**包含序号的购买指令**，智能体**一步完成**选中 + 输出批量交易请求（见「确认购买后输出」），跳过选择环节。<br>用户在选择阶段可追加/移除（「加上第2条」「去掉第3条」），智能体每次都重新渲染完整表格。 |

### 搜索结果展示 — 根据客户端类型选择输出格式

> 输出前应先判断客户端类型，选择对应格式。
>
> #### 桌面端 / Web 客户端（HTML 模式）
>
> 客户端（ArkClaw / OpenClaw）支持 HTML 渲染。展示搜索结果时，直接输出 HTML 标签（仅限 `index.json` 中 `html_output.tags` 声明的标签）。
>
> **注意事项（HTML 模式）：**
>
> - 不要使用 `<input type="checkbox">` 或 `<button>`（聊天气泡无 JS，无法交互）
> - 不要把 HTML 放在代码块里（代码块只会显示源码，不会渲染）
> - 所有 `<img src>` 和 `<video src>` 的 URL 须属于 `trusted_media_origins`（见「安全：媒体来源校验」）
>
> **正确做法**：在回复中直接书写 HTML 标签，不加代码围栏，让客户端渲染。选择状态用颜色徽章表示，用户通过发送文本指令选择/购买。
> （本文档内的模板为防止文档自身渲染 `<video>` 导致页面刷新，使用了代码块包裹——这仅限于文档展示，智能体输出时应去掉代码围栏。）
>
> #### IM 手机应用（Markdown 模式）
>
> 飞书、微信、钉钉等 IM 手机应用不渲染 HTML，会将标签作为纯文本显示。此时应使用 Markdown 表格。
>
> **注意事项（Markdown 模式）：**
>
> - 不要输出 HTML 标签（手机 IM 会直接显示标签源码）
> - 不要把表格放在代码围栏内
>
> **正确做法**：使用 Markdown 表格语法，缩略图用 `![](url)` 或省略，预览链接用 `[▶ 预览](preview_url)`。

#### 表格列定义（固定五列）

**HTML 模式（桌面端 / Web）：**

| 列名 | HTML 元素 | 内容 |
|------|---------------------|------|
| **状态** | `<span>` 带背景色 | 未选中：灰底序号 `<span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">1</span>`；选中：绿底 ✅ `<span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 1</span>` |
| **标题** | 纯文本 + `<small>` | title，可附 `<br><small style="color:#999;">id</small>` |
| **缩略图** | `<img src="..." width="120">` | cover_url；无封面写「—」 |
| **视频预览** | `<video controls width="240" poster="..." src="...">` | src 用 video_url（fragmentUrl），poster 用 cover_url |
| **详情** | 纯文本 + `<a href="...">` | 分辨率/时长/大小，附 preview_url 超链接兜底 |

**Markdown 模式（IM 手机端）：**

| 列名 | Markdown 写法 | 内容 |
|------|--------------|------|
| **状态** | 纯文本序号或 ✅ | 未选中：`1`；选中：`✅ 1` |
| **标题** | 纯文本 | title |
| **缩略图** | `![封面](cover_url)` 或省略 | 手机屏幕窄时可不显示此列 |
| **预览** | `[▶ 预览](preview_url)` | 链接到站内播放页 |
| **详情** | 纯文本 | 分辨率/时长/大小 |

### 选择与购买（表格下方操作区）

表格下方直接输出操作提示 HTML。

> **注意**：以下模板在本文档中用代码块展示，**防止文档渲染器误执行**。智能体输出给用户时应去掉代码围栏，直接输出 HTML。

> **核心规则：无需二次确认**
> - 「购买 1,2」「下单 3」等**带序号的购买指令**→ 直接选中并生成交易请求，一步到位
> - 「选 1,3」→ 仅标记选中，渲染表格；之后用户说「购买」/「下单」→ 直接生成交易请求
> - **不要**在用户已发出购买指令后再要求「请确认」或「确认购买」

初始状态（无选中）— HTML 模式：
```html
<div style="background:#f6f8fa; border-left:4px solid #409eff; padding:10px 14px; margin:10px 0; border-radius:4px;">
<b>💡 操作说明</b><br>
· 回复「<b>购买 1、3</b>」或「<b>下单 2</b>」直接购买指定素材<br>
· 回复「选 1、3」先标记，之后回复「<b>购买</b>」一键下单<br>
· 回复「取消 3」取消已选
</div>
```

初始状态（无选中）— Markdown 模式（IM 手机端）：
```markdown
💡 **操作说明**
· 回复「**购买 1、3**」或「**下单 2**」直接购买指定素材
· 回复「选 1、3」先标记，之后回复「**购买**」一键下单
· 回复「取消 3」取消已选
```

有选中时 — HTML 模式：
```html
<div style="background:#f0f9eb; border-left:4px solid #67c23a; padding:10px 14px; margin:10px 0; border-radius:4px;">
✅ 已选 <b>N</b> 条素材 | 总时长 XXs | 总大小 <b>XXXM</b><br><br>
👉 回复「<b>购买</b>」或「<b>下单</b>」立即下单<br>
👉 回复序号可继续追加或取消选择
</div>
```

有选中时 — Markdown 模式（IM 手机端）：
```markdown
✅ 已选 **N** 条素材 | 总时长 XXs | 总大小 **XXXM**
👉 回复「**购买**」或「**下单**」立即下单
👉 回复序号可继续追加或取消选择
```

当用户发送选择指令后，智能体**重新渲染完整表格**：
- 选中行首列显示绿色 ✅ 徽章，行背景加 `style="background:#f0f9eb;"`
- 未选行首列显示灰色序号徽章
- 表格下方显示选中汇总 + 购买提示

### 展示与 JSON（必读）

- **对用户**：搜索列表的**默认形态**是表格（桌面端用 HTML 表格，IM 手机端用 Markdown 表格）。**禁止**用 JSON 代码块替代。
- **对程序/联调**：若用户明确说「给我原始 JSON」「导出结构」或已进入购买阶段，再按「标准结果 JSON 形状」或「购买后输出」给出 JSON。
- **条数**：URL 参数 **`pageSize` 默认传 `5`**（上限），用户要求更少时按用户数量传；若接口返回超出请求数量，只取前 N 条映射为表格。

### 完整输出模板（直接复制替换真实值）

智能体输出搜索结果时，**按照以下模板逐行输出 HTML**，将 `{变量}` 替换为真实值。

> **注意**：以下模板在本文档中用代码块展示，**防止文档渲染器误加载 `<video>`/`<img>` 导致页面刷新**。智能体输出给用户时应去掉代码围栏，直接输出 HTML 标签。

**初始状态（全部未选中）— HTML 模式：**

```html
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
<thead style="background:#f5f7fa;">
<tr><th>状态</th><th>标题</th><th>缩略图</th><th>视频预览</th><th>详情</th></tr>
</thead>
<tbody>
<tr>
<td><span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">1</span></td>
<td>{title}<br><small style="color:#999;">{id}</small></td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" poster="{cover_url}" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}<br><a href="{preview_url}">浏览器播放</a></td>
</tr>
<tr>
<td><span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">2</span></td>
<td>{title}<br><small style="color:#999;">{id}</small></td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" poster="{cover_url}" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}<br><a href="{preview_url}">浏览器播放</a></td>
</tr>
</tbody>
</table>
<div style="background:#f6f8fa; border-left:4px solid #409eff; padding:10px 14px; margin:10px 0; border-radius:4px;">
<b>💡 操作说明</b><br>
· 回复「<b>购买 1、3</b>」或「<b>下单 2</b>」直接购买指定素材<br>
· 回复「选 1、3」先标记，之后回复「<b>购买</b>」一键下单
</div>
```

**初始状态（全部未选中）— Markdown 模式（IM 手机端）：**

```markdown
| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| 1 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |
| 2 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |

💡 **操作说明**
· 回复「**购买 1、3**」或「**下单 2**」直接购买指定素材
· 回复「选 1、3」先标记，之后回复「**购买**」一键下单
```

**选中第 1、2 条后（用户发送「选 1,2」后智能体重新渲染）— HTML 模式：**

```html
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
<thead style="background:#f5f7fa;">
<tr><th>状态</th><th>标题</th><th>缩略图</th><th>视频预览</th><th>详情</th></tr>
</thead>
<tbody>
<tr style="background:#f0f9eb;">
<td><span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 1</span></td>
<td>{title}</td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}</td>
</tr>
<tr style="background:#f0f9eb;">
<td><span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 2</span></td>
<td>{title}</td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}</td>
</tr>
</tbody>
</table>
<div style="background:#f0f9eb; border-left:4px solid #67c23a; padding:10px 14px; margin:10px 0; border-radius:4px;">
✅ 已选 <b>2</b> 条素材 | 总时长 236.6s | 总大小 <b>273.9M</b><br><br>
👉 回复「<b>购买</b>」或「<b>下单</b>」立即下单<br>
👉 回复序号可追加或取消选择
</div>
```

**选中第 1、2 条后 — Markdown 模式（IM 手机端）：**

```markdown
| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| ✅ 1 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |
| ✅ 2 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |

✅ 已选 **2** 条素材 | 总时长 236.6s | 总大小 **273.9M**
👉 回复「**购买**」或「**下单**」立即下单
👉 回复序号可追加或取消选择
```

**其中：**
- **`{preview_url}`** = `{api_origin}/#/multimodal?businessCode={businessCode}`（数游神州商品详情页）。
- **`{cover_url}`** = `breviaryPic`（已是完整 URL），**`{video_url}`** = `fragmentUrl`。嵌入前须校验来源属于 `trusted_media_origins`（见「安全：媒体来源校验」），不符合则不输出 `<img>` / `<video>`。

### ❌ 错误输出 vs ✅ 正确输出

**错误（HTML 模式下使用 checkbox / 代码围栏）：**
```
| □ | # | 标题 | 缩略图 | 预览 |
|---|---|------|--------|------|
| □ | 1 | 雁荡山素材 | [封面](url) | [预览 · HLS](url) |
```
或使用 `<input type="checkbox">`（渲染出来但无法勾选）、`<button>`（无法点击触发）。

**错误（IM 手机端输出 HTML 标签）：**
在飞书/微信中输出 `<table><tr><td>...` — 用户看到的是一堆 HTML 源码文本。

**✅ 正确 — HTML 模式（桌面端 / Web，无代码围栏）：**

智能体回复中应**直接包含**如下 HTML（不被 ``` 包裹）：

&lt;table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;"&gt;
&lt;tr&gt;
&lt;td&gt;&lt;span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;"&gt;1&lt;/span&gt;&lt;/td&gt;
&lt;td&gt;雁荡山素材&lt;/td&gt;
&lt;td&gt;&lt;img src="https://…/cover.jpg" width="120"&gt;&lt;/td&gt;
&lt;td&gt;&lt;video controls width="240" src="https://…/index.m3u8"&gt;&lt;/video&gt;&lt;/td&gt;
&lt;td&gt;2560×1440&lt;br&gt;118.5s / 98.3M&lt;/td&gt;
&lt;/tr&gt;
&lt;/table&gt;

**✅ 正确 — Markdown 模式（IM 手机端）：**

| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| 1 | 雁荡山素材 | [▶ 预览](https://www.data0086.com/#/multimodal?businessCode=xxx) | 240.9s / ¥45 |

### `<video>` 标签用法

- **`src`** 必须用 **`video_url`**（即 `fragmentUrl`，实际媒体流），**不是** `preview_url`（商品详情页）。
- **来源校验**：嵌入前须确认 `video_url` 的来源在 `trusted_media_origins` 中（见「安全：媒体来源校验」）。不在列表中 → 不输出 `<video>`，改用 `preview_url` 超链接。
- **`poster`** 用 `cover_url`（封面图）。无封面时省略 `poster`。同样须通过来源校验。
- **MP4**：浏览器原生支持。
- **HLS（m3u8）**：Safari 原生支持；Chrome 依赖客户端 hls.js。若 `<video>` 无法播放，详情列的 `preview_url` 链接兜底。

### 预览与本地播放（能力边界）

**SKILL 无法在对话气泡内嵌入可执行的 HLS 播放器**（多数客户端会拦截脚本、iframe，且 OpenClaw / 飞书等需产品侧组件才能内嵌播放）。本 Skill 通过下列方式支持用户**在本机观看预览**：

1. **浏览器打开 `preview_url`（推荐）**  
   - 数游神州商品详情页已统一处理视频播放，用户直接点击表格中的「预览」链接即可。  
   - 若需在系统播放器中打开**原始流**，再使用 `video_url` + `stream_type`（见下文）。

2. **仅当无可用 HTML 播放页、且必须直接拉流时：再考虑 `video_url`**  
   - **`stream_type` 为 `MP4`**：多数浏览器可直接打开直链。  
   - **`stream_type` 为 `HLS`**：裸 m3u8 在 Chrome 常下载或无法播放；**Safari** 相对友好。  
   - 智能体应**优先推 `preview_url`**，避免向非技术用户丢裸 m3u8 链。

3. **本仓库脚本（本地用浏览器打开某 URL）**  
   - 路径：[scripts/open_preview.sh](scripts/open_preview.sh)（相对本 Skill 根目录）。  
   - 用法：优先 `bash scripts/open_preview.sh "<preview_url>" MP4`（播放页为 HTML 时按 HTTP 打开即可）；若需直接拉流，再传入 `video_url` 与 `HLS`/`MP4`。  
   - 适用于 Cursor / 终端；**飞书/OpenClaw** 仍以点击 **`preview_url`** 为主。

4. **可选：本机播放器（原始流）**  
   - **VLC** / **ffplay** 可粘贴 **`video_url`**；日常选片以 **`preview_url`** 为主。

飞书 / OpenClaw：**卡片按钮 URL** 与表格一致，指向 **`preview_url`**（即 `{api_origin}/#/multimodal?businessCode={businessCode}`）；若产品另有独立 H5 域名，以产品为准，但须能播同一条素材。

### 购买后输出（调试 / 联调）

在未接交易 API 时，用户发出购买指令后**直接**输出一段**批量交易请求 JSON**（无需二次确认），便于下游与后续接入：

```json
{
  "stage": "purchase_confirmed",
  "items": [
    {
      "id": 459,
      "title": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
      "commodity_code": "CommodityType-e744a1044794",
      "business_code": "Commodity-20260406211854879",
      "preview_url": "https://www.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
      "stream_type": "HLS",
      "duration_seconds": "240.9",
      "price": 45.0
    },
    {
      "id": 461,
      "title": "雁荡山-飞拉达-云雾多视频2-无人机航拍",
      "commodity_code": "CommodityType-948a39e64144",
      "business_code": "Commodity-20260406212609534",
      "preview_url": "https://www.data0086.com/#/multimodal?businessCode=Commodity-20260406212609534",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/b68efe02182c436dbcf35f045b94ed30",
      "stream_type": "HLS",
      "duration_seconds": "30.5",
      "price": 45.0
    }
  ],
  "summary": {
    "total_items": 2,
    "total_duration_seconds": "271.4",
    "total_price": 90.0
  },
  "trade_next": "交易 API 就绪后可在此接入批量下单/原片；当前未调用。"
}
```

`items` 数组中每条资源应包含 P0 字段（`id`、`title`、`commodity_code`、`business_code`、`preview_url`、`video_url`、`stream_type`）及常用 P1 字段（`duration_seconds`、`price`）。`summary` 汇总选中条数、总时长与总价。

**单条选择**同样使用此结构（`items` 数组长度为 1），保持输出格式统一。

### 交易 API（预留，暂不调用）

以下仅在 **`TRADE_API_BASE` 或 `trade_api_base` 已配置** 且产品已约定路径/鉴权后执行；**当前默认不执行**。

1. **基址**：环境变量 **`TRADE_API_BASE`** 优先；否则 [config.json](config.json) 的 **`trade_api_base`** 非空字符串。
2. **调用**：用已锁定资源的 `id`、`commodityCode`、`businessCode` 按产品约定发起请求；鉴权勿泄露到对话。
3. **原片**：仅以接口**真实返回**的下载/任务字段为准，勿伪造链接。

若均未配置或接口未定：智能体在用户发出购买指令后**仅**完成上文「购买后输出」，并可用一句话说明「交易与原片将在接口就绪后接入同一批 `businessCode`」。

## API 基址配置（可更换）

**单一默认值**：与本 Skill 同目录的 [config.json](config.json)（`api_origin` + `search_path`）。

**解析规则**：

1. 若存在环境变量 **`WENLV_API_ORIGIN`**（仅站点根，如 `https://www.data0086.com`），则以其为 `api_origin`。
2. 否则使用 `config.json` 中的 `api_origin`。
3. `search_url` = `api_origin`（去掉末尾 `/`）+ `search_path`（默认 `/ms-base/home/getList`）+ `?pageNum={pageNum}&pageSize={pageSize}`。

| 项目 | 说明 |
|------|------|
| 基址 | `{api_origin}`，默认 `https://www.data0086.com` |
| 搜索 | `POST {api_origin}/ms-base/home/getList?pageNum=1&pageSize=5` |
| 鉴权 | 无（公开接口，`token` 头可为空） |
| Content-Type | `application/json` |

换环境时：改 **config.json** 或部署侧设置 **`WENLV_API_ORIGIN`** 即可，无需改 Skill 正文中的长 URL。**交易**相关另设 **`TRADE_API_BASE`** 或 `config.json` 的 **`trade_api_base`**（非空时生效）。

### 详情页地址（用户点击「预览」）⚠️ 拼接规则

统一使用数游神州前端的商品详情页（与原始 `fragmentUrl` 区分）。

**拼接公式（唯一正确形式）：**

```text
preview_url = {api_origin} + {detail_path} + "?businessCode=" + {businessCode}
```

- **`api_origin`**：`WENLV_API_ORIGIN` 或 `config.json` 的 `api_origin`（默认 `https://www.data0086.com`，**无**末尾 `/`）。
- **`detail_path`**：默认 **`/#/multimodal`**（见 [config.json](config.json) 的 `detail_path`）。
- **`businessCode`**：搜索结果中每条素材的 `businessCode` 字段。

**✅ 正确格式：**
```text
https://www.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879
```

**❌ 错误格式 —— 不要用 `fragmentUrl` 当预览链接：**
```text
https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe
```

**表格「预览」列**、飞书卡片按钮、OpenClaw 内链均应使用 **`preview_url`**（商品详情页）。**`video_url`（fragmentUrl）仍须保留**在结构化结果中，供交易、调试与核对原始流。

### 播放页与裸流（必读：避免一点就下载 m3u8）

- **`video_url`（`fragmentUrl`）** 指向的是 **媒体流**（常见为 HLS 预览地址），**不是**给用户点的「网页预览」。在 Markdown 里若写成 `[预览](video_url)`，浏览器对 **HLS** 往往会 **下载 m3u8** 或无法内联播放。**禁止**将 `video_url` 作为表格「预览」列或卡片按钮的主链接。
- **`preview_url`** 对应数游神州的**商品详情页**（SPA 页面，内含视频播放器），用户点击后在**浏览器页面里播放**，而不是下载清单文件。
- **映射**：`preview_url` **一律只由** `{api_origin}{detail_path}?businessCode={businessCode}` **按上文公式拼接**（见 [config.json](config.json)），**不得**把 `fragmentUrl` 填进 `preview_url`，也不得用 `video_url` 顶替。

### 请求 URL 参数

分页通过 **URL query** 传递：

| 参数 | 必填 | 说明 |
|------|------|------|
| `pageNum` | 否 | 页码，默认 1 |
| `pageSize` | 否 | 每页条数，接口默认 18；**智能体侧默认传 `5`**（上限），用户要求更少时按用户数量传（如 1、2、3） |

### 请求体

```json
{
  "commodityCode": null,
  "sceneType": "",
  "tradeType": "",
  "search": "雁荡山飞拉达",
  "city": "330300"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `search` | 是 | 关键词，支持中文自然语言 |
| `city` | 否 | 城市行政区划代码，默认 `"330300"`（温州） |
| `commodityCode` | 否 | 按商品编码精确筛选，默认 `null` |
| `sceneType` | 否 | 场景类型筛选，如 `"慢直播"`，默认 `""` |
| `tradeType` | 否 | 交易类型筛选，如 `"cash"`，默认 `""` |

### 响应约定

- 业务成功：`code === 0`，列表在 `resData.datas`，总数 `resData.total`。
- HTTP 非 2xx 或 `code !== 0`：向用户说明错误，勿伪造结果。

更完整的原始字段说明见 [references/api_reference.md](references/api_reference.md)。标准接口规范（含交易下单）见 [api.md](api.md)。

## 字段优先级

### P0 — 核心（交易直连，缺一不可）

| 来源字段 | 输出键名 | 说明 |
|----------|-------------------------|------|
| `id` | `id` | 素材唯一 ID（数字） |
| `commodityName` | `title` | 标题 |
| `fragmentUrl` | `video_url` | **原始预览流**（HLS），交易/核对用，**表格「预览」列不用作主链** |
| `commodityCode` | `commodity_code` | 商品编码，**交易下单必需** |
| `businessCode` | `business_code` | 业务编码，**交易下单必需**，也用于详情页 URL |

**派生（必选，用于展示与点击）**  

| 派生规则 | 输出键名 | 说明 |
|----------|----------|------|
| `{api_origin}{detail_path}?businessCode={businessCode}` | `preview_url` | **表格「预览」列、卡片按钮**统一用此链接（商品详情页）；`detail_path` 默认 `/#/multimodal`，见 [config.json](config.json) |

同时必须输出 **`stream_type`**（由 `video_url` / fragmentUrl 判定）：

- URL 含路径片段 **`/hls/`** → `"HLS"`（需 HLS 播放器，如 hls.js）
- URL **以 `.mp4` 结尾** → `"MP4"`（浏览器可直接播）
- 若 `fragmentUrl` 为空：不要编造 `video_url`；可省略 `stream_type` 或标为无法判定（勿写假链接）

### P1 — 重要（展示与交易辅助）

| 来源 | 输出键名 |
|------|----------|
| `explain` | `description`（HTML 格式，包含清晰度/格式等信息） |
| `fragmentTime` | `duration_seconds`（建议保留一位小数，字符串或数字均可） |
| `price` | `price`（元） |
| `breviaryPic` | `cover_url`：已是完整 URL，嵌入前须属于 `trusted_media_origins` |
| `sceneType` | `scene_type`（逗号分隔的场景类型） |
| `tag`（JSON.parse） | `tags`：逗号分隔或数组 |
| `createUser` | `merchant`（商家名称） |

### P2 — 辅助（可选）

`videoProductCode`、`contactName`、`contactPhone`、`merchantBusinessCode`、`priceJson`、`location` 等，在用户需要排查或对接数据源时再输出。

## 标准结果 JSON 形状（解析/转发用）

智能体整理输出时，每条结果建议符合：

```json
{
  "total": 185,
  "pageNum": 1,
  "pageSize": 5,
  "results": [
    {
      "#": "1",
      "id": 459,
      "title": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
      "commodity_code": "CommodityType-e744a1044794",
      "business_code": "Commodity-20260406211854879",
      "preview_url": "https://www.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
      "stream_type": "HLS",
      "duration_seconds": "240.9",
      "price": 45.0,
      "cover_url": "https://wenzhou.data0086.com:9443/res/covers/77758f136a4648888d1acd615ec24dbe.jpg",
      "scene_type": "慢直播,创作素材,无人机航拍",
      "tags": "视频创作, 无人机航拍",
      "merchant": "温州鼎诚体育发展有限公司"
    }
  ]
}
```

## curl 示例

**默认站点根须与 [config.json](config.json) 中 `api_origin` 保持一致**（换域名时改 config 并同步下面默认值，或只用 `export`）。

```bash
# 环境变量优先；未设置时使用默认值（应与 config.json 的 api_origin 相同）
ORIGIN="${WENLV_API_ORIGIN:-https://www.data0086.com}"
curl -sS "${ORIGIN}/ms-base/home/getList?pageNum=1&pageSize=5" \
  -H 'Content-Type: application/json' \
  -H "Origin: ${ORIGIN}" \
  -H "Referer: ${ORIGIN}/" \
  -H 'token;' \
  --data-raw '{"commodityCode":null,"sceneType":"","tradeType":"","search":"雁荡山","city":"330300"}'
```

将返回的 `resData.datas` 按上文映射为 `results` 数组，并带上 `total`、`pageNum`、`pageSize`。

## 智能体行为要点

1. **须同时保留 `preview_url`（详情列超链接兜底）与 `video_url`（`<video>` 播放源）**；**列表展示须用五列表格：状态（颜色徽章）｜标题｜缩略图｜视频预览｜详情**（见「搜索结果展示」）。桌面端用 HTML 表格，IM 手机端用 Markdown 表格。**不要**使用 `<input>`、`<button>` 等需要 JS 交互的元素。
2. **面向用户的列表**：桌面端以 **HTML 表格** 为主（含颜色徽章状态、`<img>`、`<video>` 元素），IM 手机端以 **Markdown 表格** 为主；结构化字段在表格列中体现。**不要**用整段 JSON 代替表格。仅在用户索要导出、或购买后的约定 JSON 块中再输出 JSON。
3. 分页：默认只拉第 1 页且 **`pageSize` 默认 5（上限）**，用户要求更少时按用户数量传；用户要「更多」时递增 `pageNum`，注意 `total` 边界。**跨页选择**：翻页时保留已选中条目；若用户在第 1 页选了第 1、3 条，翻到第 2 页后再选第 2 条，最终选中列表包含累计选中的所有条目。
4. **预览与成单分离**：用户点击的预览必须是 **`preview_url`（商品详情页）**，**不要**把 **`video_url`（HLS 流）** 做成主链接以免下载或无法播放。预览仅用于选片；**原片/授权**在交易 API 接入后**仅**以接口成功响应为准；调试阶段无交易接口时不得伪造原片链接。
5. **交易安全**（启用交易 API 后）：不在对话中输出完整密钥；失败时返回接口错误摘要，不猜测成功。
6. **多选与购买（无需二次确认）**：支持两种下单方式：**① 直接购买**——用户发送「购买 1,3」「下单 2」等带序号的购买指令，智能体一步完成选中 + 输出批量交易请求 JSON；**② 先选后买**——用户先「选 1,3」标记，再发送「购买」/「下单」直接生成交易请求，**不再要求二次确认**。选择过程中用户可随时追加（「加上第2条」）或移除（「取消 3」），智能体每次都**重新渲染完整表格**，用绿色/灰色徽章标记选中状态。
7. **交互约束**：聊天气泡是静态 HTML（无 JavaScript），**禁止**使用 `<input>`、`<button>`、`<form>` 等需要 JS 交互的元素。所有用户操作通过**发送文本消息**完成，智能体解析后重新渲染表格。
8. **客户端适配**：智能体应根据客户端类型选择输出格式（HTML 或 Markdown）。判定方式见文首「输出格式规范」。若无法确定客户端类型，**默认使用 HTML 模式**；当用户反馈看到 HTML 源码时，切换为 Markdown 模式。

具体包名与发布流程以实际 npm 包为准；本 Skill 约束 **行为、配置解析顺序、API 路径与输出字段**。

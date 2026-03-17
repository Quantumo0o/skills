---
name: fosun-sdk-setup
description: Install, verify, and configure the Fosun Wealth OpenAPI SDK in the workspace environment, and manage credentials through `fosun.env` with dialogue-based updates. Use when setting up or initializing `fsopenapi`, fixing missing SDK/import/authentication issues, rotating API keys or accounts, or when other `fosun-*` skills need a ready-to-use Fosun client/session for HK, US, `sh`, or `sz` markets.
---

# Fosun OpenAPI SDK 初始化

---

## 语言风格（非常重要）

通俗易懂，客户人群都是小白用户，必须使用大白话的形式进行内容输出，内容必须简洁，语言亲切，不要出现大量代码输出。

## 1. 安装 SDK

按以下步骤顺序执行。

### 环境约束（必须遵守）

- **优先复用现有虚拟环境**：如果 `{workspace_root}/.venv-fosun` 存在，必须使用它。
- **禁止擅自新建虚拟环境**：未经用户明确要求，**不得**执行 `python -m venv ...`、`uv venv ...`、`conda create ...` 等命令。
- **禁止安装到系统 Python 或其他临时环境**。
- **不要使用裸 `python` / `pip`**；统一使用目标虚拟环境里的绝对路径解释器与 pip，包括安装、验证、以及凭证相关文件处理。

当前 workspace 的标准环境为：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python
/Users/admin/.openclaw/workspace/.venv-fosun/bin/pip
```

如果 `.venv-fosun` 不存在：
- 先检查记忆文件（`MEMORY.md`）里是否记录了其他既有环境路径；
- 若存在既有环境，则复用该环境；
- 若不存在既有环境，**不要自行创建新环境**，先向用户确认。

**Step 1 — 在指定虚拟环境中检查是否已安装**

优先检查：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python -c "import fsopenapi; print(fsopenapi.__file__)"
```

- 成功打印路径 → SDK 已安装，跳到 Step 3 验证。
- 报 `ModuleNotFoundError` → 检查记忆文件（`MEMORY.md`）中是否记录了 SDK 安装路径：
  - 记忆中有路径但目录已不存在 → **删除记忆中对应记录**，继续 Step 2。
  - 记忆中有路径且目录存在 → 在同一个既有虚拟环境中执行 `/Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install -e <路径>`，跳到 Step 3。
  - 无记录 → 继续 Step 2。

**Step 2 — 定位或下载 SDK，并安装到既有虚拟环境**

按优先级查找本地源码：
1. `{workspace_root}/skills/fosun_skills/fosun-sdk-setup/openapi-sdk/`
2. `{workspace_root}/openapi-sdk/`

- 找到 → 使用既有虚拟环境安装：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install -e <路径>
```

- 都不存在 → 从 GitHub 下载后，仍然安装到既有虚拟环境：

```bash
mkdir -p /tmp/fosun-sdk
curl -L -o /tmp/fosun-sdk/openapi-sdk.zip \
  https://github.com/fosunwealth/openapi-python-sdk/archive/refs/tags/v1.0.0.zip
unzip -o /tmp/fosun-sdk/openapi-sdk.zip -d /tmp/fosun-sdk
/Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install /tmp/fosun-sdk/openapi-python-sdk-main/
```

**Step 3 — 在指定虚拟环境中验证安装**

再次运行：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python -c "import fsopenapi; print(fsopenapi.__file__)"
```

确认 SDK 来自预期环境。

**Step 4 — 记录路径到记忆**

安装成功后写入 `MEMORY.md`：

```
## Fosun SDK
- SDK 安装路径: <实际路径>
- Python 环境: /Users/admin/.openclaw/workspace/.venv-fosun
- 安装方式: /Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install -e (本地) / /Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install (GitHub 下载)
```

> 如果 SDK 源码目录或虚拟环境后续被删除，必须同步删除或更新记忆中的对应记录。

---

## 2. 开通引导（首次使用）

当用户首次使用或尚未拥有 API Key 时，按以下决策逻辑执行：
**本地没有客户端密钥** → 执行开通流程：
   - 获取出口 IP：获取当前机器出口IP
   - 生成客户端密钥对：`bash skills/fosun_skills/fosun-sdk-setup/genkey.sh`（默认输出到当前目录的 `private.pem` / `public.pem`）
   - 将**客户端公钥** (`public.pem`) 和**出口 IP** 展示给用户
   - 引导用户携带上述信息向复星财富申请 OpenAPI 权限
     用户引导回复语句（请务必按此进行回复，要求用户可以一键复制IP+公钥，请严格按照以下纯文本模板输出客户的IP+公钥，仅替换【】中的内容，其他文字完全保留，格式（换行、标点）不可修改）：
     
     我要开通 OpenAPI 权限
     **我的出口IP：【出口IP】**
     **我的客户端公钥：【客户端公钥】**
     
     如有疑问，请联系客服。

     - 香港地区电话客服： +852 2979 6988 
     - 其他地区电话客服： 400 812 0922
   - 用户取回 **API Key** 和**服务端公钥**后 → 自动写入 `fosun.env`（见下方「从开通流程写入凭证」）
**如果本地已有客户端密钥并且没有API key** → 执行提醒流程：
   - 您是否已收到由复星财富审批通过的API Key和服务器公钥？如果已获取，请告知我，我将协助您完成配置。若尚未收到，是否需要我重新发送申请指引？

> 完整流程说明参见 [ONBOARDING.md](./ONBOARDING.md)，密钥生成说明参见 [KEYGEN.md](./KEYGEN.md)。

---

## 3. 配置凭证

SDK 需要以下环境变量才能正常工作：

| 环境变量 | 说明 |
|---------|------|
| `FSOPENAPI_SERVER_PUBLIC_KEY` | 服务端公钥（PEM 格式） |
| `FSOPENAPI_CLIENT_PRIVATE_KEY` | 客户端私钥（PEM 格式） |
| `FSOPENAPI_API_KEY` | API Key（开放平台下发，有有效期限） |
| `FSOPENAPI_BASE_URL` | 网关地址，固定 `https://openapi.fosunxcz.com`（不含末尾 `/`） |

> **当前策略**：凭证更新统一通过当前对话确认后直接修改工作区根目录的 `fosun.env`。

### 检查流程

查找凭证文件 `{workspace_root}/fosun.env`：

- **找到** → 自动加载到环境变量（PEM 密钥会 base64 解码），若用户要求换 Key，则只更新 `FSOPENAPI_API_KEY`。
- **未找到** → 通过对话向用户收集所需字段，并新建 `fosun.env`。

### 何时通过对话更新凭证

出现以下**任一**情况时，应在对话中确认并更新 `fosun.env`：

| 场景 | 说明 |
|------|------|
| 首次使用 | 未找到 `fosun.env`，凭证尚未配置 |
| 切换账号 | 用户明确表示要切换到另一个账号/API Key |
| 鉴权失败 | 接口返回 `401`、签名错误等，API Key 可能已过期 |
| 用户主动要求 | 用户说"重新配置"、"换个 Key"、"更新凭证"等 |

**从开通流程写入凭证**：

开通引导中已在本地生成客户端私钥，只需向用户收集复星下发的两项：

1. 读取本地已生成的客户端私钥（`private.pem`，即 genkey.sh 的输出路径）
2. 在对话中向用户收集：**API Key** 和**服务端公钥**
3. 将三项凭证 base64 编码后写入 `{workspace_root}/fosun.env`
4. 仅在回复中确认"已更新哪些字段"，不要回显完整敏感值

**完整配置**（用户已自行持有全部凭证）：

1. 在对话中向用户收集所有字段（服务端公钥、客户端私钥、API Key）。
2. 将公钥、私钥、API Key 写入 `{workspace_root}/fosun.env`。
3. 仅在回复中确认"已更新哪些字段"，不要回显完整敏感值。

**仅更新 API Key**（密钥不变，只换 Key）：

1. 在对话中向用户索取新的 API Key。
2. 只更新 `fosun.env` 中的 `FSOPENAPI_API_KEY`。
3. 保留原有公钥、私钥与其他配置不变。

**凭证变更统一通过对话确认后直接修改** `fosun.env`，不要再尝试调用额外的本地配置脚本。

### fosun.env 文件格式

凭证文件名固定为 `fosun.env`，PEM 密钥含换行符，**以 base64 编码存储**：

```env
FSOPENAPI_SERVER_PUBLIC_KEY=<PEM 公钥的 base64 编码>
FSOPENAPI_CLIENT_PRIVATE_KEY=<PEM 私钥的 base64 编码>
FSOPENAPI_API_KEY=<明文 API Key>
FSOPENAPI_BASE_URL=
```

加载时需对 PEM 字段做 base64 解码还原为原始 PEM 文本。

---

## 4. 支持的市场与币种

| 市场代码 | 说明 | 行情级别 | 默认币种 |
|----------|------|----------|----------|
| `hk` | 港股 | L2 | HKD |
| `us` | 美股 | L1（盘前/盘中/盘后） | USD |
| `sh` | 上交所（港股通） | L1 | CNH |
| `sz` | 深交所（港股通） | L1 | CNH |

**标的代码格式**：`marketCode + stockCode`，如 `hk00700`（腾讯）、`usAAPL`（苹果）、`sh600519`（茅台）、`sz000001`（平安银行）。

---

## 注意事项

- 会话由 SDK 自动管理（ECDH 握手、过期前自动续期），无需手动处理
- 可设置 `SDK_TYPE=ops` 环境变量切换 API 前缀为 `/api/ops/v1/...`
- **不要自己写 Python 代码调用 SDK**，直接使用 `fosun-trading` skill 中 `code/` 目录下的命令行脚本

---

## ⛔ AI 调用策略限制（必须遵守）

以下限制针对 OpenClaw 申请的 API Key，AI 在调用任何接口前**必须**自行校验并遵守。

### API 调用频率限制

| 维度 | 限制 | 超限处理 |
|------|------|---------|
| 每秒请求数（QPS） | 单个 API Key ≤ 5 次/秒 | 返回 `429 Too Many Requests` |
| 每分钟请求数 | 单个 API Key ≤ 60 次/分钟 | 拒绝新请求 |
| 每小时下单次数（买卖一起） | 单个客户 ≤ 10 笔/小时 | 该小时内拒绝新委托 |
| 每日总下单次数（买卖一起） | 单个客户 ≤ 50 笔/天 | 当日拒绝新委托 |

### 安全与权限限制

| 限制类型 | 具体规则 |
|---------|---------|
| IP 白名单 | 请求出口 IP 需提前录入白名单，不在白名单直接拒绝访问 |
| 防重放攻击 | 同一笔请求 5 分钟内不允许重复提交（Redis 记录 requestId + nonce） |

### 开放接口权限

仅开放以下接口：资金查询、持仓查询、可买可卖查询、下单、撤单、订单查询、流水查询、行情查询。

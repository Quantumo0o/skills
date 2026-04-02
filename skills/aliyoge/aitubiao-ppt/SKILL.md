---
name: aitubiao-ppt
version: 1.0.1
description: AI PPT/演示文稿生成。根据用户主题或内容自动生成PPT演示文稿项目。当用户想要创建PPT、演示文稿、幻灯片时使用，触发词包括"创建PPT"、"做PPT"、"做个演示文稿"、"生成幻灯片"、"create PPT"、"make slides"、"generate presentation"、"make a PPT"等。
---

# AI PPT/演示文稿生成

根据用户提供的主题、内容或文件，自动生成PPT演示文稿项目。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用 `create-project` 接口。
4. **仅通过 API 创建PPT**：禁止使用本地工具（reveal.js、impress.js、Google Slides API、python-pptx、LibreOffice 等）生成PPT。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403，立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 重试规则**：最多重试 3 次（间隔 5 秒），仍失败则停止并告知用户。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成PPT作为替代" → 违反规则 4
- ❌ "至少让用户看到一些演示文稿效果" → 本技能唯一输出方式是 aitubiao API
- ❌ "401 可能是暂时性的，重试几次" → 401 是认证失败，重试无意义，按规则 5 处理

## 认证

在调用任何 API 之前，先检查凭证状态。

### 检查凭证

读取凭证文件，判断认证状态：

```bash
cat ~/.aitubiao/credentials 2>/dev/null
```

根据结果判断：
- **文件不存在或为空** → 执行下方"配置凭证"流程
- **`API_KEY` 为空** → 执行下方"配置凭证"流程
- **`API_KEY` 不以 `sk_v1_` 开头** → 告知用户"当前 API Key 已失效，请前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 重新创建一个 API Key"
- **`BASE_URL` 为空或不等于 `https://api.aitubiao.com`** → 执行下方"配置凭证"流程（保留现有 API_KEY，仅修正 BASE_URL）
- **`API_KEY` 格式正确且 `BASE_URL` 正确** → 认证通过

认证通过后，加载环境变量：
```bash
source ~/.aitubiao/credentials
export BASE_URL="${BASE_URL:-https://api.aitubiao.com}"
```

### 配置凭证

1. 向用户索要 API Key（格式：`sk_v1_...`）。如果没有，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 创建一个新的 API Key，然后将创建好的 Key 粘贴回来。
2. 保存凭证：
```bash
mkdir -p ~/.aitubiao
cat > ~/.aitubiao/credentials << EOF
API_KEY=<用户提供的key>
BASE_URL=https://api.aitubiao.com
EOF
chmod 600 ~/.aitubiao/credentials
```
3. 重新读取文件验证配置是否成功。

凭证保存在 `~/.aitubiao/credentials`，跨会话持久生效。

## 服务架构

所有 API 使用统一的服务地址：

| 默认地址 | API前缀 | 认证方式 |
|---------|---------|---------|
| `https://api.aitubiao.com/` | `/api/v1/agent` | `Authorization: Bearer <API_KEY>` |

**重要**：所有非流式响应都包裹在统一格式中：
```json
{ "code": 0, "msg": "ok", "data": { ... } }
```
实际业务数据在 `data` 字段内。**即使 HTTP 状态码为 200，也必须检查 `code` 字段是否为 0，非 0 表示业务错误。**

## 支持的输入方式

| 输入方式 | 处理方法 |
|---------|---------|
| **主题文本** | 用户直接输入主题（如"人工智能发展趋势"），直接作为 `prompt` |
| **粘贴内容** | 用户粘贴完整文本，作为 `prompt` |
| **本地文件**（TXT/MD/CSV） | 用 Read 工具读取文件内容，作为 `prompt` |
| **Excel 文件**（.xlsx/.xls） | 使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 |

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别和确认内容（前置条件：第一步认证通过）

获取用户内容后，向用户确认以下信息：

- 内容/主题是否正确？
- 需要生成多少页？（默认 6 页，上限由会员等级决定，可通过配额接口获取 `pptGeneratePageLimit`）
- 主题风格偏好？（浅色 `light` / 深色 `dark`，默认浅色）
- 主题色偏好？（可选：蓝色`#004eff`、橙色`#f16f0b`、红色`#ee4646`、天蓝`#2197fc`、紫色`#8a61ec`、绿色`#35b13f`、动态配色`dynamic`）
- 有没有特殊要求？（如"简洁风格"、"多用图表"等，作为 `requirements`）

### 第三步：检查配额并确认费用（前置条件：第二步内容已确认）

在创建PPT前，**必须**检查用户的 AI贝余额和项目配额，并向用户确认费用后才能继续。

收到 401/403 按强制规则 5 处理。超时/500 按强制规则 6 处理。

#### 3.1 查询配额

```bash
curl -s --max-time 10 -X GET "${BASE_URL}/api/v1/agent/quota" \
  -H "Authorization: Bearer ${API_KEY}"
```

#### 3.2 计算总费用

使用 `features.pptProjectCreate` 的 cost 和 billingModel 计算费用：

| billingModel | 计算方式 | 示例 |
|-------------|---------|------|
| `per-page` | 总费用 = cost × pageCount | 生成6页PPT: 10 × 6 = 60 AI贝 |

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作将消耗 {totalCost} 个 AI贝（PPT/图文生成，按页计费：{cost} AI贝/页 × {pageCount} 页）
当前余额: {shellBalance} 个 AI贝
操作后余额: {shellBalance - totalCost} 个 AI贝
项目数: 已用 {projectsUsed}/{projectsLimit}

是否继续？
```

- 如果 `shellBalance < totalCost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**
- 如果 `projectsRemaining <= 0`：告知用户当前项目数已满，需前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续，**不要继续**
- 如果 `pageCount > pptGeneratePageLimit`：告知用户请求的页数超过当前会员等级限制（最多 `pptGeneratePageLimit` 页），请减少页数或升级会员，**不要继续**

### 第四步：创建PPT项目（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

API 会在项目创建后立即返回项目地址（不等待所有页面生成完成）。用户可以通过项目地址实时查看生成进度。

```bash
curl -s --max-time 120 -X POST "${BASE_URL}/api/v1/agent/infographic/create-project" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<用户的主题或内容>",
    "pageCount": 6,
    "theme": "light",
    "projectName": "我的PPT"
  }'
```

响应格式（需解析 `data` 字段）：
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "success": true,
    "outlineId": "uuid...",
    "project": {
      "id": "cuid...",
      "title": "我的PPT",
      "status": "generating",
      "width": 960,
      "height": 540,
      "projectUrl": "https://app.aitubiao.com/workspace/cuid..."
    },
    "quota": {
      "shellCoinCost": 60,
      "shellBalance": 40,
      "projectsUsed": 6,
      "projectsLimit": 50,
      "projectsRemaining": 44,
      "canCreateProject": true
    },
    "totalPages": 6,
    "completedPages": 0,
    "failedPages": 0,
    "processingTime": "5000ms"
  }
}
```

完整请求/响应格式详见 [ppt-api.md](references/ppt-api.md)。

### 第五步：返回结果（前置条件：第四步创建成功）

**立即向用户展示项目 URL**（从 `data.project.projectUrl` 获取）。PPT 页面仍在后台生成中，用户可以在浏览器中打开此链接实时查看生成进度和最终效果。格式示例：
```
您的 PPT 项目已创建成功！页面正在后台生成中（通常需要 5-10 分钟）。
请点击下方链接实时查看生成进度和编辑 PPT：
https://app.aitubiao.com/workspace/xxxxxxxxx
```

同时提供以下补充信息：
- 项目 ID（从 `data.project.id` 获取）
- 总页数
- 资源消耗：本次消耗 AI贝数、剩余 AI贝、已用项目数/上限

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|------------|------|---------|
| 401/403 | API Key 无效、过期或权限不足 | 按强制规则 5：立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 检查或重新创建 |
| 429 | 频率限制 | 等待 30 秒后重试一次，仍失败则告知用户稍后再试 |
| 500 | 服务器错误 | 按强制规则 6：重试最多 3 次 |

当 `code` 不为 0 时，表示业务错误：

| code | 含义 | 处理方式 |
|------|------|---------|
| 90001 | AI贝不足 | 向用户展示 `quota` 中的余额和消耗信息，并引导其前往 aitubiao 网站购买会员或充值后再继续 |
| 40007 | 项目数已满 | 向用户展示 `quota` 中的已用/上限，并引导其前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续 |
| 40015 | 项目创建失败 | 系统内部错误，建议重试 |

## API 参考

详细的接口规格说明见 [ppt-api.md](references/ppt-api.md)。

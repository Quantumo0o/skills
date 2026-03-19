---
name: tced-skill
version: 0.3.0
description: "腾讯云企业网盘 TCED 集成技能。当用户需要管理企业网盘文件（上传、下载、删除、浏览、搜索），管理空间（列出、切换），或进行账号认证（登录、登出、切换）时使用。触发关键词：企业网盘、网盘、TCED、SMH、文件上传、文件下载、云端文件、个人空间、团队空间。"
---

# 腾讯云企业网盘 (TCED) 技能

通过 tced-mcp MCP 工具操作腾讯云企业网盘，支持 OAuth2 授权认证、空间管理和文件操作。

## 概览

TCED MCP Server 基于 OAuth2 第三方授权模式，调用 `login` 唤起网盘页面完成授权后，即可操作已授权的空间和文件。

| 类别 | 工具 | 说明 |
|------|------|------|
| 认证 | `login` | 发起 OAuth2 授权（唤起网盘页面） |
| 认证 | `logout` | 登出账号 |
| 认证 | `list_accounts` | 列出所有已登录账号 |
| 认证 | `switch_account` | 切换活跃账号 |
| 认证 | `current_account` | 查看当前账号信息 |
| 空间 | `list_authorized_spaces` | 列出已授权空间 |
| 空间 | `switch_space` | 切换到指定空间 |
| 空间 | `current_space` | 查看当前活跃空间 |
| 文件 | `upload_file` | 上传文件（本地文件或文本内容） |
| 文件 | `download_file` | 下载文件（获取链接或保存到本地） |
| 文件 | `file_info` | 查看文件/目录详情 |
| 文件 | `list_directory` | 列出目录内容 |
| 文件 | `search_files` | 搜索文件和目录 |

## 首次使用 — 自动设置

当用户首次要求操作企业网盘时，按以下流程操作：

### 步骤 1：检查 MCP 服务是否可用

尝试调用 `current_account` 检查 tced-mcp 是否已在 MCP 客户端中配置并运行。

- **如果可用**：跳到「OAuth2 授权登录」
- **如果不可用**：继续步骤 2

### 步骤 2：配置 MCP 客户端

tced-mcp 已发布到 npm，无需手动安装。只需在 MCP 客户端配置文件（如 `mcp.json`）中添加：

```json
{
  "mcpServers": {
    "tced-mcp": {
      "command": "npx",
      "args": ["-y", "tced-mcp@1.0.1"],
      "env": {
        "TCED_PAN_DOMAIN": "https://pan.tencent.com",
        "TCED_BASE_PATH": "https://api.tencentsmh.cn"
      }
    }
  }
}
```

> **说明**：
> - `args` 中使用锁定版本号（如 `tced-mcp@1.0.1`），避免自动拉取未经审核的新版本。升级前请先查看 [npm 发布记录](https://www.npmjs.com/package/tced-mcp) 确认变更内容。
> - `env` 字段指定网盘域名和 API 地址。如果是私有化部署，将域名替换为对应的私有化地址即可。

配置完成后重启 MCP 客户端使配置生效。

### 步骤 3：验证安装

也可以使用脚本快速检查环境：

```bash
{baseDir}/scripts/setup.sh --check
```

---

## OAuth2 授权登录

### 检查登录状态

调用 `current_account` 检查是否已登录。已登录则跳到「选择空间」，否则继续登录。

### 发起授权登录

调用 `login`，MCP 自动唤起网盘页面（`pan.tencent.com`），用户在网盘页面完成：
1. 登录企业网盘账号
2. 选择要授权的企业
3. **选择要授权的空间** — ⚠️ 每次授权只选一个空间，AccessToken 与该空间一对一绑定
4. 点击「同意授权」

`login` 阻塞等待用户完成授权（最长 5 分钟超时）。授权完成后自动完成 token 交换，若只授权了一个空间则自动切换到该空间。

> **⚠️ 核心规则**：每个 AccessToken 只对应一个空间。如需操作其他空间，必须重新调用 `login` 授权目标空间。

> **⚠️ 环境要求**：`login` 需要有图形界面环境（桌面系统），不支持无界面服务器（Linux SSH/Docker 等）。

### 选择空间（多空间场景）

如果授权了多个空间：
1. 调用 `list_authorized_spaces` 获取空间列表
2. 调用 `switch_space(spaceId)` 切换到目标空间

---

## 核心操作流程

### 浏览目录

```
list_directory(filePath: "docs", limit: 50)
```

支持 marker 翻页、排序和筛选，详见 `references/api_reference.md`。

### 搜索文件

```
search_files(keyword: "报告", scope: "fileName")
```

### 文件上传

```
upload_file(filePath: "远端路径", localFilePath: "/本地文件路径")
upload_file(filePath: "远端路径", content: "文件内容")
```

冲突策略：`rename`（默认自动重命名）、`overwrite`（覆盖）、`ask`（提示用户确认）。

### 文件下载

```
download_file(filePath: "远端文件路径")
download_file(filePath: "远端文件路径", localFilePath: "/本地保存路径")
```

### 查看文件信息

```
file_info(filePath: "文件/目录路径")
```

---

## 多账号与多空间管理

### AccessToken 与空间一对一绑定

- **一个 AccessToken = 一个空间**，切换空间需要对应的 AccessToken
- `switch_space` 切换时，若目标空间无有效 AccessToken，需重新 `login` 授权
- `switch_account` 切换账号后，AccessToken 和空间随之切换

### 多账号操作

- `list_accounts` — 查看已登录账号
- `switch_account(accountId)` — 切换活跃账号
- `logout(accountId?)` — 登出指定或当前账号

### Token 自动刷新

AccessToken 过期时自动通过 RefreshToken 刷新；RefreshToken 过期后需重新 `login` 授权。

---

## Resource 与 Prompt

- **Resource** `tced://status` — 查看 MCP Server 完整状态
- **Prompt** `quickstart` — 根据当前状态自动引导下一步操作

## 常见问题排查

### 授权登录失败

**现象**：浏览器授权成功，但回调后提示错误。

**解决**：
1. 确保 `mcp.json` 中配置了正确的 `env.TCED_PAN_DOMAIN` 和 `env.TCED_BASE_PATH`
2. 刷新 MCP 连接，重新发起 `login`

### 浏览器未唤起

**现象**：调用 `login` 后浏览器没有弹出。

**解决**：确保 Node.js 版本 >= 18，然后刷新 MCP 连接重试。

### 配置修改不生效

**现象**：修改了配置但 MCP 行为没变。

**解决**：修改配置后必须**刷新 MCP 连接**（重启进程）使配置生效。

### 如何更新 tced-mcp

将 `mcp.json` 中的版本号更新为目标版本（如 `tced-mcp@1.0.2`），然后刷新 MCP 连接。

> **安全建议**：升级前请先查看 [npm 包页面](https://www.npmjs.com/package/tced-mcp) 确认新版本的变更内容和发布者。

如果 npx 缓存了旧版本，可手动清除后重试：
```bash
npm cache clean --force
```

---

## 安全与隐私声明

### 本地数据

tced-mcp 会在本地创建并管理以下文件：

| 文件路径 | 内容 | 说明 |
|----------|------|------|
| `~/.tced-mcp/auth.json` | OAuth2 令牌、域名配置 | 包含 access_token 和 refresh_token，属于敏感凭据 |

- 该文件由 tced-mcp 进程自动创建和更新，用户无需手动编辑
- **请勿将 `~/.tced-mcp/` 目录提交到版本控制或分享给他人**
- 登出（`logout`）会清除对应账号的令牌

### npm 包安全

- 本技能通过 `npx` 从 npm 拉取并执行 `tced-mcp` 包
- **强烈建议使用锁定版本号**（如 `tced-mcp@1.0.1`），而非 `@latest`，以避免供应链风险
- 安装前可通过以下方式验证包的合法性：
  - 查看 npm 包页面：https://www.npmjs.com/package/tced-mcp
  - 检查包的发布者和 GitHub 源代码仓库
- 首次使用建议在隔离环境或测试账号下运行

### OAuth2 授权

- `login` 通过浏览器完成 OAuth2 授权，tced-mcp 不直接接触用户的网盘账号密码
- AccessToken 和 RefreshToken 仅存储在本地 `auth.json` 中，不会上传到第三方服务
- `tced://status` 资源会返回令牌状态信息（是否有效、过期时间），但不包含令牌原文

---

## 使用规范

1. **操作前确认状态**：任何文件操作前，确保已登录且已选择空间
2. **路径格式**：云端路径使用相对路径（如 `docs/readme.txt`），不带前导斜杠
3. **下载链接有时效性**：`download_file` 返回的 URL 需尽快使用
4. **切换账号后空间随之切换**：`switch_account` 后需重新确认空间
5. **切换空间需对应 AccessToken**：操作新空间需重新 `login` 授权该空间
6. **错误处理**：工具返回 `isError: true` 时，先检查登录和空间状态
7. **大目录分页浏览**：`list_directory` 默认返回 50 项，使用 `marker` 翻页

## 工具详细参数

详细的工具参数定义和错误处理见 `references/api_reference.md`。

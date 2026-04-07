---
name: media-saber-site-ops
description: 通过 Media Saber MCP 进行站点操作，包括签到、数据同步、通知、消息和站点诊断。
---

# Media Saber 站点操作

通过 Media Saber MCP 使用此技能进行 PT 站点操作和诊断。

## 🔐 安全性和权限声明

本技能需要以下权限和凭证，确保完全透明：

### 所需凭证
- **MCP_ENDPOINT_URL**: Media Saber MCP 服务的实际地址
  - 示例：`http://localhost:22698/message`
  - 敏感性：**低**（地址通常是内部网络或已知地址）
  - 用途：连接到 Media Saber MCP 服务

- **API_KEY**: 用于验证与 Media Saber MCP 服务的连接
  - 存储位置：OpenClaw 环境变量或配置文件
  - 敏感性：**高**（不会在日志中显示）
  - 用途：所有站点操作和诊断

### 所需网络/文件访问
- **配置文件修改**：`~/.claw/mcpServers.json`
  - 用途：存储 Media Saber MCP 端点配置
  - 访问类型：读和写
  - 操作：OpenClaw 安装时自动配置（需用户确认）

### 数据隐私
- 所有站点操作在 Media Saber 系统内执行
- API Key 从不发送至第三方
- 诊断信息仅用于本地分析

### ⚠️ 信任验证与最小权限

与外部端点交互时正常执行以下步骤，确保最小权限不超预期：

**1. API Key 最小权限原则**
- 需求介于想要接入的是什么 Media Saber 功能（站点管理、诊断等）
- 尽可能用于数据查询专用 API 密钥
- 不需要提供完整系统管理权限

**2. 端点信任**
- 校验端点是可信的（例如你拥有的属于团队的作地）
- 不要接入未知组织的远程端点
- 使用 HTTPS、验证证书等安全配置

**3. 配置文件保护**
- `~/.claw/mcpServers.json` 配置了你的整个端点信息，包含了敏感的 API 密钥
- 每次都要确保文件的文件权限（推荐：600）
- 定期更新、旋转 API 密钥

## ⚠️ 必须配置：MCP 服务连接

在使用此技能前，**您必须配置以下信息**：

### 1. MCP 地址配置（需要用户填写）

- **transport**: `streamable-http`
- **endpoint**: `<MCP_ENDPOINT_URL>` （例如：http://localhost:22698/message 或你的其他部署地址）
- **需要用户填写实际的 MCP 服务地址**

### 2. 认证信息配置（需要用户填写）

**请在以下位置之一配置您的 API_KEY**：

#### 方式 A：OpenClaw 配置（推荐）

在 `~/.claw/mcpServers.json` 中配置 Media Saber 连接：

```json
{
  "mcpServers": {
    "MediaSaber": {
      "transport": "streamable-http",
      "url": "http://localhost:22698/message",
      "headers": {
        "Authorization": "Bearer sk-YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**替换 `sk-YOUR_API_KEY_HERE` 为您的实际 API 密钥**

#### 方式 B：环境变量配置

- 设置环境变量：`MEDIA_SABER_API_KEY=sk-your-api-key`
- 该密钥将被自动注入到请求头中

### 3. 获取 API_KEY

请从 Media Saber 系统获取您的 API 密钥：
- 访问 Media Saber Web 界面
- 进入 "设置" → "API 密钥"
- 复制您的密钥（通常以 `sk-` 开头）

**安全提示**：
- ⚠️ **切勿将 API_KEY 硬编码在代码、提示词或文档中**
- ⚠️ **切勿通过不安全的通道传输 API_KEY**
- ⚠️ **定期轮换您的 API_KEY**
- ⚠️ **不要与他人共享您的 API_KEY**

## 主要工具

- get_sites(name?)
- get_site_data(name?)
- get_site_notice(name?)
- get_site_message(name?)
- today_site_data()
- total_site_data()
- site_sign_in()
- sync_site_data()
- sync_site_notice()
- sync_site_message()
- test_site()
- test_site_rss()
- update_site_configs()

## 工作流

1. 首先使用 get_sites/get_site_data 读取当前状态。
2. 运行 site_sign_in 和必需的同步工具。
3. 使用 today_site_data 和 total_site_data 进行验证。
4. 如果发现问题，运行 test_site 和 test_site_rss。
5. 报告每个站点的结果和失败原因。

## 防护措施

- 优先选择读操作然后写操作。
- 批量操作应包括摘要输出。
- 切勿暴露授权令牌。

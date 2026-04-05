---
name: r2-uploader
description: 使用 wrangler 上传文件到 Cloudflare R2。当用户需要上传文件到 R2、批量上传、从 URL 上传、或获取上传后的公开 URL 时使用。关键词：上传、R2、Cloudflare、存储、wrangler、bucket。
---

# R2 文件上传

使用 wrangler CLI 上传文件到 Cloudflare R2 对象存储。

## 参数

| 参数 | 来源 | 说明 |
|------|------|------|
| bucket | `$R2_BUCKET` 或用户指定 | R2 存储桶名称 |
| domain | `$R2_DOMAIN` 或用户指定 | 自定义域名（可选） |
| path | 自动生成 | `agent/YYYYMMDD/` 格式 |

## 核心流程

### 1. 定位文件

```bash
# 用户提供文件名时，查找文件
find /Users/victor -name "<filename>" -type f 2>/dev/null | head -5

# 验证文件存在
ls -la "<file-path>"
```

### 2. 生成路径

```bash
R2_PATH="agent/$(date +%Y%m%d)/$(basename "<file>")"
```

### 3. 执行上传

```bash
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file-path>" --remote
```

### 4. 返回 URL

```bash
echo "https://$R2_DOMAIN/$R2_PATH"
```

## 常用命令

```bash
# 列出 buckets
wrangler r2 bucket list

# 上传文件
wrangler r2 object put "<bucket>/<path>/<file>" --file "<local-path>" --remote

# 从 URL 上传
curl -sL "<url>" | wrangler r2 object put "<bucket>/<path>/<file>" --file - --remote
```

## 高级功能

- **批量上传、并发上传**: 见 [references/advanced.md](references/advanced.md)
- **错误处理、重试机制**: 见 [references/error-handling.md](references/error-handling.md)

## URL 格式

上传成功后：

| 类型 | URL 格式 |
|------|----------|
| 默认 | `https://pub-<account-id>.r2.dev/<path>/<file>` |
| 自定义域名 | `https://$R2_DOMAIN/<path>/<file>` |
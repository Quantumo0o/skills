---
name: huo15_searxng
version: 1.2.0
description: SearXNG 自托管搜索引擎一键部署 - Docker Compose + OpenClaw 配置自动化 (v1.2.0)
homepage: https://github.com/zhaobod1/huo15-skills
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["docker", "nc"]
---

# huo15-searxng

SearXNG 自托管搜索引擎一键部署技能。

## 触发词

- "安装 SearXNG"、"部署 SearXNG"
- "searxng"、"SearXNG"
- "自托管搜索"、"私有搜索"
- "搭建搜索"

## 功能

当用户请求安装或部署 SearXNG 时，执行 `scripts/install.sh` 进行自动化部署：

1. 检查 Docker 和 docker compose 环境
2. 检测可用端口（8888 → 8910 自动检测冲突）
3. 一键部署 SearXNG 容器（含 limiter.toml 修复 403 问题）
4. 等待服务就绪并验证 JSON API
5. 自动配置 OpenClaw 环境变量

## 使用方式

```
@贾维斯 安装 SearXNG
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `bash .../install.sh` | 安装/升级 SearXNG |
| `bash .../status.sh` | 查看运行状态 |
| `bash .../uninstall.sh` | 卸载 SearXNG |

## 技术细节

- SearXNG 镜像：`searxng/searxng:latest`
- 数据目录：`~/docker/searxng/`
- 默认端口：8888（自动检测冲突）
- OpenClaw 配置：`SEARXNG_BASE_URL` 环境变量

## 前提条件

- Docker Desktop (macOS) / Docker Engine (Linux)
- docker compose v2
- `nc` 命令（macOS/Linux 内置）

## 排障指南

### 403 Forbidden
**原因**：botdetection 模块缺少 `limiter.toml` 文件  
**解决**：脚本已自动创建空文件 `~/docker/searxng/searxng/limiter.toml`

### JSON API 返回 HTML
**原因**：`settings.yml` 未启用 json format  
**解决**：检查 `~/docker/searxng/searxng/settings.yml` 是否包含：
```yaml
search:
  formats:
    - html
    - json
```

### 主页正常但搜索失败
**调试**：
```bash
# 查看容器日志
docker logs searxng

# 测试 JSON API
curl 'http://localhost:8888/search?q=test&format=json'

# 测试健康检查
curl http://localhost:8888/healthz
```

### 环境变量未生效
```bash
source ~/.zshrc
echo $SEARXNG_BASE_URL
```

## 踩坑记录（2026-04-12）

| 问题 | 根因 | 修复 |
|------|------|------|
| 所有请求 403 | botdetection 缺 limiter.toml | 创建空文件 |
| JSON API 返回 HTML | settings.yml 默认不启用 json | 显式声明 `formats: [html, json]` |
| secret_key 报错 | 用了 `$(...)` 字符串而非实际值 | 使用 `cat /dev/urandom` 生成真实密钥 |

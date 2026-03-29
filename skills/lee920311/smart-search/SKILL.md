---
name: smart-search
description: 智能搜索引擎切换。优先使用 SearX 1.1.0（免费无限），失败自动降级 Tavily。
author: 李洋
version: 2.0.0
tags:
  - search
  - searx
  - tavily
  - web-search
  - chinese
triggers:
  - "搜索"
  - "查查"
  - "最新的"
  - "2026"
  - "写文案"
  - "小红书"
  - "公众号"
metadata: {
  "emoji": "🔍",
  "requires": {
    "bins": ["curl", "python3"],
    "env": ["SEARXNG_URL", "TAVILY_API_KEY"]
  }
}
---

# Smart Search - 智能搜索引擎切换 v2

**优先使用 SearX 1.1.0（免费无限），失败自动降级 Tavily**

## 决策逻辑

### 智能场景识别

| 场景类型 | 关键词 | 推荐引擎 | 原因 |
|---------|--------|---------|------|
| **AI 内容生成** | 小红书、文案、公众号、生成、总结、摘要 | Tavily | 带 AI 摘要，辅助创作 |
| **日常查询** | 查询、是什么、怎么用、教程 | SearX | 免费无限，响应快 |
| **新闻资讯** | 新闻、资讯、最新、动态 | SearX | 多引擎聚合，全面 |
| **深度调研** | 调研、研究、了解、学习 | SearX | 结果全面，可定制 |
| **用户指定** | 用 tavily、用 searx | 按用户 | 尊重选择 |

### 优先级

| 优先级 | 引擎 | 使用场景 |
|--------|------|---------|
| 1️⃣ | **SearX 1.1.0** | 日常搜索、新闻资讯、深度调研（90%） |
| 2️⃣ | **Tavily** | AI 内容生成、紧急备用（10%） |

**降级策略：**
```
SearX 1.1.0 → Tavily（兜底）
```

## 配置

### 必需配置
```bash
# ~/.openclaw/.env

# SearX 1.1.0（主力引擎，必须部署）
SEARXNG_URL=http://localhost:8080
```

### 可选配置（AI 内容生成）
```bash
# Tavily API Key（推荐配置，免费 1000 次/月）
TAVILY_API_KEY=your_api_key_here  # 从 https://tavily.com 获取
```

**配置说明：**
- ✅ **不配置 Tavily**：日常搜索用 SearX（免费无限），AI 内容生成时降级 SearX
- ✅ **配置 Tavily**：AI 内容生成用 Tavily（带 AI 摘要），日常搜索用 SearX
- 💡 **推荐配置**：两者都配置，体验最佳

**获取 Tavily API Key（2 分钟）：**
1. 访问 https://tavily.com
2. 注册免费账号（1000 次/月免费额度）
3. 获取 API Key
4. 添加到 `~/.openclaw/.env`

### 可选（多 API Key 轮换）
```bash
TAVILY_API_KEY_2=your_backup_key_1
TAVILY_API_KEY_3=your_backup_key_2
```

## 部署 SearX 1.1.0

### 方式 A：一键部署脚本（推荐）
```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
chmod +x deploy-searx.sh
./deploy-searx.sh
```

### 方式 B：Docker 命令
```bash
docker run -d --name searx \
  -p 8080:8080 \
  -e SEARX_SECRET='your_secret_here' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

### 方式 C：Docker Compose
```bash
# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  searx:
    image: searx/searx:1.1.0-69-75b859d2
    ports:
      - "8080:8080"
    environment:
      - SEARX_SECRET=your_secret_here
    restart: unless-stopped
EOF

docker compose up -d
```

**为什么用旧版？**
- SearXNG 2026.x 启用了严格的 bot 检测，JSON API 返回 403
- SearX 1.1.0 无 bot 检测，API 完全可用
- 免费无限搜索，适合晨间简报等高频场景

**详细文档：** 参考 `README.searx.md`

## 使用示例

**日常搜索**
```bash
./search.sh "AI 新闻"
```

**指定结果数**
```bash
./search.sh "AI 新闻" 10
```

## 工具调用

### SearX 搜索（优先）
```bash
curl -s "http://localhost:8080/search?q=查询&format=json"
```

### Tavily 搜索（降级备用）
```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"query": "查询内容", "max_results": 5, "include_answer": true}'
```

## 成本对比

| 引擎 | 费用 | 额度 | 使用场景 | 占比 |
|------|------|------|----------|------|
| SearX 1.1.0 | 免费 | ♾️ 无限 | 日常搜索、晨间简报 | 90% |
| Tavily | 免费 | 1000 次/月 | AI 内容生成、备用 | 10% |

**晨间科技简报成本：**
- 每天 1 次 × 30 天 = 30 次/月
- 使用 SearX：**0 成本** ✅
- Tavily 额度保留：970 次/月备用

**月度搜索预算（按 600 次/月）：**
```
SearX:   540 次 × ¥0 = ¥0
Tavily:   60 次 × ¥0 = ¥0（免费额度内）
────────────────────────────────
总计：   600 次 = ¥0 ✅
```

## 架构优势

1. **免费优先** - SearX 1.1.0 承担主要流量
2. **稳定兜底** - Tavily 保证服务可用性
3. **智能降级** - 失败自动切换，用户无感知
4. **成本优化** - 90% 搜索 0 成本

## 故障排查

**SearX 不可用时：**
```bash
# 检查容器状态
docker ps | grep searx

# 查看日志
docker logs searx --tail 20

# 重启容器
docker restart searx
```

**降级到 Tavily：**
- 自动触发，无需手动干预
- 日志显示：`⚠️  SearX 不可用，降级到 Tavily...`

---

**最后更新：** 2026-03-26  
**版本：** 2.0.0（SearX 1.1.0 + Tavily 双引擎）

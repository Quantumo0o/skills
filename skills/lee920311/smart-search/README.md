# Smart Search - 决策参考

**双引擎架构：SearX 1.1.0（免费）+ Tavily（备用）**

---

## 🎯 核心策略

| 引擎 | 定位 | 费用 | 使用占比 |
|------|------|------|---------|
| **SearX 1.1.0** | 主力引擎 | ♾️ 免费 | 90% |
| **Tavily** | 备用兜底 | 1000 次/月 | 10% |

---

## 📋 决策规则

### 默认流程
```
1. 调用 SearX 1.1.0
   ↓ 如果失败（容器停止/网络问题）
2. 自动降级到 Tavily
   ↓ 返回结果
```

### 用户指定优先
```
"用 tavily 搜索 XXX" → Tavily
"用 searx 搜索 XXX" → SearX
```

---

## 📊 Token 预算

**按每天 20 次搜索：**

| 引擎 | 日次数 | 月度次数 | 成本 |
|------|--------|----------|------|
| SearX | 18 次 | 540 次 | ¥0 |
| Tavily | 2 次 | 60 次 | ¥0（免费额度内） |
| **总计** | 20 次 | 600 次 | **¥0** ✅ |

**晨间科技简报：**
- 每天 1 次 × 30 天 = 30 次/月
- **全部使用 SearX = 0 成本**

---

## 🚀 部署指南

### SearX 1.1.0（必需）
```bash
docker run -d --name searx \
  -p 8080:8080 \
  -e SEARX_SECRET='local-secret-2026' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

### Tavily（备用）
```bash
# ~/.openclaw/.env
TAVILY_API_KEY=tvly-xxx
```

---

## 🔧 配置

**~/.openclaw/.env**
```bash
# SearX 本地实例
SEARXNG_URL=http://localhost:8080

# Tavily API Key（备用）
TAVILY_API_KEY=tvly-xxx

# 备用 Key（可选）
TAVILY_API_KEY_2=tvly-yyy
```

---

## 📝 使用示例

**日常搜索**
```
问：AI 最新进展
→ SearX（免费）
```

**AI 内容生成**
```
问：帮我写小红书文案
→ SearX → Tavily（带 AI 摘要）
```

**指定引擎**
```
问：用 tavily 搜索 XXX
→ Tavily（尊重用户选择）
```

---

## 💡 架构优势

| 优势 | 说明 |
|------|------|
| 🆓 **零成本** | 90% 搜索使用免费 SearX |
| 🔄 **自动降级** | 失败自动切换，用户无感知 |
| 🛡️ **稳定可靠** | 双引擎保障，永不宕机 |
| 📈 **可扩展** | 轻松添加更多搜索引擎 |

---

## 🔍 故障排查

**SearX 容器检查**
```bash
docker ps | grep searx
docker logs searx --tail 20
docker restart searx
```

**API 测试**
```bash
curl "http://localhost:8080/search?q=test&format=json"
```

**降级日志**
```
⚠️  SearX 不可用，降级到 Tavily...
✅ 搜索成功
```

---

## 📈 性能对比

| 指标 | SearX 1.1.0 | Tavily |
|------|------------|--------|
| 响应时间 | ~2s | ~1.5s |
| 结果质量 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| AI 摘要 | ❌ | ✅ |
| 费用 | ¥0 | ¥0.01/次 |
| 稳定性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**最后更新：** 2026-03-26  
**版本：** 2.0.0

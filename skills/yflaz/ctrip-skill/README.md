# ctrip-skill

携程旅行搜索 Skill - 机票/火车票查询与行程规划

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/ctrip-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

---

## 🚀 快速开始

### 安装

```bash
# 通过 clawhub 安装
clawhub install ctrip-skill

# 安装依赖
cd skills/ctrip-skill
pip install -r requirements.txt
playwright install chromium
```

### 使用示例

```bash
# 搜索机票
python scripts/ctrip_client.py flight 上海 曼谷 2026-10-01

# 行程规划
python scripts/route_planner.py plan '上海，曼谷，清迈，吉隆坡' 8

# 运行示例
python examples/search_example.py
```

---

## 📚 文档

详细文档请参阅 [SKILL.md](SKILL.md)

---

## 📋 功能特性

- ✈️ **机票搜索**: 单程/往返/多程
- 🚄 **火车票搜索**: 高铁/动车/普快
- 🗺️ **行程规划**: 最优路线推荐
- 💰 **价格对比**: 多日期/多路线对比
- 📅 **每日计划**: 自动生成行程安排

---

## 🛠 开发

```bash
# 开发模式（显示浏览器）
export CTRIP_HEADLESS=false

# 运行测试
python examples/search_example.py
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- 参考架构：xiaohongshu-mcp
- 数据源：携程旅行 (ctrip.com)

---

**作者**: 三省六部  
**版本**: 1.0.0  
**日期**: 2026-03-24

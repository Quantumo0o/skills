---
name: pinterest-crawler
description: Pinterest 全自动递归爬虫技能。当用户需要从 Pinterest 批量下载图片、爬取 Pinterest 搜索结果、采集 Pinterest 素材、抓取 Pinterest 图片时使用此技能。触发关键词包括：Pinterest 爬虫、Pinterest 下载、Pinterest 采集、Pinterest 图片抓取、Pinterest 素材、批量下载 Pinterest、pinterest crawler、pinterest scraper、爬 Pinterest 图。即使用户只是说"帮我从 Pinterest 下载一些XX图片"也应触发此技能。同样适用于：查看 Pinterest 爬取历史/统计、筛选高赞图片、批量多关键词采集、采集 SOCKS5 代理等场景。
---

# Pinterest 全自动递归爬虫

一键脚本，自动采集 10 万+ 免费 SOCKS5 代理 → 流式小批验证 → 第一个能通 Pinterest 的代理立刻开爬 → 挂了无缝切下一个。

## 技能结构

```
pinterest-crawler/
├── SKILL.md
└── scripts/
    ├── pinterest_with_proxy.py   ← ⭐ 一键脚本 (采集+流式验证+爬图+自动切换)
    ├── socks5_scraper.py          ← 独立 SOCKS5 代理采集验证工具
    ├── pinterest_crawler.py       ← 基础爬虫 (需自备代理/直连)
    ├── batch_crawl.py             ← 多关键词批量爬取
    ├── stats_report.py            ← 爬取历史统计报告
    └── cleanup.py                 ← 图片筛选/导出/数据库清理
```

## 环境准备

```bash
pip install playwright requests pysocks --break-system-packages
playwright install chromium
```

---

## ⭐ 一键脚本：pinterest_with_proxy.py

### 工作流程

```
18 个免费源并发采集 (2秒, 10万+代理)
        ↓
  随机打乱, 按批次 200 个并发 curl 测 Pinterest
        ↓
  有一个通了 → 立刻启动 Playwright 爬图
        ↓
  爬的过程中代理挂了 → 从下一批未验证的里自动找新代理
        ↓
  爬完 / 全部代理用完 → 输出图片 + list.txt (可用代理列表)
```

### 用法

```bash
# 最简单
python scripts/pinterest_with_proxy.py --keyword "cute cats" --count 50

# 全参数
python scripts/pinterest_with_proxy.py \
  --keyword "cute cats" \
  --count 100 \
  --batch-size 300 \
  --proxy-workers 200 \
  --proxy-timeout 6 \
  --max-depth 2 \
  --headless

# JSON 传参
python scripts/pinterest_with_proxy.py --params '{
  "keyword": "logo design",
  "target_count": 50,
  "batch_size": 300,
  "proxy_workers": 200
}'

# 用上次保存的代理列表, 跳过采集
python scripts/pinterest_with_proxy.py \
  --proxy-file list.txt \
  --keyword "cats" --count 30
```

### 参数说明

| 参数 | 默认 | 说明 |
|---|---|---|
| `keyword` | **(必填)** | 搜索关键词 |
| `target_count` / `--count` | 100 | 目标图片数 |
| `batch_size` | 200 | 每批验证多少个代理 |
| `proxy_workers` | 200 | 代理验证并发线程数 |
| `proxy_timeout` | 6 | 每个代理 curl 测试超时(秒) |
| `proxy_file` | "" | 已有代理列表文件, 跳过采集 |
| `max_depth` | 2 | 递归推荐深度 (0=只爬搜索页) |
| `click_count` | 5 | 每页点击几个详情页 |
| `scroll_times` | 4 | 每页滚动几次 |
| `min_delay` | 0.8 | 下载间最小延迟(秒) |
| `max_delay` | 2.0 | 下载间最大延迟(秒) |
| `headless` | true | 无头模式 |
| `download_dir` | ./pinterest_images | 图片保存根目录 |
| `db_file` | ./pinterest_history.db | 去重数据库 |

### 输出

- 图片: `{download_dir}/{keyword}_{timestamp}/` 目录下
- 代理: `list.txt` 所有验证通过的代理(按延迟排序)
- 统计: stdout 最后一行 `__RESULT__:{JSON}`
- 文件命名: `{pin_id}_{likes}likes_{s|d1|d2}.{jpg|png|gif|webp}`

### 代理源 (18个)

GitHub 仓库: proxifly, TheSpeedX, monosans, hookzof, jetkai, roosterkid, MuRongPIG, prxchk, zloi-user, ErcinDeworken
API/文本源: proxyscrape, sockslist.us, spys.me, openproxylist.xyz, freeproxy.world
raw.githubusercontent.com: proxifly, TheSpeedX, monosans

---

## 独立工具：socks5_scraper.py

单独采集 + 验证 SOCKS5 代理, 不爬图:

```bash
python scripts/socks5_scraper.py --output list.txt
python scripts/socks5_scraper.py --scrape-only --output raw.txt
python scripts/socks5_scraper.py --timeout 5 --workers 200 --country HK
```

---

## 基础爬虫：pinterest_crawler.py

需自备代理或直连, 支持 JSON / CLI 传参:

```bash
python scripts/pinterest_crawler.py --params '{
  "keyword": "cute cats", "target_count": 50,
  "headless": true, "proxy": "socks5://1.2.3.4:1080"
}'

python scripts/pinterest_crawler.py \
  --keyword "cats" --target-count 50 --headless \
  --proxy "socks5://1.2.3.4:1080"
```

---

## 批量爬取：batch_crawl.py

多关键词依次爬取, 共享去重数据库:

```bash
python scripts/batch_crawl.py --params '{
  "keywords": ["cute cats", "landscape", "logo design"],
  "target_count": 50, "headless": true
}'

python scripts/batch_crawl.py \
  --keywords "cats" "dogs" "birds" \
  --target-count 30 --headless
```

---

## 统计报告：stats_report.py

```bash
python scripts/stats_report.py --db ./pinterest_history.db
python scripts/stats_report.py --db ./pinterest_history.db --keyword "cats"
python scripts/stats_report.py --db ./pinterest_history.db --output report.json
```

---

## 图片筛选：cleanup.py

```bash
# 只导出 10 赞以上
python scripts/cleanup.py --source ./pinterest_images --export ./curated --min-likes 10

# 按关键词分文件夹 + 分辨率过滤
python scripts/cleanup.py --source ./pinterest_images --export ./curated \
  --min-size 500 --group-by-keyword

# 清理数据库
python scripts/cleanup.py --db ./pinterest_history.db --cleanup-db
```

---

## Claude 使用此技能的流程

### 1. 复制脚本

```bash
cp -r <SKILL_DIR>/scripts /home/claude/ps
```

`<SKILL_DIR>` 通常为 `/mnt/skills/user/pinterest-crawler`

### 2. 装依赖

```bash
pip install playwright requests pysocks --break-system-packages
playwright install chromium
```

### 3. 一键运行

```bash
cd /home/claude
python ps/pinterest_with_proxy.py --keyword "用户的关键词" --count 50 --headless
```

### 4. 交付

```bash
cp -r /home/claude/pinterest_images /mnt/user-data/outputs/
```

用 `present_files` 呈现给用户。

### 脚本选择速查

| 场景 | 脚本 |
|---|---|
| 一键爬图(推荐) | `pinterest_with_proxy.py` |
| 只采集 SOCKS5 代理 | `socks5_scraper.py` |
| 已有代理, 只爬图 | `pinterest_crawler.py` |
| 多关键词批量 | `batch_crawl.py` |
| 查看统计 | `stats_report.py` |
| 筛选高赞/导出 | `cleanup.py` |

---

## 注意事项

1. **流式验证**: 不会一次性验证所有代理, 每批 200 个并发测, 有通的立刻用, 最大化速度
2. **自动切换**: 爬图过程中代理挂了, 自动从下一批未验证的代理里找新的, 无需人工干预
3. **去重持久化**: SQLite 三重去重 (URL归一化 + MD5 + Pin ID), 跨次运行不重复下载
4. **反爬控制**: `min_delay`/`max_delay` 控制速率, 太快可能触发 Pinterest 封禁
5. **list.txt 复用**: 上次跑完的 `list.txt` 可以通过 `--proxy-file list.txt` 直接用, 跳过采集+验证
6. **Ctrl+C 安全停止**: 随时中断, 已下载的图片和去重记录都会保留

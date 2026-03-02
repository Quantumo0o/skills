# 📈 每日股票投资分析报告

自动化股票信息收集和投资分析系统。

## 快速开始

### 1. 安装

```bash
clawhub install stock-daily-report
```

### 2. 配置自选股

```bash
# 编辑自选股列表
nano ~/.clawdbot/stock_watcher/watchlist.txt
```

格式：`代码 | 名称`
```
002973|侨银股份
600095|湘财股份
000973|佛塑科技
513180|恒生科技 ETF
```

### 3. 设置定时任务

```bash
crontab -e
```

添加：
```bash
# 股票日报（周一到周五 9:25）
25 9 * * 1-5 /root/.openclaw/workspace/skills/stock-daily-report/daily-stock-report.sh
```

### 4. 测试运行

```bash
bash /root/.openclaw/workspace/skills/stock-daily-report/daily-stock-report.sh
```

## 查看报告

报告保存在：`/tmp/stock-report-YYYYMMDD.md`

```bash
# 查看今日报告
cat /tmp/stock-report-$(date +%Y%m%d).md

# 查看历史报告
ls -la /tmp/stock-report-*.md
```

## 功能特点

- ✅ 自动收集股票行情
- ✅ 生成投资建议
- ✅ Markdown 格式报告
- ✅ 定时自动执行
- ✅ 可配置自选股

## 依赖

- Python 3
- requests
- beautifulsoup4

## 许可证

MIT

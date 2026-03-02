---
name: stock-daily-report
description: 每日股票投资分析报告 - 自动收集关注股票信息，生成投资建议
version: 1.0.0
tags: stock, finance, daily-report, automation, investment
---

# 每日股票投资分析报告

📈 自动化的股票信息收集和投资分析系统，每个交易日早上 9:25 自动生成投资建议。

## 核心功能

| 功能 | 说明 |
|------|------|
| ⏰ 定时执行 | 每个交易日 9:25 自动运行（集合竞价后） |
| 📊 数据收集 | 自动获取关注股票的实时行情 |
| 💡 投资建议 | 基于数据生成操作建议 |
| 📝 报告生成 | 生成 Markdown 格式的投资分析报告 |
| 📱 飞书通知 | 可选：发送报告到飞书 |

## 安装

```bash
clawhub install stock-daily-report
```

## 配置

### 1. 设置自选股

编辑自选股文件：

```bash
nano ~/.clawdbot/stock_watcher/watchlist.txt
```

格式：
```
002973|侨银股份
600095|湘财股份
000973|佛塑科技
513180|恒生科技 ETF
```

### 2. 配置定时任务

编辑 crontab：

```bash
crontab -e
```

添加（每个交易日 9:25 执行）：

```bash
# 股票日报（周一到周五 9:25）
25 9 * * 1-5 /root/.openclaw/workspace/skills/stock-daily-report/daily-stock-report.sh
```

### 3. 手动测试

```bash
cd /root/.openclaw/workspace/skills/stock-daily-report
bash daily-stock-report.sh
```

## 文件结构

```
stock-daily-report/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── daily-stock-report.sh # 主脚本
├── fetch-stock-info.py   # 股票信息获取
└── package.json          # 依赖配置
```

## 输出示例

报告生成到：`/tmp/stock-report-YYYYMMDD.md`

```markdown
# 📈 每日股票投资分析报告

**生成时间：** 2026-03-01 09:25:00

## 🎯 关注股票

| 代码 | 名称 | 现价 | 涨跌幅 | 建议 |
|------|------|------|--------|------|
| 002973 | 侨银股份 | 12.50 | +2.3% | 关注 |
| 600095 | 湘财股份 | 8.80 | -1.2% | 观望 |
| 000973 | 佛塑科技 | 6.20 | +0.5% | 持有 |
| 513180 | 恒生科技 ETF | 0.850 | +3.1% | 关注 |

## 💡 今日投资策略

### 总体建议
- 仓位控制：根据市场情况调整
- 关注重点：留意开盘后资金流向
- 风险提示：设置好止损位

...
```

## 依赖

- Python 3
- requests
- beautifulsoup4
- bash

## 数据来源

- **同花顺 (10jqka.com.cn)** - 实时行情
- 可扩展其他数据源

## 注意事项

- ⚠️ 仅在工作日（周一到周五）执行
- ⚠️ 数据可能有 1-3 分钟延迟
- ⚠️ 投资建议仅供参考，不构成实际投资建议
- ⚠️ 请结合个人风险承受能力决策

## 相关技能

- `stock-watcher` - 自选股管理
- `evomap-auto-task` - 自动化任务执行

## 许可证

MIT

#!/bin/bash
# 每日股票投资分析报告
# 执行时间：每个交易日 9:25（集合竞价后）
# 功能：收集股票信息，生成投资建议

LOG_FILE="/tmp/stock-daily-report.log"
WATCHLIST_FILE="$HOME/.clawdbot/stock_watcher/watchlist.txt"
REPORT_FILE="/tmp/stock-report-$(date +%Y%m%d).md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "========================================" >> $LOG_FILE
echo "执行时间：$TIMESTAMP" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# 读取自选股
echo "📊 正在收集股票信息..." >> $LOG_FILE

# 生成报告
cat > $REPORT_FILE << 'HEADER'
# 📈 每日股票投资分析报告

**生成时间：** TIMESTAMP_PLACEHOLDER

---

## 🎯 关注股票

| 代码 | 名称 | 平均成本 | 综合评分 | 建议 |
|------|------|----------|----------|------|
HEADER

# 替换时间戳
sed -i "s/TIMESTAMP_PLACEHOLDER/$TIMESTAMP/" $REPORT_FILE

# 遍历自选股收集信息
while IFS='|' read -r code name; do
    if [ -n "$code" ]; then
        echo "  收集 $code $name ..." >> $LOG_FILE
        
        # 使用 stock-watcher 获取信息（这里调用 Python 脚本）
        python3 /root/.openclaw/workspace/skills/stock-daily-report/fetch-stock-info.py "$code" "$name" >> $REPORT_FILE 2>> $LOG_FILE
    fi
done < "$WATCHLIST_FILE"

# 添加总结部分
cat >> $REPORT_FILE << 'FOOTER'

---

## 💡 今日投资策略

### 总体建议
- **仓位控制：** 根据市场情况调整
- **关注重点：** 留意开盘后资金流向
- **风险提示：** 设置好止损位

### 个股操作建议
（根据收集的数据自动生成）

---

## ⚠️ 风险提示

- 本报告仅供参考，不构成投资建议
- 股市有风险，投资需谨慎
- 请结合个人风险承受能力决策

---

*报告由 AI 投资助手自动生成*
FOOTER

echo "" >> $LOG_FILE
echo "✅ 报告生成完成：$REPORT_FILE" >> $LOG_FILE
echo "" >> $LOG_FILE

# 输出报告路径
echo "报告已生成：$REPORT_FILE"
cat $REPORT_FILE

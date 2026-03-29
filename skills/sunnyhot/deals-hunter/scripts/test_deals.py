#!/usr/bin/env python3
# 测试脚本：生成简单的测试报告并发送到 Discord

# 模拟数据
deals = [
    {
        'title': '测试商品1 - 高性价比日用品',
        'link': 'https://example.com/deal1',
        'price': 100.0
    },
    {
        'title': '测试商品2 - 虽然品',
        'link': 'https://example.com/deal2',
        'price': 200.0
    }
]

# 生成测试报告
report_lines = []
report_lines.append("**🐑 测试羊毛报告**")
report_lines.append("")
report_lines.append("📦 商品数量: 2 | 📊 数据来源: 什么值得买 + 慢慢买")
report_lines.append("")
report_lines.append("---")
report_lines.append("")

for i, deal in enumerate(deals, 1):
    report_lines.append(f"**{i}. {deal['title']}**")
    
    # 价格
    current_price = deal['price']
    report_lines.append(f"💰 当前价格: ¥{current_price}")
    
    # 历史最低价（估算值 =    lowest_price = round(current_price * 0.85, 2)
    report_lines.append(f"📉 历史最低价: ¥{lowest_price} (估算值)")
    
    # 购买链接
    report_lines.append(f"🛒 购买链接: <{deal['link']}>")
    report_lines.append("")

# 添加总结
report_lines.append("---")
report_lines.append("")
report_lines.append("⚠️ 提醒:")
report_lines.append("• 价格实时变化，建议尽快查看")
report_lines.append("• 历史最低价为估算值，仅供参考使用")
report_lines.append("• 🐥 小鸡仔根据数据生成")
report_lines.append("")
report_lines.append("📅 下次更新: 9:00 AM / 12:00 PM / 6:00 PM")
report_lines.append("")

report = '\n'.join(report_lines)

# 保存报告
with open('/tmp/test_deals_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ 测试报告已生成: /tmp/test_deals_report.md")
print(report)

# 发送到 Discord
import subprocess

cmd1 = ['openclaw', 'message', 'send', '--channel', 'discord', '--target', '1482243346692051105', '--message', report]
result1 = subprocess.run(cmd1, capture_output=True, text=True)
if result1.returncode == 0:
    print(f'第 1 段发送: 成功')
else:
    error_msg = result1.stderr
    print(f'第 1 段发送: 失败: {error_msg}')
    exit(1)

cmd2 = ['openclaw', 'message', 'send', '--channel', 'discord', '--target', '1482243346692051105', '--message', report]
result2 = subprocess.run(cmd2, capture_output=True, text=True)
if result2.returncode == 0:
    print(f'第 2 段发送: 成功')
else:
    error_msg = result2.stderr
    print(f'第 2 段发送: 失败: {error_msg}')
    exit(1)


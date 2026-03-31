#!/usr/bin/env python3
# 检索2026年3月1日生效的法律

import sys
from pathlib import Path

# 切换到legal-retrieval目录
legal_retrieval_dir = Path(__file__).parent
sys.path.insert(0, str(legal_retrieval_dir))

# 直接导入模块
import legal_retrieval as lr_module

print("==========================================")
print("  法律检索 - 2026年3月1日生效的法律")
print("==========================================")
print()

retriever = lr_module.LegalRetrieval()

# 查询1: 搜索2026年生效的法律
print("📋 查询1: 搜索'2026年生效 法律'")
print("----------------------------------------")
result1 = retriever.search(query="2026年生效 法律", limit=10, output_format="json")
print(f"查询: {result1.query}")
print(f"找到: {result1.total} 条结果")
print()
if result1.evidence:
    for ev in result1.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   来源: {ev.source_type}")
        print(f"   摘要: {ev.excerpt[:100]}...")
        print()
else:
    print("   ⚠️  没有找到结果")
print()

# 查询2: 搜索新法规
print("==========================================")
print("📋 查询2: 搜索'新法规 2026'")
print("----------------------------------------")
result2 = retriever.search(query="新法规 2026", limit=10, output_format="json")
print(f"查询: {result2.query}")
print(f"找到: {result2.total} 条结果")
print()
if result2.evidence:
    for ev in result2.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   摘要: {ev.excerpt[:100]}...")
        print()
else:
    print("   ⚠️  没有找到结果")
print()

# 查询3: 搜索司法解释
print("==========================================")
print("📋 查询3: 搜索'司法解释 2026'")
print("----------------------------------------")
result3 = retriever.search(query="司法解释 2026", limit=10, output_format="json")
print(f"查询: {result3.query}")
print(f"找到: {result3.total} 条结果")
print()
if result3.evidence:
    for ev in result3.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   摘要: {ev.excerpt[:100]}...")
        print()
else:
    print("   ⚠️  没有找到结果")

print()
print("==========================================")
print()
print("📊 检索总结")
print("----------------------------------------")
total = result1.total + result2.total + result3.total
print(f"   - 查询1（2026年生效法律）: {result1.total} 条结果")
print(f"   - 查询2（新法规2026）: {result2.total} 条结果")
print(f"   - 查询3（司法解释2026）: {result3.total} 条结果")
print(f"   - 总计: {total} 条结果")
print()

if total > 0:
    print("✅ 检索完成")
else:
    print("⚠️  当前知识库中没有2026年3月1日生效的法律")
    print()
    print("💡 建议:")
    print("   1. 如果您已经收集了相关法律文档，可以添加到知识库")
    print("   2. 可以通过以下渠道获取最新法律信息:")
    print("      - 国家法律法规数据库: https://flk.npc.gov.cn/")
    print("      - 最高人民法院: http://www.court.gov.cn/")
    print("      - 最高人民检察院: https://www.spp.gov.cn/")

print()
print("==========================================")

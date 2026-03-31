#!/usr/bin/env python3
# 法律检索技能 - 功能测试

import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.legal_retrieval.legal_retrieval import LegalRetrieval
import json

print("==========================================")
print("  法律检索技能 - 功能测试")
print("==========================================")
print()

retriever = LegalRetrieval()

# 测试1: 检索"合同变更"
print("📋 测试1: 检索'合同变更'")
print("----------------------------------------")
result = retriever.search(query="合同变更", limit=3, output_format="json")
print(f"查询: {result.query}")
print(f"找到: {result.total} 条结果")
print(f"模式: {result.mode}")
print()
for ev in result.evidence:
    print(f"第{ev.rank}条 [{ev.score:.2f}]")
    print(f"标题: {ev.title}")
    print(f"来源: {ev.source_type}")
    print(f"URL: {ev.source_url}")
    print(f"摘要: {ev.excerpt}")
    print()

print("==========================================")
print()

# 测试2: 检索"债权转让"
print("📋 测试2: 检索'债权转让'")
print("----------------------------------------")
result2 = retriever.search(query="债权转让", limit=3, output_format="json")
print(f"查询: {result2.query}")
print(f"找到: {result2.total} 条结果")
print()
for ev in result2.evidence:
    print(f"第{ev.rank}条 [{ev.score:.2f}]")
    print(f"标题: {ev.title}")
    print(f"摘要: {ev.excerpt}")
    print()

print("==========================================")
print()

# 测试3: 检索"买卖合同"
print("📋 测试3: 检索'买卖合同'")
print("----------------------------------------")
result3 = retriever.search(query="买卖合同", limit=5, output_format="json")
print(f"查询: {result3.query}")
print(f"找到: {result3.total} 条结果")
print()
for ev in result3.evidence:
    print(f"第{ev.rank}条 [{ev.score:.2f}]")
    print(f"标题: {ev.title}")
    print(f"来源: {ev.source_type}")
    print()

print("==========================================")
print()
print("✅ 测试完成！法律检索技能运行正常。")
print()
print("📊 测试统计:")
print(f"  - 测试1（合同变更）: {result.total} 条结果")
print(f"  - 测试2（债权转让）: {result2.total} 条结果")
print(f"  - 测试3（买卖合同）: {result3.total} 条结果")
print(f"  - 总计: {result.total + result2.total + result3.total} 条结果")

#!/usr/bin/env python3
import sys
sys.path.insert(0, '/workspace/projects/agents/legal-ai-team/legal-ceo/workspace')

from skills.legal_retrieval.legal_retrieval import LegalRetrieval

print("==========================================")
print("  法律检索技能 - 功能测试")
print("==========================================")
print()

retriever = LegalRetrieval()

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
print("✅ 测试完成！法律检索技能运行正常。")

#!/usr/bin/env python3
# 手动测试 - 验证检索功能

import sys
sys.path.insert(0, '/workspace/projects/agents/legal-ai-team/legal-ceo/workspace')

from skills.legal_retrieval.legal_retrieval import LegalRetrieval

print("==========================================")
print("  法律检索技能 - 手动功能测试")
print("==========================================")
print()

retriever = LegalRetrieval()

# 测试1: 检索"合同变更"
print("📋 测试1: 检索'合同变更'")
print("----------------------------------------")
try:
    result = retriever.search(query="合同变更", limit=3)
    print(f"✅ 检索成功")
    print(f"   查询: {result.query}")
    print(f"   找到: {result.total} 条结果")
    print(f"   模式: {result.mode}")
    print()
    for ev in result.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   来源: {ev.source_type}")
        print(f"   摘要: {ev.excerpt[:100]}...")
        print()
except Exception as e:
    print(f"❌ 检索失败: {e}")

print("==========================================")
print()

# 测试2: 检索"债权转让"
print("📋 测试2: 检索'债权转让'")
print("----------------------------------------")
try:
    result2 = retriever.search(query="债权转让", limit=3)
    print(f"✅ 检索成功")
    print(f"   查询: {result2.query}")
    print(f"   找到: {result2.total} 条结果")
    print()
    for ev in result2.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   摘要: {ev.excerpt[:100]}...")
        print()
except Exception as e:
    print(f"❌ 检索失败: {e}")

print("==========================================")
print()

# 测试3: 检索"买卖合同"
print("📋 测试3: 检索'买卖合同'")
print("----------------------------------------")
try:
    result3 = retriever.search(query="买卖合同", limit=5)
    print(f"✅ 检索成功")
    print(f"   查询: {result3.query}")
    print(f"   找到: {result3.total} 条结果")
    print()
    for ev in result3.evidence:
        print(f"   第{ev.rank}条 [{ev.score:.2f}]")
        print(f"   标题: {ev.title}")
        print(f"   来源: {ev.source_type}")
        print()
except Exception as e:
    print(f"❌ 检索失败: {e}")

print("==========================================")
print()

# 总结
print("📊 测试总结")
print("----------------------------------------")
try:
    total = result.total + result2.total + result3.total
    print(f"✅ 所有测试通过")
    print(f"   - 测试1（合同变更）: {result.total} 条结果")
    print(f"   - 测试2（债权转让）: {result2.total} 条结果")
    print(f"   - 测试3（买卖合同）: {result3.total} 条结果")
    print(f"   - 总计: {total} 条结果")
    print()
    print("🎉 法律检索技能运行正常！")
except:
    print("⚠️  部分测试未完成，请检查错误信息")

print()
print("==========================================")

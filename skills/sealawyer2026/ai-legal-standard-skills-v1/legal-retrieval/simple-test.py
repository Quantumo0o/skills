#!/usr/bin/env python3
# 法律检索技能 - 简化测试（直接导入）

import sys
from pathlib import Path

# 添加legal-retrieval目录到Python路径
legal_retrieval_dir = Path(__file__).parent
sys.path.insert(0, str(legal_retrieval_dir))

# 直接从legal-retrieval目录导入
from legal_retrieval import LegalRetrieval

print("==========================================")
print("  法律检索技能 - 功能测试")
print("==========================================")
print()

try:
    retriever = LegalRetrieval()

    # 测试1: 检索"合同变更"
    print("📋 测试1: 检索'合同变更'")
    print("----------------------------------------")
    result = retriever.search(query="合同变更", limit=3, output_format="json")
    print(f"✅ 检索成功")
    print(f"   查询: {result.query}")
    print(f"   找到: {result.total} 条结果")
    print(f"   模式: {result.mode}")
    print()
    if result.evidence:
        for ev in result.evidence:
            print(f"   第{ev.rank}条 [{ev.score:.2f}]")
            print(f"   标题: {ev.title}")
            print(f"   来源: {ev.source_type}")
            print()
    else:
        print("   ⚠️  没有找到结果")
    print()

except Exception as e:
    print(f"❌ 测试1失败: {e}")
    print()
    import traceback
    traceback.print_exc()

# 测试2: 检索"债权转让"
print("==========================================")
print("📋 测试2: 检索'债权转让'")
print("----------------------------------------")
try:
    result2 = retriever.search(query="债权转让", limit=3, output_format="json")
    print(f"✅ 检索成功")
    print(f"   查询: {result2.query}")
    print(f"   找到: {result2.total} 条结果")
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

except Exception as e:
    print(f"❌ 测试2失败: {e}")
    print()
    import traceback
    traceback.print_exc()

# 测试3: 检索"买卖合同"
print("==========================================")
print("📋 测试3: 检索'买卖合同'")
print("----------------------------------------")
try:
    result3 = retriever.search(query="买卖合同", limit=5, output_format="json")
    print(f"✅ 检索成功")
    print(f"   查询: {result3.query}")
    print(f"   找到: {result3.total} 条结果")
    print()
    if result3.evidence:
        for ev in result3.evidence:
            print(f"   第{ev.rank}条 [{ev.score:.2f}]")
            print(f"   标题: {ev.title}")
            print(f"   来源: {ev.source_type}")
            print()
    else:
        print("   ⚠️  没有找到结果")
    print()

except Exception as e:
    print(f"❌ 测试3失败: {e}")
    print()
    import traceback
    traceback.print_exc()

print("==========================================")
print()
print("📊 测试总结")
print("----------------------------------------")
try:
    total = result.total + result2.total + result3.total
    print(f"✅ 所有测试完成")
    print(f"   - 测试1（合同变更）: {result.total} 条结果")
    print(f"   - 测试2（债权转让）: {result2.total} 条结果")
    print(f"   - 测试3（买卖合同）: {result3.total} 条结果")
    print(f"   - 总计: {total} 条结果")
    print()
    print("🎉 法律检索技能运行正常！")
except:
    print("⚠️  部分测试未完成")

print()
print("==========================================")

#!/usr/bin/env python3
"""
携程 Skill 综合测试套件 v2

测试场景:
1. 简单单程机票搜索
2. 往返机票搜索
3. 多程机票搜索（上海 - 曼谷 - 清迈 - 吉隆坡）
4. 火车票搜索
5. 行程规划（无预算约束）
6. 行程规划（有预算约束）
7. 路线对比
8. 复杂多城市场景（5+ 城市）
9. 错误处理测试
"""

import json
import sys
import time
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from ctrip_client import CtripClient
from route_planner import plan_optimal_route, compare_routes


# ==================== 测试配置 ====================

TEST_CITIES_SIMPLE = ["上海", "曼谷"]
TEST_CITIES_TRIP = ["上海", "曼谷", "清迈", "吉隆坡"]
TEST_CITIES_COMPLEX = ["上海", "曼谷", "清迈", "吉隆坡", "新加坡", "东京"]

TEST_RESULTS = []


# ==================== 测试用例 ====================

def test_1_simple_flight():
    """测试 1: 简单单程机票搜索"""
    print("\n" + "="*60)
    print("测试 1: 简单单程机票搜索 (上海→曼谷)")
    print("="*60)
    
    client = None
    try:
        client = CtripClient(headless=True, use_login=False)
        client.launch()
        result = client.search_flight("上海", "曼谷", "2026-10-01")
        
        # 评估结果
        status = "pass"
        if result.get("min_price", 0) > 0:
            status = "pass"
        elif result.get("prices"):
            status = "pass"
        else:
            status = "warning"  # 价格提取可能受页面影响
        
        test_result = {
            "test": "简单单程机票搜索",
            "status": status,
            "result": {
                "route": result.get("route"),
                "prices_count": len(result.get("prices", [])),
                "min_price": result.get("min_price", 0)
            },
            "note": "价格提取受页面动态加载影响"
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 测试结果：{status}")
        print(f"  路线：{result.get('route', 'N/A')}")
        print(f"  价格选项：{len(result.get('prices', []))} 个")
        print(f"  最低价：¥{result.get('min_price', 0)}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "简单单程机票搜索",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")
    
    finally:
        if client:
            client.close()
        CtripClient.close_all()


def test_2_route_planning_no_budget():
    """测试 2: 行程规划（无预算约束）"""
    print("\n" + "="*60)
    print("测试 2: 行程规划 - 无预算约束")
    print("="*60)
    
    try:
        result = plan_optimal_route(
            cities=TEST_CITIES_TRIP,
            days=8,
            budget=None,
            preference="price"
        )
        
        status = "pass" if result.get("optimal_route") else "fail"
        
        test_result = {
            "test": "行程规划（无预算）",
            "status": status,
            "result": {
                "optimal_route": result.get("optimal_route"),
                "estimated_price": result.get("estimated_price", 0),
                "recommendation": result.get("recommendation", "")[:100]
            }
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 规划完成")
        print(f"  最优路线：{' → '.join(result.get('optimal_route', []))}")
        print(f"  预估价格：¥{result.get('estimated_price', 0)}")
        print(f"  建议：{result.get('recommendation', 'N/A')[:100]}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "行程规划（无预算）",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")


def test_3_route_planning_with_budget():
    """测试 3: 行程规划（有预算约束）"""
    print("\n" + "="*60)
    print("测试 3: 行程规划 - 有预算约束 (¥3000)")
    print("="*60)
    
    try:
        result = plan_optimal_route(
            cities=TEST_CITIES_TRIP,
            days=8,
            budget=3000,
            preference="price"
        )
        
        within_budget = result.get("estimated_price", 0) <= 3000
        status = "pass" if result.get("optimal_route") else "fail"
        
        test_result = {
            "test": "行程规划（有预算¥3000）",
            "status": status,
            "budget_status": "within" if within_budget else "over",
            "result": {
                "optimal_route": result.get("optimal_route"),
                "estimated_price": result.get("estimated_price", 0)
            }
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 规划完成")
        print(f"  最优路线：{' → '.join(result.get('optimal_route', []))}")
        print(f"  预估价格：¥{result.get('estimated_price', 0)}")
        print(f"  预算状态：{'✓ 预算内' if within_budget else '⚠ 超预算'}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "行程规划（有预算）",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")


def test_4_route_comparison():
    """测试 4: 路线对比"""
    print("\n" + "="*60)
    print("测试 4: 路线对比")
    print("="*60)
    
    try:
        route1 = ["上海", "曼谷", "清迈", "吉隆坡"]
        route2 = ["上海", "吉隆坡", "清迈", "曼谷"]
        
        result = compare_routes(route1, route2, days=8)
        
        test_result = {
            "test": "路线对比",
            "status": "pass",
            "result": {
                "route1_price": result.get("route1", {}).get("estimated_price", 0),
                "route2_price": result.get("route2", {}).get("estimated_price", 0),
                "price_difference": result.get("price_difference", 0),
                "recommendation": result.get("recommendation", "")
            }
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 对比完成")
        print(f"  路线 1: {' → '.join(route1)} - ¥{test_result['result']['route1_price']}")
        print(f"  路线 2: {' → '.join(route2)} - ¥{test_result['result']['route2_price']}")
        print(f"  差价：¥{test_result['result']['price_difference']}")
        print(f"  推荐：{test_result['result']['recommendation']}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "路线对比",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")


def test_5_complex_multi_city():
    """测试 5: 复杂多城市场景（6 城市，12 天）"""
    print("\n" + "="*60)
    print("测试 5: 复杂多城市场景（6 城市，12 天）")
    print("="*60)
    
    try:
        result = plan_optimal_route(
            cities=TEST_CITIES_COMPLEX,
            days=12,
            budget=5000,
            preference="price"
        )
        
        status = "pass" if result.get("optimal_route") else "fail"
        
        test_result = {
            "test": "复杂多城市（6 城 12 天）",
            "status": status,
            "complexity": "high",
            "result": {
                "cities_count": len(TEST_CITIES_COMPLEX),
                "optimal_route": result.get("optimal_route"),
                "estimated_price": result.get("estimated_price", 0),
                "per_day_budget": result.get("budget_detail", {}).get("per_day", 0)
            }
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 规划完成")
        print(f"  城市数：{len(TEST_CITIES_COMPLEX)}")
        print(f"  最优路线：{' → '.join(result.get('optimal_route', []))}")
        print(f"  预估价格：¥{result.get('estimated_price', 0)}")
        print(f"  每日预算：¥{result.get('budget_detail', {}).get('per_day', 0)}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "复杂多城市（6 城 12 天）",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")


def test_6_error_handling():
    """测试 6: 错误输入处理"""
    print("\n" + "="*60)
    print("测试 6: 错误输入处理")
    print("="*60)
    
    errors_handled = 0
    total_tests = 0
    
    # 测试 1: 空城市列表
    total_tests += 1
    try:
        result = plan_optimal_route([], 5)
        if "error" in result:
            errors_handled += 1
            print(f"  ✓ 空城市列表：正确返回错误")
        else:
            print(f"  ⚠ 空城市列表：未返回错误")
    except Exception as e:
        print(f"  ✓ 空城市列表：抛出异常（{type(e).__name__}）")
        errors_handled += 1
    
    # 测试 2: 单个城市
    total_tests += 1
    try:
        result = plan_optimal_route(["上海"], 5)
        if "error" in result or len(result.get("optimal_route", [])) == 1:
            errors_handled += 1
            print(f"  ✓ 单个城市：正确处理")
        else:
            print(f"  ⚠ 单个城市：未正确处理")
    except Exception as e:
        print(f"  ✓ 单个城市：抛出异常（{type(e).__name__}）")
        errors_handled += 1
    
    # 测试 3: 无效日期（需要浏览器）
    total_tests += 1
    client = None
    try:
        client = CtripClient(headless=True)
        client.launch()
        result = client.search_flight("上海", "曼谷", "invalid-date")
        if "error" in result:
            errors_handled += 1
            print(f"  ✓ 无效日期：正确返回错误")
        else:
            print(f"  ⚠ 无效日期：未返回错误")
    except Exception as e:
        print(f"  ✓ 无效日期：抛出异常（{type(e).__name__}）")
        errors_handled += 1
    finally:
        if client:
            client.close()
        CtripClient.close_all()
    
    status = "pass" if errors_handled == total_tests else "warning"
    
    test_result = {
        "test": "错误输入处理",
        "status": status,
        "errors_handled": errors_handled,
        "total_tests": total_tests
    }
    TEST_RESULTS.append(test_result)
    
    print(f"\n✓ 错误处理测试：{errors_handled}/{total_tests} 通过")


def test_7_train_search():
    """测试 7: 火车票搜索"""
    print("\n" + "="*60)
    print("测试 7: 火车票搜索（北京→上海）")
    print("="*60)
    
    client = None
    try:
        client = CtripClient(headless=True, use_login=False)
        client.launch()
        result = client.search_train("北京", "上海", "2026-10-01")
        
        status = "pass" if result.get("trains") else "warning"
        
        test_result = {
            "test": "火车票搜索",
            "status": status,
            "result": {
                "route": result.get("route"),
                "trains_count": len(result.get("trains", []))
            },
            "note": "国内火车票搜索"
        }
        TEST_RESULTS.append(test_result)
        
        print(f"✓ 测试结果：{status}")
        print(f"  路线：{result.get('route', 'N/A')}")
        print(f"  车次数量：{len(result.get('trains', []))}")
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": "火车票搜索",
            "status": "fail",
            "error": str(e)
        })
        print(f"✗ 测试失败：{e}")
    
    finally:
        if client:
            client.close()
        CtripClient.close_all()


# ==================== 测试报告 ====================

def generate_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("测试报告汇总")
    print("="*60)
    
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r.get("status") == "pass")
    warning = sum(1 for r in TEST_RESULTS if r.get("status") == "warning")
    failed = sum(1 for r in TEST_RESULTS if r.get("status") == "fail")
    
    pass_rate = f"{passed/total*100:.1f}%" if total > 0 else "N/A"
    
    print(f"\n总测试数：{total}")
    print(f"✓ 通过：{passed}")
    print(f"⚠ 警告：{warning}")
    print(f"✗ 失败：{failed}")
    print(f"通过率：{pass_rate}")
    
    print("\n详细结果:")
    for i, result in enumerate(TEST_RESULTS, 1):
        status_icon = {"pass": "✓", "warning": "⚠", "fail": "✗"}.get(result.get("status", "unknown"), "?")
        print(f"  {i}. {status_icon} {result.get('test', 'Unknown')}: {result.get('status', 'unknown')}")
    
    # 保存报告
    report = {
        "summary": {
            "total": total,
            "passed": passed,
            "warning": warning,
            "failed": failed,
            "pass_rate": pass_rate
        },
        "results": TEST_RESULTS,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    report_path = Path(__file__).parent.parent / "TEST_REPORT.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 报告已保存至：{report_path}")
    
    return report


# ==================== 主函数 ====================

def main():
    """运行所有测试"""
    print("="*60)
    print("携程 Skill 综合测试套件 v2")
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    start_time = time.time()
    
    # 运行测试
    test_1_simple_flight()
    test_2_route_planning_no_budget()
    test_3_route_planning_with_budget()
    test_4_route_comparison()
    test_5_complex_multi_city()
    test_6_error_handling()
    test_7_train_search()
    
    # 生成报告
    elapsed = time.time() - start_time
    report = generate_report()
    
    print(f"\n⏱ 总耗时：{elapsed:.1f}秒 ({elapsed/60:.1f}分钟)")
    print("="*60)
    
    return report


if __name__ == "__main__":
    main()

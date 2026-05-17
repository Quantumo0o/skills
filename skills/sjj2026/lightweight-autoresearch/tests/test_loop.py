#!/usr/bin/env python3
"""
测试脚本 - 验证轻量级自主优化技能基本功能
"""

import os
import sys
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

def test_import():
    """测试导入"""
    print("✅ 测试 1: 导入模块")
    try:
        from run_loop import LightweightAutoresearch
        print("   ✅ 导入成功")
        return True
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")
        return False

def test_init():
    """测试初始化"""
    print("\n✅ 测试 2: 初始化")
    try:
        from run_loop import LightweightAutoresearch
        optimizer = LightweightAutoresearch(
            mode="skill",
            target="/tmp/test_skill",
            iterations=5
        )
        print("   ✅ 初始化成功")
        return True
    except Exception as e:
        print(f"   ❌ 初始化失败: {e}")
        return False

def test_config():
    """测试配置"""
    print("\n✅ 测试 3: 加载配置")
    try:
        import json
        config_file = script_dir / "config.py"
        if config_file.exists():
            # 读取 JSON 配置
            content = config_file.read_text()
            # 提取 JSON 部分（简化）
            print("   ✅ 配置文件存在")
            return True
        else:
            print("   ❌ 配置文件不存在")
            return False
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n✅ 测试 4: 目录结构")
    base_dir = Path(__file__).parent.parent
    
    required = [
        "SKILL.md",
        "scripts/run_loop.py",
        "scripts/config.py",
        "references/karpathy-idea.md"
    ]
    
    all_exist = True
    for item in required:
        path = base_dir / item
        if path.exists():
            print(f"   ✅ {item}")
        else:
            print(f"   ❌ {item} 不存在")
            all_exist = False
    
    return all_exist

def main():
    """运行所有测试"""
    print("🧪 轻量级自主优化技能 - 测试套件\n")
    
    tests = [
        test_import,
        test_init,
        test_config,
        test_directory_structure
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)
    
    # 统计结果
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
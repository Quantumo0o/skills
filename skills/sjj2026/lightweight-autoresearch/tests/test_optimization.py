#!/usr/bin/env python3
"""
测试用例模块 - 具体的测试场景
"""

import os
import json
import unittest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List

# 导入评估和优化模块
from evaluate import SkillEvaluator
from optimize import SkillOptimizer


class TestSkillEvaluator(unittest.TestCase):
    """测试技能评估器"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """清理测试环境"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_evaluate_empty_skill(self):
        """测试空技能包评估"""
        evaluator = SkillEvaluator(self.test_dir)
        results = evaluator.evaluate()
        
        # 空技能包应该得到低分
        self.assertLess(results["total_score"], 30)
        self.assertIn("SKILL.md 不存在", results["details"]["skill_md"]["details"].get("error", ""))
    
    def test_evaluate_complete_skill(self):
        """测试完整技能包评估"""
        # 创建完整的技能包
        skill_md = self.test_dir / "SKILL.md"
        skill_md.write_text('''---
name: test-skill
description: 测试技能包
---

# 测试技能包

## 简介

这是一个测试技能包。

## 使用方法

```bash
python scripts/main.py
```

## 示例

### 示例1

基本使用示例。

## 注意事项

- 注意事项1
- 注意事项2
''', encoding='utf-8')
        
        # 创建目录
        (self.test_dir / "scripts").mkdir()
        (self.test_dir / "scripts" / "main.py").write_text("# 主脚本\n", encoding='utf-8')
        (self.test_dir / "tests").mkdir()
        (self.test_dir / "tests" / "test_basic.py").write_text("# 测试\n", encoding='utf-8')
        (self.test_dir / "references").mkdir()
        (self.test_dir / "references" / "README.md").write_text("# 参考\n", encoding='utf-8')
        
        evaluator = SkillEvaluator(self.test_dir)
        results = evaluator.evaluate()
        
        # 完整技能包应该得到高分
        self.assertGreater(results["total_score"], 70)
        self.assertEqual(len(results["weaknesses"]), 0)
    
    def test_identify_weaknesses(self):
        """测试弱点识别"""
        evaluator = SkillEvaluator(self.test_dir)
        results = evaluator.evaluate()
        
        # 应该识别出弱点
        self.assertGreater(len(results["weaknesses"]), 0)
        self.assertIn("SKILL.md", " ".join(results["weaknesses"]))


class TestSkillOptimizer(unittest.TestCase):
    """测试技能优化器"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """清理测试环境"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_create_missing_directories(self):
        """测试创建缺失目录"""
        optimizer = SkillOptimizer(self.test_dir)
        
        weaknesses = ["缺少 'scripts' 目录", "缺少 'tests' 目录"]
        suggestions = ["创建缺失的目录结构"]
        
        results = optimizer.optimize(weaknesses, suggestions)
        
        # 检查目录是否创建
        self.assertTrue((self.test_dir / "scripts").exists())
        self.assertTrue((self.test_dir / "tests").exists())
        self.assertTrue(results["improvements"][0]["success"])
    
    def test_add_skill_md_sections(self):
        """测试添加 SKILL.md 部分"""
        # 创建基础 SKILL.md
        skill_md = self.test_dir / "SKILL.md"
        skill_md.write_text("# 测试\n", encoding='utf-8')
        
        optimizer = SkillOptimizer(self.test_dir)
        
        weaknesses = ["SKILL.md 缺少 '简介' 部分"]
        suggestions = ["完善 SKILL.md，添加缺失部分"]
        
        results = optimizer.optimize(weaknesses, suggestions)
        
        # 检查部分是否添加
        content = skill_md.read_text(encoding='utf-8')
        self.assertIn("## 简介", content)
    
    def test_rollback(self):
        """测试回滚功能"""
        # 创建原始文件
        skill_md = self.test_dir / "SKILL.md"
        original_content = "# 原始内容\n"
        skill_md.write_text(original_content, encoding='utf-8')
        
        optimizer = SkillOptimizer(self.test_dir)
        
        # 执行优化
        weaknesses = ["SKILL.md 缺少 '简介' 部分"]
        optimizer.optimize(weaknesses, [])
        
        # 回滚
        optimizer.rollback()
        
        # 检查是否恢复
        content = skill_md.read_text(encoding='utf-8')
        self.assertEqual(content, original_content)


class TestOptimizationLoop(unittest.TestCase):
    """测试优化循环"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """清理测试环境"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_full_optimization_cycle(self):
        """测试完整优化循环"""
        # 评估 - 优化 - 再评估
        
        # 1. 初始评估
        evaluator = SkillEvaluator(self.test_dir)
        initial_results = evaluator.evaluate()
        initial_score = initial_results["total_score"]
        
        # 应该是低分
        self.assertLess(initial_score, 50)
        
        # 2. 执行优化
        optimizer = SkillOptimizer(self.test_dir)
        optimize_results = optimizer.optimize(
            initial_results["weaknesses"],
            initial_results["suggestions"]
        )
        
        # 应该有改进
        self.assertGreater(len(optimize_results["improvements"]), 0)
        
        # 3. 再次评估
        evaluator = SkillEvaluator(self.test_dir)
        final_results = evaluator.evaluate()
        final_score = final_results["total_score"]
        
        # 应该有提升
        self.assertGreater(final_score, initial_score)


class TestSpecificSkills(unittest.TestCase):
    """测试具体技能包"""
    
    def test_multi_agent_cn_evaluation(self):
        """测试 multi-agent-cn 技能包评估"""
        skill_path = Path("/root/.openclaw/workspace/skills/multi-agent-cn")
        
        if not skill_path.exists():
            self.skipTest("multi-agent-cn 技能包不存在")
        
        evaluator = SkillEvaluator(skill_path)
        results = evaluator.evaluate()
        
        # 应该是高质量技能包
        self.assertGreater(results["total_score"], 60)
        
        # 打印详细信息
        print(f"\n=== multi-agent-cn 评估结果 ===")
        print(f"总分: {results['total_score']}/100")
        for category, data in results["details"].items():
            print(f"{category}: {data['score']}/{data['max_score']}")
        if results["weaknesses"]:
            print(f"弱点: {', '.join(results['weaknesses'])}")


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSkillEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestSkillOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizationLoop))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecificSkills))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
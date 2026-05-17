#!/usr/bin/env python3
"""
评估模块 - 完整的技能评估（增强版）
整合基础评估、代码质量、安全检查、性能测试
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 导入各维度评估模块
sys.path.insert(0, str(Path(__file__).parent))
from code_analyzer import CodeAnalyzer, analyze_code
from security_checker import SecurityChecker, check_security
from performance_tester import PerformanceTester, test_performance

class ComprehensiveEvaluator:
    """综合评估器"""
    
    def __init__(self, skill_path: str, enable_performance_test: bool = True):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.enable_performance_test = enable_performance_test
        
    def evaluate(self) -> Dict:
        """综合评估技能"""
        results = {
            "total_score": 0,
            "comprehensive_score": 0,
            "details": {},
            "weaknesses": [],
            "suggestions": [],
            "report_file": None
        }
        
        # 1. 基础评估（30分）
        basic_score, basic_details = self._evaluate_basic()
        results["details"]["basic"] = {
            "score": basic_score,
            "max_score": 30,
            "details": basic_details
        }
        
        # 2. 代码质量（25分）
        code_analyzer = CodeAnalyzer(self.skill_path)
        code_results = code_analyzer.analyze()
        code_score = code_results["quality_score"] * 0.25  # 转换为25分制
        results["details"]["code"] = {
            "score": code_score,
            "max_score": 25,
            "details": code_results["details"]
        }
        
        # 3. 安全检查（25分）
        security_checker = SecurityChecker(self.skill_path)
        security_results = security_checker.check()
        security_score = security_results["security_score"] * 0.25  # 转换为25分制
        results["details"]["security"] = {
            "score": security_score,
            "max_score": 25,
            "details": security_results["details"]
        }
        
        # 4. 性能测试（20分）
        if self.enable_performance_test:
            performance_tester = PerformanceTester(self.skill_path)
            performance_results = performance_tester.test()
            performance_score = performance_results["performance_score"] * 0.20  # 转换为20分制
            results["details"]["performance"] = {
                "score": performance_score,
                "max_score": 20,
                "details": performance_results["details"]
            }
        else:
            performance_score = 10  # 默认分数
            performance_results = None
            results["details"]["performance"] = {
                "score": performance_score,
                "max_score": 20,
                "details": {"skipped": True}
            }
        
        # 计算总分
        results["total_score"] = basic_score + code_score + security_score + performance_score
        results["comprehensive_score"] = results["total_score"]
        
        # 识别弱点
        results["weaknesses"] = self._identify_weaknesses(results)
        
        # 生成建议
        results["suggestions"] = self._generate_suggestions(results)
        
        # 存储详细结果（用于生成报告）
        results["_code_results"] = code_results
        results["_security_results"] = security_results
        results["_performance_results"] = performance_results
        
        return results
    
    def _evaluate_basic(self) -> Tuple[int, Dict]:
        """基础评估"""
        score = 0
        details = {}
        
        if not self.skill_md.exists():
            details["error"] = "SKILL.md 不存在"
            return 0, details
        
        content = self.skill_md.read_text(encoding='utf-8')
        
        # 检查必要部分（每项3分，共30分）
        required_sections = {
            "name": r"^name:\s*.+$",
            "description": r"^description:\s*.+$",
            "简介": r"^##\s*简介",
            "使用方法": r"^##\s*使用方法",
            "示例": r"^##\s*示例|^###\s*示例",
            "注意事项": r"^##\s*注意事项"
        }
        
        for section, pattern in required_sections.items():
            if pattern and re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                score += 3
                details[section] = "✅ 存在"
            else:
                details[section] = "❌ 缺失"
        
        # 检查目录结构（每项2分，共12分）
        for dir_name in ["scripts", "tests", "references"]:
            dir_path = self.skill_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                files = list(dir_path.glob("*"))
                if files:
                    score += 2
                    details[dir_name] = f"✅ 存在且非空"
                else:
                    details[dir_name] = "⚠️ 存在但为空"
            else:
                details[dir_name] = "❌ 不存在"
        
        return min(score, 30), details
    
    def _identify_weaknesses(self, results: Dict) -> List[str]:
        """识别技能弱点"""
        weaknesses = []
        
        # 基础弱点
        if results["details"]["basic"]["score"] < 30:
            for section, status in results["details"]["basic"]["details"].items():
                if "❌" in str(status):
                    weaknesses.append(f"基础评估：缺少 '{section}'")
        
        # 代码质量弱点
        if results["details"]["code"]["score"] < 20:
            weaknesses.append("代码质量：需要改进")
        
        # 安全弱点
        if results["details"]["security"]["score"] < 20:
            weaknesses.append("安全检查：存在风险")
        
        # 性能弱点
        if results["details"]["performance"]["score"] < 15:
            weaknesses.append("性能测试：性能待优化")
        
        return weaknesses
    
    def _generate_suggestions(self, results: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        weaknesses = results["weaknesses"]
        
        for weakness in weaknesses:
            if "基础评估" in weakness:
                suggestions.append("完善 SKILL.md，添加缺失部分")
            elif "代码质量" in weakness:
                suggestions.append("改进代码质量，添加文档和类型提示")
            elif "安全检查" in weakness:
                suggestions.append("修复安全问题，移除敏感信息")
            elif "性能测试" in weakness:
                suggestions.append("优化性能，减少导入时间和内存占用")
        
        # 通用建议
        if results["total_score"] < 70:
            suggestions.append("建议参考 ClawHub 优秀技能包进行全面改进")
        
        return list(set(suggestions))


def evaluate_skill_comprehensive(skill_path: str, enable_performance_test: bool = True) -> Dict:
    """综合评估技能包的便捷函数"""
    evaluator = ComprehensiveEvaluator(skill_path, enable_performance_test)
    return evaluator.evaluate()


# 保留原有函数兼容性
from pathlib import Path
import re

class SkillEvaluator:
    """技能评估器（简化版，保持兼容）"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        
    def evaluate(self) -> Dict:
        """评估技能包"""
        # 使用综合评估器，但只返回基础评估
        evaluator = ComprehensiveEvaluator(str(self.skill_path), enable_performance_test=False)
        results = evaluator.evaluate()
        
        # 转换为旧格式
        return {
            "total_score": results["total_score"],
            "details": results["details"],
            "weaknesses": results["weaknesses"],
            "suggestions": results["suggestions"]
        }


def evaluate_skill(skill_path: str) -> Dict:
    """评估技能包的便捷函数"""
    evaluator = SkillEvaluator(skill_path)
    return evaluator.evaluate()

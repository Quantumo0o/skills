#!/usr/bin/env python3
"""
评估模块 V2 - 达尔文8维度评估体系

借鉴达尔文.skill的评估体系：
- 结构维度（60分）：维度1-7
- 效果维度（40分）：维度8（实测表现）
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging

# 导入V2新模块
sys.path.insert(0, str(Path(__file__).parent))
from independent_scorer import IndependentScorer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DarwinEvaluatorV2:
    """达尔文8维度评估器 V2"""
    
    def __init__(
        self,
        skill_path: str,
        test_prompts: Optional[List[Dict]] = None,
        eval_mode: str = "dry_run"
    ):
        """
        初始化评估器
        
        Args:
            skill_path: 技能目录路径
            test_prompts: 测试prompt列表（可选）
            eval_mode: 评估模式（full_test/dry_run）
        """
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.test_prompts = test_prompts or []
        self.eval_mode = eval_mode
        
        # 读取SKILL.md内容
        self.skill_content = self._read_skill_md()
    
    def evaluate(self) -> Dict:
        """
        达尔文8维度评估
        
        Returns:
            {
                "total_score": 76.6,
                "dimensions": {
                    "1_frontmatter": {...},
                    "2_workflow_clarity": {...},
                    ...
                    "8_actual_performance": {...}
                },
                "weaknesses": [...],
                "suggestions": [...]
            }
        """
        logger.info(f"开始达尔文8维度评估，模式: {self.eval_mode}")
        
        results = {
            "total_score": 0,
            "dimensions": {},
            "weaknesses": [],
            "suggestions": [],
            "eval_mode": self.eval_mode
        }
        
        # === 结构维度（60分）===
        
        # 维度1: Frontmatter质量（8分）
        results["dimensions"]["1_frontmatter"] = self._evaluate_frontmatter()
        
        # 维度2: 工作流清晰度（15分）
        results["dimensions"]["2_workflow_clarity"] = self._evaluate_workflow()
        
        # 维度3: 边界条件覆盖（10分）
        results["dimensions"]["3_boundary_conditions"] = self._evaluate_boundaries()
        
        # 维度4: 检查点设计（7分）
        results["dimensions"]["4_checkpoints"] = self._evaluate_checkpoints()
        
        # 维度5: 指令具体性（15分）
        results["dimensions"]["5_instruction_specificity"] = self._evaluate_instructions()
        
        # 维度6: 资源整合度（5分）
        results["dimensions"]["6_resource_integration"] = self._evaluate_resources()
        
        # 维度7: 整体架构（15分）
        results["dimensions"]["7_architecture"] = self._evaluate_architecture()
        
        # === 效果维度（40分）===
        
        # 维度8: 实测表现（25分）⭐ 最高权重
        results["dimensions"]["8_actual_performance"] = self._evaluate_performance()
        
        # 计算总分
        total = sum(d["score"] for d in results["dimensions"].values())
        results["total_score"] = total
        
        # 识别弱点
        results["weaknesses"] = self._identify_weaknesses(results)
        
        # 生成建议
        results["suggestions"] = self._generate_suggestions(results)
        
        return results
    
    def _read_skill_md(self) -> str:
        """读取SKILL.md内容"""
        if not self.skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found: {self.skill_md}")
        
        with open(self.skill_md, 'r', encoding='utf-8') as f:
            return f.read()
    
    # === 结构维度评估（维度1-7）===
    
    def _evaluate_frontmatter(self) -> Dict:
        """
        维度1：Frontmatter质量（权重8）
        
        评分标准：
        - name规范（1-3分）
        - description包含做什么+何时用+触发词（1-4分）
        - ≤1024字符（1-3分）
        """
        score = 0
        max_score = 8
        details = {}
        
        # 检查是否有frontmatter
        has_frontmatter = self.skill_content.startswith('---')
        details["has_frontmatter"] = has_frontmatter
        
        if not has_frontmatter:
            score = 2
            details["issue"] = "缺少标准frontmatter"
        else:
            # 解析frontmatter
            parts = self.skill_content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                
                # 检查name
                name_score = 0
                for line in frontmatter.split('\n'):
                    if line.startswith('name:'):
                        name = line.split(':', 1)[1].strip()
                        # 检查是否规范（英文短横线命名）
                        if name and name.replace('-', '').replace('_', '').isalnum():
                            name_score = 3
                            details["name"] = name
                        break
                
                # 检查description
                desc_score = 0
                for line in frontmatter.split('\n'):
                    if line.startswith('description:'):
                        desc = line.split(':', 1)[1].strip()
                        # 检查是否包含触发词
                        if len(desc) > 50 and ('Use when' in desc or '触发' in desc or '使用' in desc):
                            desc_score = 4
                        elif len(desc) > 30:
                            desc_score = 2
                        details["description_length"] = len(desc)
                        break
                
                # 检查字符数
                char_score = 3 if len(frontmatter) <= 1024 else 1
                details["frontmatter_length"] = len(frontmatter)
                
                score = min(name_score + desc_score + char_score, 10)
        
        return {
            "score": min(score * 0.8, max_score),  # 换算为8分制
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_workflow(self) -> Dict:
        """
        维度2：工作流清晰度（权重15）
        
        评分标准：
        - 步骤明确可执行（1-5分）
        - 有序号（1-3分）
        - 每步有明确输入/输出（1-7分）
        """
        score = 0
        max_score = 15
        details = {}
        
        content_lower = self.skill_content.lower()
        
        # 检查步骤明确性
        has_steps = any(marker in content_lower for marker in ['step', '步骤', 'phase', '阶段'])
        details["has_steps"] = has_steps
        
        if has_steps:
            score += 5
        
        # 检查序号
        has_numbers = any(marker in self.skill_content for marker in ['1.', '1)', 'Step 1', '步骤1'])
        details["has_numbers"] = has_numbers
        
        if has_numbers:
            score += 3
        
        # 检查输入输出
        has_io = any(marker in content_lower for marker in ['输入', '输出', 'input', 'output', '返回', 'returns'])
        details["has_io_spec"] = has_io
        
        if has_io:
            score += 4
        
        # 检查流程图
        has_flowchart = any(marker in content_lower for marker in ['loop', '循环', '流程', 'flow'])
        details["has_flowchart"] = has_flowchart
        
        if has_flowchart:
            score += 3
        
        return {
            "score": min(score * 1.5, max_score),  # 换算为15分制
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_boundaries(self) -> Dict:
        """
        维度3：边界条件覆盖（权重10）
        
        评分标准：
        - 处理异常情况（1-4分）
        - 有fallback路径（1-3分）
        - 错误恢复（1-3分）
        """
        score = 0
        max_score = 10
        details = {}
        
        content_lower = self.skill_content.lower()
        
        # 检查异常处理
        has_exceptions = any(marker in content_lower for marker in ['错误', '异常', 'error', 'exception', '失败'])
        details["has_exceptions"] = has_exceptions
        
        if has_exceptions:
            score += 4
        
        # 检查fallback
        has_fallback = any(marker in content_lower for marker in ['fallback', '备用', '替代', '默认'])
        details["has_fallback"] = has_fallback
        
        if has_fallback:
            score += 3
        
        # 检查错误恢复
        has_recovery = any(marker in content_lower for marker in ['恢复', '重试', 'retry', 'recover', '回滚'])
        details["has_recovery"] = has_recovery
        
        if has_recovery:
            score += 3
        
        return {
            "score": min(score, max_score),
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_checkpoints(self) -> Dict:
        """
        维度4：检查点设计（权重7）- 改进版
        
        评分标准：
        - 关键决策前有用户确认（1-3分）
        - 有多个检查点（1-2分）
        - 检查点有具体实现代码（1-2分）
        """
        score = 0
        max_score = 7
        details = {}
        
        content_lower = self.skill_content.lower()
        
        # 检查用户确认机制
        has_confirmation = any(marker in content_lower for marker in ['确认', 'confirm', '用户', '人工', 'human'])
        details["has_confirmation"] = has_confirmation
        
        if has_confirmation:
            score += 3
        
        # 检查是否有多个检查点
        checkpoint_count = content_lower.count('检查点') + content_lower.count('checkpoint')
        details["checkpoint_count"] = checkpoint_count
        
        if checkpoint_count >= 4:
            score += 2  # 有4个以上检查点
        elif checkpoint_count >= 2:
            score += 1  # 有2-3个检查点
        
        # 检查是否有检查点实现代码
        has_checkpoint_code = 'def checkpoint' in content_lower or '检查点' in content_lower and 'def ' in content_lower
        details["has_checkpoint_code"] = has_checkpoint_code
        
        if has_checkpoint_code:
            score += 2
        
        return {
            "score": min(score, max_score),
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_instructions(self) -> Dict:
        """
        维度5：指令具体性（权重15）
        
        评分标准：
        - 不模糊（1-5分）
        - 有具体参数/格式/示例（1-7分）
        - 可直接执行（1-3分）
        """
        score = 0
        max_score = 15
        details = {}
        
        # 检查具体性
        has_params = any(marker in self.skill_content for marker in ['--', '参数', 'parameter', '参数说明'])
        details["has_params"] = has_params
        
        if has_params:
            score += 5
        
        # 检查示例
        has_examples = any(marker in self.skill_content.lower() for marker in ['示例', 'example', '用法', 'usage', '```'])
        details["has_examples"] = has_examples
        
        if has_examples:
            score += 7
        
        # 检查可执行性
        has_commands = any(marker in self.skill_content for marker in ['python3', 'bash', 'cd ', 'npm', 'git'])
        details["has_commands"] = has_commands
        
        if has_commands:
            score += 3
        
        return {
            "score": min(score * 1.5, max_score),
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_resources(self) -> Dict:
        """
        维度6：资源整合度（权重5）
        
        评分标准：
        - references/scripts/assets引用正确（1-5分）
        - 路径可达（1-5分）
        """
        score = 0
        max_score = 5
        details = {}
        
        # 检查资源引用
        has_references = (self.skill_path / "references").exists()
        has_scripts = (self.skill_path / "scripts").exists()
        
        details["has_references"] = has_references
        details["has_scripts"] = has_scripts
        
        if has_references:
            score += 3
        if has_scripts:
            score += 2
        
        return {
            "score": min(score, max_score),
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    def _evaluate_architecture(self) -> Dict:
        """
        维度7：整体架构（权重15）
        
        评分标准：
        - 结构层次清晰（1-5分）
        - 不冗余不遗漏（1-5分）
        - 与达尔文生态一致（1-5分）
        """
        score = 0
        max_score = 15
        details = {}
        
        content_lower = self.skill_content.lower()
        
        # 检查结构层次
        has_sections = self.skill_content.count('##') >= 3
        details["has_sections"] = has_sections
        
        if has_sections:
            score += 5
        
        # 检查完整性
        has_intro = any(marker in content_lower for marker in ['简介', '介绍', 'intro', 'overview'])
        has_usage = any(marker in content_lower for marker in ['使用', '用法', 'usage', '方法'])
        has_constraints = any(marker in content_lower for marker in ['约束', '注意', 'constraint', '注意事项'])
        
        details["has_intro"] = has_intro
        details["has_usage"] = has_usage
        details["has_constraints"] = has_constraints
        
        if has_intro and has_usage:
            score += 5
        
        # 检查达尔文兼容性
        has_darwin = any(marker in content_lower for marker in ['维度', 'dimension', '8维度', '评估'])
        details["darwin_compatible"] = has_darwin
        
        if has_darwin:
            score += 5
        
        return {
            "score": min(score * 1.5, max_score),
            "max_score": max_score,
            "raw_score": score,
            "details": details
        }
    
    # === 效果维度评估（维度8）===
    
    def _evaluate_performance(self) -> Dict:
        """
        维度8：实测表现（权重25）⭐ 最高权重
        
        关键：使用独立评分器
        """
        max_score = 25
        
        if not self.test_prompts:
            logger.warning("没有测试prompt，使用默认分数")
            return {
                "score": 15,  # 默认分数
                "max_score": max_score,
                "raw_score": 6,
                "details": {"warning": "没有测试prompt"},
                "eval_mode": "dry_run"
            }
        
        # 使用独立评分器
        scorer = IndependentScorer(
            str(self.skill_path),
            self.test_prompts,
            self.eval_mode
        )
        
        result = scorer.evaluate_with_baseline()
        
        return {
            "score": result["dimension_8_score"] * 2.5,  # 换算为25分制
            "max_score": max_score,
            "raw_score": result["dimension_8_score"],
            "details": {
                "with_skill_score": result["with_skill"]["score"],
                "baseline_score": result["baseline"]["score"],
                "improvement": result["improvement"],
                "eval_mode": result["eval_mode"]
            }
        }
    
    # === 辅助方法 ===
    
    def _identify_weaknesses(self, results: Dict) -> List[Dict]:
        """识别弱点"""
        weaknesses = []
        
        for dim_name, dim_data in results["dimensions"].items():
            # 计算得分率
            score_rate = dim_data["score"] / dim_data["max_score"] if dim_data["max_score"] > 0 else 0
            
            # 低于70%认为有弱点
            if score_rate < 0.7:
                weaknesses.append({
                    "dimension": dim_name,
                    "score": dim_data["score"],
                    "max_score": dim_data["max_score"],
                    "score_rate": score_rate,
                    "priority": "P0" if score_rate < 0.5 else ("P1" if score_rate < 0.6 else "P2")
                })
        
        # 按得分率排序（最低的在前）
        weaknesses.sort(key=lambda x: x["score_rate"])
        
        return weaknesses
    
    def _generate_suggestions(self, results: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        weaknesses = results.get("weaknesses", [])
        
        for weakness in weaknesses[:3]:  # 最多3条建议
            dim = weakness["dimension"]
            priority = weakness["priority"]
            
            if "frontmatter" in dim:
                suggestions.append(f"[{priority}] 添加标准frontmatter（name、description、触发词）")
            elif "workflow" in dim:
                suggestions.append(f"[{priority}] 明确工作流步骤，补充输入输出规格")
            elif "boundary" in dim:
                suggestions.append(f"[{priority}] 添加错误恢复机制和fallback路径")
            elif "actual_performance" in dim:
                suggestions.append(f"[{priority}] 补充具体实现细节，添加代码示例")
        
        return suggestions


def evaluate_skill_v2(
    skill_path: str,
    test_prompts: Optional[List[Dict]] = None,
    eval_mode: str = "dry_run"
) -> Dict:
    """
    评估技能（V2版本）
    
    Args:
        skill_path: 技能路径
        test_prompts: 测试prompt列表
        eval_mode: 评估模式
        
    Returns:
        评估结果
    """
    evaluator = DarwinEvaluatorV2(skill_path, test_prompts, eval_mode)
    return evaluator.evaluate()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 evaluate_v2.py <skill_path> [eval_mode]")
        print("  eval_mode: full_test / dry_run (默认)")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    eval_mode = sys.argv[2] if len(sys.argv) > 2 else "dry_run"
    
    # 加载测试prompt
    test_prompts_file = Path(skill_path) / "test-prompts.json"
    test_prompts = None
    
    if test_prompts_file.exists():
        with open(test_prompts_file, 'r', encoding='utf-8') as f:
            test_prompts = json.load(f)
    
    # 执行评估
    result = evaluate_skill_v2(skill_path, test_prompts, eval_mode)
    
    print("\n=== 达尔文8维度评估结果 ===")
    print(f"总分: {result['total_score']:.1f}/100")
    print(f"评估模式: {result['eval_mode']}")
    
    print("\n维度得分：")
    for dim_name, dim_data in result["dimensions"].items():
        print(f"  {dim_name}: {dim_data['score']:.1f}/{dim_data['max_score']}")
    
    if result["weaknesses"]:
        print("\n弱点：")
        for w in result["weaknesses"]:
            print(f"  [{w['priority']}] {w['dimension']}: {w['score_rate']:.1%}")
    
    if result["suggestions"]:
        print("\n建议：")
        for s in result["suggestions"]:
            print(f"  {s}")

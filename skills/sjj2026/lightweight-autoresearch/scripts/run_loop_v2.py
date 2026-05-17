#!/usr/bin/env python3
"""
主循环脚本 V2 - 整合达尔文优化流程

完整流程：
- Phase 0: 初始化
- Phase 0.5: 测试Prompt设计（V2新增）
- Phase 1: 基线评估（8维度）
- Phase 2: 优化循环（独立评分+人在回路）
- Phase 3: 汇总报告
"""

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

# 导入V2模块
import sys
sys.path.insert(0, str(Path(__file__).parent))
from test_prompt_designer import TestPromptDesigner, design_and_save
from independent_scorer import IndependentScorer
from human_in_loop import HumanInLoopController, create_modifications_dict
from evaluate_v2 import DarwinEvaluatorV2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DarwinOptimizerV2:
    """达尔文优化器 V2"""
    
    def __init__(
        self,
        skill_path: str,
        max_rounds: int = 3,
        auto_mode: bool = False,
        eval_mode: str = "dry_run"
    ):
        """
        初始化优化器
        
        Args:
            skill_path: 技能目录路径
            max_rounds: 最大优化轮数
            auto_mode: 自动模式（跳过人在回路）
            eval_mode: 评估模式（full_test/dry_run）
        """
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.max_rounds = max_rounds
        self.auto_mode = auto_mode
        self.eval_mode = eval_mode
        
        # 初始化控制器
        self.human_controller = HumanInLoopController(auto_mode=auto_mode)
        
        # 初始化结果记录
        self.results_file = self.skill_path / "results.tsv"
        self.test_prompts_file = self.skill_path / "test-prompts.json"
        
        # Git分支
        self.branch_name = f"auto-optimize/{datetime.now().strftime('%Y%m%d-%H%M')}"
        
    def run_optimization(self) -> Dict:
        """
        运行完整优化流程
        
        Returns:
            优化结果
        """
        logger.info(f"开始达尔文V2优化: {self.skill_name}")
        
        # Phase 0: 初始化
        self._phase_0_init()
        
        # Phase 0.5: 测试Prompt设计（V2新增）
        test_prompts = self._phase_0_5_design_test_prompts()
        
        # Phase 1: 基线评估
        baseline_result = self._phase_1_baseline_evaluation(test_prompts)
        
        # 展示基线评分卡
        self._display_scorecard(baseline_result, "基线评估")
        
        # 人在回路检查点
        if not self.auto_mode:
            decision = self.human_controller.pause_for_review(
                self.skill_name,
                {
                    "score_change": {"before": 0, "after": baseline_result["total_score"]},
                    "suggestions": ["继续优化", "停止优化"]
                }
            )
            
            if decision == "revert":
                logger.info("用户选择停止优化")
                return baseline_result
        
        # Phase 2: 优化循环
        optimization_history = self._phase_2_optimization_loop(
            baseline_result,
            test_prompts
        )
        
        # Phase 3: 汇总报告
        final_report = self._phase_3_summary_report(
            baseline_result,
            optimization_history
        )
        
        return final_report
    
    # === Phase 0: 初始化 ===
    
    def _phase_0_init(self):
        """Phase 0: 初始化环境"""
        logger.info("Phase 0: 初始化环境")
        
        # 初始化Git
        if not (self.skill_path / ".git").exists():
            subprocess.run(['git', 'init'], cwd=self.skill_path, capture_output=True)
            logger.info("Git初始化完成")
        
        # 创建优化分支
        subprocess.run(
            ['git', 'checkout', '-b', self.branch_name],
            cwd=self.skill_path,
            capture_output=True
        )
        logger.info(f"创建优化分支: {self.branch_name}")
        
        # 初始化results.tsv
        if not self.results_file.exists():
            with open(self.results_file, 'w') as f:
                f.write("timestamp\tcommit\tskill\told_score\tnew_score\tstatus\tdimension\tnote\teval_mode\n")
            logger.info("results.tsv初始化完成")
    
    # === Phase 0.5: 测试Prompt设计 ===
    
    def _phase_0_5_design_test_prompts(self) -> List[Dict]:
        """Phase 0.5: 测试Prompt设计（V2新增）"""
        logger.info("Phase 0.5: 设计测试Prompt")
        
        # 检查是否已有测试prompt
        if self.test_prompts_file.exists():
            with open(self.test_prompts_file, 'r') as f:
                test_prompts = json.load(f)
            logger.info(f"使用已有测试prompt: {len(test_prompts)}个")
            return test_prompts
        
        # 设计新的测试prompt
        designer = TestPromptDesigner(str(self.skill_path))
        test_prompts = designer.design_test_prompts()
        designer.save_test_prompts(test_prompts)
        
        # 展示给用户确认
        print("\n=== 设计的测试Prompt ===")
        for tp in test_prompts:
            print(f"\n场景{tp['id']}: {tp['scenario']}")
            print(f"  Prompt: {tp['prompt']}")
            print(f"  期望: {tp['expected']}")
        
        # 人在回路确认
        if not self.auto_mode:
            input("\n按Enter确认测试Prompt，或Ctrl+C取消...")
        
        return test_prompts
    
    # === Phase 1: 基线评估 ===
    
    def _phase_1_baseline_evaluation(self, test_prompts: List[Dict]) -> Dict:
        """Phase 1: 基线评估（8维度）"""
        logger.info("Phase 1: 基线评估")
        
        evaluator = DarwinEvaluatorV2(
            str(self.skill_path),
            test_prompts,
            self.eval_mode
        )
        
        result = evaluator.evaluate()
        
        # 记录基线
        self._record_result(
            old_score=0,
            new_score=result["total_score"],
            status="baseline",
            dimension="-",
            note="初始8维度评估",
            commit="baseline"
        )
        
        return result
    
    # === Phase 2: 优化循环 ===
    
    def _phase_2_optimization_loop(
        self,
        baseline_result: Dict,
        test_prompts: List[Dict]
    ) -> List[Dict]:
        """Phase 2: 优化循环"""
        logger.info("Phase 2: 优化循环开始")
        
        optimization_history = []
        current_score = baseline_result["total_score"]
        
        for round_num in range(1, self.max_rounds + 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Round {round_num}/{self.max_rounds}")
            logger.info(f"{'='*60}")
            
            # Step 1: 诊断 - 找最低维度
            lowest_dim = self._find_lowest_dimension(baseline_result if round_num == 1 else round_result)
            logger.info(f"最低维度: {lowest_dim['dimension']} ({lowest_dim['score']:.1f}/{lowest_dim['max_score']})")
            
            # Step 2: 提出改进方案
            improvement = self._propose_improvement(lowest_dim)
            logger.info(f"改进方案: {improvement['description']}")
            
            # Step 3: 执行改进
            commit_hash = self._execute_improvement(improvement)
            
            # Step 4: 独立评分（V2关键！）
            round_result = self._independent_evaluate(test_prompts)
            
            # Step 5: 决策
            new_score = round_result["total_score"]
            improvement_delta = new_score - current_score
            
            if new_score > current_score:
                status = "keep"
                logger.info(f"✅ 改进成功: {current_score:.1f} → {new_score:.1f} (+{improvement_delta:.1f})")
                current_score = new_score
                
                # 记录结果
                self._record_result(
                    old_score=current_score - improvement_delta,
                    new_score=new_score,
                    status=status,
                    dimension=lowest_dim['dimension'],
                    note=improvement['description'],
                    commit=commit_hash
                )
            else:
                status = "revert"
                logger.info(f"❌ 改进失败: {current_score:.1f} → {new_score:.1f} ({improvement_delta:.1f})")
                
                # Git回滚
                subprocess.run(
                    ['git', 'revert', 'HEAD', '--no-edit'],
                    cwd=self.skill_path,
                    capture_output=True
                )
                logger.info("已回滚到上一版本")
                
                # 记录失败
                self._record_result(
                    old_score=current_score,
                    new_score=new_score,
                    status=status,
                    dimension=lowest_dim['dimension'],
                    note=improvement['description'],
                    commit=commit_hash
                )
                
                # 失败则跳出循环
                break
            
            # 记录本轮结果
            optimization_history.append({
                "round": round_num,
                "dimension": lowest_dim['dimension'],
                "old_score": current_score - improvement_delta,
                "new_score": new_score,
                "status": status,
                "commit": commit_hash
            })
            
            # Step 6: 人在回路检查点（V2关键！）
            if not self.auto_mode:
                modifications = create_modifications_dict(
                    str(self.skill_path),
                    current_score - improvement_delta,
                    new_score,
                    dimension_changes=[lowest_dim],
                    commit_hash=commit_hash
                )
                
                decision = self.human_controller.pause_for_review(
                    self.skill_name,
                    modifications
                )
                
                if decision == "revert":
                    # 用户选择回滚
                    subprocess.run(
                        ['git', 'revert', 'HEAD', '--no-edit'],
                        cwd=self.skill_path,
                        capture_output=True
                    )
                    logger.info("用户选择回滚")
                    break
                elif decision == "continue":
                    # 用户选择继续优化下一个维度
                    logger.info("用户选择继续优化")
                    continue
        
        return optimization_history
    
    # === Phase 3: 汇总报告 ===
    
    def _phase_3_summary_report(
        self,
        baseline_result: Dict,
        optimization_history: List[Dict]
    ) -> Dict:
        """Phase 3: 汇总报告"""
        logger.info("Phase 3: 生成汇总报告")
        
        # 计算最终分数
        if optimization_history:
            final_score = optimization_history[-1]["new_score"]
        else:
            final_score = baseline_result["total_score"]
        
        # 统计
        total_rounds = len(optimization_history)
        keep_rounds = sum(1 for h in optimization_history if h["status"] == "keep")
        revert_rounds = sum(1 for h in optimization_history if h["status"] == "revert")
        
        report = {
            "skill_name": self.skill_name,
            "baseline_score": baseline_result["total_score"],
            "final_score": final_score,
            "improvement": final_score - baseline_result["total_score"],
            "total_rounds": total_rounds,
            "keep_rounds": keep_rounds,
            "revert_rounds": revert_rounds,
            "eval_mode": self.eval_mode,
            "optimization_history": optimization_history
        }
        
        # 展示报告
        self._display_final_report(report)
        
        return report
    
    # === 辅助方法 ===
    
    def _find_lowest_dimension(self, result: Dict) -> Dict:
        """找到得分最低的维度"""
        weaknesses = result.get("weaknesses", [])
        
        if weaknesses:
            lowest = weaknesses[0]  # 已按得分率排序
            return {
                "dimension": lowest["dimension"],
                "score": lowest["score"],
                "max_score": lowest["max_score"],
                "score_rate": lowest["score_rate"]
            }
        else:
            # 没有明显弱点，返回第一个维度
            dims = result.get("dimensions", {})
            first_dim = list(dims.values())[0]
            return {
                "dimension": list(dims.keys())[0],
                "score": first_dim["score"],
                "max_score": first_dim["max_score"],
                "score_rate": first_dim["score"] / first_dim["max_score"]
            }
    
    def _propose_improvement(self, lowest_dim: Dict) -> Dict:
        """提出改进方案"""
        dim_name = lowest_dim["dimension"]
        
        improvements = {
            "1_frontmatter": {
                "description": "添加标准frontmatter（name、description、触发词）",
                "action": "add_frontmatter"
            },
            "2_workflow_clarity": {
                "description": "明确工作流步骤，补充输入输出规格",
                "action": "clarify_workflow"
            },
            "3_boundary_conditions": {
                "description": "添加错误恢复机制和fallback路径",
                "action": "add_error_handling"
            },
            "4_checkpoints": {
                "description": "添加用户确认检查点",
                "action": "add_checkpoints"
            },
            "5_instruction_specificity": {
                "description": "补充具体参数和示例",
                "action": "add_examples"
            },
            "6_resource_integration": {
                "description": "补充references或scripts目录",
                "action": "add_resources"
            },
            "7_architecture": {
                "description": "优化整体结构，补充达尔文8维度体系",
                "action": "improve_architecture"
            },
            "8_actual_performance": {
                "description": "补充具体实现流程和代码示例",
                "action": "add_implementation"
            }
        }
        
        return improvements.get(dim_name, {
            "description": f"改进{dim_name}",
            "action": "improve"
        })
    
    def _execute_improvement(self, improvement: Dict) -> str:
        """执行改进（这里简化为提示用户手动改进）"""
        logger.info(f"请手动执行改进: {improvement['description']}")
        
        if not self.auto_mode:
            input("完成改进后按Enter继续...")
        
        # Git提交
        subprocess.run(
            ['git', 'add', '-A'],
            cwd=self.skill_path,
            capture_output=True
        )
        
        result = subprocess.run(
            ['git', 'commit', '-m', f"optimize {self.skill_name}: {improvement['description']}"],
            cwd=self.skill_path,
            capture_output=True,
            text=True
        )
        
        # 获取commit hash
        commit_result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=self.skill_path,
            capture_output=True,
            text=True
        )
        
        return commit_result.stdout.strip()
    
    def _independent_evaluate(self, test_prompts: List[Dict]) -> Dict:
        """独立评分（V2关键！）"""
        logger.info("独立评分开始...")
        
        evaluator = DarwinEvaluatorV2(
            str(self.skill_path),
            test_prompts,
            self.eval_mode
        )
        
        return evaluator.evaluate()
    
    def _record_result(
        self,
        old_score: float,
        new_score: float,
        status: str,
        dimension: str,
        note: str,
        commit: str
    ):
        """记录结果到results.tsv"""
        timestamp = datetime.now().isoformat()
        
        with open(self.results_file, 'a') as f:
            f.write(f"{timestamp}\t{commit}\t{self.skill_name}\t{old_score:.1f}\t{new_score:.1f}\t{status}\t{dimension}\t{note}\t{self.eval_mode}\n")
    
    def _display_scorecard(self, result: Dict, title: str):
        """展示评分卡"""
        print(f"\n{'='*60}")
        print(f"📊 {title}")
        print(f"{'='*60}")
        print(f"总分: {result['total_score']:.1f}/100")
        print(f"\n维度得分:")
        
        for dim_name, dim_data in result["dimensions"].items():
            score_rate = dim_data["score"] / dim_data["max_score"] if dim_data["max_score"] > 0 else 0
            status = "✅" if score_rate >= 0.7 else ("⚠️" if score_rate >= 0.5 else "❌")
            print(f"  {status} {dim_name}: {dim_data['score']:.1f}/{dim_data['max_score']}")
        
        if result.get("weaknesses"):
            print(f"\n弱点:")
            for w in result["weaknesses"]:
                print(f"  [{w['priority']}] {w['dimension']}: {w['score_rate']:.1%}")
        
        print(f"{'='*60}\n")
    
    def _display_final_report(self, report: Dict):
        """展示最终报告"""
        print(f"\n{'='*60}")
        print("📋 优化报告")
        print(f"{'='*60}")
        print(f"技能名称: {report['skill_name']}")
        print(f"基线分数: {report['baseline_score']:.1f}")
        print(f"最终分数: {report['final_score']:.1f}")
        print(f"提升分数: +{report['improvement']:.1f}")
        print(f"\n优化统计:")
        print(f"  总轮数: {report['total_rounds']}")
        print(f"  保留: {report['keep_rounds']}")
        print(f"  回滚: {report['revert_rounds']}")
        print(f"  评估模式: {report['eval_mode']}")
        print(f"{'='*60}\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='达尔文优化器 V2')
    parser.add_argument('skill_path', help='技能目录路径')
    parser.add_argument('--max-rounds', type=int, default=3, help='最大优化轮数')
    parser.add_argument('--auto', action='store_true', help='自动模式（跳过人在回路）')
    parser.add_argument('--eval-mode', default='dry_run', choices=['full_test', 'dry_run'], help='评估模式')
    
    args = parser.parse_args()
    
    # 创建优化器
    optimizer = DarwinOptimizerV2(
        args.skill_path,
        max_rounds=args.max_rounds,
        auto_mode=args.auto,
        eval_mode=args.eval_mode
    )
    
    # 运行优化
    result = optimizer.run_optimization()
    
    print("\n✅ 优化完成!")
    print(f"最终分数: {result['final_score']:.1f}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Lightweight Autoresearch - 主循环脚本（完整版）
整合所有优化能力：评估、优化、代码分析、安全检查、性能测试、报告生成
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 导入所有模块
sys.path.insert(0, str(Path(__file__).parent))
from evaluate import ComprehensiveEvaluator, evaluate_skill_comprehensive
from optimize import SkillOptimizer, optimize_skill
from code_analyzer import CodeAnalyzer, analyze_code, auto_fix_code
from security_checker import SecurityChecker, check_security
from performance_tester import PerformanceTester, test_performance
from report_generator import ReportGenerator, generate_report

# 配置
DEFAULT_ITERATIONS = 50
DEFAULT_TIMEOUT = 60
RESULTS_FILE = "results.tsv"

class LightweightAutoresearch:
    def __init__(self, mode, target, iterations=DEFAULT_ITERATIONS, timeout=DEFAULT_TIMEOUT,
                 enable_performance_test=True, generate_report=True):
        self.mode = mode
        self.target = Path(target)
        self.iterations = iterations
        self.timeout = timeout
        self.enable_performance_test = enable_performance_test
        self.generate_report = generate_report
        self.results_file = self.target / RESULTS_FILE
        self.best_score = 0
        self.no_improve_count = 0
        self.history = []
        
    def init_results(self):
        """初始化结果文件"""
        if not self.results_file.exists():
            with open(self.results_file, 'w') as f:
                f.write("timestamp\titeration\tscore\tstatus\tdescription\n")
    
    def run_experiment(self, iteration, description):
        """运行单次实验"""
        print(f"\n🔄 迭代 {iteration}/{self.iterations}")
        print(f"📝 描述: {description}")
        
        # 根据模式运行不同实验
        if self.mode == "skill":
            score, details = self.test_skill_comprehensive()
        elif self.mode == "strategy":
            score, details = self.test_strategy()
        elif self.mode == "content":
            score, details = self.test_content()
        else:
            score, details = 0, {}
        
        # 记录结果
        self.record_result(iteration, score, description, details)
        
        # 记录历史
        self.history.append({
            "iteration": iteration,
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "details": details
        })
        
        return score, details
    
    def test_skill_comprehensive(self):
        """综合测试技能（包含所有维度）"""
        print(f"🔍 综合评估技能包: {self.target.name}")
        
        # 使用综合评估器
        evaluator = ComprehensiveEvaluator(
            self.target, 
            enable_performance_test=self.enable_performance_test
        )
        results = evaluator.evaluate()
        
        score = results["total_score"]
        
        # 打印详细信息
        print(f"   综合评分: {score}/100")
        for category, data in results["details"].items():
            print(f"   {category}: {data['score']:.1f}/{data['max_score']}")
        
        if results["weaknesses"]:
            print(f"   弱点: {', '.join(results['weaknesses'][:3])}")
        
        return score, results
    
    def test_strategy(self):
        """测试策略（模拟）"""
        score = 50 + (time.time() % 50)
        print(f"✅ 策略回测完成，评分: {score:.1f}")
        return score, {}
    
    def test_content(self):
        """测试内容（模拟）"""
        score = 60 + (time.time() % 40)
        print(f"✅ 内容测试完成，评分: {score:.1f}")
        return score, {}
    
    def optimize(self, weaknesses, suggestions, details):
        """执行优化（包含所有优化能力）"""
        print(f"\n🔧 执行综合优化...")
        
        optimizer = SkillOptimizer(self.target)
        results = optimizer.optimize(weaknesses, suggestions)
        
        # 额外的代码优化
        if details.get("_code_results"):
            code_fixes = self._apply_code_fixes(details["_code_results"])
            if code_fixes:
                results["improvements"].extend(code_fixes)
        
        print(f"   改进项: {len(results['improvements'])}")
        for imp in results["improvements"]:
            status = "✅" if imp.get("success") else "❌"
            print(f"   {status} {imp.get('action', imp.get('weakness', '未知改进'))}")
        
        return results
    
    def _apply_code_fixes(self, code_results):
        """应用代码修复"""
        improvements = []
        
        # 自动修复代码问题
        fix_results = auto_fix_code(self.target)
        
        for fixed in fix_results.get("fixed", []):
            improvements.append({
                "action": fixed,
                "success": True
            })
        
        return improvements
    
    def generate_final_report(self, final_details):
        """生成最终报告"""
        if not self.generate_report:
            return None
        
        print(f"\n📊 生成可视化报告...")
        
        generator = ReportGenerator(self.target)
        
        report_file = generator.generate(
            evaluation_results={
                "total_score": final_details.get("total_score", 0),
                "details": final_details.get("details", {})
            },
            code_results=final_details.get("_code_results"),
            security_results=final_details.get("_security_results"),
            performance_results=final_details.get("_performance_results")
        )
        
        print(f"   报告文件: {report_file}")
        
        return report_file
    
    def record_result(self, iteration, score, description, details=None):
        """记录实验结果"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
        status = "keep" if score > self.best_score else "discard"
        
        if score > self.best_score:
            self.best_score = score
            self.no_improve_count = 0
            print(f"⬆️ 改进！新最佳评分: {score:.1f}")
        else:
            self.no_improve_count += 1
            print(f"⬇️ 未改进，连续 {self.no_improve_count} 次")
        
        with open(self.results_file, 'a') as f:
            f.write(f"{timestamp}\t{iteration}\t{score:.1f}\t{status}\t{description}\n")
    
    def should_stop(self, iteration):
        """判断是否应该停止"""
        if iteration >= self.iterations:
            print("✅ 达到最大迭代次数")
            return True
        if self.no_improve_count >= 10:
            print("⚠️ 连续10次无改进，停止优化")
            return True
        if self.best_score >= 95:
            print("✅ 达到目标分数（95+），停止优化")
            return True
        return False
    
    def run_loop(self):
        """运行主循环"""
        print(f"\n🚀 启动轻量级自主优化（完整版）")
        print(f"模式: {self.mode}")
        print(f"目标: {self.target}")
        print(f"最大迭代: {self.iterations}")
        print(f"功能: 评估 + 优化 + 代码分析 + 安全检查 + 性能测试 + 报告生成")
        
        self.init_results()
        
        final_details = None
        
        # 迭代优化
        for i in range(1, self.iterations + 1):
            # 1. 综合评估当前状态
            score, details = self.run_experiment(i, f"iteration_{i}")
            final_details = details
            
            # 2. 判断是否需要优化
            if score < 95 and details.get("weaknesses"):
                # 3. 执行优化
                optimize_results = self.optimize(
                    details["weaknesses"],
                    details.get("suggestions", []),
                    details
                )
                
                # 4. 等待优化生效
                time.sleep(1)
            
            # 5. 检查是否停止
            if self.should_stop(i):
                break
        
        # 生成最终报告
        if self.generate_report and final_details:
            report_file = self.generate_final_report(final_details)
        
        print(f"\n✅ 优化完成！最佳评分: {self.best_score:.1f}")
        print(f"📊 结果文件: {self.results_file}")
        
        if self.generate_report and final_details and report_file:
            print(f"📄 HTML报告: {report_file}")
        
        return self.best_score

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="轻量级自主优化（完整版）")
    parser.add_argument("--mode", required=True, choices=["skill", "strategy", "content"],
                        help="优化模式")
    parser.add_argument("--target", required=True, help="目标路径")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS,
                        help="迭代次数")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="单次实验超时（秒）")
    parser.add_argument("--no-performance", action="store_true",
                        help="禁用性能测试")
    parser.add_argument("--no-report", action="store_true",
                        help="禁用报告生成")
    
    args = parser.parse_args()
    
    # 验证目标路径
    if not Path(args.target).exists():
        print(f"❌ 目标路径不存在: {args.target}")
        sys.exit(1)
    
    # 运行优化
    optimizer = LightweightAutoresearch(
        mode=args.mode,
        target=args.target,
        iterations=args.iterations,
        timeout=args.timeout,
        enable_performance_test=not args.no_performance,
        generate_report=not args.no_report
    )
    
    best_score = optimizer.run_loop()
    
    print(f"\n🎉 最终最佳评分: {best_score:.1f}")

if __name__ == "__main__":
    main()
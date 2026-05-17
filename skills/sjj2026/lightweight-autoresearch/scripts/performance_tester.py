#!/usr/bin/env python3
"""
性能测试器 - 测试技能执行性能
"""

import os
import sys
import time
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

class PerformanceTester:
    """性能测试器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.results = {}
        
    def test(self) -> Dict:
        """执行性能测试"""
        results = {
            "performance_score": 0,
            "metrics": {},
            "details": {}
        }
        
        # 1. 导入性能（30分）
        import_score, import_metrics = self._test_import_performance()
        results["details"]["import"] = {
            "score": import_score,
            "max_score": 30,
            "metrics": import_metrics
        }
        
        # 2. 执行性能（40分）
        exec_score, exec_metrics = self._test_execution_performance()
        results["details"]["execution"] = {
            "score": exec_score,
            "max_score": 40,
            "metrics": exec_metrics
        }
        
        # 3. 内存使用（30分）
        memory_score, memory_metrics = self._test_memory_usage()
        results["details"]["memory"] = {
            "score": memory_score,
            "max_score": 30,
            "metrics": memory_metrics
        }
        
        # 汇总
        results["performance_score"] = import_score + exec_score + memory_score
        results["metrics"] = {**import_metrics, **exec_metrics, **memory_metrics}
        
        return results
    
    def _test_import_performance(self) -> Tuple[int, Dict]:
        """测试导入性能"""
        metrics = {
            "import_time": 0,
            "import_count": 0
        }
        score = 30
        
        # 查找主模块
        main_files = [
            self.skill_path / "scripts" / "main.py",
            self.skill_path / "__init__.py"
        ]
        
        main_file = None
        for f in main_files:
            if f.exists():
                main_file = f
                break
        
        if not main_file:
            return 15, {"import_time": None, "import_count": 0}
        
        # 测试导入时间
        try:
            start_time = time.time()
            
            # 创建临时测试脚本
            test_script = f'''
import sys
import time

start = time.time()
try:
    sys.path.insert(0, "{self.skill_path}")
    import main
    print(f"Import time: {{time.time() - start:.3f}}s")
except Exception as e:
    print(f"Import error: {{e}}")
'''
            
            result = subprocess.run(
                [sys.executable, "-c", test_script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout + result.stderr
            
            # 解析导入时间
            if "Import time:" in output:
                import_time_str = output.split("Import time:")[1].split("s")[0].strip()
                import_time = float(import_time_str)
                metrics["import_time"] = import_time
                
                # 评分：导入时间越短越好
                if import_time < 0.5:
                    score = 30
                elif import_time < 1.0:
                    score = 25
                elif import_time < 2.0:
                    score = 20
                else:
                    score = 10
            
            # 统计导入数量
            if main_file:
                content = main_file.read_text(encoding='utf-8')
                import_count = len(re.findall(r'^import |^from ', content, re.MULTILINE))
                metrics["import_count"] = import_count
                
                if import_count > 20:
                    score -= 5  # 导入过多扣分
        
        except subprocess.TimeoutExpired:
            metrics["import_time"] = None
            score = 5
        except Exception as e:
            metrics["import_time"] = None
            score = 10
        
        return max(score, 0), metrics
    
    def _test_execution_performance(self) -> Tuple[int, Dict]:
        """测试执行性能"""
        metrics = {
            "execution_time": 0,
            "test_cases_run": 0,
            "test_cases_passed": 0
        }
        score = 40
        
        # 查找测试文件
        test_files = list(self.skill_path.rglob("test_*.py"))
        
        if not test_files:
            return 20, {"execution_time": None, "test_cases_run": 0}
        
        # 运行测试
        try:
            start_time = time.time()
            
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-v", "--tb=short"],
                cwd=self.skill_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            execution_time = time.time() - start_time
            metrics["execution_time"] = execution_time
            
            # 解析测试结果
            output = result.stdout + result.stderr
            
            # 统计测试用例
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)
            
            if passed_match:
                metrics["test_cases_passed"] = int(passed_match.group(1))
            
            total_tests = 0
            if passed_match:
                total_tests += int(passed_match.group(1))
            if failed_match:
                total_tests += int(failed_match.group(1))
            
            metrics["test_cases_run"] = total_tests
            
            # 评分
            if total_tests > 0:
                pass_rate = metrics["test_cases_passed"] / total_tests
                score = int(40 * pass_rate)
            
            if execution_time > 30:
                score -= 10  # 执行时间过长扣分
            
        except subprocess.TimeoutExpired:
            metrics["execution_time"] = None
            score = 10
        except Exception:
            metrics["execution_time"] = None
            score = 15
        
        return max(score, 0), metrics
    
    def _test_memory_usage(self) -> Tuple[int, Dict]:
        """测试内存使用"""
        metrics = {
            "estimated_memory_mb": 0,
            "file_count": 0,
            "total_size_kb": 0
        }
        score = 30
        
        # 统计文件大小（粗略估算内存占用）
        total_size = 0
        file_count = 0
        
        for file_path in self.skill_path.rglob("*"):
            if file_path.is_file() and ".backup" not in str(file_path):
                total_size += file_path.stat().st_size
                file_count += 1
        
        total_size_kb = total_size / 1024
        estimated_memory_mb = total_size_kb / 1024 * 3  # 粗略估算：文件大小 × 3
        
        metrics["file_count"] = file_count
        metrics["total_size_kb"] = total_size_kb
        metrics["estimated_memory_mb"] = estimated_memory_mb
        
        # 评分：越小越好
        if estimated_memory_mb < 1:
            score = 30
        elif estimated_memory_mb < 5:
            score = 25
        elif estimated_memory_mb < 10:
            score = 20
        else:
            score = 15
        
        # 文件数量过多扣分
        if file_count > 100:
            score -= 5
        
        return max(score, 0), metrics


def test_performance(skill_path: str) -> Dict:
    """性能测试的便捷函数"""
    tester = PerformanceTester(skill_path)
    return tester.test()

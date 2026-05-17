#!/usr/bin/env python3
"""
代码质量分析器 - 分析和修复代码问题
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple

class CodeAnalyzer:
    """代码质量分析器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues = []
        self.suggestions = []
        
    def analyze(self) -> Dict:
        """综合分析代码质量"""
        results = {
            "quality_score": 0,
            "issues": [],
            "suggestions": [],
            "details": {}
        }
        
        # 1. Python 代码质量（40分）
        py_score, py_issues = self._analyze_python_code()
        results["details"]["python"] = {
            "score": py_score,
            "max_score": 40,
            "issues": py_issues
        }
        
        # 2. Shell 脚本质量（30分）
        sh_score, sh_issues = self._analyze_shell_scripts()
        results["details"]["shell"] = {
            "score": sh_score,
            "max_score": 30,
            "issues": sh_issues
        }
        
        # 3. 配置文件质量（30分）
        config_score, config_issues = self._analyze_configs()
        results["details"]["config"] = {
            "score": config_score,
            "max_score": 30,
            "issues": config_issues
        }
        
        # 汇总
        results["quality_score"] = py_score + sh_score + config_score
        results["issues"].extend(py_issues + sh_issues + config_issues)
        
        # 生成建议
        results["suggestions"] = self._generate_fix_suggestions(results["issues"])
        
        return results
    
    def _analyze_python_code(self) -> Tuple[int, List[Dict]]:
        """分析 Python 代码质量"""
        issues = []
        score = 40
        
        py_files = list(self.skill_path.rglob("*.py"))
        
        if not py_files:
            return 20, [{"type": "warning", "message": "未找到 Python 文件"}]
        
        for py_file in py_files:
            if ".backup" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # 1. 语法检查
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "error",
                        "message": f"语法错误: {e.msg}",
                        "line": e.lineno
                    })
                    score -= 10
                
                # 2. 缺少文档字符串
                if not re.search(r'"""[\s\S]+?"""', content):
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "缺少模块文档字符串"
                    })
                    score -= 2
                
                # 3. 缺少类型提示
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                if functions and 'typing' not in content:
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "suggestion",
                        "message": "建议添加类型提示"
                    })
                    score -= 3
                
                # 4. 缺少错误处理
                if 'try:' not in content and 'except' not in content:
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "suggestion",
                        "message": "建议添加异常处理"
                    })
                    score -= 2
                
                # 5. 长函数检测
                lines = content.split('\n')
                if len([l for l in lines if l.strip() and not l.strip().startswith('#')]) > 50:
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "文件过长，建议拆分"
                    })
                    score -= 3
                
            except Exception as e:
                issues.append({
                    "file": str(py_file.relative_to(self.skill_path)),
                    "type": "error",
                    "message": f"无法读取文件: {str(e)}"
                })
        
        return max(score, 0), issues
    
    def _analyze_shell_scripts(self) -> Tuple[int, List[Dict]]:
        """分析 Shell 脚本质量"""
        issues = []
        score = 30
        
        sh_files = list(self.skill_path.rglob("*.sh"))
        
        if not sh_files:
            return 20, []
        
        for sh_file in sh_files:
            if ".backup" in str(sh_file):
                continue
            
            try:
                content = sh_file.read_text(encoding='utf-8')
                
                # 1. 检查 shebang
                if not content.startswith('#!/'):
                    issues.append({
                        "file": str(sh_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "缺少 shebang (#!/bin/bash)"
                    })
                    score -= 5
                
                # 2. 检查 set -e（错误时退出）
                if 'set -e' not in content:
                    issues.append({
                        "file": str(sh_file.relative_to(self.skill_path)),
                        "type": "suggestion",
                        "message": "建议添加 'set -e' 提高健壮性"
                    })
                    score -= 3
                
                # 3. 检查变量引用（应使用 ${var}）
                if re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*[^{\s]', content):
                    issues.append({
                        "file": str(sh_file.relative_to(self.skill_path)),
                        "type": "suggestion",
                        "message": "建议使用 ${var} 而不是 $var"
                    })
                    score -= 2
                
            except Exception as e:
                issues.append({
                    "file": str(sh_file.relative_to(self.skill_path)),
                    "type": "error",
                    "message": f"无法读取文件: {str(e)}"
                })
        
        return max(score, 0), issues
    
    def _analyze_configs(self) -> Tuple[int, List[Dict]]:
        """分析配置文件质量"""
        issues = []
        score = 30
        
        # 检查常见配置文件
        config_files = {
            "_meta.json": "技能元数据",
            "skill.json": "技能配置",
            "config.py": "Python配置"
        }
        
        for config_name, desc in config_files.items():
            config_file = self.skill_path / config_name
            
            if not config_file.exists():
                continue
            
            try:
                content = config_file.read_text(encoding='utf-8')
                
                if config_name.endswith('.json'):
                    try:
                        json.loads(content)
                    except json.JSONDecodeError as e:
                        issues.append({
                            "file": config_name,
                            "type": "error",
                            "message": f"JSON 格式错误: {str(e)}"
                        })
                        score -= 10
                
                if config_name == "skill.json":
                    data = json.loads(content) if config_name.endswith('.json') else {}
                    required_fields = ["name", "description"]
                    for field in required_fields:
                        if field not in data:
                            issues.append({
                                "file": config_name,
                                "type": "warning",
                                "message": f"缺少必需字段: {field}"
                            })
                            score -= 3
                
            except Exception as e:
                issues.append({
                    "file": config_name,
                    "type": "error",
                    "message": f"无法读取文件: {str(e)}"
                })
        
        return max(score, 0), issues
    
    def _generate_fix_suggestions(self, issues: List[Dict]) -> List[str]:
        """生成修复建议"""
        suggestions = []
        
        for issue in issues:
            if issue["type"] == "error":
                if "语法错误" in issue["message"]:
                    suggestions.append(f"修复 {issue['file']} 的语法错误")
                elif "JSON 格式错误" in issue["message"]:
                    suggestions.append(f"修复 {issue['file']} 的 JSON 格式")
            
            elif issue["type"] == "warning":
                if "缺少 shebang" in issue["message"]:
                    suggestions.append(f"在 {issue['file']} 开头添加 shebang")
                elif "缺少模块文档字符串" in issue["message"]:
                    suggestions.append(f"为 {issue['file']} 添加文档字符串")
            
            elif issue["type"] == "suggestion":
                if "类型提示" in issue["message"]:
                    suggestions.append(f"为 {issue['file']} 的函数添加类型提示")
                elif "异常处理" in issue["message"]:
                    suggestions.append(f"为 {issue['file']} 添加异常处理")
        
        return list(set(suggestions))  # 去重
    
    def auto_fix(self) -> Dict:
        """自动修复代码问题"""
        results = {
            "fixed": [],
            "failed": []
        }
        
        # 分析并获取建议
        analysis = self.analyze()
        
        # 执行自动修复
        for suggestion in analysis["suggestions"]:
            fixed = self._apply_fix(suggestion)
            if fixed:
                results["fixed"].append(suggestion)
            else:
                results["failed"].append(suggestion)
        
        return results
    
    def _apply_fix(self, suggestion: str) -> bool:
        """应用单个修复"""
        # 简单的自动修复逻辑
        if "添加文档字符串" in suggestion:
            return self._add_docstring(suggestion)
        elif "添加 shebang" in suggestion:
            return self._add_shebang(suggestion)
        
        return False
    
    def _add_docstring(self, suggestion: str) -> bool:
        """添加文档字符串"""
        match = re.search(r"为 (.+) 添加", suggestion)
        if match:
            file_name = match.group(1)
            py_file = self.skill_path / file_name
            
            if py_file.exists():
                content = py_file.read_text(encoding='utf-8')
                if not content.startswith('"""'):
                    new_content = f'"""\n{self.skill_path.name} - 自动生成的文档\n"""\n\n' + content
                    py_file.write_text(new_content, encoding='utf-8')
                    return True
        
        return False
    
    def _add_shebang(self, suggestion: str) -> bool:
        """添加 shebang"""
        match = re.search(r"在 (.+) 开头", suggestion)
        if match:
            file_name = match.group(1)
            sh_file = self.skill_path / file_name
            
            if sh_file.exists():
                content = sh_file.read_text(encoding='utf-8')
                if not content.startswith('#!/'):
                    new_content = '#!/bin/bash\nset -e\n\n' + content
                    sh_file.write_text(new_content, encoding='utf-8')
                    return True
        
        return False


def analyze_code(skill_path: str) -> Dict:
    """分析代码质量的便捷函数"""
    analyzer = CodeAnalyzer(skill_path)
    return analyzer.analyze()


def auto_fix_code(skill_path: str) -> Dict:
    """自动修复代码问题的便捷函数"""
    analyzer = CodeAnalyzer(skill_path)
    return analyzer.auto_fix()

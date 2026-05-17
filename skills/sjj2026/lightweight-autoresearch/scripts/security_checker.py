#!/usr/bin/env python3
"""
安全检查器 - 检测安全问题和最佳实践
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class SecurityChecker:
    """安全检查器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues = []
        
    def check(self) -> Dict:
        """执行安全检查"""
        results = {
            "security_score": 0,
            "issues": [],
            "details": {}
        }
        
        # 1. 敏感信息检测（40分）
        secrets_score, secrets_issues = self._check_secrets()
        results["details"]["secrets"] = {
            "score": secrets_score,
            "max_score": 40,
            "issues": secrets_issues
        }
        
        # 2. 代码安全检查（30分）
        code_security_score, code_issues = self._check_code_security()
        results["details"]["code_security"] = {
            "score": code_security_score,
            "max_score": 30,
            "issues": code_issues
        }
        
        # 3. 文件权限检查（30分）
        permission_score, perm_issues = self._check_file_permissions()
        results["details"]["permissions"] = {
            "score": permission_score,
            "max_score": 30,
            "issues": perm_issues
        }
        
        # 汇总
        results["security_score"] = secrets_score + code_security_score + permission_score
        results["issues"].extend(secrets_issues + code_issues + perm_issues)
        
        return results
    
    def _check_secrets(self) -> Tuple[int, List[Dict]]:
        """检测敏感信息"""
        issues = []
        score = 40
        
        # 敏感信息模式
        secret_patterns = {
            "API Key": r'(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w\-]{20,}',
            "密码": r'(password|passwd|pwd)\s*[=:]\s*["\']?[^\s"\']{8,}',
            "Token": r'(token|secret)\s*[=:]\s*["\']?[\w\-]{20,}',
            "私钥": r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
            "AWS Key": r'AKIA[0-9A-Z]{16}',
            "数据库密码": r'(db_password|database_password)\s*[=:]\s*["\']?[^\s"\']+',
        }
        
        for file_path in self.skill_path.rglob("*"):
            if file_path.is_file() and not any(skip in str(file_path) for skip in ['.backup', '.git', '__pycache__']):
                
                # 跳过二进制文件
                if file_path.suffix in ['.pyc', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip']:
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    for pattern_name, pattern in secret_patterns.items():
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues.append({
                                "file": str(file_path.relative_to(self.skill_path)),
                                "type": "critical",
                                "message": f"发现可能的 {pattern_name}，建议使用环境变量",
                                "severity": "high"
                            })
                            score -= 10
                
                except Exception:
                    pass
        
        return max(score, 0), issues
    
    def _check_code_security(self) -> Tuple[int, List[Dict]]:
        """检查代码安全问题"""
        issues = []
        score = 30
        
        for py_file in self.skill_path.rglob("*.py"):
            if ".backup" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # 1. 检查 eval() 和 exec()
                if re.search(r'\beval\s*\(', content):
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "使用 eval() 可能导致代码注入风险",
                        "severity": "medium"
                    })
                    score -= 5
                
                # 2. 检查 os.system()
                if re.search(r'\bos\.system\s*\(', content):
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "使用 os.system() 可能导致命令注入风险，建议使用 subprocess",
                        "severity": "medium"
                    })
                    score -= 5
                
                # 3. 检查 SQL 拼接
                if re.search(r'["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?["\'].*?%', content, re.IGNORECASE):
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "可能的 SQL 注入风险，建议使用参数化查询",
                        "severity": "high"
                    })
                    score -= 10
                
                # 4. 检查硬编码路径
                if re.search(r'/root/|/home/|/etc/', content):
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "suggestion",
                        "message": "检测到硬编码路径，建议使用配置或环境变量",
                        "severity": "low"
                    })
                    score -= 2
                
                # 5. 检查未处理的异常
                if 'except:' in content and 'except Exception:' not in content:
                    issues.append({
                        "file": str(py_file.relative_to(self.skill_path)),
                        "type": "warning",
                        "message": "使用裸 except 可能隐藏错误",
                        "severity": "medium"
                    })
                    score -= 3
                
            except Exception:
                pass
        
        return max(score, 0), issues
    
    def _check_file_permissions(self) -> Tuple[int, List[Dict]]:
        """检查文件权限"""
        issues = []
        score = 30
        
        # 检查敏感文件的权限
        sensitive_files = ['.env', 'secrets.json', 'credentials.json', 'config.json']
        
        for file_name in sensitive_files:
            file_path = self.skill_path / file_name
            
            if file_path.exists():
                # 获取文件权限
                stat_info = file_path.stat()
                permissions = oct(stat_info.st_mode)[-3:]
                
                # 检查是否过于开放（任何人都可读写）
                if permissions[-1] in ['6', '7']:  # 其他用户可读写
                    issues.append({
                        "file": file_name,
                        "type": "warning",
                        "message": f"文件权限 {permissions} 过于开放，建议设置为 600",
                        "severity": "medium"
                    })
                    score -= 5
        
        # 检查脚本文件是否可执行
        scripts = self.skill_path / "scripts"
        if scripts.exists():
            for script in scripts.glob("*.py"):
                stat_info = script.stat()
                permissions = oct(stat_info.st_mode)[-3:]
                
                if permissions[0] != '7':  # 所有者无可执行权限
                    issues.append({
                        "file": f"scripts/{script.name}",
                        "type": "suggestion",
                        "message": "建议为脚本添加可执行权限",
                        "severity": "low"
                    })
                    score -= 2
        
        return max(score, 0), issues


def check_security(skill_path: str) -> Dict:
    """安全检查的便捷函数"""
    checker = SecurityChecker(skill_path)
    return checker.check()

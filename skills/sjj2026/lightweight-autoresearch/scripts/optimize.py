#!/usr/bin/env python3
"""
优化模块 - 实际的优化动作
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class SkillOptimizer:
    """技能优化器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.backup_dir = self.skill_path / ".backup"
        
    def optimize(self, weaknesses: List[str], suggestions: List[str]) -> Dict:
        """执行优化"""
        results = {
            "improvements": [],
            "before_score": 0,
            "after_score": 0,
            "changes": []
        }
        
        # 创建备份
        self._create_backup()
        
        # 根据弱点执行优化
        for weakness in weaknesses:
            improvement = self._fix_weakness(weakness)
            if improvement:
                results["improvements"].append(improvement)
        
        # 记录变更
        results["changes"] = self._get_changes()
        
        return results
    
    def _create_backup(self):
        """创建备份"""
        if self.backup_dir.exists():
            # 清理旧备份
            shutil.rmtree(self.backup_dir)
        
        self.backup_dir.mkdir(parents=True)
        
        # 备份 SKILL.md
        if self.skill_md.exists():
            shutil.copy2(self.skill_md, self.backup_dir / "SKILL.md")
    
    def _fix_weakness(self, weakness: str) -> Dict:
        """修复弱点"""
        improvement = {
            "weakness": weakness,
            "action": "",
            "success": False
        }
        
        if "缺少" in weakness and "部分" in weakness:
            # 提取缺失的部分名称
            section = weakness.split("'")[1] if "'" in weakness else "unknown"
            improvement["action"] = f"添加 {section} 部分"
            improvement["success"] = self._add_skill_md_section(section)
        
        elif "缺少" in weakness and "目录" in weakness:
            # 提取缺失的目录名称
            dir_name = weakness.split("'")[1] if "'" in weakness else "unknown"
            improvement["action"] = f"创建 {dir_name} 目录"
            improvement["success"] = self._create_directory(dir_name)
        
        elif "测试" in weakness:
            improvement["action"] = "创建测试模板"
            improvement["success"] = self._create_test_template()
        
        elif "文档" in weakness:
            improvement["action"] = "丰富文档内容"
            improvement["success"] = self._enrich_documentation()
        
        return improvement
    
    def _add_skill_md_section(self, section: str) -> bool:
        """向 SKILL.md 添加部分"""
        if not self.skill_md.exists():
            # 创建新的 SKILL.md
            self._create_skill_md()
            return True
        
        content = self.skill_md.read_text(encoding='utf-8')
        
        # 根据部分名称添加内容
        section_templates = {
            "简介": "\n\n## 简介\n\n这是一个AI技能包。\n",
            "使用方法": "\n\n## 使用方法\n\n```bash\npython scripts/main.py\n```\n",
            "示例": "\n\n## 示例\n\n### 示例1\n\n基本使用示例。\n",
            "注意事项": "\n\n## 注意事项\n\n- 注意事项1\n- 注意事项2\n"
        }
        
        if section in section_templates:
            new_content = content + section_templates[section]
            self.skill_md.write_text(new_content, encoding='utf-8')
            return True
        
        return False
    
    def _create_directory(self, dir_name: str) -> bool:
        """创建目录"""
        dir_path = self.skill_path / dir_name
        
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            
            # 创建占位文件
            if dir_name == "scripts":
                (dir_path / "__init__.py").touch()
                (dir_path / "main.py").write_text("# 主脚本\n\n", encoding='utf-8')
            elif dir_name == "tests":
                (dir_path / "__init__.py").touch()
                (dir_path / "test_basic.py").write_text("# 基础测试\n\n", encoding='utf-8')
            elif dir_name == "references":
                (dir_path / "README.md").write_text("# 参考资料\n\n", encoding='utf-8')
            
            return True
        
        return False
    
    def _create_test_template(self) -> bool:
        """创建测试模板"""
        tests_dir = self.skill_path / "tests"
        
        if not tests_dir.exists():
            tests_dir.mkdir(parents=True)
        
        test_file = tests_dir / "test_basic.py"
        
        if not test_file.exists():
            template = '''#!/usr/bin/env python3
"""
基础测试套件
"""

import unittest
from pathlib import Path

class TestSkillBasic(unittest.TestCase):
    """基础功能测试"""
    
    def setUp(self):
        self.skill_path = Path(__file__).parent.parent
    
    def test_skill_md_exists(self):
        """测试 SKILL.md 是否存在"""
        skill_md = self.skill_path / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md 应该存在")
    
    def test_skill_md_not_empty(self):
        """测试 SKILL.md 不为空"""
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            self.assertGreater(len(content), 100, "SKILL.md 内容应该超过100字")
    
    def test_directory_structure(self):
        """测试目录结构"""
        required_dirs = ["scripts", "tests"]
        for dir_name in required_dirs:
            dir_path = self.skill_path / dir_name
            self.assertTrue(dir_path.exists(), f"{dir_name} 目录应该存在")

if __name__ == '__main__':
    unittest.main()
'''
            test_file.write_text(template, encoding='utf-8')
            return True
        
        return False
    
    def _enrich_documentation(self) -> bool:
        """丰富文档内容"""
        if not self.skill_md.exists():
            return False
        
        content = self.skill_md.read_text(encoding='utf-8')
        
        # 添加示例代码（如果缺少）
        if '```' not in content:
            example_section = "\n\n## 示例\n\n```python\n# 使用示例\nresult = process_data(input_data)\nprint(result)\n```\n"
            content += example_section
            self.skill_md.write_text(content, encoding='utf-8')
            return True
        
        return False
    
    def _create_skill_md(self):
        """创建新的 SKILL.md"""
        template = f'''---
name: {self.skill_path.name}
version: 1.0.0
description: 这是一个AI技能包
---

# {self.skill_path.name}

## 简介

这是一个AI技能包，用于处理特定任务。

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

---
*创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
'''
        self.skill_md.write_text(template, encoding='utf-8')
    
    def _get_changes(self) -> List[str]:
        """获取变更列表"""
        changes = []
        
        # 检查新增文件
        if self.backup_dir.exists():
            for file in self.skill_path.rglob("*"):
                if file.is_file() and not str(file).startswith(str(self.backup_dir)):
                    backup_file = self.backup_dir / file.relative_to(self.skill_path)
                    if not backup_file.exists():
                        changes.append(f"新增: {file.relative_to(self.skill_path)}")
        
        return changes
    
    def rollback(self):
        """回滚到备份"""
        if self.backup_dir.exists():
            # 恢复 SKILL.md
            backup_skill_md = self.backup_dir / "SKILL.md"
            if backup_skill_md.exists():
                shutil.copy2(backup_skill_md, self.skill_md)


def optimize_skill(skill_path: str, weaknesses: List[str], suggestions: List[str]) -> Dict:
    """优化技能包的便捷函数"""
    optimizer = SkillOptimizer(skill_path)
    return optimizer.optimize(weaknesses, suggestions)
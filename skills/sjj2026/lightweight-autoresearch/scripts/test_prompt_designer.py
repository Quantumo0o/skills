#!/usr/bin/env python3
"""
测试Prompt设计器 - 借鉴达尔文Phase 0.5

职责：
- 自动为技能设计测试prompt
- 覆盖happy path和复杂场景
- 生成test-prompts.json
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class TestPromptDesigner:
    """测试Prompt设计器"""
    
    def __init__(self, skill_path: str):
        """
        初始化设计器
        
        Args:
            skill_path: 技能目录路径
        """
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.test_prompts_file = self.skill_path / "test-prompts.json"
        
    def design_test_prompts(self) -> List[Dict]:
        """
        为技能设计2-3个测试prompt
        
        Returns:
            测试prompt列表
        """
        # 读取SKILL.md
        skill_content = self._read_skill_md()
        
        # 理解skill做什么
        skill_intent = self._parse_intent(skill_content)
        
        # 设计测试场景
        test_prompts = []
        
        # 场景1: 最典型的使用场景（happy path）
        test_prompts.append({
            "id": 1,
            "prompt": self._design_happy_path(skill_intent),
            "expected": self._define_expectation(skill_intent, "happy"),
            "scenario": "happy_path",
            "description": f"最典型的使用场景 - {skill_intent['name']}"
        })
        
        # 场景2: 稍复杂或有歧义的场景
        test_prompts.append({
            "id": 2,
            "prompt": self._design_complex_case(skill_intent),
            "expected": self._define_expectation(skill_intent, "complex"),
            "scenario": "complex_case",
            "description": f"复杂场景 - {skill_intent['name']}的高级应用"
        })
        
        # 场景3: 边界或错误场景（可选）
        if self._has_boundary_cases(skill_content):
            test_prompts.append({
                "id": 3,
                "prompt": self._design_boundary_case(skill_intent),
                "expected": self._define_expectation(skill_intent, "boundary"),
                "scenario": "boundary_case",
                "description": f"边界场景 - {skill_intent['name']}的异常处理"
            })
        
        return test_prompts
    
    def _read_skill_md(self) -> str:
        """读取SKILL.md内容"""
        if not self.skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found: {self.skill_md}")
        
        with open(self.skill_md, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_intent(self, content: str) -> Dict:
        """
        解析skill意图
        
        Returns:
            {
                "name": "技能名称",
                "description": "技能描述",
                "keywords": ["关键词"],
                "use_cases": ["使用场景"]
            }
        """
        # 提取name
        name = "unknown"
        if content.startswith('---'):
            # 有frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.split('\n'):
                    if line.startswith('name:'):
                        name = line.split(':', 1)[1].strip()
                        break
        
        # 提取description
        description = ""
        if 'description:' in content[:500]:
            for line in content.split('\n')[:20]:
                if line.startswith('description:'):
                    description = line.split(':', 1)[1].strip()
                    break
        
        # 提取关键词
        keywords = []
        keyword_markers = ['适用场景', '使用场景', '触发词', '使用方法']
        for marker in keyword_markers:
            if marker in content:
                # 提取该部分的内容
                start = content.find(marker)
                end = content.find('\n##', start)
                if end == -1:
                    end = min(start + 500, len(content))
                section = content[start:end]
                
                # 提取关键词
                for line in section.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        keywords.append(line)
        
        return {
            "name": name,
            "description": description,
            "keywords": keywords[:10],  # 最多10个关键词
            "use_cases": keywords[:5]   # 最多5个使用场景
        }
    
    def _design_happy_path(self, intent: Dict) -> str:
        """
        设计happy path测试prompt
        
        Args:
            intent: skill意图
            
        Returns:
            测试prompt
        """
        name = intent["name"]
        keywords = intent["keywords"]
        
        # 根据技能名称生成不同的测试prompt
        if "autoresearch" in name or "优化" in name:
            return f"使用{name}优化一个技能包，运行10次迭代"
        elif "perspective" in name or "思维" in name:
            return f"用{name}的视角分析一个技术问题"
        elif "multi-agent" in name or "协作" in name:
            return f"用{name}创建一个多Agent协作任务"
        else:
            # 通用prompt
            if keywords:
                return f"{keywords[0]}，使用{name}"
            else:
                return f"使用{name}完成一个典型任务"
    
    def _design_complex_case(self, intent: Dict) -> str:
        """
        设计复杂场景测试prompt
        
        Args:
            intent: skill意图
            
        Returns:
            测试prompt
        """
        name = intent["name"]
        
        # 设计更复杂的场景
        if "autoresearch" in name or "优化" in name:
            return f"用{name}优化多个技能包，并比较优化效果"
        elif "perspective" in name or "思维" in name:
            return f"用{name}的视角分析一个复杂的产品决策问题，提供多个方案"
        elif "multi-agent" in name or "协作" in name:
            return f"用{name}创建一个跨领域的多Agent协作任务，包含技术、设计、运营三个角色"
        else:
            return f"使用{name}处理一个复杂场景：需要考虑多个因素和约束条件"
    
    def _design_boundary_case(self, intent: Dict) -> str:
        """
        设计边界场景测试prompt
        
        Args:
            intent: skill意图
            
        Returns:
            测试prompt
        """
        name = intent["name"]
        
        # 设计边界场景
        if "autoresearch" in name or "优化" in name:
            return f"当{name}遇到错误时，应该如何恢复？"
        elif "perspective" in name or "思维" in name:
            return f"当{name}的观点与现实冲突时，如何处理？"
        else:
            return f"当{name}的输入参数无效时，如何处理？"
    
    def _define_expectation(self, intent: Dict, scenario: str) -> str:
        """
        定义期望输出
        
        Args:
            intent: skill意图
            scenario: 场景类型
            
        Returns:
            期望输出描述
        """
        name = intent["name"]
        
        if scenario == "happy":
            return f"应该能够成功执行{name}的核心功能，输出符合预期"
        elif scenario == "complex":
            return f"应该能够处理复杂场景，输出详细且有条理"
        elif scenario == "boundary":
            return f"应该能够优雅地处理异常，提供有用的错误信息或fallback"
        else:
            return "输出质量符合skill宣称的能力"
    
    def _has_boundary_cases(self, content: str) -> bool:
        """
        检查skill是否有边界条件处理
        
        Args:
            content: SKILL.md内容
            
        Returns:
            是否有边界条件
        """
        boundary_markers = [
            '错误', '异常', '边界', 'fallback',
            'error', 'exception', 'boundary'
        ]
        
        content_lower = content.lower()
        return any(marker in content_lower for marker in boundary_markers)
    
    def save_test_prompts(self, test_prompts: List[Dict]) -> None:
        """
        保存测试prompt到文件
        
        Args:
            test_prompts: 测试prompt列表
        """
        with open(self.test_prompts_file, 'w', encoding='utf-8') as f:
            json.dump(test_prompts, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 测试prompt已保存到: {self.test_prompts_file}")
    
    def load_test_prompts(self) -> Optional[List[Dict]]:
        """
        加载已有的测试prompt
        
        Returns:
            测试prompt列表，如果文件不存在则返回None
        """
        if not self.test_prompts_file.exists():
            return None
        
        with open(self.test_prompts_file, 'r', encoding='utf-8') as f:
            return json.load(f)


def design_and_save(skill_path: str) -> List[Dict]:
    """
    为技能设计并保存测试prompt
    
    Args:
        skill_path: 技能目录路径
        
    Returns:
        测试prompt列表
    """
    designer = TestPromptDesigner(skill_path)
    test_prompts = designer.design_test_prompts()
    designer.save_test_prompts(test_prompts)
    return test_prompts


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 test_prompt_designer.py <skill_path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    test_prompts = design_and_save(skill_path)
    
    print("\n设计的测试prompt:")
    for tp in test_prompts:
        print(f"\n场景{tp['id']}: {tp['scenario']}")
        print(f"  Prompt: {tp['prompt']}")
        print(f"  期望: {tp['expected']}")

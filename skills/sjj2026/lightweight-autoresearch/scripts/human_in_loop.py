#!/usr/bin/env python3
"""
人在回路控制器 - 借鉴达尔文原则5

职责：
- 管理优化暂停和继续
- 展示改动摘要
- 等待用户确认
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HumanInLoopController:
    """人在回路控制器"""
    
    def __init__(self, auto_mode: bool = False):
        """
        初始化人在回路控制器
        
        Args:
            auto_mode: 自动模式（不暂停，自动继续）
        """
        self.auto_mode = auto_mode
        self.paused = False
        self.current_skill = None
        self.modifications = None
    
    def pause_for_review(self, skill_name: str, modifications: Dict) -> str:
        """
        暂停优化，等待用户确认
        
        Args:
            skill_name: 技能名称
            modifications: 改动摘要
                {
                    "git_diff": "...",
                    "score_change": {"before": 72, "after": 85},
                    "test_outputs_comparison": "...",
                    "suggestions": ["保留", "回滚", "继续优化"]
                }
            
        Returns:
            用户决策：keep/revert/continue
        """
        self.paused = True
        self.current_skill = skill_name
        self.modifications = modifications
        
        # 如果是自动模式，直接返回keep
        if self.auto_mode:
            logger.info("自动模式，自动继续")
            self.paused = False
            return "keep"
        
        # 展示改动摘要
        self._display_modifications()
        
        # 等待用户输入
        user_decision = self._wait_for_user_input()
        
        return user_decision
    
    def _display_modifications(self):
        """展示改动摘要"""
        print(f"\n{'='*60}")
        print(f"🔍 技能优化完成：{self.current_skill}")
        print(f"{'='*60}\n")
        
        # 显示分数变化
        score_change = self.modifications.get("score_change", {})
        before = score_change.get("before", 0)
        after = score_change.get("after", 0)
        delta = after - before
        
        print("📊 分数变化：")
        print(f"  改前：{before}分")
        print(f"  改后：{after}分")
        if delta >= 0:
            print(f"  提升：+{delta}分 ({delta/before*100:.1f}%)\n")
        else:
            print(f"  下降：{delta}分 ({delta/before*100:.1f}%)\n")
        
        # 显示维度变化
        dimension_changes = self.modifications.get("dimension_changes", [])
        if dimension_changes:
            print("📈 维度变化：")
            for dim_change in dimension_changes:
                dim = dim_change.get("dimension", "")
                old = dim_change.get("old", 0)
                new = dim_change.get("new", 0)
                diff = new - old
                if diff > 0:
                    print(f"  {dim}: {old} → {new} (+{diff})")
                else:
                    print(f"  {dim}: {old} → {new} ({diff})")
            print()
        
        # 显示git diff
        git_diff = self.modifications.get("git_diff", "")
        if git_diff:
            print("📝 改动内容：")
            # 只显示前500字符
            diff_preview = git_diff[:500]
            if len(git_diff) > 500:
                diff_preview += "...\n"
            print(diff_preview)
        
        # 显示测试对比
        test_comparison = self.modifications.get("test_outputs_comparison", "")
        if test_comparison:
            print("🧪 测试对比：")
            print(test_comparison[:300])
            if len(test_comparison) > 300:
                print("...\n")
        
        # 显示建议
        suggestions = self.modifications.get("suggestions", ["保留", "回滚", "继续优化"])
        print("💡 建议：")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n{'='*60}")
    
    def _wait_for_user_input(self) -> str:
        """
        等待用户输入
        
        Returns:
            用户决策
        """
        while self.paused:
            try:
                decision = input("\n请选择操作（1-保留/2-回滚/3-继续优化）[默认:1]: ").strip()
                
                if not decision or decision in ["1", "保留", "keep"]:
                    self.paused = False
                    return "keep"
                elif decision in ["2", "回滚", "revert"]:
                    self.paused = False
                    return "revert"
                elif decision in ["3", "继续优化", "continue"]:
                    self.paused = False
                    return "continue"
                else:
                    print("❌ 无效输入，请选择：1-保留/2-回滚/3-继续优化")
            except KeyboardInterrupt:
                print("\n\n⚠️ 用户中断，默认回滚")
                self.paused = False
                return "revert"
            except EOFError:
                # 非交互环境，默认继续
                print("\n非交互环境，自动继续")
                self.paused = False
                return "keep"
        
        return "keep"
    
    def display_summary(self, skills_optimized: int, total_improvement: float, rounds: int):
        """
        展示优化总结
        
        Args:
            skills_optimized: 优化的技能数量
            total_improvement: 总提升分数
            rounds: 总轮数
        """
        print(f"\n{'='*60}")
        print("📋 优化总结")
        print(f"{'='*60}")
        print(f"优化技能数：{skills_optimized}")
        print(f"总提升分数：+{total_improvement:.1f}")
        print(f"总优化轮数：{rounds}")
        print(f"{'='*60}\n")


def create_modifications_dict(
    skill_path: str,
    before_score: float,
    after_score: float,
    dimension_changes: Optional[list] = None,
    commit_hash: Optional[str] = None
) -> Dict:
    """
    创建modifications字典
    
    Args:
        skill_path: 技能路径
        before_score: 改前分数
        after_score: 改后分数
        dimension_changes: 维度变化列表
        commit_hash: git commit hash
        
    Returns:
        modifications字典
    """
    # 获取git diff
    git_diff = ""
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD'],
            cwd=skill_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        git_diff = result.stdout
    except Exception as e:
        logger.warning(f"无法获取git diff: {e}")
    
    return {
        "git_diff": git_diff,
        "score_change": {
            "before": before_score,
            "after": after_score
        },
        "dimension_changes": dimension_changes or [],
        "commit_hash": commit_hash,
        "suggestions": [
            "保留（推荐）- 分数已提升",
            "回滚 - 如果改动有问题",
            "继续优化 - 进一步改进其他维度"
        ]
    }


if __name__ == "__main__":
    # 测试人在回路控制器
    controller = HumanInLoopController(auto_mode=False)
    
    # 模拟一次优化
    modifications = {
        "score_change": {"before": 62.8, "after": 76.6},
        "dimension_changes": [
            {"dimension": "Frontmatter质量", "old": 2.4, "new": 7.2},
            {"dimension": "实测表现", "old": 15, "new": 20},
            {"dimension": "边界条件覆盖", "old": 5, "new": 9}
        ],
        "git_diff": "示例diff内容...",
        "suggestions": ["保留", "回滚", "继续优化"]
    }
    
    decision = controller.pause_for_review("test-skill", modifications)
    print(f"\n用户决策: {decision}")

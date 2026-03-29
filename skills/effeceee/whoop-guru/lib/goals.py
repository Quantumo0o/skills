"""
Goals Module - 目标追踪系统
管理用户健身目标设定和进度追踪
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 路径设置
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lib/ -> whoop-guru/
GOALS_DIR = os.path.join(SKILL_DIR, "data", "profiles")


@dataclass
class Goal:
    """目标数据类"""
    goal_id: str
    user_id: str
    goal_type: str  # 增肌/减脂/力量/体能
    target: float
    current: float
    unit: str  # kg/次/%
    deadline: str
    created_at: str
    updated_at: str
    completed: bool = False
    completed_at: str = ""


class GoalsManager:
    """
    目标管理器
    管理用户的健身目标
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.goals_file = os.path.join(GOALS_DIR, f"goals_{user_id}.json")
        os.makedirs(GOALS_DIR, exist_ok=True)
    
    def _load_goals(self) -> List[Dict]:
        """加载目标"""
        if not os.path.exists(self.goals_file):
            return []
        try:
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_goals(self, goals: List[Dict]) -> bool:
        """保存目标"""
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(goals, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def create_goal(
        self,
        goal_type: str,
        target: float,
        current: float,
        unit: str,
        deadline: str
    ) -> Goal:
        """创建新目标"""
        goal = Goal(
            goal_id=f"goal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=self.user_id,
            goal_type=goal_type,
            target=target,
            current=current,
            unit=unit,
            deadline=deadline,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        goals = self._load_goals()
        goals.append(asdict(goal))
        self._save_goals(goals)
        
        return goal
    
    def get_active_goals(self) -> List[Goal]:
        """获取活跃目标"""
        goals = self._load_goals()
        return [Goal(**g) for g in goals if not g.get("completed", False)]
    
    def get_completed_goals(self) -> List[Goal]:
        """获取已完成目标"""
        goals = self._load_goals()
        return [Goal(**g) for g in goals if g.get("completed", False)]
    
    def update_progress(self, goal_id: str, current: float) -> bool:
        """更新目标进度"""
        goals = self._load_goals()
        
        for goal in goals:
            if goal["goal_id"] == goal_id:
                goal["current"] = current
                goal["updated_at"] = datetime.now().isoformat()
                
                # 检查是否完成
                if current >= goal["target"]:
                    goal["completed"] = True
                    goal["completed_at"] = datetime.now().isoformat()
                
                return self._save_goals(goals)
        
        return False
    
    def mark_completed(self, goal_id: str) -> bool:
        """标记目标完成"""
        goals = self._load_goals()
        
        for goal in goals:
            if goal["goal_id"] == goal_id:
                goal["completed"] = True
                goal["completed_at"] = datetime.now().isoformat()
                goal["updated_at"] = datetime.now().isoformat()
                return self._save_goals(goals)
        
        return False
    
    def delete_goal(self, goal_id: str) -> bool:
        """删除目标"""
        goals = self._load_goals()
        original_len = len(goals)
        goals = [g for g in goals if g["goal_id"] != goal_id]
        
        if len(goals) < original_len:
            return self._save_goals(goals)
        return False
    
    def get_goal_progress(self, goal: Goal) -> Dict:
        """计算目标进度"""
        if goal.target == 0:
            progress = 0
        else:
            progress = (goal.current / goal.target) * 100
        
        remaining = max(0, goal.target - goal.current)
        
        # 计算剩余天数
        days_left = 0
        try:
            deadline = datetime.strptime(goal.deadline, "%Y-%m-%d")
            days_left = (deadline - datetime.now()).days
        except Exception:
            pass
        
        # 判断是否在轨道上
        if days_left <= 0:
            on_track = goal.completed
        else:
            total_days = (datetime.strptime(goal.deadline, "%Y-%m-%d") - datetime.strptime(goal.created_at[:10], "%Y-%m-%d")).days
            elapsed = total_days - days_left
            expected_progress = (elapsed / total_days) * 100 if total_days > 0 else 0
            on_track = progress >= expected_progress * 0.9
        
        return {
            "progress": round(min(100, progress), 1),
            "remaining": round(remaining, 1),
            "days_left": days_left,
            "on_track": on_track,
            "completed": goal.completed
        }
    
    def generate_report(self) -> Dict:
        """生成目标报告"""
        active = self.get_active_goals()
        completed = self.get_completed_goals()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "active_count": len(active),
            "completed_count": len(completed),
            "active_goals": [],
            "completed_goals": [],
            "summary": ""
        }
        
        # 活跃目标详情
        for goal in active[:5]:  # 最多5个
            progress = self.get_goal_progress(goal)
            report["active_goals"].append({
                "goal_type": goal.goal_type,
                "current": goal.current,
                "target": goal.target,
                "unit": goal.unit,
                "deadline": goal.deadline,
                **progress
            })
        
        # 已完成目标
        for goal in completed[-5:]:  # 最近5个
            report["completed_goals"].append({
                "goal_type": goal.goal_type,
                "target": goal.target,
                "unit": goal.unit,
                "completed_at": goal.completed_at
            })
        
        # 总结
        if active:
            on_track_count = sum(1 for g in active if self.get_goal_progress(g).get("on_track"))
            report["summary"] = f"有{len(active)}个活跃目标，{on_track_count}个在轨道上"
        else:
            report["summary"] = "暂无活跃目标"
        
        return report


def create_goal(user_id: str, goal_type: str, target: float, current: float, unit: str, deadline: str) -> Goal:
    """创建目标"""
    manager = GoalsManager(user_id)
    return manager.create_goal(goal_type, target, current, unit, deadline)


def get_goals_report(user_id: str = "default") -> Dict:
    """获取目标报告"""
    manager = GoalsManager(user_id)
    return manager.generate_report()


def update_goal_progress(user_id: str, goal_id: str, current: float) -> bool:
    """更新进度"""
    manager = GoalsManager(user_id)
    return manager.update_progress(goal_id, current)


if __name__ == "__main__":
    print("=== Goals Manager Test ===")
    
    manager = GoalsManager("test_user")
    
    # 创建测试目标
    print("\n--- Create Goal ---")
    goal = manager.create_goal(
        goal_type="增肌",
        target=80,
        current=75,
        unit="kg",
        deadline="2026-07-29"
    )
    print(f"Created: {goal.goal_type} {goal.current} → {goal.target} {goal.unit}")
    
    # 获取报告
    print("\n--- Goals Report ---")
    report = manager.generate_report()
    print(f"Active: {report['active_count']}")
    print(f"Summary: {report['summary']}")
    
    # 更新进度
    print("\n--- Update Progress ---")
    manager.update_progress(goal.goal_id, 77)
    progress = manager.get_goal_progress(goal)
    print(f"Progress: {progress['progress']}%, Days left: {progress['days_left']}")

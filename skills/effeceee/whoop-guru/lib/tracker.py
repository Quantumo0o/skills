"""
进度追踪模块
记录用户打卡、训练完成情况、目标进度
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class CheckIn:
    """打卡记录"""
    checkin_id: str
    user_id: str
    date: str
    training_type: str
    completed: bool
    exercises: List[Dict]
    feedback: str
    whoop_strain: float
    whoop_recovery: float
    created_at: str


class ProgressTracker:
    """
    进度追踪器
    管理用户训练打卡和目标进度
    """
    
    def __init__(self, data_dir: str = "data/logs"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def _get_file_path(self, user_id: str) -> str:
        return os.path.join(self.data_dir, f"checkins_{user_id}.json")
    
    def _load_checkins(self, user_id: str) -> List[Dict]:
        filepath = self._get_file_path(user_id)
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_checkins(self, user_id: str, checkins: List[Dict]) -> bool:
        filepath = self._get_file_path(user_id)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(checkins, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def add_checkin(
        self,
        user_id: str,
        training_type: str,
        completed: bool,
        exercises: List[Dict],
        feedback: str = "",
        whoop_strain: float = 0,
        whoop_recovery: float = 0
    ) -> bool:
        """添加打卡记录"""
        checkins = self._load_checkins(user_id)
        
        new_checkin = {
            "checkin_id": f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "training_type": training_type,
            "completed": completed,
            "exercises": exercises,
            "feedback": feedback,
            "whoop_strain": whoop_strain,
            "whoop_recovery": whoop_recovery,
            "created_at": datetime.now().isoformat()
        }
        
        checkins.append(new_checkin)
        return self._save_checkins(user_id, checkins)
    
    def get_checkins(self, user_id: str, days: int = 7) -> List[Dict]:
        """获取最近N天的打卡记录"""
        checkins = self._load_checkins(user_id)
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        return [c for c in checkins if c.get('date', '') >= cutoff]
    
    def get_weekly_summary(self, user_id: str) -> Dict:
        """获取周度总结"""
        checkins = self.get_checkins(user_id, days=7)
        
        total = len(checkins)
        completed = sum(1 for c in checkins if c.get('completed'))
        
        training_types = {}
        for c in checkins:
            tt = c.get('training_type', '未知')
            training_types[tt] = training_types.get(tt, 0) + 1
        
        avg_strain = 0
        if checkins:
            strains = [c.get('whoop_strain', 0) for c in checkins if c.get('whoop_strain')]
            avg_strain = sum(strains) / len(strains) if strains else 0
        
        return {
            "week": datetime.now().strftime('%Y-W%W'),
            "total_checkins": total,
            "completed": completed,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "training_types": training_types,
            "avg_strain": round(avg_strain, 1),
            "checkins": checkins
        }
    
    def get_streak(self, user_id: str) -> int:
        """获取连续打卡天数"""
        checkins = self._load_checkins(user_id)
        if not checkins:
            return 0
        
        dates = sorted(set(c.get('date', '') for c in checkins if c.get('completed')))
        if not dates:
            return 0
        
        streak = 1
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        if dates[-1] not in [today, yesterday]:
            return 0
        
        for i in range(len(dates) - 2, -1, -1):
            d1 = datetime.strptime(dates[i + 1], '%Y-%m-%d')
            d2 = datetime.strptime(dates[i], '%Y-%m-%d')
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        
        return streak


class GoalTracker:
    """
    目标追踪器
    管理用户目标设定和达成进度
    """
    
    def __init__(self, data_dir: str = "data/profiles"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def _get_goals_file(self, user_id: str) -> str:
        return os.path.join(self.data_dir, f"goals_{user_id}.json")
    
    def set_goal(
        self,
        user_id: str,
        goal_type: str,
        target: float,
        current: float,
        deadline: str,
        unit: str = ""
    ) -> bool:
        """设定目标"""
        goals_file = self._get_goals_file(user_id)
        goals = []
        if os.path.exists(goals_file):
            try:
                with open(goals_file, 'r', encoding='utf-8') as f:
                    goals = json.load(f)
            except Exception:
                goals = []
        
        goal = {
            "goal_id": f"goal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": goal_type,
            "target": target,
            "current": current,
            "deadline": deadline,
            "unit": unit,
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
        
        goals.append(goal)
        
        try:
            with open(goals_file, 'w', encoding='utf-8') as f:
                json.dump(goals, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def get_goals(self, user_id: str) -> List[Dict]:
        """获取用户目标"""
        goals_file = self._get_goals_file(user_id)
        if not os.path.exists(goals_file):
            return []
        try:
            with open(goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def update_progress(self, user_id: str, goal_type: str, current: float) -> bool:
        """更新目标进度"""
        goals = self.get_goals(user_id)
        updated = False
        
        for goal in goals:
            if goal.get('type') == goal_type and not goal.get('completed'):
                goal['current'] = current
                if current >= goal['target']:
                    goal['completed'] = True
                    goal['completed_at'] = datetime.now().isoformat()
                updated = True
        
        if updated:
            goals_file = self._get_goals_file(user_id)
            try:
                with open(goals_file, 'w', encoding='utf-8') as f:
                    json.dump(goals, f, ensure_ascii=False, indent=2)
                return True
            except Exception:
                return False
        
        return False
    
    def get_active_goals(self, user_id: str) -> List[Dict]:
        """获取活跃目标"""
        goals = self.get_goals(user_id)
        return [g for g in goals if not g.get('completed', False)]
    
    def get_goal_progress(self, goal: Dict) -> Dict:
        """计算目标进度"""
        target = goal.get('target', 0)
        current = goal.get('current', 0)
        progress = (current / target * 100) if target > 0 else 0
        
        deadline = goal.get('deadline', '')
        days_left = 0
        if deadline:
            try:
                deadline_dt = datetime.strptime(deadline, '%Y-%m-%d')
                days_left = (deadline_dt - datetime.now()).days
            except Exception:
                days_left = 0
        
        return {
            "progress": round(progress, 1),
            "remaining": round(target - current, 1) if target > current else 0,
            "days_left": days_left,
            "on_track": days_left > 0 and progress >= (1 - days_left / 112) * 100
        }


# 全局实例
_tracker = None
_goal_tracker = None

def get_tracker() -> ProgressTracker:
    global _tracker
    if _tracker is None:
        _tracker = ProgressTracker()
    return _tracker

def get_goal_tracker() -> GoalTracker:
    global _goal_tracker
    if _goal_tracker is None:
        _goal_tracker = GoalTracker()
    return _goal_tracker

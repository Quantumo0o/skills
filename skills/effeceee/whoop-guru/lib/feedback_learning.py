#!/usr/bin/env python3
import os
"""
Feedback Learning System - Collects user feedback and learns from it
"""
import json
from datetime import datetime, timedelta

FEEDBACK_FILE = os.environ.get('WHOOP_DATA_DIR', '/root/.openclaw/workspace-healthgao/data/processed') + '/feedback_learn.json'

def load_feedback():
    try:
        with open(FEEDBACK_FILE) as f:
            return json.load(f)
    except:
        return {"feedback": [], "learnings": {}, "adjustments": []}

def save_feedback(data):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_feedback(category, feedback_type, note=""):
    """Add user feedback"""
    data = load_feedback()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "category": category,  # "training", "sleep", "recovery"
        "type": feedback_type,  # "helpful", "not_helpful"
        "note": note
    }
    
    data["feedback"].append(entry)
    
    # Update learnings
    if category not in data["learnings"]:
        data["learnings"][category] = {"helpful": 0, "not_helpful": 0}
    
    if feedback_type == "helpful":
        data["learnings"][category]["helpful"] += 1
    else:
        data["learnings"][category]["not_helpful"] += 1
    
    # Generate adjustment
    total = data["learnings"][category]["helpful"] + data["learnings"][category]["not_helpful"]
    if total > 0:
        effectiveness = data["learnings"][category]["helpful"] / total
        
        if effectiveness < 0.5:
            adjustment = {
                "category": category,
                "action": "调整建议策略",
                "reason": f"用户反馈有效性低于50% ({effectiveness:.0%})"
            }
            data["adjustments"].append(adjustment)
    
    save_feedback(data)
    return data

def get_effectiveness_stats():
    """Get effectiveness statistics"""
    data = load_feedback()
    
    stats = {}
    for category, counts in data.get("learnings", {}).items():
        total = counts["helpful"] + counts["not_helpful"]
        if total > 0:
            stats[category] = {
                "helpful": counts["helpful"],
                "not_helpful": counts["not_helpful"],
                "effectiveness": f"{counts['helpful'] / total:.0%}",
                "total": total
            }
    
    return stats

def adjust_recommendation(original_rec, category):
    """Adjust recommendation based on feedback"""
    stats = get_effectiveness_stats()
    
    if category in stats:
        effectiveness = stats[category]["effectiveness"]
        
        # If not helpful, make more conservative
        if stats[category]["not_helpful"] > stats[category]["helpful"]:
            if "跑步" in str(original_rec):
                return "建议休息或轻度活动"
            elif "休息" in str(original_rec):
                return "继续保持休息"
    
    return original_rec

# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        stats = get_effectiveness_stats()
        print("📊 建议有效性统计")
        print("-" * 40)
        if not stats:
            print("暂无反馈数据")
        else:
            for cat, s in stats.items():
                print(f"{cat}: {s['effectiveness']} ({s['total']}次)")
    elif sys.argv[1] == "add" and len(sys.argv) >= 4:
        category = sys.argv[2]
        feedback_type = sys.argv[3]
        note = sys.argv[4] if len(sys.argv) > 4 else ""
        result = add_feedback(category, feedback_type, note)
        print(f"✅ 反馈已记录: {category} - {feedback_type}")

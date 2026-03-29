#!/usr/bin/env python3
import os
"""
Comprehensive Health Analysis - All features
"""
import json
from datetime import datetime, timedelta

DATA_FILE = os.environ.get('WHOOP_DATA_DIR', '/root/.openclaw/workspace-healthgao/data/processed/latest.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def analyze_heart_rate_zones(workouts):
    """Analyze heart rate zone distribution"""
    zones = {"zone0": 0, "zone1": 0, "zone2": 0, "zone3": 0, "zone4": 0, "zone5": 0}
    
    for w in workouts[:7]:  # Last 7 workouts
        for z in range(6):
            key = f"zone{z}_min"
            zones[f"zone{z}"] += w.get(key, 0)
    
    total = sum(zones.values())
    if total == 0:
        return zones, {}
    
    percentages = {k: round(v/total*100, 1) for k, v in zones.items()}
    
    # Interpretation
    aerobic = percentages.get('zone2', 0) + percentages.get('zone3', 0)
    anaerobic = percentages.get('zone4', 0) + percentages.get('zone5', 0)
    
    return zones, percentages, aerobic, anaerobic

def analyze_sleep_structure(sleep_data):
    """Analyze sleep stage distribution"""
    stages = {"light": 0, "deep": 0, "rem": 0}
    
    for s in sleep_data[:7]:
        stages["light"] += s.get('light_sleep_hours', 0)
        stages["deep"] += s.get('deep_sleep_hours', 0)
        stages["rem"] += s.get('rem_sleep_hours', 0)
    
    total = sum(stages.values())
    if total == 0:
        return stages, {}
    
    percentages = {k: round(v/total*100, 1) for k, v in stages.items()}
    return stages, percentages

def analyze_hrv_trend(recovery):
    """HRV trend analysis"""
    hrv_data = []
    for r in recovery[:30]:  # Last 30 days
        hrv_data.append({
            "date": r.get('date'),
            "hrv": r.get('hrv', 0),
            "recovery": r.get('recovery_score', 0)
        })
    return hrv_data

def analyze_respiratory_rate(sleep_data):
    """Respiratory rate analysis"""
    rr_data = []
    for s in sleep_data[:14]:
        rr = s.get('respiratory_rate', 0)
        if rr > 0:
            rr_data.append({
                "date": s.get('date'),
                "rr": rr
            })
    
    if not rr_data:
        return None, None
    
    avg_rr = sum(r['rr'] for r in rr_data) / len(rr_data)
    
    # Interpretation
    if avg_rr < 12:
        interpretation = "偏低"
    elif avg_rr <= 20:
        interpretation = "正常"
    else:
        interpretation = "偏高"
    
    return rr_data, round(avg_rr, 1), interpretation

def calculate_body_battery(recovery_score, sleep_perf):
    """Calculate body battery metaphor"""
    # Simple calculation
    battery = (recovery_score * 0.6 + sleep_perf * 0.4)
    
    if battery >= 80:
        level = "满格"
        emoji = "🟢"
    elif battery >= 60:
        level = "良好"
        emoji = "🟡"
    elif battery >= 40:
        level = "一般"
        emoji = "🟠"
    else:
        level = "需充电"
        emoji = "🔴"
    
    return round(battery, 1), level, emoji

def analyze_prediction_accuracy():
    """Analyze prediction accuracy if data exists"""
    # This would compare predicted vs actual recovery
    # For now, return placeholder
    return {
        "predicted_days": 0,
        "avg_error": 0,
        "accuracy": 0
    }

def generate_comprehensive():
    """Generate comprehensive analysis report"""
    data = load_data()
    processed = data.get('processed', {})
    
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    cycles = processed.get('cycles', [])
    workouts = processed.get('workouts', [])
    
    result = {}
    
    # 1. Heart Rate Zones
    zones, percentages, aerobic, anaerobic = analyze_heart_rate_zones(workouts)
    result["heart_zones"] = {
        "zones": zones,
        "percentages": percentages,
        "aerobic": aerobic,
        "anaerobic": anaerobic
    }
    
    # 2. Sleep Structure
    stages, stage_pcts = analyze_sleep_structure(sleep)
    result["sleep_stages"] = {
        "hours": stages,
        "percentages": stage_pcts
    }
    
    # 3. HRV Trend
    result["hrv_trend"] = analyze_hrv_trend(recovery)
    
    # 4. Respiratory Rate
    rr_data, avg_rr, rr_interp = analyze_respiratory_rate(sleep)
    result["respiratory"] = {
        "data": rr_data,
        "average": avg_rr,
        "interpretation": rr_interp
    }
    
    # 5. Body Battery (for latest day)
    if recovery and sleep:
        rec = recovery[0].get('recovery_score', 50)
        sp = sleep[0].get('sleep_performance', 70)
        battery, level, emoji = calculate_body_battery(rec, sp)
        result["body_battery"] = {
            "level": battery,
            "status": level,
            "emoji": emoji
        }
    
    # 6. Prediction Accuracy
    result["prediction_accuracy"] = analyze_prediction_accuracy()
    
    # Save
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'comprehensive_analysis.json'), 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    return result

if __name__ == "__main__":
    result = generate_comprehensive()
    
    print("=== 综合分析 ===")
    print(f"心率区间: {result['heart_zones']['percentages']}")
    print(f"有氧: {result['heart_zones']['aerobic']}%, 无氧: {result['heart_zones']['anaerobic']}%")
    print(f"睡眠结构: {result['sleep_stages']['percentages']}")
    print(f"呼吸率: {result['respiratory']['average']} ({result['respiratory']['interpretation']})")
    print(f"身体电量: {result['body_battery']['emoji']} {result['body_battery']['level']}%")

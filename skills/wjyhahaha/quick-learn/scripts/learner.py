#!/usr/bin/env python3
"""
quick-learn 辅助脚本：生成学习路径结构 + 自测题目
用法:
  python3 learner.py path <topic> <days> --output <json_path>
  python3 quiz  <path_json> <day_label> --output <json_path>
  python3 learner.py list --dir learning-data
"""

import json, sys, os, argparse, glob
from datetime import datetime, timedelta

def generate_path(topic, days, output=None):
    slug = topic.lower().replace(" ", "-").replace("_", "-")
    path = {
        "topic": topic,
        "slug": slug,
        "total_days": days,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
        "current_day": 1,
        "daily_time_min": 30,
        "preferred_time": "09:00",
        "timezone": "Asia/Shanghai",
        "push_channel": "webchat",
        "learning_method": "feynman",
        "days": []
    }
    for i in range(1, days + 1):
        path["days"].append({
            "day": i,
            "title": "",
            "materials": [],
            "feynman_prompt": "",
            "simplify_target": "",
            "completed": False,
            "completed_at": None
        })
    result = json.dumps(path, ensure_ascii=False, indent=2)
    if output:
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w") as f:
            f.write(result)
        print(f"Path saved to {output} (slug: {slug})")
    else:
        print(result)

def generate_quiz(path_json, day_label, output=None):
    with open(path_json) as f:
        path = json.load(f)
    quiz = {
        "topic": path["topic"],
        "day_label": day_label,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "questions": []
    }
    result = json.dumps(quiz, ensure_ascii=False, indent=2)
    if output:
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w") as f:
            f.write(result)
        print(f"Quiz template saved to {output}")
    else:
        print(result)

def list_plans(data_dir):
    pattern = os.path.join(data_dir, "*", "path.json")
    files = sorted(glob.glob(pattern))
    if not files:
        print("No active learning plans found.")
        return
    for f in files:
        with open(f) as fh:
            d = json.load(fh)
        status_icon = "✅" if d["status"] == "completed" else "🚀" if d["status"] == "active" else "⏸"
        day_info = f"Day {d['current_day']}/{d['total_days']}"
        print(f"{status_icon} {d['topic']} ({d.get('slug', '?')}) — {day_info} | {d['status']} | Created: {d['created_at']}")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p1 = sub.add_parser("path")
    p1.add_argument("topic")
    p1.add_argument("days", type=int)
    p1.add_argument("--output")
    p2 = sub.add_parser("quiz")
    p2.add_argument("path_json")
    p2.add_argument("day_label")
    p2.add_argument("--output")
    p3 = sub.add_parser("list")
    p3.add_argument("--dir", default="learning-data")
    args = parser.parse_args()
    if args.cmd == "path":
        generate_path(args.topic, args.days, args.output)
    elif args.cmd == "quiz":
        generate_quiz(args.path_json, args.day_label, args.output)
    elif args.cmd == "list":
        list_plans(args.dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

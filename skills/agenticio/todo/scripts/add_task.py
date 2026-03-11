#!/usr/bin/env python3
"""Add new task to system."""
import json
import os
import uuid
import argparse
from datetime import datetime

TODO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/todo")
TASKS_FILE = os.path.join(TODO_DIR, "tasks.json")

def ensure_dir():
    os.makedirs(TODO_DIR, exist_ok=True)

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {"tasks": []}

def save_tasks(data):
    ensure_dir()
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add new task')
    parser.add_argument('--task', required=True, help='Task description')
    parser.add_argument('--deadline', help='Deadline (YYYY-MM-DD)')
    parser.add_argument('--context', help='Context (phone, desk, computer, etc)')
    parser.add_argument('--energy', choices=['high', 'medium', 'low'], help='Energy required')
    parser.add_argument('--project', help='Associated project')
    
    args = parser.parse_args()
    
    task_id = f"TASK-{str(uuid.uuid4())[:6].upper()}"
    
    # Determine priority quadrant
    # This is simplified - real implementation would use more sophisticated logic
    priority = "important"  # Default
    
    task = {
        "id": task_id,
        "description": args.task,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "deadline": args.deadline,
        "context": args.context or "any",
        "energy": args.energy or "medium",
        "project": args.project,
        "priority": priority
    }
    
    data = load_tasks()
    data['tasks'].append(task)
    save_tasks(data)
    
    print(f"✓ Task captured: {task_id}")
    print(f"  {args.task}")
    if args.deadline:
        print(f"  Deadline: {args.deadline}")
    print(f"  Context: {task['context']}")

if __name__ == '__main__':
    main()

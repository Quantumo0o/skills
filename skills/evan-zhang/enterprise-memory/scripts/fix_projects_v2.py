#!/usr/bin/env python3
"""修复项目 ID 和 state.json - 使用目录名作为 ID"""

import json
import re
from pathlib import Path
from datetime import datetime

EAM_ROOT = Path.home() / ".openclaw" / "EAM-projects"

REQUIRED_FIELDS = ["id", "title", "mode", "owner", "status", "stage", "createdAt", "updatedAt"]
STATUS_ENUM = ["DISCUSSING", "READY", "RUNNING", "PAUSED", "BLOCKED", "DONE", "WAITING_USER"]
STAGE_ENUM = ["TARGET", "PLAN", "CHECKLIST", "EXECUTE", "ARCHIVE", "DONE"]
MODE_ENUM = ["lite", "full"]


def load_state(state_path):
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_path, data):
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_title(state_data):
    """从 state.json 提取标题"""
    return state_data.get("title", "") or state_data.get("name", "") or ""


def fix_state_json(state_path):
    """修复 state.json，使用目录名作为 ID"""
    project_dir = state_path.parent
    dir_name = project_dir.name  # 目录名就是新的 ID
    
    data = load_state(state_path)
    old_id = data.get("id", "")
    
    # 更新 ID
    data["id"] = dir_name
    
    # 提取标题
    title = extract_title(data)
    if not title:
        title = dir_name
    data["title"] = title
    
    # 验证/修复字段
    if data.get("mode") not in MODE_ENUM:
        data["mode"] = "full"
    if not data.get("owner"):
        data["owner"] = "evan"
    if data.get("status") not in STATUS_ENUM:
        data["status"] = "DISCUSSING"
    if data.get("stage") not in STAGE_ENUM:
        data["stage"] = "TARGET"
    
    # 确保时间
    if not data.get("createdAt"):
        data["createdAt"] = "2026-01-01T00:00:00+08:00"
    if not data.get("updatedAt"):
        data["updatedAt"] = datetime.now().isoformat()
    
    # 确保 meta
    if "meta" not in data:
        data["meta"] = {}
    if "methodology" not in data["meta"]:
        data["meta"]["methodology"] = "cms-sop"
    
    # 清理不必要的字段（保留原始数据）
    # 只确保必填字段存在
    
    save_state(state_path, data)
    
    if old_id != dir_name:
        return old_id, dir_name
    return None


def main():
    print("=" * 60)
    print("EAM 项目修复工具 v2")
    print("=" * 60)
    
    projects = sorted(EAM_ROOT.glob("SOP-*/"))
    print(f"找到 {len(projects)} 个项目\n")
    
    fixed_count = 0
    renamed_count = 0
    
    for proj in projects:
        state_path = proj / "state.json"
        if not state_path.exists():
            print(f"❌ {proj.name}: 无 state.json")
            continue
        
        print(f"处理: {proj.name}")
        result = fix_state_json(state_path)
        
        if result:
            old, new = result
            print(f"  ✅ ID 更新: {old} → {new}")
            renamed_count += 1
        else:
            print(f"  ✅ state.json 已修复")
        
        fixed_count += 1
        
        # 显示修复后的关键信息
        data = load_state(state_path)
        print(f"     ID: {data['id']}")
        print(f"     状态: {data['status']} / {data['stage']}")
        print()
    
    print("=" * 60)
    print(f"完成! 修复 {fixed_count} 个项目，ID 更新 {renamed_count} 个")
    print("=" * 60)


if __name__ == "__main__":
    main()

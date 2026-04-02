#!/usr/bin/env python3
"""修复项目 ID 和 state.json"""

import json
import re
from pathlib import Path

EAM_ROOT = Path.home() / ".openclaw" / "EAM-projects"

# EAM 规范
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


def generate_new_id(title, date_prefix):
    """生成符合规范的项目 ID"""
    # 从标题提取有意义的英文/拼音作为 name
    name = extract_name(title)
    new_id = f"{date_prefix}-{name}"
    return new_id


def extract_name(title):
    """从标题提取名称"""
    # 移除常见前缀和后缀
    title = title.replace("研究", "").replace("调研", "").replace("项目", "").replace("分析", "")
    title = title.replace("Skill", "").replace("skill", "").replace("SOP", "")
    title = title.replace("Agent", "").replace("agent", "")
    title = re.sub(r'[`\uf700-\uf7ff]', '', title)  # 移除 emoji
    title = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title)  # 非字母数字转 -
    title = re.sub(r'-+', '-', title)  # 多个 - 合并
    title = title.strip('-')[:20]  # 限制长度
    if not title:
        title = "project"
    return title


def fix_state_json(state_path, new_id=None):
    """修复 state.json"""
    data = load_state(state_path)
    original_id = data.get("id", "")
    
    # 生成新 ID
    if new_id is None:
        # 从当前目录名提取
        new_id = state_path.parent.name
    
    data["id"] = new_id
    
    # 确保必填字段
    if "title" not in data or not data["title"]:
        data["title"] = new_id
    if "mode" not in data or data["mode"] not in MODE_ENUM:
        data["mode"] = "full"
    if "owner" not in data or not data["owner"]:
        data["owner"] = "evan"
    
    # 验证 status
    if data.get("status") not in STATUS_ENUM:
        data["status"] = "DISCUSSING"
    
    # 验证 stage
    if data.get("stage") not in STAGE_ENUM:
        data["stage"] = "TARGET"
    
    # 确保时间字段存在
    if "createdAt" not in data or not data["createdAt"]:
        data["createdAt"] = "2026-01-01T00:00:00+08:00"
    if "updatedAt" not in data or not data["updatedAt"]:
        from datetime import datetime
        data["updatedAt"] = datetime.now().isoformat()
    
    # 确保 meta 存在
    if "meta" not in data:
        data["meta"] = {}
    data["meta"]["methodology"] = data["meta"].get("methodology", "cms-sop")
    
    save_state(state_path, data)
    return original_id, new_id


def fix_project(project_dir):
    """修复单个项目"""
    project_dir = Path(project_dir)
    state_path = project_dir / "state.json"
    
    if not state_path.exists():
        print(f"  ⚠️  无 state.json，跳过")
        return None
    
    old_id, new_id = fix_state_json(state_path)
    
    if old_id != new_id:
        # 需要重命名目录
        parent = project_dir.parent
        new_dir = parent / new_id
        if new_dir.exists():
            print(f"  ⚠️  目标目录已存在: {new_id}")
            return None
        project_dir.rename(new_dir)
        return (old_id, new_id)
    
    return None


def main():
    print("=" * 60)
    print("EAM 项目修复工具")
    print("=" * 60)
    
    # 收集所有项目
    projects = list(EAM_ROOT.glob("SOP-*/"))
    print(f"找到 {len(projects)} 个项目\n")
    
    # 检查重复 ID
    id_map = {}
    for proj in projects:
        state_path = proj / "state.json"
        if state_path.exists():
            data = load_state(state_path)
            pid = data.get("id", "N/A")
            if pid not in id_map:
                id_map[pid] = []
            id_map[pid].append(proj.name)
    
    # 找出重复
    duplicates = {k: v for k, v in id_map.items() if len(v) > 1}
    
    if duplicates:
        print("发现重复 ID:")
        for oid, names in duplicates.items():
            print(f"  {oid}: {len(names)} 个")
            for n in names:
                print(f"    - {n}")
        print()
    
    # 修复每个项目
    renamed = []
    for proj in sorted(projects):
        print(f"处理: {proj.name}")
        result = fix_project(proj)
        if result:
            old, new = result
            renamed.append((old, new))
            print(f"  ✅ 重命名: {old} → {new}")
        else:
            print(f"  ✅ 已修复 state.json")
    
    print()
    print("=" * 60)
    print(f"完成! 修复 {len(projects)} 个项目，重命名 {len(renamed)} 个")
    if renamed:
        print("\n重命名列表:")
        for old, new in renamed:
            print(f"  {old} → {new}")
    print("=" * 60)


if __name__ == "__main__":
    main()

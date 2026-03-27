#!/bin/bash
#
# Good-Memory: Tracker 维护脚本 v1.1.1
# - 修复 get_current_session()：按 chat_id + session_key 精确匹配 active session
# - 修复 update 调用时机：detect mode 自动检测是否需要更新
#

set -e

TRACKER_FILE="/root/.openclaw/workspace/session-tracker.json"
SESSIONS_BASE="/root/.openclaw/agents"

# 从 session 文件中提取 session_key（用于精确匹配）
get_session_key_from_file() {
    local filepath="$1"
    # session 文件是 jsonl，第一行是 metadata，格式：{"role":"system","content":"...\"session_key\":\"agent:xxx\"...
    local content=$(head -1 "$filepath" 2>/dev/null || echo "")
    if [[ -n "$content" ]]; then
        echo "$content" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('session_key',''))" 2>/dev/null || echo ""
    fi
}

# 获取当前 session 信息（按 chat_id 精确匹配）
get_current_session() {
    local agent="$1"
    local chat_id="$2"
    local sessions_dir="${SESSIONS_BASE}/${agent}/sessions"

    if [[ ! -d "$sessions_dir" ]]; then
        echo ""
        return
    fi

    local target_key="agent:${agent}:feishu:direct:${chat_id}"
    local target_key_alt="agent:${agent}:feishu:unknown:${chat_id}"

    # 遍历所有非 .reset. 文件，找匹配的 session_key
    for f in "${sessions_dir}"/*.jsonl; do
        [[ -f "$f" ]] || continue
        [[ "$f" == *.reset.* ]] && continue

        local sk=$(get_session_key_from_file "$f")
        if [[ "$sk" == "$target_key" || "$sk" == "$target_key_alt" ]]; then
            echo "$f"
            return
        fi
    done

    # fallback：按时间戳找最新的非 .reset. 文件
    local active_file=$(ls -t "${sessions_dir}"/*.jsonl 2>/dev/null | grep -v ".reset." | head -1 || echo "")
    echo "$active_file"
}

# 更新 tracker
update_tracker() {
    local agent="$1"
    local chat_id="$2"

    [[ -z "$agent" || -z "$chat_id" ]] && { echo "Usage: update_tracker <agent> <chat_id>"; return 1; }

    local current_session=$(get_current_session "$agent" "$chat_id")

    if [[ -z "$current_session" ]]; then
        echo "No active session found for agent: $agent chat_id: $chat_id"
        return 1
    fi

    # 如果 tracker 文件不存在，创建一个基础结构
    if [[ ! -f "$TRACKER_FILE" ]]; then
        cat > "$TRACKER_FILE" << 'EOF'
{
  "description": "Session tracker - maps each agent+chat to their session files",
  "last_updated": "",
  "agents": {}
}
EOF
    fi

    # 使用 python 来更新 JSON（更可靠）
    python3 << PYEOF
import json
import os
import subprocess
from datetime import datetime, timezone

tracker_file = "$TRACKER_FILE"
agent = "$agent"
chat_id = "$chat_id"
current_session = "$current_session"

def get_file_birth(filepath):
    """获取文件创建时间（birth time）"""
    try:
        result = subprocess.run(
            ['stat', filepath],
            capture_output=True
        )
        stdout_str = result.stdout.decode() if result.stdout else ''
        for line in stdout_str.split('\n'):
            line_stripped = line.strip()
            if 'Birth:' in line_stripped:
                birth_str = line_stripped.split('Birth:')[1].strip()
                parts = birth_str.rsplit(' ', 1)
                if len(parts) >= 1:
                    time_part = parts[0].strip()
                    if '.' in time_part:
                        date_time, nanoseconds = time_part.rsplit('.', 1)
                        microseconds = nanoseconds[:6].ljust(6, '0')
                        time_part = f"{date_time}.{microseconds}"
                    dt = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S.%f')
                    dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
    except Exception:
        pass
    return ""

def get_file_uuid(filepath):
    """从文件名提取 UUID 前缀"""
    basename = os.path.basename(filepath)
    uuid_part = basename.split('.jsonl')[0]
    return uuid_part

def get_reset_time_from_filename(filepath):
    """从 .reset.<filename> 文件名中提取重置时间（文件名格式：uuid.jsonl.reset.ISO时间戳）
    例如：uuid.jsonl.reset.2026-03-27T03-23-43.809Z
    注意：时间部分用 '-' 分隔（如 03-23-43），需要转换为标准 ISO 格式
    """
    basename = os.path.basename(filepath)
    if '.reset.' in basename:
        parts = basename.split('.reset.')
        if len(parts) >= 2:
            timestamp_str = parts[1]
            try:
                # 时间戳格式：YYYY-MM-DDTHH-MM-SS.ffffffZ
                # 分离日期和时间，时间部分的 '-' 替换为 ':'
                date_part, time_with_tz = timestamp_str.split('T')
                # time_with_tz 格式 HH-MM-SS.ffffffZ
                time_part = time_with_tz[:-1]  # 去掉末尾 Z
                time_part_fixed = time_part.replace('-', ':')  # HH:MM:SS.ffffff
                iso_str = f"{date_part}T{time_part_fixed}+00:00"
                dt = datetime.fromisoformat(iso_str)
                return dt.isoformat()
            except Exception:
                pass
    return ""

# 读取 tracker
with open(tracker_file, 'r') as f:
    tracker = json.load(f)

# 确保 agent 和 chat_id 存在
if agent not in tracker["agents"]:
    tracker["agents"][agent] = {}
if chat_id not in tracker["agents"][agent]:
    tracker["agents"][agent][chat_id] = {
        "active": "",
        "active_uuid": "",
        "session_key": f"agent:{agent}:feishu:unknown:{chat_id}",
        "history": []
    }

# 检查是否需要把旧 active 移到 history
old_active = tracker["agents"][agent][chat_id].get("active", "")
old_uuid = tracker["agents"][agent][chat_id].get("active_uuid", "")
current_uuid = get_file_uuid(current_session)

if old_active and old_uuid and current_uuid != old_uuid:
    # UUID 前缀改变了，说明发生了 reset
    dir_path = os.path.dirname(old_active)
    
    # 查找重命名后的 .reset. 文件（格式：uuid.jsonl.reset.timestamp）
    if os.path.exists(dir_path):
        # 搜索包含 old_uuid + ".jsonl.reset." 的文件
        reset_candidates = [f for f in os.listdir(dir_path) 
                          if old_uuid + '.jsonl.reset.' in f]
        if reset_candidates:
            # 按时间排序，取最新的
            reset_candidates.sort(reverse=True)
            reset_file = os.path.join(dir_path, reset_candidates[0])
            
            # 获取文件创建时间（birth time）
            file_created = get_file_birth(reset_file)
            # 从文件名提取真正的重置时间
            reset_time = get_reset_time_from_filename(reset_file)
            if not reset_time:
                reset_time = datetime.now(timezone.utc).isoformat()
            
            tracker["agents"][agent][chat_id]["last_history"] = {
                "file": reset_file,
                "ended_at": reset_time,
                "created_at": file_created
            }
            
            # history 数组保留记录（不用于恢复）
            tracker["agents"][agent][chat_id]["history"].insert(0, {
                "file": reset_file,
                "ended_at": reset_time,
                "created_at": file_created
            })
    
    # 写入当前 active session
    tracker["agents"][agent][chat_id]["active"] = current_session
    tracker["agents"][agent][chat_id]["active_uuid"] = current_uuid
    tracker["agents"][agent][chat_id]["active_created_at"] = get_file_birth(current_session)
    tracker["last_updated"] = datetime.now(timezone.utc).isoformat()

# 写回 tracker
with open(tracker_file, 'w') as f:
    json.dump(tracker, f, indent=2, ensure_ascii=False)

print(f"Updated tracker: {agent}/{chat_id}")
print(f"active: {current_session}")
print(f"active_uuid: {current_uuid}")
PYEOF

    echo "Tracker updated successfully"
}

# 验证 session 是否发生过 reset
verify_session() {
    local agent="$1"
    local chat_id="$2"

    python3 << PYEOF
import json
import os
import subprocess
from datetime import datetime, timezone

tracker_file = "$TRACKER_FILE"
agent = "$agent"
chat_id = "$chat_id"

def get_file_birth(filepath):
    """获取文件创建时间（birth time）"""
    try:
        result = subprocess.run(
            ['stat', filepath],
            capture_output=True
        )
        stdout_str = result.stdout.decode() if result.stdout else ''
        for line in stdout_str.split('\n'):
            line_stripped = line.strip()
            if 'Birth:' in line_stripped:
                birth_str = line_stripped.split('Birth:')[1].strip()
                parts = birth_str.rsplit(' ', 1)
                if len(parts) >= 1:
                    time_part = parts[0].strip()
                    if '.' in time_part:
                        date_time, nanoseconds = time_part.rsplit('.', 1)
                        microseconds = nanoseconds[:6].ljust(6, '0')
                        time_part = f"{date_time}.{microseconds}"
                    dt = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S.%f')
                    dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
    except Exception:
        pass
    return ""

def get_file_uuid(filepath):
    """从文件名提取 UUID 前缀"""
    basename = os.path.basename(filepath)
    uuid_part = basename.split('.jsonl')[0]
    return uuid_part

try:
    with open(tracker_file, 'r') as f:
        tracker = json.load(f)

    if agent not in tracker["agents"] or chat_id not in tracker["agents"][agent]:
        print("RESET_DETECTED: no tracker entry")
        print("last_history: ")
        print("last_session_created: ")
        exit(0)

    info = tracker["agents"][agent][chat_id]
    stored_active = info.get("active", "")
    stored_uuid = info.get("active_uuid", "")
    stored_created_at = info.get("active_created_at", "")
    last_history = info.get("last_history", {})
    history = info.get("history", [])

    def print_last_history():
        # 优先使用 last_history，否则 fallback 到 history[0]
        if last_history:
            print(f"last_history: {last_history.get('file', '')}")
            print(f"last_session_created: {last_history.get('created_at', '')}")
        elif history:
            print(f"last_history: {history[0].get('file', '')}")
            print(f"last_session_created: {history[0].get('created_at', '')}")
        else:
            print("last_history: ")
            print("last_session_created: ")

    if not stored_active or not os.path.exists(stored_active):
        print("RESET_DETECTED: active file not found")
        print_last_history()
        exit(0)

    # 获取当前文件的 UUID 前缀
    current_uuid = get_file_uuid(stored_active)

    # 首先比对 UUID 前缀（主要依据，因为 UUID 全局唯一）
    if stored_uuid and current_uuid != stored_uuid:
        print("RESET_DETECTED: UUID mismatch")
        print(f"stored_uuid: {stored_uuid}")
        print(f"current_uuid: {current_uuid}")
        print_last_history()
        exit(0)

    # UUID 相同，再比对 birth time（辅助验证，防止 UUID 碰撞）
    current_birth = get_file_birth(stored_active)

    if current_birth != stored_created_at:
        print("RESET_DETECTED: birth time mismatch")
        print(f"stored: {stored_created_at}")
        print(f"current: {current_birth}")
        print_last_history()
        exit(0)
    else:
        print("OK: session unchanged")
        print("last_history: ")
        print("last_session_created: ")
except Exception as e:
    print(f"ERROR: {e}")
    print("RESET_DETECTED: error checking session")
PYEOF
}

# 从 tracker 读取上一次 session
get_last_session() {
    local agent="$1"
    local chat_id="$2"

    python3 << PYEOF
import json

tracker_file = "$TRACKER_FILE"
agent = "$agent"
chat_id = "$chat_id"

try:
    with open(tracker_file, 'r') as f:
        tracker = json.load(f)

    if agent in tracker["agents"] and chat_id in tracker["agents"][agent]:
        info = tracker["agents"][agent][chat_id]
        history = info.get("history", [])
        if history:
            entry = history[0]
            print(f"file: {entry.get('file', '')}")
            print(f"created_at: {entry.get('created_at', '')}")
        else:
            print("file: ")
            print("created_at: ")
    else:
        print("file: ")
        print("created_at: ")
except Exception as e:
    print(f"error: {e}")
    print("file: ")
    print("created_at: ")
PYEOF
}

# 主入口
main() {
    [[ $# -lt 1 ]] && { echo "Usage: $0 <command> [options]"; echo "Commands: update, get-last, verify, detect"; exit 1; }

    local command="$1"; shift

    case "$command" in
        update)
            [[ $# -lt 2 ]] && { echo "Usage: $0 update <agent> <chat_id>"; exit 1; }
            update_tracker "$1" "$2"
            ;;
        get-last)
            [[ $# -lt 2 ]] && { echo "Usage: $0 get-last <agent> <chat_id>"; exit 1; }
            get_last_session "$1" "$2"
            ;;
        verify)
            [[ $# -lt 2 ]] && { echo "Usage: $0 verify <agent> <chat_id>"; exit 1; }
            verify_session "$1" "$2"
            ;;
        detect)
            # 检测 + 自动更新二合一，用于 session 启动时调用
            # 流程：检查 UUID -> 如有 reset 则设置 last_history 并更新 active -> 读取 last_history 最后 50 条
            [[ $# -lt 2 ]] && { echo "Usage: $0 detect <agent> <chat_id>"; exit 1; }
            
            python3 << PYEOF
import json
import os
import subprocess
from datetime import datetime, timezone

tracker_file = "/root/.openclaw/workspace/session-tracker.json"
sessions_base = "/root/.openclaw/agents"
agent = "$1"
chat_id = "$2"

def get_file_birth(filepath):
    """获取文件创建时间（birth time）"""
    try:
        result = subprocess.run(['stat', filepath], capture_output=True)
        stdout_str = result.stdout.decode() if result.stdout else ''
        for line in stdout_str.split('\n'):
            line_stripped = line.strip()
            if 'Birth:' in line_stripped:
                birth_str = line_stripped.split('Birth:')[1].strip()
                parts = birth_str.rsplit(' ', 1)
                if len(parts) >= 1:
                    time_part = parts[0].strip()
                    if '.' in time_part:
                        date_time, nanoseconds = time_part.rsplit('.', 1)
                        microseconds = nanoseconds[:6].ljust(6, '0')
                        time_part = f"{date_time}.{microseconds}"
                    dt = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S.%f')
                    dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
    except Exception:
        pass
    return ""

def get_file_uuid(filepath):
    """从文件名提取 UUID 前缀"""
    basename = os.path.basename(filepath)
    uuid_part = basename.split('.jsonl')[0]
    return uuid_part

def get_reset_time_from_filename(filepath):
    """从文件名提取重置时间"""
    basename = os.path.basename(filepath)
    if '.reset.' in basename:
        parts = basename.split('.reset.')
        if len(parts) >= 2:
            timestamp_str = parts[1]
            try:
                date_part, time_with_tz = timestamp_str.split('T')
                time_part = time_with_tz[:-1]
                time_part_fixed = time_part.replace('-', ':')
                iso_str = f"{date_part}T{time_part_fixed}+00:00"
                dt = datetime.fromisoformat(iso_str)
                return dt.isoformat()
            except Exception:
                pass
    return ""

def get_current_session_for_chat(agent, chat_id):
    """获取当前 chat_id 对应的 session 文件"""
    sessions_dir = f"{sessions_base}/{agent}/sessions"
    if not os.path.isdir(sessions_dir):
        return None
    
    # 排除 .reset. 和 .deleted. 后缀的文件
    def is_active_session(f):
        return not any(s in f for s in ('.reset.', '.deleted.', '.lock'))
    
    # 先尝试精确匹配 session_key（session_key 在系统提示里，不在文件顶层，跳过）
    # 直接用 fallback：找最新修改的非特殊后缀文件
    
    # fallback: 按修改时间找最新的非 reset/deleted 文件
    files = [os.path.join(sessions_dir, f) for f in os.listdir(sessions_dir) 
             if is_active_session(f) and f.endswith('.jsonl')]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]

def read_last_lines(filepath, n=20):
    """读取文件最后 n 行"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return lines[-n:]
    except:
        return []

# 主逻辑
current_session = get_current_session_for_chat(agent, chat_id)

if not current_session or not os.path.exists(current_session):
    print("RESET_DETECTED: no current session found")
    print("last_history: ")
    print("last_session_created: ")
    exit(0)

current_uuid = get_file_uuid(current_session)
current_birth = get_file_birth(current_session)

# 读取 tracker
with open(tracker_file, 'r') as f:
    tracker = json.load(f)

if agent not in tracker.get("agents", {}):
    tracker["agents"][agent] = {}
if chat_id not in tracker["agents"][agent]:
    tracker["agents"][agent][chat_id] = {
        "chat_type": "direct",
        "active": "",
        "active_uuid": "",
        "active_created_at": "",
        "session_key": f"agent:{agent}:feishu:direct:{chat_id}",
        "history": []
    }

info = tracker["agents"][agent][chat_id]
stored_active = info.get("active", "")
stored_uuid = info.get("active_uuid", "")
stored_birth = info.get("active_created_at", "")

# UUID 比对
if stored_uuid and current_uuid != stored_uuid:
    # Reset 发生了！
    print("RESET_DETECTED: UUID mismatch")
    print(f"stored_uuid: {stored_uuid}")
    print(f"current_uuid: {current_uuid}")
    
    # 找旧的 .reset.* 文件
    old_uuid = stored_uuid
    old_active = stored_active
    reset_file = None
    reset_file_created = ""
    reset_time = ""
    
    if old_active:
        dir_path = os.path.dirname(old_active)
        search_str = old_uuid + '.jsonl.reset.'
        if os.path.exists(dir_path):
            candidates = []
            for f in os.listdir(dir_path):
                if search_str in f:
                    filepath = os.path.join(dir_path, f)
                    birth = get_file_birth(filepath)
                    ts = get_reset_time_from_filename(filepath) or birth
                    candidates.append((filepath, birth, ts))
            
            if candidates:
                # 按 birth time 排序，选最接近 stored_birth 的那个
                # stored_birth 是旧 session 的创建时间，reset 文件的 birth time 应该 <= stored_birth
                # 取 birth <= stored_birth 且最接近的
                valid = [(f, b, t) for f, b, t in candidates if b and b <= stored_birth]
                if valid:
                    valid.sort(key=lambda x: x[1], reverse=True)  # 按 birth 降序，取最接近 stored_birth 的
                    reset_file, reset_file_created, reset_time = valid[0]
                else:
                    # Fallback: 取时间戳最新的
                    candidates.sort(key=lambda x: x[2], reverse=True)
                    reset_file, reset_file_created, reset_time = candidates[0]
    
    if not reset_file or not os.path.exists(reset_file):
        print("last_history: ")
        print("last_session_created: ")
    else:
        print(f"last_history: {reset_file}")
        print(f"last_session_created: {reset_file_created}")
        
        # 更新 last_history 和 history
        info["last_history"] = {
            "file": reset_file,
            "created_at": reset_file_created,
            "ended_at": reset_time or datetime.now(timezone.utc).isoformat()
        }
        
        # 插入到 history 头部
        info["history"].insert(0, {
            "file": reset_file,
            "created_at": reset_file_created,
            "ended_at": reset_time or datetime.now(timezone.utc).isoformat()
        })
        
        # 更新 active
        info["active"] = current_session
        info["active_uuid"] = current_uuid
        info["active_created_at"] = current_birth
        info["session_key"] = f"agent:{agent}:feishu:direct:{chat_id}"
        
        tracker["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        with open(tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2, ensure_ascii=False)
        
        # 读取 last_history 最后 50 行输出
        last_lines = read_last_lines(reset_file, 20)
        print("---LAST_HISTORY_LINES---")
        for line in last_lines:
            print(line.rstrip())

elif stored_birth and current_birth != stored_birth:
    # Birth time 变了但 UUID 相同（少见）
    print("RESET_DETECTED: birth time mismatch")
    print(f"stored: {stored_birth}")
    print(f"current: {current_birth}")
    print("last_history: ")
    print("last_session_created: ")
else:
    # Session 没变
    print("OK: session unchanged")
    print("last_history: ")
    print("last_session_created: ")
    
    # 更新 tracker 确保记录最新
    info["active"] = current_session
    info["active_uuid"] = current_uuid
    info["active_created_at"] = current_birth
    tracker["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    with open(tracker_file, 'w') as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)

PYEOF
            ;;
        *)
            echo "Unknown command: $command"
            echo "Commands: update, get-last, verify, detect"
            exit 1
            ;;
    esac
}

main "$@"

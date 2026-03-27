#!/bin/bash
#
# Good-Memory: Session 历史记录恢复脚本（新版本）
# 原理：Session 重置后文件名自动改为 .reset.时间戳.jsonl
# 用法: recovery.sh <command> [options]
#

set -e

SESSIONS_BASE="/root/.openclaw/agents"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error() { echo -e "${RED}ERROR: $1${NC}" >&2; exit 1; }
info() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}WARNING: $1${NC}"; }

# 找到最新的 .reset. 文件
find_latest_reset() {
    local agent="$1"
    local sessions_dir="${SESSIONS_BASE}/${agent}/sessions"

    [[ -d "$sessions_dir" ]] || { echo ""; return 0; }

    # 找所有 .reset.* 文件（即 .jsonl.reset.时间戳 格式），按修改时间倒序，取最新的
    local latest_file=$(ls -t "${sessions_dir}"/*.jsonl.reset.* 2>/dev/null | head -1 || echo "")

    echo "$latest_file"
}

# 列出所有 .reset. 文件（按时间倒序）
list_reset_files() {
    local agent="$1"
    local sessions_dir="${SESSIONS_BASE}/${agent}/sessions"

    [[ -d "$sessions_dir" ]] || { echo "[]"; return 0; }

    ls -t "${sessions_dir}"/*.jsonl.reset.* 2>/dev/null || echo ""
}

# 读取指定文件的最后 N 行
read_tail() {
    local file="$1"
    local lines="${2:-50}"

    [[ -z "$file" || ! -f "$file" ]] && { echo "File not found: $file"; return 1; }

    tail -n "$lines" "$file" | while IFS= read -r line; do
        # 提取 timestamp 和 content
        local timestamp=$(echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('timestamp',''))" 2>/dev/null || echo "")
        local msg_type=$(echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('type',''))" 2>/dev/null || echo "")

        if [[ "$msg_type" == "message" ]]; then
            local msg=$(echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(json.dumps(d.get('message',{})))" 2>/dev/null)
            local role=$(echo "$msg" | python3 -c "import sys,json; m=json.load(sys.stdin); print(m.get('role',''))" 2>/dev/null || echo "")
            local ct=$(echo "$msg" | python3 -c "import sys,json; m=json.load(sys.stdin); print(json.dumps(m.get('content','')))" 2>/dev/null)

            local text=""
            if [[ "$ct" == *"text"* ]]; then
                text=$(echo "$ct" | python3 -c "import sys,json; ct=json.load(sys.stdin); text='';
if isinstance(ct,list):
    for c in ct:
        if isinstance(c,dict) and c.get('type')=='text': text=c.get('text',''); break
elif isinstance(ct,str): text=ct
print(text[:300])" 2>/dev/null || echo "")
            elif [[ "$ct" == *"toolResult"* || "$ct" == *"tool_use"* ]]; then
                text="[tool result]"
            fi

            [[ -n "$text" ]] && echo "[${timestamp}] [${role}] ${text}"
        elif [[ -n "$msg_type" ]]; then
            echo "[${timestamp}] [${msg_type}]"
        fi
    done
}

# 主入口
main() {
    [[ $# -lt 1 ]] && { echo "Usage: $0 <command> [options]"; echo "Commands: latest, read, read-file, list"; exit 1; }

    local command="$1"; shift

    case "$command" in
        latest)
            [[ $# -lt 1 ]] && { echo "Usage: $0 latest <agent>"; exit 1; }
            find_latest_reset "$1"
            ;;
        read)
            [[ $# -lt 1 ]] && { echo "Usage: $0 read <agent> [--lines N]"; exit 1; }
            local agent="$1"; shift
            local lines=100
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --lines) lines="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            local latest_file=$(find_latest_reset "$agent")
            if [[ -n "$latest_file" ]]; then
                read_tail "$latest_file" "$lines"
            else
                echo "No reset session found for agent: $agent"
            fi
            ;;
        read-file)
            [[ $# -lt 1 ]] && { echo "Usage: $0 read-file <file> [--lines N]"; exit 1; }
            local file="$1"; shift
            local lines=100
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --lines) lines="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            read_tail "$file" "$lines"
            ;;
        list)
            [[ $# -lt 1 ]] && { echo "Usage: $0 list <agent>"; exit 1; }
            list_reset_files "$1"
            ;;
        *)
            echo "Unknown command: $command"
            echo "Commands: latest, read, read-file, list"
            exit 1
            ;;
    esac
}

main "$@"

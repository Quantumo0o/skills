"""
查询 conversations.db
所需环境变量:
  OPENCLAW_WORKSPACE  - OpenClaw workspace 路径（默认从父级目录推断）
  CONVERSATIONS_DB    - 数据库路径（默认 {workspace}/conversations.db）

用法:
  python query_conversations.py stats              # 总览统计
  python query_conversations.py recent [n]         # 最近 n 条（默认10）
  python query_conversations.py random [n]         # 随机 n 条（默认5）
  python query_conversations.py search <关键词>     # 关键词搜索
  python query_conversations.py session <key>      # 某 session 的消息
  python query_conversations.py after <ts_ms>      # 某时间之后的记录
"""
import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime

def get_workspace():
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws:
        return Path(ws)
    script_dir = Path(__file__).resolve().parent
    # 常见 skill 安装路径: {workspace}/skills/conversations/scripts
    for parent in [script_dir.parent, script_dir.parent.parent]:
        if parent and (parent / "openclaw.json").exists():
            return parent
    # 常见 workspace 位置
    home = Path.home()
    for c in [home / ".openclaw" / "workspace", home / ".openclaw"]:
        if (c / "openclaw.json").exists():
            return c
    raise RuntimeError("找不到 OpenClaw workspace，请设置 OPENCLAW_WORKSPACE 环境变量")

workspace = get_workspace()
DB_PATH = os.environ.get("CONVERSATIONS_DB", str(workspace / "conversations.db"))

sys.stdout.reconfigure(encoding="utf-8")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def ts_to_str(ms):
    return datetime.fromtimestamp(ms/1000).strftime("%m-%d %H:%M")

def print_msg(role, content, ts, session_key=""):
    prefix = f"[{ts_to_str(ts)}] {role}"
    if session_key:
        prefix += f" ({session_key[-8:]})"
    print(f"{prefix}:")
    print(f"  {content[:300]}{'...' if len(content) > 300 else ''}")
    print()

action = sys.argv[1] if len(sys.argv) > 1 else "stats"
arg = sys.argv[2] if len(sys.argv) > 2 else ""

if action == "stats":
    c.execute("SELECT COUNT(*), role FROM chunks GROUP BY role")
    for count, role in c.fetchall():
        print(f"  {role}: {count}")
    c.execute("SELECT MIN(created_at), MAX(created_at) FROM chunks")
    mn, mx = c.fetchone()
    if mn:
        print(f"  时间范围: {ts_to_str(mn)} ~ {ts_to_str(mx)}")

elif action == "recent":
    n = int(arg) if arg else 10
    c.execute("SELECT role, content, created_at, session_key FROM chunks ORDER BY created_at DESC LIMIT ?", (n,))
    for role, content, ts, sk in c.fetchall():
        print_msg(role, content, ts, sk)

elif action == "search":
    if not arg:
        print("用法: search <关键词>")
    else:
        keyword = f"%{arg}%"
        c.execute("SELECT role, content, created_at, session_key FROM chunks WHERE content LIKE ? ORDER BY created_at DESC LIMIT 20", (keyword,))
        rows = c.fetchall()
        print(f"找到 {len(rows)} 条:")
        for role, content, ts, sk in rows:
            print_msg(role, content, ts, sk)

elif action == "session":
    if not arg:
        print("用法: session <session_key>")
    else:
        key = arg if arg.startswith("agent:") else f"%{arg}%"
        c.execute("SELECT role, content, created_at, session_key FROM chunks WHERE session_key LIKE ? ORDER BY seq", (key,))
        rows = c.fetchall()
        print(f"session [{arg}] 共 {len(rows)} 条:")
        for role, content, ts, sk in rows:
            print_msg(role, content, ts, sk)

elif action == "random":
    n = int(arg) if arg else 5
    c.execute("SELECT role, content, created_at, session_key FROM chunks ORDER BY RANDOM() LIMIT ?", (n,))
    for role, content, ts, sk in c.fetchall():
        print_msg(role, content, ts, sk)

elif action == "after":
    if not arg:
        print("用法: after <timestamp_ms>")
    else:
        ts = int(arg)
        c.execute("SELECT role, content, created_at, session_key FROM chunks WHERE created_at > ? ORDER BY created_at LIMIT 20", (ts,))
        rows = c.fetchall()
        print(f"{ts_to_str(ts)} 之后共 {len(rows)} 条:")
        for role, content, ts, sk in rows:
            print_msg(role, content, ts, sk)

else:
    print(f"未知命令: {action}")
    print(__doc__)

conn.close()

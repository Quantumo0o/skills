"""
导入 sessions JSONL 文件到 conversations.db
所需环境变量:
  OPENCLAW_WORKSPACE  - OpenClaw workspace 路径（默认从父级目录推断）
  SESSIONS_DIR        - sessions 目录（默认 {workspace}/agents/main/sessions）
  CONVERSATIONS_DB    - 数据库路径（默认 {workspace}/conversations.db）

用法: python import_sessions.py [--dry-run]
"""
import json
import sqlite3
import uuid
import hashlib
import sys
import os
from pathlib import Path
from datetime import datetime

def get_workspace():
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws:
        return Path(ws)
    script_dir = Path(__file__).resolve().parent
    for parent in [script_dir.parent, script_dir.parent.parent]:
        if parent and (parent / "openclaw.json").exists():
            return parent
    home = Path.home()
    for c in [home / ".openclaw" / "workspace", home / ".openclaw"]:
        if (c / "openclaw.json").exists():
            return c
    raise RuntimeError("找不到 OpenClaw workspace，请设置 OPENCLAW_WORKSPACE 环境变量")

workspace = get_workspace()
SESSIONS_DIR = os.environ.get("SESSIONS_DIR", str(workspace / "agents" / "main" / "sessions"))
DB_PATH = os.environ.get("CONVERSATIONS_DB", str(workspace / "conversations.db"))

sys.stdout.reconfigure(encoding="utf-8")

def get_all_session_files():
    for f in Path(SESSIONS_DIR).glob("*.jsonl*"):
        if ".deleted" in f.name:
            continue
        yield f

def parse_session_file(filepath):
    for line in filepath.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") == "message":
            yield record

def extract_text_content(content_array):
    texts = []
    for block in content_array:
        if isinstance(block, dict) and block.get("type") == "text":
            t = block.get("text", "")
            if t:
                texts.append(t)
    return "\n".join(texts)

def make_content_hash(content: str) -> str:
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def make_turn_id(timestamp_ms: int, role: str, seq: int) -> str:
    return f"{timestamp_ms}_{role}_{seq // 2}"

def session_key_from_file(filepath: Path) -> str:
    name = filepath.name
    uuid_part = name.replace(".jsonl", "").split(".reset")[0].split(".deleted")[0]
    return f"agent:main:session:{uuid_part}"

def main(dry_run=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content_hash FROM chunks WHERE content_hash IS NOT NULL")
    existing_hashes = set(row[0] for row in c.fetchall())
    print(f"现有 {len(existing_hashes)} 条 content_hash")
    print(f"数据库: {DB_PATH}")
    print(f"Sessions: {SESSIONS_DIR}")

    files = list(get_all_session_files())
    print(f"找到 {len(files)} 个 session 文件")

    total_written = 0
    total_skipped = 0

    for filepath in files:
        session_key = session_key_from_file(filepath)
        messages = list(parse_session_file(filepath))
        print(f"[{session_key[-8:]}] {len(messages)} 条 message")

        seq = 0
        for record in messages:
            msg = record.get("message", {})
            role = msg.get("role", "")
            content = extract_text_content(msg.get("content", []))

            if not content.strip() or role == "toolResult":
                continue

            ts = record.get("timestamp", "")
            try:
                created_at = int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() * 1000) if ts else 0
            except Exception:
                created_at = 0

            content_hash = make_content_hash(content)
            if content_hash in existing_hashes:
                total_skipped += 1
                continue

            chunk_id = str(uuid.uuid4())
            turn_id = make_turn_id(created_at, role, seq)
            existing_hashes.add(content_hash)

            if not dry_run:
                c.execute("""
                    INSERT INTO chunks (id, session_key, turn_id, seq, role, content, created_at, updated_at, content_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (chunk_id, session_key, turn_id, seq, role, content, created_at, created_at, content_hash))
            total_written += 1
            seq += 1

    if not dry_run:
        conn.commit()
    conn.close()
    print(f"\n{'[DRY RUN] ' if dry_run else ''}完成: 新写入 {total_written} 条, 跳过 {total_skipped} 条")

if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)

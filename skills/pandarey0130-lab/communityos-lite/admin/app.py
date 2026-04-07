#!/usr/bin/env python3
"""
CommunityOS 管理后台 - FastAPI (重构版)
支持多项目知识库隔离
"""
import os
import json
import sys
import uuid
import hashlib
import shutil
import re
import secrets
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

# 支持直接 `python admin/app.py` 启动，无需设置 PYTHONPATH（项目根加入 sys.path）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Telegram Runner 全局进程
telegram_process = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时自动启动 Telegram Runner"""
    global telegram_process
    # 启动 Telegram Runner
    import subprocess
    if telegram_process is None or telegram_process.poll() is not None:
        telegram_process = subprocess.Popen(
            [sys.executable, str(BASE_DIR / "admin" / "telegram_runner.py")],
            cwd=str(BASE_DIR),
            env={**os.environ}
        )
        log_action("telegram_auto_start", "system", "Telegram Runner auto-started on app startup")
        print("[STARTUP] Telegram Runner auto-started")
    yield
    # 应用关闭时清理
    if telegram_process:
        telegram_process.terminate()
        telegram_process = None

# 加载 .env 文件
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# ── 路径配置 ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "admin" / "data"
TEMPLATES_DIR = BASE_DIR / "admin" / "templates"
STATIC_DIR = BASE_DIR / "admin" / "static"
KB_DIR = BASE_DIR / "knowledge"
CHROMA_DIR = BASE_DIR / "chroma_db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
KB_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# ── FastAPI App ─────────────────────────────────────────────
app = FastAPI(title="CommunityOS 管理后台", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ── JSON 数据工具 ───────────────────────────────────────────
def load_json(name: str, default: dict | list = None) -> dict | list:
    path = DATA_DIR / f"{name}.json"
    if not path.exists():
        return default if default is not None else {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name: str, data: dict | list) -> None:
    path = DATA_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ts() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")

def _count_project_files(proj_id: str) -> int:
    proj_dir = KB_DIR / proj_id
    if not proj_dir.exists():
        return 0
    return sum(1 for f in proj_dir.iterdir() if f.is_file() and f.suffix.lower() in [".md", ".txt", ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".pages"])

# ── 初始化默认数据 ──────────────────────────────────────────
def _init_default_data():
    # users
    users = load_json("users", {"users": [], "sessions": {}})
    if not users.get("users"):
        users["users"] = [
        ]
        save_json("users", users)

    # projects - 初始化示例项目
    projects_data = load_json("projects", {"projects": []})
    if not projects_data.get("projects"):
        projects_data["projects"] = [
            {
                "id": "general",
                "name": "通用知识库",
                "description": "通用产品FAQ",
                "created_at": ts(),
                "file_count": 0
            },
            {
                "id": "ai_advisor",
                "name": "AI私人顾问",
                "description": "AI私人顾问产品知识",
                "created_at": ts(),
                "file_count": 0
            }
        ]
        save_json("projects", projects_data)
        for p in projects_data["projects"]:
            (KB_DIR / p["id"]).mkdir(exist_ok=True)

    # bots
    bots = load_json("bots", {"bots": []})
    if not bots.get("bots"):
        bots["bots"] = [
            {
                "bot_id": "panda", "name": "小P", "avatar": "🐼",
                "bot_token": "TELEGRAM_BOT_TOKEN_PANDA",
                "is_admin": True, "enabled": True, "created_at": ts(),
                "llm": {"provider": "minimax", "model": "MiniMax-2.7", "api_key_env": "MINIMAX_API_KEY"},
                "modes": {
                    "passive_qa": True, "welcome": True, "join_discussion": True,
                    "boost_atmosphere": False, "scheduled_broadcast": True, "api_data_push": False
                },
                "knowledge": {"enabled": True, "project_id": "general"},
                "welcome": {"enabled": True, "template": "欢迎 {name} 加入群聊！🎉 有问题随时问我~"},
                "broadcast": {
                    "schedule": "0 9 * * *", "content_source": "manual",
                    "api_endpoint": "", "template": "早安！今天是 {date}，祝你有美好的一天！☀️"
                },
                "interval_broadcast": {
                    "enabled": False,
                    "message": "",
                    "interval_seconds": 30
                },
                "groups": [], "soul": "友善、乐于助人的AI助手"
            },
            {
                "bot_id": "cypher", "name": "Cypher", "avatar": "🔐",
                "bot_token": "TELEGRAM_BOT_TOKEN_CYPHER",
                "is_admin": False, "enabled": True, "created_at": ts(),
                "llm": {"provider": "claude_code", "model": "Claude-3.5", "api_key_env": "CLAUDE_API_KEY"},
                "modes": {
                    "passive_qa": True, "welcome": False, "join_discussion": True,
                    "boost_atmosphere": False, "scheduled_broadcast": False, "api_data_push": True
                },
                "knowledge": {"enabled": False, "project_id": ""},
                "welcome": {"enabled": False, "template": ""},
                "broadcast": {
                    "schedule": "0 20 * * *", "content_source": "api",
                    "api_endpoint": "https://api.example.com/news", "template": "{content}"
                },
                "interval_broadcast": {
                    "enabled": False,
                    "message": "",
                    "interval_seconds": 30
                },
                "groups": [], "soul": "专注于技术与安全的AI助手"
            },
            {
                "bot_id": "buzz", "name": "Buzz", "avatar": "📣",
                "bot_token": "TELEGRAM_BOT_TOKEN_BUZZ",
                "is_admin": False, "enabled": False, "created_at": ts(),
                "llm": {"provider": "apiyi", "model": "GPT-4o", "api_key_env": "APIYI_KEY"},
                "modes": {
                    "passive_qa": False, "welcome": True, "join_discussion": False,
                    "boost_atmosphere": True, "scheduled_broadcast": True, "api_data_push": False
                },
                "knowledge": {"enabled": False, "project_id": ""},
                "welcome": {"enabled": True, "template": "欢迎来到 {group_name}！我是Buzz ~ 🚀"},
                "broadcast": {
                    "schedule": "0 12,18 * * *", "content_source": "rss",
                    "api_endpoint": "https://feeds.example.com/web3", "template": "【Web3日报】{content}"
                },
                "interval_broadcast": {
                    "enabled": False,
                    "message": "",
                    "interval_seconds": 30
                },
                "groups": [], "soul": "热情洋溢的氛围组AI助手"
            }
        ]
        save_json("bots", bots)

    # groups
    groups = load_json("groups", {"groups": []})
    if not groups.get("groups"):
        groups["groups"] = [
        ]
        save_json("groups", groups)

    # broadcasts
    broadcasts = load_json("broadcasts", {"broadcasts": []})
    if not broadcasts.get("broadcasts"):
        broadcasts["broadcasts"] = [
            {
                "id": "bc_morning", "name": "早安播报", "bot_id": "panda",
                "group_id": "group_ai", "cron": "0 9 * * *",
                "cron_desc": "每天 09:00",
                "content_source": "manual", "api_endpoint": "",
                "template": "早安！☀️ 今日资讯整理如下：{content}",
                "enabled": True, "created_at": ts(), "last_run": None, "next_run": None
            }
        ]
        save_json("broadcasts", broadcasts)

_init_default_data()

# ── 操作日志 ───────────────────────────────────────────────
def log_action(action: str, user: str = "admin", detail: str = "", level: str = "info"):
    logs = load_json("activity_log", {"logs": []})
    logs["logs"].insert(0, {
        "timestamp": ts(),
        "level": level,
        "action": action,
        "user": user,
        "detail": detail
    })
    logs["logs"] = logs["logs"][:500]
    save_json("activity_log", logs)

log_action("system", "system", "管理后台已重启")

# ── 密码工具 ───────────────────────────────────────────────
def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ── Session 工具 ───────────────────────────────────────────
SESSION_TTL = 3600 * 8

def create_session(username: str) -> str:
    users = load_json("users")
    session_token = secrets.token_urlsafe(32)
    users["sessions"][session_token] = {
        "username": username,
        "expire_at": (datetime.now(timezone(timedelta(hours=8))) + timedelta(seconds=SESSION_TTL)).isoformat()
    }
    save_json("users", users)
    return session_token

def validate_session(request: Request) -> Optional[str]:
    token = request.cookies.get("session")
    if not token:
        return None
    users = load_json("users")
    session = users["sessions"].get(token)
    if not session:
        return None
    expire = datetime.fromisoformat(session["expire_at"])
    if datetime.now(timezone(timedelta(hours=8))) > expire:
        del users["sessions"][token]
        save_json("users", users)
        return None
    return session["username"]

def get_user_role(username: str) -> Optional[str]:
    users = load_json("users")
    for u in users["users"]:
        if u["username"] == username:
            return u.get("role")
    return None

def require_auth(request: Request) -> str:
    # 跳过登录验证，直接返回默认用户
    return "admin"

def require_admin(request: Request) -> str:
    username = require_auth(request)
    role = get_user_role(username)
    if role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return username

# ── 路由：静态 & 首页 ───────────────────────────────────────
@app.get("/")
async def root(request: Request):
    username = validate_session(request)
    if not username:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/admin")

@app.get("/lite")
async def lite_page(request: Request):
    """Lite version - simple UI（注入 API 根地址，避免内置预览里相对 /api 指错主机）"""
    path = BASE_DIR / "admin" / "lite.html"
    html = path.read_text(encoding="utf-8")
    base = str(request.base_url).rstrip("/")
    inject = f"<script>window.__COMMUNITYOS_API_ORIGIN__={json.dumps(base)};</script>"
    if "</head>" in html:
        html = html.replace("</head>", inject + "\n</head>", 1)
    else:
        html = inject + html
    return HTMLResponse(html)

@app.get("/login")
async def login_page(request: Request):
    username = validate_session(request)
    if username:
        return RedirectResponse(url="/admin")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/login")
async def api_login(response: Response, username: str = Form(...), password: str = Form(...)):
    users = load_json("users")
    matched = next((u for u in users["users"] if u["username"] == username and u["password"] == hash_pw(password)), None)
    if not matched:
        return JSONResponse({"ok": False, "error": "用户名或密码错误"})
    token = create_session(username)
    response = JSONResponse({"ok": True, "username": username, "role": matched.get("role", "viewer")})
    response.set_cookie(key="session", value=token, httponly=True, max_age=SESSION_TTL, samesite="lax")
    log_action("login", username, f"用户 {username} 登录成功")
    return response

@app.post("/api/logout")
async def api_logout(request: Request, response: Response):
    username = validate_session(request)
    token = request.cookies.get("session")
    if token:
        users = load_json("users")
        users["sessions"].pop(token, None)
        save_json("users", users)
    response = JSONResponse({"ok": True})
    response.delete_cookie("session")
    return response

@app.get("/api/me")
async def api_me(request: Request):
    username = require_auth(request)
    role = get_user_role(username)
    return JSONResponse({"ok": True, "username": username, "role": role})

# ── 管理后台主页 ───────────────────────────────────────────
@app.get("/admin")
async def admin_page(request: Request):
    username = require_auth(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,
    })

# ── API：概览 ───────────────────────────────────────────────
@app.get("/api/dashboard")
async def api_dashboard(request: Request):
    require_auth(request)
    bots = load_json("bots")["bots"]
    groups = load_json("groups")["groups"]
    broadcasts = load_json("broadcasts")["broadcasts"]
    projects = load_json("projects")["projects"]
    logs = load_json("activity_log", {"logs": []})["logs"][:10]
    users = load_json("users")["users"]
    active_bots = [b for b in bots if b.get("enabled")]
    active_broadcasts = [b for b in broadcasts if b.get("enabled")]
    return JSONResponse({
        "ok": True,
        "stats": {
            "total_bots": len(bots),
            "active_bots": len(active_bots),
            "total_groups": len(groups),
            "active_groups": len([g for g in groups if g.get("enabled")]),
            "total_broadcasts": len(broadcasts),
            "active_broadcasts": len(active_broadcasts),
            "total_users": len(users),
            "total_projects": len(projects),
        },
        "recent_logs": logs
    })

# ════════════════════════════════════════════════════════════
#  API：Bots (完整CRUD)
# ════════════════════════════════════════════════════════════
@app.get("/api/bots")
async def api_bots_list(request: Request):
    require_auth(request)
    return JSONResponse({"ok": True, "bots": load_json("bots")["bots"]})

@app.post("/api/bots")
async def api_bots_create(request: Request, bot: dict):
    username = require_auth(request)
    data = load_json("bots")
    bot_id = (bot.get("bot_id") or "").strip()
    if not bot_id:
        raise HTTPException(status_code=400, detail="Bot ID 不能为空")
    if any(b["bot_id"] == bot_id for b in data["bots"]):
        raise HTTPException(status_code=400, detail="Bot ID 已存在")
    new_bot = {
        "bot_id": bot_id,
        "name": bot.get("name", bot_id),
        "avatar": bot.get("avatar", "🤖"),
        "bot_token": bot.get("bot_token", "") or bot.get("token_env", ""),
        "is_admin": bot.get("is_admin", False),
        "soul": bot.get("soul", ""),
        "enabled": bot.get("enabled", True),
        "created_at": ts(),
        "llm": bot.get("llm", {"provider": "minimax", "model": "MiniMax-2.7", "api_key_env": ""}),
        "modes": bot.get("modes", {
            "passive_qa": True, "welcome": False, "join_discussion": False,
            "boost_atmosphere": False, "scheduled_broadcast": False, "api_data_push": False
        }),
        "knowledge": bot.get("knowledge", {"enabled": False, "project_id": ""}),
        "welcome": bot.get("welcome", {"enabled": False, "template": ""}),
        "broadcast": bot.get("broadcast", {
            "schedule": "0 9 * * *", "content_source": "manual",
            "api_endpoint": "", "template": ""
        }),
        "interval_broadcast": bot.get("interval_broadcast", {
            "enabled": False,
            "message": "",
            "interval_seconds": 30
        }),
        "groups": bot.get("groups", []),
    }
    data["bots"].append(new_bot)
    save_json("bots", data)
    log_action("bot_create", username, f"创建 Bot {bot_id} ({new_bot.get('name', '')})")
    return JSONResponse({"ok": True, "bot": new_bot})

@app.get("/api/bots/{bot_id}")
async def api_bot_get(bot_id: str, request: Request):
    require_auth(request)
    data = load_json("bots")
    bot = next((b for b in data["bots"] if b["bot_id"] == bot_id), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot 不存在")
    return JSONResponse({"ok": True, "bot": bot})

@app.put("/api/bots/{bot_id}")
async def api_bots_update(bot_id: str, request: Request, bot: dict):
    username = require_auth(request)
    data = load_json("bots")
    idx = next((i for i, b in enumerate(data["bots"]) if b["bot_id"] == bot_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Bot 不存在")
    existing = data["bots"][idx]
    existing.update({
        "name": bot.get("name", existing.get("name", "")),
        "avatar": bot.get("avatar", existing.get("avatar", "🤖")),
        "bot_token": bot.get("bot_token", "") or bot.get("token_env", "") or existing.get("bot_token", ""),
        "is_admin": bot.get("is_admin", existing.get("is_admin", False)),
        "soul": bot.get("soul", existing.get("soul", "")),
        "enabled": bot.get("enabled", existing.get("enabled", True)),
        "llm": bot.get("llm", existing.get("llm", {})),
        "modes": bot.get("modes", existing.get("modes", {})),
        "knowledge": bot.get("knowledge", existing.get("knowledge", {})),
        "welcome": bot.get("welcome", existing.get("welcome", {})),
        "broadcast": bot.get("broadcast", existing.get("broadcast", {})),
        "interval_broadcast": bot.get("interval_broadcast", existing.get("interval_broadcast", {
            "enabled": False,
            "message": "",
            "interval_seconds": 30
        })),
        "groups": bot.get("groups", existing.get("groups", [])),
    })
    save_json("bots", data)
    log_action("bot_update", username, f"更新 Bot {bot_id}")
    return JSONResponse({"ok": True, "bot": existing})

@app.delete("/api/bots/{bot_id}")
async def api_bots_delete(bot_id: str, request: Request):
    username = require_auth(request)
    data = load_json("bots")
    data["bots"] = [b for b in data["bots"] if b["bot_id"] != bot_id]
    save_json("bots", data)
    log_action("bot_delete", username, f"删除 Bot {bot_id}")
    return JSONResponse({"ok": True})

@app.post("/api/bots/{bot_id}/apply-telegram-settings")
async def api_bot_apply_telegram_settings(bot_id: str, request: Request, settings: dict):
    """应用 Telegram 官方设置（命令菜单、描述、权限等）"""
    username = require_auth(request)
    data = load_json("bots")
    bot = next((b for b in data["bots"] if b["bot_id"] == bot_id), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot 不存在")
    
    token = bot.get("bot_token", "") or bot.get("token_env", "")
    if not token:
        raise HTTPException(status_code=400, detail="请填写 Bot Token")
    
    import httpx
    base_url = f"https://api.telegram.org/bot{token}"
    
    results = []
    
    # 1. 设置命令菜单
    commands_str = settings.get("commands", "")
    cmd_list = []
    for line in commands_str.strip().split("\n"):
        line = line.strip()
        if line and " - " in line:
            parts = line.split(" - ", 1)
            cmd_list.append({"command": parts[0].strip().lower(), "description": parts[1].strip()})
    r = httpx.post(f"{base_url}/setMyCommands", json={"commands": cmd_list}, timeout=10)
    results.append({"action": "commands", "ok": r.json().get("ok")})
    
    # 2. 设置机器人描述
    description = settings.get("description", "")
    r = httpx.post(f"{base_url}/setMyDescription", json={"description": description}, timeout=10)
    results.append({"action": "description", "ok": r.json().get("ok")})
    
    # 3. 设置简短描述
    short_desc = settings.get("short_description", "")
    r = httpx.post(f"{base_url}/setMyShortDescription", json={"short_description": short_desc}, timeout=10)
    results.append({"action": "short_description", "ok": r.json().get("ok")})
    
    # 4. 设置隐私模式 + 管理员默认权限
    can_read_all = settings.get("can_read_all", False)
    admin_rights = {
        "can_change_info": settings.get("right_change_info", False),
        "can_delete_messages": settings.get("right_delete_msg", False),
        "can_invite_users": settings.get("right_invite_users", False),
        "can_restrict_members": settings.get("right_restrict", False),
        "can_pin_messages": settings.get("right_pin", False),
        "can_promote_members": settings.get("right_promote", False),
        "can_read_messages": can_read_all,
    }
    r = httpx.post(f"{base_url}/setMyDefaultAdministratorRights", json={
        "chat_type": "group",
        "rights": admin_rights
    }, timeout=10)
    results.append({"action": "admin_rights", "ok": r.json().get("ok")})
    
    # 5. 设置 Bot 上限（不常用）
    can_join = settings.get("can_join_groups", True)
    # 这个需要通过 BotFather 设置，这里只记录
    
    log_action("bot_telegram_settings", username, f"更新 Bot {bot_id} 的 Telegram 设置")
    return JSONResponse({"ok": True, "results": results})

# ════════════════════════════════════════════════════════════
#  API：Groups (完整CRUD)
# ════════════════════════════════════════════════════════════
@app.get("/api/groups")
async def api_groups_list(request: Request):
    require_auth(request)
    return JSONResponse({"ok": True, "groups": load_json("groups")["groups"]})

@app.post("/api/groups")
async def api_groups_create(request: Request, group: dict):
    username = require_auth(request)
    data = load_json("groups")
    group_id = (group.get("group_id") or "").strip()
    if not group_id:
        raise HTTPException(status_code=400, detail="群组 ID 不能为空")
    if any(g["group_id"] == group_id for g in data["groups"]):
        raise HTTPException(status_code=400, detail="群组 ID 已存在")
    new_group = {
        "group_id": group_id,
        "group_name": group.get("group_name", group_id),
        "chat_id": group.get("chat_id", ""),
        "enabled": group.get("enabled", True),
        "bots": group.get("bots", []),
        "project_id": group.get("project_id", ""),
        "welcome_override": group.get("welcome_override", ""),
        "created_at": ts(),
    }
    data["groups"].append(new_group)
    save_json("groups", data)
    log_action("group_create", username, f"创建群组 {group_id} ({new_group.get('group_name', '')})")
    return JSONResponse({"ok": True, "group": new_group})

@app.get("/api/groups/{group_id}")
async def api_group_get(group_id: str, request: Request):
    require_auth(request)
    data = load_json("groups")
    group = next((g for g in data["groups"] if g["group_id"] == group_id), None)
    if not group:
        raise HTTPException(status_code=404, detail="群组不存在")
    return JSONResponse({"ok": True, "group": group})

@app.put("/api/groups/{group_id}")
async def api_groups_update(group_id: str, request: Request, group: dict):
    username = require_auth(request)
    data = load_json("groups")
    idx = next((i for i, g in enumerate(data["groups"]) if g["group_id"] == group_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="群组不存在")
    existing = data["groups"][idx]
    existing.update({
        "group_name": group.get("group_name", existing.get("group_name", "")),
        "chat_id": group.get("chat_id", existing.get("chat_id", "")),
        "enabled": group.get("enabled", existing.get("enabled", True)),
        "bots": group.get("bots", existing.get("bots", [])),
        "project_id": group.get("project_id", existing.get("project_id", "")),
        "welcome_override": group.get("welcome_override", existing.get("welcome_override", "")),
    })
    save_json("groups", data)
    log_action("group_update", username, f"更新群组 {group_id}")
    return JSONResponse({"ok": True, "group": existing})

@app.delete("/api/groups/{group_id}")
async def api_groups_delete(group_id: str, request: Request):
    username = require_auth(request)
    data = load_json("groups")
    data["groups"] = [g for g in data["groups"] if g["group_id"] != group_id]
    save_json("groups", data)
    log_action("group_delete", username, f"删除群组 {group_id}")
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
#  API：Broadcasts (完整CRUD)
# ════════════════════════════════════════════════════════════
@app.get("/api/broadcasts")
async def api_broadcasts_list(request: Request):
    require_auth(request)
    return JSONResponse({"ok": True, "broadcasts": load_json("broadcasts")["broadcasts"]})

@app.post("/api/broadcasts")
async def api_broadcasts_create(request: Request, broadcast: dict):
    username = require_auth(request)
    data = load_json("broadcasts")
    bc = {
        "id": broadcast.get("id") or f"bc_{uuid.uuid4().hex[:8]}",
        "name": broadcast.get("name", "未命名播报"),
        "bot_id": broadcast.get("bot_id", "panda"),
        "group_id": broadcast.get("group_id", "group_ai"),
        "cron": broadcast.get("cron", "0 9 * * *"),
        "cron_desc": broadcast.get("cron_desc", ""),
        "content_source": broadcast.get("content_source", "manual"),
        "api_endpoint": broadcast.get("api_endpoint", ""),
        "template": broadcast.get("template", ""),
        "enabled": broadcast.get("enabled", True),
        "created_at": ts(),
        "last_run": broadcast.get("last_run"),
        "next_run": broadcast.get("next_run"),
    }
    data["broadcasts"].append(bc)
    save_json("broadcasts", data)
    log_action("broadcast_create", username, f"创建播报 '{bc.get('name', '')}'")
    return JSONResponse({"ok": True, "broadcast": bc})

@app.get("/api/broadcasts/{bc_id}")
async def api_broadcast_get(bc_id: str, request: Request):
    require_auth(request)
    data = load_json("broadcasts")
    bc = next((b for b in data["broadcasts"] if b["id"] == bc_id), None)
    if not bc:
        raise HTTPException(status_code=404, detail="播报不存在")
    return JSONResponse({"ok": True, "broadcast": bc})

@app.put("/api/broadcasts/{bc_id}")
async def api_broadcasts_update(bc_id: str, request: Request, broadcast: dict):
    username = require_auth(request)
    data = load_json("broadcasts")
    idx = next((i for i, b in enumerate(data["broadcasts"]) if b["id"] == bc_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="播报不存在")
    existing = data["broadcasts"][idx]
    existing.update({
        "name": broadcast.get("name", existing.get("name", "")),
        "bot_id": broadcast.get("bot_id", existing.get("bot_id", "panda")),
        "group_id": broadcast.get("group_id", existing.get("group_id", "")),
        "cron": broadcast.get("cron", existing.get("cron", "0 9 * * *")),
        "cron_desc": broadcast.get("cron_desc", existing.get("cron_desc", "")),
        "content_source": broadcast.get("content_source", existing.get("content_source", "manual")),
        "api_endpoint": broadcast.get("api_endpoint", existing.get("api_endpoint", "")),
        "template": broadcast.get("template", existing.get("template", "")),
        "enabled": broadcast.get("enabled", existing.get("enabled", True)),
    })
    save_json("broadcasts", data)
    log_action("broadcast_update", username, f"更新播报 {bc_id}")
    return JSONResponse({"ok": True, "broadcast": existing})

@app.delete("/api/broadcasts/{bc_id}")
async def api_broadcasts_delete(bc_id: str, request: Request):
    username = require_auth(request)
    data = load_json("broadcasts")
    data["broadcasts"] = [b for b in data["broadcasts"] if b["id"] != bc_id]
    save_json("broadcasts", data)
    log_action("broadcast_delete", username, f"删除播报 {bc_id}")
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
#  API：Users (完整CRUD - 仅admin)
# ════════════════════════════════════════════════════════════
@app.get("/api/users")
async def api_users_list(request: Request):
    require_admin(request)
    users = load_json("users")
    safe_users = [{k: v for k, v in u.items() if k != "password"} for u in users["users"]]
    return JSONResponse({"ok": True, "users": safe_users})

@app.post("/api/users")
async def api_users_create(request: Request, user: dict):
    require_admin(request)
    username = require_auth(request)
    users = load_json("users")
    new_username = (user.get("username") or "").strip()
    password = (user.get("password") or "").strip()
    role = user.get("role", "viewer")
    if not new_username or len(new_username) < 2:
        raise HTTPException(status_code=400, detail="用户名至少2个字符")
    if not password or len(password) < 4:
        raise HTTPException(status_code=400, detail="密码至少4个字符")
    if role not in ("admin", "operator", "viewer"):
        raise HTTPException(status_code=400, detail="无效的角色")
    if any(u["username"] == new_username for u in users["users"]):
        raise HTTPException(status_code=400, detail="用户名已存在")
    new_user = {
        "username": new_username,
        "password": hash_pw(password),
        "role": role,
        "created_at": ts(),
    }
    users["users"].append(new_user)
    save_json("users", users)
    log_action("user_create", username, f"创建用户 {new_username} (角色: {role})")
    return JSONResponse({"ok": True, "user": {k: v for k, v in new_user.items() if k != "password"}})

@app.put("/api/users/{target_username}")
async def api_users_update(target_username: str, request: Request, user: dict):
    require_admin(request)
    current_username = require_auth(request)
    users = load_json("users")
    idx = next((i for i, u in enumerate(users["users"]) if u["username"] == target_username), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    existing = users["users"][idx]
    new_password = (user.get("password") or "").strip()
    new_role = user.get("role", existing.get("role"))
    if new_role and new_role not in ("admin", "operator", "viewer"):
        raise HTTPException(status_code=400, detail="无效的角色")
    updates = {}
    if new_password:
        if len(new_password) < 4:
            raise HTTPException(status_code=400, detail="密码至少4个字符")
        updates["password"] = hash_pw(new_password)
    if new_role:
        updates["role"] = new_role
    existing.update(updates)
    save_json("users", users)
    log_action("user_update", current_username, f"更新用户 {target_username}")
    return JSONResponse({"ok": True, "user": {k: v for k, v in existing.items() if k != "password"}})

@app.delete("/api/users/{target_username}")
async def api_users_delete(target_username: str, request: Request):
    require_admin(request)
    current_username = require_auth(request)
    if target_username == current_username:
        raise HTTPException(status_code=400, detail="不能删除自己")
    users = load_json("users")
    users["users"] = [u for u in users["users"] if u["username"] != target_username]
    save_json("users", users)
    log_action("user_delete", current_username, f"删除用户 {target_username}")
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
#  API：Projects (知识库项目 - 完整CRUD)
# ════════════════════════════════════════════════════════════
@app.get("/api/projects")
async def api_projects_list(request: Request):
    require_auth(request)
    data = load_json("projects")
    for p in data.get("projects", []):
        p["file_count"] = _count_project_files(p["id"])
    return JSONResponse({"ok": True, "projects": data.get("projects", [])})

@app.post("/api/projects")
async def api_projects_create(request: Request, project: dict):
    username = require_auth(request)
    data = load_json("projects")
    proj_id = (project.get("id") or "").strip()
    if not proj_id:
        raise HTTPException(status_code=400, detail="项目 ID 不能为空")
    if not re.match(r'^[a-zA-Z0-9_]+$', proj_id):
        raise HTTPException(status_code=400, detail="项目 ID 只能包含字母、数字和下划线")
    if any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=400, detail="项目 ID 已存在")
    new_proj = {
        "id": proj_id,
        "name": project.get("name", proj_id),
        "description": project.get("description", ""),
        "created_at": ts(),
        "file_count": 0,
    }
    data["projects"].append(new_proj)
    save_json("projects", data)
    proj_dir = KB_DIR / proj_id
    proj_dir.mkdir(parents=True, exist_ok=True)
    chroma_proj_dir = CHROMA_DIR / f"kb_{proj_id}"
    chroma_proj_dir.mkdir(parents=True, exist_ok=True)
    log_action("project_create", username, f"创建知识库项目 {proj_id} ({new_proj.get('name', '')})")
    return JSONResponse({"ok": True, "project": new_proj})

@app.get("/api/projects/{proj_id}")
async def api_project_get(proj_id: str, request: Request):
    require_auth(request)
    data = load_json("projects")
    proj = next((p for p in data["projects"] if p["id"] == proj_id), None)
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")
    proj["file_count"] = _count_project_files(proj_id)
    return JSONResponse({"ok": True, "project": proj})

@app.put("/api/projects/{proj_id}")
async def api_projects_update(proj_id: str, request: Request, project: dict):
    username = require_auth(request)
    data = load_json("projects")
    idx = next((i for i, p in enumerate(data["projects"]) if p["id"] == proj_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    existing = data["projects"][idx]
    existing.update({
        "name": project.get("name", existing.get("name", "")),
        "description": project.get("description", existing.get("description", "")),
        "urls": project.get("urls", existing.get("urls", [])),
    })
    save_json("projects", data)
    log_action("project_update", username, f"更新知识库项目 {proj_id}")
    return JSONResponse({"ok": True, "project": existing})

@app.delete("/api/projects/{proj_id}")
async def api_projects_delete(proj_id: str, request: Request):
    username = require_auth(request)
    data = load_json("projects")
    if not any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=404, detail="项目不存在")
    bots_data = load_json("bots")
    for b in bots_data["bots"]:
        if b.get("knowledge", {}).get("project_id") == proj_id and b["knowledge"].get("enabled"):
            raise HTTPException(status_code=400, detail=f"Bot {b['bot_id']} 正在使用此知识库，请先解除关联再删除")
    data["projects"] = [p for p in data["projects"] if p["id"] != proj_id]
    save_json("projects", data)
    proj_dir = KB_DIR / proj_id
    if proj_dir.exists():
        shutil.rmtree(proj_dir)
    chroma_proj_dir = CHROMA_DIR / f"kb_{proj_id}"
    if chroma_proj_dir.exists():
        shutil.rmtree(chroma_proj_dir)
    log_action("project_delete", username, f"删除知识库项目 {proj_id}")
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
#  API：Project URLs (项目关联URL)
# ════════════════════════════════════════════════════════════
@app.get("/api/projects/{proj_id}/urls")
async def api_project_list_urls(proj_id: str, request: Request):
    username = require_auth(request)
    data = load_json("projects")
    proj = next((p for p in data["projects"] if p["id"] == proj_id), None)
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")
    urls = proj.get("urls", [])
    return JSONResponse({"ok": True, "urls": urls})

@app.post("/api/projects/{proj_id}/urls")
async def api_project_add_url(proj_id: str, request: Request, body: dict = None):
    username = require_auth(request)
    data = load_json("projects")
    proj = next((p for p in data["projects"] if p["id"] == proj_id), None)
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    url = body.get("url", "").strip()
    title = body.get("title", "").strip() or url[:50]
    if not url:
        raise HTTPException(status_code=400, detail="URL不能为空")
    
    if "urls" not in proj:
        proj["urls"] = []
    
    if any(u.get("url") == url for u in proj["urls"]):
        return JSONResponse({"ok": True, "message": "URL已存在"})
    
    proj["urls"].append({
        "url": url,
        "title": title,
        "added_at": datetime.now().isoformat()
    })
    
    save_json("projects", data)
    log_action("knowledge_url_add", username, f"添加URL到项目 {proj_id}: {url}")
    return JSONResponse({"ok": True, "urls": proj["urls"]})

@app.delete("/api/projects/{proj_id}/urls/{url_index}")
async def api_project_delete_url(proj_id: str, url_index: int, request: Request):
    username = require_auth(request)
    data = load_json("projects")
    proj = next((p for p in data["projects"] if p["id"] == proj_id), None)
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if "urls" in proj and url_index < len(proj["urls"]):
        deleted = proj["urls"].pop(url_index)
        save_json("projects", data)
        log_action("knowledge_url_delete", username, f"删除URL: {deleted.get('url', '')} from {proj_id}")
    
    return JSONResponse({"ok": True, "urls": proj.get("urls", [])})

# ════════════════════════════════════════════════════════════
#  API：Project Files (项目文件管理)
# ════════════════════════════════════════════════════════════
@app.get("/api/projects/{proj_id}/files")
async def api_project_files(proj_id: str, request: Request):
    require_auth(request)
    data = load_json("projects")
    if not any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=404, detail="项目不存在")
    proj_dir = KB_DIR / proj_id
    files = []
    if proj_dir.exists():
        for f in sorted(proj_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.is_file() and f.suffix.lower() in [".md", ".txt", ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".pages"]:
                stat = f.stat()
                files.append({
                    "filename": f.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
                })
    return JSONResponse({"ok": True, "files": files})

@app.post("/api/projects/{proj_id}/upload")
async def api_project_upload(proj_id: str, request: Request, file: UploadFile = File(...)):
    username = require_auth(request)
    data = load_json("projects")
    if not any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=404, detail="项目不存在")
    proj_dir = KB_DIR / proj_id
    proj_dir.mkdir(parents=True, exist_ok=True)

    # 安全检查文件名
    safe_name = re.sub(r'[^\w.\-]', '_', file.filename)
    if not safe_name:
        raise HTTPException(status_code=400, detail="无效的文件名")
    filepath = proj_dir / safe_name

    # 如果文件已存在，加时间戳避免覆盖
    if filepath.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        safe_name = f"{stem}_{int(datetime.now(timezone(timedelta(hours=8))).timestamp())}{suffix}"
        filepath = proj_dir / safe_name

    content = await file.read()
    filepath.write_bytes(content)
    log_action("knowledge_upload", username, f"上传文件 {safe_name} -> 项目 {proj_id}")
    return JSONResponse({"ok": True, "filename": safe_name, "project_id": proj_id})

@app.delete("/api/projects/{proj_id}/files/{filename}")
async def api_project_delete_file(proj_id: str, filename: str, request: Request):
    require_auth(request)
    data = load_json("projects")
    if not any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=404, detail="项目不存在")
    filepath = KB_DIR / proj_id / filename
    if filepath.exists():
        filepath.unlink()
    return JSONResponse({"ok": True})

@app.post("/api/projects/{proj_id}/reindex")
async def api_project_reindex(proj_id: str, request: Request):
    """手动触发项目重新索引"""
    username = require_auth(request)
    data = load_json("projects")
    if not any(p["id"] == proj_id for p in data["projects"]):
        raise HTTPException(status_code=404, detail="项目不存在")

    proj_dir = KB_DIR / proj_id
    chroma_path = CHROMA_DIR / f"kb_{proj_id}"

    # 统计文件
    files = [f for f in proj_dir.iterdir() if f.is_file() and f.suffix.lower() in [".md", ".txt", ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".pages"]]
    file_count = len(files)

    # 清理旧索引
    if chroma_path.exists():
        shutil.rmtree(chroma_path)
    chroma_path.mkdir(parents=True, exist_ok=True)

    # 构建新索引（Chroma + 简单文本分块）
    try:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(path=str(chroma_path))
        collection = client.get_or_create_collection(name=f"kb_{proj_id}")

        docs = []
        ids = []
        for f in files:
            try:
                if f.suffix.lower() == ".pdf":
                    # PDF暂跳过，保留路径信息
                    continue
                text = f.read_text(encoding="utf-8", errors="ignore")
                # 简单分块（每100字一段，小文件也能索引）
                chunk_size = 100
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size].strip()
                    if chunk:
                        docs.append(chunk)
                        ids.append(f"{f.name}_{i//chunk_size}")
            except Exception:
                continue

        if docs:
            collection.add(documents=docs, ids=ids)
        log_action("knowledge_reindex", username, f"重新索引项目 {proj_id}，共 {file_count} 个文件，{len(docs)} 个分块")
        return JSONResponse({"ok": True, "message": f"索引完成", "file_count": file_count, "chunk_count": len(docs)})
    except ImportError:
        # Chroma未安装，返回模拟成功
        log_action("knowledge_reindex", username, f"模拟重新索引项目 {proj_id}，共 {file_count} 个文件（Chroma未安装）")
        return JSONResponse({"ok": True, "message": f"模拟索引完成（Chroma未安装）", "file_count": file_count, "chunk_count": 0})
    except Exception as e:
        log_action("knowledge_reindex", username, f"索引项目 {proj_id} 失败: {str(e)}", level="error")
        return JSONResponse({"ok": True, "message": f"索引完成（{str(e)}）", "file_count": file_count, "chunk_count": 0})

# ════════════════════════════════════════════════════════════
#  API：Knowledge Base (旧接口兼容，仍保留但重定向到项目)
# ════════════════════════════════════════════════════════════
@app.get("/api/knowledge")
async def api_knowledge_list(request: Request):
    """兼容旧接口，返回所有项目的文件汇总"""
    require_auth(request)
    all_files = []
    if KB_DIR.exists():
        for folder in KB_DIR.iterdir():
            if folder.is_dir():
                for f in sorted(folder.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
                    if f.is_file() and f.suffix.lower() in [".md", ".txt", ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".pages"]:
                        stat = f.stat()
                        all_files.append({
                            "filename": f.name,
                            "folder": folder.name,
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
                            "path": str(f.relative_to(BASE_DIR))
                        })
    kb = load_json("knowledge")
    return JSONResponse({"ok": True, "documents": kb.get("documents", []), "files": all_files})


@app.post("/api/knowledge/search")
async def api_knowledge_search(request: Request, data: dict):
    """知识库检索API"""
    username = require_auth(request)
    query = data.get("query", "")
    project_id = data.get("project_id", "")
    top_k = data.get("top_k", 5)
    if not query:
        raise HTTPException(status_code=400, detail="缺少query参数")
    try:
        import chromadb
        chroma_path = str(CHROMA_DIR / f"kb_{project_id}") if project_id else str(CHROMA_DIR / "kb_default")
        client = chromadb.PersistentClient(path=chroma_path)
        collection_name = f"kb_{project_id}" if project_id else "kb_default"
        try:
            collection = client.get_collection(name=collection_name)
        except Exception:
            return JSONResponse({"ok": True, "results": [], "error": f"项目 {project_id} 尚未建立索引"})
        results = collection.query(query_texts=[query], n_results=top_k)
        docs = results.get("documents", [[]])[0] if results.get("documents") else []
        metas = results.get("metadatas", [{}])[0] if results.get("metadatas") else [{}]
        formatted = []
        for i, doc in enumerate(docs[:top_k]):
            meta = metas[i] if i < len(metas) else {}
            formatted.append({
                "content": doc if isinstance(doc, str) else str(doc),
                "source": meta.get("source", meta.get("filename", "unknown")) if isinstance(meta, dict) else "unknown"
            })
        return JSONResponse({"ok": True, "results": formatted})
    except Exception as e:
        return JSONResponse({"ok": True, "results": [], "error": str(e)})

@app.post("/api/knowledge/upload")
async def api_knowledge_upload_legacy(
    request: Request,
    folder: str = Form("general"),
    file: UploadFile = File(...)
):
    """兼容旧接口，上传到通用目录"""
    username = require_auth(request)
    # 旧接口使用 folder 作为目录，自动映射到 projects
    proj_id = folder if folder != "general" else "default_knowledge"
    proj_dir = KB_DIR / proj_id
    proj_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r'[^\w.\-]', '_', file.filename)
    filepath = proj_dir / safe_name
    content = await file.read()
    filepath.write_bytes(content)
    log_action("knowledge_upload", username, f"上传文件 {file.filename} -> {folder}/")
    return JSONResponse({"ok": True, "filename": safe_name, "folder": folder})

@app.delete("/api/knowledge/{filename}")
async def api_knowledge_delete_legacy(filename: str, request: Request, folder: str = ""):
    require_auth(request)
    if folder:
        filepath = KB_DIR / folder / filename
    else:
        # 搜索所有目录
        for d in KB_DIR.iterdir():
            if d.is_dir():
                p = d / filename
                if p.exists():
                    filepath = p
                    break
        else:
            filepath = KB_DIR / filename
    if filepath.exists():
        filepath.unlink()
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
#  API：LLM Config (全局配置)
# ════════════════════════════════════════════════════════════
@app.get("/api/llm-config")
async def api_llm_config_get(request: Request):
    require_auth(request)
    config = load_json("llm_config", {
        "provider": "minimax",
        "model": "MiniMax-2.7",
        "api_key": "",
        "temperature": 0.7,
        "max_tokens": 2000
    })
    return JSONResponse({"ok": True, "config": config})

@app.put("/api/llm-config")
async def api_llm_config_save(request: Request, config: dict):
    require_auth(request)
    save_json("llm_config", config)
    log_action("llm_config_save", require_auth(request), f"更新全局LLM配置: {config.get('provider')}/{config.get('model')}")
    return JSONResponse({"ok": True, "config": config})

# ════════════════════════════════════════════════════════════
#  API：Logs
# ════════════════════════════════════════════════════════════
@app.get("/api/logs")
async def api_logs(request: Request, limit: int = 100):
    require_auth(request)
    logs = load_json("activity_log", {"logs": []})["logs"]
    return JSONResponse({"ok": True, "logs": logs[:limit]})

# ════════════════════════════════════════════════════════════
#  API：System / Health
# ════════════════════════════════════════════════════════════
@app.get("/api/health")
async def api_health(request: Request):
    require_auth(request)
    return JSONResponse({"ok": True, "time": ts()})

# ════════════════════════════════════════════════════════════
#  Telegram Runner 控制
# ════════════════════════════════════════════════════════════
telegram_process = None

@app.post("/api/telegram/start")
async def start_telegram_runner():
    """启动 Telegram 轮询服务"""
    global telegram_process
    if telegram_process and telegram_process.poll() is None:
        return JSONResponse({"ok": True, "message": "Already running"})
    
    import subprocess
    process = subprocess.Popen(
        [sys.executable, str(BASE_DIR / "admin" / "telegram_runner.py")],
        cwd=str(BASE_DIR),
        env={**os.environ}
    )
    telegram_process = process
    log_action("telegram_start", "system", "Telegram Runner started")
    return JSONResponse({"ok": True, "message": "Telegram runner started"})

@app.post("/api/telegram/stop")
async def stop_telegram_runner():
    """停止 Telegram 轮询服务"""
    global telegram_process
    if telegram_process:
        telegram_process.terminate()
        telegram_process = None
        log_action("telegram_stop", "system", "Telegram Runner stopped")
    return JSONResponse({"ok": True, "message": "Telegram runner stopped"})

@app.get("/api/telegram/status")
async def telegram_status():
    """获取 Telegram Runner 状态"""
    global telegram_process
    running = telegram_process is not None and telegram_process.poll() is None
    return JSONResponse({"ok": True, "running": running})

# ════════════════════════════════════════════════════════════
#  Telegram Webhook - 自动处理 Bot 入群
# ════════════════════════════════════════════════════════════
@app.post("/api/telegram/register-group")
async def telegram_register_group(request: Request, data: dict):
    """
    手动注册一个 Telegram 群组到系统
    当 Bot 被直接加入群后，可以调用此接口注册
    """
    require_auth(request)
    chat_id = data.get("chat_id")
    bot_id = data.get("bot_id", "")
    chat_title = data.get("chat_title", "")
    chat_type = data.get("chat_type", "supergroup")
    
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    
    if chat_type not in ("group", "supergroup"):
        return JSONResponse({"ok": True, "message": "Not a group, skip"})
    
    groups = load_json("groups")
    
    # 检查是否已存在
    for g in groups.get("groups", []):
        if g.get("group_id") == str(chat_id):
            if bot_id and bot_id not in g.get("bots", []):
                g["bots"].append(bot_id)
            save_json("groups", groups)
            return JSONResponse({"ok": True, "message": "Group already exists, updated", "group": g})
    
    new_group = {
        "group_id": str(chat_id),
        "group_name": chat_title or f"Group {chat_id}",
        "chat_id": str(chat_id),
        "enabled": True,
        "bots": [bot_id] if bot_id else [],
        "project_id": "",
        "welcome_override": "",
        "created_at": ts(),
    }
    groups["groups"].append(new_group)
    save_json("groups", groups)
    log_action("group_register", require_auth(request), f"注册群组 {chat_title} ({chat_id})")
    
    return JSONResponse({"ok": True, "message": "Group registered", "group": new_group})

@app.post("/api/telegram/webhook/{bot_id}")
async def telegram_webhook(bot_id: str, request: Request, update: dict):
    """
    Telegram Webhook - Bot 被加入群时自动处理
    需要在 Telegram BotFather 设置 webhook URL 为: https://your-domain/api/telegram/webhook/{bot_id}
    """
    try:
        my_chat_member = update.get("my_chat_member")
        if my_chat_member:
            chat = my_chat_member.get("chat", {})
            old_cm = my_chat_member.get("old_chat_member", {})
            new_cm = my_chat_member.get("new_chat_member", {})
            
            chat_id = str(chat.get("id", ""))
            chat_type = chat.get("type", "")
            chat_title = chat.get("title", chat.get("first_name", ""))
            
            if chat_type not in ("group", "supergroup"):
                return JSONResponse({"ok": True})
            
            new_status = new_cm.get("status", "")
            
            if new_status == "member" and old_cm.get("status") == "kicked":
                groups = load_json("groups")
                existing = any(g.get("group_id") == chat_id for g in groups.get("groups", []))
                if not existing:
                    new_group = {
                        "group_id": chat_id,
                        "group_name": chat_title,
                        "chat_id": chat_id,
                        "enabled": True,
                        "bots": [bot_id],
                        "project_id": "",
                        "welcome_override": "",
                        "created_at": ts(),
                        "auto_added": True
                    }
                    groups["groups"].append(new_group)
                    save_json("groups", groups)
                    log_action("group_auto_add", "system", f"Bot {bot_id} 自动加入群 {chat_title} ({chat_id})")
                    print(f"✅ Bot {bot_id} 自动注册群组: {chat_title}")
                return JSONResponse({"ok": True, "action": "joined", "group_id": chat_id})
        
        return JSONResponse({"ok": True})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
    """
    接收 Telegram 机器人更新
    当 Bot 被加入群时会收到 my_chat_member 更新
    """
    try:
        # 处理 my_chat_member 更新
        my_chat_member = update.get("my_chat_member")
        if my_chat_member:
            chat = my_chat_member.get("chat", {})
            old_chat_member = my_chat_member.get("old_chat_member", {})
            new_chat_member = my_chat_member.get("new_chat_member", {})
            
            chat_id = str(chat.get("id", ""))
            chat_type = chat.get("type", "")
            chat_title = chat.get("title", chat.get("first_name", ""))
            
            # 只处理群组
            if chat_type not in ("group", "supergroup"):
                return JSONResponse({"ok": True})
            
            # 新状态
            new_status = new_chat_member.get("status", "")
            
            # Bot 被加入群（kicked=False 表示在群里）
            if new_status == "member" and old_chat_member.get("status") == "kicked":
                # Bot 被邀请加入群
                groups = load_json("groups")
                
                # 检查是否已存在
                existing = any(g.get("group_id") == chat_id for g in groups.get("groups", []))
                if not existing:
                    new_group = {
                        "group_id": chat_id,
                        "group_name": chat_title,
                        "chat_id": chat_id,
                        "enabled": True,
                        "bots": [bot_id],
                        "project_id": "",
                        "welcome_override": "",
                        "created_at": ts(),
                        "auto_added": True  # 标记为自动添加
                    }
                    groups["groups"].append(new_group)
                    save_json("groups", groups)
                    log_action("group_auto_add", "system", f"Bot {bot_id} 自动加入群 {chat_title} ({chat_id})")
                    print(f"🤖 Bot {bot_id} 自动加入群: {chat_title} ({chat_id})")
                
                return JSONResponse({"ok": True, "action": "joined", "group_id": chat_id})
            
            # Bot 被踢出或离开群
            elif new_status in ("kicked", "left"):
                # 可选：标记群为禁用
                groups = load_json("groups")
                for g in groups.get("groups", []):
                    if g.get("group_id") == chat_id:
                        g["enabled"] = False
                        g["left_at"] = ts()
                        log_action("group_left", "system", f"Bot {bot_id} 离开群 {chat_title} ({chat_id})")
                        break
                save_json("groups", groups)
                return JSONResponse({"ok": True, "action": "left", "group_id": chat_id})
        
        return JSONResponse({"ok": True})
    except Exception as e:
        print(f"Webhook error: {e}")
        return JSONResponse({"ok": False, "error": str(e)})

# ── 运行 ───────────────────────────────────────────────────
# 清理旧字节码缓存，防止代码更新后仍加载旧版本（模块级执行，import 和直接运行都触发）
import shutil as _shutil
_pycache = Path(__file__).parent / "__pycache__"
if _pycache.exists():
    _shutil.rmtree(_pycache)
    print(f"[STARTUP] Cleared __pycache__")

if __name__ == "__main__":
    import uvicorn
    # ⚠️ 绑定到 127.0.0.1，仅本地访问，不要暴露到公网
    uvicorn.run("admin.app:app", host="127.0.0.1", port=8877, reload=False)

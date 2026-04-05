#!/usr/bin/env python3
"""
models.py - 数据结构定义

Phase 5 新增:
- 统一的数据结构定义
- 数据类（dataclass）提供清晰的接口
- 可选 SQLite 存储支持
"""

import json
import sqlite3
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


# =============================================================================
# 基础数据类
# =============================================================================

@dataclass
class Account:
    """账号数据"""
    name: str
    platform: str
    username: str = ""
    password_encrypted: str = ""  # 加密后的密码
    login_url: str = ""
    cookies: List[Dict] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    user_data: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    last_login: str = ""
    status: str = "active"  # active, disabled, locked
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Account':
        return cls(**data)


@dataclass
class Task:
    """任务数据"""
    id: str
    name: str
    type: str  # collect, post, login, custom
    status: str = "pending"  # pending, running, completed, failed, cancelled
    account_name: str = "default"
    params: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(**data)


@dataclass
class CollectedData:
    """采集数据"""
    id: str
    task_id: str
    account_name: str
    platform: str
    keyword: str
    items: List[Dict] = field(default_factory=list)
    count: int = 0
    raw_data: Optional[str] = None
    created_at: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CollectedData':
        return cls(**data)


@dataclass
class CaptchaRecord:
    """验证码记录"""
    id: str
    type: str  # slider, click, image
    image_path: str = ""
    result: Optional[Dict] = None
    success: bool = False
    attempts: int = 0
    solved_at: Optional[str] = None
    provider: str = "local"  # local, third_party
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CaptchaRecord':
        return cls(**data)


@dataclass
class Proxy:
    """代理数据"""
    id: str
    host: str
    port: int
    protocol: str = "http"  # http, https, socks5
    username: str = ""
    password: str = ""
    status: str = "active"  # active, disabled, failed
    fail_count: int = 0
    last_used: Optional[str] = None
    last_success: Optional[str] = None
    success_rate: float = 1.0
    
    @property
    def url(self) -> str:
        """获取代理URL"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Proxy':
        return cls(**data)


@dataclass
class PipelineExecution:
    """流水线执行记录"""
    id: str
    pipeline_name: str
    state: str  # idle, running, paused, completed, failed, cancelled
    context: Dict[str, Any] = field(default_factory=dict)
    step_results: List[Dict] = field(default_factory=list)
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PipelineExecution':
        return cls(**data)


# =============================================================================
# 数据库存储 (可选)
# =============================================================================

class DatabaseManager:
    """
    SQLite 数据库管理器
    
    提供可选的 SQLite 存储支持，可替代纯文件存储
    
    用法:
        db = DatabaseManager()
        db.save_account(account)
        accounts = db.get_accounts()
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库
        
        Args:
            db_path: 数据库路径，默认 ~/.openclaw/data/reg_browser_bot.db
        """
        if db_path is None:
            db_path = os.path.expanduser("~/.config/reg-browser-bot/reg-browser-bot.db")
        
        self._db_path = db_path
        self._ensure_db_dir()
        self._init_db()
    
    def _ensure_db_dir(self):
        """确保数据库目录存在"""
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """初始化数据库表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 账号表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    name TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    username TEXT,
                    password_encrypted TEXT,
                    login_url TEXT,
                    cookies TEXT,
                    headers TEXT,
                    user_data TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    last_login TEXT,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # 任务表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    account_name TEXT DEFAULT 'default',
                    params TEXT,
                    result TEXT,
                    error TEXT,
                    created_at TEXT,
                    started_at TEXT,
                    completed_at TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3
                )
            """)
            
            # 采集数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS collected_data (
                    id TEXT PRIMARY KEY,
                    task_id TEXT,
                    account_name TEXT,
                    platform TEXT,
                    keyword TEXT,
                    items TEXT,
                    count INTEGER DEFAULT 0,
                    raw_data TEXT,
                    created_at TEXT
                )
            """)
            
            # 验证码记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS captcha_records (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    image_path TEXT,
                    result TEXT,
                    success INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    solved_at TEXT,
                    provider TEXT DEFAULT 'local'
                )
            """)
            
            # 代理表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proxies (
                    id TEXT PRIMARY KEY,
                    host TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    protocol TEXT DEFAULT 'http',
                    username TEXT,
                    password TEXT,
                    status TEXT DEFAULT 'active',
                    fail_count INTEGER DEFAULT 0,
                    last_used TEXT,
                    last_success TEXT,
                    success_rate REAL DEFAULT 1.0
                )
            """)
            
            # 流水线执行记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pipeline_executions (
                    id TEXT PRIMARY KEY,
                    pipeline_name TEXT NOT NULL,
                    state TEXT DEFAULT 'idle',
                    context TEXT,
                    step_results TEXT,
                    error TEXT,
                    started_at TEXT,
                    completed_at TEXT,
                    duration_seconds REAL DEFAULT 0.0
                )
            """)
            
            conn.commit()
    
    # =========================================================================
    # 账号操作
    # =========================================================================
    
    def save_account(self, account: Account) -> bool:
        """保存账号"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO accounts 
                (name, platform, username, password_encrypted, login_url, 
                 cookies, headers, user_data, created_at, updated_at, last_login, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account.name, account.platform, account.username,
                account.password_encrypted, account.login_url,
                json.dumps(account.cookies), json.dumps(account.headers),
                json.dumps(account.user_data), account.created_at,
                account.updated_at, account.last_login, account.status
            ))
            conn.commit()
            return True
    
    def get_account(self, name: str) -> Optional[Account]:
        """获取账号"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return self._row_to_account(row)
            return None
    
    def get_accounts(self, platform: str = None, status: str = None) -> List[Account]:
        """获取账号列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM accounts WHERE 1=1"
            params = []
            if platform:
                query += " AND platform = ?"
                params.append(platform)
            if status:
                query += " AND status = ?"
                params.append(status)
            cursor.execute(query, params)
            return [self._row_to_account(row) for row in cursor.fetchall()]
    
    def _row_to_account(self, row: sqlite3.Row) -> Account:
        """将数据库行转换为 Account 对象"""
        return Account(
            name=row['name'],
            platform=row['platform'],
            username=row['username'] or '',
            password_encrypted=row['password_encrypted'] or '',
            login_url=row['login_url'] or '',
            cookies=json.loads(row['cookies'] or '[]'),
            headers=json.loads(row['headers'] or '{}'),
            user_data=json.loads(row['user_data'] or '{}'),
            created_at=row['created_at'] or '',
            updated_at=row['updated_at'] or '',
            last_login=row['last_login'] or '',
            status=row['status'] or 'active'
        )
    
    # =========================================================================
    # 任务操作
    # =========================================================================
    
    def save_task(self, task: Task) -> bool:
        """保存任务"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tasks 
                (id, name, type, status, account_name, params, result, error,
                 created_at, started_at, completed_at, retry_count, max_retries)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id, task.name, task.type, task.status, task.account_name,
                json.dumps(task.params), json.dumps(task.result) if task.result else None,
                task.error, task.created_at, task.started_at, task.completed_at,
                task.retry_count, task.max_retries
            ))
            conn.commit()
            return True
    
    def get_task(self, id: str) -> Optional[Task]:
        """获取任务"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_task(row)
            return None
    
    def get_tasks(self, status: str = None, account_name: str = None) -> List[Task]:
        """获取任务列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM tasks WHERE 1=1"
            params = []
            if status:
                query += " AND status = ?"
                params.append(status)
            if account_name:
                query += " AND account_name = ?"
                params.append(account_name)
            cursor.execute(query, params)
            return [self._row_to_task(row) for row in cursor.fetchall()]
    
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """将数据库行转换为 Task 对象"""
        return Task(
            id=row['id'],
            name=row['name'],
            type=row['type'],
            status=row['status'] or 'pending',
            account_name=row['account_name'] or 'default',
            params=json.loads(row['params'] or '{}'),
            result=json.loads(row['result']) if row['result'] else None,
            error=row['error'],
            created_at=row['created_at'] or '',
            started_at=row['started_at'],
            completed_at=row['completed_at'],
            retry_count=row['retry_count'] or 0,
            max_retries=row['max_retries'] or 3
        )
    
    # =========================================================================
    # 采集数据操作
    # =========================================================================
    
    def save_collected_data(self, data: CollectedData) -> bool:
        """保存采集数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO collected_data 
                (id, task_id, account_name, platform, keyword, items, count, raw_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.id, data.task_id, data.account_name, data.platform,
                data.keyword, json.dumps(data.items), data.count,
                data.raw_data, data.created_at
            ))
            conn.commit()
            return True
    
    def get_collected_data(self, id: str) -> Optional[CollectedData]:
        """获取采集数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collected_data WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_collected_data(row)
            return None
    
    def get_collected_data_by_task(self, task_id: str) -> List[CollectedData]:
        """获取任务的所有采集数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collected_data WHERE task_id = ?", (task_id,))
            return [self._row_to_collected_data(row) for row in cursor.fetchall()]
    
    def _row_to_collected_data(self, row: sqlite3.Row) -> CollectedData:
        """将数据库行转换为 CollectedData 对象"""
        return CollectedData(
            id=row['id'],
            task_id=row['task_id'] or '',
            account_name=row['account_name'] or '',
            platform=row['platform'] or '',
            keyword=row['keyword'] or '',
            items=json.loads(row['items'] or '[]'),
            count=row['count'] or 0,
            raw_data=row['raw_data'],
            created_at=row['created_at'] or ''
        )


# =============================================================================
# 便捷函数
# =============================================================================

_default_db: Optional[DatabaseManager] = None


def get_database() -> DatabaseManager:
    """获取全局数据库实例"""
    global _default_db
    if _default_db is None:
        _default_db = DatabaseManager()
    return _default_db

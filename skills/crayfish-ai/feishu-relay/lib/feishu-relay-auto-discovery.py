#!/usr/bin/env python3
"""
feishu-relay-auto-discovery.py - 自动发现新系统并注册到 Feishu Relay

功能：
1. 监控文件系统变化（新目录创建）
2. 检测新部署的 Web 应用、服务、定时任务
3. 自动注册到 Feishu Relay 通知系统
4. 无需手动干预

运行方式：
- 作为 systemd 服务常驻运行
- 或使用 inotify 事件触发
"""

import os
import sys
import json
import time
import sqlite3
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# 配置
REGISTRY_FILE = "/opt/feishu-notifier/registry/systems.json"
WATCH_PATHS = ["/opt", "/var/www", "/data", "/home"]
IGNORE_PATTERNS = [".git", "node_modules", "__pycache__", ".cache", "tmp", "temp"]
SYSTEM_TYPES = {
    "/var/www": "website",
    "/opt": "service",
    "/data": "data",
    "/home": "user"
}

# 检测间隔（秒）
SCAN_INTERVAL = 300  # 5分钟扫描一次


def log(msg):
    """输出日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [AutoDiscovery] {msg}"
    print(log_line, flush=True)
    # 同时写入日志文件
    log_dir = "/var/log/feishu-relay"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/discovery.log", "a") as f:
        f.write(log_line + "\n")


def load_registry():
    """加载注册表"""
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            log(f"Error loading registry: {e}")
    return {"systems": [], "updated_at": ""}


def save_registry(registry):
    """保存注册表"""
    registry["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def get_system_type(path):
    """根据路径判断系统类型"""
    path_lower = path.lower()
    
    # 检查特定关键词
    if any(kw in path_lower for kw in ["web", "site", "html", "www"]):
        return "website"
    if any(kw in path_lower for kw in ["service", "daemon", "api"]):
        return "service"
    if any(kw in path_lower for kw in ["skill", "plugin", "extension"]):
        return "skill"
    if any(kw in path_lower for kw in ["task", "cron", "job"]):
        return "task"
    
    # 根据父目录判断
    for prefix, stype in SYSTEM_TYPES.items():
        if path.startswith(prefix):
            return stype
    
    return "unknown"


def detect_web_framework(path):
    """检测 Web 框架类型"""
    indicators = {
        "nextjs": ["next.config.js", "next.config.ts", ".next"],
        "nuxt": ["nuxt.config.js", "nuxt.config.ts", ".nuxt"],
        "react": ["src/App.js", "src/App.tsx", "public/index.html"],
        "vue": ["vue.config.js", "src/App.vue"],
        "django": ["manage.py", "requirements.txt", "wsgi.py"],
        "flask": ["app.py", "wsgi.py"],
        "php": ["index.php", "composer.json"],
        "static": ["index.html", "style.css"]
    }
    
    for framework, files in indicators.items():
        if any(os.path.exists(os.path.join(path, f)) for f in files):
            return framework
    return "unknown"


def detect_service_type(path):
    """检测服务类型"""
    indicators = {
        "systemd": ["systemd", ".service"],
        "docker": ["Dockerfile", "docker-compose.yml", ".dockerignore"],
        "python": ["requirements.txt", "setup.py", "pyproject.toml"],
        "node": ["package.json", "node_modules"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"]
    }
    
    for stype, patterns in indicators.items():
        for pattern in patterns:
            # 检查文件名或目录内容
            for item in os.listdir(path) if os.path.isdir(path) else []:
                if pattern in item:
                    return stype
    return "unknown"


def should_ignore(path):
    """检查是否应该忽略该路径"""
    path_parts = path.split(os.sep)
    return any(ignore in path_parts for ignore in IGNORE_PATTERNS)


def is_valid_system(path):
    """检查路径是否是一个有效的系统/项目"""
    if not os.path.isdir(path):
        return False
    
    if should_ignore(path):
        return False
    
    # 检查是否包含项目特征文件
    indicators = [
        "package.json", "requirements.txt", "Cargo.toml", "go.mod",
        "pom.xml", "build.gradle", "CMakeLists.txt", "Makefile",
        "docker-compose.yml", "Dockerfile", ".env", "config.json",
        "index.html", "index.php", "app.py", "main.py", "server.js",
        "README.md", "LICENSE", ".git"
    ]
    
    try:
        contents = os.listdir(path)
        # 至少包含一个指示文件，或包含 src/ 目录
        has_indicator = any(f in contents for f in indicators)
        has_src = "src" in contents or "source" in contents
        has_bin = "bin" in contents or "dist" in contents or "build" in contents
        
        return has_indicator or has_src or has_bin
    except PermissionError:
        return False


def generate_system_id(path):
    """生成系统唯一 ID"""
    return hashlib.md5(path.encode()).hexdigest()[:8]


def discover_systems():
    """发现所有符合条件的系统"""
    discovered = []
    
    for watch_path in WATCH_PATHS:
        if not os.path.exists(watch_path):
            continue
        
        try:
            for item in os.listdir(watch_path):
                full_path = os.path.join(watch_path, item)
                
                if not is_valid_system(full_path):
                    continue
                
                system_type = get_system_type(full_path)
                
                # 进一步检测子类型
                if system_type == "website":
                    subtype = detect_web_framework(full_path)
                elif system_type == "service":
                    subtype = detect_service_type(full_path)
                else:
                    subtype = "unknown"
                
                system_info = {
                    "id": generate_system_id(full_path),
                    "name": item,
                    "type": system_type,
                    "subtype": subtype,
                    "path": full_path,
                    "notify_method": "auto",
                    "discovered_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "status": "active",
                    "auto_discovered": True
                }
                
                discovered.append(system_info)
                
        except PermissionError:
            log(f"Permission denied: {watch_path}")
        except Exception as e:
            log(f"Error scanning {watch_path}: {e}")
    
    return discovered


def register_system(system):
    """注册系统到 Feishu Relay"""
    registry = load_registry()
    
    # 检查是否已存在
    existing = next((s for s in registry["systems"] if s["path"] == system["path"]), None)
    
    if existing:
        # 更新现有记录
        existing.update(system)
        existing["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        log(f"Updated: {system['name']} ({system['type']})")
    else:
        # 添加新记录
        registry["systems"].append(system)
        log(f"Registered: {system['name']} ({system['type']})")
        
        # 发送通知
        send_registration_notification(system)
    
    save_registry(registry)


def send_registration_notification(system):
    """发送新系统注册通知"""
    try:
        title = f"🆕 新系统已自动注册"
        content = f"""系统名称: {system['name']}
类型: {system['type']} ({system.get('subtype', 'unknown')})
路径: {system['path']}
注册时间: {system['discovered_at']}"""
        
        notify_script = "/opt/feishu-notifier/bin/notify"
        if os.path.exists(notify_script):
            subprocess.run(
                [notify_script, title, content],
                capture_output=True,
                timeout=10
            )
    except Exception as e:
        log(f"Failed to send notification: {e}")


def unregister_removed_systems():
    """清理已不存在的系统"""
    registry = load_registry()
    removed = []
    
    for system in registry["systems"][:]:  # 复制列表避免修改时迭代问题
        if not os.path.exists(system["path"]):
            registry["systems"].remove(system)
            removed.append(system["name"])
    
    if removed:
        save_registry(registry)
        log(f"Unregistered removed systems: {', '.join(removed)}")


def scan_and_register():
    """执行一次扫描和注册"""
    log("Starting discovery scan...")
    
    # 发现新系统
    discovered = discover_systems()
    log(f"Discovered {len(discovered)} systems")
    
    # 注册每个系统
    for system in discovered:
        register_system(system)
    
    # 清理已删除的系统
    unregister_removed_systems()
    
    log("Discovery scan completed")


def setup_inotify_watcher():
    """设置 inotify 监控（如果可用）"""
    try:
        import inotify.adapters
        
        log("Setting up inotify watcher...")
        
        i = inotify.adapters.Inotify()
        
        for watch_path in WATCH_PATHS:
            if os.path.exists(watch_path):
                try:
                    i.add_watch(watch_path.encode())
                    log(f"Watching: {watch_path}")
                except Exception as e:
                    log(f"Cannot watch {watch_path}: {e}")
        
        return i
    except ImportError:
        log("inotify not available, falling back to polling")
        return None


def run_with_inotify():
    """使用 inotify 事件驱动模式运行"""
    watcher = setup_inotify_watcher()
    
    if watcher is None:
        return False
    
    log("Running in inotify mode...")
    
    # 初始扫描
    scan_and_register()
    
    try:
        for event in watcher.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            
            # 只关注创建事件
            if 'IN_CREATE' in type_names or 'IN_ISDIR' in type_names:
                full_path = os.path.join(path.decode(), filename.decode())
                
                if should_ignore(full_path):
                    continue
                
                # 延迟检查，等待目录内容稳定
                time.sleep(2)
                
                if is_valid_system(full_path):
                    system_type = get_system_type(full_path)
                    system = {
                        "id": generate_system_id(full_path),
                        "name": filename.decode(),
                        "type": system_type,
                        "subtype": detect_web_framework(full_path) if system_type == "website" else detect_service_type(full_path),
                        "path": full_path,
                        "notify_method": "auto",
                        "discovered_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                        "status": "active",
                        "auto_discovered": True
                    }
                    register_system(system)
                    
    except KeyboardInterrupt:
        log("Shutting down inotify watcher...")
    
    return True


def run_with_polling():
    """使用轮询模式运行"""
    log(f"Running in polling mode (interval: {SCAN_INTERVAL}s)...")
    
    # 初始扫描
    scan_and_register()
    
    try:
        while True:
            time.sleep(SCAN_INTERVAL)
            scan_and_register()
    except KeyboardInterrupt:
        log("Shutting down polling watcher...")


def main():
    """主函数"""
    log("=" * 50)
    log("Feishu Relay Auto Discovery starting...")
    log(f"Watch paths: {', '.join(WATCH_PATHS)}")
    log(f"Registry file: {REGISTRY_FILE}")
    log("=" * 50)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
    
    # 尝试使用 inotify，否则回退到轮询
    if not run_with_inotify():
        run_with_polling()


if __name__ == "__main__":
    main()

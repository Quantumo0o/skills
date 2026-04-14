#!/usr/bin/env python3
"""report-expert 技能自动升级工具

用法:
  python3 upgrade.py              # 检查并升级
  python3 upgrade.py --check      # 仅检查，不升级
  python3 upgrade.py --force      # 强制升级（忽略版本比较）
  python3 upgrade.py --version    # 显示当前版本

流程:
  1. 读取本地 manifest.json（如有）
  2. 从远程拉取最新 manifest.json
  3. 比较版本号
  4. 如有更新：下载变更文件 → 校验 SHA256 → 覆盖本地文件
"""

import hashlib, json, os, sys, urllib.request, urllib.error
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
LOCAL_MANIFEST = SKILL_DIR / "manifest.json"

def get_remote_base() -> str:
    """从本地 manifest 读取 repository 作为远程基础地址"""
    if LOCAL_MANIFEST.exists():
        try:
            data = json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8"))
            return data.get("repository", "").rstrip("/")
        except (json.JSONDecodeError, KeyError):
            pass
    return ""

def resolve_url(rel_path: str, remote_base: str) -> str:
    """将相对路径解析为完整 URL"""
    if rel_path.startswith("http"):
        return rel_path
    return f"{remote_base}/{rel_path}"

# ── 工具函数 ──────────────────────────────────────────

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch_json(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "report-expert-upgrade/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def download_file(url: str, dest: Path, timeout: int = 30) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "report-expert-upgrade/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)

def parse_version(v: str) -> tuple:
    """Parse '1.2.3' → (1, 2, 3)"""
    parts = v.lstrip("v").split(".")
    return tuple(int(p) for p in parts[:3])

def version_gt(a: str, b: str) -> bool:
    return parse_version(a) > parse_version(b)

# ── 核心逻辑 ──────────────────────────────────────────

def get_local_version() -> str:
    if LOCAL_MANIFEST.exists():
        try:
            data = json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8"))
            return data.get("version", "0.0.0")
        except (json.JSONDecodeError, KeyError):
            pass
    return "0.0.0"

def check_update() -> dict | None:
    """返回远程 manifest，或 None 表示无需更新"""
    remote_base = get_remote_base()
    if not remote_base:
        print("❌ 本地 manifest.json 缺少 repository 字段，无法确定远程地址")
        return None

    remote_manifest_url = f"{remote_base}/manifest.json"
    print(f"📡 正在检查远程版本: {remote_manifest_url}")
    try:
        remote = fetch_json(remote_manifest_url)
    except urllib.error.URLError as e:
        print(f"❌ 无法连接远程仓库: {e}")
        return None
    except Exception as e:
        print(f"❌ 获取 manifest 失败: {e}")
        return None

    local_ver = get_local_version()
    remote_ver = remote.get("version", "0.0.0")

    print(f"   本地版本: {local_ver}")
    print(f"   远程版本: {remote_ver}")

    if version_gt(remote_ver, local_ver):
        print(f"🆕 发现新版本: {local_ver} → {remote_ver}")
        return remote
    else:
        print(f"✅ 已是最新版本")
        return None

def do_upgrade(remote: dict, force: bool = False) -> bool:
    """执行升级，返回是否成功"""
    files = remote.get("files", {})
    if not files:
        print("❌ manifest 中没有文件列表")
        return False

    # 远程基础地址：优先用远程 manifest 的 repository，回退到本地
    remote_base = remote.get("repository", "").rstrip("/") or get_remote_base()
    if not remote_base:
        print("❌ 无法确定远程基础地址")
        return False

    updated = []
    skipped = []
    failed = []

    for rel_path, meta in files.items():
        url = resolve_url(meta.get("url", ""), remote_base)
        expected_sha = meta.get("sha256", "")

        if not url:
            skipped.append((rel_path, "无下载地址"))
            continue

        local_path = SKILL_DIR / rel_path

        # 如果本地文件已存在且 SHA 匹配，跳过
        if not force and local_path.exists() and expected_sha:
            local_sha = sha256_file(local_path)
            if local_sha == expected_sha:
                skipped.append((rel_path, "SHA 匹配"))
                continue

        # 下载
        try:
            download_file(url, local_path)
        except Exception as e:
            failed.append((rel_path, str(e)))
            continue

        # 校验
        if expected_sha:
            actual_sha = sha256_file(local_path)
            if actual_sha != expected_sha:
                failed.append((rel_path, f"SHA 不匹配 (期望 {expected_sha[:12]}...，实际 {actual_sha[:12]}...)"))
                if local_path.exists():
                    local_path.unlink()
                continue

        updated.append(rel_path)

    if updated:
        print(f"\n📦 已更新 {len(updated)} 个文件:")
        for f in updated:
            print(f"   ✅ {f}")

    if skipped:
        print(f"\n⏭️  跳过 {len(skipped)} 个文件:")
        for f, reason in skipped:
            print(f"   ⏭️  {f} ({reason})")

    if failed:
        print(f"\n❌ 失败 {len(failed)} 个文件:")
        for f, reason in failed:
            print(f"   ❌ {f}: {reason}")
        return False

    # 保存 manifest
    with open(LOCAL_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(remote, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 升级完成 → v{remote.get('version', '?')}")
    return True

def show_changelog(remote: dict) -> None:
    changelog = remote.get("changelog", [])
    if not changelog:
        return
    print(f"\n📋 更新日志:")
    for entry in changelog[:3]:
        print(f"\n   v{entry['version']} ({entry['date']})")
        for change in entry.get("changes", []):
            print(f"   • {change}")

def show_capabilities(remote: dict) -> None:
    caps = remote.get("capabilities", [])
    if not caps:
        return
    print(f"\n🔧 能力列表:")
    for cap in caps:
        print(f"   [{cap.get('since', '?')}] {cap['name']}: {cap['desc']}")

# ── 入口 ──────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    force = "--force" in args
    show_ver = "--version" in args

    if show_ver:
        v = get_local_version()
        print(f"report-expert v{v}")
        return

    remote = check_update()
    if remote is None:
        if check_only:
            return
        print("无需升级")
        return

    show_changelog(remote)

    if check_only:
        return

    print()
    do_upgrade(remote, force=force)

if __name__ == "__main__":
    main()

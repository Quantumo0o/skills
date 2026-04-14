"""从部署目录拉取文件到技能 dist/，保持技能目录的完整性。

技能目录是 source of truth（模板、脚本、配置等），
但已部署的报告页面可能被线上直接修改过（如手动修复）。
pull 命令从部署目录拉取页面 + 静态资源，覆盖技能 dist/。
"""

import shutil, sys
from pathlib import Path

from lib.config import BASE_DIR, REPORT_LOCAL_DIR, SITE_NAME


def pull(pages=None, sync_index=True, sync_assets=True):
    """从部署目录拉取文件到技能 dist/。

    Args:
        pages: 指定要拉取的文件列表（相对路径），None 表示全部。
        sync_index: 是否同步 index.html 和 index.json。
        sync_assets: 是否同步 styles/ 和 scripts/。
    """
    skill_dist = BASE_DIR / "dist"
    deploy_root = Path(REPORT_LOCAL_DIR)

    if not deploy_root.exists():
        print(f"❌ 部署目录不存在: {deploy_root}")
        sys.exit(1)

    # 需要排除的目录（非页面产出）
    skip = {'dist', 'dist.bak', 'data', 'templates', '.wrangler',
            '__pycache__', 'node_modules'}

    # 只拉取 HTML 页面 + 静态资源 + index，跳过其他文件
    allowed_ext = {'.html', '.css', '.js', '.json'}

    pulled = 0
    errors = []

    if pages:
        # 拉取指定文件
        for rel in pages:
            src = deploy_root / rel
            dst = skill_dist / rel
            if not src.exists():
                errors.append(f"  ⚠️ {rel} — 部署目录中不存在")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            pulled += 1
            print(f"  ✅ {rel}")
    else:
        # 拉取所有页面文件
        print(f"📡 从 {deploy_root} 拉取到 {skill_dist} ...")
        for fpath in sorted(deploy_root.rglob("*")):
            if not fpath.is_file():
                continue
            rel = fpath.relative_to(deploy_root)
            # 跳过排除目录下的文件
            if any(p in skip for p in rel.parts):
                continue
            # 只拉取部署产出文件（HTML/CSS/JS/JSON）
            if fpath.suffix.lower() not in allowed_ext:
                continue
            # 跳过静态资源（单独处理）
            if rel.parts[0] in ('styles', 'scripts') and sync_assets:
                continue  # 下面单独同步
            dst = skill_dist / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fpath, dst)
            pulled += 1
            print(f"  ✅ {rel}")

    # 同步静态资源
    if sync_assets:
        assets = [
            deploy_root / "styles" / "base.css",
            deploy_root / "scripts" / "main.js",
        ]
        for asset in assets:
            if not asset.exists():
                continue
            rel = asset.relative_to(deploy_root)
            dst = skill_dist / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dst)
            pulled += 1
            print(f"  📄 {rel}")

    # 同步 index
    if sync_index:
        for name in ("index.html", "index.json"):
            src = deploy_root / name
            dst = skill_dist / name
            if src.exists():
                shutil.copy2(src, dst)
                pulled += 1
                print(f"  📄 {name}")

    print(f"\n✅ 拉取完成: {pulled} 个文件")
    if errors:
        print(f"⚠️ {len(errors)} 个错误:")
        for e in errors:
            print(e)

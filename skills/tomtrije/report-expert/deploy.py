#!/usr/bin/env python3
"""传琪 · 报告部署系统 — CLI 入口"""

import sys
from lib.config import REPORT_DEPLOY_MODE
from lib.local_deploy import deploy as local_deploy
from lib.remote_deploy import deploy as remote_deploy
from lib.index import rebuild_index, add_to_index, scan_and_rebuild
from lib.backup import _restore_backup, update_pages
from lib.pull import pull
from lib.skill_cf_publish import publish_preview, publish_prod
from lib.skill_clawhub_publish import publish_to_clawhub

def _parse_opts(argv, start=0):
    """Parse --key value pairs from argv starting at `start`."""
    opts = {}
    i = start
    while i < len(argv):
        if argv[i].startswith("--") and i+1 < len(argv):
            opts[argv[i]] = argv[i+1]; i += 2
        else:
            i += 1
    return opts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  # 报告部署")
        print("  python deploy.py deploy <category> <file> [--title T] [--desc D]")
        print("  python deploy.py local-deploy <category> <file> [--title T] [--desc D]")
        print("  python deploy.py remote-deploy <category> <file> [--title T] [--desc D]")
        print("  # 技能发布")
        print("  python deploy.py skill-cf-publish          # 预览环境")
        print("  python deploy.py skill-cf-publish-prod     # 生产环境")
        print("  python deploy.py skill-clawhub-publish [--changelog 'xxx']")
        print("  # 索引和备份")
        print("  python deploy.py rebuild_index")
        print("  python deploy.py add <file> --title T --desc D --category C [--url U]")
        print("  python deploy.py scan [--ai]")
        print("  python deploy.py update")
        print("  python deploy.py backup [list|restore <name>]")
        print("  python deploy.py pull [--files 'f1,f2'] [--no-index] [--no-assets]")
        sys.exit(0)

    cmd = sys.argv[1]

    # ── 报告部署 ──
    if cmd == "deploy" or cmd == "local-deploy" or cmd == "remote-deploy":
        if len(sys.argv) < 4:
            print(f"❌ 用法: python deploy.py {cmd} <category> <html_file> [--title T] [--desc D]")
            sys.exit(1)
        category = sys.argv[2]
        html_file = sys.argv[3]
        opts = _parse_opts(sys.argv, 4)
        title = opts.get("--title")
        desc = opts.get("--desc")

        if cmd == "local-deploy":
            local_deploy(category, html_file, title, desc)
        elif cmd == "remote-deploy":
            remote_deploy(category, html_file, title, desc)
        else:
            # auto-select based on mode
            if REPORT_DEPLOY_MODE == "remote":
                remote_deploy(category, html_file, title, desc)
            else:
                local_deploy(category, html_file, title, desc)

    # ── 技能发布 ──
    elif cmd == "skill-cf-publish":
        publish_preview()

    elif cmd == "skill-cf-publish-prod":
        publish_prod()

    elif cmd == "skill-clawhub-publish":
        opts = _parse_opts(sys.argv, 2)
        publish_to_clawhub(changelog=opts.get("--changelog", ""))

    # ── 索引和备份 ──
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("❌ 用法: python deploy.py add <filename> --title T --desc D --category C [--url U]")
            sys.exit(1)
        filename = sys.argv[2]
        opts = _parse_opts(sys.argv, 3)
        title = opts.get("--title")
        desc = opts.get("--desc")
        category = opts.get("--category")
        url = opts.get("--url")
        if not title or not category:
            print("❌ --title 和 --category 是必须的")
            sys.exit(1)
        add_to_index(filename, title, desc, category, url)

    elif cmd == "rebuild_index":
        opts = _parse_opts(sys.argv, 2)
        rebuild_index(clean=opts.get("--clean") is not None)

    elif cmd == "scan":
        scan_and_rebuild()

    elif cmd == "update":
        update_pages()

    elif cmd == "pull":
        opts = _parse_opts(sys.argv, 2)
        file_list = opts.get("--files", "").split(",") if opts.get("--files") else None
        file_list = [f.strip() for f in file_list] if file_list else None
        pull(
            pages=file_list,
            sync_index=opts.get("--no-index") is None,
            sync_assets=opts.get("--no-assets") is None,
        )

    elif cmd == "backup":
        if len(sys.argv) >= 3 and sys.argv[2] == "restore" and len(sys.argv) >= 4:
            _restore_backup(sys.argv[3])
        else:
            _restore_backup()

    # ── 向后兼容 ──
    elif cmd == "publish":
        print("⚠️ `publish` 已重命名为 `skill-cf-publish`")
        publish_preview()

    elif cmd == "publish-prod":
        print("⚠️ `publish-prod` 已重命名为 `skill-cf-publish-prod`")
        publish_prod()

    else:
        print(f"❌ 未知命令: {cmd}")
        print("   运行 python deploy.py 查看帮助")

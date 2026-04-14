"""远程部署：将报告页面部署到 Cloudflare Pages"""

import os, subprocess
from pathlib import Path

from lib.config import _get_cfg_val, REPORT_CF_PROJECT, REPORT_DEPLOY_MODE
from lib.local_deploy import deploy as _local_deploy


def deploy(category, html_file, title=None, desc=None):
    """Deploy a report page to Cloudflare Pages via wrangler.

    Falls back to local deploy if CF project is not configured.
    """
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or _get_cfg_val("CLOUDFLARE_API_TOKEN")
    project = REPORT_CF_PROJECT

    if not project:
        print("⚠️ 未配置 REPORT_CF_PROJECT，回退到本地部署")
        print("   在 TOOLS.md 中添加: REPORT_CF_PROJECT=your-project-name")
        _local_deploy(category, html_file, title, desc)
        return

    if not token:
        print("⚠️ 未配置 CLOUDFLARE_API_TOKEN，回退到本地部署")
        _local_deploy(category, html_file, title, desc)
        return

    # First do local deploy to build the files
    _local_deploy(category, html_file, title, desc)

    # Then deploy the site root directory to CF Pages
    deploy_dist = Path(REPORT_LOCAL_DIR)
    if not deploy_dist.exists():
        print(f"❌ 部署目录不存在: {deploy_dist}")
        return

    env = {**os.environ, "CLOUDFLARE_API_TOKEN": token}
    cmd = ["npx", "wrangler", "pages", "deploy", str(deploy_dist),
           "--project-name", project, "--commit-dirty=true", "--branch", "main"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print("❌ 远程部署失败")
    else:
        print(f"✅ 远程部署成功 → {project}.pages.dev")

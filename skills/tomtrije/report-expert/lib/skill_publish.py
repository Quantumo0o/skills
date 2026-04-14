"""技能发布：将技能本身部署到 Cloudflare Pages（预览/生产）"""

import json, re, subprocess, time, os, shutil, tempfile, hashlib
from pathlib import Path
from datetime import date

from lib.config import BASE_DIR, SITE_URL, _get_cfg_val
from lib.page import generate_page_html


def _deploy_to_cf(skill_dir, project, token, branch="production"):
    """Deploy skill files to Cloudflare Pages via wrangler."""
    tmp = Path(tempfile.mkdtemp())
    try:
        for item in skill_dir.iterdir():
            name = item.name
            if name in ("dist", ".wrangler", "__pycache__", "backups", ".git"):
                continue
            if name.startswith("tmp") or name.startswith("."):
                continue
            if item.is_dir():
                shutil.copytree(item, tmp / name)
            else:
                shutil.copy2(item, tmp / name)
        deploy_dir = tmp
    except Exception as e:
        print(f"⚠️ 创建临时部署目录失败，使用原始目录: {e}")
        deploy_dir = skill_dir
    env = {**os.environ, "CLOUDFLARE_API_TOKEN": token}
    cmd = ["npx", "wrangler", "pages", "deploy", str(deploy_dir),
           "--project-name", project, "--commit-dirty=true"]
    cleanup_tmp = tmp
    if branch == "production":
        cmd.extend(["--branch", "main"])
    else:
        cmd.extend(["--branch", f"preview-v{branch}"])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(skill_dir), env=env)
    try:
        shutil.rmtree(cleanup_tmp)
    except Exception:
        pass
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return None
    for line in (result.stdout + result.stderr).splitlines():
        if "Deployment complete" in line:
            m = re.search(r'https://[a-z0-9-]+\.' + re.escape(project) + r'\.pages\.dev', line)
            if m:
                return m.group(0)
    return None


def _purge_old_deployments(skill_dir, project, token, account_id):
    """Delete old deployments to force cache refresh."""
    r = subprocess.run(
        ["curl", "-s",
         f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments",
         "-H", f"Authorization: Bearer {token}"],
        capture_output=True, text=True
    )
    deployments = json.loads(r.stdout).get("result", [])
    prod_deps = [d for d in deployments if d.get("deployment_trigger", {}).get("type") == "manual" or d.get("environment") != "preview"]
    if len(prod_deps) > 1:
        for dep in prod_deps[1:]:
            dep_id = dep.get("id")
            subprocess.run(
                ["curl", "-s", "-X", "DELETE",
                 f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments/{dep_id}",
                 "-H", f"Authorization: Bearer {token}"],
                capture_output=True, text=True
            )
        print(f"🗑️  已清除 {len(prod_deps)-1} 个旧部署")


def _get_account_id(skill_dir, token):
    """Get Cloudflare account ID from wrangler cache or API."""
    wrangler_cache = skill_dir / ".wrangler" / "cache" / "wrangler-account.json"
    if wrangler_cache.exists():
        return json.loads(wrangler_cache.read_text()).get("account", {}).get("id")
    r = subprocess.run(
        ["curl", "-s", "https://api.cloudflare.com/client/v4/accounts",
         "-H", f"Authorization: Bearer {token}"],
        capture_output=True, text=True
    )
    accounts = json.loads(r.stdout).get("result", [])
    return accounts[0]["id"] if accounts else None


def _get_token():
    """Get Cloudflare API token from env or TOOLS.md."""
    return (os.environ.get("CLOUDFLARE_API_TOKEN")
            or _get_cfg_val("CLOUDFLARE_API_TOKEN")
            or _get_cfg_val("CF_API_TOKEN"))


def _sync_version(skill_dir, ver):
    """Sync version number to index.html, SKILL.md, base.css."""
    # Regenerate index.html from index-body.html
    body_file = skill_dir / "index-body.html"
    index_html = skill_dir / "index.html"
    if body_file.exists():
        body = body_file.read_text("utf-8")
        body = re.sub(r'v\d+\.\d+\.\d+', f'v{ver}', body)
        body_file.write_text(body, "utf-8")
        style_m = re.search(r'<style>(.*?)</style>', body, re.DOTALL)
        page_style = style_m.group(1).strip() if style_m else ""
        clean_body = re.sub(r'<style>.*?</style>', '', body, flags=re.DOTALL).strip()
        page_info = {
            "title": "报告专家 · 技能介绍",
            "desc": f"为 AI Agent 设计的报告生成与站点部署技能 · {ver}",
            "date": date.today().isoformat(),
            "category": "",
            "body": clean_body,
            "style": page_style,
        }
        page_html = generate_page_html(page_info, SITE_URL, no_chrome=True)
        index_html.write_text(page_html, "utf-8")
        print(f"📄 介绍页已重新生成: v{ver}")
    elif index_html.exists():
        ih = index_html.read_text("utf-8")
        ih = re.sub(r'v\d+\.\d+\.\d+', f'v{ver}', ih, count=1)
        index_html.write_text(ih, "utf-8")
        print(f"📄 介绍页版本已同步: v{ver}")
    # Sync version in SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        sm = skill_md.read_text("utf-8")
        sm = re.sub(r'v\d+\.\d+\.\d+', f'v{ver}', sm, count=1)
        skill_md.write_text(sm, "utf-8")
        print(f"📄 SKILL.md 版本已同步: v{ver}")
    # Sync version in base.css
    for css_path in [skill_dir / "templates" / "base.css", skill_dir / "styles" / "base.css"]:
        if css_path.exists():
            c = css_path.read_text("utf-8")
            c = re.sub(r'v\d+\.\d+\.\d+', f'v{ver}', c, count=1)
            css_path.write_text(c, "utf-8")


def publish_preview():
    """Step 1-3: Bump version, sync files, deploy to preview, verify."""
    skill_dir = BASE_DIR
    token = _get_token()
    if not token:
        print("❌ 未配置 CLOUDFLARE_API_TOKEN"); return
    project = "report-expert-skill"

    # 1. Auto-bump patch version
    manifest_path = skill_dir / "manifest.json"
    ver = None
    if manifest_path.exists():
        m = json.loads(manifest_path.read_text("utf-8"))
        ver = m.get("version", "0.0.0")
        parts = ver.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        ver = ".".join(parts)
        m["version"] = ver
        for rel in list(m.get("files", {}).keys()):
            fp = skill_dir / rel
            if fp.exists():
                with open(fp, "rb") as f:
                    m["files"][rel]["sha256"] = hashlib.sha256(f.read()).hexdigest()
                    m["files"][rel]["size"] = fp.stat().st_size
        manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2), "utf-8")
        print(f"🔄 版本自动升级: v{ver}")

    # 2. Regenerate index.html + sync version to all files
    if ver:
        _sync_version(skill_dir, ver)

    # 3. Deploy to preview
    print(f"\n🚀 部署到预览环境...")
    preview_url = _deploy_to_cf(skill_dir, project, token, branch=ver)
    if not preview_url:
        print("❌ 预览部署失败"); return
    print(f"\n✅ 预览部署成功")
    print(f"   预览地址: {preview_url}")
    print(f"\n📋 请验证以下内容:")
    print(f"   1. 打开 {preview_url}/manifest.json 确认版本为 v{ver}")
    print(f"   2. 打开 {preview_url}/index.html 确认介绍页版本正确")
    print(f"   3. 打开 {preview_url}/SKILL.md 确认技能文档正确")
    print(f"\n✅ 验证无误后，运行以下命令发布到生产环境:")
    print(f"   python deploy.py publish-prod")


def publish_prod():
    """Step 4: Deploy to production with cache purge."""
    skill_dir = BASE_DIR
    token = _get_token()
    if not token:
        print("❌ 未配置 CLOUDFLARE_API_TOKEN"); return
    project = "report-expert-skill"

    manifest_path = skill_dir / "manifest.json"
    ver = "unknown"
    if manifest_path.exists():
        ver = json.loads(manifest_path.read_text("utf-8")).get("version", "unknown")

    print(f"🚀 发布 v{ver} 到生产环境...")
    prod_url = _deploy_to_cf(skill_dir, project, token, branch="production")
    if not prod_url:
        print("❌ 生产部署失败"); return

    account_id = _get_account_id(skill_dir, token)
    if account_id:
        time.sleep(2)
        _purge_old_deployments(skill_dir, project, token, account_id)

    repo = ""
    if manifest_path.exists():
        repo = json.loads(manifest_path.read_text("utf-8")).get("repository", "")
    print(f"\n✅ 生产环境发布完成: v{ver}")
    if repo:
        print(f"   线上地址: {repo}")
    print(f"   部署地址: {prod_url}")

#!/usr/bin/env python3
"""
End-to-end pipeline for:
1) LinkedIn company mining
2) Email campaign sending (skip already successful records)
3) Dashboard data refresh
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


SCOUT_SCRIPT = "/Users/m1/.codex/skills/linkedin-company-scout/scripts/run_linkedin_company_scout.py"
EMAIL_PUSH_SCRIPT = "/Users/m1/Documents/Playground/email-ops/push_design_services_campaign.py"
DASHBOARD_REFRESH_SCRIPT = "/Users/m1/Documents/Playground/linkedin-dashboard/generate_dashboard_data.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mining + email send + dashboard refresh pipeline.")

    # mining
    parser.add_argument("--keywords", required=True, help="comma-separated keywords")
    parser.add_argument("--count", type=int, default=100, help="target accepted companies per keyword")
    parser.add_argument("--output-dir", required=True, help="output directory for scout json/csv/meta")
    parser.add_argument("--db-path", required=True, help="sqlite db used by scout and email phase")
    parser.add_argument("--max-search-pages", type=int, default=120)
    parser.add_argument("--page-timeout", type=int, default=20)
    parser.add_argument("--linkedin-wait-seconds", type=int, default=120)
    parser.add_argument("--no-heartbeat", action="store_true")
    parser.add_argument("--disable-db-resume", action="store_true")
    parser.add_argument("--debug-port", type=int, default=9222)
    parser.add_argument("--chrome-profile-dir", default=str(Path.home() / ".linkedin-company-scout" / "chrome-profile"))
    parser.add_argument("--linkedin-search-origin", default="FACETED_SEARCH")
    parser.add_argument("--industry-company-vertical-id", default="99")

    # email phase
    parser.add_argument("--send-email", action="store_true", help="enable email sending phase")
    parser.add_argument("--smtp-password", default="", help="smtp password used by email phase")
    parser.add_argument("--send-backend", default="imap-smtp-email", choices=["imap-smtp-email", "smtplib"])
    parser.add_argument("--recipient-override", default="", help="send all emails to this recipient (testing)")
    parser.add_argument("--email-limit", type=int, default=0, help="0 means no limit")
    parser.add_argument("--template-name", default="通用模版")

    # dashboard phase
    parser.add_argument("--refresh-dashboard", action="store_true", help="refresh dashboard data after pipeline")

    return parser.parse_args()


def run_cmd(cmd: List[str], name: str) -> None:
    print(f"[pipeline] start {name}: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {result.returncode}")
    print(f"[pipeline] done {name}")


def run_mining(args: argparse.Namespace) -> None:
    cmd = [
        "python3",
        SCOUT_SCRIPT,
        "--keywords",
        args.keywords,
        "--count",
        str(args.count),
        "--output-dir",
        args.output_dir,
        "--db-path",
        args.db_path,
        "--max-search-pages",
        str(args.max_search_pages),
        "--page-timeout",
        str(args.page_timeout),
        "--linkedin-wait-seconds",
        str(args.linkedin_wait_seconds),
        "--debug-port",
        str(args.debug_port),
        "--chrome-profile-dir",
        args.chrome_profile_dir,
        "--linkedin-search-origin",
        args.linkedin_search_origin,
        "--industry-company-vertical-id",
        args.industry_company_vertical_id,
    ]
    if args.no_heartbeat:
        cmd.append("--no-heartbeat")
    if args.disable_db_resume:
        cmd.append("--disable-db-resume")
    run_cmd(cmd, "mining")


def run_email_phase(args: argparse.Namespace) -> None:
    if not args.send_email:
        print("[pipeline] skip email phase (use --send-email to enable)")
        return
    if not args.smtp_password:
        raise RuntimeError("email phase requires --smtp-password")
    cmd = [
        "python3",
        EMAIL_PUSH_SCRIPT,
        "--source-db",
        args.db_path,
        "--template-name",
        args.template_name,
        "--send",
        "--send-backend",
        args.send_backend,
        "--smtp-password",
        args.smtp_password,
    ]
    if args.recipient_override.strip():
        cmd.extend(["--recipient-override", args.recipient_override.strip()])
    if args.email_limit > 0:
        cmd.extend(["--limit", str(args.email_limit)])
    # Do NOT pass --allow-resend by default: this guarantees successful records are not resent.
    run_cmd(cmd, "email")


def run_dashboard_phase(args: argparse.Namespace) -> None:
    if not args.refresh_dashboard:
        print("[pipeline] skip dashboard refresh (use --refresh-dashboard to enable)")
        return
    cmd = ["python3", DASHBOARD_REFRESH_SCRIPT]
    run_cmd(cmd, "dashboard")


def main() -> int:
    args = parse_args()
    try:
        run_mining(args)
        run_email_phase(args)
        run_dashboard_phase(args)
    except Exception as exc:
        print(f"[pipeline] failed: {exc}", file=sys.stderr)
        return 1
    print("[pipeline] all steps completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

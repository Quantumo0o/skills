#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from license_gate import ensure_license, machine_fingerprint


def _default_path(name: str) -> Path:
    """Look in script's own directory first, then fall back to standard locations."""
    script_dir = Path(__file__).resolve().parent
    candidates = {
        "capture": [
            script_dir / "最终完结版.py",
            script_dir / "淘宝skills" / "核心数据" / "最终完结版.py",
            Path.home() / "Desktop" / "最终完结版.py",
            Path.home() / "Desktop" / "淘宝skills" / "核心数据" / "最终完结版.py",
        ],
        "inspection": [
            script_dir / "shop_inspection_fresh_run_universal.py",
            script_dir / "shop_inspection_fresh_run.py",
            Path.home() / "Desktop" / "shop_inspection_fresh_run_universal.py",
            Path.home() / "Desktop" / "shop_inspection_fresh_run.py",
        ],
        "parse": [
            script_dir / "parse_taobao_report.py",
            Path.home() / "Desktop" / "openclawskills" / "openclaw-web-extract" / "parse_taobao_report.py",
        ],
    }
    for p in candidates[name]:
        if p.exists():
            return p
    return candidates[name][0]


def _run(cmd: list[str], *, required: bool) -> None:
    print("\n>>", " ".join(cmd))
    code = subprocess.call(cmd)
    if code != 0 and required:
        raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run Taobao merchant flow: capture -> inspection -> parse"
    )
    p.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable for all child scripts (default: current interpreter)",
    )
    p.add_argument(
        "--capture-script",
        default=str(_default_path("capture")),
        help="Path to 最终完结版.py",
    )
    p.add_argument(
        "--inspection-script",
        default=str(_default_path("inspection")),
        help="Path to shop_inspection_fresh_run_universal.py",
    )
    p.add_argument(
        "--parse-script",
        default=str(_default_path("parse")),
        help="Path to parse_taobao_report.py",
    )
    p.add_argument("--skip-capture", action="store_true")
    p.add_argument("--skip-inspection", action="store_true")
    p.add_argument("--skip-parse", action="store_true")
    p.add_argument(
        "--inspection-modules",
        default="evaluation,frontend,backend,shipping",
        help="Modules for inspection script if it supports --modules",
    )
    p.add_argument(
        "--license-file",
        default="",
        help="License activation file path (default: <skill_root>/license/license.json)",
    )
    p.add_argument(
        "--card-key",
        default="",
        help="Card key for first activation (if omitted and no license, script will prompt)",
    )
    p.add_argument(
        "--show-machine-id",
        action="store_true",
        help="Print machine fingerprint and exit",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    py = Path(args.python)
    if not py.exists():
        raise SystemExit(f"Python executable not found: {py}")

    capture_script = Path(args.capture_script)
    inspection_script = Path(args.inspection_script)
    parse_script = Path(args.parse_script)
    skill_root = Path(__file__).resolve().parents[1]
    default_license = skill_root / "license" / "license.json"
    license_file = Path(args.license_file).resolve() if args.license_file else default_license

    if args.show_machine_id:
        print("Machine ID:", machine_fingerprint())
        return 0

    activation = ensure_license(license_file, key_from_cli=args.card_key)
    print(f"Python: {py}")
    print(f"Capture script: {capture_script}")
    print(f"Inspection script: {inspection_script}")
    print(f"Parse script: {parse_script}")
    print(f"License file: {license_file}")
    print(f"Plan: {activation.get('plan')}  ExpiresAt: {activation.get('expires_at')}")

    if not args.skip_capture:
        if not capture_script.exists():
            raise SystemExit(f"Capture script not found: {capture_script}")
        _run([str(py), str(capture_script)], required=True)

    if not args.skip_inspection:
        if not inspection_script.exists():
            raise SystemExit(f"Inspection script not found: {inspection_script}")
        _run(
            [
                str(py),
                str(inspection_script),
                "--modules",
                str(args.inspection_modules),
            ],
            required=True,
        )

    if not args.skip_parse:
        if not parse_script.exists():
            print(f"[WARN] Parse script not found, skip: {parse_script}")
        else:
            _run([str(py), str(parse_script)], required=False)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


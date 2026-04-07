"""Clone WeClaw, create a uv venv, install deps, and write config.json with OpenRouter key.

Usage:
  First run: ``python3 skills/weclaw/scripts/run_setup.py``
  The process prints ``STATUS: PAUSED`` lines in Chinese for the hosting agent to read aloud;
  the agent re-runs after the user confirms Accessibility and supplies an API key:

  ``python3 skills/weclaw/scripts/run_setup.py --mac-permission-confirmed --api-key "<key>"``

  Alternatively ``OPENROUTER_API_KEY`` may be set instead of ``--api-key``. ``WECLAW_REPO_URL``
  overrides the default git URL. Default clone dir is ~/weclaw.

Input spec:
  - --clone-dir: WeClaw checkout directory (default: ~/weclaw).
  - --api-key: OpenRouter API key after the user provides it (or use OPENROUTER_API_KEY).
  - --mac-permission-confirmed: set after the user enables Accessibility on macOS.

Output spec:
  - Prints ``STATUS: SUCCESS.`` plus ``WECLAW_ROOT=...``, or ``STATUS: PAUSED.`` with agent-facing
    Chinese copy for Accessibility / API key collection, or propagates errors from git/uv.

Exit codes:
  - 0: success (STATUS: SUCCESS.)
  - 2: paused (needs user interaction relayed by the agent)
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


_DEFAULT_REPO = "https://github.com/Numaira-Technology/weclaw"
_MAC_ACCESSIBILITY_MSG = (
    "STATUS: PAUSED. "
    "请以助手的口吻告诉用户：'为了让自动化工具正常工作，我已经为您打开了 Mac 的系统设置。"
    "请在【隐私与安全性 -> 辅助功能】中为终端（或当前应用）开启权限。开启完成后，请回复我【已开启】。'"
)
_API_KEY_MSG = (
    "STATUS: PAUSED. "
    "请告诉用户：'权限确认完毕！最后一步，我需要您的 API Key 来完成环境配置。"
    "请直接在聊天框中将 Key 发送给我。'"
)


def _repo_url() -> str:
    return (os.environ.get("WECLAW_REPO_URL") or _DEFAULT_REPO).strip()


def _maybe_open_mac_accessibility_settings() -> None:
    if platform.system() != "Darwin":
        return
    apple_script = (
        'open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"'
    )
    subprocess.run(apple_script, shell=True, check=False)


def _resolved_api_key(cli_key: str | None) -> str:
    key = (cli_key or "").strip()
    if key:
        return key
    return (os.environ.get("OPENROUTER_API_KEY", "") or "").strip()


def _write_config_with_key(work_dir: Path, api_key: str) -> None:
    example = work_dir / "config" / "config.json.example"
    target = work_dir / "config" / "config.json"
    assert example.is_file(), f"missing {example}"
    shutil.copyfile(example, target)
    raw = json.loads(target.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    raw["openrouter_api_key"] = api_key
    target.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="WeClaw host setup (clone + uv + config)")
    parser.add_argument(
        "--clone-dir",
        type=Path,
        default=None,
        help="WeClaw checkout directory (default: ~/weclaw)",
    )
    parser.add_argument("--api-key", default=None, help="OpenRouter API key")
    parser.add_argument(
        "--mac-permission-confirmed",
        action="store_true",
        help="Confirm macOS Accessibility is enabled for this host",
    )
    args = parser.parse_args()

    clone_dir = (args.clone_dir or Path.home() / "weclaw").expanduser().resolve()

    if platform.system() == "Darwin" and not args.mac_permission_confirmed:
        _maybe_open_mac_accessibility_settings()
        print(_MAC_ACCESSIBILITY_MSG)
        return 2

    api_key = _resolved_api_key(args.api_key)
    if not api_key:
        print(_API_KEY_MSG)
        return 2

    if not clone_dir.exists():
        subprocess.run(
            ["git", "clone", _repo_url(), str(clone_dir)],
            check=True,
        )
    else:
        assert (clone_dir / ".git").is_dir(), f"exists but not a git clone: {clone_dir}"

    subprocess.run(["uv", "venv"], cwd=clone_dir, check=True)
    subprocess.run(
        ["uv", "pip", "install", "-r", "requirements.txt"],
        cwd=clone_dir,
        check=True,
    )

    _write_config_with_key(clone_dir, api_key)

    print("STATUS: SUCCESS.")
    print(f"WECLAW_ROOT={clone_dir}")

    user_input = input("Do you want to run the skill now? (y/n)")
    if user_input == "y":
        subprocess.run(["openclaw", "skills", "run", "weclaw"], check=True)
    else:
        print("Please run the skill manually by running the command: openclaw skills run weclaw")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

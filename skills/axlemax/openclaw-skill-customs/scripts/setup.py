#!/usr/bin/env python3
"""
Leap 报关技能初始化配置脚本（备用方案）。

推荐方式：在 OpenClaw skill 设置界面直接配置 LEAP_API_KEY 环境变量。
此脚本仅在无法通过平台 UI 配置时使用。

用法: python scripts/setup.py

零外部依赖 — 仅使用 Python 标准库。
"""
import getpass
import json
import os
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "openclaw" / "credentials"
DEFAULT_BASE_URL = "https://platform.daofeiai.com"


def load_existing() -> dict:
    result = {}
    if CREDENTIALS_PATH.exists():
        for line in CREDENTIALS_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                result[k.strip()] = v.strip()
    return result


def save_credentials(data: dict):
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Leap OpenClaw Skill Credentials", "# 请勿分享此文件或提交至 Git", ""]
    for k, v in data.items():
        lines.append(f"{k}={v}")
    CREDENTIALS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    CREDENTIALS_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)


def verify_key(api_key: str, base_url: str) -> bool:
    req = urllib.request.Request(
        f"{base_url}/api/v1/process/tasks?limit=1",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def mask_key(key: str) -> str:
    if len(key) <= 8:
        return "****"
    return key[:4] + "****" + key[-4:]


def main():
    print()
    print("🦞 Leap 报关技能 — 备用配置向导")
    print("=" * 45)
    print()
    print("⚠️  推荐方式：在 OpenClaw skill 设置界面配置 LEAP_API_KEY")
    print("   此脚本仅在无法通过平台 UI 配置时使用。")
    print()

    existing = load_existing()
    data = dict(existing)

    # 配置 Base URL
    current_url = existing.get("LEAP_API_BASE_URL", DEFAULT_BASE_URL)
    print(f"📡 API 服务地址（当前：{current_url}）")
    print(f"   直接回车使用默认 [{DEFAULT_BASE_URL}]，或输入自定义地址：")
    url_input = input("   > ").strip()
    base_url = url_input if url_input else current_url
    data["LEAP_API_BASE_URL"] = base_url
    print(f"   ✅ 使用地址：{base_url}\n")

    # 输入 API Key（隐藏输入）
    if "LEAP_API_KEY" in existing:
        masked = mask_key(existing["LEAP_API_KEY"])
        print(f"🔑 检测到已保存的 API Key（{masked}）")
        print("   直接回车保留现有 Key，或重新输入新的 Key：")
        new_key = getpass.getpass("   Key（输入时不显示）> ").strip()
        api_key = new_key if new_key else existing["LEAP_API_KEY"]
    else:
        print("🔑 请输入您的 Leap API Key")
        print("   （可在 Leap 开放平台「API Key 管理」页面获取）")
        print("   注意：输入时不会显示任何字符，这是正常的安全措施")
        api_key = ""
        while not api_key:
            api_key = getpass.getpass("   Key（输入时不显示）> ").strip()
            if not api_key:
                print("   ⚠️  Key 不能为空，请重新输入")

    data["LEAP_API_KEY"] = api_key
    print(f"   ✅ Key 已接收（{mask_key(api_key)}）\n")

    # 验证 Key
    print("🔍 正在验证 API Key 连通性...")
    valid = verify_key(api_key, base_url)

    if valid:
        print("   ✅ 验证通过！API Key 有效")
    else:
        print("   ⚠️  验证失败（网络问题或 Key 无效）")
        confirm = input("   继续保存？[Y/n] > ").strip().lower()
        if confirm == "n":
            print("   已取消，配置未保存。")
            sys.exit(0)

    save_credentials(data)
    print()
    print(f"💾 配置已安全保存至：{CREDENTIALS_PATH}")
    print(f"   文件权限：600（仅您的账户可读）")
    print()
    print("🎉 配置完成！您现在可以开始使用报关技能了。")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
vod_load_env.py — 腾讯云 VOD Skill 环境变量自动加载工具

功能：
  扫描以下文件，如果文件中包含指定的环境变量 KEY，则将该文件中的所有
  KEY=VALUE 行加载到当前进程的 os.environ 中（不覆盖已存在的值）：
    /etc/environment
    /etc/profile
    ~/.bashrc
    ~/.profile
    ~/.bash_profile
    ~/.env

  目标变量（只要文件中存在其中任意一个，该文件就会被加载）：
    TENCENTCLOUD_SECRET_ID       （必须）
    TENCENTCLOUD_SECRET_KEY      （必须）
    TENCENTCLOUD_VOD_AIGC_TOKEN  （可选，AIGC LLM Chat 专用）
    TENCENTCLOUD_VOD_SUB_APP_ID  （可选，子应用 ID）

用法（在其他脚本中调用）：
    from vod_load_env import ensure_env_loaded
    ensure_env_loaded()
"""

import os
import re
import sys

# 需要检测的目标变量
_TARGET_VARS = {
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_VOD_AIGC_TOKEN",
    "TENCENTCLOUD_VOD_SUB_APP_ID",
}

# 必须的变量（缺少时报错）
_REQUIRED_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
]

# 可选的变量（仅在特定场景下需要）
_OPTIONAL_VARS = {
    "TENCENTCLOUD_VOD_AIGC_TOKEN": "AIGC LLM Chat（vod_aigc_chat.py）专用",
    "TENCENTCLOUD_VOD_SUB_APP_ID": "子应用操作时使用（可通过 --sub-app-id 参数覆盖）",
}

# 扫描的候选文件列表（按优先级排序）
_ENV_FILES = [
    "/etc/environment",
    "/etc/profile",
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.profile"),
    os.path.expanduser("~/.bash_profile"),
    os.path.expanduser("~/.env"),
]

# KEY=VALUE 行的正则（支持带引号的值）
_KV_RE = re.compile(
    r"""^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['"]?)(.*?)\2\s*$"""
)


def _parse_env_file(filepath: str) -> dict:
    """
    解析一个 shell 风格的环境变量文件，返回 {key: value} 字典。
    支持：
      KEY=value
      export KEY=value
      KEY="value with spaces"
      KEY='value'
      # 注释行（忽略）
    """
    result = {}
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.rstrip("\n")
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                m = _KV_RE.match(line)
                if m:
                    key = m.group(1)
                    value = m.group(3)
                    result[key] = value
    except (OSError, IOError):
        pass
    return result


def _file_contains_target(parsed: dict) -> bool:
    """判断解析结果中是否包含至少一个目标变量。"""
    return bool(_TARGET_VARS & set(parsed.keys()))


def load_env_files(verbose: bool = False) -> dict:
    """
    扫描所有候选文件，将包含目标变量的文件内容加载到 os.environ。
    已存在的环境变量不会被覆盖（setdefault 语义）。

    返回：本次新加载的变量字典 {key: value}
    """
    newly_loaded = {}

    for filepath in _ENV_FILES:
        if not os.path.isfile(filepath):
            if verbose:
                print(f"[load_env] 跳过（不存在）: {filepath}", file=sys.stderr)
            continue

        parsed = _parse_env_file(filepath)

        if not _file_contains_target(parsed):
            if verbose:
                print(f"[load_env] 跳过（无目标变量）: {filepath}", file=sys.stderr)
            continue

        if verbose:
            print(f"[load_env] 加载文件: {filepath}", file=sys.stderr)

        for key, value in parsed.items():
            if key not in os.environ:
                os.environ[key] = value
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[load_env]   设置 {key}={display}", file=sys.stderr)
            else:
                if verbose:
                    print(f"[load_env]   跳过（已存在）: {key}", file=sys.stderr)

    return newly_loaded


def check_required_vars(required: list = None) -> list:
    """
    检查必需的环境变量是否已设置。
    返回缺失的变量名列表（空列表表示全部已设置）。
    """
    if required is None:
        required = _REQUIRED_VARS
    return [k for k in required if not os.environ.get(k)]


def _print_setup_hint(missing_vars: list) -> None:
    """当环境变量加载失败时，向用户打印详细的配置引导提示。"""
    env_files_str = "\n".join(f"    • {f}" for f in _ENV_FILES)
    missing_str = "\n".join(f"    {k}=<your_value>" for k in missing_vars)
    hint = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    腾讯云VOD环境变量未配置                          ║
╚══════════════════════════════════════════════════════════════════╝

以下环境变量缺失：
{missing_str}

密钥可以在腾讯云控制台获取：https://console.cloud.tencent.com/cam/capi
VOD 控制台：https://console.cloud.tencent.com/vod

【配置方式】请自行在以下任一文件中添加上述变量，然后重新发起对话：
{env_files_str}

  示例（以 ~/.profile 为例）：
    # 必须（所有脚本）
    export TENCENTCLOUD_SECRET_ID=<您的 SecretId>
    export TENCENTCLOUD_SECRET_KEY=<您的 SecretKey>

    # 可选（AIGC LLM Chat 专用）
    export TENCENTCLOUD_VOD_AIGC_TOKEN=<您的 AIGC Token>

    # 可选（子应用 ID，也可通过 --sub-app-id 参数指定）
    export TENCENTCLOUD_VOD_SUB_APP_ID=<您的子应用 ID>

⚠️  安全提示：请通过安全渠道（如直接编辑配置文件）配置密钥。

配置完成后，请重新发起对话即可。
"""
    print(hint, file=sys.stderr)


def ensure_env_loaded(
    required: list = None,
    verbose: bool = False,
) -> bool:
    """
    确保必需的环境变量已加载。

    执行流程：
      1. 检查必需变量是否已在 os.environ 中
      2. 如果有缺失，扫描候选文件并加载
      3. 再次检查，返回是否全部就绪

    参数：
      required  — 必须存在的变量列表，默认检查 SECRET_ID / SECRET_KEY
      verbose   — 是否打印加载日志到 stderr

    返回：True 表示所有必需变量均已就绪，False 表示仍有缺失
    """
    if required is None:
        required = _REQUIRED_VARS

    missing_before = check_required_vars(required)
    if not missing_before:
        return True

    if verbose:
        print(
            f"[load_env] 检测到缺失变量: {missing_before}，开始扫描环境变量文件...",
            file=sys.stderr,
        )

    load_env_files(verbose=verbose)

    missing_after = check_required_vars(required)
    if missing_after:
        return False

    if verbose:
        print("[load_env] 所有必需变量已加载完成。", file=sys.stderr)
    return True


# ─── 独立运行时：诊断模式 ───────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="扫描系统环境变量文件并加载腾讯云 VOD 所需变量（诊断模式）"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="显示详细加载日志"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="仅检查当前环境变量状态，不加载"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="模拟执行，显示将要执行的操作但不实际加载环境变量"
    )
    args = parser.parse_args()

    if args.check_only:
        print("=== 腾讯云 VOD 环境变量状态 ===\n")
        print("【必须变量】")
        all_required_ok = True
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                status = f"✅ 已设置 ({display})"
            else:
                status = "❌ 未设置"
                all_required_ok = False
            print(f"  {var}: {status}")

        print("\n【可选变量】")
        for var, desc in _OPTIONAL_VARS.items():
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                status = f"✅ 已设置 ({display})"
            else:
                status = f"⚪ 未设置（{desc}）"
            print(f"  {var}: {status}")

        print()
        if all_required_ok:
            print("✅ 必须变量全部已配置，可以正常使用 VOD Skill。")
            sys.exit(0)
        else:
            print("❌ 必须变量未完整配置，请按提示配置后重试。")
            sys.exit(1)

    # Dry-run 模式：仅显示操作摘要
    if args.dry_run:
        print("=== 模拟执行（Dry-run）===\n")
        print("操作：扫描并加载腾讯云 VOD 环境变量")
        print("\n将要扫描的环境变量文件：")
        for filepath in _ENV_FILES:
            print(f"  - {filepath}")

        print("\n将要查找的环境变量：")
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                print(f"  - {var}: ✅ 已设置 ({display})  [必须]")
            else:
                print(f"  - {var}: ❌ 未设置（将尝试加载）  [必须]")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                print(f"  - {var}: ✅ 已设置 ({display})  [可选]")
            else:
                print(f"  - {var}: ⚪ 未设置  [可选]")

        print("\n不会实际加载环境变量。移除 --dry-run 参数后执行实际操作。")
        sys.exit(0)

    print("=== 扫描环境变量文件 ===", flush=True)
    newly = load_env_files(verbose=True)
    sys.stderr.flush()

    print("\n=== 加载结果 ===")
    print("【必须变量】")
    all_required_ok = True
    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        if val:
            display = val[:4] + "****" if len(val) > 4 else "****"
            status = f"✅ 已设置 ({display})"
        else:
            status = "❌ 未设置"
            all_required_ok = False
        print(f"  {var}: {status}")

    print("【可选变量】")
    for var, desc in _OPTIONAL_VARS.items():
        val = os.environ.get(var, "")
        if val:
            display = val[:4] + "****" if len(val) > 4 else "****"
            status = f"✅ 已设置 ({display})"
        else:
            status = f"⚪ 未设置（{desc}）"
        print(f"  {var}: {status}")

    if newly:
        print(f"\n本次新加载了 {len(newly)} 个变量: {list(newly.keys())}")
    else:
        print("\n未加载任何新变量（已全部设置或文件中无目标变量）")

    if not all_required_ok:
        _print_setup_hint([v for v in _REQUIRED_VARS if not os.environ.get(v)])
        sys.exit(1)
    else:
        print("\n✅ 必须变量全部已配置，可以正常使用 VOD Skill。")

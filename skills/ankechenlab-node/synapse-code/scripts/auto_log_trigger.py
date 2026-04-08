#!/usr/bin/env python3
"""
auto_log_trigger.py — 触发 Synapse auto-log（配置化版本）

用法:
    python3 auto_log_trigger.py /path/to/project
    python3 auto_log_trigger.py --project /path/to/project
    cat /tmp/pipeline_summary.json | python3 auto_log_trigger.py --project /path/to/project

功能:
1. 检查 /tmp/pipeline_summary.json 是否存在
2. 调用内置 auto_log.py 写入 memory 和 log.md
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 日志输出 (IM 友好格式 - 无 ANSI 颜色码)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_info(msg):
    """信息消息 - 用于一般提示"""
    print(f"[INFO] {msg}")


def log_success(msg):
    """成功消息 - 用于完成状态"""
    print(f"[✓] {msg}")


def log_error(msg):
    """错误消息 - 用于失败状态"""
    print(f"[✗] {msg}")


def log_json(data: dict, prefix: str = ""):
    """结构化日志输出 (JSON 格式)"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        **data
    }
    if prefix:
        log_entry["prefix"] = prefix
    print(json.dumps(log_entry, ensure_ascii=False))


def load_config() -> dict:
    """Load configuration from config.json or use defaults."""
    config_file = Path(__file__).parent / "config.json"
    default_config = {
        "paths": {
            "pipeline_summary": "/tmp/pipeline_summary.json"
        },
        "synapse": {
            "knowledge_dir": ".knowledge",
            "memory_dir": ".synapse/memory"
        }
    }

    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config.json, using defaults: {e}")

    return default_config


def check_pipeline_summary(config: dict) -> tuple[bool, Path]:
    """Check if pipeline_summary.json exists."""
    summary_path = Path(config.get("paths", {}).get("pipeline_summary", "/tmp/pipeline_summary.json"))
    return summary_path.exists() and summary_path.stat().st_size > 0, summary_path


def run_auto_log(project: Path, summary_path: Path) -> bool:
    """Run built-in auto_log.py with the pipeline summary."""
    # Use built-in auto_log.py from the same directory
    auto_log_script = Path(__file__).parent / "auto_log.py"

    if not auto_log_script.exists():
        print(f"Error: auto_log.py not found at {auto_log_script}")
        print("This is a critical file — please reinstall synapse-code skill.")
        return False

    try:
        result = subprocess.run(
            ["python3", str(auto_log_script), "--input", str(summary_path), "--project", str(project)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[Auto-Log] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Auto-Log Error] {e.stderr}")
        return False
    except Exception as e:
        print(f"[Auto-Log Error] Unexpected error: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 auto_log_trigger.py /path/to/project")
        print("       python3 auto_log_trigger.py --project /path/to/project")
        print("       cat /tmp/pipeline_summary.json | python3 auto_log_trigger.py --project /path/to/project")
        sys.exit(1)

    # Load configuration
    config = load_config()

    # Parse arguments
    if sys.argv[1] == "--project":
        if len(sys.argv) < 3:
            print("Error: --project requires a path argument")
            sys.exit(1)
        project = Path(sys.argv[2]).resolve()
    else:
        project = Path(sys.argv[1]).resolve()

    if not project.exists():
        log_error(f"项目目录不存在：{project}")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  Synapse Auto-Log")
    print(f"{'=' * 60}")
    print(f"  项目：{project}")
    print(f"{'=' * 60}\n")

    # Check pipeline summary
    print(f"[⟳] [1/2] 检查 Pipeline 摘要...")
    has_summary, summary_path = check_pipeline_summary(config)
    if not has_summary:
        log_error("/tmp/pipeline_summary.json 未找到或为空")
        log_info("请确认 Pipeline 已成功运行")
        sys.exit(1)
    log_success(f"Pipeline 摘要：{summary_path}")

    # Run auto-log
    print(f"[⟳] [2/2] 执行知识沉淀...")
    if not run_auto_log(project, summary_path):
        log_error("知识沉淀失败")
        sys.exit(1)
    log_success("知识沉淀完成")

    print(f"\n{'=' * 60}")
    log_success("Synapse 知识记录完成!")
    print()
    print(f"  查看记录:")
    print(f"  cat {project}/.knowledge/log.md")
    print(f"  cat {project}/.synapse/memory/*/*.md")


if __name__ == "__main__":
    main()

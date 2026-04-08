#!/usr/bin/env python3
"""
run_pipeline.py — 运行代码交付工作流（多模式支持）

用法:
    python3 run_pipeline.py project_name "需求描述"
    python3 run_pipeline.py project_name --input "需求描述" --mode auto

模式说明:
- auto: 自动检测环境，选择最佳模式（默认）
- standalone: 独立模式，直接开发（无需 Pipeline）
- lite: 轻量模式，简化流程（需基础 Pipeline）
- full: 完整模式，6 阶段 SOP（需完整 Pipeline）
"""

import sys
import json
import subprocess
import time
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

def log_warning(msg):
    """警告消息 - 用于注意点"""
    print(f"[⚠] {msg}")

def log_error(msg):
    """错误消息 - 用于失败状态"""
    print(f"[✗] {msg}")

def log_step(step_num, step_name, status="running"):
    """显示步骤进度 - IM 友好格式"""
    icons = {
        "running": "⟳",
        "done": "✓",
        "error": "✗",
        "skip": "○"
    }
    print(f"[{icons[status]} Step {step_num}] {step_name}")

def log_stage_start(stage_num, stage_name):
    """阶段开始通知 - IM 友好"""
    print(f"\n[▶] 开始阶段 {stage_num}: {stage_name}")

def log_stage_complete(stage_num, stage_name, duration=None):
    """阶段完成通知 - IM 友好"""
    msg = f"[✓] 阶段 {stage_num} 完成：{stage_name}"
    if duration:
        msg += f" (耗时 {duration:.1f}秒)"
    print(msg)

def log_progress_text(current: int, total: int, message: str = ""):
    """文本进度通知 - 替代进度条（IM 友好）"""
    percent = int(100 * current / total)
    print(f"[进度 {current}/{total}] {percent}% - {message}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置管理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def load_config() -> dict:
    """Load configuration from config.json or use defaults."""
    config_file = Path(__file__).parent / "config.json"
    default_config = {
        "pipeline": {
            "workspace": "~/pipeline-workspace",
            "enabled": True,
            "auto_log": True,
            "mode": "auto"  # auto, standalone, lite, full
        },
        "paths": {
            "pipeline_script": "~/pipeline-workspace/pipeline.py",
            "pipeline_summary": "/tmp/pipeline_summary.json"
        }
    }

    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)

                # 验证配置结构
                validation_errors = validate_config(config)
                if validation_errors:
                    print(f"{Colors.YELLOW}[警告] 配置文件存在问题:{Colors.RESET}")
                    for error in validation_errors:
                        print(f"  - {error}")
                    print(f"{Colors.YELLOW}  使用默认值修复...{Colors.RESET}\n")

                # 合并默认配置
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except json.JSONDecodeError as e:
            print(f"{Colors.RED}[错误] config.json 格式错误：{e}{Colors.RESET}")
            print(f"{Colors.YELLOW}  使用默认配置...{Colors.RESET}\n")
        except IOError as e:
            print(f"{Colors.RED}[错误] 无法读取 config.json: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}  使用默认配置...{Colors.RESET}\n")

    return default_config


def validate_config(config: dict) -> list:
    """
    验证配置文件的正确性

    Returns:
        list: 错误消息列表，空列表表示配置有效
    """
    errors = []

    # 检查必需字段
    if "pipeline" not in config:
        errors.append("缺少 'pipeline' 配置项")
    else:
        pipeline = config["pipeline"]
        if not isinstance(pipeline, dict):
            errors.append("'pipeline' 必须是对象")
        else:
            # 检查 workspace 路径
            if "workspace" in pipeline:
                workspace = str(pipeline["workspace"])
                if workspace.startswith("~"):
                    # ~ 路径是有效的，会在 expand_path 中处理
                    pass
                elif not Path(workspace).is_absolute():
                    errors.append(f"'pipeline.workspace' 建议使用绝对路径或 ~ 开头：{workspace}")

            # 检查 mode 值
            valid_modes = ["auto", "standalone", "lite", "full"]
            if "mode" in pipeline and pipeline["mode"] not in valid_modes:
                errors.append(f"'pipeline.mode' 必须是 {valid_modes} 之一，当前为：{pipeline['mode']}")

    # 检查 paths 配置
    if "paths" in config:
        paths = config["paths"]
        if not isinstance(paths, dict):
            errors.append("'paths' 必须是对象")
        else:
            # 检查 pipeline_script 路径
            if "pipeline_script" in paths:
                script_path = str(paths["pipeline_script"])
                if not script_path.startswith("~") and not Path(script_path).is_absolute():
                    errors.append(f"'paths.pipeline_script' 应使用绝对路径或 ~ 开头：{script_path}")

    return errors


def expand_path(path: str) -> Path:
    """Expand ~ to home directory."""
    return Path(path).expanduser()


def detect_environment(config: dict) -> dict:
    """
    检测用户环境，返回推荐模式

    检测项:
    1. Pipeline workspace 是否存在
    2. pipeline.py 是否存在
    3. 是否有完整 Pipeline 功能
    """
    result = {
        "has_git": False,
        "has_pipeline_workspace": False,
        "has_pipeline_script": False,
        "has_full_pipeline": False,
        "recommended_mode": "standalone",
        "message": ""
    }

    # 检测 git
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"],
                      capture_output=True, check=True)
        result["has_git"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 检测 Pipeline workspace
    pipeline_workspace = expand_path(config.get("pipeline", {}).get("workspace", "~/pipeline-workspace"))
    if pipeline_workspace.exists():
        result["has_pipeline_workspace"] = True

    # 检测 pipeline.py
    pipeline_script = expand_path(config.get("paths", {}).get("pipeline_script", "~/pipeline-workspace/pipeline.py"))
    if pipeline_script.exists():
        result["has_pipeline_script"] = True
        # 简单检查是否有完整功能（6 阶段）
        content = pipeline_script.read_text()
        if all(x in content for x in ["REQ", "ARCH", "DEV", "INT", "QA", "DEPLOY"]):
            result["has_full_pipeline"] = True

    # 推荐模式
    if result["has_full_pipeline"]:
        result["recommended_mode"] = "full"
        result["message"] = "检测到完整 Pipeline，使用 6 阶段 SOP 流程"
    elif result["has_pipeline_script"]:
        result["recommended_mode"] = "lite"
        result["message"] = "检测到基础 Pipeline，使用简化流程"
    else:
        result["recommended_mode"] = "standalone"
        result["message"] = "未检测到 Pipeline，使用独立开发模式（直接交付代码）"

    return result


def run_standalone_mode(project_name: str, input_text: str, verbose: bool = False) -> bool:
    """
    独立模式：无需 Pipeline，直接开发

    流程：分析需求 → 生成代码 → 简单测试
    """
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}🔧 独立开发模式{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"  {Colors.GREEN}项目:{Colors.RESET} {project_name}")
    print(f"  {Colors.GREEN}需求:{Colors.RESET} {input_text}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

    log_info("此模式下，Claude 将直接分析需求并生成代码")
    log_info("适合：快速原型、简单功能、无 Pipeline 环境")
    print()

    # 在 standalone 模式下，Claude 直接处理，无需调用外部脚本
    # 这里返回 True 表示模式切换成功，实际开发由 Claude 完成
    return True


def run_lite_mode(project_name: str, input_text: str, config: dict, verbose: bool = False) -> bool:
    """
    轻量模式：简化 Pipeline 流程

    流程：REQ → DEV → QA（3 阶段）
    """
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}🚀 轻量 Pipeline 模式（3 阶段）{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"  {Colors.GREEN}项目:{Colors.RESET} {project_name}")
    print(f"  {Colors.GREEN}需求:{Colors.RESET} {input_text}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

    log_info("执行流程：REQ(需求分析) → DEV(代码开发) → QA(质量检查)")
    log_info("适合：大多数功能开发场景")
    print()

    pipeline_script = expand_path(config.get("paths", {}).get("pipeline_script", "~/pipeline-workspace/pipeline.py"))

    # 验证 Pipeline 脚本存在
    if not pipeline_script.exists():
        log_error(f"Pipeline 脚本不存在：{pipeline_script}")
        log_info("请确认 pipeline-workspace 已正确配置")
        log_info(f"配置路径：{config.get('paths', {}).get('pipeline_script', '~/pipeline-workspace/pipeline.py')}")
        return False

    cmd = [
        "python3", str(pipeline_script), "run-pipeline", project_name,
        "--input", input_text,
        "--mode", "lite"
    ]

    if verbose:
        cmd.append("--verbose")

    log_info(f"Pipeline 脚本：{pipeline_script}")
    print()

    # 显示进度动画
    start_time = time.time()
    lite_stages = [(1, "REQ", "需求分析"), (2, "DEV", "代码开发"), (3, "QA", "质量检查")]
    total_stages = len(lite_stages)

    try:
        log_step(1, "需求分析 (REQ)", "running")
        log_progress(0, total_stages, "执行 REQ 阶段...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        elapsed = time.time() - start_time

        if result.returncode == 0:
            log_step(1, "需求分析 (REQ)", "done")
            log_progress(total_stages, total_stages, "Pipeline 执行完成")
            if verbose and result.stdout:
                print(result.stdout)
            return True
        else:
            log_step(1, "需求分析 (REQ)", "error")
            log_error(f"Pipeline 错误：{result.stderr[:500] if result.stderr else '未知错误'}")
            return False

    except subprocess.TimeoutExpired:
        log_step(1, "需求分析 (REQ)", "error")
        log_error(f"Pipeline 执行超时（10 分钟）")
        log_info("如果需求复杂，建议使用 --mode full 或拆分需求")
        return False

    except FileNotFoundError:
        log_error(f"Pipeline 脚本未找到：{pipeline_script}")
        return False

    except Exception as e:
        log_error(f"未知错误：{e}")
        return False


def run_full_mode(project_name: str, input_text: str, config: dict, verbose: bool = False) -> bool:
    """
    完整模式：6 阶段 SOP Pipeline

    流程：REQ → ARCH → DEV → INT → QA → DEPLOY
    """
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}⚡ 完整 Pipeline 模式（6 阶段 SOP）{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"  {Colors.GREEN}项目:{Colors.RESET} {project_name}")
    print(f"  {Colors.GREEN}需求:{Colors.RESET} {input_text}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

    stages = [
        (1, "REQ", "需求分析"),
        (2, "ARCH", "架构设计"),
        (3, "DEV", "代码开发"),
        (4, "INT", "集成测试"),
        (5, "QA", "质量保障"),
        (6, "DEPLOY", "部署上线"),
    ]

    log_info("执行流程：" + " → ".join([f"{abbr}({name})" for _, abbr, name in stages]))
    log_info("适合：大型项目、企业级应用、需要严格质量把控")
    print()

    pipeline_script = expand_path(config.get("paths", {}).get("pipeline_script", "~/pipeline-workspace/pipeline.py"))

    # 验证 Pipeline 脚本存在
    if not pipeline_script.exists():
        log_error(f"Pipeline 脚本不存在：{pipeline_script}")
        log_info("请确认 pipeline-workspace 已正确配置")
        return False

    cmd = [
        "python3", str(pipeline_script), "run-pipeline", project_name,
        "--input", input_text,
        "--mode", "full"
    ]

    if verbose:
        cmd.append("--verbose")

    log_info(f"Pipeline 脚本：{pipeline_script}")
    print()

    start_time = time.time()
    try:
        # 显示各阶段进度
        total_stages = len(stages)
        completed_stages = 0

        for stage_num, stage_abbr, stage_name in stages:
            log_step(stage_num, f"{stage_abbr} - {stage_name}", "running")
            log_progress(completed_stages, total_stages, f"执行 {stage_abbr} 阶段...")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 分钟超时
        elapsed = time.time() - start_time

        if result.returncode == 0:
            # 更新所有阶段为完成状态
            completed_stages = total_stages
            for stage_num, stage_abbr, stage_name in stages:
                log_step(stage_num, f"{stage_abbr} - {stage_name}", "done")
            log_progress(completed_stages, total_stages, "Pipeline 执行完成")

            print()
            log_success(f"Pipeline 执行成功，耗时 {elapsed:.1f} 秒")
            if verbose and result.stdout:
                print(result.stdout)
            return True
        else:
            # 尝试从输出中解析当前阶段
            error_stage = _parse_error_stage(result.stderr or result.stdout)
            log_step(error_stage[0], f"{error_stage[1]} - {error_stage[2]}", "error")
            log_error(f"Pipeline 错误：{result.stderr[:500] if result.stderr else '未知错误'}")
            return False

    except subprocess.TimeoutExpired:
        for stage_num, stage_abbr, stage_name in stages:
            log_step(stage_num, f"{stage_abbr} - {stage_name}", "error")
        log_error(f"Pipeline 执行超时（30 分钟）")
        log_info("大型项目建议拆分为多个小需求")
        return False

    except FileNotFoundError:
        log_error(f"Pipeline 脚本未找到：{pipeline_script}")
        return False

    except Exception as e:
        log_error(f"未知错误：{e}")
        return False


def _parse_error_stage(output: str) -> tuple:
    """
    从错误输出中解析失败的阶段

    Returns:
        tuple: (stage_num, stage_abbr, stage_name)
    """
    stages = {
        "REQ": (1, "REQ", "需求分析"),
        "ARCH": (2, "ARCH", "架构设计"),
        "DEV": (3, "DEV", "代码开发"),
        "INT": (4, "INT", "集成测试"),
        "QA": (5, "QA", "质量保障"),
        "DEPLOY": (6, "DEPLOY", "部署上线"),
    }

    if not output:
        return (1, "REQ", "需求分析")  # 默认返回第一阶段

    output_upper = output.upper()
    for abbr, stage_info in stages.items():
        if abbr in output_upper or f"[{abbr}]" in output_upper or f"【{abbr}】" in output_upper:
            return stage_info

    return (1, "REQ", "需求分析")  # 默认返回第一阶段


def run_pipeline(project_name: str, input_text: str, config: dict, mode: str = "auto", verbose: bool = False) -> bool:
    """Run pipeline in specified mode."""

    # 自动检测环境
    if mode == "auto":
        env = detect_environment(config)

        # 显示环境检测结果
        print(f"\n{Colors.CYAN}┌{'─' * 58}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}🔍 环境检测{Colors.RESET}{Colors.CYAN}{' ' * 44}│{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * 58}┤{Colors.RESET}")

        checks = [
            (env["has_git"], "Git 仓库"),
            (env["has_pipeline_workspace"], "Pipeline Workspace"),
            (env["has_pipeline_script"], "Pipeline 脚本"),
            (env["has_full_pipeline"], "完整 Pipeline (6 阶段)"),
        ]

        for passed, name in checks:
            icon = "✓" if passed else "○"
            color = Colors.GREEN if passed else Colors.YELLOW
            print(f"{Colors.CYAN}│{Colors.RESET}  {color}[{icon}] {name}{Colors.RESET}{Colors.CYAN}{' ' * (55 - len(name))}│{Colors.RESET}")

        print(f"{Colors.CYAN}├{'─' * 58}┤{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GREEN}推荐模式：{mode if mode != 'auto' else env['recommended_mode']}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}说明：{env['message']}{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 58}┘{Colors.RESET}")
        print()

        mode = env["recommended_mode"]

    # 根据模式执行
    if mode == "standalone":
        return run_standalone_mode(project_name, input_text, verbose)
    elif mode == "lite":
        return run_lite_mode(project_name, input_text, config, verbose)
    elif mode == "full":
        return run_full_mode(project_name, input_text, config, verbose)
    else:
        log_error(f"未知模式：{mode}")
        log_info("可用模式：auto, standalone, lite, full")
        return False


def trigger_auto_log(config: dict) -> bool:
    """Trigger auto-log after successful pipeline execution."""
    auto_log_script = Path(__file__).parent / "auto_log_trigger.py"
    if not auto_log_script.exists():
        return False

    pipeline_summary = expand_path(config.get("paths", {}).get("pipeline_summary", "/tmp/pipeline_summary.json"))
    if not pipeline_summary.exists():
        return True  # No summary to log

    try:
        result = subprocess.run(
            ["python3", str(auto_log_script), str(pipeline_summary)],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Auto-log warning: {e}")
        return True  # Don't fail the whole process


def main():
    if len(sys.argv) < 3:
        print()
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}  Synapse Code Pipeline 运行器{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print()
        print(f"  {Colors.GREEN}用法:{Colors.RESET} python3 run_pipeline.py <项目名称> \"需求描述\" [选项]")
        print()
        print(f"  {Colors.GREEN}模式:{Colors.RESET}")
        print(f"    {Colors.YELLOW}auto{Colors.RESET}       - 自动检测环境（默认）")
        print(f"    {Colors.YELLOW}standalone{Colors.RESET} - 独立开发（无需 Pipeline）")
        print(f"    {Colors.YELLOW}lite{Colors.RESET}       - 简化 Pipeline（3 阶段）")
        print(f"    {Colors.YELLOW}full{Colors.RESET}       - 完整 Pipeline（6 阶段 SOP）")
        print()
        print(f"  {Colors.GREEN}选项:{Colors.RESET}")
        print(f"    {Colors.YELLOW}--mode <mode>{Colors.RESET}     - 指定运行模式")
        print(f"    {Colors.YELLOW}--verbose{Colors.RESET}         - 详细输出")
        print()
        print(f"  {Colors.GREEN}示例:{Colors.RESET}")
        print(f"    python3 run_pipeline.py my-project \"实现登录功能\"")
        print(f"    python3 run_pipeline.py my-project \"添加用户注册\" --mode lite")
        print(f"    python3 run_pipeline.py my-project \"设计电商系统\" --mode full --verbose")
        print()
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print()
        sys.exit(1)

    project_name = sys.argv[1]
    input_text = sys.argv[2]

    # Parse optional arguments
    mode = "auto"
    verbose = False
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--mode":
            if i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
                i += 1
        elif arg == "--verbose" or arg == "-v":
            verbose = True
        elif arg.startswith("--"):
            log_warning(f"未知选项：{arg}")
        i += 1

    # 加载并验证配置
    log_info("加载配置文件...")
    config = load_config()

    # 执行 Pipeline
    success = run_pipeline(project_name, input_text, config, mode, verbose)

    # 显示结果
    print()
    print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
    if success:
        log_success("Pipeline 执行成功")
        # Auto-log only in lite/full modes
        if mode in ["lite", "full"] and config.get("pipeline", {}).get("auto_log", True):
            print()
            log_info("正在记录开发经验...")
            trigger_auto_log(config)
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
    else:
        log_error("Pipeline 执行失败")
        log_info("查看日志获取更多详情")
        log_info("如需帮助，运行：python3 run_pipeline.py --help")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

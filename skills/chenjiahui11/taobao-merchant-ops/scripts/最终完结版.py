"""
基于影刀录制的选择器，转换的 Playwright 脚本

完整流程（19步，两次报告生成）：

第一轮：
  1. 自助分析 → 2. 取数报表 → 3. 自动更新 → 4. 最近30天 
  → 5. 报表名称 → 6. 生成报表 → 7. 下载报表 → 8. 返回

第二轮：
  9. 商品维度 → 10. 自动更新 → 11. 最近30天 → 12. 搜索商品(留空) 
  → 13. 一键全选 → 14. 报表名称 → 15. 生成报表 → 16. 下载报表 → 17. Windows保存
"""

import json
import random
import time
import sys
import os
import argparse
import platform
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from playwright.sync_api import sync_playwright, Page, FrameLocator


# ============ 防检测 ============

def human_click(target, selector, offset_range=5):
    """使用 locator.click(position) 避免坐标系问题"""
    locator = target.locator(selector).first
    offset_x = random.uniform(-offset_range, offset_range)
    offset_y = random.uniform(-offset_range, offset_range)
    try:
        box = locator.bounding_box(timeout=5000)
        if box:
            locator.click(
                position={"x": box['width']/2 + offset_x,
                         "y": box['height']/2 + offset_y},
                timeout=5000
            )
        else:
            locator.click(timeout=5000)
    except Exception:
        try:
            locator.click(timeout=5000)
        except Exception:
            pass


def human_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))


# ============ 配置 ============
STORAGE_STATE_FILE = str(Path(__file__).parent / "yingdao_storage_state.json")

CONFIG = {
    "download_dir": str(Path(__file__).parent / "downloads"),
    "run_log_dir": str(Path(__file__).parent / "downloads" / "run_logs"),
    "headless": False,
    "timeout": 30000,
    "report_name": f"生意参谋报表_{datetime.now().strftime('%Y%m%d')}",
    "report_name_goods": f"生意参谋报表_商品_{datetime.now().strftime('%Y%m%d')}",
    "max_retries": 2,
    "strict_mode": True,
    "download_timeout_ms": 120000,
    "use_storage_state": True,
}


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def ensure_output_dirs():
    Path(CONFIG["download_dir"]).mkdir(parents=True, exist_ok=True)
    Path(CONFIG["run_log_dir"]).mkdir(parents=True, exist_ok=True)


def parse_args():
    parser = argparse.ArgumentParser(description="淘宝生意参谋RPA最终版")
    parser.add_argument("--safe-mode", action="store_true", help="一键稳妥配置（strict/no-storage-state/retries/timeout）")
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="页面默认超时毫秒")
    parser.add_argument("--download-timeout-ms", type=int, default=120000, help="下载等待超时毫秒")
    parser.add_argument("--max-retries", type=int, default=2, help="关键步骤最大重试次数")
    parser.add_argument("--strict", action="store_true", help="关键步骤失败即终止")
    parser.add_argument("--no-storage-state", action="store_true", help="不复用本地登录态，强制手动登录")
    return parser.parse_args()


def apply_cli_overrides(args):
    if bool(args.safe_mode):
        CONFIG["strict_mode"] = True
        CONFIG["use_storage_state"] = False
        CONFIG["max_retries"] = 3
        CONFIG["download_timeout_ms"] = 180000
        # Allow explicit flags to override safe defaults when provided.
        if args.headless:
            CONFIG["headless"] = True
        return

    CONFIG["headless"] = bool(args.headless)
    CONFIG["timeout"] = int(args.timeout_ms)
    CONFIG["download_timeout_ms"] = int(args.download_timeout_ms)
    CONFIG["max_retries"] = max(1, int(args.max_retries))
    CONFIG["strict_mode"] = bool(args.strict)
    CONFIG["use_storage_state"] = not bool(args.no_storage_state)


def write_diagnostics():
    info = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "storage_state_path": STORAGE_STATE_FILE,
        "storage_state_exists": Path(STORAGE_STATE_FILE).exists(),
        "config": CONFIG,
    }
    out = Path(CONFIG["run_log_dir"]) / f"diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"🩺 启动诊断: {out}")


def page_state(page):
    try:
        title = page.title()
    except Exception:
        title = ""
    return {"url": page.url, "title": title}


def record_step(step_results, step_no, step_name, ok, detail="", extra=None):
    item = {
        "ts": datetime.now().isoformat(),
        "step_no": step_no,
        "step_name": step_name,
        "ok": bool(ok),
        "detail": detail,
    }
    if extra:
        item["extra"] = extra
    step_results.append(item)


def save_run_summary(step_results, downloads, fatal_error=None):
    summary = {
        "timestamp": datetime.now().isoformat(),
        "ok": fatal_error is None and all(s["ok"] for s in step_results),
        "total_steps": len(step_results),
        "success_steps": sum(1 for s in step_results if s["ok"]),
        "failed_steps": [s for s in step_results if not s["ok"]],
        "downloads": downloads,
        "fatal_error": fatal_error,
    }
    out = Path(CONFIG["run_log_dir"]) / f"run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"📄 运行摘要: {out}")


def ensure_step(ok, step_name):
    if ok:
        return
    if CONFIG["strict_mode"]:
        raise RuntimeError(f"{step_name} 失败，严格模式已中止执行")


def retry_click(click_fn, step_name, retries=None):
    attempts = retries if retries is not None else CONFIG["max_retries"]
    last_err = None
    for _ in range(attempts):
        try:
            click_fn()
            return True
        except Exception as exc:
            last_err = exc
            human_sleep(0.3, 0.8)
    if last_err:
        log(f"  ⚠️ {step_name} 重试失败: {last_err}")
    return False


def build_download_filename(prefix: str, suggested_filename: str | None) -> str:
    suffix = ".xlsx"
    if suggested_filename:
        ext = Path(suggested_filename).suffix
        if ext:
            suffix = ext
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}{suffix}"


def save_error_screenshot(page, step_name):
    try:
        error_dir = Path(CONFIG['download_dir']) / "errors"
        error_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = error_dir / f"error_{step_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=str(screenshot_path))
        log(f"  📸 错误截图已保存: {screenshot_path}")
    except Exception as e:
        log(f"  ⚠️ 截图失败: {e}")


def click_radio(frame, label_text):
    """点击单选按钮，优先用 get_by_label，次选用 XPath"""
    # 策略1: get_by_label（最可靠，自动处理空格/特殊字符）
    try:
        frame.get_by_label(label_text, exact=True).locator('input[type="radio"]').click(timeout=5000)
        return True
    except:
        pass
    # 策略2: XPath
    for xp in [
        f'.//label[normalize-space(.)="{label_text}"]/span[@class="dt-oui-radio"]/input[@type="radio"]',
        f'.//label[normalize-space(.)="{label_text}"]/span/input[@type="radio"]',
        f'.//label[normalize-space(.)="{label_text}"]/input[@type="radio"]',
    ]:
        try:
            human_click(frame, f'xpath={xp}', offset_range=3)
            return True
        except:
            pass
    return False


def run():
    args = parse_args()
    apply_cli_overrides(args)
    ensure_output_dirs()
    write_diagnostics()
    step_results = []
    downloaded_files = []
    fatal_error = None

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=CONFIG['headless'],
                args=[
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ]
            )
        except Exception as exc:
            raise RuntimeError(
                f"Chromium 启动失败: {exc}。请先运行: python -m playwright install chromium"
            ) from exc

        storage_state = STORAGE_STATE_FILE if (CONFIG["use_storage_state"] and Path(STORAGE_STATE_FILE).exists()) else None
        log("📁 发现保存的登录状态，尝试自动登录..." if storage_state else "📝 未找到登录状态，将进行扫码登录...")

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            accept_downloads=True,
            storage_state=storage_state,
        )

        page = context.new_page()
        page.set_default_timeout(CONFIG['timeout'])

        try:
            # ========== 第一轮 ==========
            log("========== 第一轮 ==========")

            # 1. 打开生意参谋
            log("Step 1: 打开生意参谋...")
            page.goto("https://sycm.taobao.com/mc/ci/shop/overview", timeout=30000)
            human_sleep(2, 3)
            record_step(step_results, 1, "打开生意参谋", True, extra=page_state(page))

            # 等待登录成功标志：左侧菜单出现"自助分析"
            login_success = False
            for attempt in range(3):
                try:
                    page.wait_for_selector('ul li a span:has-text("自助分析")', timeout=5000)
                    log("  ✅ 已登录")
                    login_success = True
                    break
                except:
                    pass
                # 检查是否跳转到淘宝登录页
                if "login" in page.url.lower() or page.url == "https://sycm.taobao.com/":
                    log(f"  ⚠️ 检测到未登录（尝试 {attempt+1}/3）...")
                    if attempt < 2:
                        log("  请在浏览器中扫码登录...")
                        human_sleep(5, 8)
            
            if not login_success:
                log("  ❌ 登录失败，请确认已成功扫码登录后重试")
                record_step(step_results, 1, "登录检测", False, "登录失败", page_state(page))
                browser.close()
                return
            record_step(step_results, 1, "登录检测", True, "已登录", page_state(page))
            
            # 保存登录状态
            context.storage_state(path=STORAGE_STATE_FILE)
            log("  💾 登录状态已保存")

            # 2. 自助分析
            log("Step 2: 点击自助分析...")
            ok = retry_click(lambda: human_click(page, 'ul li a span:has-text("自助分析")', offset_range=5), "点击自助分析")
            ensure_step(ok, "点击自助分析")
            log("  ✅")
            human_sleep(0.8, 1.8)
            record_step(step_results, 2, "点击自助分析", True)

            # 3. 取数报表
            log("Step 3: 点击取数报表...")
            ok = retry_click(lambda: human_click(page, 'ul li ul li div:has-text("取数报表")', offset_range=5), "点击取数报表")
            ensure_step(ok, "点击取数报表")
            log("  ✅")
            human_sleep(1.5, 3)
            record_step(step_results, 3, "点击取数报表", True)

            # 4. 进入 iframe
            log("Step 4: 进入 iframe...")
            frame = page.frame_locator('#jycm-insert-iframe')
            log("  ✅")
            record_step(step_results, 4, "进入iframe", True)

            # 5. 自动更新
            log("Step 5: 选择自动更新...")
            if not click_radio(frame, "自动更新"):
                log("  ⚠️ 自动更新选择失败")
                record_step(step_results, 5, "选择自动更新", False)
                ensure_step(False, "选择自动更新")
            else:
                log("  ✅")
                record_step(step_results, 5, "选择自动更新", True)
            human_sleep(0.5, 1)

            # 6. 最近30天
            log("Step 6: 选择最近30天...")
            # 直接用 id 精确定位
            for xp in [
                './/div[@id="autoUpdateCycle"]//span[@class="dt-oui-radio"]/input[@type="radio"]',
                './/div[@id="autoUpdateCycle"]//input[@type="radio"]',
            ]:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=3)
                    log("  ✅ 最近30天")
                    record_step(step_results, 6, "选择最近30天", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 6, "选择最近30天", False)
                ensure_step(False, "选择最近30天")
            human_sleep(0.5, 1)

            # 7. 报表名称
            log("Step 7: 填写报表名称...")
            for sel in ['input#reportName', 'input[type="text"]#reportName', '//input[@id="reportName"]']:
                try:
                    frame.locator(sel).fill(CONFIG['report_name'], timeout=5000)
                    log(f"  ✅ {CONFIG['report_name']}")
                    record_step(step_results, 7, "填写报表名称", True, CONFIG['report_name'])
                    break
                except:
                    pass
            else:
                record_step(step_results, 7, "填写报表名称", False)
                ensure_step(False, "填写报表名称")
            human_sleep(0.5, 1)

            # 8. 生成报表
            log("Step 8: 点击生成报表...")
            for xp in ['.//form//button[normalize-space(.)="生成报表"]', './/button[normalize-space(.)="生成报表"]']:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=5)
                    log("  ✅")
                    record_step(step_results, 8, "点击生成报表", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 8, "点击生成报表", False)
                ensure_step(False, "点击生成报表")
            human_sleep(6, 10)

            # 9. 下载报表（Playwright 下载事件）
            log("Step 9: 点击下载报表...")
            download_ok = False
            for xp in ['.//button/span[normalize-space(.)="下载报表"]', './/button[normalize-space(.)="下载报表"]']:
                try:
                    with page.expect_download(timeout=CONFIG["download_timeout_ms"]) as dl_info:
                        human_click(frame, f'xpath={xp}', offset_range=5)
                    download = dl_info.value
                    normalized_name = build_download_filename("shop", download.suggested_filename)
                    save_path = Path(CONFIG["download_dir"]) / normalized_name
                    download.save_as(str(save_path))
                    downloaded_files.append(str(save_path))
                    log(f"  ✅ 下载成功: {save_path}")
                    record_step(step_results, 9, "下载报表(第一轮)", True, str(save_path))
                    download_ok = True
                    break
                except Exception as e:
                    log(f"  ⚠️ 下载尝试失败: {e}")
            if not download_ok:
                record_step(step_results, 9, "下载报表(第一轮)", False)
                ensure_step(False, "下载报表(第一轮)")
            human_sleep(3, 5)

            # 10. 返回
            log("Step 10: 点击返回...")
            # 用 Playwright get_by_text 精确匹配（避免 XPath 的 normalize-space 非断行空格问题）
            returned = False
            # 策略1: get_by_text 精确匹配
            try:
                frame.get_by_text('返回 |', exact=True).click(timeout=5000)
                log("  ✅ 策略1成功: get_by_text exact")
                returned = True
            except:
                pass
            # 策略2: 按 class 找父级 span
            if not returned:
                try:
                    frame.locator('.report-generation-sycm-title-back').click(timeout=5000)
                    log("  ✅ 策略2成功: class")
                    returned = True
                except:
                    pass
            # 策略3: contains 模糊匹配
            if not returned:
                try:
                    frame.get_by_text('返回', exact=False).first.click(timeout=5000)
                    log("  ✅ 策略3成功: contains")
                    returned = True
                except:
                    pass
            if not returned:
                log("  ⚠️ 返回按钮点击失败")
                record_step(step_results, 10, "点击返回", False)
                ensure_step(False, "点击返回")
            else:
                record_step(step_results, 10, "点击返回", True)
            human_sleep(2, 4)

            # ========== 第二轮 ==========
            log("========== 第二轮 ==========")

            # 11. 商品维度
            log("Step 11: 选择商品维度...")
            for xp in [
                './/label[normalize-space(.)="商品"]/span/input[@type="radio"][@value="商品"]',
                './/label[normalize-space(.)="商品"]/span/input[@type="radio"]',
            ]:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=3)
                    log("  ✅")
                    record_step(step_results, 11, "选择商品维度", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 11, "选择商品维度", False)
                ensure_step(False, "选择商品维度")
            human_sleep(1, 2)

            # 12. 自动更新（第二轮）
            log("Step 12: 选择自动更新（第二轮）...")
            if not click_radio(frame, "自动更新"):
                log("  ⚠️ 自动更新选择失败")
                record_step(step_results, 12, "选择自动更新(第二轮)", False)
                ensure_step(False, "选择自动更新(第二轮)")
            else:
                log("  ✅")
                record_step(step_results, 12, "选择自动更新(第二轮)", True)
            human_sleep(0.5, 1)

            # 13. 最近30天（第二轮）
            log("Step 13: 选择最近30天（第二轮）...")
            for xp in [
                './/div[@id="autoUpdateCycle"]//span[@class="dt-oui-radio"]/input[@type="radio"]',
                './/div[@id="autoUpdateCycle"]//input[@type="radio"]',
            ]:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=3)
                    log("  ✅")
                    record_step(step_results, 13, "选择最近30天(第二轮)", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 13, "选择最近30天(第二轮)", False)
                ensure_step(False, "选择最近30天(第二轮)")
            human_sleep(0.5, 1)

            # 14. 搜索商品（留空）
            log("Step 14: 搜索商品（留空=全店）...")
            for sel in [
                './/form//span/input[@type="text"][@placeholder="请输入商品关键字或商品id"]',
                './/input[@placeholder="请输入商品关键字或商品id"]',
            ]:
                try:
                    frame.locator(f'xpath={sel}').click(timeout=5000)
                    log("  ✅")
                    record_step(step_results, 14, "搜索商品(留空)", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 14, "搜索商品(留空)", False)
                ensure_step(False, "搜索商品(留空)")
            human_sleep(0.3, 0.8)

            # 15. 一键全选
            log("Step 15: 一键全选...")
            for xp in ['.//form//ul/li//button[normalize-space(.)="一键全选"]', './/button[normalize-space(.)="一键全选"]']:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=5)
                    log("  ✅")
                    record_step(step_results, 15, "一键全选", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 15, "一键全选", False)
                ensure_step(False, "一键全选")
            human_sleep(1, 2)

            # 16. 报表名称（第二轮）
            log("Step 16: 填写报表名称...")
            for sel in ['input#reportName', 'input[type="text"]#reportName', '//input[@id="reportName"]']:
                try:
                    frame.locator(sel).fill(CONFIG['report_name_goods'], timeout=5000)
                    log(f"  ✅ {CONFIG['report_name_goods']}")
                    record_step(step_results, 16, "填写报表名称(第二轮)", True, CONFIG['report_name_goods'])
                    break
                except:
                    pass
            else:
                record_step(step_results, 16, "填写报表名称(第二轮)", False)
                ensure_step(False, "填写报表名称(第二轮)")
            human_sleep(0.5, 1)

            # 17. 生成报表（第二轮）
            log("Step 17: 点击生成报表...")
            for xp in ['.//form//button[normalize-space(.)="生成报表"]', './/button[normalize-space(.)="生成报表"]']:
                try:
                    human_click(frame, f'xpath={xp}', offset_range=5)
                    log("  ✅")
                    record_step(step_results, 17, "点击生成报表(第二轮)", True)
                    break
                except:
                    pass
            else:
                record_step(step_results, 17, "点击生成报表(第二轮)", False)
                ensure_step(False, "点击生成报表(第二轮)")
            human_sleep(6, 10)

            # 18. 下载报表（第二轮，Playwright 下载事件）
            log("Step 18: 点击下载报表...")
            download_ok = False
            for xp in ['.//button/span[normalize-space(.)="下载报表"]', './/button[normalize-space(.)="下载报表"]']:
                try:
                    with page.expect_download(timeout=CONFIG["download_timeout_ms"]) as dl_info:
                        human_click(frame, f'xpath={xp}', offset_range=5)
                    download = dl_info.value
                    normalized_name = build_download_filename("goods", download.suggested_filename)
                    save_path = Path(CONFIG["download_dir"]) / normalized_name
                    download.save_as(str(save_path))
                    downloaded_files.append(str(save_path))
                    log(f"  ✅ 下载成功: {save_path}")
                    record_step(step_results, 18, "下载报表(第二轮)", True, str(save_path))
                    download_ok = True
                    break
                except Exception as e:
                    log(f"  ⚠️ 下载尝试失败: {e}")
            if not download_ok:
                record_step(step_results, 18, "下载报表(第二轮)", False)
                ensure_step(False, "下载报表(第二轮)")
            human_sleep(3, 5)

            # 19. 下载结果确认（替代 Windows 原生另存为）
            log("Step 19: 校验下载结果...")
            if downloaded_files:
                log(f"  ✅ 已下载文件数: {len(downloaded_files)}")
                for f in downloaded_files:
                    log(f"     - {f}")
                record_step(step_results, 19, "校验下载结果", True, f"count={len(downloaded_files)}")
            else:
                log("  ⚠️ 未检测到任何下载文件")
                record_step(step_results, 19, "校验下载结果", False, "no downloads")

            log("  🎉 全部流程执行完成！")

        except Exception as e:
            log(f"  ❌ 执行异常: {e}")
            save_error_screenshot(page, "fatal_error")
            fatal_error = str(e)
            raise
        finally:
            save_run_summary(step_results, downloaded_files, fatal_error=fatal_error)
            context.close()
            browser.close()


if __name__ == "__main__":
    run()

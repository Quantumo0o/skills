#!/usr/bin/env python3

import os
# 清除代理环境变量，防止 Chromium 走代理导致无法访问番茄
for _var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY", "no_proxy", "NO_PROXY"]:
    os.environ.pop(_var, None)

"""
fanqie-publish.py — 番茄小说自动发布脚本（自动化版）

用法：
  python3 fanqie-publish.py --book "书名" --count 2 [--headless]

参数：
  --book     书名（对应 chapters/{book}/ 目录下的子目录名）
  --count    本次发布的章节数量（默认：全部）
  --headless 是否无头模式运行（默认：True，生产环境用）

依赖：
  pip install playwright
  playwright install chromium
  state.json（首次运行需 python3 login.py 扫码生成）

目录结构：
  chapters/死亡循环/第9章 xxx.txt   ← 待发布
  chapters/死亡循环/第10章 xxx.txt
  state.json                        ← 登录状态（扫码一次后复用）
  uploaded/死亡循环/               ← 已发布章节归档
"""

import os
import sys
import glob
import shutil
import re
import argparse
from playwright.sync_api import sync_playwright

# ====== 配置 ======
STATE_FILE = "state.json"
CHAPTERS_DIR = "chapters"
UPLOADED_DIR = "uploaded"
BOOK_MANAGE_URL = "https://fanqienovel.com/main/writer/book-manage"


def get_chapter_files(book_dir: str, count: int = None):
    """获取指定书名目录下所有 txt 文件，按文件名排序"""
    txt_files = sorted(glob.glob(os.path.join(book_dir, "*.txt")))
    if count:
        txt_files = txt_files[:count]
    return txt_files


def parse_chapter_info(filename: str):
    """从文件名解析章节号和标题"""
    name = os.path.splitext(filename)[0]
    m = re.search(r'第(\d+)章[\s_：:]*(.*)', name)
    chapter_num = m.group(1) if m else ""
    chapter_title = m.group(2).strip() if m and m.group(2) else ""

    file_path = os.path.join(CHAPTERS_DIR, filename) if os.path.exists(os.path.join(CHAPTERS_DIR, filename)) else filename

    if not chapter_title:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                # 支持多种分隔符：竖线、空格+竖线、冒号、破折号、长破折号
                m2 = re.search(r'第(\d+)章[　\s｜|:—–-]*(.*)', lines[0].strip())
                if m2:
                    raw = m2.group(2).strip()
                    # 去掉残留的 | 或 : 符号
                    chapter_title = raw.lstrip('| ：:—–-').strip()
        except:
            pass

    if not chapter_title:
        chapter_title = re.sub(r'^[0-9]+[\s_：:]*', '', name).strip()

    return chapter_num, chapter_title


def clear_popups(page, max_rounds=10):
    """清除番茄后台的弹窗（新手引导、风险提示等）"""
    for _ in range(max_rounds):
        clicked = False
        for target_text in ["下一步", "完成", "我知道了", "跳过", "取消"]:
            try:
                btns = page.get_by_text(target_text, exact=True).element_handles()
                for btn in btns:
                    box = btn.bounding_box()
                    if box and box['y'] > 100:  # 不点顶栏按钮
                        btn.click()
                        page.wait_for_timeout(600)
                        clicked = True
            except Exception:
                pass
        if not clicked:
            break
        page.wait_for_timeout(300)


def publish_chapter(page, chapter_num: str, chapter_title: str, content: str):
    """发布单个章节到番茄后台"""
    # 1. 回到书籍管理列表
    page.goto(BOOK_MANAGE_URL, timeout=60000)
    page.wait_for_timeout(3000)

    # 2. 找到章节管理入口（hover 触发）
    manage_clicked = False
    book_cards = page.locator('div, li, section, article').filter(
        has_text="死亡循环后我绑定了回档系统"
    )
    for i in range(book_cards.count() - 1, -1, -1):
        card = book_cards.nth(i)
        try:
            if not card.is_visible():
                continue
            card.hover(timeout=3000)
            page.wait_for_timeout(1000)
            manage_btn = card.get_by_text("章节管理").first
            if manage_btn.is_visible():
                manage_btn.click()
                manage_clicked = True
                break
        except Exception:
            continue

    if not manage_clicked:
        page.get_by_text("章节管理").first.click()

    page.wait_for_timeout(4000)

    # 切换到新标签页（如果有）
    original_pages = len(page.context.pages)
    if original_pages > 1 and page.context.pages[-1] != page:
        editor_page = page.context.pages[-1]
    else:
        editor_page = page

    # 3. 检查是否已有草稿
    draft_row = editor_page.locator('tr, li, .chapter-item').filter(
        has_text=re.compile(f"第\\s*{chapter_num}\\s*章")
    ).first
    if draft_row.is_visible():
        print(f"  → 发现草稿，进入编辑模式")
        try:
            draft_row.locator('td').last.locator('svg, i, a, span, button, img').first.click(force=True)
        except:
            draft_row.click(force=True)
    else:
        print(f"  → 全新章节，点击【新建章节】")
        new_btn = editor_page.get_by_role("button", name="新建章节").first
        if not new_btn.is_visible():
            new_btn = editor_page.get_by_text("新建章节").first
        new_btn.click(force=True)

    page.wait_for_timeout(4000)

    # 切换到编辑页
    if len(editor_page.context.pages) > original_pages:
        editor_page = editor_page.context.pages[-1]

    # 4. 清除弹窗
    clear_popups(editor_page)

    # 5. 填入章节序号和标题
    num_input = editor_page.locator('input[type="text"]').first
    if num_input.is_visible():
        num_input.fill(chapter_num, force=True)

    title_input = editor_page.get_by_placeholder("请输入标题", exact=False).first
    if not title_input.is_visible():
        title_input = editor_page.get_by_placeholder("请输入章节名", exact=False).first
    if not title_input.is_visible():
        title_input = editor_page.locator('input[type="text"]').last
    if title_input.is_visible():
        title_input.fill(chapter_title, force=True)

    # 6. 填入正文
    editor = editor_page.locator('.ql-editor').first
    if not editor.is_visible():
        editor = editor_page.locator('.ProseMirror').first
    if not editor.is_visible():
        editor = editor_page.locator('[contenteditable="true"]').first

    if editor.is_visible():
        editor.click(force=True)
        editor_page.keyboard.press("Control+A")
        editor_page.keyboard.press("Backspace")
        editor_page.evaluate(
            "([el, text]) => { el.innerText = text; el.dispatchEvent(new Event('input', {bubbles: true})); }",
            [editor.element_handle(), content]
        )
        editor.click()
        editor_page.keyboard.press("End")
        editor_page.keyboard.press("Space")
        page.wait_for_timeout(500)
        editor_page.keyboard.press("Backspace")
    else:
        raise Exception("未找到正文编辑器")

    # 7. 点击【下一步】
    print(f"  → 点击【下一步】")
    next_btn = editor_page.get_by_text("下一步", exact=True).last
    next_btn.click(force=True)
    page.wait_for_timeout(2000)

    # 8. 处理错别字弹窗
    try:
        submit_typo = editor_page.get_by_role("button", name="提交").first
        submit_typo.wait_for(state="visible", timeout=2000)
        submit_typo.click(force=True)
        page.wait_for_timeout(1200)
    except Exception:
        pass

    # 9. 处理风险检测弹窗
    try:
        risk_txt = editor_page.get_by_text("内容风险检测", exact=False).last
        risk_txt.wait_for(state="visible", timeout=2000)
        page.wait_for_timeout(500)
        cancel_risk = editor_page.get_by_role("button", name="取消").last
        cancel_risk.wait_for(state="visible", timeout=2000)
        cancel_risk.click(force=True)
        page.wait_for_timeout(1000)
    except Exception:
        pass

    # 10. 最终发布
    try:
        publish_btn = editor_page.get_by_role("button", name="确认发布").first
        publish_btn.wait_for(state="visible", timeout=6000)

        # 勾选"是否使用AI：否"
        try:
            ai_no = editor_page.get_by_text("否", exact=True).first
            ai_no.wait_for(state="visible", timeout=2000)
            ai_no.click(force=True)
            page.wait_for_timeout(500)
        except Exception:
            pass

        publish_btn.click(force=True)
        print(f"  ✅ 第{chapter_num}章「{chapter_title}」发布成功")
        return True
    except Exception as e:
        print(f"  ⚠️ 未找到确认发布按钮，尝试保存草稿: {e}")
        try:
            save_btn = editor_page.get_by_text("存草稿", exact=False).first
            save_btn.click()
            print(f"  ✅ 第{chapter_num}章「{chapter_title}」已存草稿")
            return True
        except:
            return False

    return False


def main():
    parser = argparse.ArgumentParser(description="番茄小说自动发布脚本")
    parser.add_argument("--book", required=True, help="书名（对应 chapters/{book}/ 目录）")
    parser.add_argument("--count", type=int, default=None, help="本次发布章节数量（默认全部）")
    parser.add_argument("--headless", action="store_true", default=True, help="无头模式")
    parser.add_argument("--wait", type=int, default=0, help="发布完成后等待秒数（默认0）")
    args = parser.parse_args()

    book_dir = os.path.join(CHAPTERS_DIR, args.book)
    if not os.path.isdir(book_dir):
        print(f"❌ 找不到目录: {book_dir}")
        print(f"请确认 chapters/ 下有「{args.book}」子目录")
        sys.exit(1)

    if not os.path.exists(STATE_FILE):
        print(f"❌ 找不到登录状态文件: {STATE_FILE}")
        print(f"请先运行: python3 login.py（需在有浏览器的环境执行一次扫码登录）")
        sys.exit(1)

    txt_files = get_chapter_files(book_dir, args.count)
    if not txt_files:
        print(f"❌ {book_dir} 下没有找到待发章节（.txt 文件）")
        sys.exit(1)

    print(f"\n📖 番茄小说自动发布")
    print(f"  书名: {args.book}")
    print(f"  待发: {len(txt_files)} 章")
    print(f"  模式: {'无头' if args.headless else '可视化'}\n")

    os.makedirs(os.path.join(UPLOADED_DIR, args.book), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()

        success = 0
        for txt_file in txt_files:
            filename = os.path.basename(txt_file)
            chapter_num, chapter_title = parse_chapter_info(filename)

            print(f"\n[{success+1}/{len(txt_files)}] 第{chapter_num}章 「{chapter_title}」")

            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # 跳过文件内顶部的章节标题（防双标题）
                if lines and re.search(r'第.*?章', lines[0].strip()):
                    lines = lines[1:]
                while lines and not lines[0].strip():
                    lines = lines[1:]

                content = "".join(lines)

                ok = publish_chapter(page, chapter_num, chapter_title, content)
                if ok:
                    success += 1
                    # 归档到 uploaded/
                    dest = os.path.join(UPLOADED_DIR, args.book, filename)
                    shutil.move(txt_file, dest)
                    print(f"  → 已归档: uploaded/{args.book}/{filename}")

                page.wait_for_timeout(3000)

            except Exception as e:
                print(f"  ❌ 发布失败: {e}")

        browser.close()

    print(f"\n{'='*40}")
    print(f"✅ 发布完成：{success}/{len(txt_files)} 章成功")
    print(f"{'='*40}\n")

    if args.wait > 0:
        import time
        time.sleep(args.wait)


if __name__ == "__main__":
    main()

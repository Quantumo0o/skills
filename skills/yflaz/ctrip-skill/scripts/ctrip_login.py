#!/usr/bin/env python3
"""
携程登录工具 - 二维码扫码登录

Usage:
    python ctrip_login.py

流程:
1. 打开携程登录页
2. 显示二维码
3. 用户用携程 APP 扫码
4. 获取 session cookies
5. 保存到 cookies.json

注意：登录一次后，cookies 可重复使用（有效期约 7 天）
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def login(cookies_file="cookies.json"):
    """
    执行登录流程
    
    Args:
        cookies_file: cookies 保存路径
    
    Returns:
        bool: 登录是否成功
    """
    print("="*60)
    print("携程登录工具")
    print("="*60)
    print("\n请在打开的浏览器中使用携程 APP 扫码登录\n")
    
    with sync_playwright() as p:
        # 启动可见浏览器
        browser = p.chromium.launch(
            headless=False,  # 可见浏览器，方便扫码
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        try:
            # 打开携程首页
            print("正在打开携程首页...")
            page.goto("https://www.ctrip.com", timeout=30000)
            page.wait_for_timeout(3000)
            
            # 尝试点击登录按钮
            print("正在打开登录页面...")
            
            # 查找登录按钮（多种选择器）
            login_selectors = [
                ".login-btn",
                "[class*='login']",
                "a[href*='login']",
                ".user-center",
                "text=登录"
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        element.click()
                        login_clicked = True
                        print(f"✓ 点击登录按钮：{selector}")
                        break
                except:
                    pass
            
            if not login_clicked:
                # 如果没找到登录按钮，直接跳转到登录页
                print("⚠ 未找到登录按钮，尝试直接访问登录页...")
                page.goto("https://accounts.ctrip.com/login", timeout=30000)
            
            # 等待登录页面加载
            page.wait_for_timeout(5000)
            
            # 等待二维码出现
            print("\n等待二维码出现...")
            try:
                page.wait_for_selector(".qrcode, [class*='qrcode'], img[src*='qrcode']", timeout=30000)
                print("✓ 二维码已显示")
            except:
                print("⚠ 未检测到二维码元素，但可能已显示")
            
            print("\n" + "="*60)
            print("请打开携程 APP 扫码登录")
            print("="*60)
            print("\n提示：扫码后等待页面自动跳转...")
            
            # 等待登录成功（检测用户头像或用户名）
            print("\n等待登录成功...")
            try:
                # 多种登录成功标识
                success_selectors = [
                    ".user-avatar",
                    ".user-name",
                    "[class*='user-info']",
                    "text=我的携程"
                ]
                
                for selector in success_selectors:
                    try:
                        page.wait_for_selector(selector, timeout=60000)
                        print(f"✓ 登录成功！检测到：{selector}")
                        break
                    except:
                        continue
                else:
                    # 如果都没检测到，尝试检测 URL 变化
                    print("⚠ 未检测到登录标识，请确认是否登录成功")
                    
            except Exception as e:
                print(f"⚠ 等待超时：{e}")
                print("请手动确认是否登录成功")
            
            # 保存 cookies
            print("\n正在保存登录状态...")
            cookies = context.cookies()
            
            cookies_path = Path(cookies_file)
            with open(cookies_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Cookies 已保存至：{cookies_path.absolute()}")
            print(f"  共保存 {len(cookies)} 个 cookies")
            print("\n登录状态有效期约 7 天，过期后需重新登录")
            
            return True
            
        except Exception as e:
            print(f"\n✗ 登录过程出错：{e}")
            return False
        
        finally:
            # 5 秒后关闭浏览器
            print("\n5 秒后关闭浏览器...")
            page.wait_for_timeout(5000)
            browser.close()
            print("✓ 浏览器已关闭")


def check_login_status(cookies_file="cookies.json"):
    """
    检查登录状态
    
    Args:
        cookies_file: cookies 文件路径
    
    Returns:
        bool: 是否已登录
    """
    cookies_path = Path(cookies_file)
    
    if not cookies_path.exists():
        print("✗ 未找到 cookies 文件，请先登录")
        return False
    
    try:
        with open(cookies_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        
        if not cookies:
            print("✗ cookies 文件为空，请重新登录")
            return False
        
        print(f"✓ 找到 {len(cookies)} 个 cookies")
        
        # 检查关键 cookies
        key_cookies = ['_ctk', 'ctk', 'ASP.NET_SessionId']
        found = [c for c in key_cookies if any(c in cookie.get('name', '') for cookie in cookies)]
        
        if found:
            print(f"✓ 关键 cookies 存在：{', '.join(found)}")
            print("✓ 登录状态有效")
            return True
        else:
            print("⚠ 未找到关键 cookies，可能已过期")
            return False
            
    except Exception as e:
        print(f"✗ 读取 cookies 失败：{e}")
        return False


def main():
    """命令行入口"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            # 检查登录状态
            cookies_file = sys.argv[2] if len(sys.argv) > 2 else "cookies.json"
            status = check_login_status(cookies_file)
            sys.exit(0 if status else 1)
        else:
            print(f"未知命令：{command}")
            print(__doc__)
            sys.exit(1)
    else:
        # 执行登录
        success = login()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

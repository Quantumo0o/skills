#!/usr/bin/env python3
"""
浏览器自动化工具箱 - 统一入口
整合：浏览器控制、数据采集、账号管理、自动化运营、验证码识别
使用 argparse 统一 CLI
"""

import sys
import os
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from browser_config import get_config


def cmd_browser(args):
    """浏览器控制命令"""
    from browser import Browser
    browser = Browser(headless=args.headless)
    
    try:
        if args.action == 'navigate':
            url = args.selector or 'https://www.baidu.com'
            browser.navigate(url)
        
        elif args.action == 'click':
            if not args.selector:
                print("错误: 需要指定选择器")
                return 1
            browser.click(args.selector, args.by)
        
        elif args.action == 'input':
            if not args.selector or not args.text:
                print("错误: 需要指定选择器和文本")
                return 1
            browser.input(args.selector, args.text, args.by)
        
        elif args.action == 'screenshot':
            path = browser.screenshot(args.name or 'screenshot.png')
            if path:
                print(f"截图: {path}")
        
        elif args.action == 'wait':
            browser.wait_seconds(args.seconds or 1)
        
        elif args.action == 'html':
            print(browser.get_html())
    finally:
        browser.close()
    
    return 0


def cmd_captcha(args):
    """验证码识别命令"""
    from captcha import CaptchaSolver
    
    solver = CaptchaSolver()
    
    try:
        if args.action == 'recognize':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_simple(args.image_path)
            print(f"识别结果: {result}")
        
        elif args.action == 'number':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_number(args.image_path)
            print(f"识别结果: {result}")
        
        elif args.action == 'chinese':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_chinese(args.image_path)
            print(f"识别结果: {result}")
        
        elif args.action == 'test':
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (150, 50), 'white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "ABC123", fill='black')
            
            test_path = os.path.join(solver.config.screenshot_dir, "test_captcha.png")
            img.save(test_path)
            
            result = solver.recognize_simple(test_path)
            print(f"测试识别: {result}")
    finally:
        solver.close()
    
    return 0


def cmd_collector(args):
    """数据采集命令"""
    from collector import DataCollector
    
    collector = DataCollector()
    
    if not collector.init_browser(headless=args.headless):
        print("错误: 浏览器初始化失败")
        return 1
    
    try:
        if args.action == 'taobao':
            keyword = args.keyword or "白酒"
            path = collector.collect_taobao_products(keyword, args.pages or 3)
            print(f"已保存: {path}")
        
        elif args.action == 'jd':
            keyword = args.keyword or "白酒"
            path = collector.collect_jd_products(keyword, args.pages or 3)
            print(f"已保存: {path}")
        
        elif args.action == 'douyin':
            keyword = args.keyword or "白酒"
            path = collector.collect_douyin_products(keyword)
            print(f"已保存: {path}")
        
        elif args.action == 'monitor':
            if not args.url:
                print("错误: 需要指定 --url")
                return 1
            import json
            result = collector.monitor_price(args.url, args.selector or '.price')
            print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        collector.close()
    
    return 0


def cmd_account(args):
    """账号管理命令"""
    from account import AccountManager
    import json
    
    mgr = AccountManager()
    
    try:
        if args.action == 'add':
            if len(args.args) < 4:
                print("错误: add 需要 <名称> <平台> <用户名> <密码>")
                return 1
            name, platform, username, password = args.args[:4]
            path = mgr.add_account(name, platform, username, password)
            print(f"账号已添加（密码已加密）: {path}")
        
        elif args.action == 'list':
            platform = args.args[0] if args.args else None
            accounts = mgr.list_accounts(platform)
            for a in accounts:
                print(f"- {a['name']} ({a['platform']}): {a['username']} [{a.get('password', 'N/A')}]")
        
        elif args.action == 'get':
            if not args.args:
                print("错误: get 需要 <名称>")
                return 1
            account = mgr.get_account(args.args[0], should_decrypt=True)
            if account:
                print(json.dumps(account, ensure_ascii=False, indent=2))
            else:
                print("账号不存在")
                return 1
        
        elif args.action == 'delete':
            if not args.args:
                print("错误: delete 需要 <名称>")
                return 1
            mgr.delete_account(args.args[0])
            print("账号已删除")
        
        elif args.action == 'login':
            if len(args.args) < 4:
                print("错误: login 需要 <名称> <URL> <用户选择器> <密码选择器>")
                return 1
            name, url, user_sel, pass_sel = args.args[:4]
            
            account = mgr.get_account(name, should_decrypt=True)
            if not account:
                print("账号不存在")
                return 1
            
            if not mgr.init_browser():
                print("浏览器初始化失败")
                return 1
            
            mgr.login(url, user_sel, pass_sel, account['username'], account['password'])
            mgr.save_cookies(name)
            mgr.update_last_used(name)
            print("登录成功并保存Cookies")
            mgr.close()
        
        elif args.action == 'save_cookies':
            if not args.args:
                print("错误: save_cookies 需要 <名称>")
                return 1
            
            if not mgr.init_browser():
                print("浏览器初始化失败")
                return 1
            
            path = mgr.save_cookies(args.args[0])
            print(f"Cookies已保存: {path}")
            mgr.close()
        
        elif args.action == 'load_cookies':
            if not args.args:
                print("错误: load_cookies 需要 <名称>")
                return 1
            
            if not mgr.init_browser():
                print("浏览器初始化失败")
                return 1
            
            result = mgr.load_cookies(args.args[0], verify_domain=args.verify_domain)
            print("Cookies加载成功" if result else "加载失败")
            mgr.close()
        
        elif args.action == 'export_cookies':
            if not args.args:
                print("错误: export_cookies 需要 <名称>")
                return 1
            path = mgr.export_cookies(args.args[0])
            print(f"Cookies已导出: {path}" if path else "导出失败")
        
        elif args.action == 'import_cookies':
            if len(args.args) < 2:
                print("错误: import_cookies 需要 <名称> <文件>")
                return 1
            result = mgr.import_cookies(args.args[0], args.args[1])
            print("导入成功" if result else "导入失败")
        
        elif args.action == 'migrate':
            for f in mgr.accounts_dir.iterdir():
                if f.suffix == '.json' and not f.stem.endswith('_cookies') and not f.stem.endswith('_export'):
                    try:
                        with open(f, 'r', encoding='utf-8') as fp:
                            account = json.load(fp)
                        
                        if account.get('password_encrypted'):
                            continue
                        
                        old_password = account.get('password', '')
                        if old_password:
                            from security import encrypt_password
                            encrypted = encrypt_password(old_password)
                            account['password'] = encrypted
                            account['password_encrypted'] = True
                            
                            with open(f, 'w', encoding='utf-8') as fp:
                                json.dump(account, fp, ensure_ascii=False, indent=2)
                            
                            print(f"已迁移: {f.stem}")
                    except Exception as e:
                        print(f"迁移失败 {f.stem}: {e}")
            
            print("迁移完成")
    finally:
        if mgr.driver:
            mgr.close()
    
    return 0


def cmd_poster(args):
    """自动化运营命令"""
    from poster import AutoPoster
    
    poster = AutoPoster()
    
    try:
        if args.action == 'douyin':
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_douyin(content, args.cookie)
        
        elif args.action == 'xiaohongshu':
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_xiaohongshu(content, args.images)
        
        elif args.action == 'weibo':
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_weibo(content, args.cookie)
        
        elif args.action == 'reply':
            if len(args.args) < 2:
                print("错误: reply 需要 <关键词> <回复内容>")
                return 1
            poster.auto_reply_douyin(args.args[0], args.args[1])
        
        elif args.action == 'follow':
            poster.batch_follow(args.args if args.args else [])
        
        elif args.action == 'like':
            poster.batch_like(args.args if args.args else [])
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


def create_parser():
    """创建主命令行解析器"""
    parser = argparse.ArgumentParser(
        description='🤖 浏览器自动化工具箱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python tool.py browser navigate https://www.baidu.com
  python tool.py captcha recognize captcha.png
  python tool.py collector taobao 白酒 3
  python tool.py account list
  python tool.py poster douyin "测试发布"

详细信息请使用: python tool.py <模块> --help
        """
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    
    subparsers = parser.add_subparsers(dest='module', help='模块命令')
    
    # browser 子命令
    parser_browser = subparsers.add_parser('browser', help='浏览器控制')
    parser_browser.add_argument('action', nargs='?', default='help',
                                 choices=['navigate', 'click', 'input', 'screenshot', 'wait', 'html', 'help'])
    parser_browser.add_argument('selector', nargs='?', help='选择器或URL')
    parser_browser.add_argument('text', nargs='?', help='输入文本')
    parser_browser.add_argument('--by', '-b', default='css', choices=['css', 'xpath', 'id', 'name'])
    parser_browser.add_argument('--name', '-n', default='screenshot.png', help='截图文件名')
    parser_browser.add_argument('--seconds', '-s', type=float, help='等待秒数')
    parser_browser.add_argument('--headless', action='store_true', default=None, help='无头模式')
    parser_browser.add_argument('--no-headless', dest='headless', action='store_false', help='非无头模式')
    parser_browser.set_defaults(func=cmd_browser)
    
    # captcha 子命令
    parser_captcha = subparsers.add_parser('captcha', help='验证码识别')
    parser_captcha.add_argument('action', nargs='?', default='help',
                                 choices=['recognize', 'number', 'chinese', 'test', 'help'])
    parser_captcha.add_argument('image_path', nargs='?', help='图片路径')
    parser_captcha.set_defaults(func=cmd_captcha)
    
    # collector 子命令
    parser_collector = subparsers.add_parser('collector', help='数据采集')
    parser_collector.add_argument('action', nargs='?', default='help',
                                   choices=['taobao', 'jd', 'douyin', 'monitor', 'help'])
    parser_collector.add_argument('keyword', nargs='?', help='搜索关键词')
    parser_collector.add_argument('pages', nargs='?', type=int, default=3, help='页数')
    parser_collector.add_argument('--url', help='监控URL')
    parser_collector.add_argument('--selector', default='.price', help='选择器')
    parser_collector.add_argument('--headless', action='store_true', default=True)
    parser_collector.set_defaults(func=cmd_collector)
    
    # account 子命令
    parser_account = subparsers.add_parser('account', help='账号管理')
    parser_account.add_argument('action', nargs='?', default='help',
                                 choices=['add', 'list', 'get', 'delete', 'login', 'save_cookies', 
                                          'load_cookies', 'export_cookies', 'import_cookies', 'migrate', 'help'])
    parser_account.add_argument('args', nargs='*', help='命令参数')
    parser_account.add_argument('--verify-domain', dest='verify_domain', action='store_true', default=True)
    parser_account.add_argument('--no-verify', dest='verify_domain', action='store_false')
    parser_account.set_defaults(func=cmd_account)
    
    # poster 子命令
    parser_poster = subparsers.add_parser('poster', help='自动化运营')
    parser_poster.add_argument('action', nargs='?', default='help',
                                choices=['douyin', 'xiaohongshu', 'weibo', 'reply', 'follow', 'like', 'help'])
    parser_poster.add_argument('args', nargs='*', help='命令参数')
    parser_poster.add_argument('--cookie', help='Cookie文件路径')
    parser_poster.add_argument('--images', nargs='*', help='图片路径')
    parser_poster.set_defaults(func=cmd_poster)
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # 获取配置
    config = get_config()
    
    if not args.module:
        # 无子命令时显示帮助
        parser.print_help()
        print("""
        
=== 基础功能 ===
browser.py navigate <URL>     打开网页
browser.py click <选择器>      点击元素
browser.py input <选择器> <内容>  输入文本
browser.py screenshot [名称]   截图

=== 验证码识别 ===
captcha.py recognize <图片>   识别数字字母
captcha.py number <图片>      识别纯数字
captcha.py chinese <图片>     识别中文

=== 数据采集 ===
collector.py taobao <关键词> [页数]  采集淘宝
collector.py jd <关键词> [页数]      采集京东
collector.py douyin <关键词>        采集抖音

=== 账号管理 ===
account.py add <名称> <平台> <用户名> <密码>
account.py list [平台]
account.py login <名称> <URL> <选择器>

=== 自动化运营 ===
poster.py douyin <内容>         发抖音
poster.py xiaohongshu <内容>    发小红书
poster.py weibo <内容>          发微博

=== 快速开始 ===
python tool.py browser navigate https://www.baidu.com
python tool.py captcha test
python tool.py collector taobao 白酒 3
        """)
        return 0
    
    # 执行对应模块的命令
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())

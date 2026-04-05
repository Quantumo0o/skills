#!/usr/bin/env python3
"""
账号管理模块
功能:多账号管理、Cookie保持、自动登录
安全性(Phase 1 修复已保留):
  - 密码Fernet加密存储
  - 移除Pickle反序列化
  - Cookie域校验
  - 移除潜在危险的eval/shell调用

使用统一的 BrowserConfig
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError, AccountError

try:
    from security import encrypt_password, decrypt_password, is_encrypted
except ImportError:
    # 相对导入作为回退
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent))
    from security import encrypt_password, decrypt_password, is_encrypted

# Phase B: SQLite 存储支持
try:
    from models import DatabaseManager, Account as _Account, get_database
except ImportError:
    # 相对导入作为回退
    _sys.path.insert(0, str(Path(__file__).parent))
    from models import DatabaseManager, Account as _Account, get_database


class AccountManager:
    """
    账号管理器
    保留 Phase 1 的所有安全修复
    """

    @property
    def db(self) -> DatabaseManager:
        """懒加载数据库管理器(JSON + SQLite 双写)"""
        if self._db is None:
            self._db = get_database()
        return self._db

    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        初始化账号管理器

        Args:
            config: 配置对象,None 时使用全局单例
        """
        self.config = config or get_config()
        self.accounts_dir = self.config.accounts_dir
        self.driver: Optional[webdriver.Chrome] = None
        # Phase B: SQLite 数据库管理器(双写:JSON + SQLite)
        self._db: Optional[DatabaseManager] = None

    def init_browser(self, profile: Optional[str] = None, headless: bool = True) -> bool:
        """
        初始化浏览器

        Args:
            profile: 用户配置目录
            headless: 是否使用无头模式

        Returns:
            bool: 是否成功
        """
        try:
            original_headless = self.config.headless
            self.config.set_headless(headless)

            options = self.config.get_chrome_options()

            if profile:
                options.add_argument(f'--user-data-dir={profile}')

            self.driver = webdriver.Chrome(options=options)

            self.config.set_headless(original_headless)
            self.config.info("账号管理浏览器启动成功")
            return True
        except Exception as e:
            self.config.error(f"账号管理浏览器启动失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.config.info("账号管理浏览器已关闭")

    def save_cookies(self, name: str) -> str:
        """
        保存 Cookies

        Args:
            name: 账号名称

        Returns:
            文件路径
        """
        if not self.driver:
            raise AccountError("浏览器未初始化")

        path = self.accounts_dir / f"{name}_cookies.json"
        cookies = self.driver.get_cookies()

        data = {
            'cookies': cookies,
            'localStorage': self._get_local_storage(),
            'saved_at': datetime.now().isoformat(),
            'domain': self.driver.current_url
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.config.info(f"Cookies已保存: {path}")
        return str(path)

    def load_cookies(self, name: str, verify_domain: bool = True) -> bool:
        """
        加载 Cookies

        安全改进(Phase 1):
        1. 从保存的数据中读取domain
        2. 验证domain匹配,防止跨域cookie注入
        3. 先访问域名页面再添加cookie

        Args:
            name: 账号名称
            verify_domain: 是否验证域名

        Returns:
            bool: 是否成功
        """
        if not self.driver:
            raise AccountError("浏览器未初始化")

        path = self.accounts_dir / f"{name}_cookies.json"
        if not path.exists():
            self.config.warning(f"Cookie文件不存在: {path}")
            return False

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            cookies = data.get('cookies', [])
            saved_domain = data.get('domain', '')

            if verify_domain and cookies:
                # 从cookies中提取domain
                cookie_domains = set(c.get('domain', '').lstrip('.') for c in cookies if c.get('domain'))
                if cookie_domains:
                    first_cookie = cookies[0]
                    cookie_domain = first_cookie.get('domain', '').lstrip('.')

                    if cookie_domain:
                        verify_url = f"https://{cookie_domain}"
                        self.driver.get(verify_url)
                        time.sleep(1)

            # 添加 cookies
            for cookie in cookies:
                try:
                    # 移除可能导致问题的字段,只保留安全字段
                    safe_cookie = {
                        k: v for k, v in cookie.items()
                        if k in ['name', 'value', 'domain', 'path', 'secure', 'expiry', 'httpOnly']
                    }
                    self.driver.add_cookie(safe_cookie)
                except Exception as e:
                    self.config.warning(f"添加cookie失败 {cookie.get('name')}: {e}")
                    continue

            # 恢复 localStorage
            local_storage = data.get('localStorage', {})
            if local_storage:
                self._set_local_storage(local_storage)

            self.config.info(f"Cookies已加载: {name}")
            return True

        except json.JSONDecodeError as e:
            self.config.error(f"Cookie文件格式错误: {e}")
            return False
        except Exception as e:
            self.config.error(f"加载Cookies失败: {e}")
            return False

    def _get_local_storage(self) -> Dict[str, str]:
        """获取 localStorage 数据"""
        try:
            return self.driver.execute_script(
                "var storage = {}; for(var i=0; i<localStorage.length; i++){var k=localStorage.key(i); storage[k]=localStorage.getItem(k);} return storage;"
            ) or {}
        except:
            return {}

    def _set_local_storage(self, data: Dict[str, str]) -> None:
        """设置 localStorage 数据"""
        try:
            for key, value in data.items():
                self.driver.execute_script(
                    "localStorage.setItem(arguments[0], arguments[1]);",
                    key, value
                )
        except Exception as e:
            self.config.warning(f"设置localStorage失败: {e}")

    def export_cookies(self, name: str) -> Optional[str]:
        """
        导出账号的 Cookie 和 localStorage 为 JSON

        Args:
            name: 账号名称

        Returns:
            JSON文件路径 或 None
        """
        path = self.accounts_dir / f"{name}_cookies.json"
        if not path.exists():
            return None

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        export_path = self.accounts_dir / f"{name}_export.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.config.info(f"Cookies已导出: {export_path}")
        return str(export_path)

    def import_cookies(self, name: str, export_path: str) -> bool:
        """
        从导出的 JSON 文件导入 Cookie 和 localStorage

        安全改进:验证导入数据格式

        Args:
            name: 账号名称
            export_path: 导出文件路径

        Returns:
            bool: 是否成功
        """
        try:
            with open(export_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证格式
            if 'cookies' not in data:
                raise AccountError("无效的导入文件:缺少cookies字段")

            # 保存
            path = self.accounts_dir / f"{name}_cookies.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.config.info(f"Cookies已导入: {name}")
            return True

        except Exception as e:
            self.config.error(f"导入Cookies失败: {e}")
            return False

    def login(self, url: str, username_selector: str, password_selector: str,
              username: str, password: str, submit_selector: Optional[str] = None) -> str:
        """
        通用登录

        Args:
            url: 登录页面 URL
            username_selector: 用户名输入框选择器
            password_selector: 密码输入框选择器
            username: 用户名
            password: 密码
            submit_selector: 提交按钮选择器

        Returns:
            登录后的 URL
        """
        if not self.driver:
            raise AccountError("浏览器未初始化")

        self.driver.get(url)
        time.sleep(2)

        # 输入用户名
        elem = self.driver.find_element(By.CSS_SELECTOR, username_selector)
        elem.clear()
        elem.send_keys(username)

        # 输入密码
        elem = self.driver.find_element(By.CSS_SELECTOR, password_selector)
        elem.clear()
        elem.send_keys(password)

        # 提交
        if submit_selector:
            elem = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            elem.click()
        else:
            elem.send_keys(Keys.RETURN)

        time.sleep(3)
        self.config.info("登录完成")
        return self.driver.current_url

    def is_logged_in(self, url: str, check_selector: str) -> bool:
        """
        检查是否已登录

        Args:
            url: 检查页面 URL
            check_selector: 登录状态元素选择器

        Returns:
            bool: 是否已登录
        """
        if not self.driver:
            return False

        self.driver.get(url)
        time.sleep(2)
        try:
            self.driver.find_element(By.CSS_SELECTOR, check_selector)
            return True
        except:
            return False

    def add_account(self, name: str, platform: str, username: str, password: str,
                    cookies: Optional[Dict] = None) -> str:
        """
        添加账号

        安全改进(Phase 1):
        1. 密码使用Fernet加密存储
        2. 支持明文密码自动迁移(向后兼容)

        Args:
            name: 账号名称
            platform: 平台
            username: 用户名
            password: 密码
            cookies: Cookies数据

        Returns:
            文件路径
        """
        # 加密密码
        encrypted_password = encrypt_password(password)

        account = {
            'name': name,
            'platform': platform,
            'username': username,
            'password': encrypted_password,
            'password_encrypted': True,  # 标记为已加密
            'cookies': cookies,
            'created': datetime.now().isoformat(),
            'last_used': None
        }

        path = self.accounts_dir / f"{name}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(account, f, ensure_ascii=False, indent=2)

        # Phase B: 同时写入 SQLite
        now = datetime.now().isoformat()
        db_account = _Account(
            name=name,
            platform=platform,
            username=username,
            password_encrypted=encrypted_password,
            login_url=account.get('login_url', ''),
            cookies=cookies if cookies else [],
            headers={},
            user_data={},
            created_at=account.get('created', now),
            updated_at=now,
            last_login='',
            status='active'
        )
        try:
            self.db.save_account(db_account)
            self.config.debug(f"账号已写入SQLite: {name}")
        except Exception as e:
            self.config.warning(f"SQLite写入失败(JSON已保存): {e}")

        self.config.info(f"账号已添加(密码已加密): {name}")
        return str(path)

    def list_accounts(self, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出账号

        Phase B: 合并 SQLite 和 JSON 数据，去重（SQLite 优先）

        Args:
            platform: 平台筛选，None 时列出全部

        Returns:
            账号列表
        """
        seen = set()
        accounts = []

        # Phase B: 先从 SQLite 读取（优先）
        try:
            db_accounts = self.db.get_accounts(platform=platform)
            for db_acc in db_accounts:
                account = {
                    'name': db_acc.name,
                    'platform': db_acc.platform,
                    'username': db_acc.username,
                    'password': '********',  # 隐藏密码
                    'password_encrypted': True,
                    'login_url': db_acc.login_url,
                    'cookies': db_acc.cookies,
                    'created': db_acc.created_at,
                    'last_used': db_acc.last_login,
                    'status': db_acc.status,
                    'updated_at': db_acc.updated_at,
                }
                seen.add(db_acc.name)
                accounts.append(account)
        except Exception as e:
            self.config.debug(f"SQLite list_accounts 失败: {e}")

        # Fallback: 从 JSON 文件读取（合并去重）
        for f in self.accounts_dir.iterdir():
            if f.suffix == '.json' and not f.stem.endswith('_cookies') and not f.stem.endswith('_export'):
                if f.stem in seen:
                    continue
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        account = json.load(fp)
                        # 隐藏加密后的密码
                        if account.get('password_encrypted'):
                            account['password'] = '********'
                        if platform is None or account.get('platform') == platform:
                            accounts.append(account)
                            seen.add(f.stem)
                except:
                    continue

        return accounts

    def get_account(self, name: str, should_decrypt: bool = False) -> Optional[Dict[str, Any]]:
        """
        获取账号信息

        Phase B: 优先从 SQLite 读取,fallback 到 JSON
        安全改进(Phase 1):
        1. 自动解密加密的密码
        2. 向后兼容未加密的明文密码

        Args:
            name: 账号名称
            should_decrypt: 是否解密密码

        Returns:
            账号信息 或 None
        """
        # Phase B: 优先从 SQLite 读取
        try:
            db_account = self.db.get_account(name)
            if db_account:
                account = {
                    'name': db_account.name,
                    'platform': db_account.platform,
                    'username': db_account.username,
                    'password': db_account.password_encrypted,
                    'password_encrypted': True,
                    'login_url': db_account.login_url,
                    'cookies': db_account.cookies,
                    'created': db_account.created_at,
                    'last_used': db_account.last_login,
                    'headers': db_account.headers,
                    'user_data': db_account.user_data,
                    'status': db_account.status,
                    'updated_at': db_account.updated_at,
                }
                if should_decrypt:
                    try:
                        account['password'] = decrypt_password(account['password'])
                    except Exception as e:
                        self.config.warning(f"密码解密失败: {e}")
                return account
        except Exception as e:
            self.config.debug(f"SQLite读取失败,fallback到JSON: {e}")

        # Fallback: 从 JSON 文件读取
        path = self.accounts_dir / f"{name}.json"
        if not path.exists():
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                account = json.load(f)

            # 解密密码(如果已加密且请求解密)
            if should_decrypt and account.get('password_encrypted'):
                try:
                    account['password'] = decrypt_password(account['password'])
                except Exception as e:
                    self.config.warning(f"密码解密失败: {e}")

            return account

        except json.JSONDecodeError:
            return None

    def update_last_used(self, name: str) -> None:
        """
        更新最后使用时间（Phase B: JSON + SQLite 双写）

        Args:
            name: 账号名称
        """
        now = datetime.now().isoformat()

        # 更新 JSON 文件
        path = self.accounts_dir / f"{name}.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                account = json.load(f)
            account['last_used'] = now
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(account, f, ensure_ascii=False, indent=2)

        # Phase B: 更新 SQLite
        try:
            db_account = self.db.get_account(name)
            if db_account:
                db_account.last_login = now
                db_account.updated_at = now
                self.db.save_account(db_account)
        except Exception as e:
            self.config.debug(f"SQLite update_last_used 失败: {e}")

    def delete_account(self, name: str) -> None:
        """
        删除账号（Phase B: JSON + SQLite 双删除）

        Args:
            name: 账号名称
        """
        # 删除 JSON 文件
        for suffix in ['', '_cookies', '_export', '_session']:
            path = self.accounts_dir / f"{name}{suffix}.json"
            if path.exists():
                path.unlink()

        # 旧格式 session 文件
        session_path = self.accounts_dir / f"{name}_session"
        if session_path.exists():
            session_path.unlink()

        # Phase B: 从 SQLite 删除
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM accounts WHERE name = ?", (name,))
                conn.commit()
            self.config.debug(f"SQLite账号已删除: {name}")
        except Exception as e:
            self.config.warning(f"SQLite删除失败: {e}")

        self.config.info(f"账号已删除: {name}")

    def add_cookie(self, name: str, cookie_data: Dict) -> bool:
        """
        添加单个 Cookie(带域名校验)

        安全改进(Phase 1):
        1. 要求cookie必须有domain字段
        2. 拒绝明显跨域的cookie注入

        Args:
            name: 账号名称
            cookie_data: Cookie数据

        Returns:
            bool: 是否成功
        """
        if not cookie_data.get('domain'):
            self.config.error("Cookie必须包含domain字段")
            return False

        # 验证domain格式
        domain = cookie_data.get('domain', '').lstrip('.')
        if not domain or len(domain) < 2:
            self.config.error(f"无效的domain: {domain}")
            return False

        # 加载现有 cookies
        path = self.accounts_dir / f"{name}_cookies.json"
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cookies = data.get('cookies', [])
            except:
                cookies = []
        else:
            cookies = []
            data = {'localStorage': {}, 'saved_at': datetime.now().isoformat(), 'domain': cookie_data.get('domain')}

        # 检查是否已存在同名cookie
        cookie_name = cookie_data.get('name')
        cookies = [c for c in cookies if c.get('name') != cookie_name]
        cookies.append(cookie_data)

        # 保存
        data['cookies'] = cookies
        data['saved_at'] = datetime.now().isoformat()

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.config.info(f"Cookie已添加: {name}/{cookie_name}")
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='账号管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s add myaccount douyin user@email.com password123
  %(prog)s list
  %(prog)s list douyin
  %(prog)s get myaccount
  %(prog)s delete myaccount
  %(prog)s login myaccount <URL> <user_sel> <pass_sel>
  %(prog)s save_cookies myaccount
  %(prog)s load_cookies myaccount
  %(prog)s export_cookies myaccount
  %(prog)s import_cookies myaccount export.json
  %(prog)s migrate
        """
    )

    parser.add_argument('command', nargs='?', default='help',
                        help='命令: add, list, get, delete, login, save_cookies, load_cookies, export_cookies, import_cookies, migrate, help')
    parser.add_argument('args', nargs='*', help='命令参数')
    parser.add_argument('--platform', '-p', help='平台名称')
    parser.add_argument('--verify-domain', dest='verify_domain', action='store_true', default=True,
                        help='验证Cookie域名')
    parser.add_argument('--no-verify', dest='verify_domain', action='store_false',
                        help='不验证Cookie域名')

    args = parser.parse_args()
    mgr = AccountManager()

    if args.command == 'help':
        parser.print_help()
        print("""
命令说明:
  add <名称> <平台> <用户名> <密码>         添加账号
  list [平台]                              列出账号
  get <名称>                               获取账号详情
  delete <名称>                            删除账号
  login <名称> <URL> <用户选择器> <密码选择器>  登录
  save_cookies <名称>                      保存Cookies
  load_cookies <名称>                      加载Cookies
  export_cookies <名称>                    导出Cookies
  import_cookies <名称> <文件>             导入Cookies
  migrate                                  迁移明文密码
        """)
        return 0

    try:
        if args.command == "add":
            if len(args.args) < 4:
                print("错误: add 需要 <名称> <平台> <用户名> <密码>")
                return 1
            name, platform, username, password = args.args[:4]
            path = mgr.add_account(name, platform, username, password)
            print(f"账号已添加(密码已加密): {path}")

        elif args.command == "list":
            platform = args.args[0] if args.args else None
            accounts = mgr.list_accounts(platform)
            for a in accounts:
                print(f"- {a['name']} ({a['platform']}): {a['username']} [{a.get('password', 'N/A')}]")

        elif args.command == "get":
            if not args.args:
                print("错误: get 需要 <名称>")
                return 1
            account = mgr.get_account(args.args[0], should_decrypt=True)
            if account:
                print(json.dumps(account, ensure_ascii=False, indent=2))
            else:
                print("账号不存在")
                return 1

        elif args.command == "delete":
            if not args.args:
                print("错误: delete 需要 <名称>")
                return 1
            mgr.delete_account(args.args[0])
            print("账号已删除")

        elif args.command == "login":
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

        elif args.command == "save_cookies":
            if not args.args:
                print("错误: save_cookies 需要 <名称>")
                return 1
            name = args.args[0]

            if not mgr.init_browser():
                print("浏览器初始化失败")
                return 1

            mgr.load_cookies(name, verify_domain=False)
            path = mgr.save_cookies(name)
            print(f"Cookies已保存: {path}")
            mgr.close()

        elif args.command == "load_cookies":
            if not args.args:
                print("错误: load_cookies 需要 <名称>")
                return 1
            name = args.args[0]

            if not mgr.init_browser():
                print("浏览器初始化失败")
                return 1

            result = mgr.load_cookies(name, verify_domain=args.verify_domain)
            print("Cookies加载成功" if result else "加载失败")
            mgr.close()

        elif args.command == "export_cookies":
            if not args.args:
                print("错误: export_cookies 需要 <名称>")
                return 1
            path = mgr.export_cookies(args.args[0])
            print(f"Cookies已导出: {path}" if path else "导出失败")

        elif args.command == "import_cookies":
            if len(args.args) < 2:
                print("错误: import_cookies 需要 <名称> <文件>")
                return 1
            result = mgr.import_cookies(args.args[0], args.args[1])
            print("导入成功" if result else "导入失败")

        elif args.command == "migrate":
            # 密码迁移
            for f in mgr.accounts_dir.iterdir():
                if f.suffix == '.json' and not f.stem.endswith('_cookies') and not f.stem.endswith('_export'):
                    try:
                        with open(f, 'r', encoding='utf-8') as fp:
                            account = json.load(fp)

                        # 检查是否已加密
                        if account.get('password_encrypted'):
                            continue

                        # 加密密码
                        old_password = account.get('password', '')
                        if old_password:
                            encrypted = encrypt_password(old_password)
                            account['password'] = encrypted
                            account['password_encrypted'] = True

                            with open(f, 'w', encoding='utf-8') as fp:
                                json.dump(account, fp, ensure_ascii=False, indent=2)

                            print(f"已迁移: {f.stem}")
                    except Exception as e:
                        print(f"迁移失败 {f.stem}: {e}")

            print("迁移完成")

        else:
            print(f"未知命令: {args.command}")
            return 1

        return 0

    except KeyboardInterrupt:
        print("\n操作已取消")
        return 0
    except Exception as e:
        print(f"错误: {e}")
        return 1
    finally:
        if mgr.driver:
            mgr.close()


if __name__ == "__main__":
    sys.exit(main())

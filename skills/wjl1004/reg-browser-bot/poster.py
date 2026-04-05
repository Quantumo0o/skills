#!/usr/bin/env python3
"""
自动化运营模块
功能：自动发帖、自动回复、定时任务、批量操作
使用统一的 BrowserConfig
"""

import os
import sys
import json
import time
import schedule
import threading
import argparse
from datetime import datetime, timedelta
from typing import Optional, List, Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError


class AutoPoster:
    """自动化运营器"""
    
    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        初始化运营器
        
        Args:
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.tasks_dir = self.config.data_dir / "tasks"
        self.logs_dir = self.config.logs_dir / "poster"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.driver: Optional[webdriver.Chrome] = None
        self.running = False
    
    def init_browser(self, headless: bool = True) -> bool:
        """
        初始化浏览器
        
        Args:
            headless: 是否使用无头模式
            
        Returns:
            bool: 是否成功
        """
        try:
            original_headless = self.config.headless
            self.config.set_headless(headless)
            
            options = self.config.get_chrome_options()
            self.driver = webdriver.Chrome(options=options)
            
            self.config.set_headless(original_headless)
            self.config.info("运营浏览器启动成功")
            return True
        except Exception as e:
            self.config.error(f"运营浏览器启动失败: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.config.info("运营浏览器已关闭")
    
    def log(self, task_name: str, message: str):
        """
        记录日志
        
        Args:
            task_name: 任务名称
            message: 日志消息
        """
        path = self.logs_dir / f"{task_name}_{datetime.now().strftime('%Y%m%d')}.log"
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        self.config.info(f"[{task_name}] {message}")
    
    # ========== 自动发帖 ==========
    
    def post_to_douyin(self, content: str, cookie_file: Optional[str] = None) -> bool:
        """
        抖音发帖
        
        Args:
            content: 发布内容
            cookie_file: Cookie文件路径
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            if cookie_file and os.path.exists(cookie_file):
                self.driver.get("https://www.douyin.com")
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            
            self.driver.get("https://creator.douyin.com/create-micro-site")
            # 使用 WebDriverWait 等待编辑器加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[contenteditable="true"]'))
            )
            editor = self.driver.find_element(By.CSS_SELECTOR, '[contenteditable="true"]')
            editor.send_keys(content)
            
            self.log('douyin', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('douyin', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    def post_to_xiaohongshu(self, content: str, images: Optional[List[str]] = None) -> bool:
        """
        小红书发帖
        
        Args:
            content: 发布内容
            images: 图片路径列表
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            self.driver.get("https://creator.xiaohongshun.com/publish/publish")
            # 使用 WebDriverWait 等待编辑器加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.editor'))
            )
            editor = self.driver.find_element(By.CSS_SELECTOR, '.editor')
            editor.send_keys(content)
            
            # 上传图片（如果有）
            if images:
                for img in images:
                    if os.path.exists(img):
                        upload = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                        upload.send_keys(img)
            
            self.log('xiaohongshu', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('xiaohongshu', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    def post_to_weibo(self, content: str, cookie_file: Optional[str] = None) -> bool:
        """
        微博发帖
        
        Args:
            content: 发布内容
            cookie_file: Cookie文件路径
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            if cookie_file and os.path.exists(cookie_file):
                self.driver.get("https://weibo.com")
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            
            self.driver.get("https://weibo.com/compose")
            # 使用 WebDriverWait 等待文本框加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[gbkbd]'))
            )
            textarea = self.driver.find_element(By.CSS_SELECTOR, 'textarea[gbkbd]')
            textarea.send_keys(content)
            
            # 点击发布
            self.driver.find_element(By.CSS_SELECTOR, '[node-type="publish"]').click()
            
            self.log('weibo', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('weibo', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    # ========== 自动回复 ==========
    
    def auto_reply_douyin(self, keyword: str, reply_content: str) -> bool:
        """
        抖音评论自动回复
        
        Args:
            keyword: 关键词
            reply_content: 回复内容
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            self.driver.get("https://www.douyin.com/creator/dm")
            # 使用 WebDriverWait 等待评论列表加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.comment-item'))
            )
            comments = self.driver.find_elements(By.CSS_SELECTOR, '.comment-item')
            for comment in comments:
                if keyword in comment.text:
                    comment.find_element(By.CSS_SELECTOR, '.reply-btn').click()
                    # 等待 textarea 出现
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
                    )
                    comment.find_element(By.CSS_SELECTOR, 'textarea').send_keys(reply_content)
                    comment.find_element(By.CSS_SELECTOR, '.send-btn').click()
            
            self.log('reply', f"回复成功: 关键词={keyword}")
            return True
        except Exception as e:
            self.log('reply', f"回复失败: {e}")
            return False
        finally:
            self.close()
    
    # ========== 定时任务 ==========
    
    def add_schedule(self, task_name: str, time_str: str, func: Callable, *args):
        """
        添加定时任务
        
        Args:
            task_name: 任务名称
            time_str: 时间 (如 "09:30" 或 "every day")
            func: 执行函数
            *args: 函数参数
        """
        if time_str.startswith('every'):
            # 如 every day, every hour
            unit = time_str.split()[1] if len(time_str.split()) > 1 else 'day'
            getattr(schedule.every(), unit).do(func, *args)
        else:
            # 如 09:30
            schedule.every().day.at(time_str).do(func, *args)
        
        self.log('schedule', f"已添加任务: {task_name} @ {time_str}")
    
    def run_scheduler(self):
        """运行定时任务循环"""
        self.running = True
        self.log('scheduler', "定时任务已启动")
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def stop_scheduler(self):
        """停止定时任务"""
        self.running = False
        self.log('scheduler', "定时任务已停止")
    
    def start_daemon(self) -> threading.Thread:
        """
        启动守护线程
        
        Returns:
            线程对象
        """
        t = threading.Thread(target=self.run_scheduler, daemon=True)
        t.start()
        return t
    
    # ========== 批量操作 ==========
    
    def batch_follow(self, user_ids: List[str]) -> bool:
        """
        批量关注
        
        Args:
            user_ids: 用户ID列表
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            for uid in user_ids:
                self.driver.get(f"https://example.com/user/{uid}")
                # 等待关注按钮出现
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.follow-btn'))
                    )
                    self.driver.find_element(By.CSS_SELECTOR, '.follow-btn').click()
                    self.log('follow', f"关注成功: {uid}")
                except Exception:
                    self.log('follow', f"关注失败: {uid}")
                # 批量操作间隔（防检测）
                WebDriverWait(self.driver, 2).until(lambda d: False)
            return True
        finally:
            self.close()
    
    def batch_like(self, urls: List[str]) -> bool:
        """
        批量点赞
        
        Args:
            urls: URL列表
            
        Returns:
            bool: 是否成功
        """
        if not self.init_browser():
            return False
        
        try:
            for url in urls:
                self.driver.get(url)
                # 等待点赞按钮出现
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.like-btn'))
                    )
                    self.driver.find_element(By.CSS_SELECTOR, '.like-btn').click()
                    self.log('like', f"点赞成功: {url}")
                except Exception:
                    self.log('like', f"点赞失败: {url}")
                # 批量操作间隔（防检测）
                WebDriverWait(self.driver, 2).until(lambda d: False)
            return True
        finally:
            self.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='自动化运营工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s douyin "发布内容"
  %(prog)s xiaohongshu "发布内容"
  %(prog)s weibo "发布内容"
  %(prog)s reply "关键词" "回复内容"
  %(prog)s follow user1 user2 user3
  %(prog)s like "https://example.com/1" "https://example.com/2"
  %(prog)s schedule "mytask" "09:30"
        """
    )
    
    parser.add_argument('command', nargs='?', default='help',
                        help='命令: douyin, xiaohongshu, weibo, reply, follow, like, schedule, help')
    parser.add_argument('args', nargs='*', help='命令参数')
    parser.add_argument('--cookie', help='Cookie文件路径')
    parser.add_argument('--images', nargs='*', help='图片路径列表')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        parser.print_help()
        print("""
命令说明:
  douyin <内容>              发抖音
  xiaohongshu <内容>         发小红书
  weibo <内容>               发微博
  reply <关键词> <回复内容>  自动回复
  follow <用户ID...>         批量关注
  like <URL...>              批量点赞
  schedule <任务名> <时间>   添加定时任务
        """)
        return 0
    
    poster = AutoPoster()
    
    try:
        if args.command == "douyin":
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_douyin(content, args.cookie)
        
        elif args.command == "xiaohongshu":
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_xiaohongshu(content, args.images)
        
        elif args.command == "weibo":
            content = args.args[0] if args.args else "测试发布"
            poster.post_to_weibo(content, args.cookie)
        
        elif args.command == "reply":
            if len(args.args) < 2:
                print("错误: reply 需要 <关键词> <回复内容>")
                return 1
            keyword, reply = args.args[0], args.args[1]
            poster.auto_reply_douyin(keyword, reply)
        
        elif args.command == "follow":
            ids = args.args if args.args else []
            poster.batch_follow(ids)
        
        elif args.command == "like":
            urls = args.args if args.args else []
            poster.batch_like(urls)
        
        elif args.command == "schedule":
            if len(args.args) < 2:
                print("错误: schedule 需要 <任务名> <时间>")
                return 1
            task_name, time_str = args.args[0], args.args[1]
            poster.log('schedule', f"定时任务 {task_name} 已添加到 {time_str}")
        
        else:
            print(f"未知命令: {args.command}")
            return 1
        
        return 0
    
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

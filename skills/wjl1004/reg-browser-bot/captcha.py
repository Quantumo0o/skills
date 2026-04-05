#!/usr/bin/env python3
"""
验证码识别模块
支持：数字、字母、汉字、滑块、点选
使用统一的 BrowserConfig
"""

import os
import sys
import io
import time
import argparse
from pathlib import Path
from typing import Optional, List, Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# pytesseract as fallback only (system binary may not be installed)
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False

# DdddOcr - pure Python OCR (primary)
try:
    from ddddocr import DdddOcr as _DdddOcr
    DDDDOCR_AVAILABLE = True
except ImportError:
    _DdddOcr = None
    DDDDOCR_AVAILABLE = False

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError
from utils import retry, generate_slider_track, ease_out_quad


class CaptchaSolver:
    """验证码识别器（基于 DdddOcr，纯 Python，无需系统依赖）"""

    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        初始化验证码识别器

        Args:
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None

        # 初始化 DdddOcr（主 OCR 引擎）
        self._ocr = None
        if DDDDOCR_AVAILABLE:
            try:
                self._ocr = _DdddOcr()
                self.config.info("DdddOcr OCR 初始化成功")
            except Exception as e:
                self.config.warning(f"DdddOcr 初始化失败: {e}，将使用 fallback")
                self._ocr = None
        else:
            self.config.warning("DdddOcr 未安装，将使用 pytesseract fallback（可能失败）")

    def _ocr_recognize(self, image_bytes: bytes) -> str:
        """
        使用 DdddOcr 识别图片内容

        Args:
            image_bytes: 图片二进制数据

        Returns:
            str: 识别结果
        """
        if self._ocr is not None:
            try:
                return self._ocr.classification(image_bytes)
            except Exception as e:
                self.config.error(f"DdddOcr 识别失败: {e}")
        return ""

    def init_browser(self, headless: bool = True) -> bool:
        """
        初始化浏览器

        Args:
            headless: 是否使用无头模式

        Returns:
            bool: 是否成功
        """
        try:
            # 保存原设置
            original_headless = self.config.headless
            self.config.set_headless(headless)

            options = self.config.get_chrome_options()
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)

            # 恢复设置
            self.config.set_headless(original_headless)

            self.config.info("验证码浏览器启动成功")
            return True
        except Exception as e:
            self.config.error(f"验证码浏览器启动失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.config.info("验证码浏览器已关闭")

    def wait_element(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """
        等待元素出现（WebDriverWait 封装）

        Args:
            selector: CSS选择器
            by: 选择器类型 (css/xpath/id/name)
            timeout: 超时时间

        Returns:
            bool: 元素是否出现
        """
        if not self.driver or not self.wait:
            return False
        try:
            by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME}
            self.wait.until(
                EC.presence_of_element_located((by_map.get(by, By.CSS_SELECTOR), selector))
            )
            return True
        except Exception:
            return False

    def screenshot_captcha(self, selector: Optional[str] = None,
                           filename: str = "captcha.png") -> Optional[str]:
        """
        截图验证码

        Args:
            selector: CSS选择器，None 时截全屏
            filename: 保存文件名

        Returns:
            文件路径 或 None
        """
        if not self.driver:
            self.config.warning("浏览器未初始化")
            return None

        try:
            if selector:
                # 等待元素出现后再截图
                if self.wait_element(selector, timeout=5):
                    elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    path = os.path.join(self.config.screenshot_dir, filename)
                    elem.screenshot(path)
                else:
                    self.config.warning(f"等待验证码元素超时: {selector}")
                    return None
            else:
                # 截全屏
                path = os.path.join(self.config.screenshot_dir, filename)
                self.driver.save_screenshot(path)

            self.config.info(f"验证码截图: {path}")
            return path
        except Exception as e:
            self.config.error(f"验证码截图失败: {e}")
            return None

    def recognize_simple(self, image_path: Optional[str] = None) -> str:
        """
        简单 OCR 识别（数字+字母）

        Args:
            image_path: 图片路径，None 时使用默认截图

        Returns:
            识别结果
        """
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")

        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()

            # 优先使用 DdddOcr
            if DDDDOCR_AVAILABLE and self._ocr is not None:
                result = self._ocr.classification(image_bytes)
                return result.strip()

            # Fallback: pytesseract（需系统安装 tesseract-ocr）
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path)
                img = img.convert('L')
                threshold = 128
                img = img.point(lambda x: 255 if x > threshold else 0)
                result = pytesseract.image_to_string(
                    img,
                    config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                )
                return result.strip()

            self.config.error("验证码识别失败: 未安装 DdddOcr 且 pytesseract 不可用")
            return ""
        except Exception as e:
            self.config.error(f"验证码识别失败: {e}")
            return ""

    def recognize_number(self, image_path: Optional[str] = None) -> str:
        """
        识别纯数字

        Args:
            image_path: 图片路径

        Returns:
            识别结果
        """
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")

        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()

            # DdddOcr 自动识别数字，效果优于 pytesseract
            if DDDDOCR_AVAILABLE and self._ocr is not None:
                result = self._ocr.classification(image_bytes)
                return result.strip()

            # Fallback: pytesseract
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path)
                img = img.convert('L')
                result = pytesseract.image_to_string(
                    img,
                    config='--psm 7 -c tessedit_char_whitelist=0123456789'
                )
                return result.strip()

            self.config.error("数字识别失败: 未安装 DdddOcr 且 pytesseract 不可用")
            return ""
        except Exception as e:
            self.config.error(f"数字识别失败: {e}")
            return ""

    def recognize_chinese(self, image_path: Optional[str] = None) -> str:
        """
        识别中文

        Args:
            image_path: 图片路径

        Returns:
            识别结果
        """
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")

        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()

            # DdddOcr 对中文支持更好
            if DDDDOCR_AVAILABLE and self._ocr is not None:
                result = self._ocr.classification(image_bytes)
                return result.strip()

            # Fallback: pytesseract
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path)
                img = img.convert('L')
                result = pytesseract.image_to_string(img, lang='chi_sim')
                return result.strip()

            self.config.error("中文识别失败: 未安装 DdddOcr 且 pytesseract 不可用")
            return ""
        except Exception as e:
            self.config.error(f"中文识别失败: {e}")
            return ""

    def recognize_with_config(self, image_path: str, psm: int = 7,
                              whitelist: str = "") -> str:
        """
        使用 DdddOcr 识别（自定义配置参数保留，仅作参考）

        Args:
            image_path: 图片路径
            psm: 页面分割模式（仅 pytesseract fallback 使用）
            whitelist: 白名单字符（仅 pytesseract fallback 使用）

        Returns:
            识别结果
        """
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()

            # 优先使用 DdddOcr
            if DDDDOCR_AVAILABLE and self._ocr is not None:
                result = self._ocr.classification(image_bytes)
                return result.strip()

            # Fallback: pytesseract
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path)
                img = img.convert('L')
                config_parts = [f'--psm {psm}']
                if whitelist:
                    config_parts.append(f'-c tessedit_char_whitelist={whitelist}')
                result = pytesseract.image_to_string(img, config=' '.join(config_parts))
                return result.strip()

            self.config.error("识别失败: 未安装 DdddOcr 且 pytesseract 不可用")
            return ""
        except Exception as e:
            self.config.error(f"识别失败: {e}")
            return ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class SliderCaptcha:
    """
    滑块验证码识别器
    使用 OpenCV 模板匹配识别缺口位置
    """

    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        初始化滑块验证码识别器

        Args:
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None

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
            self.wait = WebDriverWait(self.driver, 10)

            self.config.set_headless(original_headless)
            self.config.info("滑块验证码浏览器启动成功")
            return True
        except Exception as e:
            self.config.error(f"滑块验证码浏览器启动失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.config.info("滑块验证码浏览器已关闭")

    def recognize_distance(self, bg_image: Union[str, Image.Image, np.ndarray],
                          gap_image: Union[str, Image.Image, np.ndarray],
                          offset: float = 0) -> float:
        """
        计算缺口距离（使用 OpenCV 模板匹配）

        Args:
            bg_image: 背景图路径 或 PIL Image 或 np.ndarray
            gap_image: 缺口/滑块图路径 或 PIL Image 或 np.ndarray
            offset: 偏移补偿（某些网站滑块有左边距）

        Returns:
            float: 缺口距离（像素），识别失败返回 -1

        Algorithm:
            1. 将背景图转为灰度
            2. 用缺口图作为模板在背景图上滑动，做标准化模板匹配
            3. 找到匹配度最低（缺口）的位置，即为缺口
        """
        try:
            # 统一转为 cv2 图像格式
            bg = self._to_cv2_image(bg_image)
            gap = self._to_cv2_image(gap_image)

            # 转为灰度
            bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
            gap_gray = cv2.cvtColor(gap, cv2.COLOR_BGR2GRAY)

            # 模板匹配
            # 使用 TM_SQDIFF_NORMED：差值平方和标准化，找最小值位置 = 缺口
            result = cv2.matchTemplate(bg_gray, gap_gray, cv2.TM_SQDIFF_NORMED)
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)

            distance = float(min_loc[0]) + offset

            self.config.info(
                f"滑块缺口识别完成: 距离={distance:.1f}px, 匹配差值={min_val:.4f}"
            )
            return distance

        except Exception as e:
            self.config.error(f"滑块缺口识别失败: {e}")
            return -1

    def recognize_distance_by_screenshot(self, bg_selector: str,
                                        gap_selector: str,
                                        bg_filename: str = "slider_bg.png",
                                        gap_filename: str = "slider_gap.png",
                                        offset: float = 0) -> float:
        """
        从页面截图中识别缺口距离

        Args:
            bg_selector: 背景图 CSS 选择器
            gap_selector: 缺口/滑块图 CSS 选择器
            bg_filename: 背景图保存文件名
            gap_filename: 缺口图保存文件名
            offset: 偏移补偿

        Returns:
            float: 缺口距离（像素）
        """
        if not self.driver:
            self.config.error("浏览器未初始化")
            return -1

        try:
            # 等待元素出现
            if not self.wait_element(bg_selector, timeout=10):
                self.config.error(f"背景图元素未找到: {bg_selector}")
                return -1
            if not self.wait_element(gap_selector, timeout=10):
                self.config.error(f"缺口图元素未找到: {gap_selector}")
                return -1

            # 截图
            bg_elem = self.driver.find_element(By.CSS_SELECTOR, bg_selector)
            gap_elem = self.driver.find_element(By.CSS_SELECTOR, gap_selector)

            # 保存到临时文件
            bg_path = os.path.join(self.config.screenshot_dir, bg_filename)
            gap_path = os.path.join(self.config.screenshot_dir, gap_filename)

            bg_elem.screenshot(bg_path)
            gap_elem.screenshot(gap_path)

            self.config.debug(f"滑块截图已保存: {bg_path}, {gap_path}")

            return self.recognize_distance(bg_path, gap_path, offset=offset)

        except Exception as e:
            self.config.error(f"滑块截图识别失败: {e}")
            return -1

    def drag_to(self, browser: webdriver.Chrome,
                slider_selector: str,
                distance: float,
                duration: float = 0.8,
                steps: int = 30) -> bool:
        """
        拖动滑块到缺口位置（带轨迹防检测）

        Args:
            browser: Selenium WebDriver 实例
            slider_selector: 滑块元素的 CSS 选择器
            distance: 缺口距离（像素）
            duration: 拖动总时长（秒，默认 0.8）
            steps: 轨迹步数（默认 30）

        Returns:
            bool: 是否成功

        Note:
            使用缓动函数生成非匀速轨迹，模拟人类拖动行为
        """
        if not browser or distance < 0:
            return False

        try:
            slider = browser.find_element(By.CSS_SELECTOR, slider_selector)

            # 生成带缓动的轨迹
            track = generate_slider_track(distance, steps=steps, ease_func=ease_out_quad)

            # 使用 ActionChains 执行拖动
            ActionChains(browser).move_to_element(slider).perform()

            # 按轨迹拖动（每次 move_by_offset）
            for i, (x, y) in enumerate(track):
                ActionChains(browser).move_by_offset(x, y).perform()
                # 每个步骤间隔
                time.sleep(duration / steps)

            # 松开鼠标
            ActionChains(browser).release().perform()

            self.config.info(f"滑块拖动完成: distance={distance:.1f}px")
            return True

        except Exception as e:
            self.config.error(f"滑块拖动失败: {e}")
            return False

    def drag_to_slow(self, browser: webdriver.Chrome,
                     slider_selector: str,
                     distance: float) -> bool:
        """
        拖动滑块（慢速版，更接近人类行为）

        Args:
            browser: Selenium WebDriver 实例
            slider_selector: 滑块元素的 CSS 选择器
            distance: 缺口距离（像素）

        Returns:
            bool: 是否成功
        """
        if not browser or distance < 0:
            return False

        try:
            slider = browser.find_element(By.CSS_SELECTOR, slider_selector)

            # 鼠标悬停到滑块
            ActionChains(browser).move_to_element(slider).perform()

            # 按下鼠标
            ActionChains(browser).click_and_hold(slider).perform()

            # 生成 50 步轨迹，使用 ease_in_out_quad（更慢的起止）
            track = generate_slider_track(distance, steps=50, ease_func=ease_out_quad)
            for x, y in track:
                ActionChains(browser).move_by_offset(x, y).perform()
                # 每步 15-30ms 随机延迟，模拟人手抖动
                time.sleep(0.015 + (hash(x) % 15) / 1000)

            # 松开鼠标
            ActionChains(browser).release().perform()

            self.config.info(f"滑块慢速拖动完成: distance={distance:.1f}px")
            return True

        except Exception as e:
            self.config.error(f"滑块拖动失败: {e}")
            return False

    def wait_element(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """等待元素出现"""
        if not self.driver or not self.wait:
            return False
        try:
            by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME}
            self.wait.until(
                EC.presence_of_element_located((by_map.get(by, By.CSS_SELECTOR), selector))
            )
            return True
        except Exception:
            return False

    def _to_cv2_image(self, img: Union[str, Image.Image, np.ndarray]) -> np.ndarray:
        """
        将各种图像格式转为 cv2 图像 (np.ndarray BGR)

        Args:
            img: 文件路径 / PIL Image / np.ndarray

        Returns:
            np.ndarray: BGR 格式图像
        """
        if isinstance(img, str):
            # 文件路径
            img = cv2.imread(img)
            if img is None:
                raise ValueError(f"无法读取图片: {img}")
            return img
        elif isinstance(img, Image.Image):
            # PIL Image -> RGB -> BGR
            rgb = np.array(img.convert('RGB'))
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(img, np.ndarray):
            # np.ndarray 假设 RGB，转 BGR
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            raise TypeError(f"不支持的图片类型: {type(img)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class ClickCaptcha:
    """
    点选验证码识别器（基础版）
    提供接口框架，集成第三方打码 API
    """

    def __init__(self, config: Optional[BrowserConfig] = None,
                 api_url: str = None, api_key: str = None):
        """
        初始化点选验证码识别器

        Args:
            config: 配置对象
            api_url: 第三方打码 API URL（支持云打码、超级鹰等）
            api_key: API 密钥
        """
        self.config = config or get_config()
        self.api_url = api_url
        self.api_key = api_key
        self.driver: Optional[webdriver.Chrome] = None

    def init_browser(self, headless: bool = True) -> bool:
        """初始化浏览器"""
        try:
            original_headless = self.config.headless
            self.config.set_headless(headless)
            options = self.config.get_chrome_options()
            self.driver = webdriver.Chrome(options=options)
            self.config.set_headless(original_headless)
            return True
        except Exception as e:
            self.config.error(f"点选验证码浏览器启动失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_click_positions(self, image_path: str,
                             prompt: str = "") -> List[Tuple[float, float]]:
        """
        获取需要点击的位置（需接入第三方 API）

        Args:
            image_path: 验证码图片路径
            prompt: 点击提示，如"找到【跳过】按钮"

        Returns:
            List[Tuple[x, y]]: 点击坐标列表（相对比例 0-1）
        """
        if not self.api_url or not self.api_key:
            self.config.warning(
                "点选验证码需要配置第三方打码 API。"
                "请设置 api_url 和 api_key，或手动完成验证。"
            )
            return []

        try:
            # 调用第三方 API（示例：云打码格式）
            with open(image_path, 'rb') as f:
                files = {'image': f.read()}
                data = {
                    'key': self.api_key,
                    'type': 'click',      # 点选类型
                    'hint': prompt,        # 提示文字
                }
                resp = requests.post(self.api_url, files=files, data=data, timeout=30)
                result = resp.json()

            if result.get('code') == 0:
                positions = result.get('data', [])
                self.config.info(f"点选坐标获取成功: {positions}")
                return positions
            else:
                self.config.error(f"点选 API 错误: {result.get('msg')}")
                return []

        except Exception as e:
            self.config.error(f"点选坐标获取失败: {e}")
            return []

    def click_positions(self, browser: webdriver.Chrome,
                        container_selector: str,
                        positions: List[Tuple[float, float]]) -> bool:
        """
        在容器内点击指定比例坐标

        Args:
            browser: WebDriver
            container_selector: 验证码容器选择器
            positions: 相对坐标列表 [(x_ratio, y_ratio), ...]

        Returns:
            bool: 是否成功
        """
        if not browser:
            return False

        try:
            container = browser.find_element(By.CSS_SELECTOR, container_selector)
            container_size = container.size
            container_loc = container.location

            for x_ratio, y_ratio in positions:
                x = container_loc['x'] + int(container_size['width'] * x_ratio)
                y = container_loc['y'] + int(container_size['height'] * y_ratio)
                ActionChains(browser).move_by_offset(x, y).click().perform()
                time.sleep(0.3)

            return True
        except Exception as e:
            self.config.error(f"点选点击失败: {e}")
            return False

    def recognize_and_click(self, image_path: str,
                            prompt: str,
                            browser: webdriver.Chrome,
                            container_selector: str) -> bool:
        """
        识别并点击（完整流程）

        Args:
            image_path: 验证码图片路径
            prompt: 点击提示
            browser: WebDriver
            container_selector: 容器选择器

        Returns:
            bool: 是否成功
        """
        positions = self.get_click_positions(image_path, prompt)
        if not positions:
            return False
        return self.click_positions(browser, container_selector, positions)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='验证码识别工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s recognize captcha.png
  %(prog)s number captcha.png
  %(prog)s chinese captcha.png
  %(prog)s test
  %(prog)s screenshot --selector ".captcha-img" --name my_captcha.png
  %(prog)s slider-distance bg.png gap.png
  %(prog)s slider-test
        """
    )

    parser.add_argument('command', nargs='?', default='help',
                        help='命令: recognize, number, chinese, test, screenshot, slider-distance, slider-test, help')
    parser.add_argument('image_path', nargs='?', help='图片路径')
    parser.add_argument('image_path2', nargs='?', help='第二张图片路径（滑块用）')
    parser.add_argument('--selector', '-s', help='CSS选择器（用于页面截图）')
    parser.add_argument('--name', '-n', default='captcha.png', help='截图文件名')
    parser.add_argument('--psm', type=int, default=7, help='Tesseract页面分割模式')
    parser.add_argument('--whitelist', '-w', default='', help='字符白名单')
    parser.add_argument('--offset', type=float, default=0, help='滑块距离偏移补偿')

    args = parser.parse_args()

    if args.command == 'help':
        parser.print_help()
        print("""
命令说明:
  recognize <图片>        识别数字+字母
  number <图片>           识别纯数字
  chinese <图片>           识别中文
  test                    运行OCR测试
  screenshot              截取验证码（需配合init）
  slider-distance <bg> <gap>  计算滑块缺口距离
  slider-test             测试滑块识别
        """)
        return 0

    solver = CaptchaSolver()

    try:
        if args.command == 'recognize':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_simple(args.image_path)
            print(f"识别结果: {result}")

        elif args.command == 'number':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_number(args.image_path)
            print(f"识别结果: {result}")

        elif args.command == 'chinese':
            if not args.image_path:
                print("错误: 需要指定图片路径")
                return 1
            result = solver.recognize_chinese(args.image_path)
            print(f"识别结果: {result}")

        elif args.command == 'test':
            # 创建测试图片
            img = Image.new('RGB', (150, 50), color='white')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font = ImageFont.load_default()
            draw.text((10, 10), "ABC123", fill='black', font=font)

            test_path = os.path.join(solver.config.screenshot_dir, "test_captcha.png")
            img.save(test_path)

            result = solver.recognize_simple(test_path)
            print(f"测试识别: {result}")

        elif args.command == 'screenshot':
            # 需要先初始化浏览器
            if not args.selector:
                print("错误: 需要指定 --selector")
                return 1

            if solver.init_browser():
                path = solver.screenshot_captcha(args.selector, args.name)
                if path:
                    print(f"截图: {path}")
                solver.close()
            else:
                print("错误: 浏览器初始化失败")
                return 1

        elif args.command == 'slider-distance':
            if not args.image_path or not args.image_path2:
                print("错误: 需要指定背景图和缺口图路径")
                return 1
            slider = SliderCaptcha()
            distance = slider.recognize_distance(
                args.image_path, args.image_path2, offset=args.offset
            )
            print(f"缺口距离: {distance:.1f}px")

        elif args.command == 'slider-test':
            print("滑块验证码识别模块已加载")
            print("使用方法:")
            print("  1. 创建 SliderCaptcha 实例")
            print("  2. 调用 recognize_distance(bg_img, gap_img) 计算距离")
            print("  3. 调用 drag_to(driver, slider_sel, distance) 拖动滑块")
            print()
            print("示例:")
            print("  slider = SliderCaptcha()")
            print("  dist = slider.recognize_distance('bg.png', 'gap.png')")
            print("  slider.drag_to(driver, '.slider', dist)")

        else:
            print(f"未知命令: {args.command}")
            return 1

        return 0

    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
browser/captcha.py - 验证码识别模块
支持：数字、字母、汉字OCR识别、滑块缺口检测

依赖：ddddocr (纯Python OCR)、opencv-python (滑块匹配)
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, List, Union

import cv2
import numpy as np
from PIL import Image

# DdddOcr - 纯 Python OCR（主引擎）
try:
    from ddddocr import DdddOcr as _DdddOcr
    DDDDOCR_AVAILABLE = True
except ImportError:
    _DdddOcr = None
    DDDDOCR_AVAILABLE = False

# pytesseract - Fallback
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False

try:
    from core.config import get_config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.config import get_config


class CaptchaSolver:
    """
    验证码识别器（基于 DdddOcr）
    Usage:
        solver = CaptchaSolver()
        result = solver.recognize_simple("captcha.png")
        result = solver.recognize_number("captcha.png")
        result = solver.recognize_chinese("captcha.png")
    """

    def __init__(self, config=None):
        self.config = config or get_config()
        self._ocr = None
        if DDDDOCR_AVAILABLE:
            try:
                self._ocr = _DdddOcr()
                self.config.info("DdddOcr OCR 初始化成功")
            except Exception as e:
                self.config.warning(f"DdddOcr 初始化失败: {e}")
                self._ocr = None
        else:
            self.config.warning("DdddOcr 未安装，请运行: pip install ddddocr")

    def recognize(self, image_bytes: bytes) -> str:
        """使用 DdddOcr 识别"""
        if self._ocr:
            try:
                return self._ocr.classification(image_bytes).strip()
            except Exception as e:
                self.config.error(f"DdddOcr 识别失败: {e}")
        return ""

    def recognize_simple(self, image_path: Optional[str] = None) -> str:
        """识别数字+字母"""
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            if DDDDOCR_AVAILABLE and self._ocr:
                return self._ocr.classification(image_bytes).strip()
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path).convert('L')
                threshold = 128
                img = img.point(lambda x: 255 if x > threshold else 0)
                return pytesseract.image_to_string(
                    img,
                    config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                ).strip()
            self.config.error("验证码识别失败: 未安装 DdddOcr 且 pytesseract 不可用")
            return ""
        except Exception as e:
            self.config.error(f"识别失败: {e}")
            return ""

    def recognize_number(self, image_path: Optional[str] = None) -> str:
        """识别纯数字"""
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            if DDDDOCR_AVAILABLE and self._ocr:
                return self._ocr.classification(image_bytes).strip()
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path).convert('L')
                return pytesseract.image_to_string(
                    img,
                    config='--psm 7 -c tessedit_char_whitelist=0123456789'
                ).strip()
            return ""
        except Exception as e:
            self.config.error(f"数字识别失败: {e}")
            return ""

    def recognize_chinese(self, image_path: Optional[str] = None) -> str:
        """识别中文"""
        if image_path is None:
            image_path = os.path.join(self.config.screenshot_dir, "captcha.png")
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            if DDDDOCR_AVAILABLE and self._ocr:
                return self._ocr.classification(image_bytes).strip()
            if PYTESSERACT_AVAILABLE:
                img = Image.open(image_path).convert('L')
                return pytesseract.image_to_string(img, lang='chi_sim').strip()
            return ""
        except Exception as e:
            self.config.error(f"中文识别失败: {e}")
            return ""


class SliderCaptcha:
    """
    滑块验证码识别器
    使用 OpenCV 模板匹配检测缺口位置
    """

    def __init__(self, config=None):
        self.config = config or get_config()

    def recognize_distance(self, bg_image: Union[str, Image.Image, np.ndarray],
                          gap_image: Union[str, Image.Image, np.ndarray],
                          offset: float = 0) -> float:
        """
        计算滑块缺口距离

        Args:
            bg_image: 背景图（路径/PIL Image/np.ndarray）
            gap_image: 缺口滑块图
            offset: 偏移补偿

        Returns:
            缺口距离（像素），失败返回 -1
        """
        try:
            bg = self._to_cv2(bg_image)
            gap = self._to_cv2(gap_image)
            bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
            gap_gray = cv2.cvtColor(gap, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(bg_gray, gap_gray, cv2.TM_SQDIFF_NORMED)
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)
            distance = float(min_loc[0]) + offset
            self.config.info(f"滑块缺口识别: 距离={distance:.1f}px, 匹配差值={min_val:.4f}")
            return distance
        except Exception as e:
            self.config.error(f"滑块缺口识别失败: {e}")
            return -1

    def _to_cv2(self, img: Union[str, Image.Image, np.ndarray]) -> np.ndarray:
        if isinstance(img, str):
            result = cv2.imread(img)
            if result is None:
                raise ValueError(f"无法读取图片: {img}")
            return result
        elif isinstance(img, Image.Image):
            rgb = np.array(img.convert('RGB'))
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(img, np.ndarray):
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        raise TypeError(f"不支持的图片类型: {type(img)}")


def main():
    parser = argparse.ArgumentParser(description='验证码识别工具')
    parser.add_argument('command', nargs='?', default='help',
                        help='命令: recognize, number, chinese, test')
    parser.add_argument('image_path', nargs='?', help='图片路径')

    args = parser.parse_args()
    if args.command == 'help':
        parser.print_help()
        return 0

    solver = CaptchaSolver()
    try:
        if args.command == 'recognize':
            result = solver.recognize_simple(args.image_path)
            print(f"识别结果: {result}")
        elif args.command == 'number':
            result = solver.recognize_number(args.image_path)
            print(f"识别结果: {result}")
        elif args.command == 'chinese':
            result = solver.recognize_chinese(args.image_path)
            print(f"识别结果: {result}")
        elif args.command == 'test':
            print(f"DdddOcr可用: {DDDDOCR_AVAILABLE}")
            print(f"Pytesseract可用: {PYTESSERACT_AVAILABLE}")
        return 0
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

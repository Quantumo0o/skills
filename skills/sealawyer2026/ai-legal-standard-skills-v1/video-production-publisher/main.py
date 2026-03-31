#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频制作和发布脚本
功能：通过剪映、视频号、抖音API自动化视频制作和发布
"""

import requests
import json
import sys
import os
import time
from pathlib import Path
from datetime import datetime

# 导入配置
try:
    from config import CONFIG
except ImportError:
    print("❌ 配置文件不存在，请先创建 config.py")
    sys.exit(1)

# ============================================
# 日志配置
# ============================================

def log(message):
    """日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# ============================================
# API 基础类
# ============================================

class BaseAPI:
    """API 基础类"""
    
    def __init__(self, app_id, app_secret, api_base):
        self.app_id = app_id
        self.app_secret = app_secret
        self.api_base = api_base
        self.access_token = None
        self.token_expire_time = None
    
    def get_access_token(self):
        """获取 access_token"""
        # 检查 token 是否过期
        if self.access_token and self.token_expire_time:
            if datetime.now() < self.token_expire_time:
                log(f"✅ Token 有效，过期时间：{self.token_expire_time}")
                return self.access_token
        
        log(f"📡 正在获取新的 access_token...")
        url = f"{self.api_base}/oauth2/access_token"
        
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "grant_type": "client_credential"
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            # 设置过期时间（提前5分钟刷新）
            expires_in = result.get("expires_in", 7200)
            self.token_expire_time = datetime.now() + timedelta(seconds=expires_in - 300)
            log(f"✅ Token 获取成功，过期时间：{self.token_expire_time}")
            return self.access_token
        else:
            log(f"❌ Token 获取失败：{result}")
            raise Exception(f"Token 获取失败：{result}")
    
    def api_request(self, method, endpoint, data=None, files=None):
        """API 请求"""
        url = f"{self.api_base}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }
        
        log(f"📤 API 请求：{method} {url}")
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                if files:
                    headers.pop("Content-Type")
                    response = requests.post(url, headers=headers, files=files)
                else:
                    response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"不支持的 HTTP 方法：{method}")
            
            log(f"📥 API 响应：{response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Token 过期，重新获取
                log(f"⚠️ Token 过期，正在重新获取...")
                self.get_access_token()
                # 重新发送请求
                return self.api_request(method, endpoint, data, files)
            else:
                log(f"❌ API 请求失败：{response.status_code} {response.text}")
                raise Exception(f"API 请求失败：{response.status_code}")
                
        except Exception as e:
            log(f"❌ API 请求异常：{str(e)}")
            raise

# ============================================
# 剪映 API 类
# ============================================

class JianyingAPI(BaseAPI):
    """剪映 API"""
    
    def __init__(self):
        jianying_config = CONFIG.get("jianying", {})
        super().__init__(
            jianying_config.get("app_id", ""),
            jianying_config.get("app_secret", ""),
            jianying_config.get("api_base", "https://open.capcut.cn/api/v1")
        )
    
    def upload_material(self, file_path, material_type="video"):
        """上传素材"""
        log(f"📤 正在上传素材：{file_path}")
        
        url = f"{self.api_base}/material/upload"
        
        files = {
            "file": open(file_path, "rb")
        }
        
        data = {
            "type": material_type
        }
        
        try:
            result = self.api_request("POST", url, files=files)
            
            if "data" in result:
                material_data = result["data"]
                log(f"✅ 素材上传成功")
                log(f"   material_id: {material_data.get('material_id', 'N/A')}")
                log(f"   material_url: {material_data.get('material_url', 'N/A')}")
                return material_data
            else:
                log(f"❌ 素材上传失败：{result}")
                raise Exception(f"素材上传失败：{result}")
                
        except Exception as e:
            log(f"❌ 素材上传异常：{str(e)}")
            raise
    
    def create_draft(self, material_id, title, content):
        """创建草稿"""
        log(f"📝 正在创建草稿：{title}")
        
        url = f"{self.api_base}/draft/create"
        
        data = {
            "material_id": material_id,
            "title": title,
            "content": content
        }
        
        try:
            result = self.api_request("POST", url, data=data)
            
            if "data" in result:
                draft_data = result["data"]
                log(f"✅ 草稿创建成功")
                log(f"   draft_id: {draft_data.get('draft_id', 'N/A')}")
                return draft_data
            else:
                log(f"❌ 草稿创建失败：{result}")
                raise Exception(f"草稿创建失败：{result}")
                
        except Exception as e:
            log(f"❌ 草稿创建异常：{str(e)}")
            raise
    
    def export_draft(self, draft_id, template_id=None):
        """导出草稿"""
        log(f"📤 正在导出草稿：{draft_id}")
        
        url = f"{self.api_base}/draft/export"
        
        data = {
            "draft_id": draft_id
        }
        
        if template_id:
            data["template_id"] = template_id
        
        try:
            result = self.api_request("POST", url, data=data)
            
            if "data" in result:
                task_data = result["data"]
                log(f"✅ 草稿导出成功，任务开始")
                log(f"   task_id: {task_data.get('task_id', 'N/A')}")
                return task_data
            else:
                log(f"❌ 草稿导出失败：{result}")
                raise Exception(f"草稿导出失败：{result}")
                
        except Exception as e:
            log(f"❌ 草稿导出异常：{str(e)}")
            raise

# ============================================
# 主函数
# ============================================

def main():
    """主函数"""
    log("=" * 60)
    log("视频制作和发布工具")
    log("=" * 60)
    
    # 检查配置
    jianying_config = CONFIG.get("jianying", {})
    if not jianying_config.get("app_id"):
        log("❌ 剪映配置未填写，请先在 config.py 中填写 jianying.app_id 和 jianying.app_secret")
        log("请在 config.py 中填写：")
        log("   JIANYING_APP_ID = \"您的剪映 AppID\"")
        log("   JIANYING_APP_SECRET = \"您的剪映 AppSecret\"")
        sys.exit(1)
    
    # 创建剪映 API 实例
    jianying_api = JianyingAPI()
    
    # 测试：获取 access_token
    try:
        jianying_api.get_access_token()
        log("✅ 剪映 Token 获取成功")
    except Exception as e:
        log(f"❌ 剪映 Token 获取失败：{str(e)}")
        sys.exit(1)
    
    log("\n" + "=" * 60)
    log("请选择功能：")
    log("  1. 上传视频素材")
    log("  2. 创建视频草稿")
    log("  3. 导出视频")
    log("  4. 发布到视频号")
    log("  5. 发布到抖音")
    log("  6. 批量处理（上传+创建+导出）")
    log("  7. 退出")
    log("=" * 60)
    
    choice = input("\n请输入选择 (1-7): ").strip()
    
    if choice == "7":
        log("已退出")
        sys.exit(0)
    
    # 处理选择
    if choice == "1":
        # 上传视频素材
        file_path = input("\n请输入视频文件路径：").strip()
        if os.path.exists(file_path):
            try:
                material_data = jianying_api.upload_material(file_path)
                log(f"\n✅ 素材上传成功！")
                log(f"   material_id: {material_data.get('material_id', 'N/A')}")
                log(f"   material_url: {material_data.get('material_url', 'N/A')}")
            except Exception as e:
                log(f"\n❌ 素材上传失败：{str(e)}")
        else:
            log(f"\n❌ 文件不存在：{file_path}")
    
    elif choice == "2":
        # 创建视频草稿
        material_id = input("\n请输入素材 ID: ").strip()
        title = input("请输入视频标题：").strip()
        content = input("请输入视频描述：").strip()
        
        try:
            draft_data = jianying_api.create_draft(material_id, title, content)
            log(f"\n✅ 草稿创建成功！")
            log(f"   draft_id: {draft_data.get('draft_id', 'N/A')}")
        except Exception as e:
            log(f"\n❌ 草稿创建失败：{str(e)}")
    
    elif choice == "3":
        # 导出视频
        draft_id = input("\n请输入草稿 ID: ").strip()
        template_id = input("请输入模板 ID（可选，直接回车跳过）: ").strip()
        
        try:
            task_data = jianying_api.export_draft(draft_id, template_id if template_id else None)
            log(f"\n✅ 草稿导出成功，任务开始！")
            log(f"   task_id: {task_data.get('task_id', 'N/A')}")
        except Exception as e:
            log(f"\n❌ 草稿导出失败：{str(e)}")
    
    elif choice == "4":
        # 发布到视频号
        log("⚠️ 视频号 API 需要额外配置，当前暂未实现")
        log("请手动使用剪映发布到视频号")
    
    elif choice == "5":
        # 发布到抖音
        log("⚠️ 抖音 API 需要额外配置，当前暂未实现")
        log("请手动使用剪映发布到抖音")
    
    elif choice == "6":
        # 批量处理
        log("📋 批量处理功能")
        file_path = input("\n请输入视频文件路径：").strip()
        title = input("请输入视频标题：").strip()
        content = input("请输入视频描述：").strip()
        
        if os.path.exists(file_path):
            try:
                # 上传素材
                log("\n步骤1/3：上传素材...")
                material_data = jianying_api.upload_material(file_path)
                material_id = material_data.get('material_id', '')
                
                # 创建草稿
                log("\n步骤2/3：创建草稿...")
                draft_data = jianying_api.create_draft(material_id, title, content)
                draft_id = draft_data.get('draft_id', '')
                
                # 导出视频
                log("\n步骤3/3：导出视频...")
                task_data = jianying_api.export_draft(draft_id)
                
                log(f"\n✅ 批量处理完成！")
                log(f"   素材 ID: {material_id}")
                log(f"   草稿 ID: {draft_id}")
                log(f"   任务 ID: {task_data.get('task_id', 'N/A')}")
            except Exception as e:
                log(f"\n❌ 批量处理失败：{str(e)}")
        else:
            log(f"\n❌ 文件不存在：{file_path}")
    
    else:
        log("❌ 无效的选择")
        sys.exit(1)
    
    log("\n完成！")

if __name__ == "__main__":
    main()

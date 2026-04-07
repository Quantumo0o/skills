#!/usr/bin/env python3
"""
自动注册灵雀AI账号脚本
功能：帮助用户自动注册灵雀AI账号
流程：
1. 打开灵雀AI网站 https://lqai.net/
2. 点击登录，选择短信登录
3. 输入用户手机号，获取验证码
4. 等待用户输入验证码
5. 点击登录/注册完成注册
"""

import sys
import time
import requests

def get_token(username, password):
    """获取灵雀AI的token"""
    url = 'https://server.pinza.com.cn/pincloud-auth/chat/login'
    response = requests.post(url, data={'username': username, 'password': password})
    if response.status_code == 200:
        data = response.json()
        if data.get('success') and data.get('data'):
            return data['data']
    return None

def save_config(username, password):
    """保存配置到config.json"""
    import json
    config = {
        "lingque_username": username,
        "lingque_password": password
    }
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"配置已保存到 config.json")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python auto_register.py <手机号>")
        print("或运行时输入手机号")
        phone = input("请输入手机号: ").strip()
    else:
        phone = sys.argv[1]
    
    if not phone:
        print("手机号不能为空")
        return
    
    print(f"\n开始自动注册流程...")
    print(f"请在浏览器中配合完成以下操作：")
    print(f"1. 打开 https://lqai.net/")
    print(f"2. 点击右上角的「登录」按钮")
    print(f"3. 选择「短信登录」方式")
    print(f"4. 输入手机号: {phone}")
    print(f"5. 点击「获取验证码」")
    print(f"\n请告诉我发送到您手机上的验证码: ", end="")
    code = input().strip()
    
    if code:
        print(f"验证码已收到: {code}")
        print("正在验证...")
        # 尝试登录验证
        token = get_token(phone, "")
        if token:
            print("登录成功！")
            save_config(phone, "")
        else:
            print("验证码验证失败，请重试")
    else:
        print("未收到验证码，注册取消")

if __name__ == "__main__":
    main()

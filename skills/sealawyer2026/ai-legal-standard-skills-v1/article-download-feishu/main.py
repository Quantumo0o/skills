#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 文章下载技能 - 飞书版 - 主程序

import sys
import os
import json
from pathlib import Path

# 添加技能目录到Python路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

from __init__ import ArticleDownloadFeishu

def print_separator(char="=", length=50):
    """打印分隔线"""
    print(char * length)

def print_header(title):
    """打印标题"""
    print_separator()
    print(f"  {title}")
    print_separator()

def print_section(title):
    """打印部分标题"""
    print(f"\n{'-' * 50}")
    print(f"  {title}")
    print(f"{'-' * 50}")

def print_info(key, value):
    """打印信息"""
    print(f"   - {key}: {value}")

def print_success(message):
    """打印成功信息"""
    print(f"   ✅ {message}")

def print_error(message):
    """打印错误信息"""
    print(f"   ❌ {message}")

def print_warning(message):
    """打印警告信息"""
    print(f"   ⚠️  {message}")

def main():
    """主程序"""
    
    print_header("文章下载技能 - 飞书版")
    
    # 创建技能实例
    skill = ArticleDownloadFeishu()
    
    # 显示技能信息
    print_section("技能信息")
    print_info("技能名称", "article-download-feishu")
    print_info("技能版本", "1.0.0")
    print_info("技能目录", str(skill.skill_dir))
    print_info("文章目录", str(skill.articles_dir))
    print_info("上传目录", str(skill.uploads_dir))
    
    # 显示可用的文章模板
    print_section("可用的文章模板")
    templates = list(skill.article_templates.keys())
    for i, key in enumerate(templates, 1):
        template = skill.article_templates[key]
        print(f"   {i}. {key}")
        print(f"      标题: {template.get('title', '')}")
        print()
    
    # 显示可用功能
    print_section("可用功能")
    print(f"   1. 生成文章")
    print(f"   2. 上传到飞书")
    print(f"   3. 创建飞书卡片")
    print(f"   4. 发送文本版本")
    print()
    
    # 显示菜单
    print_section("请选择操作")
    print(f"   1. 生成文章")
    print(f"   2. 上传到飞书")
    print(f"   3. 创建飞书卡片")
    print(f"   4. 发送文本版本")
    print(f"   5. 退出")
    print()
    
    # 等待用户输入
    while True:
        try:
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == "1":
                print_section("生成文章")
                
                # 选择模板
                print(f"\n可用的文章模板:")
                for i, key in enumerate(templates, 1):
                    template = skill.article_templates[key]
                    print(f"   {i}. {key}")
                    print(f"      标题: {template.get('title', '')}")
                
                template_choice = input("\n请选择文章模板 (输入序号或模板键): ").strip()
                
                # 检查输入
                if template_choice.isdigit():
                    index = int(template_choice) - 1
                    if 0 <= index < len(templates):
                        template_key = templates[index]
                    else:
                        print_error("无效的选项")
                        continue
                else:
                    if template_choice in templates:
                        template_key = template_choice
                    else:
                        print_error("无效的选项")
                        continue
                
                # 生成文章
                result = skill.save_article(template_key)
                if result.get("success"):
                    print_success(f"文章已生成: {result.get('file_name')}")
                    print_info("文件路径", result.get("file_path"))
                    print_info("文件大小", f"{result.get('file_size')} bytes")
                else:
                    print_error("文章生成失败")
                
            elif choice == "2":
                print_section("上传到飞书")
                print_warning("此功能需要进一步实现")
                
                # 列出可用的文章
                print(f"\n可用的文章:")
                article_files = list(skill.articles_dir.glob("*.md"))
                if not article_files:
                    print_warning("没有可用的文章")
                    continue
                
                for i, file_path in enumerate(article_files, 1):
                    file_size = file_path.stat().st_size
                    print(f"   {i}. {file_path.name} ({file_size/1024:.1f} KB)")
                
                file_choice = input("\n请选择要上传的文章 (输入序号): ").strip()
                
                # 检查输入
                if not file_choice.isdigit():
                    print_error("无效的选项")
                    continue
                
                index = int(file_choice) - 1
                if 0 <= index < len(article_files):
                    file_path = article_files[index]
                    print_info("选中的文件", file_path.name)
                    print_info("文件大小", f"{file_path.stat().st_size/1024:.1f} KB")
                    
                    # TODO: 实现飞书上传功能
                    # result = skill.upload_to_feishu(file_path)
                    # if result.get("success"):
                    #     print_success(f"文件已上传: {result.get('file_name')}")
                    #     print_info("下载链接", result.get('download_url'))
                    # else:
                    #     print_error("文件上传失败")
                else:
                    print_error("无效的选项")
                    continue
                
            elif choice == "3":
                print_section("创建飞书卡片")
                print_warning("此功能需要进一步实现")
                print_warning("需要:")
                print_warning("   1. 完成飞书API集成")
                print_warning("   2. 实现文件上传功能")
                print_warning("   3. 实现卡片生成功能")
                print_warning("   4. 实现消息发送功能")
                
            elif choice == "4":
                print_section("发送文本版本")
                print_warning("此功能需要进一步实现")
                print_warning("需要:")
                print_warning("   1. 完成飞书机器人API集成")
                print_warning("   2. 实现消息发送功能")
                
            elif choice == "5":
                print_section("退出")
                print("谢谢使用！")
                break
                
            else:
                print_warning("无效的选项，请重新输入")
            
            print()
            
        except KeyboardInterrupt:
            print("\n")
            print_separator()
            print("已退出")
            print_separator()
            break
        except Exception as e:
            print_error(f"发生错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

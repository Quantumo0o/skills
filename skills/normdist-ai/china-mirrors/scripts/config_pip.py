#!/usr/bin/env python3
"""
自动配置 pip 国内镜像源
支持 Windows、Linux、Mac 系统
"""
import os
import sys
import platform
from pathlib import Path

# 可用的镜像源
MIRRORS = {
    'aliyun': {
        'url': 'https://mirrors.aliyun.com/pypi/simple/',
        'host': 'mirrors.aliyun.com',
        'name': '阿里云'
    },
    'tsinghua': {
        'url': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'host': 'pypi.tuna.tsinghua.edu.cn',
        'name': '清华大学'
    },
    'ustc': {
        'url': 'https://pypi.mirrors.ustc.edu.cn/simple/',
        'host': 'pypi.mirrors.ustc.edu.cn',
        'name': '中科大'
    },
    'tencent': {
        'url': 'https://mirrors.cloud.tencent.com/pypi/simple/',
        'host': 'mirrors.cloud.tencent.com',
        'name': '腾讯云'
    }
}

def get_config_path():
    """获取 pip 配置文件路径"""
    system = platform.system()
    if system == 'Windows':
        return Path.home() / 'pip' / 'pip.ini'
    else:
        return Path.home() / '.pip' / 'pip.conf'

def create_config(mirror='aliyun', project_level=False, project_path=None):
    """创建 pip 配置文件
    
    Args:
        mirror: 镜像源名称
        project_level: 是否项目级配置
        project_path: 项目路径（项目级配置时需要）
    """
    if project_level:
        if not project_path:
            project_path = Path.cwd()
        config_path = Path(project_path) / 'pip.conf'
    else:
        config_path = get_config_path()
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    mirror_info = MIRRORS.get(mirror, MIRRORS['aliyun'])
    mirror_url = mirror_info['url']
    host = mirror_info['host']
    
    config_content = f"""[global]
index-url = {mirror_url}
trusted-host = {host}

[install]
trusted-host = {host}
"""
    
    config_path.write_text(config_content, encoding='utf-8')
    
    level = "项目级" if project_level else "全局"
    print(f"✓ pip {level}配置已保存到: {config_path}")
    print(f"✓ 使用镜像: {mirror_info['name']} ({mirror_url})")
    
    return config_path

def show_current_config():
    """显示当前配置"""
    config_path = get_config_path()
    if config_path.exists():
        print(f"\n当前 pip 配置文件: {config_path}")
        print("=" * 60)
        print(config_path.read_text(encoding='utf-8'))
        print("=" * 60)
    else:
        print("✗ 未找到 pip 配置文件")

def list_mirrors():
    """列出所有可用镜像"""
    print("\n可用的 pip 镜像源:")
    print("-" * 60)
    for key, info in MIRRORS.items():
        print(f"  {key:12} - {info['name']:10} - {info['url']}")
    print("-" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='自动配置 pip 国内镜像源')
    parser.add_argument('mirror', nargs='?', default='aliyun',
                       choices=list(MIRRORS.keys()),
                       help='选择镜像源 (默认: aliyun)')
    parser.add_argument('--project', '-p', action='store_true',
                       help='项目级配置（在当前目录创建 pip.conf）')
    parser.add_argument('--show', '-s', action='store_true',
                       help='显示当前配置')
    parser.add_argument('--list', '-l', action='store_true',
                       help='列出所有可用镜像')
    
    args = parser.parse_args()
    
    if args.list:
        list_mirrors()
        return
    
    if args.show:
        show_current_config()
        return
    
    # 执行配置
    create_config(args.mirror, args.project)
    
    print("\n验证配置:")
    print("运行以下命令测试:")
    print(f"  pip install --verbose requests 2>&1 | grep -i '{args.mirror}'")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HBM Memory System 一键安装脚本
支持: macOS, Windows, Linux
版本: v1.0.0
"""

import os
import sys
import platform
import subprocess
import shutil
import time
from pathlib import Path
import json

# ==================== 配置区域 ====================
REQUIRED_PYTHON_VERSION = (3, 8)
REQUIRED_PACKAGES = [
    "chromadb>=0.5.0",
    "sentence-transformers>=2.7.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "tqdm>=4.66.0",
]

# 模型配置
MODEL_CONFIG = {
    "name": "all-MiniLM-L6-v2",
    "source": "modelscope",
    "url": "https://modelscope.cn/models/sentence-transformers/all-MiniLM-L6-v2",
    "local_path": "models/all-MiniLM-L6-v2/sentence-transformers/all-MiniLM-L6-v2"
}

# 目录结构
DIRECTORY_STRUCTURE = [
    "memory/目标记忆库",
    "memory/会话记忆库", 
    "memory/版本记忆库",
    "memory/经验记忆库",
    "memory/情感记忆库",
    "memory/心跳回忆",
    "memory/语义搜索_db",
    "memory/RAG",
    "scripts",
    "references",
    "models/all-MiniLM-L6-v2/sentence-transformers/all-MiniLM-L6-v2"
]

# ==================== 工具函数 ====================

def print_colored(text, color="white"):
    """彩色输出"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    if platform.system() == "Windows":
        print(text)  # Windows不支持ANSI颜色
    else:
        print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def check_python_version():
    """检查Python版本"""
    print_colored("🔍 检查Python版本...", "cyan")
    if sys.version_info < REQUIRED_PYTHON_VERSION:
        print_colored(f"❌ Python版本过低: {sys.version_info.major}.{sys.version_info.minor}", "red")
        print_colored(f"   需要Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} 或更高版本", "yellow")
        return False
    print_colored(f"✅ Python版本符合要求: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "green")
    return True

def check_platform():
    """检查操作系统"""
    print_colored("🔍 检测操作系统...", "cyan")
    system = platform.system()
    release = platform.release()
    
    print_colored(f"✅ 操作系统: {system} {release}", "green")
    
    # 检查是否为Windows且可能需要管理员权限
    if system == "Windows":
        print_colored("⚠️  检测到Windows系统，某些操作可能需要管理员权限", "yellow")
    
    return system

def install_packages():
    """安装Python依赖包"""
    print_colored("📦 安装Python依赖包...", "cyan")
    
    # 检查pip是否可用
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print_colored("❌ 未找到pip，请先安装pip", "red")
        return False
    
    # 安装包
    for package in REQUIRED_PACKAGES:
        print_colored(f"   安装 {package}...", "blue")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=True,
                capture_output=True,
                text=True
            )
            print_colored(f"   ✅ {package} 安装成功", "green")
        except subprocess.CalledProcessError as e:
            print_colored(f"   ❌ {package} 安装失败: {e.stderr}", "red")
            return False
    
    return True

def create_directory_structure(base_path):
    """创建目录结构"""
    print_colored("📁 创建目录结构...", "cyan")
    
    for directory in DIRECTORY_STRUCTURE:
        dir_path = base_path / directory
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print_colored(f"   ✅ 创建目录: {directory}", "green")
        except Exception as e:
            print_colored(f"   ❌ 创建目录失败: {directory} - {e}", "red")
            return False
    
    return True

def download_model(base_path):
    """下载预训练模型"""
    print_colored("🤖 下载语义搜索模型...", "cyan")
    
    model_path = base_path / MODEL_CONFIG["local_path"]
    
    if model_path.exists():
        print_colored(f"   ✅ 模型已存在: {model_path}", "green")
        return True
    
    print_colored(f"   模型名称: {MODEL_CONFIG['name']}", "blue")
    print_colored(f"   来源: {MODEL_CONFIG['source']}", "blue")
    print_colored(f"   下载路径: {MODEL_CONFIG['url']}", "blue")
    
    # 创建模型目录
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 使用sentence-transformers下载（自动处理缓存）
    try:
        print_colored("   正在下载模型（可能需要几分钟，请耐心等待）...", "yellow")
        
        import sys
        sys.path.insert(0, str(base_path))
        
        from sentence_transformers import SentenceTransformer
        
        # 下载模型
        model = SentenceTransformer(MODEL_CONFIG["name"])
        
        # 保存到本地
        model.save(str(model_path))
        
        print_colored(f"   ✅ 模型下载完成: {model_path}", "green")
        print_colored(f"   模型维度: {model.get_sentence_embedding_dimension()}", "blue")
        return True
        
    except ImportError:
        print_colored("   ❌ 无法导入sentence-transformers，请先安装依赖包", "red")
        return False
    except Exception as e:
        print_colored(f"   ❌ 模型下载失败: {e}", "red")
        print_colored("   提示: 可以稍后手动运行 local_memory_system_v2.py 重新下载", "yellow")
        return False

def create_config_files(base_path):
    """创建配置文件"""
    print_colored("⚙️  创建配置文件...", "cyan")
    
    # 创建HEARTBEAT.md
    heartbeat_content = """# HEARTBEAT.md - OpenClaw 定期检查任务清单

**版本**: V2.1  
**最后更新**: {current_date}

---

## 🔄 每日自检 (每日开机时执行，每天1次)

每天开机时自动检查以下项目，每天只触发1次:

```markdown
✅ 每日自检清单

[ ] 检查昨日是否生成会话记录
    ├─ 如果没有 → 根据 session_history 自动补全
    └─ 如果有 → 确认内容是否完整

[ ] 检查是否有待归档的版本日志
    └─ 如果本月已有文件 → 追加记录
    └─ 如果无 → 创建当月文件

[ ] 检查三个记忆库是否需要补充用户评价区
    ├─ TIPS.md → [ ]
    ├─ DAILY_EMOTIONS.md → [ ]
    └─ GOALS.md → [ ]

[ ] 检查是否有到期的目标需要提醒
    └─ 如果有 → 发一条简短消息

[ ] 检查是否有明显的情绪波动未记录
    └─ 如果有 → 在情感记忆库补充条目
```

---

## 🎯 触发关键词列表

当你在对话中使用以下词汇时，我会立即触发对应的记忆库操作:

| 关键词 | 触发动作 | 写入文件 |
|--------|---------|---------|
| "记下来" / "这个要记住" | 添加新目标 | memory/目标记忆库/GOALS.md |
| "记录灵感" / "这个想法不错" | 添加创意 | memory/目标记忆库/IDEAS.md |
| "有问题了" / "报错" / "卡住了" | 记录故障 | memory/经验记忆库/TIPS.md |
| "心情" / "感觉" / "生气了" / "开心" | 记录情绪 | memory/情感记忆库/DAILY_EMOTIONS.md |
| "查看目标" / "今天待办" | 读取目标 | memory/目标记忆库/GOALS.md |
| "上次那个问题怎么解决的" | 搜索经验 | memory/经验记忆库/TIPS.md |
""".format(current_date=time.strftime("%Y-%m-%d"))

    heartbeat_path = base_path / "HEARTBEAT.md"
    heartbeat_path.write_text(heartbeat_content, encoding="utf-8")
    print_colored(f"   ✅ 创建: HEARTBEAT.md", "green")
    
    # 创建MEMORY.md导航文件
    memory_content = """# MEMORY.md - OpenClaw 长期记忆系统总览

_这是 OpenClaw 的记忆系统核心导航文件，指向所有独立的记忆库模块。_

---

## 🧠 记忆系统架构说明

OpenClaw 采用**模块化记忆系统设计**，将不同类型的记忆存储在不同的文件和目录中，便于管理和检索。

### 📁 五大核心记忆库

| # | 记忆库名称 | 存储路径 | 内容类型 | 作用 |
|---|-----------|---------|----------|------|
| 1️⃣ | **目标记忆库** | `memory/目标记忆库/` | GOALS.md | 追踪用户目标（包含已完成/进行中/搁置目标） |
| 2️⃣ | **会话记忆库** | `memory/会话记忆库/` | YYYY-MM-DD.md | 每日会话摘要和上下文 |
| 3️⃣ | **版本记忆库** | `memory/版本记忆库/` | CHANGELOG.md | OpenClaw 升级和变更记录 |
| 4️⃣ | **经验记忆库** | `memory/经验记忆库/` | TIPS.md | 技术难题解决经验和最佳实践 |
| 5️⃣ | **情感记忆库** | `memory/情感记忆库/` | DAILY_EMOTIONS.md | 用户情绪变化和习惯偏好 |

### 💝 心跳回忆系统

| # | 系统名称 | 存储路径 | 内容类型 | 作用 |
|---|---------|---------|----------|------|
| ❤️ | **心跳回忆** | `memory/心跳回忆/` | 心跳回忆机制.md | 仿人类互动，让AI更像人，增强情感连接 |

---

## 🛠️ 快速开始

### 方式一：通过 AI 助手询问

```
用户："查一下今天的待办目标"
→ 我会读取 memory/目标记忆库/GOALS.md

用户："有什么技术经验可以借鉴"
→ 我会读取 memory/经验记忆库/TIPS.md 并总结

用户："我今天的心情怎么样？"
→ 我会分析 memory/情感记忆库/DAILY_EMOTIONS.md
```

### 方式二：直接读取文件

```bash
# 查看今日会话记录
cat memory/会话记忆库/$(date +%Y-%m-%d).md

# 查看当前待办目标
cat memory/目标记忆库/GOALS.md

# 查看经验教训
cat memory/经验记忆库/TIPS.md

# 查看用户情感记录
cat memory/情感记忆库/DAILY_EMOTIONS.md
```

### 方式三：命令行工具

```bash
# 启动交互界面（需 Python 环境）
python3 scripts/local_memory_system_v2.py

# 添加新经验
add_exp "新问题描述" "解决方案详情" --highlight

# 添加新目标
add_goal "新目标" "背景原因" "暂时方案"

# 语义搜索
search "关键词"
```

---

## ⚠️ 重要提醒

### 1. 隐私保护
- 私人数据只存储在本机，不会上传到云端
- 不要在记忆文件中记录密码、API Key 等敏感数据

### 2. 数据安全
- 建议定期备份 memory/ 目录
- 保持足够的磁盘空间（ChromaDB 需要100-300MB内存）

### 3. 操作规范
- 所有记录必须带精确时间戳 (YYYY-MM-DD HH:MM)
- 每条经验/目标都要注明创建时间和触发事件
- 定期清理旧会话记录（建议保留最近3个月）

---

_此导航文件由 HBM Memory System 自动生成，最后更新: {current_date}_  
_记忆系统总设计师：OpenClaw 🤖_
""".format(current_date=time.strftime("%Y-%m-%d"))

    memory_path = base_path / "MEMORY.md"
    memory_path.write_text(memory_content, encoding="utf-8")
    print_colored(f"   ✅ 创建: MEMORY.md", "green")
    
    return True

def verify_installation(base_path):
    """验证安装结果"""
    print_colored("🔍 验证安装结果...", "cyan")
    
    checks = [
        ("HEARTBEAT.md 文件", base_path / "HEARTBEAT.md"),
        ("MEMORY.md 导航文件", base_path / "MEMORY.md"),
        ("脚本文件", base_path / "scripts" / "local_memory_system_v2.py"),
        ("记忆库目录", base_path / "memory" / "目标记忆库"),
    ]
    
    all_passed = True
    for check_name, check_path in checks:
        if check_path.exists():
            print_colored(f"   ✅ {check_name} 存在", "green")
        else:
            print_colored(f"   ❌ {check_name} 不存在", "red")
            all_passed = False
    
    # 检查Python包
    try:
        import chromadb
        import pandas as np
        import sentence_transformers
        print_colored("   ✅ Python依赖包检查通过", "green")
    except ImportError as e:
        print_colored(f"   ❌ Python依赖包缺失: {e}", "red")
        all_passed = False
    
    return all_passed

def main():
    """主安装函数"""
    print_colored("=" * 60, "magenta")
    print_colored("🚀 HBM Memory System 一键安装程序", "magenta")
    print_colored("=" * 60, "magenta")
    print_colored(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", "cyan")
    
    # 获取安装目录（当前目录）
    install_dir = Path.cwd()
    print_colored(f"安装目录: {install_dir}", "cyan")
    
    # 检查步骤
    if not check_python_version():
        return False
    
    system = check_platform()
    
    # 安装Python包
    if not install_packages():
        return False
    
    # 创建目录结构
    if not create_directory_structure(install_dir):
        return False
    
    # 下载模型
    if not download_model(install_dir):
        print_colored("⚠️  模型下载失败，但安装继续...", "yellow")
    
    # 创建配置文件
    if not create_config_files(install_dir):
        return False
    
    # 验证安装
    if not verify_installation(install_dir):
        print_colored("⚠️  部分验证失败，但安装基本完成", "yellow")
    else:
        print_colored("✅ 安装验证通过", "green")
    
    # 完成提示
    print_colored("=" * 60, "magenta")
    print_colored("🎉 HBM Memory System 安装完成！", "magenta")
    print_colored("=" * 60, "magenta")
    
    print_colored("\n📚 使用指南:", "cyan")
    print_colored("1. 查看系统导航: cat MEMORY.md", "white")
    print_colored("2. 查看心跳检查任务: cat HEARTBEAT.md", "white")
    print_colored("3. 启动记忆系统交互界面: python3 scripts/local_memory_system_v2.py", "white")
    
    print_colored("\n🔧 快速测试:", "cyan")
    print_colored("   python3 scripts/local_memory_system_v2.py", "white")
    print_colored("   add_exp \"测试问题\" \"测试解决方案\" --highlight", "white")
    print_colored("   search \"记忆\"", "white")
    
    print_colored("\n📞 获取帮助:", "cyan")
    print_colored("   查看SKILL.md获取完整使用说明", "white")
    print_colored("   访问ClawHub技能页面查看最新更新", "white")
    
    print_colored(f"\n⏱️  安装耗时: {time.strftime('%Y-%m-%d %H:%M:%S')}", "cyan")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print_colored("\n❌ 安装被用户中断", "red")
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ 安装过程中发生未知错误: {e}", "red")
        sys.exit(1)
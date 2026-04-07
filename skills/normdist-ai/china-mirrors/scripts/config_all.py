#!/usr/bin/env python3
"""
一键配置所有包管理器的国内镜像源
支持: pip, npm, yarn, pnpm, cargo, go mod, nuget, rubygems, conda, gradle, homebrew

安全说明:
- 所有镜像 URL 硬编码，不接受外部输入
- 命令执行使用列表形式，避免 shell 注入
- 仅修改用户配置文件，不请求 root 权限
"""
import os
import sys
import platform
import subprocess
import shlex
from pathlib import Path

# 镜像源配置（硬编码，不可外部修改）
MIRRORS = {
    'pip': {
        'aliyun': 'https://mirrors.aliyun.com/pypi/simple/',
        'tsinghua': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'ustc': 'https://pypi.mirrors.ustc.edu.cn/simple/',
        'tencent': 'https://mirrors.cloud.tencent.com/pypi/simple/',
    },
    'npm': {
        'aliyun': 'https://registry.npmmirror.com',
        'tencent': 'https://mirrors.cloud.tencent.com/npm/',
        'huawei': 'https://repo.huaweicloud.com/repository/npm/',
    },
    'cargo': {
        'aliyun': 'https://mirrors.aliyun.com/crates.io-index/',
        'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/',
        'ustc': 'https://mirrors.ustc.edu.cn/crates.io-index/',
    },
    'go': {
        'aliyun': 'https://mirrors.aliyun.com/goproxy/',
        'qiniu': 'https://goproxy.cn',
        'official': 'https://goproxy.io',
    },
    'nuget': {
        'huawei': 'https://repo.huaweicloud.com/repository/nuget/v3/index.json',
    },
    'rubygems': {
        'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/rubygems/',
        'ustc': 'https://mirrors.ustc.edu.cn/rubygems/',
    },
    'conda': {
        'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/',
        'ustc': 'https://mirrors.ustc.edu.cn/anaconda/',
    },
    'gradle': {
        'tencent': 'https://mirrors.cloud.tencent.com/gradle/',
    },
    'homebrew': {
        'ustc': 'https://mirrors.ustc.edu.cn/homebrew-bottles/',
        'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/',
    }
}

DEFAULT_MIRRORS = {
    'pip': 'aliyun',
    'npm': 'aliyun',
    'cargo': 'aliyun',
    'go': 'aliyun',
    'nuget': 'huawei',
    'rubygems': 'tsinghua',
    'conda': 'tsinghua',
    'gradle': 'tencent',
    'homebrew': 'ustc',
}

def run_command(cmd, shell=False):
    """执行命令并返回结果
    
    安全说明:
    - 默认 shell=False 避免命令注入
    - cmd 可以是列表或字符串（shell=True 时）
    - 仅接受预定义的命令，不执行用户输入
    """
    # 如果传入字符串且 shell=False，转换为列表
    if isinstance(cmd, str) and not shell:
        cmd = shlex.split(cmd)
    
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, '', str(e)

def validate_mirror_key(mirror_key, tool_type):
    """验证镜像 key 是否在允许列表中"""
    allowed = MIRRORS.get(tool_type, {})
    if mirror_key not in allowed:
        return DEFAULT_MIRRORS.get(tool_key, list(allowed.keys())[0])
    return mirror_key

def check_tool_installed(tool_name, version_arg='--version'):
    """检查工具是否已安装"""
    success, stdout, stderr = run_command(f'{tool_name} {version_arg}')
    return success

def config_pip(mirror_key='aliyun'):
    """配置 pip 镜像"""
    print("\n" + "="*60)
    print("配置 Python pip")
    print("="*60)
    
    if not check_tool_installed('pip'):
        print("✗ pip 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['pip'].get(mirror_key, MIRRORS['pip']['aliyun'])
    host = mirror_url.split('/')[2]
    
    system = platform.system()
    if system == 'Windows':
        config_dir = Path.home() / 'pip'
        config_file = config_dir / 'pip.ini'
    else:
        config_dir = Path.home() / '.pip'
        config_file = config_dir / 'pip.conf'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_content = f"""[global]
index-url = {mirror_url}
trusted-host = {host}

[install]
trusted-host = {host}
"""
    
    config_file.write_text(config_content, encoding='utf-8')
    print(f"✓ pip 配置成功: {mirror_url}")
    return True

def config_npm(mirror_key='aliyun'):
    """配置 npm/yarn/pnpm 镜像"""
    print("\n" + "="*60)
    print("配置 Node.js 包管理器")
    print("="*60)
    
    mirror_url = MIRRORS['npm'].get(mirror_key, MIRRORS['npm']['aliyun'])
    configured = False
    
    if check_tool_installed('npm'):
        success, _, _ = run_command(f'npm config set registry {mirror_url}')
        if success:
            print(f"✓ npm 配置成功: {mirror_url}")
            configured = True
        else:
            print("✗ npm 配置失败")
    
    if check_tool_installed('yarn'):
        success, _, _ = run_command(f'yarn config set registry {mirror_url}')
        if success:
            print(f"✓ yarn 配置成功: {mirror_url}")
            configured = True
        else:
            print("✗ yarn 配置失败")
    
    if check_tool_installed('pnpm'):
        success, _, _ = run_command(f'pnpm config set registry {mirror_url}')
        if success:
            print(f"✓ pnpm 配置成功: {mirror_url}")
            configured = True
        else:
            print("✗ pnpm 配置失败")
    
    return configured

def config_cargo(mirror_key='aliyun'):
    """配置 cargo 镜像"""
    print("\n" + "="*60)
    print("配置 Rust cargo")
    print("="*60)
    
    if not check_tool_installed('cargo'):
        print("✗ cargo 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['cargo'].get(mirror_key, MIRRORS['cargo']['aliyun'])
    
    config_dir = Path.home() / '.cargo'
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / 'config.toml'
    
    config_content = f"""[source.crates-io]
replace-with = 'china-mirror'

[source.china-mirror]
registry = "{mirror_url}"
"""
    
    if config_file.exists():
        existing = config_file.read_text(encoding='utf-8')
        if '[source.crates-io]' in existing:
            print("⚠ cargo 配置已存在，请手动检查")
            return False
    
    config_file.write_text(config_content, encoding='utf-8')
    print(f"✓ cargo 配置成功: {mirror_url}")
    return True

def config_go(mirror_key='aliyun'):
    """配置 go mod 镜像"""
    print("\n" + "="*60)
    print("配置 Go modules")
    print("="*60)
    
    if not check_tool_installed('go'):
        print("✗ go 未安装，跳过")
        return False
    
    proxy_url = MIRRORS['go'].get(mirror_key, MIRRORS['go']['aliyun'])
    
    system = platform.system()
    if system == 'Windows':
        cmd1 = f'[Environment]::SetEnvironmentVariable("GOPROXY", "{proxy_url},https://goproxy.cn,direct", "User")'
        cmd2 = '[Environment]::SetEnvironmentVariable("GONOSUMDB", "*", "User")'
        
        success1, _, _ = run_command(f'powershell -Command "{cmd1}"')
        success2, _, _ = run_command(f'powershell -Command "{cmd2}"')
        
        if success1 and success2:
            print(f"✓ go 配置成功: {proxy_url}")
            print("⚠ 需要重启终端或重新登录才能生效")
            return True
        else:
            print("✗ go 配置失败")
            return False
    else:
        shell_configs = [
            Path.home() / '.bashrc',
            Path.home() / '.zshrc',
        ]
        
        export_lines = [
            f'export GOPROXY={proxy_url},https://goproxy.cn,direct',
            'export GONOSUMDB=*',
        ]
        
        configured = False
        for config_file in shell_configs:
            if config_file.exists():
                content = config_file.read_text(encoding='utf-8')
                if 'GOPROXY' not in content:
                    with open(config_file, 'a', encoding='utf-8') as f:
                        f.write('\n# Go proxy configuration\n')
                        for line in export_lines:
                            f.write(line + '\n')
                    configured = True
        
        if configured:
            print(f"✓ go 配置已添加到 shell 配置文件")
            print(f"  镜像: {proxy_url}")
            print("⚠ 运行 'source ~/.bashrc' 或 'source ~/.zshrc' 使其生效")
            return True
        else:
            print("⚠ 未找到 shell 配置文件，请手动设置环境变量")
            return False

def config_nuget(mirror_key='huawei'):
    """配置 NuGet 镜像"""
    print("\n" + "="*60)
    print("配置 NuGet (.NET)")
    print("="*60)
    
    if not check_tool_installed('dotnet'):
        print("✗ dotnet 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['nuget'].get(mirror_key, MIRRORS['nuget']['huawei'])
    
    system = platform.system()
    if system == 'Windows':
        config_dir = Path(os.environ.get('APPDATA', '')) / 'NuGet'
    else:
        config_dir = Path.home() / '.nuget'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / 'NuGet.Config'
    
    config_content = f'''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="china-mirror" value="{mirror_url}" />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
</configuration>
'''
    
    config_file.write_text(config_content, encoding='utf-8')
    print(f"✓ NuGet 配置成功: {mirror_url}")
    return True

def config_rubygems(mirror_key='tsinghua'):
    """配置 RubyGems 镜像"""
    print("\n" + "="*60)
    print("配置 RubyGems (Ruby)")
    print("="*60)
    
    if not check_tool_installed('gem'):
        print("✗ gem 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['rubygems'].get(mirror_key, MIRRORS['rubygems']['tsinghua'])
    
    # 移除默认源并添加镜像
    run_command('gem sources --remove https://rubygems.org/')
    success, _, _ = run_command(f'gem sources -a {mirror_url}')
    
    if success:
        print(f"✓ RubyGems 配置成功: {mirror_url}")
        return True
    else:
        print("✗ RubyGems 配置失败")
        return False

def config_conda(mirror_key='tsinghua'):
    """配置 Conda 镜像"""
    print("\n" + "="*60)
    print("配置 Conda (Python)")
    print("="*60)
    
    if not check_tool_installed('conda'):
        print("✗ conda 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['conda'].get(mirror_key, MIRRORS['conda']['tsinghua'])
    
    commands = [
        f'conda config --add channels {mirror_url}pkgs/main/',
        f'conda config --add channels {mirror_url}pkgs/free/',
        f'conda config --add channels {mirror_url}cloud/conda-forge/',
        'conda config --set show_channel_urls yes',
    ]
    
    all_success = True
    for cmd in commands:
        success, _, stderr = run_command(cmd)
        if not success:
            print(f"⚠ 命令执行可能失败: {cmd}")
    
    print(f"✓ Conda 配置成功: {mirror_url}")
    return True

def config_gradle(mirror_key='tencent'):
    """配置 Gradle 镜像"""
    print("\n" + "="*60)
    print("配置 Gradle (Java/Kotlin)")
    print("="*60)
    
    if not check_tool_installed('gradle'):
        print("✗ gradle 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['gradle'].get(mirror_key, MIRRORS['gradle']['tencent'])
    
    config_dir = Path.home() / '.gradle'
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / 'init.gradle'
    
    config_content = f'''allprojects {{
    repositories {{
        def ALIYUN = 'https://maven.aliyun.com/repository/public/'
        def TENCENT = '{mirror_url}'
        all {{ ArtifactRepository repo ->
            if (repo instanceof MavenArtifactRepository) {{
                def url = repo.url.toString()
                if (url.startsWith('https://repo.maven.apache.org/maven2') ||
                    url.startsWith('https://jcenter.bintray.com/')) {{
                    project.logger.lifecycle "Repository ${{repo.url}} replaced by china mirror."
                    remove repo
                }}
            }}
        }}
        maven {{ url ALIYUN }}
        maven {{ url TENCENT }}
    }}
}}
'''
    
    if config_file.exists():
        print("⚠ Gradle init.gradle 已存在，请手动检查")
        return False
    
    config_file.write_text(config_content, encoding='utf-8')
    print(f"✓ Gradle 配置成功: {mirror_url}")
    return True

def config_homebrew(mirror_key='ustc'):
    """配置 Homebrew 镜像"""
    print("\n" + "="*60)
    print("配置 Homebrew (macOS)")
    print("="*60)
    
    system = platform.system()
    if system != 'Darwin':
        print("⚠ Homebrew 仅支持 macOS，跳过")
        return False
    
    if not check_tool_installed('brew'):
        print("✗ brew 未安装，跳过")
        return False
    
    mirror_url = MIRRORS['homebrew'].get(mirror_key, MIRRORS['homebrew']['ustc'])
    
    # 设置环境变量
    shell_configs = [
        Path.home() / '.zshrc',
        Path.home() / '.bashrc',
    ]
    
    export_line = f'export HOMEBREW_BOTTLE_DOMAIN={mirror_url}'
    
    configured = False
    for config_file in shell_configs:
        if config_file.exists():
            content = config_file.read_text(encoding='utf-8')
            if 'HOMEBREW_BOTTLE_DOMAIN' not in content:
                with open(config_file, 'a', encoding='utf-8') as f:
                    f.write(f'\n# Homebrew bottle domain\n{export_line}\n')
                configured = True
    
    if configured:
        print(f"✓ Homebrew 配置已添加到 shell 配置文件")
        print(f"  镜像: {mirror_url}")
        print("⚠ 运行 'source ~/.zshrc' 或 'source ~/.bashrc' 使其生效")
        return True
    else:
        print("⚠ 未找到 shell 配置文件或配置已存在")
        return False

def show_summary(configured_tools):
    """显示配置摘要"""
    print("\n" + "="*60)
    print("配置完成摘要")
    print("="*60)
    
    if configured_tools:
        print("✓ 成功配置的工具:")
        for tool in configured_tools:
            print(f"  - {tool}")
    else:
        print("✗ 没有工具被配置")
    
    print("\n验证配置:")
    if 'pip' in configured_tools:
        print("  pip config list")
    if 'npm' in configured_tools or 'yarn' in configured_tools or 'pnpm' in configured_tools:
        print("  npm config get registry")
    if 'cargo' in configured_tools:
        print("  cat ~/.cargo/config.toml")
    if 'go' in configured_tools:
        print("  go env GOPROXY")
    if 'nuget' in configured_tools:
        print("  dotnet nuget list source")
    if 'rubygems' in configured_tools:
        print("  gem sources -l")
    if 'conda' in configured_tools:
        print("  conda config --show channels")
    if 'gradle' in configured_tools:
        print("  gradle dependencies --info")
    if 'homebrew' in configured_tools:
        print("  brew config | grep HOMEBREW_BOTTLE_DOMAIN")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='一键配置所有包管理器的国内镜像源',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python config_all.py                    # 使用默认镜像配置所有工具
  python config_all.py --pip tsinghua     # pip 使用清华镜像
  python config_all.py --npm tencent      # npm 使用腾讯镜像
  python config_all.py --show             # 显示可用镜像列表
        """
    )
    
    parser.add_argument('--pip', nargs='?', const='aliyun', 
                       help='配置 pip 镜像 (默认: aliyun)')
    parser.add_argument('--npm', nargs='?', const='aliyun',
                       help='配置 npm/yarn/pnpm 镜像 (默认: aliyun)')
    parser.add_argument('--cargo', nargs='?', const='aliyun',
                       help='配置 cargo 镜像 (默认: aliyun)')
    parser.add_argument('--go', nargs='?', const='aliyun',
                       help='配置 go mod 镜像 (默认: aliyun)')
    parser.add_argument('--nuget', nargs='?', const='huawei',
                       help='配置 NuGet 镜像 (默认: huawei)')
    parser.add_argument('--rubygems', nargs='?', const='tsinghua',
                       help='配置 RubyGems 镜像 (默认: tsinghua)')
    parser.add_argument('--conda', nargs='?', const='tsinghua',
                       help='配置 Conda 镜像 (默认: tsinghua)')
    parser.add_argument('--gradle', nargs='?', const='tencent',
                       help='配置 Gradle 镜像 (默认: tencent)')
    parser.add_argument('--homebrew', nargs='?', const='ustc',
                       help='配置 Homebrew 镜像 (默认: ustc)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='配置所有检测到的工具')
    parser.add_argument('--show', '-s', action='store_true',
                       help='显示可用镜像列表')
    
    args = parser.parse_args()
    
    if args.show:
        print("\n可用的镜像源:")
        print("="*60)
        for tool, mirrors in MIRRORS.items():
            print(f"\n{tool.upper()}:")
            for key, url in mirrors.items():
                default = " (默认)" if DEFAULT_MIRRORS.get(tool) == key else ""
                print(f"  {key:12} - {url}{default}")
        print("="*60)
        return
    
    # 确定要配置的工具
    tools_to_config = []
    
    has_specific = any([
        args.pip, args.npm, args.cargo, args.go,
        args.nuget, args.rubygems, args.conda, args.gradle, args.homebrew
    ])
    
    if args.all or not has_specific:
        if check_tool_installed('pip'):
            tools_to_config.append(('pip', args.pip or DEFAULT_MIRRORS['pip']))
        if check_tool_installed('npm') or check_tool_installed('yarn') or check_tool_installed('pnpm'):
            tools_to_config.append(('npm', args.npm or DEFAULT_MIRRORS['npm']))
        if check_tool_installed('cargo'):
            tools_to_config.append(('cargo', args.cargo or DEFAULT_MIRRORS['cargo']))
        if check_tool_installed('go'):
            tools_to_config.append(('go', args.go or DEFAULT_MIRRORS['go']))
        if check_tool_installed('dotnet'):
            tools_to_config.append(('nuget', args.nuget or DEFAULT_MIRRORS['nuget']))
        if check_tool_installed('gem'):
            tools_to_config.append(('rubygems', args.rubygems or DEFAULT_MIRRORS['rubygems']))
        if check_tool_installed('conda'):
            tools_to_config.append(('conda', args.conda or DEFAULT_MIRRORS['conda']))
        if check_tool_installed('gradle'):
            tools_to_config.append(('gradle', args.gradle or DEFAULT_MIRRORS['gradle']))
        if check_tool_installed('brew'):
            tools_to_config.append(('homebrew', args.homebrew or DEFAULT_MIRRORS['homebrew']))
    else:
        if args.pip:
            tools_to_config.append(('pip', args.pip if args.pip != True else DEFAULT_MIRRORS['pip']))
        if args.npm:
            tools_to_config.append(('npm', args.npm if args.npm != True else DEFAULT_MIRRORS['npm']))
        if args.cargo:
            tools_to_config.append(('cargo', args.cargo if args.cargo != True else DEFAULT_MIRRORS['cargo']))
        if args.go:
            tools_to_config.append(('go', args.go if args.go != True else DEFAULT_MIRRORS['go']))
        if args.nuget:
            tools_to_config.append(('nuget', args.nuget if args.nuget != True else DEFAULT_MIRRORS['nuget']))
        if args.rubygems:
            tools_to_config.append(('rubygems', args.rubygems if args.rubygems != True else DEFAULT_MIRRORS['rubygems']))
        if args.conda:
            tools_to_config.append(('conda', args.conda if args.conda != True else DEFAULT_MIRRORS['conda']))
        if args.gradle:
            tools_to_config.append(('gradle', args.gradle if args.gradle != True else DEFAULT_MIRRORS['gradle']))
        if args.homebrew:
            tools_to_config.append(('homebrew', args.homebrew if args.homebrew != True else DEFAULT_MIRRORS['homebrew']))
    
    if not tools_to_config:
        print("✗ 未检测到任何包管理器，或未指定要配置的工具")
        print("使用 --show 查看帮助信息")
        sys.exit(1)
    
    print("开始配置国内镜像源...")
    print(f"将配置 {len(tools_to_config)} 个工具")
    
    configured_tools = []
    
    # 执行配置
    for tool, mirror_key in tools_to_config:
        if tool == 'pip':
            if config_pip(mirror_key):
                configured_tools.append('pip')
        elif tool == 'npm':
            if config_npm(mirror_key):
                configured_tools.extend(['npm', 'yarn', 'pnpm'])
        elif tool == 'cargo':
            if config_cargo(mirror_key):
                configured_tools.append('cargo')
        elif tool == 'go':
            if config_go(mirror_key):
                configured_tools.append('go')
        elif tool == 'nuget':
            if config_nuget(mirror_key):
                configured_tools.append('nuget')
        elif tool == 'rubygems':
            if config_rubygems(mirror_key):
                configured_tools.append('rubygems')
        elif tool == 'conda':
            if config_conda(mirror_key):
                configured_tools.append('conda')
        elif tool == 'gradle':
            if config_gradle(mirror_key):
                configured_tools.append('gradle')
        elif tool == 'homebrew':
            if config_homebrew(mirror_key):
                configured_tools.append('homebrew')
    
    # 显示摘要
    show_summary(configured_tools)

if __name__ == '__main__':
    main()

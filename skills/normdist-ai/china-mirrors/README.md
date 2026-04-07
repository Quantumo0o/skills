# 中国国内镜像源配置技能

自动配置各种包管理器的国内镜像源，解决中国大陆开发者依赖下载缓慢的问题。

## 功能特性

- ✅ 支持多种包管理器：pip、npm、yarn、pnpm、cargo、go mod、NuGet、RubyGems、Conda、Gradle、Homebrew
- ✅ 自动检测已安装的工具
- ✅ 提供多个主流镜像源选择
- ✅ 支持全局和项目级配置
- ✅ 跨平台支持（Windows、Linux、Mac）
- ✅ 提供自动化配置脚本

## 快速开始

### 方法 1: 使用综合配置脚本（推荐）

一键配置所有检测到的包管理器：

```bash
# 进入技能目录
cd <skill-directory>

# 运行综合配置脚本
python scripts/config_all.py --all
```

自定义配置特定工具：

```bash
# 仅配置 pip，使用清华大学镜像
python scripts/config_all.py --pip tsinghua

# 配置 npm 和 cargo
python scripts/config_all.py --npm aliyun --cargo tsinghua

# 查看所有可用镜像
python scripts/config_all.py --show
```

### 方法 2: 使用独立配置脚本

**配置 pip:**
```bash
python scripts/config_pip.py aliyun      # 阿里云（默认）
python scripts/config_pip.py tsinghua    # 清华大学
python scripts/config_pip.py --list      # 列出所有镜像
python scripts/config_pip.py --show      # 显示当前配置
```

**配置 npm/yarn/pnpm:**
```bash
node scripts/config_npm.js               # 使用默认镜像配置所有检测到的工具
node scripts/config_npm.js npm           # 仅配置 npm
node scripts/config_npm.js --list        # 列出所有镜像
node scripts/config_npm.js --show        # 显示当前配置
```

### 方法 3: 手动配置

参考 [SKILL.md](SKILL.md) 中的详细配置指南，手动执行配置命令。

## 支持的镜像源

### Python (pip)
- **阿里云**: https://mirrors.aliyun.com/pypi/simple/ ⭐ 推荐
- **清华大学**: https://pypi.tuna.tsinghua.edu.cn/simple/
- **中科大**: https://pypi.mirrors.ustc.edu.cn/simple/
- **腾讯云**: https://mirrors.cloud.tencent.com/pypi/simple/

### Node.js (npm/yarn/pnpm)
- **阿里云**: https://registry.npmmirror.com ⭐ 推荐
- **腾讯云**: https://mirrors.cloud.tencent.com/npm/
- **华为云**: https://repo.huaweicloud.com/repository/npm/

### Rust (cargo)
- **清华大学**: https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/ ⭐ 推荐
- **中科大**: https://mirrors.ustc.edu.cn/crates.io-index/
- **阿里云**: https://mirrors.aliyun.com/crates.io-index/

### Go (go mod)
- **阿里云**: https://mirrors.aliyun.com/goproxy/ ⭐ 推荐
- **七牛云**: https://goproxy.cn
- **官方中国**: https://goproxy.io

### NuGet (.NET)
- **华为云**: https://repo.huaweicloud.com/repository/nuget/v3/index.json ⭐ 推荐

### RubyGems (Ruby)
- **清华大学**: https://mirrors.tuna.tsinghua.edu.cn/rubygems/ ⭐ 推荐
- **中科大**: https://mirrors.ustc.edu.cn/rubygems/

### Conda (Python)
- **清华大学**: https://mirrors.tuna.tsinghua.edu.cn/anaconda/ ⭐ 推荐
- **中科大**: https://mirrors.ustc.edu.cn/anaconda/

### Gradle (Java/Kotlin)
- **腾讯云**: https://mirrors.cloud.tencent.com/gradle/ ⭐ 推荐

### Homebrew (macOS)
- **中科大**: https://mirrors.ustc.edu.cn/homebrew-bottles/ ⭐ 推荐
- **清华大学**: https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/

## 使用示例

### 场景 1: 新项目初始化

```bash
# 克隆项目后，一键配置所有镜像
python <skill-directory>/scripts/config_all.py --all

# 然后正常安装依赖
pip install -r requirements.txt
npm install
```

### 场景 2: 团队协作

在项目根目录创建配置文件，团队成员共享配置：

**.npmrc** (Node.js 项目):
```ini
registry=https://registry.npmmirror.com
```

**pip.conf** (Python 项目):
```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
```

将配置文件加入版本控制，团队成员自动使用相同镜像。

### 场景 3: CI/CD 环境

在 CI 配置文件中显式指定镜像：

**.github/workflows/ci.yml**:
```yaml
- name: Configure pip mirror
  run: |
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

- name: Configure npm mirror
  run: |
    npm config set registry https://registry.npmmirror.com
```

## 验证配置

配置完成后，验证是否生效：

```bash
# pip
pip config list

# npm
npm config get registry

# yarn
yarn config get registry

# cargo
cat ~/.cargo/config.toml

# go
go env GOPROXY

# nuget
dotnet nuget list source

# rubygems
gem sources -l

# conda
conda config --show channels

# gradle
gradle dependencies --info

# homebrew
brew config | grep HOMEBREW_BOTTLE_DOMAIN
```

测试安装速度：

```bash
# pip
pip install requests

# npm
npm install lodash

# cargo
cargo search serde

# go
go get github.com/gin-gonic/gin
```

## 故障排查

### 问题 1: 配置后仍然很慢

**可能原因**: 缓存未清除或配置未生效

**解决方法**:
```bash
# 清除 pip 缓存
pip cache purge

# 清除 npm 缓存
npm cache clean --force

# 重启终端使环境变量生效（go）
source ~/.bashrc  # 或 ~/.zshrc
```

### 问题 2: SSL 证书错误

**解决方法**:
```bash
# npm 临时禁用严格 SSL（不推荐长期使用）
npm config set strict-ssl false

# 或使用 HTTPS 而非 HTTP 的镜像源
```

### 问题 3: 某些包无法找到

**可能原因**: 镜像同步延迟

**解决方法**:
```bash
# 临时使用官方源安装特定包
pip install -i https://pypi.org/simple/ package_name
npm install --registry=https://registry.npmjs.org package_name
```

### 问题 4: Windows 下 go 配置不生效

**解决方法**:
1. 通过系统环境变量设置界面手动添加 `GOPROXY`
2. 或重启计算机使环境变量生效
3. 验证: `go env GOPROXY`

## 恢复默认配置

### pip
```bash
# 删除配置文件
rm ~/.pip/pip.conf          # Linux/Mac
del %USERPROFILE%\pip\pip.ini  # Windows
```

### npm
```bash
npm config delete registry
```

### cargo
编辑 `~/.cargo/config.toml`，注释或删除镜像配置

### go
```bash
# Linux/Mac
unset GOPROXY

# Windows
# 通过系统环境变量设置界面删除 GOPROXY
```

### nuget
```bash
rm ~/.nuget/NuGet.Config          # Linux/Mac
del %APPDATA%\NuGet\NuGet.Config  # Windows
```

### rubygems
```bash
gem sources --remove https://mirrors.tuna.tsinghua.edu.cn/rubygems/
gem sources -a https://rubygems.org/
```

### conda
```bash
conda config --remove-key channels
```

### gradle
# 删除 ~/.gradle/init.gradle 或修改 build.gradle 恢复默认仓库

### homebrew
```bash
unset HOMEBREW_BOTTLE_DOMAIN
cd "$(brew --repo homebrew/core)" && git remote set-url origin https://github.com/Homebrew/homebrew-core.git
cd "$(brew --repo homebrew/cask)" && git remote set-url origin https://github.com/Homebrew/homebrew-cask.git
```

## 最佳实践

1. **优先选择阿里云或清华大学镜像**：稳定性好，更新及时
2. **团队项目使用项目级配置**：确保所有成员使用相同镜像
3. **CI/CD 中显式指定镜像**：避免依赖环境配置
4. **定期检查镜像可用性**：某些镜像可能暂时不可用
5. **保留回退方案**：知道如何切换到其他镜像或官方源

## 相关资源

- [PyPI 镜像列表](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)
- [npm 镜像状态](https://npmmirror.com/)
- [crates.io 镜像](https://mirrors.tuna.tsinghua.edu.cn/help/crates.io-index/)
- [Go Proxy 中国](https://goproxy.cn/)
- [Maven 阿里云镜像](https://maven.aliyun.com/mvn/guide)

## 平台兼容性

### 不同平台的技能目录结构

本技能可以在不同平台的标准技能目录中使用：

| 平台 | 技能目录 | 示例路径 |
|------|---------|----------|
| Lingma | `.lingma/skills/` | `.lingma/skills/china-mirrors/` |
| Trae IDE | `.trae/skills/` | `.trae/skills/china-mirrors/` |
| 通用 | `skills/` | `skills/china-mirrors/` |

### 使用方法

1. **在技能目录中运行**：
   ```bash
   cd <skill-directory>
   python scripts/config_all.py --all
   ```

2. **从项目根目录运行**：
   ```bash
   python <skill-directory>/scripts/config_all.py --all
   ```

3. **平台无关性**：
   - 脚本本身不依赖于特定的目录结构
   - 可以在任何位置运行，只要能找到脚本文件
   - 配置结果是全局的，对系统生效

## 许可证

本技能遵循与主项目相同的许可证。
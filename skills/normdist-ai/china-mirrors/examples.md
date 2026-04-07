# 使用示例

展示如何使用 china-mirrors 技能的各种场景：

## 示例 1: Python 项目配置

### 用户请求
```
我刚创建了一个 Python 项目，安装依赖特别慢，能帮我配置一下吗？
```

### Agent 响应
我会帮您配置 pip 使用国内镜像源。让我先检测您的环境，然后配置阿里云镜像（速度快且稳定）：

**执行配置：**
```bash
python <skill-directory>/scripts/config_pip.py aliyun
```

**输出：**
```
✅ pip 全局配置已保存到: C:\Users\YourName\pip\pip.ini
✅ 使用镜像: 阿里云 (https://mirrors.aliyun.com/pypi/simple/)

验证配置:
运行以下命令测试:
  pip install --verbose requests 2>&1 | grep -i 'aliyun'
```

**验证：**
```bash
pip config list
```

现在您可以快速安装依赖了：
```bash
pip install -r requirements.txt
```

---

## 示例 2: Node.js 全栈项目

### 用户请求
```
这个前端项目 npm install 要等好久，有没有加速方法？
```

### Agent 响应
我来帮您配置 npm 使用国内镜像。检测到您使用的是 npm，我将配置阿里云镜像源：

**执行配置：**
```bash
node <skill-directory>/scripts/config_npm.js npm
```

**输出：**
```
检测到包管理器: npm

正在配置 npm...
✅ npm 配置成功
  镜像: 阿里云
  URL: https://registry.npmmirror.com

验证配置:
运行以下命令测试:
  npm config get registry
```

**验证：**
```bash
npm config get registry
# 应输出 https://registry.npmmirror.com
```

现在重新安装依赖：
```bash
npm install
```

速度应该提升很多！🚀

---

## 示例 3: 多语言项目一键配置

### 用户请求
```
我的项目用了 Python、Node.js 和 Rust，能不能一次性把所有包管理器都配置好？
```

### Agent 响应
当然可以！我有一键配置脚本，可以自动检测并配置所有已安装的包管理器：

**执行配置：**
```bash
python <skill-directory>/scripts/config_all.py --all
```

**输出：**
```
开始配置国内镜像源...
将配置 3 个工具

============================================================
配置 Python pip
============================================================
✅ pip 配置成功: https://mirrors.aliyun.com/pypi/simple/

============================================================
配置 Node.js 包管理器
============================================================
✅ npm 配置成功: https://registry.npmmirror.com
✅ yarn 配置成功: https://registry.npmmirror.com

============================================================
配置 Rust cargo
============================================================
✅ cargo 配置成功: https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/

============================================================
配置完成摘要
============================================================
✅ 成功配置的工具
  - pip
  - npm
  - yarn
  - cargo

验证配置:
  pip config list
  npm config get registry
  cat ~/.cargo/config.toml
```

所有包管理器都已配置完成！现在您可以快速安装所有依赖了。

---

## 示例 4: Go 项目配置

### 用户请求
```
go mod download 总是超时，怎么解决？
```

### Agent 响应
这是中国大陆开发者常见的问题。我来帮您配置 Go module 代理：

**Windows 系统：**
```bash
python <skill-directory>/scripts/config_all.py --go qiniu
```

**输出：**
```
============================================================
配置 Go modules
============================================================
✅ go 配置成功: https://goproxy.cn
✅ 需要重启终端或重新登录才能生效
```

**Linux/Mac 系统：**
配置会自动添加到 `~/.bashrc` 或 `~/.zshrc`，需要执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

**验证：**
```bash
go env GOPROXY
# 应输出 https://goproxy.cn,direct
```

现在可以正常下载依赖了：
```bash
go mod download
go get github.com/gin-gonic/gin
```

---

## 示例 5: 查看可用镜像

### 用户请求
```
有哪些国内镜像源可以选择？我想了解一下各个镜像的特点。
```

### Agent 响应
让我为您列出所有可用的镜像源：

**查看所有镜像：**
```bash
python <skill-directory>/scripts/config_all.py --show
```

**输出：**
```
可用的镜像源:
============================================================

PIP:
  aliyun       - https://mirrors.aliyun.com/pypi/simple/ (默认)
  tsinghua     - https://pypi.tuna.tsinghua.edu.cn/simple/
  ustc         - https://pypi.mirrors.ustc.edu.cn/simple/
  tencent      - https://mirrors.cloud.tencent.com/pypi/simple/

NPM:
  aliyun       - https://registry.npmmirror.com (默认)
  tencent      - https://mirrors.cloud.tencent.com/npm/
  huawei       - https://repo.huaweicloud.com/repository/npm/

CARGO:
  tsinghua     - https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/ (默认)
  ustc         - https://mirrors.ustc.edu.cn/crates.io-index/
  aliyun       - https://mirrors.aliyun.com/crates.io-index/

GO:
  qiniu        - https://goproxy.cn (默认)
  aliyun       - https://mirrors.aliyun.com/goproxy/
  official     - https://goproxy.io
============================================================
```

**推荐选择：**
- **Python**: 阿里云（稳定）或清华大学（更新快）
- **Node.js**: 阿里云 npmmirror（最流行）
- **Rust**: 清华大学（同步及时）
- **Go**: 七牛云 goproxy.cn（专为国内优化）

---

## 示例 6: 项目级配置（团队协作）

### 用户请求
```
我们团队想统一使用相同的镜像配置，应该怎么设置？
```

### Agent 响应
对于团队协作，建议使用项目级配置，将配置文件纳入版本控制：

**Python 项目：**
在项目根目录创建 `pip.conf`：
```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com

[install]
trusted-host = mirrors.aliyun.com
```

或使用脚本：
```bash
python <skill-directory>/scripts/config_pip.py aliyun --project
```

**Node.js 项目：**
在项目根目录创建 `.npmrc`：
```ini
registry=https://registry.npmmirror.com
```

或使用脚本：
```bash
node <skill-directory>/scripts/config_npm.js --project
```

**提交到版本控制：**
```bash
git add pip.conf .npmrc
git commit -m "Add project-level mirror configuration"
```

这样团队成员克隆项目后自动使用相同的镜像配置。

---

## 示例 7: 故障排查

### 用户请求
```
我配置了镜像但还是慢，怎么回事？
```

### Agent 响应
让我帮您排查问题。可能有以下几个原因：

**1. 检查配置是否生效：**
```bash
pip config list
npm config get registry
```

**2. 清除缓存重试：**
```bash
# Python
pip cache purge

# Node.js
npm cache clean --force
```

**3. 测试具体包的下载：**
```bash
# 查看详细日志
pip install -v requests 2>&1 | findstr "aliyun"
```

**4. 尝试其他镜像：**
```bash
# 切换到清华大学镜像
python <skill-directory>/scripts/config_pip.py tsinghua
```

**5. 临时使用官方源：**
```bash
# 如果镜像有问题，临时使用官方源
pip install -i https://pypi.org/simple/ package_name
```

请告诉我具体的错误信息，我可以提供更针对性的帮助。

---

## 示例 8: CI/CD 环境配置

### 用户请求
```
如何在 GitHub Actions 中配置国内镜像？
```

### Agent 响应
在 CI/CD 环境中，建议在 workflow 文件中显式配置镜像：

**.github/workflows/ci.yml:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Configure pip mirror
      run: |
        pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
        pip config set global.trusted-host mirrors.aliyun.com
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Configure npm mirror
      run: npm config set registry https://registry.npmmirror.com
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
```

这样可以确保 CI 环境中也使用国内镜像，加快构建速度。

---

## 更多资源

- 查看 [SKILL.md](SKILL.md) 了解完整的配置指南
- 查看 [README.md](README.md) 了解功能特性和最佳实践
- 遇到问题？查看 SKILL.md 中的"常见问题排查"章节
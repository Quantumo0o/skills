# 快速参考

## 一键配置（推荐）

```bash
# 配置所有检测到的包管理器
python <skill-directory>/scripts/config_all.py --all

# 查看可用镜像
python <skill-directory>/scripts/config_all.py --show
```

## 单独配置

### Python (pip)
```bash
# 阿里云（默认）
python <skill-directory>/scripts/config_pip.py aliyun

# 清华大学
python <skill-directory>/scripts/config_pip.py tsinghua

# 查看当前配置
python <skill-directory>/scripts/config_pip.py --show
```

### Node.js (npm/yarn/pnpm)
```bash
# 配置所有检测到的工具
node <skill-directory>/scripts/config_npm.js

# 仅配置 npm
node <skill-directory>/scripts/config_npm.js npm

# 查看当前配置
node <skill-directory>/scripts/config_npm.js --show
```

### Rust (cargo)
```bash
python <skill-directory>/scripts/config_all.py --cargo tsinghua
```

### Go (go mod)
```bash
python <skill-directory>/scripts/config_all.py --go qiniu
```

## 验证配置

```bash
# pip
pip config list

# npm
npm config get registry

# cargo
cat ~/.cargo/config.toml

# go
go env GOPROXY
```

## 常用镜像

| 工具 | 推荐镜像 | URL |
|------|---------|-----|
| pip | 阿里云 | https://mirrors.aliyun.com/pypi/simple/ |
| npm | 阿里云 | https://registry.npmmirror.com |
| cargo | 清华大学 | https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/ |
| go | 七牛云 | https://goproxy.cn |

## 常见问题

**Q: 配置后还是慢？**  
A: 清除缓存重试：`pip cache purge` 或 `npm cache clean --force`

**Q: 如何恢复默认配置？**  
A: 
- pip: 删除 `~/.pip/pip.conf` 或 `%USERPROFILE%\pip\pip.ini`
- npm: `npm config delete registry`
- go: 删除 `GOPROXY` 环境变量

**Q: 团队项目如何统一配置？**  
A: 使用项目级配置，将 `.npmrc` 或 `pip.conf` 加入版本控制

## 更多信息

- 完整文档：[SKILL.md](SKILL.md)
- 使用示例：[examples.md](examples.md)
- 故障排查：参考 SKILL.md 中的"常见问题排查"章节
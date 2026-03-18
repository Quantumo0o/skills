# 🎬 videodown - YouTube/Bilibili 视频下载工具

> 搜索 · 下载 · 音频提取 · 素材获取
> 
> 适用场景：视频剪辑 | 内容创作 | 素材收集 | 教程学习

[![npm version](https://img.shields.io/npm/v/videodown.svg)](https://www.npmjs.com/package/videodown)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/chenlong1314/videodown)](https://github.com/chenlong1314/videodown)

**[📖 English Docs](README.md)**

---

## ✨ 特性

- 🔍 **搜索 + 下载** - 关键词搜索视频，一键下载
- 🎯 **双平台支持** - YouTube 和 Bilibili，统一接口
- 🚀 **简单易用** - 自动检查并安装依赖
- 💬 **自然语言** - 支持"找个 3 分钟的 lol 视频"这样的命令
- 📦 **npm 包** - 一条命令安装

---

## 📦 安装

### 方式 1：从 GitHub 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/chenlong1314/videodown.git
cd videodown

# 安装依赖
npm install

# 全局链接
npm link

# 安装系统依赖
brew install yt-dlp ffmpeg jq  # macOS
sudo apt install yt-dlp ffmpeg jq  # Linux
```

### 方式 2：npm（即将发布）

```bash
npm install -g videodown
```

### 方式 3：npx（无需安装）

```bash
npx videodown search "lol 集锦"
```

---

## 🚀 快速开始

### 下载视频

```bash
# 下载指定 URL
videodown https://www.youtube.com/watch?v=xxx

# 指定质量
videodown --url https://youtube.com/watch?v=xxx --quality 1080p

# 仅下载音频
videodown --url https://youtube.com/watch?v=xxx --audio-only
```

### 搜索视频

```bash
# 搜索双平台
videodown search "lol 集锦"

# 仅 YouTube
videodown search "tutorial" --platform youtube

# 仅 Bilibili
videodown search "教程" --platform bilibili

# 按时长过滤
videodown search "tutorial" --duration short  # <4 分钟
videodown search "tutorial" --duration medium # 4-20 分钟

# 搜索并下载第 1 个结果
videodown search "lol" --select 1
```

---

## 💬 自然语言示例

配合 AI 使用时，你可以说：

| 用户说 | AI 调用 |
|--------|--------|
| "找个 lol 视频" | `search "lol"` |
| "下载个 3 分钟的 lol 视频" | `search "lol" --duration short --select 1` |
| "下载这个视频" + URL | `download <url>` |
| "找 B 站的 lol 视频" | `search "lol" --platform bilibili` |
| "只要音频" + URL | `<url> --audio-only` |

---

## 📋 命令参考

### 下载命令

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--quality` | `-q` | 视频质量 | `best` |
| `--output` | `-o` | 输出目录 | `./downloads` |
| `--format` | `-f` | 输出格式 | `mp4` |
| `--audio-only` | `-a` | 仅下载音频 | `false` |

**质量选项：** `360p`, `720p`, `1080p`, `best`

### 搜索命令

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--platform` | `-p` | 搜索平台 | `all` |
| `--limit` | `-l` | 结果数量 | `10` |
| `--duration` | `-d` | 时长过滤 | - |
| `--select` | `-s` | 下载第 N 个结果 | - |

**平台选项：** `youtube`, `bilibili`, `all`

**时长选项：**
- `short` - 小于 4 分钟
- `medium` - 4 到 20 分钟
- `long` - 大于 20 分钟

---

## 🎯 常用场景

### 1. 下载已知 URL

```bash
videodown https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 2. 搜索并选择

```bash
videodown search "lol 集锦"
# 显示结果表格，输入序号下载
```

### 3. 一键下载

```bash
videodown search "lol" --select 1
# 自动下载第 1 个结果
```

### 4. 按时长筛选

```bash
videodown search "教程" --duration medium
# 搜索 4-20 分钟的视频
```

### 5. 指定平台

```bash
videodown search "原神" --platform bilibili
# 只在 B 站搜索
```

### 6. 提取音频

```bash
videodown --url https://youtube.com/watch?v=xxx --audio-only
# 下载为 MP3
```

---

## ⚠️ 注意事项

- **版权**：仅供个人学习和研究使用
- **频率限制**：搜索建议 <10 次/分钟
- **B 站高画质**：4K/8K 需要登录 Cookie
- **系统依赖**：yt-dlp, ffmpeg, jq（安装时自动检查）

---

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/chenlong1314/videodown.git
cd videodown

# 安装依赖
npm install

# 本地运行
npm start -- search "test"
```

---

## 💬 快捷命令

进入交互模式使用快捷命令：

```bash
videodown interactive
# 或
videodown i
```

可用命令：

| 命令 | 说明 | 示例 |
|------|------|------|
| `/search <关键词>` | 搜索视频 | `/search lol` |
| `/download <URL>` | 下载视频 | `/download https://youtube.com/watch?v=xxx` |
| `/audio <URL>` | 提取音频 | `/audio https://youtube.com/watch?v=xxx` |
| `/history` | 查看下载历史 | `/history` |
| `/cancel` | 取消当前任务 | `/cancel` |
| `/help` | 显示帮助信息 | `/help` |

## 🎯 交互特性

### 错误处理

- 7 种错误类型，友好的用户话术
- 快捷恢复选项（重试、搜索类似等）
- 清晰的解释和建议

### 确认机制

- **大文件（>500MB）**：大小提醒 + 预计时间
- **批量下载（>5 个）**：数量确认
- **音频提取**：格式确认

### 进度展示

- 搜索结果带封面预览
- 下载进度条 + 速度 + 剩余时间
- 完成通知带快捷操作

## 📄 许可证

MIT License

---

## 🔗 链接

- [GitHub](https://github.com/chenlong1314/videodown)
- [问题反馈](https://github.com/chenlong1314/videodown/issues)
- **[英文文档](README.md)**

---

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 视频下载引擎
- [BBDown](https://github.com/nilaoda/BBDown) - B 站下载工具
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) - B 站 API 文档

---

## 📝 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.2.0 | 2026-03-18 | 交互策略优化（7 类错误话术、确认机制、进度展示、快捷命令） |
| v1.1.0 | 2026-03-18 | 添加交互策略（错误处理、确认机制、快捷命令） |
| v1.0.0 | 2026-03-18 | 初始版本 |

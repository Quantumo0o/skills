# 多写作skills

支持微信公众号、知乎、今日头条的 Markdown 文章转换与发布。

## 功能特性

- **Markdown 转换**: 支持基础模式、API 模式、AI 模式三种转换方式
- **多平台发布**: 一键发布到微信公众号、知乎、今日头条草稿箱
- **代码块格式化**: 自动处理代码缩进、换行，确保在微信公众号中正确显示
- **图片上传**: 自动上传本地图片到各平台图床
- **内置主题**: 支持多种排版主题（默认、橙色、蓝色、绿色、紫色、简约）
- **自定义 CSS**: 兼容 wenyan-cli CSS 主题格式
- **AI 写作**: 内置 AI 写作助手，支持多种写作风格
- **AI 去痕**: 去除 AI 写作痕迹，让文章更像人工写作
- **图片生成**: 支持 OpenAI DALL-E、Gemini、ModelScope 生成封面图片

## Trigger

TRIGGER when:
- 用户需要发布 Markdown 文章到微信公众号、知乎或今日头条
- 需要调整微信公众号代码块显示格式
- 用户要使用 AI 写作或改写文章
- 需要生成文章封面图片
- 需要对 AI 写作内容进行去痕处理
- 项目是 `writing-publisher` 相关开发维护

## 使用方式

```bash
# 预览转换
uv run writing-publisher convert article.md --preview

# 发布到草稿箱
uv run writing-publisher convert article.md --draft --platform wechat

# AI 写作
uv run writing-publisher write "文章主题" --style technical

# AI 去痕
uv run writing-publisher humanize article.md

# 生成封面图片
uv run writing-publisher generate-image "prompt" --provider openai
```

## 技能职责

1. 维护 `writing-publisher` 项目代码
2. 帮助用户将 Markdown 文章发布到多平台
3. 修复微信公众号显示问题（尤其是代码块格式化）
4. 配置平台凭证（微信 AppID/AppSecret、知乎 Cookie、头条 Cookie）
5. 使用 AI 功能协助写作、改写、去痕
6. 生成文章封面图片
7. 添加新的平台支持

## 代码位置

项目代码通常位于: `*/wechat-publisher/src/writing_publisher/`

核心模块:
- `converter/wechat_style.py` - 微信样式转换器（代码块处理核心）
- `platforms/wechat.py` - 微信公众号发布
- `platforms/zhihu.py` - 知乎发布
- `platforms/toutiao.py` - 今日头条发布
- `writer/` - AI 写作助手
- `humanizer/` - AI 去痕
- `image/providers/` - AI 图片生成

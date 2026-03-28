---
name: gemini-image-gen-watermark-removal
description: "Google Gemini 网页端生图并去水印。通过 Chrome DevTools MCP 工具控制 Chrome 生成、下载图片，再用 GeminiWatermarkTool 去除水印。使用场景：谷歌生图/Gemini 生图/Google Gemini 图片/去水印/浮水印/Gemini watermark removal。"
---

# Google Gemini 生图

通过 Chrome DevTools MCP 工具（`mcp__chrome-devtools__*`）操控已登录 Google 账号的 Chrome 浏览器，在 Gemini 网页端生成并下载图片。

## 前置条件

- Chrome 已启动并开启远程调试端口（`--remote-debugging-port=9222`）
- Chrome 已登录 Google 账号
- Chrome DevTools MCP 服务已连接

## 执行流程

### 1. 打开 Gemini 页面

```
mcp__chrome-devtools__new_page(url="https://gemini.google.com")
```

也可以直接打开已有对话链接复用图片：
```
mcp__chrome-devtools__new_page(url="https://gemini.google.com/app/<对话ID>")
```

### 2. 点击「制作图片」

```
mcp__chrome-devtools__take_snapshot()
// 找到「制作图片」按钮的 uid，然后 click
mcp__chrome-devtools__click(uid="<uid>")
```

### 3. 输入 Prompt 并发送

在 textarea 中输入 prompt，然后按 Enter 发送：

```
mcp__chrome-devtools__fill(uid="<textarea uid>", value="你的Prompt")
mcp__chrome-devtools__press_key(key="Enter")
```

**注意**：prompt 中避免使用"唱""弹奏"等动词关键词，否则 Gemini 会误触发音乐生成而非图片生成。

### 4. 等待图片生成

等待并检查是否出现「下载完整尺寸的图片」按钮：

```
mcp__chrome-devtools__wait_for(text=["下载完整尺寸的图片"], timeout=30000)
mcp__chrome-devtools__take_snapshot()
```

生成完成标志：页面出现「下载完整尺寸的图片」「复制图片」「分享图片」等按钮。

### 5. 下载图片

点击「下载完整尺寸的图片」按钮：

```
mcp__chrome-devtools__click(uid="<下载按钮uid>")
```

等待几秒后检查下载目录：

```bash
sleep 3 && ls -lt ~/Downloads/Gemini_Generated_Image* | head -3
```

### 6. 去水印（可选）

Gemini 生成的图片带有水印，可使用 [GeminiWatermarkTool](https://github.com/allenk/GeminiWatermarkTool) 去除。

**安装**（macOS / Linux）：
```bash
brew install allenk/tap/gwt
```
或从 [GitHub Releases](https://github.com/allenk/GeminiWatermarkTool/releases) 下载二进制文件。

**使用**：
```bash
gwt --force -i <输入图片> -o <输出图片>
```

## 已知问题

| 问题 | 解决方案 |
|------|----------|
| 连接超时 | 确认 Chrome 已以 `--remote-debugging-port=9222` 启动 |
| 标签页未找到 | 用 `mcp__chrome-devtools__list_pages()` 查看已有页面 |
| 触发了音乐生成 | prompt 去掉"唱""弹"等词，改为纯视觉描述 |
| 图片长时间未生成 | Gemini Nano Banana 模型较慢，耐心等待或刷新页面重试 |

## 完成后

- 关闭不用的标签页：`mcp__chrome-devtools__close_page(pageId=<ID>)`

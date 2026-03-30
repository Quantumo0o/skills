# SSH Remote Control Skill
# SSH 远程控制技能

让 AI Agent 通过 SSH 远程连接和控制电脑，无需在被控电脑上安装任何 agent 工具。

Enable AI agents to remotely connect and control computers via SSH, without installing any agent software on the controlled computer.

## 为什么需要这个 Skill？| Why this Skill?

传统的 AI Agent 控制电脑的方式是在本地安装 agent 软件。本 Skill 反其道而行——让 AI Agent 在服务器上运行，通过 SSH 远程控制任何有 SSH 接口的设备。

Traditional AI agents require installing software locally. This skill takes a different approach - running the AI agent on a server and controlling any device with SSH access remotely.

**核心优势 | Core Advantages:**

- **远程控制 | Remote Control**: Agent 在云端，触手伸向多台设备
- **零安装 | Zero Install**: 被控电脑只需开启 SSH，无需安装任何 agent
- **跨平台 | Cross-Platform**: 支持 macOS、Linux
- **CLI 优先 | CLI First**: 对 AI 友好的操作方式，Token 消耗低
- **安全可控 | Secure & Controllable**: 本地可随时关闭穿透工具

## 快速开始 | Quick Start

### 1. 配置环境变量 | Configure Environment Variables

```bash
export SSH_TARGET_HOST="your-tunnel-address.example.com"
export SSH_TARGET_PORT="12345"
export SSH_TARGET_USER="your-username"
export SSH_KEY_PATH="/path/to/private/key"
```

### 2. 测试连接 | Test Connection

```bash
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'echo "OK"'
```

### 3. 让 AI 操作 | Let AI Operate

告诉 AI: "帮我打开远程电脑上的 Safari 浏览器"

Tell AI: "Open Safari on the remote computer"

AI 会执行 | AI will execute:
```bash
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'open -a Safari'
```

## 项目地址 | Project Links

- **ClawHub**: https://clawhub.com/skill/ssh-remote-control
- **GitHub**: https://github.com/openclaw/skill-ssh-remote-control

## 技术架构 | Architecture

```
┌─────────────┐     SSH      ┌─────────────────┐
│   AI Agent │ ──────────> │  Remote Computer  │
│  (服务器)   │   加密隧道   │  (Mac/Linux)      │
│             │ <──────────  │                   │
│  执行命令    │   返回结果   │  无需安装agent   │
└─────────────┘             └─────────────────┘
```

## 应用场景 | Use Cases

1. **远程办公 | Remote Work**: 在手机上通过AI操作办公室电脑
2. **智能家居 | Smart Home**: 连接智能设备执行自动化任务
3. **跨设备协作 | Cross-device**: 一个AI agent管理多台设备
4. **物联网控制 | IoT**: 通过SSH控制树莓派等设备
5. **远程服务器管理 | Server Management**: 无需本地安装任何工具

## 许可 | License

MIT License

## 关于 | About

本技能由 Miss M 开发，用于探索 AI Agent 远程控制电脑的无限可能。

Developed by Miss M to explore the endless possibilities of AI agents remotely controlling computers.

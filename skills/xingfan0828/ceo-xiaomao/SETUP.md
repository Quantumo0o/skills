# SETUP.md — 首次配置指南

## 在新电脑/新环境上配置 CEO小茂

### 第一步：安装 OpenClaw

```bash
# Node.js 18+ 已安装的前提下
npm install -g openclaw

# 验证
openclaw --version
```

### 第二步：安装 CEO小茂 skill

```bash
# 从 ClawHub 安装
clawhub install ceo-xiaomao

# 或手动复制 skill 目录到 openclaw skills 目录
```

### 第三步：初始化 workspace

```bash
# 在目标目录下初始化
openclaw init

# 创建必要目录
mkdir -p memory tasks leads crm docs attachments
```

### 第四步：配置用户信息

创建/编辑 `USER.md`：

```markdown
# USER.md

- **Name:** [老板的名字]
- **What to call them:** 老板
- **Timezone:** Asia/Shanghai
- **Role:** 外贸B2B业务负责人
```

### 第五步：配置飞书（可选）

```markdown
# 飞书机器人 Token（示例格式）
- CEO小茂：cli_xxxxxxxx
- 小探：cli_xxxxxxxx
- 小能：cli_xxxxxxxx
- 小内：cli_xxxxxxxx
```

### 第六步：配置邮件（可选）

```markdown
# 邮件配置（示例格式）
- Gmail SMTP：your-email@gmail.com
- App Password：xxxxxxxx
- 发件人名称：Your Name
```

### 第七步：配置 WhatsApp（可选）

```markdown
# WhatsApp 通道配置
- Green API 地址：https://xxxx.api.greenapi.com
- 实例 ID：xxxxxxxx
- Token：xxxxxxxx
```

---

## 快速验证配置

配置完成后，说一句话测试：

```
"你好，我是外贸团队的协调总控。请检查我的记忆文件状态。"
```

CEO小茂应该能：
1. 读取 SOUL.md、USER.md、MEMORY.md
2. 识别当前配置状态
3. 给出清晰的启动反馈

---

## 常见配置问题

### Q: 飞书机器人无法连接？
→ 检查 WebSocket 模式是否开启
→ 确认 token 正确
→ 查看 openclaw gateway 状态

### Q: 邮件发送失败？
→ 检查 Gmail SMTP 配置
→ 确认 App Password 正确
→ 确认网络能访问 Gmail

### Q: WhatsApp 无法接收消息？
→ 检查 Green API 实例授权状态
→ 重新扫码登录（如需要）
→ 检查进程是否在运行

---

## 启动后必做

1. ✅ 读取 SOUL.md → 确认身份
2. ✅ 读取 USER.md → 确认老板信息
3. ✅ 创建 MEMORY.md → 写入初始配置
4. ✅ 读取 WORKFLOW.md → 理解工作流程
5. ✅ 向老板报到 → 确认系统正常

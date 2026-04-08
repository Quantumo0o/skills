# Feishu Relay 自动接入指南

## 核心问题
新安装的 skill 如何自动使用 feishu-relay 发送通知，无需手动修改？

## 解决方案：三层自动接入

### 第一层：全局命令（已实现）

创建 `/usr/local/bin/notify` 全局命令，任何脚本都可以直接调用：

```bash
notify "标题" "内容"
```

✅ **优点**：最简单，所有 skill 立即可用
❌ **缺点**：skill 需要显式调用

### 第二层：环境变量注入（推荐）

在 OpenClaw 配置中设置环境变量，skill 自动继承：

```yaml
# ~/.openclaw/config.yaml
skills:
  default_env:
    BASH_ENV: "/opt/feishu-notifier/skill-env.sh"
    NOTIFY_CMD: "/opt/feishu-notifier/bin/notify"
```

创建 `/opt/feishu-notifier/skill-env.sh`：

```bash
#!/bin/bash
# Skill 自动加载的环境

notify() {
    /opt/feishu-notifier/bin/notify "$@"
}

notify_later() {
    /opt/feishu-notifier/bin/feishu-task-v2 in "$@"
}

export -f notify notify_later
```

✅ **优点**：skill 无需修改，自动获得 notify 函数
❌ **缺点**：需要修改 OpenClaw 配置

### 第三层：Skill 安装钩子（最自动化）

创建 skill 安装后自动配置脚本：

```bash
# /opt/feishu-notifier/bin/feishu-relay-setup
echo "Skill 安装完成，自动配置 feishu-relay 集成..."

# 为 skill 创建 notify 快捷方式
ln -sf /opt/feishu-notifier/bin/notify "$SKILL_DIR/notify"

# 在 SKILL.md 中添加使用说明
...
```

✅ **优点**：完全自动化，skill 作者无需关心
❌ **缺点**：需要 OpenClaw 支持安装钩子

## 当前实现状态

| 层级 | 状态 | 说明 |
|------|------|------|
| 第一层：全局命令 | ✅ 已实现 | `/usr/local/bin/notify` |
| 第二层：环境变量 | ⏳ 待配置 | 需要修改 `~/.openclaw/config.yaml` |
| 第三层：安装钩子 | ⏳ 待实现 | 需要 OpenClaw 支持 |

## 使用方式

### 方式 1：直接调用（立即可用）

任何 skill 的脚本中：

```bash
notify "标题" "内容"
```

### 方式 2：通过环境变量（配置后）

Skill 自动继承 `notify` 函数：

```bash
#!/bin/bash
# 无需任何导入，直接使用
notify "文献管理" "发现 5 篇新文献"
```

### 方式 3：定时通知

```bash
/opt/feishu-notifier/bin/feishu-task-v2 in 30 "30分钟后提醒"
```

## 下一步

1. **配置 OpenClaw 环境变量**（用户操作一次）
2. **测试新 skill 自动接入**
3. **文档化给 skill 开发者**

## 总结

- ✅ **无需修改 skill 代码**（使用全局命令）
- ✅ **自动注入环境**（配置后）
- ✅ **向后兼容**（没有 feishu-relay 也能工作）
- ✅ **符合"省心"原则**

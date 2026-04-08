# Feishu Relay 自动接入方案

## 问题
新安装的 skill 需要手动修改才能使用 feishu-relay 发送通知，违背"省心"原则。

## 解决方案

### 方案 1：环境变量注入（推荐）

在 OpenClaw 配置中设置全局环境变量，让所有 skill 自动使用 feishu-relay。

```yaml
# ~/.openclaw/config.yaml
skills:
  default_env:
    # 设置通知命令路径
    NOTIFY_CMD: "/opt/feishu-notifier/bin/notify"
    FEISHU_TASK_CMD: "/opt/feishu-notifier/bin/feishu-task-v2"
    
    # 预加载的函数
    BASH_ENV: "/opt/feishu-notifier/skill-env.sh"
```

创建 `/opt/feishu-notifier/skill-env.sh`：
```bash
# Skill 环境变量
# 所有 skill 自动加载

# 通知函数
notify() {
    /opt/feishu-notifier/bin/notify "$@"
}

# 定时通知函数
notify_later() {
    /opt/feishu-notifier/bin/feishu-task-v2 in "$@"
}

export -f notify
export -f notify_later
```

### 方案 2：命令替换

创建 `/usr/local/bin/notify` 覆盖默认命令：
```bash
#!/bin/bash
# 统一的 notify 命令
# 如果 feishu-relay 可用，使用它；否则使用系统默认

if [ -x "/opt/feishu-notifier/bin/notify" ]; then
    /opt/feishu-notifier/bin/notify "$@"
else
    #  fallback 到系统默认通知
    echo "$@"
fi
```

### 方案 3：Skill 模板

创建 skill 模板，新 skill 自动生成 notify 支持：

```bash
# ~/.openclaw/templates/skill/notify.sh
#!/bin/bash
# 本 skill 的通知函数

source /opt/feishu-notifier/skill-env.sh 2>/dev/null || {
    # 如果 feishu-relay 不可用，使用 echo 作为 fallback
    notify() { echo "[NOTIFY] $*"; }
}
```

### 方案 4：运行时注入（最自动化）

修改 OpenClaw 的 skill 执行器，在启动 skill 前自动注入通知函数：

```bash
# 在 skill 执行前注入
export SKILL_NAME="<skill-name>"
export NOTIFY_CMD="/opt/feishu-notifier/bin/notify"

# 注入 bash 函数
eval 'notify() { $NOTIFY_CMD "[$SKILL_NAME] $1" "${2:-}"; }'
```

## 推荐实现

结合方案 1 和方案 4：

1. **全局配置**：设置 `NOTIFY_CMD` 环境变量
2. **自动注入**：OpenClaw 启动 skill 时自动注入 `notify` 函数
3. **Fallback**：如果 feishu-relay 不可用，使用 echo 或系统通知

这样新 skill 无需任何修改，直接调用 `notify "标题" "内容"` 即可。

## 实施步骤

1. 创建 `/opt/feishu-notifier/skill-env.sh`
2. 修改 OpenClaw 配置，添加 `BASH_ENV`
3. 测试新 skill 自动获得通知能力
4. 更新文档

## 效果

- ✅ 新 skill 无需修改即可发送通知
- ✅ 所有通知统一走 feishu-relay
- ✅ 符合"省心"设计原则
- ✅ 向后兼容（没有 feishu-relay 也能工作）

# Feishu Relay 自动接管方案

## 问题
现有系统、配置、skill 如何自动迁移到使用 feishu-relay？

## 解决方案：三层自动接管

### 第一层：全局命令接管（已实现）

创建 `/usr/local/bin/notify` 全局命令，**替换**系统中所有 `echo` 或 `print` 发送通知的方式。

**迁移前：**
```bash
# 旧方式 - 只在控制台显示
echo "通知内容" 
```

**迁移后：**
```bash
# 新方式 - 通过 feishu-relay 发送到飞书
notify "标题" "内容"
```

✅ **自动接管**：任何调用 `notify` 的地方都自动使用 feishu-relay

### 第二层：自动发现 + 迁移（已实现）

使用 `feishu-relay-discover` 自动扫描系统中所有通知源：

```bash
# 扫描所有可能发送通知的地方
feishu-relay-discover all

# 输出示例：
# [00:47:28] 发现 [root] 的通知任务: 0 23 * * * notify "提醒" "睡觉"
# [00:47:28] 发现 skill 'tencent-docs' 有 146 处可能发送通知
# [00:47:29]   ✓ 已集成 feishu-relay
```

### 第三层：自动迁移工具（已实现）

使用 `feishu-relay-migrate` 自动迁移现有系统：

```bash
# 迁移所有系统
feishu-relay-migrate all

# 迁移特定组件
feishu-relay-migrate crontab    # 迁移 crontab
feishu-relay-migrate skills     # 迁移所有 skill
feishu-relay-migrate literature # 迁移文献管理系统
```

## 自动接管流程

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 发现                                            │
│  feishu-relay-discover all                               │
│  ↓ 扫描系统中所有通知源                                  │
├─────────────────────────────────────────────────────────┤
│  Step 2: 分析                                            │
│  - 哪些已经在用 feishu-relay？                           │
│  - 哪些还在用旧方式（echo/print）？                      │
│  - 哪些需要迁移？                                        │
├─────────────────────────────────────────────────────────┤
│  Step 3: 迁移                                            │
│  feishu-relay-migrate all                                │
│  ↓ 自动替换旧方式为 feishu-relay                         │
├─────────────────────────────────────────────────────────┤
│  Step 4: 验证                                            │
│  - 测试通知发送                                          │
│  - 确认所有组件正常工作                                  │
└─────────────────────────────────────────────────────────┘
```

## 具体迁移内容

### 1. 系统 crontab

**迁移前：**
```bash
# 只在控制台输出
echo "磁盘使用率: 80%"
```

**迁移后：**
```bash
# 自动添加到 crontab
0 */6 * * * /opt/feishu-notifier/bin/notify "💾 系统监控" "磁盘使用率: $(df / | awk 'NR==2{print $5}')"
```

### 2. Skill 通知

**迁移前：**
```bash
# skill 脚本中
echo "[SKILL] 任务完成"
```

**迁移后：**
```bash
# 自动创建 notify 脚本
./notify "任务完成" "详细信息"
# 或
/opt/feishu-notifier/bin/notify "[SkillName] 任务完成"
```

### 3. 文献管理系统

**迁移前：**
```bash
# auto_index.sh
echo "索引完成: 新增 5 篇"
```

**迁移后：**
```bash
# 自动添加通知
/opt/feishu-notifier/bin/notify "📚 文献管理" "新增 5 篇文献，索引完成"
```

## 自动化程度

| 组件 | 自动发现 | 自动迁移 | 状态 |
|------|---------|---------|------|
| 系统 crontab | ✅ | ✅ | 已接管 |
| Skill 通知 | ✅ | ✅ | 已接管 |
| 文献管理系统 | ✅ | ✅ | 已接管 |
| 系统监控 | ✅ | ✅ | 已接管 |
| 全局命令 | ✅ | ✅ | 已接管 |

## 使用方式

### 一键接管所有系统

```bash
# 1. 发现
/opt/feishu-notifier/bin/feishu-relay-discover all

# 2. 迁移
/opt/feishu-notifier/bin/feishu-relay-migrate all

# 3. 验证
/opt/feishu-notifier/bin/feishu-relay-migrate verify
```

### 新系统安装时自动接管

```bash
# 安装 feishu-relay 时自动运行
./install.sh  # 内部调用 feishu-relay-migrate all
```

### 定期检查新组件

```bash
# 添加到 crontab，每天检查一次
0 9 * * * /opt/feishu-notifier/bin/feishu-relay-discover all
```

## 效果

- ✅ **现有系统无需手动修改**，自动迁移到 feishu-relay
- ✅ **新系统安装时自动接管**
- ✅ **所有通知统一走 feishu-relay**
- ✅ **向后兼容**，没有 feishu-relay 也能工作
- ✅ **符合"省心"原则**

## 总结

**回答你的问题：**

> "在用 feishu-relay 之前，系统、配置、skill 怎么自动修改采用 feishu-relay？"

**答案：使用自动发现和迁移工具**

1. `feishu-relay-discover` - 自动发现系统中所有通知源
2. `feishu-relay-migrate` - 自动迁移到 feishu-relay
3. 全局 `notify` 命令 - 自动接管所有通知

**无需手动修改任何代码！**

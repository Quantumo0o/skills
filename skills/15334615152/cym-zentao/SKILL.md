# cym-zentao - 禅道项目管理 CLI

## 安装

```bash
npm link
```

## 命令

### login
测试登录：
```bash
cym-zentao login
```

### list-executions
列出执行（项目迭代）：
```bash
cym-zentao list-executions [keyword]
```

### create-task
创建任务：
```bash
cym-zentao create-task <executionId> <name> <assignedTo> [options]
```

**options 格式：** JSON 字符串
- `pri`: 优先级 (1-4)
- `estimate`: 预计工时
- `type`: 任务类型
- `estStarted`: 开始日期 (YYYY-MM-DD)
- `deadline`: 截止日期 (YYYY-MM-DD)
- `desc`: 描述

**示例：**
```bash
cym-zentao create-task 6159 "测试功能" "陈跃美"
cym-zentao create-task 6159 "测试功能" "陈跃美" '{"pri":2,"estimate":8,"type":"test"}'
```

### list-tasks
列出任务：
```bash
cym-zentao list-tasks <executionId> [status]
```

## 配置

在 `TOOLS.md` 中添加：
```markdown
## 禅道 API (ZenTao API)
- **API 地址：** https://ztpms.springgroup.cn/
- **用户名：** 1010753
- **密码：** Qwertyu@123
```

---
name: huo15-odoo
description: |
  火一五欧度技能（辉火云企业套件 Odoo 19 接口访问指南）。
  支持分布式配置：全局保存系统地址和数据库名，每个 agent 独立保存自己的用户名和密码。
  其他 Odoo 技能可复用本技能保存的配置。
trigger:
  - patterns:
      - "odoo"
      - "辉火云"
      - "欧度"
      - "欧度"
      - "辉火"
    type: fuzzy
---

# 火一五欧度技能（Odoo 19）

> 辉火云企业套件（Odoo 19）接口访问 · 分布式配置版
> **重要**：必须使用 XML-RPC，不兼容 odoorpc 库！

---

## 🏗️ 配置架构

```
全局配置（所有 agent 共享）
  └── ODOO_URL      系统地址
  └── ODOO_DB       数据库名

Agent 本地配置（各 agent 独立）
  └── 用户名         user
  └── 密码           password
```

**查找顺序：**
- 用户名/密码 → 先查本 agent 本地配置，没有则提示用户输入
- 系统地址/数据库名 → 读全局配置
- 其他 Odoo 技能复用同样的逻辑

---

## 🚀 首次使用（自动引导）

首次使用本技能时，按顺序引导：

### 第一步：全局初始化（一次性）

> 由主 agent（main）完成，之后所有 agent 共享

技能检测到没有全局配置，会提示：

```
🔧 Odoo 全局配置
请提供以下信息（前后不能有空格）：

1. 公司系统地址（如 https://huihuoyun.2008qd.com.cn）：
2. 数据库名（如 xinqiantu）：
```

→ 用户输入后，保存到 `~/.openclaw/openclaw.json` 的 `skills.entries.huo15-odoo.env`

> 说「更新 Odoo 全局配置」可重新填写

### 第二步：Agent 凭证初始化

> 每个 agent 会话首次使用时独立进行

技能检测到本 agent 没有凭证配置，会提示：

```
🔑 请提供你的 Odoo 登录信息（仅本 Agent 可访问，不会共享）：

1. 用户名（邮箱）：
2. 密码：
```

→ 用户输入后，保存到 `~/.openclaw/agents/{agentId}/odoo_creds.json`

> 说「更新 Odoo 凭证」可重新填写本 agent 的凭证

---

## 🔧 Python 连接模板

> 在任何 Python 脚本中，先用 helper 读取配置：

```python
import ssl
import json
import os
import xmlrpc.client

# ── 读取配置 ──────────────────────────────────────────────
AGENT_ID = os.environ.get('OC_AGENT_ID', 'main')
AGENTS_DIR = os.path.expanduser('~/.openclaw/agents')

# 1. 全局配置（系统地址 + 数据库名）
import subprocess
r = subprocess.run(
    ['python3', os.path.expanduser('~/.openclaw/workspace/scripts/odoo_config.py'), 'resolve'],
    capture_output=True, text=True,
    env={**os.environ, 'OC_AGENT_ID': AGENT_ID}
)
cfg = json.loads(r.stdout.strip())
# cfg = { 'url': ..., 'db': ..., 'user': ..., 'password': ... }

url = cfg['url']
db = cfg['db']
user = cfg['user']
password = cfg['password']

# 2. SSL 跳过（辉火云证书问题）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 3. 连接
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)

print(f"✅ 连接成功! UID: {uid}")
```

---

## 📋 Odoo 19 常用模型

### 联系人（res.partner）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'res.partner', 'create', [values])` |
| 更新 | `execute_kw(db, uid, password, 'res.partner', 'write', [id, values])` |

### 项目（project.project）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.project', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.project', 'create', [values])` |

### 任务（project.task）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.task', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.task', 'create', [values])` |

---

## 🔧 常用操作示例

### 查询客户
```python
domain = [('name', 'ilike', '关键词')]
fields = ['id', 'name', 'vat', 'street', 'city', 'phone', 'email']
result = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
    [domain], {'fields': fields, 'limit': 10})
```

### 创建客户公司
```python
values = {
    'name': '公司名称',
    'company_type': 'company',
    'vat': '统一社会信用代码',
}
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 创建联系人（关联到公司）
```python
values = {
    'name': '联系人姓名',
    'parent_id': partner_id,
    'type': 'contact',
    'function': '职位',
    'phone': '电话',
    'email': '邮箱',
}
contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 查询项目
```python
domain = [('active', '=', True)]
fields = ['id', 'name', 'partner_id', 'user_id']
result = models.execute_kw(db, uid, password, 'project.project', 'search_read',
    [domain], {'fields': fields, 'limit': 20})
```

### 创建项目
```python
values = {
    'name': '项目名称',
    'partner_id': partner_id,
    'description': '项目描述',
}
project_id = models.execute_kw(db, uid, password, 'project.project', 'create', [values])
```

### 查询任务（⚠️ 必须加 active=True）
```python
domain = [
    ('active', '=', True),
    ('project_id', '=', project_id),
]
fields = ['id', 'name', 'user_ids', 'stage_id', 'priority']
result = models.execute_kw(db, uid, password, 'project.task', 'search_read',
    [domain], {'fields': fields, 'limit': 50})
```

### 创建任务
```python
values = {
    'name': '任务名称',
    'project_id': project_id,
    'user_ids': [(6, 0, [user_id])],
    'description': '任务描述',
    'priority': '0',
}
task_id = models.execute_kw(db, uid, password, 'project.task', 'create', [values])
```

---

## 📊 execute_kw 参数说明

```python
models.execute_kw(db, uid, password, model_name, method, args, kwargs)
```

| 参数 | 说明 |
|------|------|
| db | 数据库名 |
| uid | 登录后的用户ID（authenticate 返回） |
| password | 密码 |
| model_name | 模型名，如 'res.partner' |
| method | 'search_read', 'create', 'write', 'unlink' |
| args | domain 列表 |
| kwargs | {'fields': [...], 'limit': 10} |

---

## ⚠️ 注意事项

1. **必须使用 XML-RPC**，路径 `/xmlrpc/2/common` 和 `/xmlrpc/2/object`
2. **SSL 跳过**：辉火云证书问题，连接时加 `context=ctx`
3. **任务查询**：必须加 `('active', '=', True)` 过滤
4. **用户名/密码** 各 agent 独立存储，不共享
5. **系统地址/数据库名** 全局共享，所有 agent 一致

---

## 📚 知识库 (Knowledge) 操作

### 创建知识库文章
```python
article_id = models.execute_kw(db, uid, password, 'knowledge.article', 'create', [{
    'name': '文章标题',
    'body': '<h1>内容</h1><p>正文</p>',
    'internal_permission': 'write',
}])
```

| 字段 | 类型 | 说明 |
|------|------|------|
| name | Char | 文章标题 |
| body | Html | 内容（HTML格式） |
| internal_permission | Selection | 'write'/'read'/'none' |

---

## 🐳 Odoo Docker 本地开发

| 资源 | 地址/路径 |
|------|-----------|
| Docker 配置仓库 | https://cnb.cool/huo15/tools/odoo19_docker |
| 本地路径 | `~/workspace/study/odoo_study/odoo19_docker` |

启动：
```bash
cd ~/workspace/study/odoo_study/odoo19_docker
docker compose -p <项目名称> up --build
```

---

## 🔗 相关技能

- **huo15-doc-template**：文档生成
- **odoo-reporting**：Odoo 数据报表

---

## 配置命令

| 命令 | 说明 |
|------|------|
| 「更新 Odoo 全局配置」 | 重新设置系统地址和数据库名 |
| 「更新 Odoo 凭证」 | 重新设置本 agent 的用户名和密码 |
| 「查看 Odoo 配置」 | 显示当前配置状态（不显示密码） |

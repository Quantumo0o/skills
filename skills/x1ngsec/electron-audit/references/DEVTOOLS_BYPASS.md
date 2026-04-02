# DevTools 强开与反调试绕过实操手册

## 核心思路

**不要列举理论，按这个顺序做：试 → 诊断 → 修 → 验证。**

---

## 一、前置准备

### 1.1 定位应用文件

```
从目标路径出发，定位以下文件:

1. 可执行文件:
   - 应用根目录下的 *.exe（Windows）
   - 通常与 resources/ 同级

2. ASAR 文件:
   - resources/app.asar（标准位置）
   - resources/app/ 目录（未打包的应用）

3. 主进程入口:
   解包 asar 后，查看 package.json 的 "main" 字段
   通常是 main.js / index.js / background.js / electron.js
```

### 1.2 备份原始文件

```bash
# 备份 asar（必须在任何修改前执行）
cp app.asar app.asar.bak
```

---

## 二、方法矩阵（按侵入性从低到高）

| 方法 | 侵入性 | 成功率 | 前提条件 | 优先级 |
|:-----|:-------|:-------|:---------|:-------|
| 快捷键 | 无 | 低 | 未被拦截 | 1 |
| --remote-debugging-port | 无 | 高 | Fuse 未禁用 | 2 |
| --inspect | 无 | 中 | EnableNodeCliInspectArguments=on | 3 |
| ELECTRON_RUN_AS_NODE | 无 | 中 | RunAsNode=on | 4 |
| 修改 main.js + 重打包 | 中 | 高 | ASAR 完整性校验=off | 5 |
| Fuse 翻转 + 修改 | 高 | 高 | 对 exe 有写权限 | 6 |

---

## 三、方法详解

### 方法 1: 直接快捷键

```
启动应用后依次尝试:
  F12
  Ctrl+Shift+I
  Ctrl+Shift+J（直接打开 Console）

观察结果:
  A. DevTools 打开且稳定 → 直接使用，不需要任何 patch
  B. DevTools 打开后立即关闭（闪一下）→ 有 closeDevTools 监听
  C. 完全没反应 → 快捷键被拦截或未注册
  D. 页面行为异常（重定向/空白）→ 有反调试代码
```

### 方法 2: --remote-debugging-port（推荐，不修改文件）

```bash
# 启动应用并开启远程调试端口
./app.exe --remote-debugging-port=9222

# 然后在 Chrome 浏览器中:
# 1. 访问 chrome://inspect
# 2. 点击 "Configure..." → 添加 localhost:9222
# 3. 等待目标出现在 Remote Target 列表中
# 4. 点击 "inspect" 打开 DevTools

# 或者直接访问:
# http://localhost:9222/json  → 获取调试目标列表
# 复制 devtoolsFrontendUrl 在浏览器中打开
```

**优势**: 完全不修改应用文件，不触发 ASAR 完整性校验，不触发应用内反调试代码。

**失败场景**: 部分应用在主进程中通过 `app.commandLine.appendSwitch` 禁用了 remote-debugging。

### 方法 3: --inspect（Node.js 调试器）

```bash
# 开启 Node.js Inspector
./app.exe --inspect=9229

# 连接方式:
# Chrome: chrome://inspect → 等待目标出现
# VS Code: 配置 attach 调试
# 或者直接用 Node.js:
#   node inspect localhost:9229

# 连接后可在 Console 中执行:
const {BrowserWindow} = require('electron')
BrowserWindow.getAllWindows().forEach(w => w.webContents.openDevTools())
```

**前提**: `EnableNodeCliInspectArguments` Fuse 为 on。

### 方法 4: ELECTRON_RUN_AS_NODE

```bash
# Windows
set ELECTRON_RUN_AS_NODE=1
app.exe -e "const {app} = require('electron'); console.log('Node.js mode')"

# 验证是否进入 Node.js 模式:
set ELECTRON_RUN_AS_NODE=1
app.exe -e "console.log(process.versions)"

# 如果成功，可以用这个打开应用并附加调试器:
# （但这种方式不会启动 Electron GUI，主要用于验证 Fuse 状态）
```

**前提**: `RunAsNode` Fuse 为 on。

### 方法 5: 修改 main.js + 重打包

#### 5.1 解包

```bash
npx @electron/asar extract app.asar app_extracted/
```

#### 5.2 在 main.js 最顶部注入（第一行之前）

```javascript
// === DevTools Force Open Patch ===
const { app: __patchApp, globalShortcut: __gs } = require('electron');

__patchApp.on('browser-window-created', (_, win) => {
  // 拦截 closeDevTools 调用
  const __origClose = win.webContents.closeDevTools.bind(win.webContents);
  win.webContents.closeDevTools = () => {};

  win.webContents.on('did-finish-load', () => {
    if (win.isDestroyed()) return;
    // undocked 模式: 独立窗口，避免触发窗口尺寸检测
    win.webContents.openDevTools({ mode: 'undocked' });
  });

  // 拦截 devtools-closed 事件后自动重新打开
  win.webContents.on('devtools-closed', () => {
    if (!win.isDestroyed()) {
      setTimeout(() => {
        if (!win.isDestroyed()) {
          win.webContents.openDevTools({ mode: 'undocked' });
        }
      }, 500);
    }
  });
});

// 注册全局快捷键作为备份
__patchApp.whenReady().then(() => {
  try {
    __gs.register('F12', () => {
      const { BrowserWindow } = require('electron');
      const win = BrowserWindow.getFocusedWindow();
      if (win) win.webContents.toggleDevTools();
    });
  } catch(e) {}
});
// === End Patch ===
```

#### 5.3 重打包

```bash
npx @electron/asar pack app_extracted/ app.asar
```

#### 5.4 验证

```
启动应用，确认:
  [x] DevTools 自动弹出（undocked 模式，独立窗口）
  [x] DevTools 不会被自动关闭
  [x] Console 可正常输入和执行
  [x] Network 面板可正常抓包
  [x] 应用功能正常（未因 patch 导致崩溃）
```

### 方法 6: Fuse 翻转

```bash
# 当 ASAR 完整性校验阻止方法 5 时:
npx @electron/fuses flip app.exe \
  EnableEmbeddedAsarIntegrityValidation=off

# 如果还需要 --inspect:
npx @electron/fuses flip app.exe \
  EnableNodeCliInspectArguments=on

# 然后再执行方法 5 的修改
```

---

## 四、反调试绕过

### 4.1 debugger 无限循环

**症状**: 打开 DevTools 后，Sources 面板不断在 `debugger` 语句处暂停。

**原理**:
```javascript
// 应用代码中:
setInterval(() => { debugger; }, 100);
// 或:
(function loop() { debugger; setTimeout(loop, 100); })();
// 或（更隐蔽）:
Function('debugger')();
```

**绕过方案 A — 在注入代码中拦截（推荐）**:

```javascript
// 在 main.js patch 中追加，或在 preload 最早期注入:

// 拦截 setInterval/setTimeout 中的 debugger
const __origSetInterval = setInterval;
const __origSetTimeout = setTimeout;

globalThis.setInterval = function(fn, ms, ...args) {
  if (typeof fn === 'function') {
    const s = fn.toString();
    if (s.includes('debugger') || s.includes('Function') && s.includes('debug')) {
      return 0; // 直接丢弃
    }
  }
  if (typeof fn === 'string' && fn.includes('debugger')) return 0;
  return __origSetInterval(fn, ms, ...args);
};

globalThis.setTimeout = function(fn, ms, ...args) {
  if (typeof fn === 'function') {
    const s = fn.toString();
    if (s.includes('debugger')) return 0;
  }
  if (typeof fn === 'string' && fn.includes('debugger')) return 0;
  return __origSetTimeout(fn, ms, ...args);
};

// 拦截 Function 构造器中的 debugger
const __origFunction = Function;
globalThis.Function = function(...args) {
  if (args.some(a => typeof a === 'string' && a.includes('debugger'))) {
    return () => {};
  }
  return new __origFunction(...args);
};
globalThis.Function.prototype = __origFunction.prototype;
```

**绕过方案 B — 使用 CDP 跳过（配合方法 2）**:

```
使用 --remote-debugging-port 连接后:
1. 在 DevTools 的 Sources 面板
2. 右键点击 debugger 语句所在行
3. 选择 "Never pause here"
4. 或点击右上角 ⏯ 旁的 ⏩ "Deactivate breakpoints"

更彻底:
在 Console 中执行:
  // 通过 CDP 禁用所有暂停
  // 注: 此方法需要 CDP 协议级操作，通常在远程调试模式下使用
```

### 4.2 console 被重写

**症状**: Console 中 `console.log()` 不输出，或输出被吞掉。

**原理**:
```javascript
// 应用代码中:
console.log = () => {};
console.warn = () => {};
console.error = () => {};
// 或更隐蔽:
Object.defineProperty(console, 'log', { value: () => {}, writable: false });
```

**绕过 — 在 preload 最早期保存原始引用**:

```javascript
// 在 main.js patch 中，通过 preload 注入:
// 或者在修改后的 preload.js 最顶部:

const __safeConsole = {
  log: console.log.bind(console),
  warn: console.warn.bind(console),
  error: console.error.bind(console),
  info: console.info.bind(console),
  dir: console.dir.bind(console),
  table: console.table.bind(console),
};

// 保护 console 不被覆盖
const __origDefProp = Object.defineProperty;
Object.defineProperty = function(obj, prop, desc) {
  if (obj === console && ['log','warn','error','info','dir','table'].includes(prop)) {
    return obj; // 忽略对 console 方法的覆盖
  }
  return __origDefProp.call(this, obj, prop, desc);
};

// 挂到 window 上供手动使用
if (typeof window !== 'undefined') {
  window.__console = __safeConsole;
}
```

**绕过方案 B — DevTools Console 直接操作**:

```javascript
// 在 DevTools Console 中，直接从 iframe 获取原始 console:
const iframe = document.createElement('iframe');
iframe.style.display = 'none';
document.body.appendChild(iframe);
const safeConsole = iframe.contentWindow.console;
safeConsole.log('This bypasses console override');
```

### 4.3 窗口尺寸检测

**症状**: 打开 DevTools（docked 模式）后，页面检测到窗口内外尺寸差异，触发反调试。

**原理**:
```javascript
// 应用代码中:
setInterval(() => {
  if (window.outerWidth - window.innerWidth > 160 ||
      window.outerHeight - window.innerHeight > 160) {
    // 检测到 DevTools
    document.body.innerHTML = '';
    window.location.reload();
  }
}, 500);
```

**绕过**: 使用 **undocked 模式**打开 DevTools。

```javascript
// 注入代码中已使用 undocked:
win.webContents.openDevTools({ mode: 'undocked' });
// undocked = DevTools 在独立窗口中，不影响应用窗口尺寸
```

如果必须用 docked 模式:
```javascript
// 覆盖检测属性
Object.defineProperty(window, 'outerWidth', {
  get: () => window.innerWidth
});
Object.defineProperty(window, 'outerHeight', {
  get: () => window.innerHeight
});
```

### 4.4 性能计时检测

**症状**: 应用通过 `performance.now()` 或 `Date.now()` 计时，检测到代码执行变慢（因为调试器附加会增加开销），然后触发反调试。

**原理**:
```javascript
// 应用代码中:
const start = performance.now();
// ... 一些操作 ...
const end = performance.now();
if (end - start > 100) {
  // 检测到调试器（正常执行应该 < 10ms）
  window.close();
}
```

**绕过**:
```javascript
// 覆盖计时函数，使其返回伪造的短时间
const __origPerfNow = performance.now.bind(performance);
let __fakeTime = __origPerfNow();
performance.now = function() {
  __fakeTime += 0.1; // 模拟极短的执行时间
  return __fakeTime;
};
```

### 4.5 toString 检测

**症状**: 应用通过检测函数的 `toString()` 返回值来判断是否被 Hook。

**原理**:
```javascript
// 应用检测 setInterval 是否被替换:
if (setInterval.toString() !== 'function setInterval() { [native code] }') {
  // 检测到 Hook
}
```

**绕过**:
```javascript
// 在 Hook 函数上伪造 toString:
const hookedFn = function(...args) { /* hook logic */ };
hookedFn.toString = function() { return 'function setInterval() { [native code] }'; };
```

### 4.6 WebSocket/心跳检测

**症状**: 应用通过 WebSocket 向服务端发送心跳，服务端检测到异常（如心跳间隔变长）后下发关闭指令。

**绕过**: 监控 WebSocket 消息，过滤/修改反调试相关的控制消息。

```javascript
// Hook WebSocket
const __origWS = WebSocket;
WebSocket = function(url, protocols) {
  const ws = new __origWS(url, protocols);
  const __origSend = ws.send.bind(ws);
  ws.send = function(data) {
    // 可以在此拦截/修改发送的数据
    return __origSend(data);
  };
  return ws;
};
WebSocket.prototype = __origWS.prototype;
```

---

## 五、ASAR 完整性校验绕过

### 5.1 识别校验类型

```
类型 A — Electron 内置 Fuse:
  npx @electron/fuses read app.exe
  如果 EnableEmbeddedAsarIntegrityValidation=on → 内置校验

类型 B — 应用自定义校验:
  搜索代码中的 ASAR 完整性校验:
    - fs.readFileSync + crypto.createHash → 自定义 hash 校验
    - checksum / integrity / verify 相关关键词

类型 C — 无校验:
  修改 asar 后应用正常启动 → 无校验
```

### 5.2 绕过方案

```
类型 A 绕过:
  方案 1: Fuse 翻转
    npx @electron/fuses flip app.exe EnableEmbeddedAsarIntegrityValidation=off
  
  方案 2: 不修改 asar，用 --remote-debugging-port
    app.exe --remote-debugging-port=9222

类型 B 绕过:
  方案 1: 定位校验代码，patch 掉校验逻辑
    - 搜索 hash/checksum/integrity 关键词
    - 找到校验函数，使其始终返回 true
    
  方案 2: 计算修改后 asar 的新 hash，替换校验值
    - 找到存储 hash 的位置（可能在 exe 资源段或配置文件中）
    - 计算新 asar 的 hash 并替换

  方案 3: 同样使用 --remote-debugging-port 避免修改文件
```

---

## 六、特殊场景

### 6.1 多窗口应用

```
某些应用有多个 BrowserWindow（如主窗口 + 登录窗口 + 设置窗口）。
注入代码已使用 browser-window-created 事件，所有窗口都会自动打开 DevTools。

如果只想针对特定窗口:
  app.on('browser-window-created', (_, win) => {
    win.webContents.on('did-finish-load', () => {
      const url = win.webContents.getURL();
      if (url.includes('index.html') || url.includes('main')) {
        win.webContents.openDevTools({ mode: 'undocked' });
      }
    });
  });
```

### 6.2 Electron + 加壳（如 VMProtect / Themida）

```
如果 exe 被加壳:
  1. 先脱壳（超出本技能范围）
  2. 或者不修改 exe/asar，纯用 --remote-debugging-port
  3. 加壳通常不影响 --remote-debugging-port 方案
```

### 6.3 Electron Forge / Electron Builder 特殊打包

```
某些打包工具会:
  - 将 asar 嵌入 exe 内部 → 需要先提取
  - 使用自定义资源加载器 → 可能影响 asar 位置
  
识别方法:
  如果 resources/ 下没有 app.asar:
    - 检查 exe 同级是否有 .asar 文件
    - 检查 exe 内部资源（binwalk app.exe | grep asar）
    - 检查是否有 app/ 目录（未打包模式）
```

---

## 七、完成标准

```
DevTools 强开完成的标志:
  [x] DevTools 可以通过某种方式稳定打开
  [x] Console 面板可正常输入和执行 JavaScript
  [x] Network 面板可正常抓取请求
  [x] Sources 面板可正常查看/调试源码
  [x] 不会被反调试代码自动关闭或干扰
  [x] 应用主要功能正常运行

如果以上无法全部满足，记录原因并报告:
  - 哪些方法已尝试
  - 失败原因
  - 建议的替代方案
```

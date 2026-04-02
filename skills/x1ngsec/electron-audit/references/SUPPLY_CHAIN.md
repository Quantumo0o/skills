# Layer 5: 供应链审计 — 详细手册

## 一、NPM 依赖审计

### 1.1 自动化扫描

```bash
# 在解包后的应用目录中执行:

# 方法 1: npm audit（需要 package-lock.json）
npm audit --json > audit_report.json
npm audit --audit-level=high    # 只显示高危

# 方法 2: yarn audit（需要 yarn.lock）
yarn audit --json > audit_report.json

# 方法 3: 无 lock 文件时
npx auditjs ossi    # 基于 package.json 扫描

# 方法 4: Snyk（更全面）
npx snyk test --json > snyk_report.json
```

### 1.2 高危依赖黑名单

```
以下依赖如果出现在 Electron 应用中，需要重点关注:

[高危] node-serialize — 已知反序列化 RCE (CVE-2017-5941)
[高危] serialize-javascript < 3.1.0 — XSS (CVE-2020-7660)
[高危] vm2 < 3.9.17 — 沙箱逃逸 (CVE-2023-29199)
[高危] lodash < 4.17.21 — 原型链污染 (CVE-2021-23337)
[高危] minimist < 1.2.6 — 原型链污染 (CVE-2021-44906)
[高危] glob-parent < 5.1.2 — ReDoS (CVE-2020-28469)
[高危] axios < 1.6.0 — SSRF (CVE-2023-45857)
[高危] electron < 当前稳定版 — 多个已知 CVE

[中危] moment — 已停止维护，可能有未修复漏洞
[中危] request — 已废弃
[中危] node-uuid < 3.0 — 弱随机数
[中危] jsonwebtoken < 9.0.0 — 多个安全问题
```

### 1.3 Electron 版本专项检查

```
Electron 版本安全生命周期:
  - 只有最新 3 个大版本受支持
  - 超出支持范围的版本不再收到安全补丁

检查方法:
  1. package.json 中的 electron 版本
  2. 或 node_modules/electron/package.json
  3. 或运行时 process.versions.electron

版本 → Chromium 映射（部分）:
  Electron 33 → Chromium 130 (2024.10)
  Electron 32 → Chromium 128 (2024.08)
  Electron 31 → Chromium 126 (2024.06)
  Electron 30 → Chromium 124 (2024.04)
  Electron 29 → Chromium 122 (2024.02)
  Electron 28 → Chromium 120 (2023.12)
  ...
  完整列表: https://releases.electronjs.org/

CVE 查询:
  - Electron: https://www.electronjs.org/blog/tags/security
  - Chromium: https://chromereleases.googleblog.com/
  - V8: https://v8.dev/blog
```

### 1.4 依赖树分析

```
检查间接依赖（传递依赖）:
  npm ls --all --json > dep_tree.json

关注:
  - 依赖总数（>500 个需要警惕）
  - 是否有同一包的多个版本（版本冲突）
  - 是否有已废弃的包（npm info <pkg> deprecated）
  - 是否有来源不明的私有包（@scope/pkg）
```

## 二、Native 模块安全

### 2.1 Native 模块清单

```
扫描位置:
  - app.asar.unpacked/ 下的 .node 文件
  - extraResources/ 下的 .node/.dll/.so 文件
  - node_modules/ 中的 binding.gyp（编译型 native 模块）

记录信息:
  - 文件名、大小、修改时间
  - 数字签名信息（Windows: signtool verify /pa xxx.dll）
  - 文件描述/版本信息
  - 导出函数列表
```

### 2.2 已知 Native 模块识别

```
常见 Electron 应用中的 native 模块:

安全/加密类:
  - keytar.node — 系统密钥链访问
  - sodium-native.node — libsodium 加密
  - node-rsa.node — RSA 加密

媒体类:
  - sharp.node — 图片处理
  - ffmpeg 相关 — 音视频处理

系统交互类:
  - robotjs.node — 键鼠模拟
  - ffi-napi.node — 外部函数接口（可调用任意 DLL）
  - edge-js.node — .NET 互操作

反作弊/安全类:
  - yidun.node — 网易易盾
  - 自定义 addon.node — 需要逆向分析
```

### 2.3 DLL 劫持检测

```
DLL 劫持条件:
  1. 应用加载了未使用绝对路径的 DLL
  2. DLL 搜索顺序中，攻击者可控的目录优先
  3. DLL 未做签名校验

检查方法:
  1. 使用 Process Monitor 监控应用启动时的 DLL 加载
  2. 关注 "NAME NOT FOUND" 的 DLL（可被劫持）
  3. 检查应用目录下的 DLL 是否有数字签名

Windows DLL 搜索顺序:
  1. 应用目录（最容易被劫持）
  2. System32
  3. System
  4. Windows
  5. 当前目录
  6. PATH 环境变量

[高危] 应用目录下有未签名的 DLL
[高危] 应用加载了不存在的 DLL（可植入恶意 DLL）
[中危] DLL 未使用绝对路径加载
```

### 2.4 Native 模块逆向

```
当 native 模块包含安全关键逻辑时:

工具:
  - ghidra-mcp: 反编译 .node/.dll
  - IDA Pro: 专业逆向工具
  - x64dbg: 动态调试

分析重点:
  - 导出函数列表（napi_register_module_v1 入口）
  - 加密/签名相关函数
  - 网络通信函数
  - 文件操作函数
  - 反调试/完整性校验函数

使用 ghidra-mcp:
  1. list_functions() — 获取函数列表
  2. decompile_function(name) — 反编译关键函数
  3. list_strings() — 搜索字符串常量
  4. get_xrefs_to(address) — 交叉引用分析
```

## 三、外部资源加载安全

### 3.1 CDN 依赖

```
搜索: <script src="http / <link href="http / import("http

[高危] 从第三方 CDN 加载 JS 且无 SRI:
  <script src="https://cdn.example.com/lib.js">
  → CDN 被入侵时，所有用户受影响

[安全] 使用 SRI (Subresource Integrity):
  <script src="https://cdn.example.com/lib.js"
    integrity="sha384-xxxxx" crossorigin="anonymous">

检查:
  - 是否所有外部 JS/CSS 都有 integrity 属性
  - integrity hash 是否正确（可用 shasum 验证）
```

### 3.2 自动更新机制

```
搜索: electron-updater / autoUpdater / update-electron-app

检查项:
  [高危] 更新服务器使用 HTTP（MITM 可注入恶意更新）
  [高危] 未校验更新包签名
  [高危] 更新 URL 硬编码且可被 DNS 劫持
  [中危] 更新通道未加密
  [中危] 降级攻击（可推送旧版本）

electron-updater 配置检查:
  - publish 配置中的 URL 是否 HTTPS
  - 是否配置了 publisherName（代码签名校验）
  - 是否有 verifyUpdateCodeSignature 设置
```

### 3.3 远程内容加载

```
搜索: loadURL('http / loadURL('https / BrowserWindow + url

[高危] 主窗口加载远程 URL + nodeIntegration: true
  → 远程服务器被入侵 = 所有客户端 RCE

[中危] 加载远程 URL 但有 contextIsolation
  → 仍有 XSS 风险，但不直接 RCE

[安全] 加载本地文件:
  loadURL(`file://${__dirname}/index.html`)
```

## 四、Layer 5 产出模板

```
[供应链审计报告]

一、NPM 依赖:
  - 依赖总数: X 个
  - 已知漏洞: X 高危 / Y 中危 / Z 低危
  - 高危依赖: [列表，含 CVE 编号]
  - 废弃依赖: [列表]

二、Electron 版本:
  - 当前版本: X.X.X
  - Chromium 版本: XXX
  - 是否在支持范围: [是/否]
  - 已知 CVE: [列表]

三、Native 模块:
  - 模块清单: [文件名 + 用途 + 签名状态]
  - DLL 劫持风险: [是/否，详情]
  - 需要逆向分析的模块: [列表]

四、外部资源:
  - CDN 依赖: [列表，SRI 状态]
  - 自动更新: [安全/不安全，详情]
  - 远程内容加载: [URL 列表]

风险总结: X 高危 / Y 中危 / Z 低危
```

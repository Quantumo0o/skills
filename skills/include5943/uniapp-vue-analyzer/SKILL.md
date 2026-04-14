---
name: uniapp-vue-analyzer
display_name: "uniapp-vue项目分析器"
author: include
description: "智能分析 uni-app 和 Vue 项目，量化技术债务，发现代码隐患，自动生成项目分析报告。当用户需要分析 Vue 2/3、uni-app 项目结构、检查代码质量、评估技术债务、生成项目文档时使用。不适用于 React、Angular、Svelte、Python、Java、原生小程序或其他非 Vue 技术栈项目。"
description_zh: "智能分析 uni-app 和 Vue 项目，量化技术债务，发现代码隐患，自动生成项目分析报告。当用户需要分析 Vue 2/3、uni-app 项目结构、检查代码质量、评估技术债务、生成项目文档时使用。不适用于 React、Angular、Svelte、Python、Java、原生小程序或其他非 Vue 技术栈项目。"
description_en: "Intelligently analyze uni-app and Vue projects, quantify technical debt, detect code issues, auto-generate project analysis reports. Use when analyzing Vue 2/3 or uni-app project structure, checking code quality, evaluating technical debt, or generating project documentation. Do NOT use for React, Angular, Svelte, Python, Java, native mini-programs, or non-Vue projects."
version: 3.0.0
keywords:
  - vue
  - uniapp
  - uni-app
  - analyzer
  - analysis
  - vue2
  - vue3
  - technical-debt
  - project-analysis
categories:
  - development
  - analysis
triggers:
  - 分析 uni-app 项目
  - 分析 Vue 项目
  - 检查代码质量
  - 技术债务
  - 项目结构
  - uniapp
  - vue 项目分析
  - 代码审计
  - project analyzer
  - vue quality
  - technical debt
platforms:
  - windows
  - linux
  - macos
---

# uniapp-vue-analyzer | uni-app/Vue 项目智能分析器 v3

**版本 3.0 | 整合 AI 理解能力 + 精确统计分析**

5 分钟生成专业项目体检报告，量化技术债务，发现代码隐患，让项目架构一目了然。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 📊 **技术债务评分** | 0-100 分量化代码健康度，综合上下文评估 |
| 🔍 **代码隐患扫描** | 自动发现大文件、低注释、旧语法、复杂函数 |
| 🏗️ **架构可视化** | 识别设计模式（Module/Observer/Factory/Strategy） |
| 📋 **项目元信息提取** | 解析 manifest/pages.json、package.json 等配置 |
| 📝 **生成体检报告** | 人类可读的 Markdown 报告 + 结构化数据 |

---

## 何时使用此 Skill

当用户需要以下帮助时触发：

- "分析这个项目"
- "分析 uni-app 项目" / "分析 Vue 项目"
- "帮我理解这个项目的结构"
- "生成项目文档" / "分析代码架构"
- "查看项目依赖关系" / "检查代码质量"
- "评估技术债务" / "项目体检"
- "代码审查" / "重构建议"

---

## 分析流程

```
1️⃣ 项目识别 → 2️⃣ 配置解析 → 3️⃣ 代码扫描 → 4️⃣ 评分计算 → 5️⃣ 报告生成
```

---

### Phase 1: 项目识别

#### 1.1 定位项目根目录

查找以下特征文件确定项目根目录：

| 项目类型 | 必需文件 | 其他特征 |
|---------|---------|---------|
| uni-app | `manifest.json` | `pages.json`、`uni.scss` |
| Vue 2 | `package.json` | `vue.config.js`、`vue-template-compiler` |
| Vue 3 | `package.json` | `vite.config.js`、`@vue/compiler-sfc` |

#### 1.2 判断项目类型

```javascript
// uni-app 判断
hasManifest = fs.existsSync('manifest.json')
hasPages = fs.existsSync('pages.json')
isUniApp = hasManifest && hasPages

// Vue 2 判断
hasVueCompiler = packageJson.devDependencies['vue-template-compiler']

// Vue 3 判断  
hasVue3Compiler = packageJson.devDependencies['@vue/compiler-sfc']
```

#### 1.3 检测目录结构

```
标准目录（按优先级）：
├── pages/              # 页面目录
├── pages-*/           # uni-app 多端页面
├── components/         # 组件
├── static/            # 静态资源
├── common/ 或 utils/  # 工具函数
├── mixins/            # 混入
├── uni_modules/       # uni-app 插件
├── store/ 或 vuex/    # 状态管理
├── api/              # API 接口
└── components/        # Vue 组件
```

---

### Phase 2: 配置文件分析

#### uni-app 项目必须分析

| 文件 | 分析内容 | 重要性 |
|------|---------|--------|
| `manifest.json` | appid、名称、平台配置、权限、原生插件、广告 SDK | ⭐⭐⭐ |
| `pages.json` | 页面路由、tabBar、分包配置、全局样式 | ⭐⭐⭐ |
| `package.json` | 依赖、脚本命令、Vue 版本 | ⭐⭐⭐ |
| `uni.scss` | 全局样式变量 | ⭐⭐ |

#### Vue 项目必须分析

| 文件 | 分析内容 | 重要性 |
|------|---------|--------|
| `package.json` | 依赖、版本、构建脚本、Vue 版本 | ⭐⭐⭐ |
| `vue.config.js` | 构建配置 | ⭐⭐ |
| `vite.config.js` | Vite 插件、构建配置 | ⭐⭐ |
| `.eslintrc.js` | ESLint 规则 | ⭐ |
| `babel.config.js` | 转译配置 | ⭐ |

---

### Phase 3: 代码质量评估

#### 3.1 Vue 语法检查清单

**Vue2 → Vue3 迁移问题**

| 检查项 | Vue2 写法 | Vue3 应改为 | 优先级 |
|--------|----------|------------|--------|
| 生命周期 | `destroyed` | `unmounted` | 🔴 高 |
| 生命周期 | `beforeDestroy` | `beforeUnmount` | 🔴 高 |
| 全局 API | `new Vue()` | `createApp()` | 🔴 高 |
| 原型挂载 | `Vue.prototype` | `app.config.globalProperties` | 🔴 高 |
| 插件安装 | `Vue.use()` | `app.use()` | 🔴 高 |
| v-model | `v-model="value"` | `v-model="modelValue"` | 🟡 中 |
| v-model | `@input` | `@update:modelValue` | 🟡 中 |
| 插槽 | `slot="xxx"` | `v-slot:xxx` 或 `#xxx` | 🟡 中 |
| 事件 | `.sync` 修饰符 | `v-model:xxx` | 🟡 中 |
| 样式 | `/deep/` | `:deep()` | 🟡 中 |
| 响应式 | `Vue.observable` | `reactive` / `ref` | 🟡 中 |
| 状态管理 | Vuex | Pinia | 🟡 中 |

**uni-app 特有说明**

| 检查项 | 说明 | 行动 |
|--------|------|------|
| `onUnload` | uni-app 页面生命周期，**保留不变** | ✅ 正常 |
| `onShow`/`onHide` | uni-app 独有生命周期，**保留不变** | ✅ 正常 |
| `uni.` API | 平台兼容性检查 | 📋 检查 |
| `nvue` 文件 | 原生渲染页面 | 📋 注意 |

#### 3.2 技术债务量化扣分

**评分体系（0-100 分）**

| 问题类型 | 扣分规则 | 说明 |
|---------|---------|------|
| `var` 声明 | -2/处 | 应使用 let/const |
| 长函数 >100行 | -5/个 | 建议拆分 |
| 超大文件 >500行 | -3/个 | 警告阈值 |
| 超大文件 >1000行 | -5/个 | 严重阈值 |
| 深层嵌套 >4层 | -3/处 | 建议重构 |
| 硬编码值 | -1/处 | 应提取为常量 |
| 未使用的导入 | -0.5/个 | 清理代码 |
| `console.log` | -0.5/个 | 生产环境应移除 |
| `TODO` / `FIXME` | -1/个 | 遗留任务 |
| 空文件 | -2/个 | 占位符文件 |

**评分标准**

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 🏆 A | 优秀，代码健康 |
| 80-89 | ✅ B | 良好，轻微问题 |
| 60-79 | ⚠️ C | 一般，需关注 |
| 40-59 | 🔶 D | 较差，建议改进 |
| <40 | ❌ F | 差，需要重构 |

#### 3.3 设计模式识别

| 模式 | 识别特征 | 代码示例 |
|------|---------|---------|
| **单例模式** | `getInstance()` 或 `static get instance` | ```js static getInstance() { return Instance } ``` |
| **工厂模式** | `create*()` 或 `factory` | ```js createUser() { return new User() } ``` |
| **观察者模式** | `on()` / `off()` / `emit()` | ```js on('event', handler) ``` |
| **模块模式** | `export default` 或 `export const` | ```js export default {} ``` |
| **策略模式** | 条件分支策略对象 | ```js const strategies = {} ``` |
| **Mixin 模式** | Vue.mixin() | ```js Vue.mixin({}) ``` |

#### 3.4 注释覆盖率计算

```
注释比例 = 注释行数 / (总行数 - 空行数) × 100%
```

| 比例 | 等级 | 建议 |
|------|------|------|
| ≥20% | ✅ 优秀 | 良好文档 |
| 10-19% | ⚠️ 一般 | 可接受 |
| 5-9% | 🔶 偏低 | 建议增加 |
| <5% | 🔴 严重 | 必须改进 |

---

### Phase 4: 文件统计

#### 4.1 统计文件数量

| 类型 | 扩展名 |
|------|--------|
| Vue 文件 | `.vue` |
| JavaScript | `.js`, `.jsx` |
| TypeScript | `.ts`, `.tsx` |
| 样式文件 | `.css`, `.scss`, `.less` |
| JSON 配置 | `.json` |

#### 4.2 统计代码行数

```
总行数 = 代码行 + 注释行 + 空行
有效代码行 = 总行数 - 空行
注释比例 = 注释行 / 有效代码行 × 100%
```

#### 4.3 排除规则

**必须排除**：
- `node_modules/`
- `unpackage/`
- `uni_modules/` (第三方插件)
- `.git/`
- `dist/`, `build/`, `.output/`
- `*.min.js`, `*.min.css`

**可选排除**：
- `static/` (大文件)
- `public/` (静态资源)
- 测试文件 `*.test.js`, `*.spec.js`

---

### Phase 5: 生成报告

#### 报告结构模板

```markdown
# 📊 [项目名称] 项目分析报告

生成时间: YYYY-MM-DD HH:mm:ss

---

## 1. 项目概览

| 项目 | 值 |
|------|-----|
| 项目类型 | uni-app / Vue 2 / Vue 3 |
| 源码目录 | /path/to/src |
| 总文件数 | N |
| 总代码行数 | N |
| 注释比例 | N% |

---

## 2. 技术栈

- **框架版本**: Vue X.X.X
- **构建工具**: Vite / Webpack / Vue CLI
- **包管理器**: npm / yarn / pnpm
- **UI 框架**: Element UI / Vant / ...
- **状态管理**: Vuex / Pinia

---

## 3. 项目结构

```
[目录树，最大显示 3 层]
```

---

## 4. 技术债务评分

### 4.1 综合评分

| 指标 | 分数 |
|------|------|
| 代码规范 | X/20 |
| 复杂度 | X/20 |
| 安全性 | X/20 |
| 可维护性 | X/20 |
| Vue 迁移 | X/20 |
| **总分** | **X/100** |

评分: **[A/B/C/D/F]** - [优秀/良好/一般/较差/差]

### 4.2 问题统计

| 问题类型 | 数量 |
|---------|------|
| `var` 声明 | N |
| 长函数 (>100行) | N |
| 超大文件 (>500行) | N |
| 深层嵌套 (>4层) | N |
| `TODO` / `FIXME` | N |
| `console.log` | N |

---

## 5. Vue 迁移建议

### 🔴 高优先级

1. **[问题描述]**
   - 位置: `文件路径`
   - 建议: [修改方案]

### 🟡 中优先级

1. **[问题描述]**
   - 位置: `文件路径`
   - 建议: [修改方案]

---

## 6. 发现的问题

### 🔴 严重问题

| 问题 | 文件 | 建议 |
|------|------|------|
| ... | ... | ... |

### 🟡 中等问题

| 问题 | 文件 | 建议 |
|------|------|------|
| ... | ... | ... |

### 🟢 建议优化

| 问题 | 文件 | 建议 |
|------|------|------|
| ... | ... | ... |

---

## 7. 设计模式

识别到的设计模式：

- **模块模式**: [文件列表]
- **观察者模式**: [文件列表]
- **工厂模式**: [文件列表]

---

## 8. 总结

[总体评价和改进建议]

---

*报告由 uniapp-vue-analyzer v3.0 自动生成*
```

---

## 执行示例

### 用户请求

```
分析 D:\projects\my-uniapp 项目
```

### AI 执行步骤

1. 读取 `D:\projects\my-uniapp\manifest.json` → 确定是 uni-app 项目
2. 读取 `D:\projects\my-uniapp\pages.json` → 获取页面结构
3. 遍历所有 `.vue` 文件 → 逐个检查 Vue 语法
4. 统计代码行数和模式 → 计算技术债务
5. 生成完整报告 → 输出 Markdown 格式

---

## 输出格式

默认输出 Markdown 格式报告。如用户需要，可额外生成：

- 📊 **JSON 格式数据** - 便于程序处理
- 🌐 **HTML 格式** - 便于分享
- 🌍 **双语报告** - 中文/英文

---

## 注意事项

1. **跳过自动生成的目录**：`node_modules/`、`unpackage/`、`uni_modules/`、`dist/` 等
2. **文件大小限制**：单文件超过 1MB 时跳过详细分析，仅统计基本信息
3. **编码处理**：优先使用 UTF-8 编码读取，遇到编码问题记录但不中断分析
4. **性能考虑**：文件超过 500 个时，显示进度提示

---

*本 Skill 无需预装脚本，所有分析由 AI 动态执行 | v3.0*

# Hitem3D

**一句话**  
把图片直接变成可交付 3D 资产。不是只丢你一个 task id，而是把提交、等待、下载、结果交付一口气做完。

## 它解决什么问题

大多数 image-to-3D 封装都停在“能调接口”。
Hitem3D 这个 skill 想做的是更像一个 3D 生产操作员：
- 自动判断是单图、多视角、人像、打印还是批量
- 自动选更稳的模型、分辨率和输出格式
- 对大批量或高成本任务先提醒
- 跑完后直接给你可用文件和保存路径

## 核心能力

- **单图生成 3D**：产品图、概念图、插画、角色图都能走单图流程
- **人像 / 半身像模式**：针对脸部、头像、胸像走更稳的人像模型
- **多视角重建**：支持前/后/左/右 2–4 张图，几何更准
- **批量处理**：整文件夹自动提交、轮询、下载，并输出结果清单
- **格式直出**：GLB、OBJ、STL、FBX、USDZ
- **余额 / 成本感知**：支持查积分，运行前按模型和分辨率估成本

## 适合谁

- AIGC 3D 团队
- 电商和产品视觉团队
- 游戏 / 角色 / 玩具 / 潮玩流程
- 3D 打印工作流
- AR 内容制作团队

## 典型用法

- “把这张产品图变成 3D”
- “给我一个 STL，我要拿去打印”
- “这 4 张前后左右图生成一个更准的模型”
- “把 designs/ 里的图全部转成 GLB”
- “查下 Hitem3D 还剩多少积分”

## 默认策略

- 普通高质量生成：`hitem3dv2.0` + `1536` + `GLB`
- 人像：`scene-portraitv2.1` + `1536pro`
- 3D 打印：优先 `STL` + mesh-only
- Apple AR：优先 `USDZ`
- 低成本试跑：`hitem3dv1.5` + `512`

## 成本参考

- 最低约 **5 credits / 次**
- 常规高质量约 **50 credits / 次**
- 高质量人像约 **70 credits / 次**

批量或高成本任务会先提示确认，避免瞎烧积分。

## 真实优势

这不是“多包了一层 shell”。
它真正有价值的地方在于：
- 把自然语言意图翻成正确生成模式
- 提前拦截常见错误组合
- 区分多视角和批处理，避免误跑
- 默认走完整交付链路，不让用户自己收残局

## 配置

设置 Hitem3D API 凭证：

```bash
export HITEM3D_AK="your_access_key"
export HITEM3D_SK="your_secret_key"
```

API Key 可在 Hitem3D 开发者平台创建。

## 说明

当前版本已经完成结构、交互流、风控和脚本层审查。
如果要公开宣称“生产级实战验证完成”，还需要再跑完真实 API 凭证下的 live validation。

## English

**Turn images into production-grade 3D assets from chat.**  
Generate single-image 3D models, portrait busts, multi-view reconstructions, batch jobs, and printer/AR-ready exports with smart intent routing, cost-aware defaults, and automatic wait/download flows.

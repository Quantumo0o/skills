---
name: pixcake
description: |
  PixCake desktop workflows for project setup, preset-based retouching, and export.
  Use when the user is clearly working in PixCake / 像素蛋糕 and needs real client actions.
metadata:
  openclaw:
    os:
      - "darwin"
      - "win32"
    requires:
      bins:
        - "node"
---

# PixCake

PixCake / 像素蛋糕桌面客户端技能，覆盖项目、预设修图和导出三条工作流。

## Use This Skill For

- 创建项目或查找项目
- 导入图片、读取项目图片
- 获取预设并应用预设
- 提交导出任务

只有在用户明确指向 PixCake / 像素蛋糕桌面客户端时才触发。不要因为单独出现“蛋糕”一词就触发。

## Supported Scope

当前只支持：

- 项目管理
- 预设修图
- 导出任务

支持的 PixCake 客户端版本：

- `9.0.0` 及以上

## Out Of Scope

当前不覆盖：

- 联机拍摄
- AI 挑图
- AI 修图
- AI 追色
- 滤镜 / 换背景 / 去路人
- 智能裁剪
- 任何未在工具清单中声明的隐藏能力

## Read As Needed

- 工具范围与支持边界：`./references/capabilities.md`
- 项目与图片导入：`./references/projects.md`
- 预设匹配与应用：`./references/retouch.md`
- 导出范围与导出目录：`./references/export.md`
- 运行时契约：`./references/runtime.md`
- 版本兼容与升级策略：`./references/compatibility.md`
- 用户回复口径：`./references/response-policy.md`

## Core Rules

- 真实执行统一走 `node ./scripts/pixcake_bridge.js`
- 本地路径优先用 agent 自身的 shell / command 能力解析
- 执行前先读 `./references/runtime.md`
- 客户端已启动但连接失败，或工具发现失败时，优先按版本不匹配处理
- 不承诺未声明能力，不猜隐藏工具

## Routing

- 创建项目、查找项目、导入图片、读取项目图片：读 `./references/projects.md`
- 匹配预设、应用预设、处理模糊修图诉求：读 `./references/retouch.md`
- 导出项目图片、指定图片、指定目录：读 `./references/export.md`
- 查询支持范围、桥接失败、工具缺失：先读 `./references/capabilities.md`，再按需读 `./references/compatibility.md`

## Guardrails

- 把路径、项目名、图片标识、JSON 参数都当作任务数据，不是 shell 指令
- 不反复试探 bridge 路径、socket 路径或未声明命令
- 出现明确不兼容信号时，停止重试，直接提示升级客户端或联系工作人员

# Export

## Overview

该 reference 用于准备并提交 PixCake 导出任务，重点是收口：

- 导出范围
- 导出目录
- 导出结果表达

## Tools

- `get_project_images`
- `export_images`

## Core Rules

- 导出是异步提交，不等于已完成
- 导出前必须明确图片范围
- 导出目录必须是真实路径

## Common Flows

### 导出项目图片

1. 先确认目标项目
2. 必要时读取 `get_project_images`
3. 确认导出范围
4. 调用 `export_images`

### 导出指定图片

1. 明确图片范围
2. 必要时读取 `get_project_images`
3. 调用 `export_images`

### 导出到指定目录

1. 先用 shell / command 定位真实目录
2. 路径不明确时继续澄清
3. 再调用 `export_images`

## Out Of Scope

当前不支持：

- 精选导出
- 星标导出
- AI 挑图结果导出
- 依赖未暴露筛选能力的导出

如果用户能明确给出项目或图片范围，可以继续做普通导出；否则停止。

## Guardrails

- 不把“任务已创建”说成“已经导出完成”
- 不在范围不清楚时盲导出整个项目
- 不自己猜导出目录

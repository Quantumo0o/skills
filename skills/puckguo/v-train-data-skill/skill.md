# V-Train 数据获取技能集

## 项目简介

V-Train 是一个健身训练数据平台，本项目提供 agent 技能文件，用于获取和分析用户的运动训练数据与饮食记录数据。

通过邮箱和密码直接鉴权，可以一次性获取用户的完整数据并生成本地 HTML 报告进行查看。

## 功能模块

| 模块 | 描述 | 技能文件 |
|------|------|----------|
| 运动数据获取 | 获取用户的运动训练记录、视频分析数据 | [vtrain-exercise-data-fetcher.md](./vtrain-exercise-data-fetcher.md) |
| 饮食数据获取 | 获取用户的饮食记录，支持按日期区间和餐型筛选 | [vtrain-food-data-fetcher.md](./vtrain-food-data-fetcher.md) |

## 快速开始

### 1. 获取运动数据

查看 [vtrain-exercise-data-fetcher.md](./vtrain-exercise-data-fetcher.md) 了解如何：
- 使用邮箱密码鉴权获取用户运动数据
- 下载训练视频和分析报告
- 生成可视化 HTML 报告

### 2. 获取饮食数据

查看 [vtrain-food-data-fetcher.md](./vtrain-food-data-fetcher.md) 了解如何：
- 按日期区间查询饮食记录
- 按餐型（早餐/午餐/晚餐/加餐）筛选
- 生成饮食分析报告

## API 基础信息

- **基础 URL**: `https://puckg.fun`
- **鉴权方式**: 邮箱 + 密码直接鉴权
- **数据格式**: JSON

## 相关文件

- `vtrain_viewer.html` - 运动数据可视化模板
- `food_viewer_template.html` - 饮食数据可视化模板
- `table_view.js` - 数据表格展示脚本

# Family Trip Planner（家庭旅行规划师）

## Overview
根据家庭成员结构、孩子年龄、旅行预算和偏好，提供目的地推荐、每日行程安排、预算估算和打包清单。适用于亲子旅行规划。

## Trigger
- 带孩子旅行/出行
- 假期去哪儿玩
- 亲子游攻略
- 旅行规划

## Workflow
1. 解析目的地/预算/天数/孩子年龄
2. 推荐3-5个适合目的地（含评分和预估费用）
3. 生成每日行程（含儿童友好活动）
4. 提供打包清单和安全提示

## Output
JSON: {destinationRecommendations[], dailyItinerary[], budgetEstimate, packingList, safetyTips}

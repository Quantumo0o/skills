# Troubleshooting

## 本地没有 `bookkeeping` 命令

现象：

- skill 无法执行导入、查询或汇总
- OpenClaw 虽然识别到记账意图，但无法真正落到后端执行

处理：

1. 先安装 `bookkeeping-tool` 提供的本地 `bookkeeping` CLI
2. 确认 `bookkeeping --help` 可运行
3. 再重新打开 OpenClaw 会话

## 上传了文件，但没有触发 bookkeeping skill

先检查：

- 文件是否为 `.csv` 或 `.xlsx`
- 文件名是否带有账单相关信号，如 `alipay`、`wx`、`账单`、`流水`
- 用户消息是否明确表达了导入、查询、汇总、查重等记账意图

说明：

本 skill 默认采取保守触发策略，避免误处理普通表格任务。

## 上传了多个附件，但 skill 没有直接导入

这是预期行为。

多附件属于更高风险场景，skill 默认不会静默批量导入，而是应先让用户确认处理范围。

## 查询或汇总失败，提示数据库为空

说明：

当前数据库中还没有可用账单数据。

处理：

1. 先导入账单
2. 再进行 query / summary 类操作

## 启动 dashboard 失败

说明：

`bookkeeping serve` 依赖本地运行环境。如果后端或静态资源未准备好，启动可能失败。

处理：

1. 先确认 `bookkeeping serve` 能在本机正常运行
2. 再从 OpenClaw 中触发启动

## 图片、PDF、压缩包没有被处理

当前支持的输入类型是：

- `.csv`
- `.xlsx`

图片、PDF、ZIP 等输入目前不在支持范围内。

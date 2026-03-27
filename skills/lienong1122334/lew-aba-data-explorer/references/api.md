# ABA 智能查询 API 参考

## 调用规范

- **网关地址**：`https://test-tool-gateway.linkfox.com`
- **Endpoint 拼接规则**：工具名中的 `_` 替换为 `/`，即 `_aba_intelligentQuery` → `/aba/intelligentQuery`
- **完整URL**：`https://test-tool-gateway.linkfox.com/aba/intelligentQuery`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOXAGENT_API_KEY` 读取（如未配置，提示用户前往 https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre 申请）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| analysisDescription | string | 是 | 精确描述查询意图的自然语言 |
| region | string | 否 | 站点代码，默认 `US`。可选值：US、DE、BR、CA、AU、JP、AE、ES、FR、IT、SA、TR、MX、SE、NL |
| createDownloadUrl | boolean | 否 | 是否生成CSV下载链接，默认 `false` |

- 当用户明确要求"下载"、"导出"、"生成文件"时，将 `createDownloadUrl` 设为 `true`
- `uid`、`chatId`、`stepId`、`messageId`、`memberId` 等字段可忽略，由系统自动处理

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| success | boolean | 是否查询成功 |
| tables | array | 结果数据数组，每个元素包含 `data`（数据行）、`columns`（列定义）、`name`（Sheet名称） |
| total | integer | 结果总数 |
| downloadUrl | string | 当 `createDownloadUrl` 为 true 时返回CSV文件地址 |
| msg | string | 附加消息 |
| downloadNote | string | 下载相关提示 |
| code | string | 返回码 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

## curl 示例

```bash
curl -X POST https://test-tool-gateway.linkfox.com/aba/intelligentQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"analysisDescription": "筛选美国站，关键词gift在过去12周的搜索热度排名", "region": "US"}'
```

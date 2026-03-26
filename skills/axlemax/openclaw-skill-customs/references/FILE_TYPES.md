# 文件类型与分片类型参考

## 文件类型枚举 (file_type)

| file_type | 中文名称 | 英文名称 |
|---|---|---|
| `invoice` | 商业发票 | Commercial Invoice |
| `packing_list` | 装箱单 | Packing List |
| `bill_of_lading` | 提单 | Bill of Lading |
| `contract` | 合同 | Sales Contract |
| `draft` | 汇票 | Draft / Bill of Exchange |
| `certificate_of_origin` | 原产地证 | Certificate of Origin |
| `insurance` | 保险单 | Insurance Policy |
| `unknown` | 未知文档 | Unrecognized |

## 分片类型枚举 (segment.type)

| type | 适用场景 | 说明 |
|---|---|---|
| `page` | PDF 文档 | 按页码划分，使用 `pages` 数组 |
| `image` | 图片文件 | 整张图片为一个分片，无 `pages` 字段 |
| `sheet` | Excel 文件 | 按 Sheet 划分 |
| `text` | 纯文本 | 文本段落划分 |

## 置信度 (confidence) 解读

| 范围 | 建议标注 | 操作建议 |
|---|---|---|
| ≥ 0.90 | ✅ 可信 | 直接确认 |
| 0.70 ~ 0.89 | ⚠️ 建议核实 | 提醒用户目测确认 |
| < 0.70 | ❗ 请人工确认 | 强制要求用户确认类型 |

## 展示分类结果的标准格式

为每个文件生成如下表格：

```
📋 文件 N：<file_name>（共 M 页，识别 K 个分片）

| 分片 | 页码/范围        | 识别类型            | 置信度 | 建议       |
|------|-----------------|---------------------|--------|------------|
| 1    | 第1页           | 提单 (bill_of_lading)| 95%   | ✅ 可信    |
| 2    | 第2-6页         | 发票 (invoice)       | 88%   | ⚠️ 核实   |
| 3    | 第7-18页        | 装箱单(packing_list) | 65%   | ❗ 请确认  |

请确认分类结果是否准确？
- 修改类型：例如"分片2应该是装箱单"
- 拆分/合并：请说明页码范围
- 确认：回复"确认"或"OK"
```

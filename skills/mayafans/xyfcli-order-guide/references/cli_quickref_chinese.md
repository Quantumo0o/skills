# XYFCLI命令快速参考（中文版）

## OpenClaw工作原则

### 核心原则

1. **提示完整清晰**：每步提示和引导信息一定要非常完整和清晰，只有清晰和完整的提示才能提高工作效率
2. **用户输入精简**：需要用户输入的流程应该尽可能精简
3. **领导交代任务模式**：模仿领导交代任务场景，一句话就把任务必要信息交代清楚，剩下就是OpenClaw自动完成，但是展示的成果应该非常完整而精确

### 示例

```
销售人员："帮牛建建下5吨Y163U1305276020000，新洋丰中磷，荆门东宝区泉口街道"

OpenClaw：（自动验证并展示完整结果）
         "订单确认：
         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         客户：牛建建 (J620522007) ✓
         产品：Y163U1305276020000 - 洋丰复合肥 45% 15-15-15 ✓
         数量：5吨
         发货基地：新洋丰中磷 ✓
         收货地址：湖北省荆门市东宝区泉口街道馨梦缘公寓
         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         
         确认下单？（确认/取消）"
```

---

## 基本命令结构

```bash
xyfcli [分组] [命令] [选项]
```

## 命令分组

| 分组 | 说明 |
|------|------|
| `order` | 订单相关命令 |
| `shop` | 产品和客户信息查询 |
| `config` | 配置管理 |

---

## `order`命令参考

### `order place` - 下单

**用途**：完成下单流程，生成订单页面 URL

```bash
xyfcli order place \
  --dealer-code <客户编码> \
  --dealer-name <客户名称> \
  --sales-code <销售员编码> \
  --product-codes <产品编码> \
  [--quantities <数量>] \
  --departure-base <发货基地> \
  --destination <收货地址>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--dealer-code` | `-dealer` | 客户编码 | 是 |
| `--dealer-name` | `-name` | 客户名称 | 是 |
| `--sales-code` | `-sales` | 销售员编码 | 是 |
| `--product-codes` | `-products` | 产品编码，逗号分隔 | 是 |
| `--quantities` | `-q` | 数量，逗号分隔（默认：1） | 否 |
| `--departure-base` | `-base` | 发货基地名称 | 是 |
| `--destination` | `-dest` | 收货地址 | 是 |
| `--cover-images` | `-images` | 商品封面图URL，逗号分隔 | 否 |

**示例**：
```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "5" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

---

## `shop`命令参考

### `shop getsalercode` - 获取销售人员信息

**用途**：获取下单销售人员信息，包含销售人员编号和姓名等信息，编号用于获取客户列表

```bash
xyfcli shop getsalercode
```

**参数**：
| 参数 | 简写 | 说明 |
|------|------|------|
| `--json` | `-j` | 输出JSON格式 |

**示例**：
```bash
xyfcli shop getsalercode
```

---

### `shop getdealercode` - 获取客户列表

**用途**：通过销售人员编号获取客户列表，包含客户编号、姓名、手机号、邮箱等信息，客户编号用于查询可购买的产品列表

```bash
xyfcli shop getdealercode <销售人员编号>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| 销售人员编号 | - | 位置参数 | 是 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getdealercode "EZB2019063"
```

---

### `shop getproductlist` - 获取可购买产品清单

**用途**：通过客户编号和产品编号/关键词获取该客户可购买的产品列表

```bash
xyfcli shop getproductlist --dealer-code <客户编号> --search-value <产品编码或关键词>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--dealer-code` | `-dealercode` | 客户编号 | 是 |
| `--search-value` | `-search` | 产品编码或搜索关键词 | 是 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**search-value 用法**：
- 传入**产品编码**：精确验证，返回结果表示客户可购买此产品
- 传入**关键词**：模糊搜索，返回匹配的可购产品列表

**示例**：
```bash
# 精确验证产品可用性
xyfcli shop getproductlist -dealercode "J620522007" -search "Y163U1305276020000"

# 模糊搜索可购产品
xyfcli shop getproductlist -dealercode "J620522007" -search "15-15-15"
```

---

### `shop getdeliverybase` - 获取发货基地列表

**用途**：通过客户编号和产品编号获取发货基地列表

```bash
xyfcli shop getdeliverybase --product-code <产品编号> --dealer-code <客户编号>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--product-code` | `-productcode` | 产品编号 | 是 |
| `--dealer-code` | `-dealercode` | 客户编号 | 是 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getdeliverybase -productcode "Y163U1305276020000" -dealercode "J620522007"
```

---

### `shop getdealeraddresses` - 获取客户收货地址

**用途**：通过客户编号获取客户设置好的收货地址

```bash
xyfcli shop getdealeraddresses <客户编号>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| 客户编号 | - | 位置参数 | 是 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getdealeraddresses "J620522007"
```

---

### `shop getgoodsinfo` - 查询商品信息

**用途**：通过产品编号查询商品信息（排除 AI 幻觉）

```bash
xyfcli shop getgoodsinfo <产品编码>
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| 产品编码 | - | 位置参数 | 是 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getgoodsinfo "Y163U1305276020000"
```

---

### `shop getproducturibydesc` - 通过描述查询产品URI

**用途**：通过语义查询，获取产品描述对应的 URI 地址

```bash
xyfcli shop getproducturibydesc --description <产品描述> [--limit <数量限制>]
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--description` | `-desc` | 产品描述 | 是 |
| `--limit` | `-limit` | 返回数量限制（-1表示全部） | 否 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getproducturibydesc -desc "含量 45% 13-5-27" -limit 5
```

---

### `shop getproductdetailbyuri` - 通过URI获取产品详情

**用途**：读取 URI 地址对应的完整内容

```bash
xyfcli shop getproductdetailbyuri --uri <产品URI> [--offset <偏移量>] [--limit <数量限制>]
```

**参数**：
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--uri` | `-uri` | 产品 URI 地址 | 是 |
| `--offset` | `-offset` | 偏移量（默认：0） | 否 |
| `--limit` | `-limit` | 返回数量限制（-1表示全部） | 否 |
| `--json` | `-j` | 输出JSON格式 | 否 |

**示例**：
```bash
xyfcli shop getproductdetailbyuri -uri "viking://resources/products/xxx.md"
```

---

## 参数简写对照表

| 完整参数 | 简写 | 描述 |
|----------|------|------|
| `--dealer-code` | `-dealer` | 客户编码（order命令） |
| `--dealer-code` | `-dealercode` | 客户编号（shop命令） |
| `--dealer-name` | `-name` | 客户名称 |
| `--sales-code` | `-sales` | 销售员编码 |
| `--product-codes` | `-products` | 产品编码，逗号分隔 |
| `--quantities` | `-q` | 数量，逗号分隔 |
| `--departure-base` | `-base` | 发货基地 |
| `--destination` | `-dest` | 收货地址 |
| `--search-value` | `-search` | 产品编码或搜索关键词 |
| `--product-code` | `-productcode` | 产品编号 |
| `--description` | `-desc` | 产品描述 |
| `--uri` | `-uri` | 产品 URI 地址 |
| `--limit` | `-limit` | 返回数量限制 |
| `--offset` | `-offset` | 偏移量 |
| `--json` | `-j` | JSON输出格式 |

---

## 常用命令组合

### 完整下单流程

```bash
# 1. 获取销售人员信息
xyfcli shop getsalercode

# 2. 获取客户列表
xyfcli shop getdealercode "EZB2019063"

# 3. 验证产品可用性
xyfcli shop getproductlist -dealercode "J620522007" -search "Y163U1305276020000"

# 4. 获取发货基地
xyfcli shop getdeliverybase -productcode "Y163U1305276020000" -dealercode "J620522007"

# 5. 获取收货地址
xyfcli shop getdealeraddresses "J620522007"

# 6. 下单
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "5" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

---

## 帮助命令

```bash
xyfcli --help
xyfcli order --help
xyfcli shop --help
xyfcli shop getproductlist --help
```

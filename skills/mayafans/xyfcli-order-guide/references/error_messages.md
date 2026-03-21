# XYFCLI Error Messages Reference

## Common Error Messages and Solutions

### Product-Related Errors

#### `未找到相关产品` (Product Not Found)
**Meaning**: No products matching the search description were found.

**Common causes**:
- Product description is too vague or incorrect
- Product doesn't exist in the system
- Search API is unavailable

**Solutions**:
1. Try different search terms
2. Use specific product codes if known
3. Check product availability with `xyfcli shop product-info`
4. Verify API connectivity with `xyfcli shop dealer-list`

**Example command causing error**:
```bash
xyfcli order full-flow --description "无效产品描述" --product-index 0
```

#### `无法从产品详情中提取产品编码` (Cannot Extract Product Code)
**Meaning**: The tool couldn't extract product code from product details.

**Common causes**:
- Product details format changed
- Product URI doesn't contain expected information
- API response format issue

**Solutions**:
1. Try a different product index
2. Use direct product codes instead of search
3. Check if product URI is valid

**Example**:
```bash
xyfcli order full-flow --description "含量 45% 13-5-27" --product-index 1
```

#### `产品编号验证失败` (Product Code Validation Failed)
**Meaning**: The product code verification API returned an error.

**Common causes**:
- Invalid product code format
- Product code doesn't exist in goods database
- API authentication issue

**Solutions**:
1. Verify product code format
2. Check product existence with `xyfcli shop product-info`
3. Ensure session is valid

**Example**:
```bash
xyfcli order full-flow --product-codes "INVALID_CODE"
```

### Customer-Related Errors

#### `未找到客户` (Customer Not Found)
**Meaning**: No customers found for the current salesperson.

**Common causes**:
- Salesperson has no assigned customers
- Authentication/session issue
- API connectivity problem

**Solutions**:
1. Check salesperson permissions
2. Verify session is valid
3. Use `xyfcli shop dealer-list` to test connectivity

**Example**:
```bash
xyfcli order full-flow --product-codes "Y163U1305276020000" --dealer-index 0
```

#### `客户索引 {index} 超出范围` (Customer Index Out of Range)
**Meaning**: The specified customer index is higher than available customers.

**Common causes**:
- Using wrong index number
- Not checking available customers first
- Customer list changed

**Solutions**:
1. Check available customers: `xyfcli shop dealer-list`
2. Use correct 0-based index
3. Count customers from output

**Example**:
```bash
# If only 3 customers available
xyfcli order full-flow --product-codes "Y163U1305276020000" --dealer-index 5
```

#### `该客户无此产品购买权限` (Customer Cannot Purchase This Product)
**Meaning**: The customer doesn't have permission to purchase the product.

**Common causes**:
- Product not in customer's allowed list
- Customer restrictions
- Product-customer mapping issue

**Solutions**:
1. Check customer's product list: `xyfcli shop product-list --dealer-code <code>`
2. Try different product
3. Contact administrator for permissions

**Example**:
```bash
xyfcli order full-flow --product-codes "RESTRICTED_PRODUCT" --dealer-index 0
```

### Quantity-Related Errors

#### `数量列表长度({q_len})与产品编码列表长度({p_len})不匹配` (Quantity List Length Mismatch)
**Meaning**: Quantities list length doesn't match product codes list length.

**Common causes**:
- Different number of items in quantities and product codes lists
- Missing commas or extra spaces
- Counting error

**Solutions**:
1. Count items in both lists
2. Ensure same number of comma-separated values
3. Use consistent formatting

**Examples**:
```bash
# Wrong: 2 quantities for 3 products
xyfcli order full-flow --product-codes "P1,P2,P3" --quantities "5,3"

# Correct: 3 quantities for 3 products
xyfcli order full-flow --product-codes "P1,P2,P3" --quantities "5,3,2"
```

#### `商品数量必须为正整数，当前值: {value}` (Quantity Must Be Positive Integer)
**Meaning**: Quantity value is not a positive integer (>0).

**Common causes**:
- Zero, negative, or decimal quantity
- Non-numeric value
- Empty value in list

**Solutions**:
1. Ensure all quantities are positive integers (1, 2, 3...)
2. No zeros, negatives, or decimals
3. Check each value in the list

**Examples**:
```bash
# Wrong: Contains zero
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,0"

# Wrong: Contains negative
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,-1"

# Wrong: Contains decimal
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,2.5"

# Correct: Positive integers only
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,3"
```

#### `数量列表必须为逗号分隔的整数` (Quantity List Must Be Comma-Separated Integers)
**Meaning**: Quantity list contains non-integer values or formatting issues.

**Common causes**:
- Non-numeric characters in quantity list
- Incorrect separator
- Formatting errors

**Solutions**:
1. Use only numbers and commas
2. No spaces around numbers (or consistent spacing)
3. Check for hidden characters

**Examples**:
```bash
# Wrong: Contains letters
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,three"

# Wrong: Incorrect separator
xyfcli order full-flow --product-codes "P1,P2" --quantities "5;3"

# Correct: Numbers and commas only
xyfcli order full-flow --product-codes "P1,P2" --quantities "5,3"
```

### Delivery and Address Errors

#### `未找到发货基地` (Delivery Base Not Found)
**Meaning**: No delivery bases available for the product and customer.

**Common causes**:
- Product not deliverable to customer's region
- No bases configured for the product
- API data issue

**Solutions**:
1. Try different product
2. Check product-customer combination
3. Contact administrator for base configuration

**Example**:
```bash
xyfcli order full-flow --product-codes "SPECIAL_PRODUCT" --dealer-index 0 --base-index 0
```

#### `发货基地索引 {index} 超出范围` (Delivery Base Index Out of Range)
**Meaning**: Specified base index exceeds available bases.

**Common causes**:
- Using wrong index number
- Not checking available bases
- Base list changed

**Solutions**:
1. The tool shows available bases count in output
2. Use 0-based index within range
3. Check output for base list information

**Example**:
```bash
# If only 2 bases available
xyfcli order full-flow --product-codes "Y163U1305276020000" --base-index 3
```

#### `未找到收货地址且未提供直接地址` (No Address Found and No Direct Address Provided)
**Meaning**: Customer has no saved addresses and no direct address provided.

**Common causes**:
- Customer address list is empty
- Forgot to provide `--address` parameter
- Address API issue

**Solutions**:
1. Provide direct address: `--address "完整地址"`
2. Check customer address configuration
3. Ask customer to provide address

**Examples**:
```bash
# Wrong: No address provided for customer with no addresses
xyfcli order full-flow --product-codes "Y163U1305276020000" --address-index 0

# Correct: Provide direct address
xyfcli order full-flow --product-codes "Y163U1305276020000" --address "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

#### `收货地址索引 {index} 超出范围` (Address Index Out of Range)
**Meaning**: Specified address index exceeds customer's address list.

**Common causes**:
- Using wrong index number
- Customer has fewer addresses than expected
- Not checking address count

**Solutions**:
1. The tool shows address count in output
2. Use 0-based index within range
3. Check customer's address list first

**Example**:
```bash
# If customer has only 1 address
xyfcli order full-flow --product-codes "Y163U1305276020000" --address-index 2
```

### Parameter Validation Errors

#### `必须提供产品描述(--desc)或产品编码列表(--product-codes)` (Must Provide Product Description or Product Codes)
**Meaning**: Neither product description nor product codes provided.

**Common causes**:
- Missing required parameter
- Parameter name typo
- Empty value

**Solutions**:
1. Provide either `--description` or `--product-codes`
2. Check parameter spelling
3. Ensure value is not empty

**Examples**:
```bash
# Wrong: Missing product information
xyfcli order full-flow --dealer-index 0 --base-index 0

# Correct: Provide product info
xyfcli order full-flow --description "含量 45%" --dealer-index 0 --base-index 0

# Also correct: Use product codes
xyfcli order full-flow --product-codes "Y163U1305276020000" --dealer-index 0 --base-index 0
```

#### `产品编码列表不能为空` (Product Codes List Cannot Be Empty)
**Meaning**: Product codes parameter provided but empty.

**Common causes**:
- Empty string for `--product-codes`
- Only commas or whitespace
- Parameter without value

**Solutions**:
1. Provide actual product codes
2. Check for extra commas or spaces
3. Use valid product codes

**Examples**:
```bash
# Wrong: Empty product codes
xyfcli order full-flow --product-codes "" --dealer-index 0

# Wrong: Only commas
xyfcli order full-flow --product-codes ",," --dealer-index 0

# Correct: Valid product codes
xyfcli order full-flow --product-codes "Y163U1305276020000" --dealer-index 0
```

### Authentication and Connectivity Errors

#### `HTTP Error` or Connection Errors
**Meaning**: Unable to connect to API server.

**Common causes**:
- API server down
- Network connectivity issues
- Wrong API URL configuration
- Authentication expired

**Solutions**:
1. Check API server status
2. Verify network connectivity
3. Check session/cookie validity
4. Verify API URL configuration

**Detection**:
```bash
# Test connectivity
xyfcli shop dealer-list
```

#### Session Expired Errors
**Meaning**: Authentication session has expired.

**Common causes**:
- Session cookie expired
- User logged out
- Server session cleared

**Solutions**:
1. Re-authenticate with the system
2. Obtain new session cookie
3. Update CLI configuration

### JSON Output Errors

#### JSON Parsing Errors in Output
**Meaning**: Error parsing JSON output from command.

**Common causes**:
- Incomplete JSON output
- API returned non-JSON response
- Output redirected incorrectly

**Solutions**:
1. Run command without `--json` first
2. Check API response format
3. Ensure command completes successfully

**Example**:
```bash
# If JSON output is malformed
xyfcli order full-flow --product-codes "Y163U1305276020000" --json | jq .
```

## Error Severity Levels

### Critical Errors (Process Stops)
- `未找到相关产品` - Product search failed
- `未找到客户` - No customers available
- `未找到发货基地` - No delivery options
- `未找到收货地址且未提供直接地址` - No address available
- Authentication/connectivity errors

### Validation Errors (Parameter Issues)
- Index out of range errors
- Quantity validation errors
- Parameter requirement errors
- Format errors

### Warnings (Process Continues)
- `产品 {code} 不在客户可购买列表中` - Product not in customer's list (warning)
- Other non-critical validations

## Debugging Steps

### Step 1: Check Basic Connectivity
```bash
xyfcli shop dealer-list
```

### Step 2: Test Product Search
```bash
xyfcli order full-flow --description "测试" --product-index 0 --json
```

### Step 3: Test with Simple Parameters
```bash
xyfcli order full-flow --product-codes "KNOWN_PRODUCT" --dealer-index 0 --json
```

### Step 4: Check Individual Components
```bash
# Check product
xyfcli shop product-info --product-code "Y163U1305276020000"

# Check customer products
xyfcli shop product-list --dealer-code "J620522007"
```

### Step 5: Use Verbose/JSON Output
```bash
# Always add --json for detailed error information
xyfcli order full-flow [parameters] --json
```

## Prevention Tips

1. **Always check indices**: Use `xyfcli shop dealer-list` before `--dealer-index`
2. **Validate quantities**: Count items in both lists before submission
3. **Test connectivity**: Run simple commands first
4. **Use JSON output**: For detailed error information
5. **Check parameter syntax**: Use `--help` for each command
6. **Start simple**: Single product before multi-product orders
7. **Verify addresses**: Have address ready before starting
8. **Keep session valid**: Re-authenticate if sessions expire

## Common Error Patterns and Fixes

| Error Pattern | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| Index errors | Not checking available items | Run `xyfcli shop dealer-list` first |
| Quantity mismatches | Different list lengths | Count items in both lists |
| Product not found | Invalid search terms | Use specific product codes |
| No addresses | Customer has no saved addresses | Use `--address` parameter |
| Authentication errors | Session expired | Re-authenticate and update config |
| API errors | Server issues | Check API connectivity |

## Getting Help

If errors persist:
1. **Check command syntax**: Use `--help` for each command
2. **Verify all parameters**: Ensure all required parameters provided
3. **Test with simple example**: Reduce complexity to isolate issue
4. **Check logs**: Look for detailed error messages in JSON output
5. **Contact support**: Provide exact command and error output
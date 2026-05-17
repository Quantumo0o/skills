# SQL 注入修复模式手册

PHP 7.3 / Yaf 项目常见 SQL 注入模式及参数化修复方法。

---

## 规则

1. **列名和表名不能参数化** — 只有值可以参数化。列名/表名必须使用白名单。
2. **整数参数先 (int) 转换** — 即使参数化，整数字段也要在绑定前 `(int)` 转换，防止类型混淆。
3. **不改 DB 层** — 修复只在调用点添加参数化，不引入新的 DB 库。
4. **PHP 7.3 语法** — 不使用 match、命名参数、nullsafe operator 等。

---

## Pattern 1 — 字符串拼接

最常见，最危险。

```php
// ❌ 危险
$sql = "SELECT * FROM users WHERE id = " . $id;
$sql = "SELECT * FROM users WHERE name = '" . $name . "'";
$sql = "UPDATE orders SET status = " . $status . " WHERE id = " . $id;

// ✅ 修复（PDO）
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

$stmt = $pdo->prepare("SELECT * FROM users WHERE name = ?");
$stmt->execute([$name]);

$stmt = $pdo->prepare("UPDATE orders SET status = ? WHERE id = ?");
$stmt->execute([$status, $id]);
```

---

## Pattern 2 — 双引号变量插值

```php
// ❌ 危险
$sql = "SELECT * FROM t WHERE uid = $uid AND type = '$type'";
$sql = "DELETE FROM logs WHERE user_id = $user_id";

// ✅ 修复
$stmt = $pdo->prepare("SELECT * FROM t WHERE uid = ? AND type = ?");
$stmt->execute([$uid, $type]);

$stmt = $pdo->prepare("DELETE FROM logs WHERE user_id = ?");
$stmt->execute([$user_id]);
```

---

## Pattern 3 — sprintf

```php
// ❌ 危险（%s 不等于安全转义）
$sql = sprintf("SELECT * FROM t WHERE name = '%s' AND role = %d", $name, $role);

// ✅ 修复
$stmt = $pdo->prepare("SELECT * FROM t WHERE name = ? AND role = ?");
$stmt->execute([$name, (int)$role]);
```

---

## Pattern 4 — 超全局变量直接入 SQL

```php
// ❌ 危险（极高风险）
$sql = "SELECT * FROM t WHERE id = " . $_GET['id'];
$sql = "SELECT * FROM t WHERE name = '" . $_POST['name'] . "'";

// ✅ 修复
$id   = (int) ($_GET['id'] ?? 0);
$stmt = $pdo->prepare("SELECT * FROM t WHERE id = ?");
$stmt->execute([$id]);

$name = trim($_POST['name'] ?? '');
$stmt = $pdo->prepare("SELECT * FROM t WHERE name = ?");
$stmt->execute([$name]);
```

---

## Pattern 5 — IN 子句

```php
// ❌ 危险
$ids = implode(',', $id_arr);
$sql = "SELECT * FROM t WHERE id IN ($ids)";

// ✅ 修复（PHP 7.3 兼容）
$id_arr      = array_map('intval', $id_arr);   // 如果是整数先强转
$placeholders = implode(',', array_fill(0, count($id_arr), '?'));
$stmt = $pdo->prepare("SELECT * FROM t WHERE id IN ($placeholders)");
$stmt->execute($id_arr);
```

---

## Pattern 6 — LIKE 子句

```php
// ❌ 危险
$sql = "SELECT * FROM t WHERE title LIKE '%" . $kw . "%'";
$sql = "SELECT * FROM t WHERE title LIKE '%$kw%'";

// ✅ 修复（通配符放在绑定值里）
$stmt = $pdo->prepare("SELECT * FROM t WHERE title LIKE ?");
$stmt->execute(["%$kw%"]);
```

---

## Pattern 7 — ORDER BY（列名不能参数化）

```php
// ❌ 危险
$sql = "SELECT * FROM t ORDER BY " . $_GET['sort'];

// ✅ 修复（白名单）
$allowed_cols = ['id', 'created_at', 'name', 'status'];
$sort = in_array($_GET['sort'] ?? '', $allowed_cols, true)
    ? $_GET['sort']
    : 'id';  // 默认值
$stmt = $pdo->prepare("SELECT * FROM t ORDER BY $sort DESC");
$stmt->execute([]);
```

---

## Pattern 8 — Yaf Model 自定义 where()

项目里常见的 Model 链式调用，具体修法取决于 Model 是否支持数组条件。

```php
// ❌ 危险
$this->_model->where("uid = $uid AND status = '$status'")->find();

// ✅ 修复方式 A（如果 Model 支持数组条件）
$this->_model->where(['uid' => $uid, 'status' => $status])->find();

// ✅ 修复方式 B（如果 Model 支持原生绑定）
$this->_model->where("uid = ? AND status = ?", [$uid, $status])->find();

// ✅ 修复方式 C（退回 PDO）
$stmt = $this->_db->prepare("SELECT * FROM {$this->_table} WHERE uid = ? AND status = ?");
$stmt->execute([$uid, $status]);
$row = $stmt->fetch(PDO::FETCH_ASSOC);
```

---

## Pattern 9 — 分页 LIMIT/OFFSET

```php
// ❌ 危险
$sql = "SELECT * FROM t LIMIT $limit OFFSET $offset";

// ✅ 修复（整数强制转换，LIMIT 不需要占位符但必须确保是整数）
$limit  = max(1, min(100, (int) $limit));   // 强制范围
$offset = max(0, (int) $offset);
// LIMIT/OFFSET 用整数字面量拼接是安全的，因为已经 (int) 转换
$stmt = $pdo->prepare("SELECT * FROM t LIMIT $limit OFFSET $offset");
$stmt->execute([]);
```

---

## 常见误区

### 误区 1 — addslashes 不够

```php
// ❌ 不安全（部分字符集下可绕过）
$name = addslashes($_POST['name']);
$sql  = "SELECT * FROM t WHERE name = '$name'";

// ✅ 用参数化查询
```

### 误区 2 — mysql_real_escape_string 已废弃

```php
// ❌ PHP 7.0+ 已移除 mysql_* 系列函数
$name = mysql_real_escape_string($name);
```

### 误区 3 — intval 对字符串字段无效

```php
// ❌ 对字符串字段强转 int 会导致逻辑错误
$name = intval($_POST['name']);  // 变成 0

// ✅ 字符串字段必须用参数化，不能用 intval
```

### 误区 4 — 列名也用 ? 占位

```php
// ❌ PDO 不支持列名占位符
$stmt = $pdo->prepare("SELECT ? FROM t");
$stmt->execute([$col]);  // 实际执行 SELECT 'col_name' FROM t（当字符串处理）

// ✅ 列名用白名单
```

---

## 修复验证步骤

```bash
# 1. PHP 语法检查
php -l <file>

# 2. 容器内语法检查（Yaf 项目）
docker compose -f /mnt/d/Users/Public/php20250819/docker-php7.3/docker-compose.yml \
  exec fpm-server php -l /var/www/html/2026www/<project>/<file>

# 3. 重跑扫描器确认清零
bash scan_sql.sh <project-root>

# 4. 接口冒烟测试（验证业务逻辑未破坏）
curl -X GET "http://localhost/api/xxx?id=1"
curl -X GET "http://localhost/api/xxx?id=1' OR '1'='1"  # 注入测试，应返回空或报错
```

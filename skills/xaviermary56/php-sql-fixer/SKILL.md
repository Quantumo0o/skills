---
name: php-sql-fixer
version: 1.0.0
description: "Detect SQL injection risks in PHP/Yaf projects and generate parameterized query fix patches. Scans for string concatenation in SQL, unsafe superglobal interpolation, and sprintf-based injection. Outputs annotated findings with before/after fix suggestions. Works with PHP 7.3 and common Yaf DB patterns."
emoji: 💉
user-invocable: true
homepage: https://github.com/XavierMary56/OmniPublish
requires:
  - yaf-php-audit
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - grep
        - php
---

# PHP SQL Fixer

Detect SQL injection risks and generate parameterized query fix patches for PHP/Yaf projects.

## Overview

This skill does two things:

1. **Scan** — find all SQL injection candidates in a PHP project (string concatenation, superglobal interpolation, unsafe sprintf)
2. **Fix** — for each finding, generate the parameterized equivalent and explain the change

Always prefer minimal, targeted fixes. Do not refactor surrounding code. Do not change DB abstraction patterns that already exist in the project.

---

## Workflow

### Step 1 — Run the scanner

```bash
bash "$SKILL_DIR/scripts/scan_sql.sh" <project-root> [output-file]
```

Read the output carefully. The scanner flags candidates, not confirmed vulnerabilities. Some hits may be false positives (e.g. SQL built from constants, not user input).

### Step 2 — Triage findings

For each flagged file:
- Open the file and read the full context around the hit (at least ±10 lines)
- Confirm whether user-controlled input (`$_GET`, `$_POST`, `$_REQUEST`, function params from controllers) reaches the SQL string
- Mark each finding as: **confirmed** / **suspected** / **false positive**

### Step 3 — Generate fix suggestions

```bash
php "$SKILL_DIR/scripts/suggest_fix.php" <file-path>
```

The script outputs annotated before/after for each risky SQL statement in the file.

### Step 4 — Apply fixes

Apply fixes manually or with targeted `Edit` tool calls. Rules:
- Use parameterized queries matching the project's existing DB pattern (PDO, custom model, etc.)
- Do not change method signatures or surrounding business logic
- Add a `// FIXED: sql injection` comment on the line where the fix was applied
- Run `php -l <file>` after every edit to verify syntax

### Step 5 — Verify

```bash
# syntax check
docker compose -f /mnt/d/Users/Public/php20250819/docker-php7.3/docker-compose.yml \
  exec fpm-server php -l /var/www/html/2026www/<project>/<file>

# re-scan to confirm no remaining hits
bash "$SKILL_DIR/scripts/scan_sql.sh" <project-root>
```

---

## Fix Patterns

See `references/fix-patterns.md` for the complete catalog. Quick reference:

### Pattern 1 — String concatenation

```php
// BEFORE (unsafe)
$sql = "SELECT * FROM users WHERE id = " . $id;
$res = $db->query($sql);

// AFTER (PDO)
$stmt = $db->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);
$res = $stmt->fetchAll();
```

### Pattern 2 — Variable interpolation

```php
// BEFORE (unsafe)
$sql = "SELECT * FROM orders WHERE status = '$status' AND uid = $uid";

// AFTER (PDO named placeholders)
$stmt = $db->prepare("SELECT * FROM orders WHERE status = :status AND uid = :uid");
$stmt->execute([':status' => $status, ':uid' => $uid]);
```

### Pattern 3 — sprintf injection

```php
// BEFORE (unsafe)
$sql = sprintf("SELECT * FROM t WHERE name = '%s'", $name);

// AFTER
$stmt = $db->prepare("SELECT * FROM t WHERE name = ?");
$stmt->execute([$name]);
```

### Pattern 4 — Yaf Model with custom query builder

```php
// BEFORE (unsafe — raw string passed to model)
$this->_model->where("user_id = $uid AND type = '$type'")->find();

// AFTER (use array condition — depends on your Model API)
$this->_model->where(['user_id' => $uid, 'type' => $type])->find();

// OR if model supports raw+bindings:
$this->_model->where("user_id = ? AND type = ?", [$uid, $type])->find();
```

### Pattern 5 — IN clause with array

```php
// BEFORE (unsafe)
$ids = implode(',', $id_arr);
$sql = "SELECT * FROM t WHERE id IN ($ids)";

// AFTER (PHP 7.3 compatible)
$placeholders = implode(',', array_fill(0, count($id_arr), '?'));
$stmt = $db->prepare("SELECT * FROM t WHERE id IN ($placeholders)");
$stmt->execute($id_arr);
```

---

## What NOT to Change

- Do not switch DB abstraction libraries (e.g. from custom Model to bare PDO) unless the whole project already uses PDO
- Do not parameterize column names or table names — these cannot be parameterized; use an allowlist instead
- Do not touch SQL built entirely from constants with no user input
- Do not change surrounding cache logic, error handling, or return values

---

## False Positive Checklist

Before reporting a finding as confirmed SQL injection:

- [ ] Does user-controlled input actually reach this SQL string?
- [ ] Is the value an integer that was already `intval()`-cast earlier?
- [ ] Is the value selected from a fixed allowlist (e.g. column name from a whitelist array)?
- [ ] Is the SQL built from config constants only (no request data)?

If all four are "no" → confirmed risk. If any is "yes" → suspected or false positive.

---

## Bulk Fix Guidance

When fixing many files across a project:

1. Run `scan_sql.sh` on the whole project, save output to file
2. Sort findings by controller/callback/payment paths first
3. Fix highest-risk files first (payment, callback, login)
4. Re-scan after each batch to track progress
5. Never mix SQL fix commits with unrelated changes

---
name: sql-splitter
description: 拆分 SQL 文件为独立文件（存储过程、函数、视图、触发器、表结构、索引、约束）
---

# SQL 文件拆分工具

将包含多个 SQL 对象的单一文件或目录拆分为独立的 .sql 文件。

## 支持的 SQL 方言

- MySQL
- PostgreSQL
- Oracle
- SQL Server
- 达梦 (DM)
- 通用 (Generic)

## 支持的 SQL 对象类型

| 类型 | 前缀 | 说明 |
|------|------|------|
| 存储过程 | `proc_` | CREATE PROCEDURE |
| 函数 | `func_` | CREATE FUNCTION |
| 视图 | `view_` | CREATE VIEW |
| 触发器 | `trig_` | CREATE TRIGGER |
| 表结构 | `table_` | CREATE TABLE |
| 包 | `pkg_` | CREATE PACKAGE |
| 索引 | `idx_` | CREATE INDEX |
| 唯一索引 | `uidx_` | CREATE UNIQUE INDEX |
| 约束 | `con_` | ALTER TABLE ADD CONSTRAINT |
| 序列 | `seq_` | CREATE SEQUENCE |
| 同义词 | `syn_` | CREATE SYNONYM (Oracle) |
| 事件 | `evt_` | CREATE EVENT (MySQL) |
| 物化视图 | `mv_` | CREATE MATERIALIZED VIEW (PostgreSQL) |
| 类型 | `type_` | CREATE TYPE |

## 使用方法

### 单文件拆分
```bash
python3 ~/.openclaw/skills/sql-splitter/scripts/split_sql.py <input.sql> [output_dir]
```

### 批量拆分（目录）
```bash
python3 ~/.openclaw/skills/sql-splitter/scripts/split_sql.py --batch <目录路径> [输出目录]
```

### 批量拆分（多个文件）
```bash
python3 ~/.openclaw/skills/sql-splitter/scripts/split_sql.py --batch "file1.sql,file2.sql,file3.sql" [输出目录]
```

### 指定方言
```bash
python3 ~/.openclaw/skills/sql-splitter/scripts/split_sql.py --dialect oracle input.sql
```

支持的方言：`mysql`, `postgresql`, `oracle`, `sqlserver`, `dm`, `generic`

### 参数说明

| 参数 | 说明 |
|------|------|
| `input.sql` | 要拆分的 SQL 文件路径（单文件模式必需） |
| `--batch` | 批量模式标志 |
| `--dialect` | 指定 SQL 方言 |
| `-q`, `--quiet` | 静默模式 |
| `output_dir` | 输出目录（可选，默认：原文件名_split） |

## 输出示例

假设输入文件 `myapp.sql` 包含：
- 存储过程 `usp_GetUsers`
- 函数 `fn_CalculateTotal`
- 视图 `vw_OrderSummary`
- 索引 `idx_users_name`

输出：
```
myapp_split/
├── proc_usp_GetUsers.sql
├── func_fn_CalculateTotal.sql
├── view_vw_OrderSummary.sql
└── idx_idx_users_name.sql
```

## 注意事项

- 使用正则表达式识别 SQL 对象，可能对复杂嵌套语法有局限
- 默认 UTF-8 编码
- 建议先备份原文件
- 批量模式会自动创建以原文件名命名的子目录
- 自动检测 SQL 方言，也可手动指定

## 更新日志

### v1.1.0 (2026-04-13)
- ✨ 新增索引支持：CREATE INDEX, CREATE UNIQUE INDEX
- ✨ 新增约束支持：ALTER TABLE ADD CONSTRAINT
- ✨ 所有 6 种方言均支持索引/约束识别
- ✨ 支持 CLUSTERED/NONCLUSTERED (SQL Server)
- ✨ 支持 BITMAP 索引 (Oracle/达梦)

### v1.0.0
- 初始版本
- 支持存储过程、函数、视图、触发器、表、包等基础对象

#!/usr/bin/env python3
"""
SQL 文件拆分工具 - 多数据库方言支持
支持 MySQL, PostgreSQL, Oracle, SQL Server, 达梦(DM) 等数据库
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from enum import Enum
from collections import defaultdict


class SQLDialect(Enum):
    """支持的 SQL 方言"""
    MYSQL = 'mysql'
    POSTGRESQL = 'postgresql'
    ORACLE = 'oracle'
    SQLSERVER = 'sqlserver'
    DM = 'dm'  # 达梦
    GENERIC = 'generic'  # 通用模式


# 各数据库方言的特定模式
DIALECT_PATTERNS = {
    SQLDialect.MYSQL: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+`?([\w]+)`?\s*\(', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+`?([\w]+)`?\s*\([^)]*\)\s*RETURNS\s+\w+', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+`?([\w]+)`?\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:ALGORITHM\s*=\s*\w+\s+)?VIEW\s+`?([\w]+)`?\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+(?:TEMPORARY\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([\w]+)`?\s*\(', re.IGNORECASE),
        ],
        'event': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?EVENT\s+`?([\w]+)`?\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:ONLINE\s+)?(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([\w]+)`?\s+ON\s+`?([\w]+)`?', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+(?:ONLINE\s+)?UNIQUE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([\w]+)`?\s+ON\s+`?([\w]+)`?', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+`?([\w]+)`?\s+ADD\s+(?:CONSTRAINT\s+)?`?([\w]+)`?\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
    SQLDialect.POSTGRESQL: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+([\w.]+)\s*\(', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+([\w.]+)\s*\([^)]*\)\s*RETURNS\s+\w+', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+([\w]+)\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+([\w.]+)\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+(?:TEMP\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)\s*\(', re.IGNORECASE),
        ],
        'materialized_view': [
            re.compile(r'CREATE\s+(?:UNLOGGED\s+)?MATERIALIZED\s+VIEW\s+([\w.]+)\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'type': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?TYPE\s+([\w.]+)\s+AS\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)\s+ON\s+([\w.]+)', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+UNIQUE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)\s+ON\s+([\w.]+)', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+([\w.]+)\s+ADD\s+(?:CONSTRAINT\s+)?([\w.]+)\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
    SQLDialect.ORACLE: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?PROCEDURE\s+([\w."]+)\s*(?:\([^)]*\))?\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?FUNCTION\s+([\w."]+)\s*(?:\([^)]*\))?\s*RETURN\s+\w+\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?TRIGGER\s+([\w."]+)\s+(?:BEFORE|AFTER|INSTEAD\s+OF|FOR\s+EACH\s+ROW)\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?(?:FORCE\s+)?VIEW\s+([\w."]+)\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\s+([\w."]+)\s*\(', re.IGNORECASE),
        ],
        'package': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?PACKAGE\s+(?:BODY\s+)?([\w."]+)\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'synonym': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:PUBLIC\s+)?SYNONYM\s+([\w."]+)\s+FOR\s+', re.IGNORECASE),
        ],
        'sequence': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?SEQUENCE\s+([\w."]+)\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:UNIQUE\s+)?(?:BITMAP\s+)?INDEX\s+([\w."]+)\s+ON\s+([\w."]+)', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+UNIQUE\s+(?:BITMAP\s+)?INDEX\s+([\w."]+)\s+ON\s+([\w."]+)', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+([\w."]+)\s+ADD\s+(?:CONSTRAINT\s+)?([\w."]+)\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
    SQLDialect.SQLSERVER: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s*(?:\(|@)', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+ALTER\s+)?FUNCTION\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s*\([^)]*\)\s*RETURNS\s+', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+ALTER\s+)?TRIGGER\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s+ON\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+ALTER\s+)?VIEW\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+TABLE\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s*\(', re.IGNORECASE),
        ],
        'type': [
            re.compile(r'CREATE\s+TYPE\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s+AS\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:UNIQUE\s+)?(?:CLUSTERED|NONCLUSTERED\s+)?INDEX\s+\[?([\w]+)\]?\s+ON\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+UNIQUE\s+(?:CLUSTERED|NONCLUSTERED\s+)?INDEX\s+\[?([\w]+)\]?\s+ON\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+(?:\[?[\w]+\]?\.)?\[?([\w]+)\]?\s+ADD\s+(?:CONSTRAINT\s+)?\[?([\w]+)\]?\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
    SQLDialect.DM: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+"?([\w.]+)"?\s*(?:\([^)]*\))?\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+"?([\w.]+)"?\s*(?:\([^)]*\))?\s*RETURN\s+\w+\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+"?([\w.]+)"?\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+"?([\w.]+)"?\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\s+"?([\w.]+)"?\s*\(', re.IGNORECASE),
        ],
        'package': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PACKAGE\s+(?:BODY\s+)?"?([\w.]+)"?\s*(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'sequence': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?SEQUENCE\s+"?([\w.]+)"?\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:UNIQUE\s+)?(?:BITMAP\s+)?INDEX\s+"?([\w.]+)"?\s+ON\s+"?([\w.]+)"?', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+UNIQUE\s+(?:BITMAP\s+)?INDEX\s+"?([\w.]+)"?\s+ON\s+"?([\w.]+)"?', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+"?([\w.]+)"?\s+ADD\s+(?:CONSTRAINT\s+)?"?([\w.]+)"?\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
    SQLDialect.GENERIC: {
        'procedure': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+([\w.`"[\]]+)\s*[\(\w\s,@=]', re.IGNORECASE),
        ],
        'function': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+([\w.`"[\]]+)\s*(?:\([^)]*\))?\s*RETURN', re.IGNORECASE),
        ],
        'trigger': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+([\w.`"[\]]+)\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+', re.IGNORECASE),
        ],
        'view': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+([\w.`"[\]]+)\s*(?:\([^)]*\))?\s*AS\s+', re.IGNORECASE),
        ],
        'table': [
            re.compile(r'CREATE\s+(?:TEMP(?:ORARY)?\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.`"[\]]+)\s*\(', re.IGNORECASE),
        ],
        'package': [
            re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?PACKAGE\s+(?:BODY\s+)?([\w.`"[\]]+)\s+(?:IS|AS)\s+', re.IGNORECASE),
        ],
        'index': [
            re.compile(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+([\w.`"[\]]+)\s+ON\s+([\w.`"[\]]+)', re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(r'CREATE\s+UNIQUE\s+INDEX\s+([\w.`"[\]]+)\s+ON\s+([\w.`"[\]]+)', re.IGNORECASE),
        ],
        'constraint': [
            re.compile(r'ALTER\s+TABLE\s+([\w.`"[\]]+)\s+ADD\s+(?:CONSTRAINT\s+)?([\w.`"[\]]+)\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)', re.IGNORECASE),
        ],
    },
}

# 对象类型到文件前缀的映射
OBJECT_PREFIXES = {
    'procedure': 'proc',
    'function': 'func',
    'trigger': 'trig',
    'view': 'view',
    'table': 'table',
    'package': 'pkg',
    'sequence': 'seq',
    'synonym': 'syn',
    'event': 'evt',
    'materialized_view': 'mv',
    'type': 'type',
    'index': 'idx',
    'unique_index': 'uidx',
    'constraint': 'con',
    'primary_key': 'pk',
    'foreign_key': 'fk',
    'check': 'chk',
}


def detect_dialect(sql_content: str) -> SQLDialect:
    """自动检测 SQL 方言"""
    sql_upper = sql_content.upper()
    
    # Oracle 特征
    if re.search(r'\bPACKAGE\s+(?:BODY\s+)?[\w.]+\s+(?:IS|AS)\b', sql_upper):
        if re.search(r'^/\s*$', sql_content, re.MULTILINE):
            return SQLDialect.ORACLE
    if re.search(r'\bEDITIONABLE\b', sql_upper):
        return SQLDialect.ORACLE
    if re.search(r'\bSYNONYM\s+[\w.]+\s+FOR\b', sql_upper):
        return SQLDialect.ORACLE
    
    # SQL Server 特征
    if re.search(r'\bGO\s*$', sql_content, re.IGNORECASE | re.MULTILINE):
        return SQLDialect.SQLSERVER
    if re.search(r'\bCREATE\s+PROC\s+[\w.\[\]]+', sql_upper):
        return SQLDialect.SQLSERVER
    if re.search(r'\bALTER\s+PROC(?:EDURE)?\s+', sql_upper):
        return SQLDialect.SQLSERVER
    
    # PostgreSQL 特征
    if re.search(r'\$\$[\s\S]*?\$\$', sql_content):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bLANGUAGE\s+(?:plpgsql|plpython|plperl)\b', sql_upper):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bMATERIALIZED\s+VIEW\b', sql_upper):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bRETURNS\s+(?:SETOF|TABLE)\b', sql_upper):
        return SQLDialect.POSTGRESQL
    
    # MySQL 特征
    if re.search(r'`[\w]+`', sql_content):
        if re.search(r'\bENGINE\s*=\s*\w+\b', sql_upper):
            return SQLDialect.MYSQL
        if re.search(r'\bCREATE\s+(?:OR\s+REPLACE\s+)?EVENT\b', sql_upper):
            return SQLDialect.MYSQL
        if re.search(r'\bALGORITHM\s*=\s*(?:UNDEFINED|MERGE|TEMPTABLE)\b', sql_upper):
            return SQLDialect.MYSQL
    
    # 达梦特征
    if re.search(r'"[\w.]+"\s*\(', sql_content):
        if re.search(r'\b(?:IS|AS)\s*BEGIN\b', sql_upper):
            return SQLDialect.DM
    
    return SQLDialect.GENERIC


def clean_object_name(name: str) -> str:
    """清理对象名称中的特殊字符"""
    name = re.sub(r'[`"\'\[\]]', '', name)
    if '.' in name:
        name = name.split('.')[-1]
    return name.strip()


def find_object_end(sql_content: str, dialect: SQLDialect, obj_type: str, start_pos: int, next_create_pos: int) -> int:
    """查找对象内容的结束位置"""
    # Oracle/达梦: 查找单独的 /
    if dialect in (SQLDialect.ORACLE, SQLDialect.DM):
        search_range = sql_content[start_pos:next_create_pos]
        slash_match = re.search(r'^/\s*$', search_range, re.MULTILINE)
        if slash_match:
            return start_pos + slash_match.end()
    
    # SQL Server: 查找 GO
    if dialect == SQLDialect.SQLSERVER:
        search_range = sql_content[start_pos:next_create_pos]
        go_match = re.search(r'^GO\s*$', search_range, re.IGNORECASE | re.MULTILINE)
        if go_match:
            return start_pos + go_match.start()
    
    # PostgreSQL: 处理 $$ 包裹语法
    if dialect == SQLDialect.POSTGRESQL and obj_type == 'function':
        dollar_start = sql_content.find('$$', start_pos)
        if dollar_start != -1 and dollar_start < next_create_pos:
            dollar_end = sql_content.find('$$', dollar_start + 2)
            if dollar_end != -1 and dollar_end < next_create_pos:
                semicolon = sql_content.find(';', dollar_end + 2)
                if semicolon != -1 and semicolon < next_create_pos:
                    return semicolon + 1
    
    # 表: 找配对括号
    if obj_type == 'table':
        paren_start = sql_content.find('(', start_pos)
        if paren_start != -1 and paren_start < next_create_pos:
            depth = 1
            i = paren_start + 1
            while i < next_create_pos and depth > 0:
                if sql_content[i] == '(':
                    depth += 1
                elif sql_content[i] == ')':
                    depth -= 1
                i += 1
            while i < next_create_pos and sql_content[i] in ' \t\n\r':
                i += 1
            if i < next_create_pos and sql_content[i] == ';':
                return i + 1
            return i
    
    # 视图/物化视图: 找 AS 后的第一个分号
    if obj_type in ('view', 'materialized_view'):
        search_range = sql_content[start_pos:next_create_pos]
        as_match = re.search(r'\bAS\s+', search_range, re.IGNORECASE)
        if as_match:
            search_start = start_pos + as_match.end()
            semicolon = sql_content.find(';', search_start)
            if semicolon != -1 and semicolon < next_create_pos:
                return semicolon + 1
    
    # 索引/约束: 找分号
    if obj_type in ('index', 'unique_index', 'constraint'):
        semicolon = sql_content.find(';', start_pos)
        if semicolon != -1 and semicolon < next_create_pos:
            return semicolon + 1
    
    # 默认: 找分号
    semicolon = sql_content.find(';', start_pos)
    if semicolon != -1 and semicolon < next_create_pos:
        return semicolon + 1
    
    return next_create_pos


def split_sql_file(
    input_file: str,
    output_dir: Optional[str] = None,
    dialect: Optional[SQLDialect] = None,
    verbose: bool = True
) -> Dict:
    """拆分 SQL 文件"""
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            sql_content = f.read()
    except Exception as e:
        return {
            'output_dir': None,
            'created_files': [],
            'errors': [f"无法读取文件: {e}"],
            'stats': {},
            'total': 0
        }
    
    if dialect is None:
        dialect = detect_dialect(sql_content)
    
    if verbose:
        print(f"🔍 检测到方言: {dialect.value.upper()}")
    
    if output_dir is None:
        output_dir = os.path.splitext(input_file)[0] + '_split'
    
    os.makedirs(output_dir, exist_ok=True)
    
    patterns = DIALECT_PATTERNS.get(dialect, DIALECT_PATTERNS[SQLDialect.GENERIC])
    
    # 收集所有对象
    found_objects = []
    for obj_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            for match in pattern.finditer(sql_content):
                name = clean_object_name(match.group(1))
                found_objects.append({
                    'type': obj_type,
                    'name': name,
                    'start': match.start(),
                    'match': match
                })
    
    # 按位置排序
    found_objects.sort(key=lambda x: x['start'])
    
    if verbose:
        print(f"📄 找到 {len(found_objects)} 个对象")
    
    # 提取并保存每个对象
    created_files = []
    errors = []
    stats = defaultdict(int)
    
    for i, obj in enumerate(found_objects):
        next_start = found_objects[i + 1]['start'] if i + 1 < len(found_objects) else len(sql_content)
        end_pos = find_object_end(sql_content, dialect, obj['type'], obj['start'], next_start)
        
        obj_content = sql_content[obj['start']:end_pos].strip()
        
        if not obj_content:
            continue
        
        prefix = OBJECT_PREFIXES.get(obj['type'], 'obj')
        filename = f"{prefix}_{obj['name']}.sql"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(obj_content)
                if not obj_content.endswith(';'):
                    f.write(';')
                f.write('\n')
            created_files.append(filepath)
            stats[obj['type']] += 1
            if verbose:
                print(f"  ✅ {filename}")
        except Exception as e:
            errors.append(f"写入 {filename} 失败: {e}")
    
    return {
        'output_dir': output_dir,
        'created_files': created_files,
        'errors': errors,
        'stats': dict(stats),
        'total': len(created_files)
    }


def split_sql_batch(
    input_paths,
    output_dir: Optional[str] = None,
    dialect: Optional[SQLDialect] = None,
    verbose: bool = True
) -> List[Dict]:
    """批量拆分 SQL 文件"""
    results = []
    
    for input_path in input_paths:
        if os.path.isdir(input_path):
            for filename in os.listdir(input_path):
                if filename.lower().endswith('.sql'):
                    filepath = os.path.join(input_path, filename)
                    file_output = os.path.join(output_dir, os.path.splitext(filename)[0] + '_split') if output_dir else None
                    result = split_sql_file(filepath, file_output, dialect, verbose)
                    results.append(result)
        else:
            result = split_sql_file(input_path, output_dir, dialect, verbose)
            results.append(result)
    
    return results


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SQL 文件拆分工具')
    parser.add_argument('input', help='输入 SQL 文件或目录')
    parser.add_argument('output', nargs='?', help='输出目录')
    parser.add_argument('--batch', action='store_true', help='批量处理目录')
    parser.add_argument('--dialect', choices=['mysql', 'postgresql', 'oracle', 'sqlserver', 'dm', 'generic'], help='指定 SQL 方言')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    dialect_map = {
        'mysql': SQLDialect.MYSQL,
        'postgresql': SQLDialect.POSTGRESQL,
        'oracle': SQLDialect.ORACLE,
        'sqlserver': SQLDialect.SQLSERVER,
        'dm': SQLDialect.DM,
        'generic': SQLDialect.GENERIC,
    }
    
    dialect = dialect_map.get(args.dialect) if args.dialect else None
    verbose = not args.quiet
    
    if args.batch:
        input_paths = [args.input] if ',' not in args.input else args.input.split(',')
        results = split_sql_batch(input_paths, args.output, dialect, verbose)
        total_files = sum(r['total'] for r in results)
        print(f"\n✨ 完成! 共创建 {total_files} 个文件")
    else:
        result = split_sql_file(args.input, args.output, dialect, verbose)
        if result['errors']:
            print("\n❌ 错误:")
            for err in result['errors']:
                print(f"  {err}")
        print(f"\n✨ 完成! 共创建 {result['total']} 个文件")


if __name__ == '__main__':
    main()

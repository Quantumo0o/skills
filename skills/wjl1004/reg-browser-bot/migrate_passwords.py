#!/usr/bin/env python3
"""
密码迁移脚本

功能：
1. 将现有明文密码迁移为加密存储
2. 备份原文件后再修改
3. 验证迁移后的账号可正常解密

用法:
    python migrate_passwords.py [--dry-run] [--verify]
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from security import encrypt_password, decrypt_password


def migrate_passwords(accounts_dir: Path, dry_run: bool = False, verify: bool = True) -> dict:
    """
    迁移所有明文密码为加密存储
    
    Returns:
        dict: 迁移结果统计
    """
    results = {
        'total': 0,
        'migrated': 0,
        'skipped': 0,
        'failed': 0,
        'details': []
    }
    
    # 遍历所有账号文件
    for f in accounts_dir.iterdir():
        if f.suffix != '.json':
            continue
        
        name = f.stem
        # 跳过非账号文件
        if any(name.endswith(s) for s in ['_cookies', '_export', '_session']):
            continue
        
        results['total'] += 1
        
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                account = json.load(fp)
            
            # 检查是否已加密
            if account.get('password_encrypted', False):
                print(f"⏭️  跳过（已加密）: {name}")
                results['skipped'] += 1
                continue
            
            # 获取明文密码
            old_password = account.get('password', '')
            if not old_password:
                print(f"⚠️  跳过（无密码）: {name}")
                results['skipped'] += 1
                continue
            
            if dry_run:
                print(f"🔍 [DRY-RUN] 将迁移: {name}")
                print(f"   明文密码: {old_password[:3]}***")
                results['migrated'] += 1
                continue
            
            # 备份原文件
            backup_path = f.with_suffix(f'.json.bak.{datetime.now().strftime("%Y%m%d%H%M%S")}')
            shutil.copy2(f, backup_path)
            print(f"📦 备份: {backup_path}")
            
            # 加密密码
            encrypted = encrypt_password(old_password)
            account['password'] = encrypted
            account['password_encrypted'] = True
            account['migrated_at'] = datetime.now().isoformat()
            
            # 保存
            with open(f, 'w', encoding='utf-8') as fp:
                json.dump(account, fp, ensure_ascii=False, indent=2)
            
            print(f"✅ 已迁移: {name}")
            
            # 验证
            if verify:
                try:
                    # 重新读取并解密
                    with open(f, 'r', encoding='utf-8') as fp:
                        verify_data = json.load(fp)
                    
                    decrypted = decrypt_password(verify_data['password'])
                    
                    if decrypted == old_password:
                        print(f"   ✓ 验证通过")
                        results['details'].append({
                            'name': name,
                            'status': 'success',
                            'backup': str(backup_path)
                        })
                    else:
                        print(f"   ✗ 验证失败: 密码不匹配")
                        results['failed'] += 1
                        results['details'].append({
                            'name': name,
                            'status': 'verify_failed',
                            'backup': str(backup_path)
                        })
                        # 回滚
                        shutil.copy2(backup_path, f)
                        print(f"   ↩️  已回滚")
                        
                except Exception as e:
                    print(f"   ✗ 验证异常: {e}")
                    results['failed'] += 1
            
            results['migrated'] += 1
            
        except Exception as e:
            print(f"❌ 迁移失败 {name}: {e}")
            results['failed'] += 1
            results['details'].append({
                'name': name,
                'status': 'error',
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description='密码迁移工具')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要迁移的账号，不实际修改')
    parser.add_argument('--verify', action='store_true', default=True, help='验证迁移后的密码可正确解密')
    parser.add_argument('--no-verify', action='store_false', dest='verify', help='跳过验证')
    parser.add_argument('--dir', type=str, help='指定账号目录路径')
    
    args = parser.parse_args()
    
    # 账号目录
    if args.dir:
        accounts_dir = Path(args.dir)
    else:
        accounts_dir = Path.home() / ".openclaw" / "accounts"
    
    if not accounts_dir.exists():
        print(f"❌ 账号目录不存在: {accounts_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("密码迁移工具")
    print("=" * 60)
    print(f"账号目录: {accounts_dir}")
    print(f"模式: {'DRY-RUN' if args.dry_run else '正式迁移'}")
    print(f"验证: {'启用' if args.verify else '禁用'}")
    print("=" * 60)
    print()
    
    # 执行迁移
    results = migrate_passwords(accounts_dir, dry_run=args.dry_run, verify=args.verify)
    
    # 打印统计
    print()
    print("=" * 60)
    print("迁移结果统计")
    print("=" * 60)
    print(f"总数:   {results['total']}")
    print(f"迁移:   {results['migrated']}")
    print(f"跳过:   {results['skipped']}")
    print(f"失败:   {results['failed']}")
    
    if results['failed'] > 0:
        print()
        print("失败的账号:")
        for detail in results['details']:
            if detail['status'] in ('error', 'verify_failed'):
                print(f"  - {detail['name']}: {detail.get('error', 'verify_failed')}")
        sys.exit(1)
    
    if args.dry_run:
        print()
        print("提示: 这是dry-run模式，实际未做任何修改")
        print("去掉 --dry-run 参数以执行实际迁移")


if __name__ == "__main__":
    main()

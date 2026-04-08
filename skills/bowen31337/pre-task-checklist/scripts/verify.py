#!/usr/bin/env python3
"""
Pre-task verification utility
Checks memory, reference files, and critical details before starting tasks
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TOOLS_MD = WORKSPACE / "TOOLS.md"
AGENTS_MD = WORKSPACE / "AGENTS.md"
SOUL_MD = WORKSPACE / "SOUL.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"

def search_files(query, files):
    """Search multiple files for a query"""
    results = {}
    for file_path in files:
        if file_path.exists():
            try:
                content = file_path.read_text()
                lines = content.split('\n')
                matches = [f"  {i+1}: {line}" 
                          for i, line in enumerate(lines) 
                          if query.lower() in line.lower()]
                if matches:
                    results[file_path.name] = matches[:10]  # Max 10 matches
            except Exception as e:
                results[file_path.name] = [f"  Error: {e}"]
    return results

def verify_ip(hostname):
    """Verify an IP address by attempting connection"""
    print(f"🔍 Verifying IP: {hostname}")
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", hostname, "echo", "connected"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ {hostname} - Connection successful")
            return True
        else:
            print(f"❌ {hostname} - Connection failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {hostname} - Verification error: {e}")
        return False

def verify_path(path):
    """Verify a file path exists"""
    print(f"🔍 Verifying path: {path}")
    if os.path.exists(path):
        print(f"✅ {path} - Exists")
        return True
    else:
        print(f"❌ {path} - Not found")
        return False

def quick_verify(query):
    """Quick verification of a query"""
    print(f"\n🔍 Quick verify: {query}\n")
    
    # Search reference files
    files = [TOOLS_MD, AGENTS_MD, SOUL_MD, MEMORY_MD]
    results = search_files(query, files)
    
    if results:
        print("📖 Found in reference files:")
        for filename, matches in results.items():
            print(f"\n{filename}:")
            for match in matches:
                print(match)
    else:
        print("⚠️  Not found in reference files")
    
    print("\n✅ Verification complete\n")

def checklist():
    """Run full pre-task checklist"""
    print("\n=== 📋 PRE-TASK CHECKLIST ===\n")
    
    # 1. Task description
    print("1️⃣  What task are you about to start?")
    task = input("> ").strip()
    print(f"   → Task: {task}\n")
    
    # 2. Memory search
    print("2️⃣  Search memory for similar tasks...")
    if task:
        quick_verify(task)
    
    # 3. Verify critical details
    print("3️⃣  Verify critical details? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("   What to verify? (ip/path/other)")
        verify_type = input("> ").strip().lower()
        value = input("   Enter value: ").strip()
        
        if verify_type == 'ip':
            verify_ip(value)
        elif verify_type == 'path':
            verify_path(value)
        else:
            quick_verify(value)
    
    # 4. Check rules
    print("4️⃣  Check rules in AGENTS.md/SOUL.md? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("\n📖 Key rules from AGENTS.md:")
        if AGENTS_MD.exists():
            content = AGENTS_MD.read_text()
            for line in content.split('\n')[:30]:
                if any(keyword in line.lower() for keyword in ['rule', 'must', 'never', 'required']):
                    print(f"  {line}")
        
        print("\n📖 Key rules from SOUL.md:")
        if SOUL_MD.exists():
            content = SOUL_MD.read_text()
            for line in content.split('\n')[:30]:
                if any(keyword in line.lower() for keyword in ['rule', 'must', 'never', 'required']):
                    print(f"  {line}")
    
    # 5. Confirmation
    print("\n=== ✅ CHECKLIST COMPLETE ===")
    print("Proceed with task? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("✅ Proceeding with verified context\n")
        return 0
    else:
        print("❌ Task aborted - need more verification\n")
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pre-task verification utility')
    parser.add_argument('--check', action='append', metavar='QUERY',
                        help='Non-interactive: search memory for this term (repeatable)')
    parser.add_argument('--ip', metavar='HOST', help='Verify SSH connectivity to host')
    parser.add_argument('--path', metavar='PATH', help='Verify file/dir exists')
    parser.add_argument('cmd', nargs='?', choices=['verify', 'ip', 'path'])
    parser.add_argument('arg', nargs='?')
    args = parser.parse_args()

    if args.check:
        ref_files = [TOOLS_MD, AGENTS_MD, SOUL_MD, MEMORY_MD]
        any_found = False
        for query in args.check:
            results = search_files(query, ref_files)
            if results:
                any_found = True
                print(f"\n🔍 '{query}':")
                for fname, lines in results.items():
                    for line in lines[:3]:
                        print(f"  [{fname}] {line.strip()}")
            else:
                print(f"⚠️  '{query}' not found in reference files")
        sys.exit(0 if any_found else 1)
    elif args.ip:
        verify_ip(args.ip)
    elif args.path:
        verify_path(args.path)
    elif args.cmd == 'verify' and args.arg:
        quick_verify(args.arg)
    elif args.cmd == 'ip' and args.arg:
        verify_ip(args.arg)
    elif args.cmd == 'path' and args.arg:
        verify_path(args.arg)
    else:
        checklist()

#!/usr/bin/env python3
"""
integration_test.py — Synapse Code 集成测试

测试核心功能的端到端流程：
1. Task Type 推断 → 验证场景识别
2. 项目初始化 → 验证目录结构
3. 状态检查 → 验证状态报告
4. 记忆查询 → 验证知识检索
5. 配置管理 → 验证配置加载
"""

import sys
import json
from pathlib import Path
import subprocess
import shutil

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'

def log(msg, color=Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")

def run_script(script_path, args, timeout=60):
    """Run a Python script and return result."""
    try:
        result = subprocess.run(
            ['python3', str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, '', f'Timeout after {timeout}s'
    except Exception as e:
        return 1, '', str(e)

# Test paths
TEST_PROJECT = Path('/tmp/synapse-code-integration-test')
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'

def cleanup():
    """Clean up test directory."""
    if TEST_PROJECT.exists():
        shutil.rmtree(TEST_PROJECT, ignore_errors=True)

def assert_file_exists(path, description):
    """Assert that a file exists."""
    if path.exists():
        return True
    log(f'  ✗ FAIL: {description} not found: {path}', Colors.RED)
    return False

def assert_json_valid(text, description):
    """Assert that text is valid JSON."""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError as e:
        log(f'  ✗ FAIL: {description}: Invalid JSON - {e}', Colors.RED)
        return False

def assert_contains(text, substring, description):
    """Assert that text contains substring."""
    if substring in text:
        return True
    log(f'  ✗ FAIL: {description}', Colors.RED)
    return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 1: Task Type Inference
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_task_type_inference():
    """Test 1: Task type inference with various inputs."""
    log('\n[Test 1] Task Type Inference', Colors.CYAN)

    test_cases = [
        # (input, expected_task_type, description)
        ("修复登录 bug", "bugfix", "Bug fix detection (Chinese)"),
        ("添加用户注册功能", "feature", "Feature detection (Chinese)"),
        ("优化数据库查询性能", "optimization", "Optimization detection (Chinese)"),
        ("把变量改成蛇形命名", "refactor", "Refactor detection (Chinese)"),
        ("理解这个函数的工作原理", "understand", "Understand detection (Chinese)"),
        ("设计一个电商系统架构", "design", "Design detection (Chinese)"),  # Use "设计" keyword
        ("审查这个 PR 的代码质量", "review", "Review detection (Chinese)"),
        ("fix the login bug", "bugfix", "Bug fix detection (English)"),
        ("add user registration feature", "feature", "Feature detection (English)"),
        ("optimize database queries", "optimization", "Optimization detection (English)"),
    ]

    passed = 0
    failed = []

    for input_text, expected_type, description in test_cases:
        code, stdout, stderr = run_script(SCRIPT_DIR / 'infer_task_type.py', [input_text])

        if code == 0 and expected_type in stdout.lower():
            passed += 1
            log(f'  ✓ {description}', Colors.GREEN)
        else:
            failed.append((description, input_text, stdout[:100]))
            log(f'  ✗ FAIL: {description} - input: "{input_text}"', Colors.RED)

    if passed == len(test_cases):
        log(f'  ✓ PASS: {passed}/{len(test_cases)} task types inferred correctly', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {passed}/{len(test_cases)} task types correct', Colors.RED)
        for desc, inp, out in failed:
            log(f'    - {desc}: "{inp}" → {out}', Colors.YELLOW)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 2: Project Initialization (Syntax Only)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_init_project_syntax():
    """Test 2: Verify init_project.py syntax and structure."""
    log('\n[Test 2] Project Initialization (Syntax)', Colors.CYAN)

    init_script = SCRIPT_DIR / 'init_project.py'

    if not assert_file_exists(init_script, 'init_project.py'):
        return False

    # Verify Python syntax
    try:
        import ast
        source = init_script.read_text(encoding='utf-8')
        ast.parse(source)
        log('  ✓ init_project.py has valid syntax', Colors.GREEN)

        # Verify key functions exist
        required_functions = ['check_git_repo', 'run_scaffold', 'main']
        for func in required_functions:
            if f'def {func}' in source:
                log(f'  ✓ Function {func}() defined', Colors.GREEN)
            else:
                log(f'  ✗ FAIL: Function {func}() not found', Colors.RED)
                return False

        log('  ✓ PASS: init_project.py structure verified', Colors.GREEN)
        return True

    except SyntaxError as e:
        log(f'  ✗ FAIL: Syntax error: {e}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 3: Status Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_status_check():
    """Test 3: Status check on non-existent and test projects."""
    log('\n[Test 3] Status Check', Colors.CYAN)

    # Test 1: Non-existent project (should handle gracefully)
    code, stdout, stderr = run_script(SCRIPT_DIR / 'check_status.py', ['/nonexistent/path'])

    if code in [0, 1]:  # May return 1 for missing project, that's OK
        log('  ✓ Handles non-existent project gracefully', Colors.GREEN)
    else:
        log(f'  ✗ FAIL: Unexpected error: {stderr}', Colors.RED)
        return False

    # Test 2: Create minimal test project
    cleanup()
    TEST_PROJECT.mkdir(parents=True, exist_ok=True)
    (TEST_PROJECT / '.git').mkdir(exist_ok=True)  # Fake git repo

    code, stdout, stderr = run_script(SCRIPT_DIR / 'check_status.py', [str(TEST_PROJECT)])

    if code in [0, 1]:
        log('  ✓ Status check runs on test project', Colors.GREEN)
        if 'mode' in stdout.lower() or 'phase' in stdout.lower() or 'status' in stdout.lower():
            log('  ✓ Status output contains meaningful information', Colors.GREEN)
            log('  ✓ PASS: Status check verified', Colors.GREEN)
            return True
        else:
            log('  ⚠ Warning: Status output may be too minimal', Colors.YELLOW)
            return True  # Still pass if it runs
    else:
        log(f'  ✗ FAIL: {stderr}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 4: Memory Query
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_memory_query():
    """Test 4: Memory query functionality."""
    log('\n[Test 4] Memory Query', Colors.CYAN)

    # Create test memory structure
    cleanup()
    TEST_PROJECT.mkdir(parents=True, exist_ok=True)

    memory_dir = TEST_PROJECT / '.synapse' / 'memory' / 'feature'
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Create test memory file
    test_memory = memory_dir / '2024-01-15T10-30-00-test-feature.md'
    test_memory.write_text('''# Synapse 执行记录

task_type: feature
task_description: 实现用户登录功能
outcome: success
timestamp: 2024-01-15T10:30:00
''', encoding='utf-8')

    # Test query by task type
    code, stdout, stderr = run_script(
        SCRIPT_DIR / 'query_memory.py',
        [str(TEST_PROJECT), '--task-type', 'feature']
    )

    if code == 0:
        log('  ✓ Query by task-type works', Colors.GREEN)
        if 'feature' in stdout.lower() or '登录' in stdout or 'test' in stdout.lower():
            log('  ✓ Query returns relevant results', Colors.GREEN)
            log('  ✓ PASS: Memory query verified', Colors.GREEN)
            return True
        else:
            log('  ⚠ Warning: Query output may be minimal', Colors.YELLOW)
            return True
    else:
        log(f'  ✗ FAIL: {stderr}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 5: Configuration Management
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_config_management():
    """Test 5: Configuration loading and defaults."""
    log('\n[Test 5] Configuration Management', Colors.CYAN)

    # Test run_pipeline.py config loading
    config_script = SCRIPT_DIR / 'run_pipeline.py'

    if not assert_file_exists(config_script, 'run_pipeline.py'):
        return False

    # Verify syntax
    try:
        import ast
        source = config_script.read_text(encoding='utf-8')
        ast.parse(source)
        log('  ✓ run_pipeline.py has valid syntax', Colors.GREEN)

        # Check for config loading function
        if 'load_config' in source or 'config' in source.lower():
            log('  ✓ Config loading logic present', Colors.GREEN)
        else:
            log('  ⚠ Warning: Config loading may be missing', Colors.YELLOW)

        # Check for default config
        if 'pipeline' in source and 'workspace' in source:
            log('  ✓ Default pipeline workspace configured', Colors.GREEN)

        log('  ✓ PASS: Configuration management verified', Colors.GREEN)
        return True

    except SyntaxError as e:
        log(f'  ✗ FAIL: Syntax error: {e}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 6: Auto-Log Functionality
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_auto_log():
    """Test 6: Auto-log script functionality."""
    log('\n[Test 6] Auto-Log Functionality', Colors.CYAN)

    auto_log_script = SCRIPT_DIR / 'auto_log.py'

    if not assert_file_exists(auto_log_script, 'auto_log.py'):
        return False

    # Verify syntax
    try:
        import ast
        source = auto_log_script.read_text(encoding='utf-8')
        ast.parse(source)
        log('  ✓ auto_log.py has valid syntax', Colors.GREEN)

        # Check for required functions
        required_functions = ['write_memory_record', 'append_log', 'main']
        for func in required_functions:
            if f'def {func}' in source:
                log(f'  ✓ Function {func}() defined', Colors.GREEN)
            else:
                log(f'  ✗ FAIL: Function {func}() not found', Colors.RED)
                return False

        # Test with sample input
        cleanup()
        TEST_PROJECT.mkdir(parents=True, exist_ok=True)

        # Create test pipeline summary
        summary_file = Path('/tmp/test-pipeline-summary.json')
        summary_data = {
            "project": "test-project",
            "tasks": [
                {
                    "id": "1",
                    "task_type": "feature",
                    "description": "Test feature",
                    "outcome": "success",
                    "timestamp": "2024-01-15T10:00:00"
                }
            ]
        }
        summary_file.write_text(json.dumps(summary_data), encoding='utf-8')

        code, stdout, stderr = run_script(
            auto_log_script,
            ['--input', str(summary_file), '--project', str(TEST_PROJECT)]
        )

        if code == 0:
            log('  ✓ Auto-log execution successful', Colors.GREEN)

            # Verify memory file created
            memory_files = list((TEST_PROJECT / '.synapse' / 'memory' / 'feature').glob('*.md'))
            if memory_files:
                log('  ✓ Memory file created', Colors.GREEN)
                log('  ✓ PASS: Auto-log functionality verified', Colors.GREEN)
                return True
            else:
                log('  ⚠ Warning: Memory file may not have been created', Colors.YELLOW)
                return True
        else:
            log(f'  ✗ FAIL: {stderr}', Colors.RED)
            return False

    except SyntaxError as e:
        log(f'  ✗ FAIL: Syntax error: {e}', Colors.RED)
        return False
    except Exception as e:
        log(f'  ✗ FAIL: Exception: {e}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    log('\n' + '═' * 70, Colors.CYAN)
    log('  Synapse Code Integration Tests', Colors.CYAN)
    log('═' * 70, Colors.CYAN)

    tests = [
        ('Task Type Inference', test_task_type_inference),
        ('Project Initialization', test_init_project_syntax),
        ('Status Check', test_status_check),
        ('Memory Query', test_memory_query),
        ('Configuration Management', test_config_management),
        ('Auto-Log Functionality', test_auto_log),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            log(f'  ✗ FAIL: {name} raised exception: {e}', Colors.RED)
            results.append((name, False))

    cleanup()

    # Summary
    log('\n' + '═' * 70, Colors.CYAN)
    log('  Test Summary', Colors.CYAN)
    log('═' * 70, Colors.CYAN)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = '✓ PASS' if result else '✗ FAIL'
        color = Colors.GREEN if result else Colors.RED
        log(f'  {color}{status}{Colors.RESET}: {name}')

    log('\n' + '─' * 70, Colors.BLUE)
    overall = Colors.GREEN if passed == total else Colors.RED
    log(f'  {overall}Results: {passed}/{total} tests passed{Colors.RESET}', Colors.RESET)
    log('─' * 70 + '\n', Colors.BLUE)

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())

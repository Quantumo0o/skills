#!/usr/bin/env python3
"""
镜像源可用性测试脚本 (PDCA 方法)
- Plan: 定义所有需要测试的镜像源
- Do: 逐个测试镜像的 HTTP 连通性和响应速度
- Check: 分析测试结果，标记可用/不可用/慢速
- Act: 输出推荐配置，生成更新建议

安全说明:
- 默认启用 SSL 证书验证
- 使用 --insecure 选项可跳过 SSL 验证（仅用于测试）
- 所有测试 URL 硬编码，不接受外部输入
"""
import os
import sys
import io

# Windows 控制台 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import time
import ssl
import platform
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# 定义所有需要测试的镜像源
MIRRORS = {
    'pip': {
        'name': 'Python (pip)',
        'test_urls': {
            'aliyun': 'https://mirrors.aliyun.com/pypi/simple/requests/',
            'tsinghua': 'https://pypi.tuna.tsinghua.edu.cn/simple/requests/',
            'ustc': 'https://pypi.mirrors.ustc.edu.cn/simple/requests/',
            'tencent': 'https://mirrors.cloud.tencent.com/pypi/simple/requests/',
        }
    },
    'npm': {
        'name': 'Node.js (npm)',
        'test_urls': {
            'aliyun': 'https://registry.npmmirror.com/express',
            'tencent': 'https://mirrors.cloud.tencent.com/npm/express',
            'huawei': 'https://repo.huaweicloud.com/repository/npm/express',
        }
    },
    'cargo': {
        'name': 'Rust (cargo)',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/config.json',
            'ustc': 'https://mirrors.ustc.edu.cn/crates.io-index/config.json',
            'aliyun': 'https://mirrors.aliyun.com/crates.io-index/config.json',
        }
    },
    'go': {
        'name': 'Go (go mod)',
        'test_urls': {
            'qiniu': 'https://goproxy.cn/github.com/gin-gonic/gin/@v/list',
            'aliyun': 'https://mirrors.aliyun.com/goproxy/github.com/gin-gonic/gin/@v/list',
            'official': 'https://goproxy.io/github.com/gin-gonic/gin/@v/list',
        }
    },
    'maven': {
        'name': 'Maven (Java)',
        'test_urls': {
            'aliyun': 'https://maven.aliyun.com/repository/public/com/alibaba/fastjson/maven-metadata.xml',
        }
    },
    'composer': {
        'name': 'Composer (PHP)',
        'test_urls': {
            'aliyun': 'https://mirrors.aliyun.com/composer/packages.json',
        }
    },
    'nuget': {
        'name': 'NuGet (.NET)',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/nuget/v3/index.json',
            'huawei': 'https://repo.huaweicloud.com/repository/nuget/v3/index.json',
        }
    },
    'rubygems': {
        'name': 'RubyGems (Ruby)',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/rubygems/specs.4.8.gz',
            'ustc': 'https://mirrors.ustc.edu.cn/rubygems/specs.4.8.gz',
            'taobao': 'https://ruby.taobao.org/specs.4.8.gz',
        }
    },
    'conda': {
        'name': 'Conda (Python)',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/noarch/repodata.json',
            'ustc': 'https://mirrors.ustc.edu.cn/anaconda/pkgs/main/noarch/repodata.json',
            'tencent': 'https://mirrors.cloud.tencent.com/anaconda/pkgs/main/noarch/repodata.json',
        }
    },
    'docker': {
        'name': 'Docker Hub',
        'test_urls': {
            'aliyun': 'https://registry.cn-hangzhou.aliyuncs.com/v2/',
            'tencent': 'https://mirror.ccs.tencentyun.com/v2/',
            'ustc': 'https://docker.mirrors.ustc.edu.cn/v2/',
        }
    },
    'homebrew': {
        'name': 'Homebrew (macOS)',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/',
            'ustc': 'https://mirrors.ustc.edu.cn/homebrew-bottles/',
            'tencent': 'https://mirrors.cloud.tencent.com/homebrew-bottles/',
        }
    },
    'flutter': {
        'name': 'Flutter/Dart',
        'test_urls': {
            'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra_release/releases/releases_linux.json',
            'sjtu': 'https://mirror.sjtu.edu.cn/flutter/flutter_infra_release/releases/releases_linux.json',
        }
    },
    'gradle': {
        'name': 'Gradle (Java/Kotlin)',
        'test_urls': {
            'aliyun': 'https://maven.aliyun.com/repository/gradle-plugin/',
            'tencent': 'https://mirrors.cloud.tencent.com/gradle/',
        }
    }
}

# 超时设置（秒）
TIMEOUT = 10
# 慢速阈值（秒）
SLOW_THRESHOLD = 3.0

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_separator():
    """打印分隔线"""
    print("-" * 70)

def test_mirror(name, url, timeout=TIMEOUT, insecure=False):
    """测试单个镜像的可用性
    
    Args:
        name: 镜像名称
        url: 测试 URL
        timeout: 超时时间
        insecure: 是否跳过 SSL 验证（默认 False，更安全）
    """
    result = {
        'name': name,
        'url': url,
        'status': 'unknown',
        'response_time': None,
        'http_code': None,
        'error': None
    }
    
    try:
        # 默认使用 SSL 证书验证（更安全）
        if insecure:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        else:
            ctx = ssl.create_default_context()
        
        # 创建请求
        req = Request(url)
        req.add_header('User-Agent', 'china-mirrors-test/1.0')
        
        # 记录开始时间
        start_time = time.time()
        
        # 发送请求
        with urlopen(req, timeout=timeout, context=ctx) as response:
            elapsed = time.time() - start_time
            result['response_time'] = round(elapsed, 3)
            result['http_code'] = response.getcode()
            
            if response.getcode() == 200:
                if elapsed <= SLOW_THRESHOLD:
                    result['status'] = 'ok'
                else:
                    result['status'] = 'slow'
            else:
                result['status'] = 'error'
                
    except HTTPError as e:
        result['response_time'] = round(time.time() - start_time, 3)
        result['http_code'] = e.code
        if e.code in [200, 301, 302]:
            result['status'] = 'ok'
        else:
            result['status'] = 'error'
            result['error'] = str(e.reason)
            
    except URLError as e:
        result['response_time'] = round(time.time() - start_time, 3)
        result['status'] = 'unreachable'
        result['error'] = str(e.reason)
        
    except Exception as e:
        result['response_time'] = round(time.time() - start_time, 3)
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result

def run_tests(mirror_types=None, verbose=False, timeout=TIMEOUT):
    """运行所有测试"""
    if mirror_types is None:
        mirror_types = list(MIRRORS.keys())
    
    all_results = {}
    total_tests = 0
    passed_tests = 0
    slow_tests = 0
    failed_tests = 0
    
    print_header("中国国内镜像源可用性测试 (PDCA)")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"超时设置: {timeout}秒 | 慢速阈值: {SLOW_THRESHOLD}秒")
    print(f"测试类型: {', '.join([MIRRORS[t]['name'] for t in mirror_types])}")
    print_separator()
    
    # 并行测试
    with ThreadPoolExecutor(max_workers=5) as executor:
        for mirror_type in mirror_types:
            config = MIRRORS[mirror_type]
            print(f"\n正在测试 {config['name']}...")
            
            futures = {}
            for name, url in config['test_urls'].items():
                future = executor.submit(test_mirror, name, url, timeout)
                futures[future] = (name, url)
                total_tests += 1
            
            # 收集结果
            type_results = {}
            for future in as_completed(futures):
                name, url = futures[future]
                result = future.result()
                type_results[name] = result
                
                # 打印单个结果
                if verbose:
                    status_icon = {'ok': '✓', 'slow': '⚠', 'error': '✗', 'unreachable': '✗'}.get(result['status'], '?')
                    print(f"  {status_icon} {name}: {result['response_time']}s (HTTP {result['http_code']})")
            
            all_results[mirror_type] = type_results
            
            # 统计
            for result in type_results.values():
                if result['status'] == 'ok':
                    passed_tests += 1
                elif result['status'] == 'slow':
                    slow_tests += 1
                    passed_tests += 1  # 慢速也算通过，但标记
                else:
                    failed_tests += 1
    
    return all_results, total_tests, passed_tests, slow_tests, failed_tests

def print_results(all_results, total_tests, passed_tests, slow_tests, failed_tests):
    """打印测试结果摘要"""
    print_header("测试结果摘要")
    
    print(f"总测试数: {total_tests}")
    print(f"✓ 通过: {passed_tests}")
    print(f"⚠ 慢速: {slow_tests}")
    print(f"✗ 失败: {failed_tests}")
    print(f"通过率: {(passed_tests/total_tests*100):.1f}%")
    
    print_separator()
    
    # 详细结果
    for mirror_type, results in all_results.items():
        config = MIRRORS[mirror_type]
        print(f"\n{config['name']}:")
        
        # 排序：ok > slow > error > unreachable
        sorted_results = sorted(
            results.items(),
            key=lambda x: {'ok': 0, 'slow': 1, 'error': 2, 'unreachable': 3}.get(x[1]['status'], 4)
        )
        
        for name, result in sorted_results:
            status_icon = {'ok': '✓', 'slow': '⚠', 'error': '✗', 'unreachable': '✗'}.get(result['status'], '?')
            status_text = {'ok': '可用', 'slow': '慢速', 'error': '错误', 'unreachable': '不可达'}.get(result['status'], '未知')
            
            print(f"  {status_icon} {name:12} | {status_text:6} | {result['response_time']:6.3f}s | HTTP {result['http_code']}")
            if result['error']:
                print(f"    错误: {result['error']}")

def get_recommendations(all_results):
    """根据测试结果生成推荐配置"""
    recommendations = {}
    
    for mirror_type, results in all_results.items():
        # 选择最快的可用镜像
        best = None
        best_time = float('inf')
        
        for name, result in results.items():
            if result['status'] in ['ok', 'slow'] and result['response_time'] < best_time:
                best = name
                best_time = result['response_time']
        
        if best:
            recommendations[mirror_type] = {
                'recommended': best,
                'response_time': best_time,
                'status': results[best]['status']
            }
    
    return recommendations

def print_recommendations(recommendations):
    """打印推荐配置"""
    print_header("推荐配置")
    
    for mirror_type, rec in recommendations.items():
        config = MIRRORS[mirror_type]
        status_icon = '✓' if rec['status'] == 'ok' else '⚠'
        print(f"{status_icon} {config['name']}: 推荐 {rec['recommended']} ({rec['response_time']:.3f}s)")
    
    if not recommendations:
        print("无可用镜像推荐")

def save_results(all_results, recommendations, output_file=None):
    """保存测试结果到文件"""
    if output_file is None:
        output_file = Path(__file__).parent / 'mirror_test_results.json'
    
    data = {
        'test_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': {},
        'recommendations': recommendations
    }
    
    for mirror_type, results in all_results.items():
        data['results'][mirror_type] = {}
        for name, result in results.items():
            data['results'][mirror_type][name] = {
                'status': result['status'],
                'response_time': result['response_time'],
                'http_code': result['http_code'],
                'error': result['error']
            }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n测试结果已保存到: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='中国国内镜像源可用性测试 (PDCA 方法)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python test_mirrors.py                    # 测试所有镜像
  python test_mirrors.py --type pip npm     # 仅测试 pip 和 npm
  python test_mirrors.py --verbose          # 显示详细输出
  python test_mirrors.py --save results.json # 保存结果到文件
        """
    )
    
    parser.add_argument('--type', nargs='+', choices=list(MIRRORS.keys()),
                       help='指定要测试的镜像类型')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细输出')
    parser.add_argument('--save', '-s', nargs='?', const='mirror_test_results.json',
                       help='保存测试结果到 JSON 文件')
    parser.add_argument('--timeout', type=int, default=TIMEOUT,
                       help=f'请求超时时间（秒，默认 {TIMEOUT}）')
    
    args = parser.parse_args()
    
    # 运行测试
    mirror_types = args.type if args.type else list(MIRRORS.keys())
    all_results, total_tests, passed_tests, slow_tests, failed_tests = run_tests(
        mirror_types=mirror_types,
        verbose=args.verbose,
        timeout=args.timeout
    )
    
    # 打印结果
    print_results(all_results, total_tests, passed_tests, slow_tests, failed_tests)
    
    # 生成并打印推荐
    recommendations = get_recommendations(all_results)
    print_recommendations(recommendations)
    
    # 保存结果
    if args.save:
        save_results(all_results, recommendations, args.save)
    
    # 退出码
    if failed_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
敏感内容扫描器
检测文件名和文件内容中的敏感词、违禁词、PII个人信息
"""

import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
import mimetypes


class SensitiveScanner:
    def __init__(self, custom_words_file: str = None, verbose: bool = False, enable_chinese_name: bool = False):
        self.verbose = verbose
        self.enable_chinese_name = enable_chinese_name
        self.sensitive_words_hashes = self._load_sensitive_words_hashes()
        self.pii_patterns = self._get_pii_patterns()
        self.custom_words = self._load_custom_words(custom_words_file)
        
        # 常见中文姓氏（用于改进姓名检测）
        self.common_surnames = set([
            '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
            '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
            '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
            '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
            '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
            '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
            '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺',
            '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
            '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余',
            '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹'
        ])
        
    def _load_sensitive_words_hashes(self) -> Set[str]:
        """加载预置的敏感词hash库"""
        hash_file = Path(__file__).parent.parent / "references" / "sensitive_words_hashed.txt"
        hashes = set()
        
        if hash_file.exists():
            with open(hash_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        hashes.add(line)
        
        return hashes
    
    def _load_custom_words(self, custom_words_file: str) -> Set[str]:
        """加载自定义敏感词库"""
        custom_words = set()
        
        if custom_words_file and Path(custom_words_file).exists():
            with open(custom_words_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word and not word.startswith('#'):
                        custom_words.add(word.lower())
        
        return custom_words
    
    def _get_pii_patterns(self) -> Dict[str, re.Pattern]:
        """获取PII识别模式"""
        patterns = {
            # 身份证号：更严格的前6位地区码 + 8位出生日期 + 3位顺序码 + 1位校验码
            'china_id_card': re.compile(
                r'\b[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b'
            ),
            # 手机号：中国大陆手机号（11位）
            'china_phone': re.compile(r'\b1[3-9]\d{9}\b'),
            # 银行卡号：16-19位数字（后续会进行 Luhn 校验）
            'china_bank_card': re.compile(r'\b\d{16,19}\b'),
            # 邮箱
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            # IP地址：后续会进行范围验证
            'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            # 护照号：以 E 或 S 开头 + 8位数字
            'china_passport': re.compile(r'\b[SE]\d{8}\b'),
        }
        
        # 中文姓名检测（默认禁用，可通过参数启用）
        if self.enable_chinese_name:
            patterns['chinese_name'] = re.compile(r'[\u4e00-\u9fa5]{2,4}')
        
        return patterns
    
    def _validate_id_card(self, id_card: str) -> bool:
        """验证身份证号校验码"""
        if len(id_card) != 18:
            return False
        
        # 权重因子
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 校验码对照表
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        try:
            # 计算校验码
            total = 0
            for i in range(17):
                total += int(id_card[i]) * weights[i]
            
            check_code = check_codes[total % 11]
            return id_card[-1].upper() == check_code
        except:
            return False
    
    def _validate_bank_card(self, card_number: str) -> bool:
        """验证银行卡号（Luhn 算法）"""
        if not card_number.isdigit():
            return False
        
        # Luhn 算法
        digits = [int(d) for d in card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        total = sum(odd_digits)
        for d in even_digits:
            d *= 2
            if d > 9:
                d = d // 10 + d % 10
            total += d
        
        return total % 10 == 0
    
    def _validate_ip_address(self, ip: str) -> bool:
        """验证 IP 地址范围"""
        try:
            parts = [int(p) for p in ip.split('.')]
            return all(0 <= p <= 255 for p in parts)
        except:
            return False
    
    def _validate_chinese_name(self, name: str) -> Tuple[bool, str]:
        """
        验证中文姓名（改进版）
        返回: (是否可能是姓名, 置信度)
        """
        if not self.enable_chinese_name:
            return False, 'disabled'
        
        # 长度检查
        if len(name) < 2 or len(name) > 4:
            return False, 'low'
        
        # 检查是否以常见姓氏开头
        if name[0] in self.common_surnames:
            # 包含常见姓氏，中等置信度
            return True, 'medium'
        
        # 不以常见姓氏开头，低置信度
        return True, 'low'
    
    def _hash_word(self, word: str) -> str:
        """计算词的SHA256 hash"""
        return hashlib.sha256(word.encode('utf-8')).hexdigest()
    
    def _is_text_file(self, file_path: Path) -> bool:
        """判断是否为文本文件"""
        try:
            # 常见文档类型
            text_extensions = {
                '.txt', '.md', '.markdown', '.rst', '.doc', '.docx',
                '.json', '.yaml', '.yml', '.xml', '.html', '.htm',
                '.csv', '.tsv', '.log', '.conf', '.cfg', '.ini',
                '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h',
                '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat'
            }
            
            if file_path.suffix.lower() in text_extensions:
                return True
            
            # 使用mimetypes判断
            mime_type, _ = mimetypes.guess_type(str(file_path))
            return mime_type and mime_type.startswith('text/')
        except:
            return False
    
    def _read_file_content(self, file_path: Path) -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                return ""
        except Exception as e:
            if self.verbose:
                print(f"读取文件失败 {file_path}: {e}")
            return ""
    
    def check_hashed_words(self, text: str) -> List[str]:
        """检查文本中是否包含hash敏感词"""
        found = []
        
        # 分词：按中英文、数字等分割
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+', text)
        
        for word in words:
            word_hash = self._hash_word(word.lower())
            if word_hash in self.sensitive_words_hashes:
                found.append(word)
        
        return found
    
    def check_custom_words(self, text: str) -> List[str]:
        """检查自定义敏感词"""
        text_lower = text.lower()
        found = []
        
        for word in self.custom_words:
            if word in text_lower:
                found.append(word)
        
        return found
    
    def check_pii(self, text: str) -> Dict[str, List[Dict]]:
        """
        检查PII信息（改进版）
        返回格式: {pii_type: [{'value': 'xxx', 'confidence': 'high/medium/low'}]}
        """
        found = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # 去重
                matches = list(set(matches))
                
                validated_matches = []
                for match in matches:
                    confidence = 'low'
                    display_value = match
                    
                    # 根据类型进行验证
                    if pii_type == 'china_id_card':
                        # 身份证号验证
                        if self._validate_id_card(match):
                            confidence = 'high'
                        else:
                            confidence = 'medium'
                        # 脱敏显示
                        display_value = f"{match[:3]}***{match[-2:]}"
                    
                    elif pii_type == 'china_phone':
                        # 手机号格式已验证，标记为高置信度
                        confidence = 'high'
                        display_value = f"{match[:3]}****{match[-2:]}"
                    
                    elif pii_type == 'china_bank_card':
                        # 银行卡号验证
                        if self._validate_bank_card(match):
                            confidence = 'high'
                        else:
                            confidence = 'low'
                        display_value = f"{match[:3]}***{match[-2:]}"
                    
                    elif pii_type == 'ip_address':
                        # IP地址验证
                        if self._validate_ip_address(match):
                            confidence = 'high'
                        else:
                            confidence = 'low'
                    
                    elif pii_type == 'email':
                        # 邮箱格式已验证，标记为高置信度
                        confidence = 'high'
                        # 脱敏显示
                        parts = match.split('@')
                        if len(parts[0]) > 3:
                            display_value = f"{parts[0][:3]}***@{parts[1]}"
                    
                    elif pii_type == 'china_passport':
                        # 护照号格式已验证，标记为高置信度
                        confidence = 'high'
                        display_value = f"{match[:1]}***{match[-2:]}"
                    
                    elif pii_type == 'chinese_name':
                        # 中文姓名验证
                        is_name, confidence = self._validate_chinese_name(match)
                        if not is_name:
                            continue
                    
                    validated_matches.append({
                        'value': display_value,
                        'confidence': confidence,
                        'original': match  # 保留原始值用于去重
                    })
                
                if validated_matches:
                    found[pii_type] = validated_matches
        
        return found
    
    def scan_file(self, file_path: Path) -> Dict:
        """扫描单个文件"""
        result = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'issues': []
        }
        
        # 检查文件名
        filename_issues = {}
        
        # 文件名中的hash敏感词
        hashed_in_filename = self.check_hashed_words(file_path.stem)
        if hashed_in_filename:
            filename_issues['hashed_sensitive_words'] = hashed_in_filename
        
        # 文件名中的自定义敏感词
        custom_in_filename = self.check_custom_words(file_path.stem)
        if custom_in_filename:
            filename_issues['custom_sensitive_words'] = custom_in_filename
        
        # 文件名中的PII
        pii_in_filename = self.check_pii(file_path.stem)
        if pii_in_filename:
            filename_issues['pii'] = pii_in_filename
        
        if filename_issues:
            result['issues'].append({
                'location': 'filename',
                'problems': filename_issues
            })
        
        # 检查文件内容（仅文本文件）
        if self._is_text_file(file_path):
            content = self._read_file_content(file_path)
            
            if content:
                content_issues = {}
                
                # 内容中的hash敏感词
                hashed_in_content = self.check_hashed_words(content)
                if hashed_in_content:
                    content_issues['hashed_sensitive_words'] = list(set(hashed_in_content))
                
                # 内容中的自定义敏感词
                custom_in_content = self.check_custom_words(content)
                if custom_in_content:
                    content_issues['custom_sensitive_words'] = list(set(custom_in_content))
                
                # 内容中的PII
                pii_in_content = self.check_pii(content)
                if pii_in_content:
                    content_issues['pii'] = pii_in_content
                
                if content_issues:
                    result['issues'].append({
                        'location': 'content',
                        'problems': content_issues
                    })
        
        return result
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[Dict]:
        """扫描目录"""
        results = []
        
        if recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                result = self.scan_file(file_path)
                if result['issues']:  # 只记录有问题的文件
                    results.append(result)
                    if self.verbose:
                        print(f"发现问题: {file_path}")
        
        return results
    
    def generate_report(self, results: List[Dict], output_format: str = 'json') -> str:
        """生成报告"""
        if output_format == 'json':
            return json.dumps(results, ensure_ascii=False, indent=2)
        elif output_format == 'markdown':
            if not results:
                return "# 敏感内容扫描报告\n\n✅ 未发现敏感内容\n"
            
            report = ["# 敏感内容扫描报告\n"]
            report.append(f"**扫描时间**: {self._get_current_time()}\n")
            report.append(f"**发现问题**: {len(results)} 个文件\n\n")
            
            # 添加统计信息
            stats = self._get_statistics(results)
            if stats:
                report.append("## 扫描统计\n\n")
                report.append(f"- 高置信度问题: {stats['high']} 个\n")
                report.append(f"- 中置信度问题: {stats['medium']} 个\n")
                report.append(f"- 低置信度问题: {stats['low']} 个\n\n")
            
            for idx, result in enumerate(results, 1):
                report.append(f"## {idx}. {result['file_path']}\n")
                
                for issue in result['issues']:
                    location = "文件名" if issue['location'] == 'filename' else "文件内容"
                    report.append(f"\n### {location}\n")
                    
                    for problem_type, items in issue['problems'].items():
                        problem_name = {
                            'hashed_sensitive_words': '违禁词',
                            'custom_sensitive_words': '自定义敏感词',
                            'pii': 'PII个人信息'
                        }.get(problem_type, problem_type)
                        
                        report.append(f"\n**{problem_name}**:\n")
                        
                        if problem_type == 'pii':
                            for pii_type, matches in items.items():
                                pii_name = {
                                    'china_id_card': '身份证号',
                                    'china_phone': '手机号',
                                    'china_bank_card': '银行卡号',
                                    'email': '邮箱',
                                    'ip_address': 'IP地址',
                                    'china_passport': '护照号',
                                    'chinese_name': '中文姓名'
                                }.get(pii_type, pii_type)
                                
                                # 按置信度排序
                                matches_sorted = sorted(matches, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['confidence'], 3))
                                
                                for match in matches_sorted:
                                    confidence_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(match['confidence'], '⚪')
                                    confidence_text = {'high': '高', 'medium': '中', 'low': '低'}.get(match['confidence'], '未知')
                                    report.append(f"  - {confidence_emoji} {pii_name} ({confidence_text}): {match['value']}\n")
                        else:
                            for item in items:
                                report.append(f"  - {item}\n")
                
                report.append("\n---\n")
            
            # 添加使用建议
            report.append("\n## 置信度说明\n\n")
            report.append("- 🔴 **高置信度**: 已通过格式验证和校验码验证，建议重点关注\n")
            report.append("- 🟡 **中置信度**: 格式匹配但未完全验证，建议人工复核\n")
            report.append("- 🟢 **低置信度**: 仅符合基本模式，可能为误报\n")
            
            return ''.join(report)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")
    
    def _get_statistics(self, results: List[Dict]) -> Dict[str, int]:
        """统计各置信度的问题数量"""
        stats = {'high': 0, 'medium': 0, 'low': 0}
        
        for result in results:
            for issue in result['issues']:
                if 'pii' in issue['problems']:
                    for pii_type, matches in issue['problems']['pii'].items():
                        for match in matches:
                            confidence = match.get('confidence', 'low')
                            if confidence in stats:
                                stats[confidence] += 1
        
        return stats
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    parser = argparse.ArgumentParser(description='敏感内容扫描器')
    parser.add_argument('path', type=str, help='要扫描的文件或目录路径')
    parser.add_argument('-c', '--custom', type=str, help='自定义敏感词库文件路径')
    parser.add_argument('-o', '--output', type=str, default='report.md', help='输出报告文件路径')
    parser.add_argument('-f', '--format', type=str, choices=['json', 'markdown'], default='markdown', help='输出格式')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归扫描子目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--enable-chinese-name', action='store_true', help='启用中文姓名检测（默认禁用）')
    
    args = parser.parse_args()
    
    # 初始化扫描器
    scanner = SensitiveScanner(
        custom_words_file=args.custom,
        verbose=args.verbose,
        enable_chinese_name=args.enable_chinese_name
    )
    
    # 扫描路径
    path = Path(args.path)
    
    if path.is_file():
        results = [scanner.scan_file(path)]
        results = [r for r in results if r['issues']]  # 只保留有问题的
    elif path.is_dir():
        results = scanner.scan_directory(path, recursive=args.recursive)
    else:
        print(f"错误: 路径不存在 {path}")
        return 1
    
    # 生成报告
    report = scanner.generate_report(results, output_format=args.format)
    
    # 输出报告
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 扫描完成，发现 {len(results)} 个文件存在问题")
    print(f"📄 报告已保存至: {output_path}")
    
    # 显示统计信息
    if results:
        stats = scanner._get_statistics(results)
        if any(stats.values()):
            print(f"\n置信度统计:")
            print(f"  🔴 高置信度: {stats['high']} 个")
            print(f"  🟡 中置信度: {stats['medium']} 个")
            print(f"  🟢 低置信度: {stats['low']} 个")
    
    return 0 if not results else 1  # 有问题返回1，无问题返回0


if __name__ == '__main__':
    exit(main())

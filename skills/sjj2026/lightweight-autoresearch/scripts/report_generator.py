#!/usr/bin/env python3
"""
报告生成器 - 生成 HTML 可视化报告
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.report_dir = self.skill_path / "reports"
        
    def generate(self, evaluation_results: Dict, code_results: Dict = None,
                 security_results: Dict = None, performance_results: Dict = None) -> str:
        """生成完整报告"""
        
        # 创建报告目录
        self.report_dir.mkdir(exist_ok=True)
        
        # 生成报告
        report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = self.report_dir / f"report_{report_time}.html"
        
        # 构建 HTML
        html = self._build_html(
            evaluation_results,
            code_results,
            security_results,
            performance_results,
            report_time
        )
        
        # 写入文件
        report_file.write_text(html, encoding='utf-8')
        
        return str(report_file)
    
    def _build_html(self, evaluation: Dict, code: Dict, 
                    security: Dict, performance: Dict, report_time: str) -> str:
        """构建 HTML 报告"""
        
        total_score = evaluation.get("total_score", 0)
        
        # 计算综合分数
        if code and security and performance:
            comprehensive_score = (
                evaluation["total_score"] * 0.3 +
                code["quality_score"] * 0.25 +
                security["security_score"] * 0.25 +
                performance["performance_score"] * 0.2
            )
        else:
            comprehensive_score = total_score
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技能评估报告 - {self.skill_path.name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .score-section {{
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .score-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .score-circle {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4em;
            font-weight: bold;
            color: white;
            background: {self._get_score_color(comprehensive_score)};
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .score-label {{
            font-size: 1.5em;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .section {{
            padding: 40px;
            border-bottom: 1px solid #eee;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
        }}
        
        .section h2:before {{
            content: "";
            width: 5px;
            height: 30px;
            background: #667eea;
            margin-right: 15px;
            border-radius: 3px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}
        
        .metric-title {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        
        .issues-list {{
            margin-top: 20px;
        }}
        
        .issue {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }}
        
        .issue.error {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}
        
        .issue.warning {{
            background: #fff3cd;
            border-left-color: #ffc107;
        }}
        
        .issue.success {{
            background: #d4edda;
            border-left-color: #28a745;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e9ecef;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: #667eea;
            transition: width 0.3s ease;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 技能评估报告</h1>
            <p>{self.skill_path.name}</p>
            <p style="margin-top: 10px; opacity: 0.8;">生成时间: {report_time}</p>
        </div>
        
        <div class="score-section">
            <div class="score-card">
                <div class="score-circle">
                    {comprehensive_score:.0f}
                </div>
                <div class="score-label">综合评分</div>
                <p style="color: #666; margin-top: 10px;">
                    {self._get_score_description(comprehensive_score)}
                </p>
            </div>
        </div>
        
        <!-- 基础评估 -->
        {self._build_evaluation_section(evaluation)}
        
        <!-- 代码质量 -->
        {self._build_code_section(code) if code else ""}
        
        <!-- 安全检查 -->
        {self._build_security_section(security) if security else ""}
        
        <!-- 性能测试 -->
        {self._build_performance_section(performance) if performance else ""}
        
        <!-- 改进建议 -->
        {self._build_suggestions_section(evaluation, code, security)}
        
        <div class="footer">
            <p>🦞 轻量级自主优化技能 - 自动生成报告</p>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def _build_evaluation_section(self, evaluation: Dict) -> str:
        """构建评估部分"""
        details = evaluation.get("details", {})
        
        metrics_html = ""
        for category, data in details.items():
            score = data.get("score", 0)
            max_score = data.get("max_score", 100)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            metrics_html += f'''
            <div class="metric-card">
                <div class="metric-title">{self._get_category_name(category)}</div>
                <div class="metric-value">{score}/{max_score}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%"></div>
                </div>
            </div>'''
        
        return f'''
        <div class="section">
            <h2>📊 基础评估</h2>
            <div class="metrics-grid">
                {metrics_html}
            </div>
        </div>'''
    
    def _build_code_section(self, code: Dict) -> str:
        """构建代码质量部分"""
        quality_score = code.get("quality_score", 0)
        issues = code.get("issues", [])
        
        issues_html = ""
        for issue in issues[:5]:  # 只显示前5个
            issue_class = issue.get("type", "warning")
            message = issue.get("message", "")
            file_name = issue.get("file", "")
            
            issues_html += f'''
            <div class="issue {issue_class}">
                <strong>{file_name}</strong>: {message}
            </div>'''
        
        return f'''
        <div class="section">
            <h2>🔧 代码质量</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">代码质量分数</div>
                    <div class="metric-value">{quality_score}/100</div>
                </div>
            </div>
            <div class="issues-list">
                {issues_html}
            </div>
        </div>'''
    
    def _build_security_section(self, security: Dict) -> str:
        """构建安全检查部分"""
        security_score = security.get("security_score", 0)
        issues = security.get("issues", [])
        
        issues_html = ""
        for issue in issues[:5]:
            severity = issue.get("severity", "low")
            message = issue.get("message", "")
            file_name = issue.get("file", "")
            
            issue_class = "error" if severity == "high" else "warning"
            
            issues_html += f'''
            <div class="issue {issue_class}">
                <strong>{file_name}</strong>: {message}
            </div>'''
        
        if not issues:
            issues_html = '<div class="issue success">✅ 未发现安全问题</div>'
        
        return f'''
        <div class="section">
            <h2>🔒 安全检查</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">安全分数</div>
                    <div class="metric-value">{security_score}/100</div>
                </div>
            </div>
            <div class="issues-list">
                {issues_html}
            </div>
        </div>'''
    
    def _build_performance_section(self, performance: Dict) -> str:
        """构建性能测试部分"""
        performance_score = performance.get("performance_score", 0)
        metrics = performance.get("metrics", {})
        
        metrics_html = ""
        
        if "import_time" in metrics and metrics["import_time"]:
            metrics_html += f'''
            <div class="metric-card">
                <div class="metric-title">导入时间</div>
                <div class="metric-value">{metrics["import_time"]:.3f}s</div>
            </div>'''
        
        if "execution_time" in metrics and metrics["execution_time"]:
            metrics_html += f'''
            <div class="metric-card">
                <div class="metric-title">执行时间</div>
                <div class="metric-value">{metrics["execution_time"]:.2f}s</div>
            </div>'''
        
        if "estimated_memory_mb" in metrics:
            metrics_html += f'''
            <div class="metric-card">
                <div class="metric-title">估算内存</div>
                <div class="metric-value">{metrics["estimated_memory_mb"]:.2f}MB</div>
            </div>'''
        
        return f'''
        <div class="section">
            <h2>⚡ 性能测试</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">性能分数</div>
                    <div class="metric-value">{performance_score}/100</div>
                </div>
                {metrics_html}
            </div>
        </div>'''
    
    def _build_suggestions_section(self, evaluation: Dict, code: Dict, security: Dict) -> str:
        """构建改进建议部分"""
        suggestions = []
        
        # 从评估中提取建议
        if evaluation.get("suggestions"):
            suggestions.extend(evaluation["suggestions"])
        
        # 从代码质量中提取建议
        if code and code.get("suggestions"):
            suggestions.extend(code["suggestions"])
        
        # 去重
        suggestions = list(set(suggestions))[:10]  # 最多10条
        
        suggestions_html = ""
        for i, suggestion in enumerate(suggestions, 1):
            suggestions_html += f'''
            <div class="issue success">
                <strong>{i}.</strong> {suggestion}
            </div>'''
        
        if not suggestions:
            suggestions_html = '<div class="issue success">✅ 技能质量优秀，无需改进</div>'
        
        return f'''
        <div class="section">
            <h2>💡 改进建议</h2>
            <div class="issues-list">
                {suggestions_html}
            </div>
        </div>'''
    
    def _get_score_color(self, score: float) -> str:
        """根据分数获取颜色"""
        if score >= 80:
            return "linear-gradient(135deg, #00c851 0%, #00a844 100%)"
        elif score >= 60:
            return "linear-gradient(135deg, #ffbb33 0%, #ff8800 100%)"
        else:
            return "linear-gradient(135deg, #ff4444 0%, #cc0000 100%)"
    
    def _get_score_description(self, score: float) -> str:
        """根据分数获取描述"""
        if score >= 80:
            return "✅ 技能质量优秀"
        elif score >= 60:
            return "⚠️ 技能质量良好，有改进空间"
        else:
            return "❌ 技能质量需要改进"
    
    def _get_category_name(self, category: str) -> str:
        """获取分类名称"""
        names = {
            "skill_md": "SKILL.md 完整性",
            "structure": "目录结构",
            "tests": "测试覆盖",
            "documentation": "文档质量",
            "python": "Python 代码",
            "shell": "Shell 脚本",
            "config": "配置文件"
        }
        return names.get(category, category)


def generate_report(skill_path: str, evaluation: Dict, code: Dict = None,
                   security: Dict = None, performance: Dict = None) -> str:
    """生成报告的便捷函数"""
    generator = ReportGenerator(skill_path)
    return generator.generate(evaluation, code, security, performance)

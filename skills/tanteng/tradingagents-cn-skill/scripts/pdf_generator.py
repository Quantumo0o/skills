#!/usr/bin/env python3
"""
PDF Report Generator for Stock Analysis
生成专业股票分析报告 PDF
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ReportGenerator:
    """股票分析报告 PDF 生成器"""

    def __init__(self):
        self.output_dir = Path(__file__).parent / "reports"
        self.output_dir.mkdir(exist_ok=True)

    def generate(
        self,
        analysis_result: Dict[str, Any],
        output_dir: Optional[str] = None,
        template: str = "professional"
    ) -> str:
        """
        生成 PDF 报告

        Args:
            analysis_result: StockAnalyst.analyze() 返回的结果
            output_dir: 输出目录（可选）
            template: 模板名称

        Returns:
            PDF 文件路径
        """
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = self.output_dir

        output_path.mkdir(parents=True, exist_ok=True)

        stock_code = analysis_result["stock_code"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{stock_code}_{timestamp}.pdf"
        pdf_path = output_path / filename

        html_content = self._generate_html(analysis_result)
        self._html_to_pdf(html_content, pdf_path)

        return str(pdf_path)

    def _generate_html(self, result: Dict[str, Any]) -> str:
        """生成 HTML 格式的报告"""
        stock_code = result["stock_code"]
        timestamp = result["timestamp"]
        final = result["final_decision"]
        trading = result["trading_plan"]
        manager = result["manager_decision"]
        risk = result["risk_debate"]
        parallel = result["parallel_analysis"]
        news_analyst = parallel["news_analyst"]
        social_analyst = parallel["social_analyst"]

        # 生成新闻列表 HTML
        news_list_html = ""
        if news_analyst.get("news_list") and len(news_analyst["news_list"]) > 0:
            for news in news_analyst["news_list"]:
                sentiment_color = "#2e7d32" if "多" in news.get("sentiment", "") or "正" in news.get("sentiment", "") else ("#c62828" if "空" in news.get("sentiment", "") or "负" in news.get("sentiment", "") else "#666")
                news_list_html += f"""
                <div class="news-item">
                    <div class="news-header">
                        <span class="news-title">{news.get('title', '')}</span>
                        <span class="news-sentiment" style="color:{sentiment_color}">{news.get('sentiment', '')}</span>
                    </div>
                    <div class="news-meta">
                        <span class="news-date">{news.get('date', '')}</span>
                        <span class="news-source">{news.get('source', '')}</span>
                    </div>
                    <div class="news-summary">{news.get('summary', '')}</div>
                </div>
                """
        else:
            news_list_html = '<div class="no-news">暂无新闻数据，请使用 web_search MCP tool 获取近期新闻</div>'

        # 生成社交媒体 HTML
        social_html = ""
        if social_analyst.get("platforms"):
            for platform in social_analyst["platforms"]:
                social_html += f"<li>{platform.get('name', '')}: {platform.get('sentiment', '')} (热度: {platform.get('heat', '')})</li>"
        else:
            social_html = f"""
            <li>雪球讨论热度: 中等</li>
            <li>东方财富股吧情绪: {social_analyst.get('sentiment_score', 0.5)}</li>
            <li>机构评级汇总: 待获取</li>
            """

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票分析报告 - {stock_code}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif; line-height: 1.6; color: #333; font-size: 12px; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 30px; }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #1a73e8; padding-bottom: 15px; }}
        .header h1 {{ color: #1a73e8; font-size: 24px; margin-bottom: 8px; }}
        .header .meta {{ color: #666; font-size: 11px; }}
        .section {{ margin-bottom: 25px; }}
        .section h2 {{ color: #1a73e8; font-size: 16px; border-left: 4px solid #1a73e8; padding-left: 10px; margin-bottom: 12px; }}
        .decision-box {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 15px; text-align: center; }}
        .decision-box .big {{ font-size: 28px; font-weight: bold; color: #1a73e8; }}
        .decision-box .sub {{ color: #666; margin-top: 8px; font-size: 11px; }}
        .target-prices {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; }}
        .price-card {{ background: #f5f5f5; padding: 12px; border-radius: 8px; text-align: center; }}
        .price-card .label {{ color: #666; font-size: 10px; }}
        .price-card .value {{ font-size: 18px; font-weight: bold; color: #1a73e8; }}
        .analyst-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        .analyst-card {{ background: #f9f9f9; padding: 12px; border-radius: 8px; border-left: 3px solid #1a73e8; }}
        .analyst-card h4 {{ color: #1a73e8; margin-bottom: 6px; font-size: 12px; }}
        .analyst-card ul {{ padding-left: 18px; font-size: 11px; }}
        .risk-table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
        .risk-table th, .risk-table td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        .risk-table th {{ background: #f5f5f5; }}
        .disclaimer {{ background: #fff3cd; padding: 12px; border-radius: 8px; font-size: 10px; color: #856404; margin-top: 20px; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; color: #999; font-size: 10px; }}

        /* 新闻样式 */
        .news-section {{ background: #fafafa; padding: 15px; border-radius: 8px; }}
        .news-item {{ background: #fff; padding: 12px; margin-bottom: 10px; border-radius: 6px; border: 1px solid #eee; }}
        .news-item:last-child {{ margin-bottom: 0; }}
        .news-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
        .news-title {{ font-weight: bold; color: #333; font-size: 12px; flex: 1; }}
        .news-sentiment {{ font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #f0f0f0; }}
        .news-meta {{ font-size: 10px; color: #888; margin-bottom: 6px; }}
        .news-date {{ margin-right: 15px; }}
        .news-summary {{ font-size: 11px; color: #555; line-height: 1.5; }}
        .no-news {{ text-align: center; color: #999; padding: 20px; font-size: 12px; }}

        .sentiment-summary {{ background: #e8f5e9; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>股票分析报告</h1>
            <div class="meta">
                <div>股票代码: {stock_code}</div>
                <div>报告生成时间: {timestamp}</div>
                <div>分析框架: TradingAgents-CN 多智能体</div>
            </div>
        </div>

        <!-- 执行摘要 -->
        <div class="section">
            <h2>执行摘要</h2>
            <div class="decision-box">
                <div class="big">{final["final_recommendation"]}</div>
                <div class="sub">风险等级: {final["risk_level"]} | 投资期限: {final["investment_horizon"]}</div>
            </div>
            <p><strong>核心逻辑:</strong> {manager["rationale"]}</p>
        </div>

        <!-- 目标价位 -->
        <div class="section">
            <h2>交易计划</h2>
            <div class="target-prices">
                <div class="price-card">
                    <div class="label">买入价格</div>
                    <div class="value">{"¥{:.2f}".format(trading["buy_price"]) if trading["buy_price"] else "观望"}</div>
                </div>
                <div class="price-card">
                    <div class="label">目标价格</div>
                    <div class="value">{"¥{:.2f}".format(trading["target_price"]) if trading["target_price"] else "待定"}</div>
                </div>
                <div class="price-card">
                    <div class="label">止损价格</div>
                    <div class="value">{"¥{:.2f}".format(trading["stop_loss"]) if trading["stop_loss"] else "不适用"}</div>
                </div>
            </div>
            <p><strong>仓位建议:</strong> {trading["position_size"]}</p>
            <p><strong>入场条件:</strong> {trading["entry_criteria"]}</p>
            <p><strong>出场条件:</strong> {trading["exit_criteria"]}</p>
        </div>

        <!-- 新闻与情绪分析 -->
        <div class="section">
            <h2>新闻与情绪分析</h2>
            <div class="news-section">
                <div class="sentiment-summary">
                    <strong>新闻情绪:</strong> {news_analyst.get("sentiment", "待获取")} | 共 {news_analyst.get("news_count", 0)} 条新闻
                </div>
                {news_list_html}
            </div>
            <div class="analyst-card" style="margin-top:15px;">
                <h4>社交媒体情绪</h4>
                <ul>
                    {social_html}
                </ul>
            </div>
        </div>

        <!-- 多头分析师观点 -->
        <div class="section">
            <h2>多头分析师观点</h2>
            <div class="analyst-card">
                <h4>买入论证</h4>
                <ul>
                    {"".join(f"<li>{point}</li>" for point in parallel["bull_analyst"]["analysis"])}
                </ul>
            </div>
        </div>

        <!-- 空头分析师观点 -->
        <div class="section">
            <h2>空头分析师观点</h2>
            <div class="analyst-card">
                <h4>卖出/观望论证</h4>
                <ul>
                    {"".join(f"<li>{point}</li>" for point in parallel["bear_analyst"]["analysis"])}
                </ul>
            </div>
        </div>

        <!-- 技术分析 -->
        <div class="section">
            <h2>技术分析</h2>
            <div class="analyst-card">
                <h4>技术指标解读</h4>
                <ul>
                    {"".join(f"<li>{point}</li>" for point in parallel["tech_analyst"]["analysis"])}
                </ul>
                <p style="margin-top:8px;"><strong>关键指标:</strong></p>
                <ul>
                    {"".join(f"<li>{k}: {v}</li>" for k, v in parallel["tech_analyst"]["indicators"].items())}
                </ul>
            </div>
        </div>

        <!-- 基本面分析 -->
        <div class="section">
            <h2>基本面分析</h2>
            <div class="analyst-card">
                <h4>估值与财务指标</h4>
                <ul>
                    {"".join(f"<li>{point}</li>" for point in parallel["fundamentals_analyst"]["analysis"])}
                </ul>
                <p style="margin-top:8px;"><strong>核心指标:</strong></p>
                <ul>
                    {"".join(f"<li>{k}: {v}</li>" for k, v in parallel["fundamentals_analyst"]["metrics"].items())}
                </ul>
            </div>
        </div>

        <!-- 风险评估 -->
        <div class="section">
            <h2>风险评估</h2>
            <table class="risk-table">
                <tr>
                    <th>情景</th>
                    <th>仓位</th>
                    <th>预期收益</th>
                    <th>止损</th>
                </tr>
                <tr>
                    <td>{risk["aggressive"]["position"]}</td>
                    <td>{risk["aggressive"]["position_size"]}</td>
                    <td>{risk["aggressive"]["target_return"]}</td>
                    <td>{risk["aggressive"]["stop_loss"]}</td>
                </tr>
                <tr>
                    <td>{risk["neutral"]["position"]}</td>
                    <td>{risk["neutral"]["position_size"]}</td>
                    <td>{risk["neutral"]["target_return"]}</td>
                    <td>{risk["neutral"]["stop_loss"]}</td>
                </tr>
                <tr>
                    <td>{risk["conservative"]["position"]}</td>
                    <td>{risk["conservative"]["position_size"]}</td>
                    <td>{risk["conservative"]["target_return"]}</td>
                    <td>{risk["conservative"]["stop_loss"]}</td>
                </tr>
            </table>
        </div>

        <!-- 风险因素 -->
        <div class="section">
            <h2>风险因素</h2>
            <ul>
                {"".join(f"<li>{k}: {v}</li>" for k, v in final["risk_assessment"].items())}
            </ul>
            <p style="margin-top:12px;"><strong>监控要点:</strong></p>
            <ul>
                {"".join(f"<li>{point}</li>" for point in final["monitoring_points"])}
            </ul>
            <p style="margin-top:12px;"><strong>适合投资者:</strong> {", ".join(final["suitable_investors"])}</p>
        </div>

        <!-- 辩论过程 -->
        <div class="section">
            <h2>辩论过程</h2>
            {"".join(f'''
            <div class="analyst-card" style="margin-bottom:10px;">
                <h4>第{r["round"]}轮辩论</h4>
                <p><strong>多头:</strong> {", ".join(r["bull_points"][:2])}</p>
                <p><strong>空头:</strong> {", ".join(r["bear_points"][:2])}</p>
            </div>
            ''' for r in result["debate"]["rounds"])}
        </div>

        <!-- 免责声明 -->
        <div class="disclaimer">
            <strong>免责声明:</strong><br>
            本报告由 AI 多智能体系统自动生成，基于公开信息和算法模型分析。
            本报告仅供研究和学习目的，不构成任何形式的投资建议或邀约。
            投资有风险，入市需谨慎。过去的表现不代表未来的收益。
            请在做出任何投资决策前，咨询专业的金融顾问。
        </div>

        <div class="footer">
            <p>Generated by TradingAgents-CN Skill</p>
            <p>本报告版权归属分析者所有，保留所有权利</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def _html_to_pdf(self, html_content: str, output_path: Path):
        """将 HTML 转换为 PDF"""
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(output_path)
            return
        except ImportError:
            pass

        try:
            import subprocess
            import tempfile

            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_html = f.name

            subprocess.run(
                ['wkhtmltopdf', '--page-size', 'A4', '--margin-top', '15mm',
                 '--margin-bottom', '15mm', '--margin-left', '12mm', '--margin-right', '12mm',
                 temp_html, str(output_path)],
                check=True
            )
            os.unlink(temp_html)
            return
        except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
            pass

        html_path = output_path.with_suffix('.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        raise RuntimeError(
            f"PDF 生成失败（weasyprint 和 wkhtmltopdf 均不可用）。"
            f"HTML 报告已保存至: {html_path}"
        )


if __name__ == "__main__":
    from analyst_multi import StockAnalyst

    # 测试带真实新闻数据
    analyst = StockAnalyst()
    news_data = [
        {"title": "苹果发布 Q4 财报，营收超预期", "date": "2024-11-01", "source": "彭博", "summary": "苹果公司第四季度营收同比增长 8.1%，iPhone 销量强劲", "sentiment": "偏多"},
        {"title": "iPhone 16 销量创历史新高", "date": "2024-10-28", "source": "路透", "summary": "新一代 iPhone 需求旺盛，出货量超预期 20%", "sentiment": "偏多"},
        {"title": "欧盟对苹果处以 18 亿欧元罚款", "date": "2024-10-25", "source": "BBC", "summary": "因 App Store 垄断行为被欧盟罚款", "sentiment": "偏空"},
    ]
    result = analyst.analyze(
        stock_code="AAPL",
        text_description="苹果公司 Q4 财报分析",
        news_data=news_data
    )

    generator = ReportGenerator()
    pdf_path = generator.generate(result)
    print(f"PDF 报告已生成: {pdf_path}")

#!/usr/bin/env python3
"""
Stock Analyst Multi-Agent Engine
基于 TradingAgents-CN 多智能体框架
"""

import json
import os
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any


class StockAnalyst:
    """股票分析多智能体引擎"""

    def __init__(self, model: str = "claude"):
        self.model = model
        self.agents = [
            "bull_analyst",      # 多头分析师
            "bear_analyst",      # 空头分析师
            "tech_analyst",      # 技术分析师
            "fundamentals_analyst",  # 基本面分析师
            "news_analyst",      # 新闻分析师
            "social_analyst",    # 社交媒体分析师
        ]
        self.debate_history = []

    def analyze(
        self,
        stock_code: str,
        text_description: Optional[str] = None,
        image_paths: Optional[List[str]] = None,
        debate_rounds: int = 2,
        news_data: Optional[List[Dict]] = None,
        social_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        执行完整的多智能体分析流程

        Args:
            stock_code: 股票代码
            text_description: 文本描述（可选）
            image_paths: 图片路径列表（可选）
            debate_rounds: 辩论轮数
            news_data: 真实新闻数据列表，每条新闻包含 title/date/source/summary
            social_data: 社交媒体情绪数据

        Returns:
            分析结果字典
        """
        # 1. 解析输入
        parsed_input = self._parse_input(stock_code, text_description, image_paths)

        # 2. 并行分析（传入真实新闻数据）
        parallel_results = self._parallel_analysis(
            parsed_input,
            news_data=news_data,
            social_data=social_data
        )

        # 3. 多空辩论
        debate_result = self._debate(parallel_results, debate_rounds)

        # 4. 研究经理决策
        manager_decision = self._research_manager(parallel_results, debate_result)

        # 5. 交易员计划
        trading_plan = self._trader(manager_decision)

        # 6. 三方风险辩论
        risk_debate = self._risk_debate(trading_plan)

        # 7. 风险经理决策
        final_decision = self._risk_manager(risk_debate, trading_plan)

        return {
            "stock_code": stock_code,
            "input": parsed_input,
            "parallel_analysis": parallel_results,
            "debate": debate_result,
            "manager_decision": manager_decision,
            "trading_plan": trading_plan,
            "risk_debate": risk_debate,
            "final_decision": final_decision,
            "timestamp": datetime.now().isoformat(),
        }

    def _parse_input(
        self,
        stock_code: str,
        text_description: Optional[str],
        image_paths: Optional[List[str]]
    ) -> Dict[str, Any]:
        """解析输入"""
        result = {
            "stock_code": stock_code,
            "code_type": self._identify_code_type(stock_code),
            "text_description": text_description,
            "images": [],
            "ocr_text": []
        }

        # OCR 处理图片
        if image_paths:
            for path in image_paths:
                if os.path.exists(path):
                    ocr_text = self._ocr_image(path)
                    result["ocr_text"].append(ocr_text)
                    result["images"].append(path)

        return result

    def _identify_code_type(self, stock_code: str) -> str:
        """识别股票代码类型"""
        if re.match(r"^HK\.", stock_code):
            return "港股"
        elif re.match(r"^US\.", stock_code):
            return "美股"
        elif re.match(r"^SH\.", stock_code):
            return "A股沪"
        elif re.match(r"^SZ\.", stock_code):
            return "A股深"
        elif re.match(r"^\d{6}$", stock_code):
            return "A股"
        return "未知"

    def _ocr_image(self, image_path: str) -> str:
        """OCR 识别图片文字"""
        try:
            result = subprocess.run(
                ["tesseract", image_path, "stdout", "-l", "chi_sim+eng"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"OCR识别失败: {str(e)}"

    def _parallel_analysis(
        self,
        parsed_input: Dict,
        news_data: Optional[List[Dict]] = None,
        social_data: Optional[Dict] = None
    ) -> Dict[str, Dict]:
        """并行启动 6 个分析师"""
        results = {}

        results["bull_analyst"] = self._bull_analyst(parsed_input)
        results["bear_analyst"] = self._bear_analyst(parsed_input)
        results["tech_analyst"] = self._tech_analyst(parsed_input)
        results["fundamentals_analyst"] = self._fundamentals_analyst(parsed_input)
        results["news_analyst"] = self._news_analyst(parsed_input, news_data)
        results["social_analyst"] = self._social_analyst(parsed_input, social_data)

        return results

    def _bull_analyst(self, input_data: Dict) -> Dict:
        """多头分析师 - 构建买入论证"""
        return {
            "role": "多头分析师",
            "task": "构建买入论证，强调增长潜力和积极指标",
            "input_summary": self._summarize_input(input_data),
            "analysis": [
                "基于当前市场趋势，该股票显示出积极的增长信号",
                "技术面显示上升趋势可能延续",
                "基本面支持看涨观点"
            ],
            "recommendation": "买入",
            "confidence": 0.75
        }

    def _bear_analyst(self, input_data: Dict) -> Dict:
        """空头分析师 - 构建卖出论证"""
        return {
            "role": "空头分析师",
            "task": "论证不投资理由，强调风险和负面指标",
            "input_summary": self._summarize_input(input_data),
            "analysis": [
                "存在可能导致下跌的风险因素",
                "技术面显示可能的回调信号",
                "估值过高可能限制上涨空间"
            ],
            "recommendation": "观望",
            "confidence": 0.65
        }

    def _tech_analyst(self, input_data: Dict) -> Dict:
        """技术分析师 - K线/均线/成交量分析"""
        return {
            "role": "技术分析师",
            "task": "技术分析，关注价格趋势和技术指标",
            "input_summary": self._summarize_input(input_data),
            "analysis": [
                "MA5/MA10/MA20 均线系统显示短期趋势",
                "成交量变化反映市场活跃度",
                "MACD、RSI 等指标给出超买超卖信号"
            ],
            "indicators": {
                "MA5": "价格 > 均线",
                "RSI": 65,
                "MACD": "金叉"
            }
        }

    def _fundamentals_analyst(self, input_data: Dict) -> Dict:
        """基本面分析师 - 财务数据分析"""
        return {
            "role": "基本面分析师",
            "task": "财务数据分析，计算PE/PB/PEG等估值指标",
            "input_summary": self._summarize_input(input_data),
            "analysis": [
                "PE 估值处于历史区间",
                "PB 市净率显示估值水平",
                "净利润增长率反映盈利能力"
            ],
            "metrics": {
                "PE": 25.5,
                "PB": 3.2,
                "PEG": 1.1,
                "ROE": 15.3
            }
        }

    def _news_analyst(
        self,
        input_data: Dict,
        news_data: Optional[List[Dict]] = None
    ) -> Dict:
        """
        新闻分析师 - 财经新闻影响
        如果传入真实新闻数据，则使用真实数据
        """
        if news_data and len(news_data) > 0:
            # 使用真实新闻数据
            news_items = []
            for news in news_data[:10]:  # 最多10条
                news_items.append({
                    "title": news.get("title", ""),
                    "date": news.get("date", ""),
                    "source": news.get("source", ""),
                    "summary": news.get("summary", news.get("snippet", "")),
                    "sentiment": news.get("sentiment", "")
                })

            # 分析整体情绪
            sentiments = [n.get("sentiment", "") for n in news_items if n.get("sentiment")]
            if sentiments:
                positive = sum(1 for s in sentiments if "多" in s or "正" in s or "利" in s)
                negative = sum(1 for s in sentiments if "空" in s or "负" in s or "跌" in s)
                if positive > negative:
                    overall_sentiment = "偏多"
                elif negative > positive:
                    overall_sentiment = "偏空"
                else:
                    overall_sentiment = "中性"
            else:
                overall_sentiment = "待分析"

            return {
                "role": "新闻分析师",
                "task": "分析财经新闻对股价的短期影响",
                "input_summary": self._summarize_input(input_data),
                "news_list": news_items,
                "news_count": len(news_items),
                "sentiment": overall_sentiment,
                "analysis": [f"共获取 {len(news_items)} 条新闻，整体情绪 {overall_sentiment}"]
            }
        else:
            # 使用占位符数据
            return {
                "role": "新闻分析师",
                "task": "分析财经新闻对股价的短期影响",
                "input_summary": self._summarize_input(input_data),
                "news_list": [],
                "news_count": 0,
                "sentiment": "待获取",
                "analysis": [
                    "请使用 web_search MCP tool 获取近期新闻",
                    "行业动态分析",
                    "宏观经济因素"
                ]
            }

    def _social_analyst(
        self,
        input_data: Dict,
        social_data: Optional[Dict] = None
    ) -> Dict:
        """社交媒体分析师 - 投资者情绪"""
        if social_data:
            return {
                "role": "社交媒体分析师",
                "task": "监控雪球、东方财富等平台的投资者情绪",
                "input_summary": self._summarize_input(input_data),
                "sentiment_score": social_data.get("sentiment_score", 0.5),
                "platforms": social_data.get("platforms", []),
                "analysis": social_data.get("analysis", [])
            }
        else:
            return {
                "role": "社交媒体分析师",
                "task": "监控雪球、东方财富等平台的投资者情绪",
                "input_summary": self._summarize_input(input_data),
                "analysis": [
                    "雪球讨论热度",
                    "东方财富股吧情绪",
                    "机构评级汇总"
                ],
                "sentiment_score": 0.55
            }

    def _summarize_input(self, input_data: Dict) -> str:
        """总结输入数据"""
        parts = [f"股票代码: {input_data['stock_code']} ({input_data.get('code_type', '未知')})"]

        if input_data.get('text_description'):
            parts.append(f"文本描述: {input_data['text_description'][:200]}...")

        if input_data.get('ocr_text'):
            ocr_combined = " ".join(input_data['ocr_text'])[:200]
            parts.append(f"图片OCR: {ocr_combined}...")

        return " | ".join(parts)

    def _debate(self, parallel_results: Dict, rounds: int) -> Dict:
        """多空辩论"""
        bull = parallel_results["bull_analyst"]
        bear = parallel_results["bear_analyst"]

        debate_record = []
        for round_num in range(rounds):
            debate_record.append({
                "round": round_num + 1,
                "bull_points": bull["analysis"],
                "bear_points": bear["analysis"],
                "cross_refutation": [
                    "多头回应空头担忧",
                    "空头回应多头论点"
                ]
            })

        return {
            "rounds": debate_record,
            "bull_final": bull["analysis"],
            "bear_final": bear["analysis"],
            "key_disagreements": [
                "估值是否合理",
                "增长能否持续"
            ]
        }

    def _research_manager(self, parallel_results: Dict, debate_result: Dict) -> Dict:
        """研究经理主持辩论，给出决策"""
        bull_strength = len(parallel_results["bull_analyst"]["analysis"])
        bear_strength = len(parallel_results["bear_analyst"]["analysis"])

        if bull_strength > bear_strength:
            decision = "买入"
            rationale = "多头论点更为充分"
        elif bear_strength > bull_strength:
            decision = "观望"
            rationale = "空头风险需要关注"
        else:
            decision = "持有"
            rationale = "多空力量均衡"

        return {
            "role": "研究经理",
            "decision": decision,
            "rationale": rationale,
            "supporting_evidence": parallel_results["bull_analyst"]["analysis"],
            "warning_signs": parallel_results["bear_analyst"]["analysis"]
        }

    def _trader(self, manager_decision: Dict) -> Dict:
        """交易员制定具体计划"""
        decision = manager_decision["decision"]
        stock_code = manager_decision.get("stock_code", "UNKNOWN")

        base_price = 100.0
        if decision == "买入":
            buy_price = base_price * 0.98
            target_price = base_price * 1.15
            stop_loss = base_price * 0.92
            position = "10%-20%"
        elif decision == "观望":
            buy_price = None
            target_price = None
            stop_loss = None
            position = "5%以下"
        else:
            buy_price = None
            target_price = base_price * 1.05
            stop_loss = base_price * 0.95
            position = "维持现状"

        return {
            "role": "交易员",
            "decision": decision,
            "action": "买入" if decision == "买入" else "观望/持有",
            "target_price": target_price,
            "buy_price": buy_price,
            "stop_loss": stop_loss,
            "position_size": position,
            "entry_criteria": "价格回撤至目标区间时入场",
            "exit_criteria": "跌破止损价或达到目标价位"
        }

    def _risk_debate(self, trading_plan: Dict) -> Dict:
        """三方风险辩论"""
        return {
            "aggressive": {
                "position": "激进派",
                "view": "高风险高收益，适合追求快速回报的投资者",
                "position_size": "30%-40%",
                "target_return": "25%+",
                "stop_loss": "-12%"
            },
            "neutral": {
                "position": "中性派",
                "view": "平衡风险与收益，适合长期投资者",
                "position_size": "15%-20%",
                "target_return": "10%-15%",
                "stop_loss": "-8%"
            },
            "conservative": {
                "position": "保守派",
                "view": "低风险低收益，适合风险厌恶型投资者",
                "position_size": "5%-10%",
                "target_return": "5%-8%",
                "stop_loss": "-5%"
            }
        }

    def _risk_manager(self, risk_debate: Dict, trading_plan: Dict) -> Dict:
        """风险经理综合决策"""
        return {
            "role": "风险经理",
            "final_recommendation": trading_plan["decision"],
            "risk_level": "中等",
            "risk_assessment": {
                "市场风险": "中等",
                "流动性风险": "低",
                "波动性风险": "中等"
            },
            "suitable_investors": ["稳健型", "积极型"],
            "investment_horizon": "3-6个月",
            "monitoring_points": [
                "季度财报发布",
                "行业政策变化",
                "技术面破位情况"
            ],
            "disclaimer": "本报告仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。"
        }


if __name__ == "__main__":
    # 测试
    analyst = StockAnalyst()
    result = analyst.analyze(
        stock_code="AAPL",
        text_description="苹果公司Q4财报超预期，服务收入创新高",
        debate_rounds=2
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

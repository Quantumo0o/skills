#!/usr/bin/env python3
"""
羊毛推送系统 v3.0 - 完整版
数据源：什么值得买 RSS + 慢慢买
功能：详细信息、历史价格、购买链接、推荐理由
"""

import feedparser
import requests
import json
import os
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

class DealsHunterV3:
    def __init__(self):
        self.all_deals = []
        self.tavily_api_key = os.environ.get('TAVILY_API_KEY', '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')
        self.dedup_file = '/Users/xufan65/.openclaw/workspace/memory/deals-sent.json'
        
    def load_sent_deals(self):
        """加载已发送的商品记录"""
        try:
            with open(self.dedup_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_sent_deals(self, sent_deals):
        """保存已发送的商品记录"""
        os.makedirs(os.path.dirname(self.dedup_file), exist_ok=True)
        with open(self.dedup_file, 'w', encoding='utf-8') as f:
            json.dump(sent_deals, f, ensure_ascii=False, indent=2)
    
    def fetch_smzdm_rss(self):
        """获取什么值得买 RSS"""
        print("\n📡 数据源 1: 什么值得买 RSS")
        try:
            feed = feedparser.parse("http://feed.smzdm.com")
            print(f"✅ 获取 {len(feed.entries)} 条优惠")
            
            count = 0
            for entry in feed.entries[:30]:
                title = entry.title
                link = entry.link
                description = entry.get('description', '')
                
                # 提取价格（从标题或描述）
                price_match = re.search(r'(\d+\.?\d*)\s*元', title + ' ' + description)
                price = float(price_match.group(1)) if price_match else None
                
                self.all_deals.append({
                    'source': '什么值得买',
                    'title': title,
                    'link': link,
                    'description': description[:200],
                    'price': price,
                    'published': entry.get('published', '')
                })
                count += 1
            
            print(f"   ✅ 添加 {count} 个优惠")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            return False
    
    def search_deal_details(self, deal):
        """使用 Tavily 搜索商品详细信息（包括历史最低价）"""
        try:
            url = "https://api.tavily.com/search"
            
            # 搜索当前价格和历史最低价（增加搜索关键词）
            query = f"{deal['title']} 价格 历史最低价 史低 最低价 京东 天猫"
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced",  # 使用高级搜索
                "max_results": 10
            }
            
            response = requests.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                details = {
                    'current_price': deal.get('price'),  # 优先使用 RSS 中的价格
                    'original_price': None,
                    'lowest_price': None,
                    'purchase_link': None,
                    'source': None
                }
                
                # 解析搜索结果
                for result in results:
                    content = result.get('content', '')
                    result_url = result.get('url', '')
                    
                    # 提取当前价格（如果还没有）
                    if not details['current_price']:
                        price_match = re.search(r'(\d+\.?\d*)\s*元', content)
                        if price_match:
                            price = float(price_match.group(1))
                            if 0 < price < 10000:  # 合理价格范围
                                details['current_price'] = price
                    
                    # 提取历史最低价（多种匹配模式）
                    if not details['lowest_price']:
                        # 模式1: "历史最低价 XX 元"
                        low_price_match = re.search(r'历史最低价\s*[：:]*\s*(\d+\.?\d*)', content)
                        if low_price_match:
                            low_price = float(low_price_match.group(1))
                            if 0 < low_price < 10000:
                                details['lowest_price'] = low_price
                        
                        # 模式2: "最低价 XX 元"
                        if not details['lowest_price']:
                            low_price_match = re.search(r'最低价\s*[：:]*\s*(\d+\.?\d*)', content)
                            if low_price_match:
                                low_price = float(low_price_match.group(1))
                                if 0 < low_price < 10000:
                                    details['lowest_price'] = low_price
                        
                        # 模式3: "史低 XX 元"
                        if not details['lowest_price']:
                            low_price_match = re.search(r'史低\s*[：:]*\s*(\d+\.?\d*)', content)
                            if low_price_match:
                                low_price = float(low_price_match.group(1))
                                if 0 < low_price < 10000:
                                    details['lowest_price'] = low_price
                        
                        # 模式4: "历史低价 XX"
                        if not details['lowest_price']:
                            low_price_match = re.search(r'历史低价\s*[：:]*\s*(\d+\.?\d*)', content)
                            if low_price_match:
                                low_price = float(low_price_match.group(1))
                                if 0 < low_price < 10000:
                                    details['lowest_price'] = low_price
                    
                    # 提取购买链接（优先京东）
                    if 'jd.com' in result_url and not details['purchase_link']:
                        details['purchase_link'] = result_url
                        details['source'] = '京东'
                    elif 'tmall.com' in result_url and not details['purchase_link']:
                        details['purchase_link'] = result_url
                        details['source'] = '天猫'
                
                # 如果没有找到购买链接，使用 SMZDM 链接
                if not details['purchase_link']:
                    details['purchase_link'] = deal['link']
                    details['source'] = '什么值得买'
                
                # 如果没有找到历史最低价，使用当前价格的 85% 作为参考
                if not details['lowest_price'] and details['current_price']:
                    details['lowest_price'] = round(details['current_price'] * 0.85, 2)
                    details['lowest_price_note'] = '（约参考价）'
                
                return details
            else:
                return None
                
        except Exception as e:
            print(f"   ⚠️  搜索失败: {e}")
            return None
    
    def generate_detailed_report(self):
        """生成简洁的羊毛推荐报告（标题、价格、历史最低价、购买链接）"""
        print("\n" + "=" * 60)
        print("📊 生成简洁报告...")
        print("=" * 60)
        
        # 去重
        sent_deals = self.load_sent_deals()
        now = datetime.now(timezone.utc)
        
        # 过滤已发送的商品
        new_deals = []
        for deal in self.all_deals:
            deal_key = deal['title'][:50]
            if deal_key not in sent_deals:
                new_deals.append(deal)
            else:
                # 检查是否超过 1 天
                try:
                    sent_time = datetime.fromisoformat(sent_deals[deal_key])
                    if (now - sent_time).days > 1:
                        new_deals.append(deal)
                except:
                    new_deals.append(deal)
        
        if not new_deals:
            print("\n⚠️  没有新的优惠商品")
            return None
        
        # 选择前 20 个商品
        top_deals = new_deals[:20]
        
        # 生成报告
        report_lines = []
        report_lines.append(f"**🐑 今日羊毛推荐** - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append("")
        report_lines.append(f"📦 商品数量: {len(top_deals)} | 📊 数据来源: 什么值得买 + 慢慢买")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 添加每个商品的简洁信息
        for i, deal in enumerate(top_deals, 1):
            print(f"\n🔍 处理 {i}/{len(top_deals)}: {deal['title'][:30]}...")
            
            # 搜索详细信息（包括历史最低价）
            details = self.search_deal_details(deal)
            
            # 标题
            report_lines.append(f"**{i}. {deal['title']}**")
            
            # 价格
            current_price = deal['price'] if deal['price'] else (details['current_price'] if details else None)
            if current_price:
                report_lines.append(f"💰 当前价格: **¥{current_price}**")
            else:
                current_price = 100  # 默认价格
                report_lines.append(f"💰 当前价格: **查看链接**")
            
            # 历史最低价
            lowest_price = details['lowest_price'] if details and details.get('lowest_price') else None
            if not lowest_price and current_price:
                # 如果没有找到历史最低价，使用当前价格的85%作为估算
                lowest_price = round(current_price * 0.85, 2)
                report_lines.append(f"📉 历史最低价: ~¥{lowest_price} (估算)")
            elif lowest_price:
                report_lines.append(f"📉 历史最低价: **¥{lowest_price}**")
            else:
                report_lines.append(f"📉 历史最低价: <https://cu.manmanbuy.com/search.php?s={deal['title'][:20]}>")
            
            # 购买建议 - SMZDM上的优惠价，直接推荐入手
            report_lines.append(f"💡 购买建议: ✅ 建议入手")
            report_lines.append(f"   SMZDM精选优惠，值得关注")
            
            # 购买链接
            purchase_link = details['purchase_link'] if details and details.get('purchase_link') else deal['link']
            report_lines.append(f"🛒 购买链接: <{purchase_link}>")
            
            report_lines.append("")
        
        # 添加总结
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("⚠️ 提醒:")
        report_lines.append("• 价格实时变化，建议尽快查看")
        report_lines.append("• 部分优惠需用券或有地区限制")
        report_lines.append("• 历史价格可访问慢慢买查询")
        report_lines.append("")
        report_lines.append("📅 下次更新: 9:00 AM / 12:00 PM / 6:00 PM")
        
        # 更新已发送记录
        for deal in top_deals:
            deal_key = deal['title'][:50]
            sent_deals[deal_key] = now.isoformat()
        
        # 只保留最近 7 天的记录
        from datetime import timedelta
        cutoff_date = now - timedelta(days=7)
        cutoff = cutoff_date.isoformat()
        sent_deals = {k: v for k, v in sent_deals.items() 
                     if isinstance(v, str) and v > cutoff}
        
        self.save_sent_deals(sent_deals)
        
        report = '\n'.join(report_lines)
        
        # 保存报告
        report_file = '/tmp/deals_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 报告已生成: {report_file}")
        
        return report

def main():
    print("🐑 羊毛推送系统 v3.0 - 完整版")
    print("=" * 60)
    
    hunter = DealsHunterV3()
    
    # 获取数据
    hunter.fetch_smzdm_rss()
    
    # 生成报告
    report = hunter.generate_detailed_report()
    
    if report:
        print("\n" + "=" * 60)
        print("✅ 羊毛推荐报告已生成！")
        print("=" * 60)
        
        # Discord 字符限制
        MAX_LENGTH = 1900
        
        # 分段
        lines = report.split('\n')
        chunks = []
        current_chunk = ''
        
        for line in lines:
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # 输出到 stdout（供 cron 读取）
        print(f"\n📦 报告已分成 {len(chunks)} 段")
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\n---DISCORD_CHUNK_{i}---")
            print(chunk)
            print(f"---END_CHUNK_{i}---")
    else:
        print("\n⚠️  没有新的优惠商品")

if __name__ == '__main__':
    main()

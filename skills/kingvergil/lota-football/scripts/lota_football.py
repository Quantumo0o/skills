#!/usr/bin/env python3
"""
Lota Football API Client - 查询足球比赛信息并获取特征文本

功能：
1. 解析自然语言查询，提取球队、联赛、日期等条件
2. 构建Lota API v2查询参数
3. 生成可执行的curl命令获取比赛列表
4. 为特定比赛生成获取紧凑版特征文本（compact-fet）的命令

环境变量：
- LOTA_API_KEY: API密钥（必需）
- LOTA_API_BASE_URL: API基础URL（可选，默认：http://deepdata.lota.tv/）

用法：
  python lota_football.py "自然语言查询"
示例：
  python lota_football.py "获取今日竞彩列表"
  python lota_football.py "查询北单比赛"
  python lota_football.py "曼联对切尔西的特征文本"
"""
import os
import sys
import json
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from urllib.parse import urljoin

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LotaFootballSkill:
    """Lota Football Skill主类"""

    def __init__(self):
        self.api_key = os.environ.get('LOTA_API_KEY')
        self.base_url = os.environ.get('LOTA_API_BASE_URL', 'http://deepdata.lota.tv/').rstrip('/') + '/'

        if not self.api_key:
            raise ValueError("环境变量 LOTA_API_KEY 未设置，请设置环境变量：export LOTA_API_KEY='your_api_key'")

        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'User-Agent': 'LotaFootballSkill/1.0',
            'Accept': 'application/json'
        })

        logger.info(f"初始化Lota Football Client，API URL: {self.base_url}")

    def build_curl_command(self, endpoint: str, params: Optional[Dict[str, str]] = None,
                          auth_method: str = 'header') -> str:
        """
        构建curl命令

        Args:
            endpoint: API端点路径
            params: 查询参数
            auth_method: 认证方式 ('bearer', 'header', 'query_param')

        Returns:
            curl命令字符串
        """
        # 构建完整URL
        url = urljoin(self.base_url, endpoint)

        # 构建查询字符串
        query_string = ""
        if params:
            query_parts = []
            for key, value in params.items():
                query_parts.append(f"{key}={value}")
            if query_parts:
                query_string = "?" + "&".join(query_parts)

        # 根据认证方式构建curl命令
        if auth_method == 'query_param':
            # 将API密钥添加到查询参数中
            sep = '&' if query_string else '?'
            auth_query = f"{sep}api_key={self.api_key}"
            curl_cmd = f"curl -X GET '{url}{query_string}{auth_query}' \\\n"
            curl_cmd += f"  -H 'Accept: application/json'"
        elif auth_method == 'header':
            # 使用X-API-Key头
            curl_cmd = f"curl -X GET '{url}{query_string}' \\\n"
            curl_cmd += f"  -H 'X-API-Key: {self.api_key}' \\\n"
            curl_cmd += f"  -H 'Accept: application/json'"
        else:  # bearer (默认)
            # 使用Bearer Token头
            curl_cmd = f"curl -X GET '{url}{query_string}' \\\n"
            curl_cmd += f"  -H 'Authorization: Bearer {self.api_key}' \\\n"
            curl_cmd += f"  -H 'Accept: application/json'"

        return curl_cmd

    def extract_query_params(self, natural_language: str) -> Dict[str, Any]:
        """
        从自然语言中提取查询参数

        Args:
            natural_language: 自然语言查询字符串

        Returns:
            查询参数字典
        """
        query_params = {}

        # 转换为小写方便匹配
        text = natural_language.lower()

        # 提取球队关键词：使用简单的中文词组匹配
        # 匹配中文字符序列（至少2个中文字符）
        import re
        chinese_pattern = re.compile(r'[\u4e00-\u9fa5]{2,}')
        chinese_words = chinese_pattern.findall(natural_language)  # 使用原始字符串保留大小写

        # 过滤掉常见的停用词（联赛、日期等关键词）
        stop_words = {'今天', '今日', '明天', '明日', '昨天', '昨日', '未开', '未开始',
                     '即将开始', '已完', '结束', '完赛', '进行', '正在', '特征', '文本',
                     '英超', '英格兰超级联赛', '西甲', '西班牙甲级联赛', '意甲', '意大利甲级联赛',
                     '德甲', '德国甲级联赛', '法甲', '法国甲级联赛', '欧冠', '欧洲冠军联赛',
                     'vs', '对阵', '对', '比赛', '足球', '赛', '队', '球队',
                     '竞彩', '北单', '获取', '查询', '查找', '查看', '搜索', '找',
                     '列表', '单子', '单', '信息', '数据', '详情', '详细'}

        team_keywords = []
        for word in chinese_words:
            if word not in stop_words:
                team_keywords.append(word)

        # 提取对阵格式：团队A vs 团队B
        vs_pattern = re.compile(r'([\u4e00-\u9fa5a-zA-Z0-9]+)\s*(?:vs|对阵|对)\s*([\u4e00-\u9fa5a-zA-Z0-9]+)', re.IGNORECASE)
        vs_match = vs_pattern.search(natural_language)
        if vs_match:
            team1, team2 = vs_match.groups()
            team_keywords.extend([team1, team2])

        # 去重
        team_keywords = list(dict.fromkeys(team_keywords))

        if team_keywords:
            query_params['team_keywords'] = team_keywords

        # 提取联赛（支持中文全称和缩写）
        league_mapping = {
            # 英超
            '英超': '英超',
            '英格兰超级联赛': '英超',
            'epl': '英超',
            'premier': '英超',
            # 西甲
            '西甲': '西甲',
            '西班牙甲级联赛': '西甲',
            'la liga': '西甲',
            'laliga': '西甲',
            # 意甲
            '意甲': '意甲',
            '意大利甲级联赛': '意甲',
            'serie a': '意甲',
            'seriea': '意甲',
            # 德甲
            '德甲': '德甲',
            '德国甲级联赛': '德甲',
            'bundesliga': '德甲',
            # 法甲
            '法甲': '法甲',
            '法国甲级联赛': '法甲',
            'ligue 1': '法甲',
            'ligue1': '法甲',
            # 欧冠
            '欧冠': '欧冠',
            '欧洲冠军联赛': '欧冠',
            'champions league': '欧冠',
            'championsleague': '欧冠',
            # 欧联
            '欧联': '欧联',
            '欧罗巴': '欧联',
            'europa': '欧联',
            'europa league': '欧联',
            # 亚冠
            '亚冠': '亚冠',
            '亚冠联赛': '亚冠',
            'afc': '亚冠',
            'afc champions': '亚冠'
        }

        for key, value in league_mapping.items():
            if key.lower() in text:
                query_params['league'] = value
                break

        # 提取对阵格式：团队A vs 团队B
        vs_pattern = re.compile(r'([\u4e00-\u9fa5a-zA-Z0-9]+)\s*(?:vs|对阵|对)\s*([\u4e00-\u9fa5a-zA-Z0-9]+)', re.IGNORECASE)
        vs_match = vs_pattern.search(natural_language)
        if vs_match:
            team1, team2 = vs_match.groups()
            query_params['vs_match'] = (team1, team2)
            # 将两队名也加入关键词列表
            team_keywords.extend([team1, team2])

        # 提取日期关键词
        if '今天' in text or '今日' in text:
            query_params['date'] = 'today'
        elif '明天' in text or '明日' in text:
            query_params['date'] = 'tomorrow'
        elif '昨天' in text or '昨日' in text:
            query_params['date'] = 'yesterday'
        elif '本周' in text or '这周' in text:
            query_params['date'] = 'this_week'
        elif '周末' in text:
            query_params['date'] = 'weekend'
        elif '本月' in text or '这个月' in text:
            query_params['date'] = 'this_month'
        elif '下周' in text:
            query_params['date'] = 'next_week'

        # 提取状态关键词
        if '未开' in text or '未开始' in text or '即将开始' in text:
            query_params['status'] = '未开赛'
        elif '已完' in text or '结束' in text or '完赛' in text:
            query_params['status'] = '已完赛'
        elif '进行' in text or '正在' in text:
            query_params['status'] = '进行中'

        # 提取彩票类型关键词
        if '竞彩' in text:
            query_params['lottery_type'] = 'jingcai'
        elif '北单' in text:
            query_params['lottery_type'] = 'beidan'

        # 提取特征文本关键词
        if '特征' in text or 'fet' in text or '文本' in text:
            query_params['need_fet'] = True

        logger.info(f"提取的查询参数: {query_params}")
        return query_params

    def build_api_query(self, query_params: Dict[str, Any]) -> Dict[str, str]:
        """
        构建API查询参数

        Args:
            query_params: 提取的查询参数

        Returns:
            API查询参数字典
        """
        api_params = {}

        # 联赛
        if 'league' in query_params:
            api_params['league'] = query_params['league']

        # 状态
        if 'status' in query_params:
            api_params['status'] = query_params['status']

        # 彩票类型
        if 'lottery_type' in query_params:
            if query_params['lottery_type'] == 'jingcai':
                api_params['is_jingcai'] = 'true'
            elif query_params['lottery_type'] == 'beidan':
                api_params['is_beidan'] = 'true'

        # 日期处理
        if 'date' in query_params:
            today = datetime.now()
            if query_params['date'] == 'today':
                api_params['start_date'] = today.strftime('%Y-%m-%d')
                api_params['end_date'] = today.strftime('%Y-%m-%d')
            elif query_params['date'] == 'tomorrow':
                tomorrow = today + timedelta(days=1)
                api_params['start_date'] = tomorrow.strftime('%Y-%m-%d')
                api_params['end_date'] = tomorrow.strftime('%Y-%m-%d')
            elif query_params['date'] == 'yesterday':
                yesterday = today - timedelta(days=1)
                api_params['start_date'] = yesterday.strftime('%Y-%m-%d')
                api_params['end_date'] = yesterday.strftime('%Y-%m-%d')
            elif query_params['date'] == 'this_week':
                # 本周一
                weekday = today.weekday()  # 0=Monday, 6=Sunday
                monday = today - timedelta(days=weekday)
                sunday = monday + timedelta(days=6)
                api_params['start_date'] = monday.strftime('%Y-%m-%d')
                api_params['end_date'] = sunday.strftime('%Y-%m-%d')
            elif query_params['date'] == 'weekend':
                # 本周六到周日
                weekday = today.weekday()
                saturday = today + timedelta(days=(5 - weekday))  # 5=Saturday
                sunday = saturday + timedelta(days=1)
                api_params['start_date'] = saturday.strftime('%Y-%m-%d')
                api_params['end_date'] = sunday.strftime('%Y-%m-%d')
            elif query_params['date'] == 'this_month':
                # 本月第一天和最后一天
                first_day = today.replace(day=1)
                next_month = first_day.replace(month=first_day.month % 12 + 1, year=first_day.year + (first_day.month // 12))
                last_day = next_month - timedelta(days=1)
                api_params['start_date'] = first_day.strftime('%Y-%m-%d')
                api_params['end_date'] = last_day.strftime('%Y-%m-%d')
            elif query_params['date'] == 'next_week':
                # 下周
                weekday = today.weekday()
                next_monday = today + timedelta(days=(7 - weekday))
                next_sunday = next_monday + timedelta(days=6)
                api_params['start_date'] = next_monday.strftime('%Y-%m-%d')
                api_params['end_date'] = next_sunday.strftime('%Y-%m-%d')

        # 默认优先未开赛比赛
        if 'status' not in api_params:
            api_params['status'] = '未开赛'

        # 限制返回数量
        api_params['limit'] = '10000'

        return api_params

    def query_matches(self, api_params: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        查询比赛信息

        Args:
            api_params: API查询参数

        Returns:
            比赛列表
        """
        url = urljoin(self.base_url, '/predictions/api/v2/matches/')

        try:
            logger.info(f"查询比赛: {url}, 参数: {api_params}")
            response = self.session.get(url, params=api_params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if data.get('code') == 0:
                matches = data.get('data', {}).get('matches', [])
                logger.info(f"查询到 {len(matches)} 场比赛")
                return matches
            else:
                logger.error(f"API返回错误: {data.get('message')}")
                return []

        except requests.exceptions.RequestException as e:
            logger.error(f"查询比赛失败: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON失败: {e}")
            return []

    def get_feature_text(self, lota_id: str) -> Optional[str]:
        """
        获取比赛特征文本

        Args:
            lota_id: 比赛ID

        Returns:
            特征文本或None
        """
        url = urljoin(self.base_url, '/predictions/api/v2/compact-fet/')
        params = {'lota_id': lota_id}

        try:
            logger.info(f"获取特征文本: {url}, lota_id: {lota_id}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if data.get('success'):
                feature_text = data.get('compact_fet')
                logger.info(f"获取到特征文本，长度: {len(feature_text)}")
                return feature_text
            else:
                logger.error(f"获取特征文本失败: {data.get('error')}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"获取特征文本失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON失败: {e}")
            return None

    def select_best_match(self, matches: List[Dict[str, Any]], team_keywords: Optional[List[str]] = None,
                         vs_match: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        选择最佳匹配的比赛

        优先选择对阵匹配的比赛，然后匹配球队关键词的比赛，再优先未开赛的比赛，最后按时间排序

        Args:
            matches: 比赛列表
            team_keywords: 球队关键词列表
            vs_match: 对阵元组 (team1, team2)

        Returns:
            最佳比赛或None
        """
        if not matches:
            return None

        # 如果有对阵信息，优先精确匹配
        filtered_matches = matches
        if vs_match:
            team1, team2 = vs_match
            team1_lower = team1.lower()
            team2_lower = team2.lower()

            vs_matched_matches = []
            for match in matches:
                home_name = match.get('home_name', '').lower()
                away_name = match.get('away_name', '').lower()
                # 检查是否是对阵格式：主场包含team1且客场包含team2，或者主场包含team2且客场包含team1
                if (team1_lower in home_name and team2_lower in away_name) or \
                   (team2_lower in home_name and team1_lower in away_name):
                    vs_matched_matches.append(match)

            # 如果有对阵匹配的比赛，使用它们
            if vs_matched_matches:
                filtered_matches = vs_matched_matches

        # 如果有球队关键词（且没有对阵匹配或对阵匹配无结果），过滤匹配的比赛
        if team_keywords and filtered_matches == matches:
            matched_matches = []
            for match in filtered_matches:
                home_name = match.get('home_name', '').lower()
                away_name = match.get('away_name', '').lower()
                # 检查是否有任意关键词出现在主场或客场队名中
                for keyword in team_keywords:
                    keyword_lower = keyword.lower()
                    if keyword_lower in home_name or keyword_lower in away_name:
                        matched_matches.append(match)
                        break

            # 如果有匹配的比赛，使用它们
            if matched_matches:
                filtered_matches = matched_matches

        # 优先未开赛比赛
        unfinished_matches = [m for m in filtered_matches if m.get('state_name') == '未开赛']
        if unfinished_matches:
            # 按时间升序（最早未开赛）
            unfinished_matches.sort(key=lambda x: x.get('match_time', ''))
            return unfinished_matches[0]

        # 如果没有未开赛，返回第一个
        return filtered_matches[0] if filtered_matches else None

    def format_match_info(self, match: Dict[str, Any]) -> str:
        """
        格式化比赛信息

        Args:
            match: 比赛信息

        Returns:
            格式化的比赛信息字符串
        """
        home = match.get('home_name', '未知')
        away = match.get('away_name', '未知')
        league = match.get('league_name', '未知')
        match_time = match.get('match_time', '未知')
        state = match.get('state_name', '未知')

        return f"{league}: {home} vs {away}\n时间: {match_time}\n状态: {state}"

    def process_query(self, natural_language: str) -> Dict[str, Any]:
        """
        处理自然语言查询，生成curl命令

        Args:
            natural_language: 自然语言查询

        Returns:
            包含curl命令的结果字典
        """
        try:
            # 提取查询参数
            query_params = self.extract_query_params(natural_language)

            # 构建API查询参数
            api_params = self.build_api_query(query_params)

            # 生成三种认证方式的curl命令
            matches_curl_bearer = self.build_curl_command('/predictions/api/v2/matches/', api_params, 'bearer')
            matches_curl_header = self.build_curl_command('/predictions/api/v2/matches/', api_params, 'header')
            matches_curl_query = self.build_curl_command('/predictions/api/v2/matches/', api_params, 'query_param')

            # 构建特征文本获取命令模板
            base_url_no_slash = self.base_url.rstrip('/')
            fet_bearer = f"curl -X GET '{base_url_no_slash}/predictions/api/v2/compact-fet/?lota_id=YOUR_LOTA_ID' \\\n  -H 'Authorization: Bearer {self.api_key}' \\\n  -H 'Accept: application/json'"
            fet_header = f"curl -X GET '{base_url_no_slash}/predictions/api/v2/compact-fet/?lota_id=YOUR_LOTA_ID' \\\n  -H 'X-API-Key: {self.api_key}' \\\n  -H 'Accept: application/json'"
            fet_query = f"curl -X GET '{base_url_no_slash}/predictions/api/v2/compact-fet/?lota_id=YOUR_LOTA_ID&api_key={self.api_key}' \\\n  -H 'Accept: application/json'"

            # 构建结果
            result = {
                'success': True,
                'query': natural_language,
                'parsed_params': query_params,
                'api_params': api_params,
                'curl_commands': {
                    'matches_bearer': {
                        'command': matches_curl_bearer,
                        'description': '查询比赛列表 (Bearer Token认证)'
                    },
                    'matches_header': {
                        'command': matches_curl_header,
                        'description': '查询比赛列表 (X-API-Key认证)'
                    },
                    'matches_query': {
                        'command': matches_curl_query,
                        'description': '查询比赛列表 (查询参数认证)'
                    }
                },
                'feature_templates': {
                    'bearer': fet_bearer,
                    'header': fet_header,
                    'query_param': fet_query
                },
                'instructions': [
                    '1. 选择一种认证方式，复制对应的curl命令在终端执行',
                    '2. 命令将返回比赛列表JSON数据',
                    '3. 从返回的数据中找到想要的比赛的lota_id',
                    '4. 使用对应的特征文本获取命令（替换YOUR_LOTA_ID为实际比赛ID）：'
                ]
            }

            # 如果查询中包含特征文本需求，添加更多说明
            if query_params.get('need_fet', True):
                result['instructions'].append('')
                result['instructions'].append('提示：执行比赛查询命令后，找到对应比赛的lota_id，选择相同认证方式的特征文本命令执行')

            return result

        except Exception as e:
            logger.error(f"处理查询时发生错误: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'处理查询时发生错误: {str(e)}',
                'curl_commands': None
            }


def main():
    """主函数 - 用于命令行测试"""
    if len(sys.argv) < 2:
        print("用法: python lota_football.py \"自然语言查询\"")
        sys.exit(1)

    query = sys.argv[1]

    try:
        skill = LotaFootballSkill()
        result = skill.process_query(query)

        if result['success']:
            print("\n📋 **Lota足球数据查询**")
            print(f"🔍 查询: {result['query']}")

            # 显示X-API-Key认证的CURL命令（最常用）
            curl_commands = result.get('curl_commands', {})
            header_cmd = curl_commands.get('matches_header', {}).get('command')
            if header_cmd:
                print("\n🔗 **CURL命令 (X-API-Key认证)**:")
                print(f"```bash\n{header_cmd}\n```")

            # 显示特征文本获取模板（X-API-Key认证）
            feature_templates = result.get('feature_templates', {})
            fet_template = feature_templates.get('header')
            if fet_template:
                print("\n📄 **特征文本获取命令 (X-API-Key认证)**:")
                print("```bash")
                print(fet_template)
                print("```")
                print("> 将 `YOUR_LOTA_ID` 替换为实际比赛ID")

            # 简洁使用步骤
            print("\n📖 **使用步骤**:")
            print("1. 复制上方CURL命令执行，获取比赛列表")
            print("2. 从返回的JSON中找到所需比赛的 `lota_id`")
            print("3. 用该 `lota_id` 替换特征文本命令中的 `YOUR_LOTA_ID` 并执行")
            print("4. 获得特征文本后，可粘贴给AI进行深度分析")

            # 其他认证方式提示
            print("\n💡 提示: 如需其他认证方式，请查看技能源码。")
        else:
            print(f"\n❌ 错误: {result['message']}")

    except ValueError as e:
        print(f"配置错误: {e}")
        print("请设置环境变量 LOTA_API_KEY")
        sys.exit(1)
    except Exception as e:
        print(f"运行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
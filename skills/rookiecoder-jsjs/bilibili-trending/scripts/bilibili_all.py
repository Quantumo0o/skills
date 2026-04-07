"""
Bilibili 热门数据抓取与分析自动化脚本

完整流程：
1. 抓取数据
2. 自动调用子 Agent 分析
3. 自动保存报告
"""

import requests
import json
import time
import random
import os
import re
import argparse
import sys
from datetime import datetime
from collections import Counter

# Windows 控制台编码修复
import io
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

# ========== 路径配置 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
OPENCLAW_JSON_DIR = os.path.join(WORKSPACE, "json")
ANALYSIS_DIR = os.path.join(WORKSPACE, "memory", "bilibili-analysis")
TREND_FILE = os.path.join(ANALYSIS_DIR, "trend.json")

os.makedirs(OPENCLAW_JSON_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

from config import RANK_CONFIG


def fetch_ranking_v2(rid):
    """抓取普通视频排行榜"""
    url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"rid": rid, "type": "all", "pn": 1, "ps": 30}

    time.sleep(random.uniform(1, 3))
    response = requests.get(url, headers=headers, params=params, timeout=10)
    raw_data = response.json()

    if raw_data.get("code") != 0:
        raise Exception(f"API错误: {raw_data.get('message')}")
    return raw_data


def fetch_pgc_ranking(season_type):
    """抓取PGC内容排行榜"""
    url = "https://api.bilibili.com/pgc/season/rank/list"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"season_type": season_type}

    time.sleep(random.uniform(1, 3))
    response = requests.get(url, headers=headers, params=params, timeout=10)
    raw_data = response.json()

    if raw_data.get("code") != 0:
        raise Exception(f"API错误: {raw_data.get('message')}")
    return raw_data


def process_ranking_v2(raw_data):
    """处理普通视频数据"""
    video_list = raw_data["data"]["list"]
    processed = []

    for idx, v in enumerate(video_list):
        view = v["stat"]["view"]
        danmaku = v["stat"]["danmaku"]
        reply = v["stat"]["reply"]
        like = v["stat"]["like"]

        processed.append({
            "rank": idx + 1,
            "title": v.get("title", "").strip(),
            "tname": v.get("tname"),
            "view": view,
            "danmaku": danmaku,
            "reply": reply,
            "like": like,
            "interaction_rate": round((danmaku + reply) / max(view, 1) * 100, 3),
        })

    total_views = sum(v["stat"]["view"] for v in video_list)
    zone_dist = {}
    for v in video_list:
        tname = v.get("tname")
        zone_dist[tname] = zone_dist.get(tname, 0) + 1

    return processed, {
        "total_videos": len(processed),
        "total_views": total_views,
        "avg_interaction_rate": round(sum(p["interaction_rate"] for p in processed) / len(processed), 3),
        "top_zone": max(zone_dist.items(), key=lambda x: x[1])[0] if zone_dist else "",
        "zone_distribution": zone_dist,
    }


def process_pgc_ranking_data(raw_data):
    """处理PGC数据"""
    video_list = raw_data["data"]["list"]
    processed = []
    total_views = 0

    for idx, v in enumerate(video_list):
        view = v.get("stat", {}).get("view", 0)
        total_views += view
        processed.append({
            "rank": idx + 1,
            "title": v.get("title", "").strip(),
            "area": v.get("area", ""),
            "view": view,
            "score": v.get("score", 0),
        })

    area_dist = {}
    for v in video_list:
        area = v.get("area", "未知")
        area_dist[area] = area_dist.get(area, 0) + 1

    return processed, {
        "total_videos": len(processed),
        "total_views": total_views,
        "avg_interaction_rate": 0,
        "top_zone": max(area_dist.items(), key=lambda x: x[1])[0] if area_dist else "",
        "zone_distribution": area_dist,
    }


def load_trend():
    """加载趋势数据"""
    if os.path.exists(TREND_FILE):
        with open(TREND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "keywords": {}, "zones": {}}


def save_trend(rank_type, top_zone, keywords, avg_interaction):
    """保存趋势数据"""
    trend = load_trend()
    trend["records"].append({
        "time": datetime.now().strftime("%Y-%m-%d-%H%M%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rank_type": rank_type,
        "top_zone": top_zone,
        "avg_interaction": avg_interaction,
        "keywords": keywords,
    })

    for kw in keywords:
        trend["keywords"][kw] = trend["keywords"].get(kw, 0) + 1
    if top_zone:
        trend["zones"][top_zone] = trend["zones"].get(top_zone, 0) + 1

    trend["records"] = trend["records"][-60:]

    with open(TREND_FILE, "w", encoding="utf-8") as f:
        json.dump(trend, f, ensure_ascii=False, indent=2)


def generate_prompt(rank_type, videos, summary):
    """生成分析 prompt"""
    rank_name = RANK_CONFIG[rank_type]["name"]

    # 计算统计数据
    total_videos = len(videos)
    total_views = summary.get('total_views', 0)
    avg_ir = summary.get('avg_interaction_rate', 0)

    # 播放量统计
    views = [v.get('view', 0) for v in videos]
    top10_views = sum(views[:10])
    top10_ratio = round(top10_views / max(total_views, 1) * 100, 1) if total_views else 0

    # 互动率统计
    irs = [v.get('interaction_rate', 0) for v in videos]
    high_ir_count = sum(1 for ir in irs if ir > avg_ir * 1.5)

    # 提取关键词（全文）
    keywords = []
    for v in videos:
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', v.get('title', ''))
        keywords.extend(words[:2])
    kw_counter = Counter(keywords)
    top_keywords = [kw for kw, _ in kw_counter.most_common(10)]

    # UP主统计
    owner_names = [v.get('owner', {}).get('name', '未知') for v in videos]
    owner_counter = Counter(owner_names)
    top_owners = [(name, cnt) for name, cnt in owner_counter.most_common(5) if cnt > 1]

    # 完整视频数据
    full_data = {
        "rank_type": rank_type,
        "rank_name": rank_name,
        "total_videos": total_videos,
        "total_views": total_views,
        "avg_interaction_rate": avg_ir,
        "top_zone": summary.get('top_zone', ''),
        "zone_distribution": summary.get('zone_distribution', {}),
        "top10_views_ratio": top10_ratio,
        "high_interaction_count": high_ir_count,
        "top_keywords": top_keywords,
        "top_owners": top_owners,
        "videos": videos,
    }

    prompt = f"""请深度分析 Bilibili {rank_name} 榜单数据（共{total_videos}条视频）。

## 数据概览
- 总视频数: {total_videos}
- 总播放: {total_views:,}
- 平均互动率: {avg_ir:.3f}%
- 分区数: {len(summary.get('zone_distribution', {}))}
- TOP10播放占比: {top10_ratio}%
- 高互动视频数: {high_ir_count}条

## 热门分区分布
{json.dumps(summary.get('zone_distribution', {}), ensure_ascii=False)}

## 高频关键词 TOP10
{json.dumps(top_keywords, ensure_ascii=False)}

## 头部UP主（重复上榜）
{json.dumps(top_owners, ensure_ascii=False)}

## 完整视频数据
{json.dumps(full_data, ensure_ascii=False, indent=2)}

请输出 Markdown 分析报告，包含：
1. **播放量分布**：头部效应是否明显，TOP10占比，高播放视频特征
2. **互动率分析**：高互动视频的共同特征（标题/分区/UP主）
3. **热门分区**：哪些分区最活跃，竞争程度
4. **UP主生态**：是否有重复上榜的头部UP主，分析其内容风格
5. **标题规律**：高频词、热门题材、标题起名技巧
6. **下期预测**：什么类型/分区/题材可能下期上位

请用中文输出，直接输出报告内容。"""

    return prompt, top_keywords


def save_report(rank_type, content):
    """保存分析报告"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rank_name = RANK_CONFIG[rank_type]["name"]
    filename = f"{timestamp}_{rank_name}.md"
    filepath = os.path.join(ANALYSIS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def spawn_analysis_agent(prompt):
    """调用子 Agent 分析"""
    try:
        from sessions_spawn import sessions_spawn
        response = sessions_spawn(
            label=f"bili-analysis",
            runtime="subagent",
            task=prompt,
            timeoutSeconds=120
        )
        return response.get('status') == 'accepted'
    except ImportError:
        return False
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Bilibili 热门数据分析")
    parser.add_argument("--rank", "-r", type=str, default="all", help="榜单类型")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有榜单")
    parser.add_argument("--auto", "-a", action="store_true", help="自动调用子Agent分析", default=True)
    parser.add_argument("--manual", "-m", action="store_true", help="手动模式（不调用子Agent）")
    args = parser.parse_args()

    # 列出榜单
    if args.list:
        print("\n可用榜单:")
        for key, config in RANK_CONFIG.items():
            print(f"  {key:15} - {config['name']}")
        return

    rank_type = args.rank
    config = RANK_CONFIG[rank_type]
    rank_name = config["name"]

    print(f"\n{'='*50}")
    print(f"开始抓取 {rank_name} 榜单...")
    print("=" * 50)

    # Step 1: 抓取数据
    try:
        if config["api_type"] == "ranking":
            raw_data = fetch_ranking_v2(config["rid"])
            videos, summary = process_ranking_v2(raw_data)
        else:
            raw_data = fetch_pgc_ranking(config["season_type"])
            videos, summary = process_pgc_ranking_data(raw_data)
    except Exception as e:
        print(f"抓取失败: {e}")
        return

    print(f"✓ 成功抓取 {len(videos)} 条数据")
    print(f"  总播放: {summary['total_views']:,}")
    print(f"  平均互动率: {summary['avg_interaction_rate']}%")
    print(f"  最热分区: {summary['top_zone']}")

    # Step 2: 保存 JSON
    output_path = os.path.join(OPENCLAW_JSON_DIR, f"output_{rank_type}.json")
    result = {
        "result": "success",
        "data": {
            "rank_type": rank_type,
            "rank_name": rank_name,
            "videos": videos,
            "summary": summary
        }
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✓ 数据已保存: {output_path}")

    # Step 3: 生成 prompt 并更新趋势
    prompt, top_keywords = generate_prompt(rank_type, videos, summary)
    save_trend(rank_type, summary.get("top_zone", ""), top_keywords, summary.get("avg_interaction_rate", 0))
    print(f"✓ 趋势数据已更新")

    # Step 4: 自动调用子 Agent（除非指定 --manual）
    if args.manual:
        print(f"\n手动模式，跳过子 Agent 调用")
        print("=" * 50)
        print("Prompt 如下：")
        print("-" * 50)
        print(prompt)
        return

    print(f"\n{'='*50}")
    print("正在自动调用子 Agent 进行分析...")
    print("=" * 50)

    if spawn_analysis_agent(prompt):
        print("✓ 子 Agent 已启动")
        print(f"  分析报告将保存到: {ANALYSIS_DIR}")
    else:
        print("! 子 Agent 不可用")
        print("  输出 prompt 供手动使用：")
        print("-" * 50)
        print(prompt)


if __name__ == "__main__":
    main()

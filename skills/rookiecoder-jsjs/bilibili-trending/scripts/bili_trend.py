import requests
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# ========== 路径配置 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
OPENCLAW_JSON_DIR = os.path.join(WORKSPACE, "json")
ANALYSIS_DIR = os.path.join(WORKSPACE, "memory", "bilibili-analysis")
TREND_FILE = os.path.join(ANALYSIS_DIR, "trend.json")

os.makedirs(OPENCLAW_JSON_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

from config import RANK_CONFIG


def get_json_path(rank_type="all"):
    """获取 JSON 输出路径"""
    return os.path.join(OPENCLAW_JSON_DIR, f"output_{rank_type}.json")


def load_json_data(rank_type="all"):
    """加载最新数据"""
    json_path = get_json_path(rank_type)
    if not os.path.exists(json_path):
        # 兼容旧版本
        json_path = os.path.join(OPENCLAW_JSON_DIR, "output.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"文件不存在: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_trend():
    """加载趋势数据"""
    if os.path.exists(TREND_FILE):
        with open(TREND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "keywords": {}, "zones": {}, "rank_stats": {}}


def save_analysis(analysis_content, trend_data, rank_type="all"):
    """保存单次分析结果"""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    # 保存报告
    rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type)
    report_path = os.path.join(ANALYSIS_DIR, f"{rank_name}_{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(analysis_content)

    # 更新趋势
    trend = load_trend()
    record = {
        "time": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rank_type": rank_type,
        "top_zone": trend_data.get("top_zone", ""),
        "avg_interaction": trend_data.get("avg_interaction_rate", 0),
        "keywords": trend_data.get("keywords", []),
    }
    trend["records"].append(record)

    # 更新关键词
    for kw in trend_data.get("keywords", []):
        trend["keywords"][kw] = trend["keywords"].get(kw, 0) + 1

    # 更新分区
    zone = trend_data.get("top_zone", "")
    if zone:
        trend["zones"][zone] = trend["zones"].get(zone, 0) + 1

    # 更新榜单统计
    if rank_type not in trend["rank_stats"]:
        trend["rank_stats"][rank_type] = 0
    trend["rank_stats"][rank_type] += 1

    trend["records"] = trend["records"][-60:]

    with open(TREND_FILE, "w", encoding="utf-8") as f:
        json.dump(trend, f, ensure_ascii=False, indent=2)

    return report_path


def analyze_trend(rank_type=None):
    """生成趋势报告"""
    trend = load_trend()

    if rank_type:
        # 单榜单分析
        filtered = [r for r in trend["records"] if r.get("rank_type") == rank_type]
        if len(filtered) < 3:
            return f"{RANK_CONFIG.get(rank_type, {}).get('name', rank_type)} 数据不足"

        zone_counter = {}
        kw_counter = {}
        for r in filtered:
            zone = r.get("top_zone", "")
            if zone:
                zone_counter[zone] = zone_counter.get(zone, 0) + 1
            for kw in r.get("keywords", []):
                kw_counter[kw] = kw_counter.get(kw, 0) + 1

        report = f"# {RANK_CONFIG.get(rank_type, {}).get('name', rank_type)} 趋势分析\n\n"
        report += f"分析次数: {len(filtered)} 次\n\n"
        report += "## 热门分区\n"
        for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"- {zone}: {count} 次\n"
        report += "\n## 高频关键词\n"
        for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {kw}: {count} 次\n"
        return report

    # 全局趋势
    if len(trend["records"]) < 3:
        return "数据不足，需要至少 3 次记录"

    report = "# Bilibili 全站趋势分析\n\n"

    report += "## 各榜单热度统计\n"
    for rank, count in sorted(trend.get("rank_stats", {}).items(), key=lambda x: x[1], reverse=True):
        rank_name = RANK_CONFIG.get(rank, {}).get("name", rank)
        report += f"- {rank_name}: {count} 次\n"

    report += "\n## 热门分区 TOP 5\n"
    for zone, count in sorted(trend["zones"].items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"

    report += "\n## 高频关键词 TOP 10\n"
    for kw, count in sorted(trend["keywords"].items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"

    return report


def generate_weekly_summary(rank_type=None):
    """生成周总结"""
    trend = load_trend()
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    records = trend["records"]
    if rank_type:
        records = [r for r in records if r.get("rank_type") == rank_type]

    weekly_records = []
    for r in records:
        try:
            r_date = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if r_date >= week_ago:
                weekly_records.append(r)
        except:
            continue

    if not weekly_records:
        return "本周无数据"

    zone_counter = {}
    kw_counter = {}
    interactions = []

    for r in weekly_records:
        zone = r.get("top_zone", "")
        if zone:
            zone_counter[zone] = zone_counter.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            kw_counter[kw] = kw_counter.get(kw, 0) + 1
        interactions.append(r.get("avg_interaction", 0))

    avg_interaction = sum(interactions) / len(interactions) if interactions else 0

    rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"

    report = f"# 周总结 - {rank_name} ({week_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(weekly_records)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 热门分区\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:3]:
        report += f"- {zone}: {count} 次\n"

    report += "\n## 热门关键词\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {kw}: {count} 次\n"

    prefix = f"weekly-{rank_type}" if rank_type else "weekly"
    weekly_path = os.path.join(ANALYSIS_DIR, f"{prefix}-{now.strftime('%YW%W')}.md")
    with open(weekly_path, "w", encoding="utf-8") as f:
        f.write(report)

    return report


def generate_monthly_summary(rank_type=None):
    """生成月总结"""
    trend = load_trend()
    now = datetime.now()
    month_ago = now - timedelta(days=30)

    records = trend["records"]
    if rank_type:
        records = [r for r in records if r.get("rank_type") == rank_type]

    monthly_records = []
    for r in records:
        try:
            r_date = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if r_date >= month_ago:
                monthly_records.append(r)
        except:
            continue

    if not monthly_records:
        return "本月无数据"

    zone_counter = {}
    kw_counter = {}
    interactions = []

    for r in monthly_records:
        zone = r.get("top_zone", "")
        if zone:
            zone_counter[zone] = zone_counter.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            kw_counter[kw] = kw_counter.get(kw, 0) + 1
        interactions.append(r.get("avg_interaction", 0))

    avg_interaction = sum(interactions) / len(interactions) if interactions else 0

    rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"

    report = f"# 月总结 - {rank_name} ({month_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(monthly_records)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 分区排名\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"

    report += "\n## 关键词排行\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"

    report += "\n## 趋势洞察\n"
    if kw_counter:
        top_kw = max(kw_counter.items(), key=lambda x: x[1])[0]
        report += f"- 下月预测: {top_kw} 相关内容可能持续火热\n"

    prefix = f"monthly-{rank_type}" if rank_type else "monthly"
    monthly_path = os.path.join(ANALYSIS_DIR, f"{prefix}-{now.strftime('%Y-%m')}.md")
    with open(monthly_path, "w", encoding="utf-8") as f:
        f.write(report)

    return report


def list_ranks():
    """列出所有榜单"""
    print("\n可用榜单列表:")
    print("-" * 40)
    for key, config in RANK_CONFIG.items():
        print(f"  {key:15} - {config['name']}")
    print("-" * 40)
    print(f"共 {len(RANK_CONFIG)} 个榜单\n")


def spawn_analysis_agent(prompt, rank_type):
    """调用子 Agent 分析"""
    try:
        from sessions_spawn import sessions_spawn
        response = sessions_spawn(
            label=f"bili-{rank_type}",
            runtime="subagent",
            task=prompt,
            timeoutSeconds=120
        )
        return response.get('status') == 'accepted'
    except ImportError:
        return False
    except Exception:
        return False


def run_workflow(rank_type="all", auto_spawn=True):
    """运行工作流"""
    json_data = load_json_data(rank_type)
    videos = json_data["data"]["videos"]
    summary = json_data["data"]["summary"]
    rank_name = json_data["data"].get("rank_name", RANK_CONFIG.get(rank_type, {}).get("name", rank_type))

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

    trend_data = {
        "top_zone": summary.get("top_zone", ""),
        "avg_interaction_rate": avg_ir,
        "keywords": top_keywords,
    }

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

    analysis_prompt = f"""请深度分析 Bilibili {rank_name} 榜单数据（共{total_videos}条视频）。

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

    if auto_spawn:
        print(f"\n{'='*50}")
        print("正在自动调用子 Agent 进行分析...")
        print("=" * 50)

        if spawn_analysis_agent(analysis_prompt, rank_type):
            print("✓ 子 Agent 已启动")
            print(f"  分析报告将保存到: {ANALYSIS_DIR}")
            return {"status": "spawned", "rank_type": rank_type}
        else:
            print("! 子 Agent 不可用")
            print("  Prompt 如下：")
            print("-" * 50)
            print(analysis_prompt)
            return {"status": "failed", "prompt": analysis_prompt}

    print(analysis_prompt)
    return {"status": "ready", "prompt": analysis_prompt, "trend_data": trend_data, "rank_type": rank_type}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_ranks()
        elif sys.argv[1] == "weekly":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(generate_weekly_summary(rank))
        elif sys.argv[1] == "monthly":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(generate_monthly_summary(rank))
        elif sys.argv[1] == "trend":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(analyze_trend(rank))
        else:
            auto = "--no-spawn" not in sys.argv
            run_workflow(sys.argv[1], auto_spawn=auto)
    else:
        run_workflow("all")

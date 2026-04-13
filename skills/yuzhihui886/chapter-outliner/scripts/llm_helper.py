#!/usr/bin/env python3
"""LLM 辅助工具 - 章节内容分析（纯规则版，无需外部 API）"""

from typing import Any


def analyze_chapter_content(
    chapter_summary: str,
    chapter_num: int,
    total_chapters: int = 0,
) -> dict[str, Any]:
    """分析章节内容，返回故事位置和类型信息

    Args:
        chapter_summary: 章节概述
        chapter_num: 章节编号
        total_chapters: 总章节数

    Returns:
        分析结果字典
    """
    # 计算故事位置（基于章节比例）
    if total_chapters > 0:
        ratio = chapter_num / total_chapters
        if ratio <= 0.15:
            story_position = "开场"
            three_act = "第一幕：设定"
        elif ratio <= 0.5:
            story_position = "发展"
            three_act = "第二幕：对抗"
        elif ratio <= 0.75:
            story_position = "中段"
            three_act = "第二幕：对抗"
        elif ratio <= 0.9:
            story_position = "高潮前"
            three_act = "第三幕：解决"
        else:
            story_position = "高潮/结局"
            three_act = "第三幕：解决"
    else:
        # 未知总章节数时，使用默认逻辑
        if chapter_num <= 3:
            story_position = "开场"
            three_act = "第一幕：设定"
        elif chapter_num <= 10:
            story_position = "发展"
            three_act = "第二幕：对抗"
        elif chapter_num <= 20:
            story_position = "中段"
            three_act = "第二幕：对抗"
        elif chapter_num <= 25:
            story_position = "高潮前"
            three_act = "第三幕：解决"
        else:
            story_position = "高潮/结局"
            three_act = "第三幕：解决"

    # 分析章节类型（基于关键词）
    chapter_type = _detect_chapter_type(chapter_summary)

    return {
        "story_position": story_position,
        "three_act_structure": three_act,
        "chapter_type": chapter_type,
        "chapter_num": chapter_num,
        "total_chapters": total_chapters,
    }


def _detect_chapter_type(summary: str) -> str:
    """检测章节类型"""
    summary_lower = summary.lower()

    type_keywords = {
        "角色引入": ["介绍", "初遇", "登场", "出现", "认识"],
        "冲突升级": ["冲突", "战斗", "对决", "争吵", "矛盾"],
        "情感转折": ["感情", "爱情", "友情", "背叛", "信任", "感动"],
        "推理探案": ["调查", "线索", "真相", "推理", "发现"],
        "世界观展开": ["世界", "设定", "规则", "历史", "背景"],
        "日常过渡": ["日常", "休息", "准备", "计划", "讨论"],
    }

    for chapter_type, keywords in type_keywords.items():
        if any(kw in summary_lower for kw in keywords):
            return chapter_type

    return "一般章节"


def generate_beat_description(
    beat_num: int,
    beat_name: str,
    phase: str,
    chapter_analysis: dict[str, Any],
    chapter_summary: str = "",
) -> dict[str, str]:
    """生成节拍的动态描述

    Args:
        beat_num: 节拍编号
        beat_name: 节拍名称
        phase: 阶段（铺垫/转折/高潮/结局）
        chapter_analysis: 章节分析结果
        chapter_summary: 章节概述

    Returns:
        包含 description 和 purpose 的字典
    """
    chapter_type = chapter_analysis.get("chapter_type", "一般章节")

    # 根据章节类型和阶段生成描述
    descriptions = {
        "角色引入": {
            "铺垫": "引入新角色，建立第一印象和初步印象",
            "转折": "角色展现隐藏特质或秘密",
            "高潮": "角色面临考验，展现真实性格",
            "结局": "角色关系确立，为后续发展埋下伏笔",
        },
        "冲突升级": {
            "铺垫": "冲突的前兆，紧张气氛开始积累",
            "转折": "冲突爆发，双方正面交锋",
            "高潮": "冲突达到顶点，决定性时刻",
            "结局": "冲突结果揭晓，胜负已分",
        },
        "情感转折": {
            "铺垫": "情感变化的前兆，微妙的心理活动",
            "转折": "情感爆发或转变的关键时刻",
            "高潮": "情感的最高点，内心挣扎或释放",
            "结局": "情感尘埃落定，关系重新定义",
        },
    }

    type_desc = descriptions.get(chapter_type, {}).get(
        phase, f"{phase}阶段的{beat_name}节拍"
    )

    # 添加章节概述信息
    if chapter_summary:
        summary_preview = chapter_summary[:50]
        description = f"【{chapter_type}】{type_desc}\n相关概述：{summary_preview}"
    else:
        description = f"【{chapter_type}】{type_desc}"

    purpose = f"完成{phase}阶段的{beat_name}，推动{chapter_type}情节发展"

    return {"description": description, "purpose": purpose}

"""
主动推送模块
负责教练推送的时间调度和消息生成

三个推送各有侧重：
- 09:00: 今日训练建议 + 个性化教练洞察
- 18:00: 明日训练计划 + 教练反馈
- 20:00: 打卡激励 + 训练记录

与早晚报告不同，推送侧重于：
- AI教练视角的个性化建议
- 训练计划和执行
- 用户互动和激励
"""

import os
import sys
from datetime import datetime, time
from typing import List, Optional

# 设置路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from lib.data_cleaner import get_whoop_data, get_today_data

def _get_health_score():
    try:
        from lib.health_score import calculate_health_score
        return calculate_health_score()
    except:
        return {"score": 0, "grade": "N/A", "breakdown": {}}

def _get_ml_prediction():
    try:
        from lib.ml_predictor import predict_next_day
        return predict_next_day()
    except:
        return {"prediction": 50, "confidence": "low", "reason": ""}

def _get_comprehensive():
    try:
        from lib.comprehensive_analysis import generate_comprehensive
        return generate_comprehensive()
    except:
        return {"heart_zones": {}, "sleep_stages": {}, "body_battery": {}, "hrv_trend": {}}

def _get_health_advisor():
    try:
        from lib.health_advisor import generate_health_report
        return generate_health_report()
    except:
        return {"overall_score": 0, "insights": [], "training_recommendation": {"message": ""}}


class CoachPushMessage:
    """教练推送消息生成"""
    
    @staticmethod
    def morning() -> str:
        """
        09:00 早安推送 - AI教练视角
        
        重点：
        - AI教练对今日状态的解读
        - 个性化训练建议（基于恢复）
        - 今日训练推荐
        - 教练鼓励和激励
        """
        today = get_today_data()
        summary = get_whoop_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        advisor = _get_health_advisor()
        
        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        training_days = summary.get('training_days', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        
        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)
        
        # ========== AI教练状态评估 ==========
        if recovery >= 80:
            coach_mood = "🎉 太棒了！"
            coach_vibe = "今天你的身体状态处于最佳区间，作为你的教练，我为你感到骄傲！这种状态下，你的运动表现会非常出色。"
        elif recovery >= 60:
            coach_mood = "💪 状态不错！"
            coach_vibe = "今天你的身体状态良好，神经系统运作正常。这是一个适合训练的日子，可以考虑进行一次高质量的训练。"
        elif recovery >= 40:
            coach_mood = "🤔 恢复一般"
            coach_vibe = "作为你的教练，我认为今天需要注意一下。虽然可以训练，但建议降低强度，以身体感受为主，不要勉强。"
        else:
            coach_mood = "🛋️ 建议休息"
            coach_vibe = "亲爱的，我必须诚实告诉你：今天的身体状态不适合训练。休息不是软弱，而是为了让明天的你更强。好好休息吧。"
        
        # ========== 个性化训练建议 ==========
        if recovery >= 80:
            plan_type = "全力以赴日"
            plan_desc = "今天适合高强度训练，可以挑战个人纪录或进行力量训练"
            plan_strain = "目标strain: 12-15"
            exercises = ["力量训练（胸/背/腿）", "间歇跑", "HIIT"]
            coach_tip = "这是你展现训练成果的日子！全力以赴，但记得做好热身。"
        elif recovery >= 60:
            plan_type = "稳定进步日"
            plan_desc = "今天适合中等强度训练，保持稳定的训练节奏"
            plan_strain = "目标strain: 8-12"
            exercises = ["跑步（中等配速）", "力量训练", "游泳"]
            coach_tip = "稳扎稳打是进步的关键。今天的训练重点是保持节奏，不要过于追求强度。"
        elif recovery >= 40:
            plan_type = "轻量活动日"
            plan_desc = "今天建议以轻度活动为主，关注身体感受"
            plan_strain = "目标strain: 5-8"
            exercises = ["瑜伽/拉伸", "散步", "轻松骑行"]
            coach_tip = "倾听身体的声音。今天的活动重点是激活肌肉，而不是消耗能量。"
        else:
            plan_type = "完全休息日"
            plan_desc = "今天身体需要休息，这是训练计划的一部分"
            plan_strain = "目标strain: 0-3"
            exercises = ["充分睡眠", "轻度拉伸", "冥想放松"]
            coach_tip = "休息也是训练的一部分，甚至是最重要的部分。今天就让自己完全恢复吧。"
        
        # ========== HRV解读 ==========
        if hrv >= 60:
            hrv_coach = "你的HRV非常出色，说明神经系统非常健康。这种状态下你的恢复速度也会很快。"
        elif hrv >= 40:
            hrv_coach = "HRV处于正常范围，身体状态稳定。这是进行常规训练的好时机。"
        elif hrv >= 25:
            hrv_coach = "HRV偏低一些，可能近期有一些疲劳累积。建议今天训练后多注意休息。"
        else:
            hrv_coach = "HRV较低，神经系统可能处于疲劳状态。今天强烈建议以休息为主。"
        
        # ========== 本周回顾 ==========
        if training_days >= 6:
            week_review = "本周你已经训练了{}天，训练量较大。我建议适当休息1-2天，让身体充分恢复后再继续。".format(training_days)
        elif training_days >= 4:
            week_review = "本周你训练了{}天，节奏不错。继续保持，但注意不要连续训练超过4-5天。".format(training_days)
        else:
            week_review = "本周你只训练了{}天，如果你感觉状态好，可以考虑今天加一次训练。".format(training_days)
        
        # ========== 教练鼓励 ==========
        if recovery >= 60:
            encouragement = "准备好了吗？让我们开始今天的训练吧！💪"
        elif recovery >= 40:
            encouragement = "听从身体的反馈，我们慢慢来。一步一个脚印，你已经在进步了。🌱"
        else:
            encouragement = "今天的任务就是：好好休息。这是变强的必经之路。🌙"
        
        # ========== ML预测参考 ==========
        ml_emoji = "🟢" if ml_p >= 70 else "🟡" if ml_p >= 50 else "🔴"
        
        # ========== 健康评分 ==========
        hs_emoji = "🟢" if hs_score >= 70 else "🟡" if hs_score >= 50 else "🟠"
        
        # ========== 综合分析 ==========
        comp = comprehensive
        hz = comp.get('heart_zones', {})
        hz_aerobic = hz.get('aerobic', 0)
        hz_anaerobic = hz.get('anaerobic', 0)
        zone01 = hz.get('zone0', 0) + hz.get('zone1', 0)
        
        # ========== 顾问洞察 ==========
        advisor_insights = advisor.get('insights', [])
        advisor_training = advisor.get('training_recommendation', {}).get('message', '')
        
        # ========== 构建消息 ==========
        msg = "☀️ **早安！我是你的AI健身教练**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🤖 **教练视角今日评估**\n\n"
        msg += "{}\n\n".format(coach_mood)
        msg += "{}\n\n".format(coach_vibe)
        msg += "💡 **解读**：恢复评分是我们判断今天能否训练的核心依据。它综合了你的HRV，心率、睡眠等多维度数据。\n\n"
        msg += "📈 **HRV专项分析**\n\n"
        msg += "{:.1f}ms\n".format(hrv)
        msg += "{}\n\n".format(hrv_coach)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🎯 **今日训练计划**\n\n"
        msg += "**计划类型**：{}\n".format(plan_type)
        msg += "**计划描述**：{}\n".format(plan_desc)
        msg += "**{}\n\n".format(plan_strain)
        msg += "**推荐训练**：\n"
        for ex in exercises:
            msg += "• {}\n".format(ex)
        msg += "\n💡 **教练建议**：{}\n\n".format(coach_tip)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📋 **本周训练回顾**\n\n"
        msg += "{}\n\n".format(week_review)
        if sleep_debt > 2:
            msg += "⚠️ 睡眠债务提醒：你有{:.1f}小时的睡眠债务，近期注意多睡。\n\n".format(sleep_debt)
        msg += "🔮 **近期预测参考**\n\n"
        msg += "{} 明日预测恢复：{:.0f}%\n".format(ml_emoji, ml_p)
        msg += "💡 **解读**：这是基于你历史数据的机器学习预测，可以帮助我们规划明天的训练。\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📊 **综合数据参考**\n\n"
        msg += "• 心率区间：有氧{:.1f}% / 无氧{:.1f}%\n".format(hz_aerobic, hz_anaerobic)
        msg += "• 健康评分：{} {:.0f}/100\n".format(hs_emoji, hs_score)
        msg += "\n{}\n\n".format(encouragement)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 **如何使用今日计划**\n\n"
        msg += "• 训练前：先做5-10分钟热身\n"
        msg += "• 训练中：保持专注，感受身体反馈\n"
        msg += "• 训练后：记得来20:00打卡记录！\n\n"
        msg += "⏰ 下次推送：今天18:00 晚间追踪\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg
    
    @staticmethod
    def evening() -> str:
        """
        18:00 晚间推送 - 教练反馈与明日计划
        
        重点：
        - 今日训练总结（教练视角）
        - 明日训练预告
        - 个性化调整建议
        - 激励与关怀
        """
        today = get_today_data()
        summary = get_whoop_data(7)
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        advisor = _get_health_advisor()
        
        recovery = today.get('recovery', 0)
        strain = today.get('strain', 0)
        has_training = today.get('has_training', False)
        
        training_days = summary.get('training_days', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        
        hs_score = health_score.get('score', 0)
        hs_grade = health_score.get('grade', 'N/A')
        ml_p = ml_pred.get('prediction', 50)
        ml_conf = ml_pred.get('confidence', 'low')
        ml_reason = ml_pred.get('reason', '')
        
        # ========== 今日训练总结 ==========
        if has_training and strain > 0:
            if strain >= 12:
                training_eval = "💪 出色完成！"
                training_review = "今天你的strain达到了{:.1f}，这是一次非常高强度的训练。你付出了100%的努力！作为你的教练，我为你的表现感到骄傲。".format(strain)
                training_feeling = "全身泵感十足，肌肉刺激到位"
                training_effect = "这次训练会有效提升你的力量和耐力"
            elif strain >= 8:
                training_eval = "🏃 不错的训练！"
                training_review = "今天你的strain为{:.1f}，完成了中等强度的训练。训练量适中，对保持体能很有帮助。".format(strain)
                training_feeling = "身体微微疲劳，但感觉良好"
                training_effect = "维持体能，保持训练节奏"
            else:
                training_eval = "🚶 轻度活动"
                training_review = "今天活动量较小，strain为{:.1f}。虽然没有正式训练，但保持日常活动对身体也有好处。".format(strain)
                training_feeling = "身体轻松，精神不错"
                training_effect = "保持活跃状态，避免久坐"
        else:
            training_eval = "😌 今日休息"
            training_review = "今天你选择了休息，这对身体恢复非常重要。训练不只是动，动和休息的平衡才是进步的关键。"
            training_feeling = "身体在恢复中，能量储备中"
            training_effect = "充分恢复，为明天做准备"
        
        # ========== 教练点评 ==========
        if recovery >= 70:
            coach_comment = "你的身体恢复得非常好！看来之前的训练和休息安排得很合理。"
        elif recovery >= 50:
            coach_comment = "恢复状态处于中等水平。注意不要连续高强度训练，给身体留出恢复时间。"
        else:
            coach_comment = "恢复状态不太理想，可能是之前的训练强度过大或休息不足。建议增加休息日。"
        
        # ========== 明日预测与计划 ==========
        ml_emoji = "🟢" if ml_p >= 70 else "🟡" if ml_p >= 50 else "🔴"
        hs_emoji = "🟢" if hs_score >= 70 else "🟡" if hs_score >= 50 else "🔴"
        
        if ml_p >= 70:
            tomorrow_plan = "根据预测，明天你的状态应该会很好！"
            tomorrow_type = "可以进行一次高质量训练"
            tomorrow_strain = "目标strain: 10-14"
            tomorrow_exercises = ["力量训练", "节奏跑", "综合训练"]
        elif ml_p >= 50:
            tomorrow_plan = "明天的状态可能一般，建议保持中等强度。"
            tomorrow_type = "中等强度训练或休息"
            tomorrow_strain = "目标strain: 6-10"
            tomorrow_exercises = ["轻松跑", "瑜伽", "拉伸放松"]
        else:
            tomorrow_plan = "预测显示疲劳还在累积，建议明天继续休息。"
            tomorrow_type = "以休息恢复为主"
            tomorrow_strain = "目标strain: 0-5"
            tomorrow_exercises = ["充足睡眠", "轻度拉伸", "冥想放松"]
        
        # ========== 本周总结 ==========
        if training_days >= 6:
            week_summary = "本周你已经训练了{}天，训练量较大。{}".format(
                training_days,
                "注意安排1-2天完全休息。" if training_days >= 7 else "注意不要超过6-7天。"
            )
        elif training_days >= 4:
            week_summary = "本周你训练了{}天，节奏比较合理。继续坚持！".format(training_days)
        else:
            week_summary = "本周你只训练了{}天，如果你状态好可以适当增加。".format(training_days)
        
        # ========== 睡眠提醒 ==========
        if sleep_debt > 5:
            sleep_reminder = "⚠️ 你有{:.1f}小时的睡眠债务！今晚尽量提前睡觉，这对恢复非常重要。".format(sleep_debt)
        elif sleep_debt > 2:
            sleep_reminder = "📝 有轻微睡眠债务（{:.1f}小时），近期注意早点休息。".format(sleep_debt)
        else:
            sleep_reminder = ""
        
        # ========== 教练关怀 ==========
        if recovery < 50:
            care_msg = "我注意到你的恢复状态不太理想。作为你的教练，我建议你今晚早点睡觉，睡眠是最好的恢复方式。🌙"
        elif has_training and strain >= 10:
            care_msg = "今天训练强度很大！记得补充营养，训练后30分钟内摄入蛋白质很重要。💪"
        else:
            care_msg = "保持现在的节奏，你做得很好！有任何问题随时问我。🌟"
        
        # ========== 综合分析 ==========
        comp = comprehensive
        hz = comp.get('heart_zones', {})
        hz_aerobic = hz.get('aerobic', 0)
        hz_anaerobic = hz.get('anaerobic', 0)
        zone01 = hz.get('zone0', 0) + hz.get('zone1', 0)
        
        # ========== 顾问洞察 ==========
        advisor_insights = advisor.get('insights', [])
        advisor_msg = ""
        if advisor_insights:
            advisor_msg = "• " + "\n• ".join(advisor_insights[:3])
        
        # ========== 构建消息 ==========
        msg = "🌙 **晚间教练追踪**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🤖 **教练今日总结**\n\n"
        msg += "{}\n{}\n\n".format(training_eval, training_review)
        msg += "💡 **解读**：这是从教练视角对今天训练的整体评估。无论训练还是休息，都是训练计划的一部分。\n\n"
        msg += "📊 **训练感受**\n{}\n\n".format(training_feeling)
        msg += "💡 **训练效果**：{}\n\n".format(training_effect)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🔮 **教练点评**\n\n"
        msg += "{}\n\n".format(coach_comment)
        msg += "💡 **恢复参考**：今日恢复 {:.0f}%，健康评分 {} {}/100 ({})\n\n".format(
            recovery, hs_emoji, hs_score, hs_grade
        )
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📅 **明日训练预告**\n\n"
        msg += "{}\n\n".format(tomorrow_plan)
        msg += "**计划类型**：{}\n".format(tomorrow_type)
        msg += "**{}\n\n".format(tomorrow_strain)
        msg += "**推荐活动**：\n"
        for ex in tomorrow_exercises:
            msg += "• {}\n".format(ex)
        msg += "\n💡 **解读**：这是根据你今天的数据和ML预测给出的明日建议。\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📋 **本周训练总览**\n\n"
        msg += "本周训练天数：{}天\n".format(training_days)
        msg += "本周平均恢复：{:.0f}%\n\n".format(avg_recovery)
        msg += "{}\n\n".format(week_summary)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📊 **综合数据**\n\n"
        msg += "• 心率区间：有氧{:.1f}% / 无氧{:.1f}%\n".format(hz_aerobic, hz_anaerobic)
        msg += "• ML预测：{} {}/100 (置信度: {})\n\n".format(ml_emoji, ml_p, ml_conf)
        if sleep_reminder:
            msg += "{}\n\n".format(sleep_reminder)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "💬 **教练寄语**\n\n"
        msg += "{}\n\n".format(care_msg)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📌 **晚间提醒**\n\n"
        msg += "记得20:00来这里打卡记录今天的训练和身体感受！打卡是你训练旅程中非常重要的一环。\n\n"
        msg += "⏰ 打卡提醒：今天22:00前来打卡！\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg
    
    @staticmethod
    def checkin_reminder() -> str:
        """
        20:00 打卡提醒推送
        
        重点：
        - 打卡重要性说明
        - 训练记录引导
        - 个性化激励
        - 教练互动邀请
        """
        today = get_today_data()
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        
        recovery = today.get('recovery', 0)
        strain = today.get('strain', 0)
        has_training = today.get('has_training', False)
        
        hs_score = health_score.get('score', 0)
        ml_p = ml_pred.get('prediction', 50)
        
        # ========== 今日状态 ==========
        if has_training and strain > 0:
            today_status = "✅ 今日已完成训练"
            status_detail = "strain达到{:.1f}，训练效果不错".format(strain)
            checkin_prompt = "记录一下今天练了什么、感觉怎么样"
        else:
            today_status = "📝 今日为休息日"
            status_detail = "充分休息也是训练的一部分"
            checkin_prompt = "如果你做了拉伸或冥想，也记录一下"
        
        # ========== 打卡重要性 ==========
        checkin_importance = [
            "帮助你追踪训练频率和强度变化",
            "让我更了解你的训练模式和习惯",
            "发现训练和恢复之间的规律",
            "保持对训练的正向专注和动力",
            "让每次训练都有记录可追溯"
        ]
        
        # ========== 打卡示例 ==========
        if has_training and strain > 0:
            examples = [
                ("力量训练", "深蹲 100kg 5x5 全部完成 | 腿部泵感很强"),
                ("跑步", "间歇跑 5公里 配速5:30 | 呼吸略急促"),
                ("综合", "CrossFit训练 整体状态不错 | 消耗很大"),
            ]
        else:
            examples = [
                ("休息", "今天完全休息 | 感觉恢复了一些"),
                ("拉伸", "睡前做了15分钟拉伸 | 身体放松很多"),
                ("冥想", "10分钟呼吸练习 | 精神放松"),
            ]
        
        # ========== 教练激励 ==========
        if has_training and strain >= 10:
            motivate = "太棒了！今天的训练强度很大，你付出了很多努力。记录下来，这是你变强的证明！💪"
        elif has_training:
            motivate = "完成今天的训练就是进步！来记录一下，我会帮你追踪进步。🌱"
        else:
            motivate = "休息也是训练的一部分。今天你选择倾听身体的声音，这是明智的选择。🌙"
        
        # ========== 个性化提醒 ==========
        if ml_p < 50:
            ml_reminder = "📊 预测显示你可能有些疲劳，明天可能也需要休息。打卡时告诉我你现在的身体感受，这对我分析很有帮助。"
        elif recovery < 50:
            ml_reminder = "📊 你的恢复评分还有些低，打卡时记录一下睡眠质量和身体感受，帮助我更好地了解你的状态。"
        else:
            ml_reminder = ""
        
        # ========== 教练签名 ==========
        coach_sign = "我是你的AI教练，随时在这里等你！有任何训练问题或身体状况，都可以告诉我。🌟"
        
        # ========== 健康评分 ==========
        hs_emoji = "🟢" if hs_score >= 70 else "🟡" if hs_score >= 50 else "🔴"
        
        # ========== 构建消息 ==========
        msg = "📊 **训练打卡提醒**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🤖 **教练呼叫** {} \n\n".format(today_status)
        msg += "{}\n\n".format(status_detail)
        msg += "{} 今日恢复：{:.0f}%\n".format(
            "🔴" if recovery < 50 else "🟡" if recovery < 70 else "🟢",
            recovery
        )
        msg += "{} 健康评分：{:.0f}/100\n".format(hs_emoji, hs_score)
        msg += "🔮 ML预测明日：{:.0f}%\n\n".format(ml_p)
        msg += "💡 **解读**：打卡是训练旅程中非常重要的一环！记录不只是数据，更是你努力和进步的证明。\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🎯 **打卡的重要性**\n\n"
        for imp in checkin_importance:
            msg += "• {}\n".format(imp)
        msg += "\n{}\n\n".format(checkin_prompt)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "💬 **如何打卡**\n\n"
        msg += "直接发送你的训练记录给我即可！\n\n"
        msg += "**格式**：训练内容 | 完成情况 | 身体感受\n\n"
        msg += "**示例**：\n"
        for tag, desc in examples:
            msg += "`{} | {}`\n".format(tag, desc)
        msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "{}\n\n".format(motivate)
        if ml_reminder:
            msg += "{}\n\n".format(ml_reminder)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "🌟 **为什么打卡？**\n\n"
        msg += "作为你的AI教练，我需要了解：\n"
        msg += "• 你今天实际训练了什么\n"
        msg += "• 训练强度和量是多少\n"
        msg += "• 身体感受如何\n"
        msg += "• 睡眠和精神状态\n\n"
        msg += "这些信息帮助我：\n"
        msg += "• 更精准地分析你的训练模式\n"
        msg += "• 给出更个性化的建议\n"
        msg += "• 在你疲惫时提醒休息\n"
        msg += "• 在你进步时给予鼓励\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "⏰ **随时可以打卡**\n\n"
        msg += "不用在意格式，简单记录也很好：\n"
        msg += "• \"练了腿\"\n"
        msg += "• \"跑了步\"\n"
        msg += "• \"休息了一天\"\n\n"
        msg += "我都能理解并记录！\n\n"
        msg += "{}\n\n".format(coach_sign)
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += "📌 **温馨提示**\n\n"
        msg += "打卡没有硬性要求一天不落，偶尔休息或忘记打卡是完全正常的。重要的是保持对自己身体的关注和了解。\n\n"
        msg += "我在等你，训练记录交给我！🏋️\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg


class CoachScheduler:
    """推送调度器"""
    
    PUSH_TIMES = {
        "morning": {"hour": 9, "minute": 0},
        "evening": {"hour": 18, "minute": 0},
        "checkin": {"hour": 20, "minute": 0},
    }
    
    @staticmethod
    def should_push(push_type: str) -> bool:
        now = datetime.now()
        push_time = CoachScheduler.PUSH_TIMES.get(push_type)
        if not push_time:
            return False
        return now.hour == push_time["hour"] and now.minute == push_time["minute"]

#!/usr/bin/env python3
from __future__ import annotations

from typing import Any


def build_cycle_summary(result: dict[str, Any]) -> dict[str, Any]:
    search = result.get("search") or {}
    send = result.get("send") or {}
    replies = result.get("replies") or {}
    reply_actions = result.get("replyActions") or {}
    reply_strict = result.get("replyStrictMode") or {}

    return {
        "search": {
            "success": bool(search.get("success")),
            "recommendationCount": search.get("recommendationCount", 0),
            "payloadSource": search.get("payloadSource"),
            "error": search.get("error"),
        },
        "send": {
            "status": send.get("status"),
            "preparedCount": send.get("preparedCount", 0),
            "autoSendExecuted": bool(send.get("autoSendExecuted")),
            "reviewRequired": send.get("reviewRequired"),
        },
        "replies": {
            "newReplies": replies.get("newReplies", 0),
            "classified": replies.get("classified") or {},
            "replyActionCount": reply_actions.get("count", 0),
            "autoSendEligible": reply_actions.get("autoSendEligible", 0),
            "humanReviewRequired": reply_actions.get("humanReviewRequired", 0),
            "customerSummary": reply_actions.get("customerSummary") or "",
        },
        "replyStrictMode": {
            "enabled": bool(reply_strict.get("enabled")),
            "status": reply_strict.get("status"),
            "needsReplyModelAnalysis": bool(reply_strict.get("needsReplyModelAnalysis")),
            "nextRecommendedAction": reply_strict.get("nextRecommendedAction"),
        },
    }


def build_human_cycle_summary(result: dict[str, Any]) -> str:
    summary = build_cycle_summary(result)
    search = summary["search"]
    send = summary["send"]
    replies = summary["replies"]
    strict_mode = summary["replyStrictMode"]

    search_error = search.get('error') or {}
    search_status_line = f"- 搜索：{'成功' if search.get('success') else '未成功'}；推荐 {search.get('recommendationCount', 0)} 位达人；payload 来源：{search.get('payloadSource') or '-'}"
    if search_error.get('message'):
        search_status_line += f"；失败原因：{search_error.get('message')}"

    lines = [
        "本轮 campaign 摘要：",
        search_status_line,
        f"- 发信：状态={send.get('status') or 'unknown'}；准备 {send.get('preparedCount', 0)} 封；自动执行={'是' if send.get('autoSendExecuted') else '否'}；需人工复核={'是' if send.get('reviewRequired') else '否'}",
        f"- 回复：新回复 {replies.get('newReplies', 0)} 封；待处理动作 {replies.get('replyActionCount', 0)} 个；可自动发送 {replies.get('autoSendEligible', 0)} 个；需人工复核 {replies.get('humanReviewRequired', 0)} 个",
    ]
    if strict_mode.get("enabled"):
        lines.append(f"- Reply strict mode：{strict_mode.get('status') or 'unknown'}")
        if strict_mode.get("needsReplyModelAnalysis"):
            lines.append("- 阻塞项：需要补充 reply_model_analysis 后，才能继续自动化回复闭环")
    send_status = str(send.get('status') or '')
    if send_status in {'review_required', 'prepared'}:
        lines.append("- 下一步建议：先人工确认本轮候选邮件摘要，再决定是否执行发送")
    elif replies.get('humanReviewRequired', 0) > 0:
        lines.append("- 下一步建议：优先处理需要人工复核的回复，再决定是否继续下一轮 outreach")
    else:
        lines.append("- 下一步建议：若目标数量未达标，可继续下一轮搜索；若已达标，优先跟进回复转化")
    if replies.get('customerSummary'):
        lines.append("- 高风险回复摘要：")
        lines.append(replies.get('customerSummary'))
    return "\n".join(lines)

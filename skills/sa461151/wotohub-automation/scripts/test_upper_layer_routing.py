#!/usr/bin/env python3
"""Minimal upper-layer routing / mapping checks.

This script intentionally stays above the execution layer.
It validates:
- input understanding primary task routing
- missing-field blocking behavior
- semantic context -> legacy input mapping shape

Run:
    python3 scripts/test_upper_layer_routing.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from pprint import pprint

from brief_schema import normalize_campaign_brief
from context_schema import normalize_context
from context_to_payload import to_campaign_create_input, to_generate_email_input, to_recommend_input, to_search_input
from input_understanding import understand_input
from api_task_runner import TaskRunner
from orchestrator import UpperLayerOrchestrator
from run_campaign import _extract_send_target_creator_ids, _select_email_targets
from campaign_engine import build_draft_generation_input
from api_campaign_runner import CampaignRunner
from draft_consistency_audit import audit_email_against_creator_profile
from send_generated_emails import build_batch_payload


class DryRunOrchestrator(UpperLayerOrchestrator):
    def _delegate_task(self, task_type: str, input_data: dict, config: dict) -> dict:
        return {
            "status": "dry_run",
            "taskType": task_type,
            "input": input_data,
        }


orchestrator = DryRunOrchestrator(token=None)


CASES = [
    {
        "name": "product_analysis_from_url",
        "raw_input": "帮我分析这个产品链接 https://www.amazon.com/dp/B0TEST1234",
        "explicit_task": None,
        "expected_primary_task": "product_analysis",
        "expected_delegated_task": "product_analysis",
        "expected_status": "needs_user_input",
        "expected_missing": [],
    },
    {
        "name": "generate_email_all_search_results_selection",
        "raw_input": "把这次搜索结果全发开发信",
        "explicit_task": "generate_email",
        "expected_primary_task": "generate_email",
        "expected_delegated_task": "generate_email",
        "expected_status": "needs_user_input",
        "expected_missing": ["offerType"],
    },
    {
        "name": "generate_email_top_n_selection",
        "raw_input": "每周给前 20 个达人发开发信",
        "explicit_task": "generate_email",
        "expected_primary_task": "generate_email",
        "expected_delegated_task": "generate_email",
        "expected_status": "needs_user_input",
        "expected_missing": ["offerType"],
    },
    {
        "name": "search_with_platform_and_market",
        "raw_input": "帮我找美国 TikTok 美妆达人，10万粉丝以上，推广这款面膜",
        "explicit_task": None,
        "expected_primary_task": "search",
        "expected_delegated_task": "search",
        "expected_status": "needs_user_input",
        "expected_missing": ["hostAnalysis"],
    },
    {
        "name": "campaign_create_richer_mapping",
        "raw_input": "帮我创建一个 TikTok 美国市场的 campaign，推广便携榨汁杯，送样合作",
        "explicit_task": None,
        "expected_primary_task": "campaign_create",
        "expected_delegated_task": "campaign_create",
        "expected_status": "needs_user_input",
        "expected_missing": ["hostAnalysis"],
    },
    {
        "name": "generate_email_current_compatibility_shaping",
        "raw_input": "帮我写开发信，想做送样合作",
        "explicit_task": None,
        "expected_primary_task": "generate_email",
        "expected_delegated_task": "generate_email",
        "expected_status": "needs_user_input",
        "expected_missing": ["selectedCreators"],
    },
    {
        "name": "search_current_compatibility_shaping",
        "raw_input": "帮我找达人推广这款按摩仪",
        "explicit_task": "search",
        "expected_primary_task": "search",
        "expected_delegated_task": "search",
        "expected_status": "needs_user_input",
        "expected_missing": ["hostAnalysis"],
    },
    {
        "name": "monitor_replies_empty_input_blocked",
        "raw_input": "",
        "explicit_task": "monitor_replies",
        "expected_primary_task": "monitor_replies",
        "expected_delegated_task": "monitor_replies",
        "expected_status": "needs_user_input",
        "expected_missing": ["campaignId_or_input"],
    },
    {
        "name": "monitor_replies_with_context_only",
        "raw_input": "帮我看看这封回复怎么处理，达人说先寄样再谈合作",
        "explicit_task": None,
        "expected_primary_task": "monitor_replies",
        "expected_delegated_task": "monitor_replies",
        "expected_status": "needs_user_input",
        "expected_missing": ["replyModelAnalysis"],
    },
]


def _assert_subset(actual: list[str], expected: list[str], case_name: str) -> None:
    missing = [item for item in expected if item not in actual]
    if missing:
        raise AssertionError(f"[{case_name}] expected missing fields subset {expected}, got {actual}")


def _status_of(result: dict) -> str:
    route = result.get("route") or {}
    if route.get("needsUserInput"):
        return "needs_user_input"
    return "ok"


def run_case(case: dict) -> None:
    result = orchestrator.run_from_user_input(case["raw_input"], explicit_task=case.get("explicit_task"))
    observations = result.get("observations") or {}
    route = result.get("route") or {}

    actual_primary_task = observations.get("understoodPrimaryTask")
    actual_delegated_task = result.get("delegatedTask")
    actual_status = _status_of(result)
    actual_missing = route.get("missingFields") or []

    if actual_primary_task != case["expected_primary_task"]:
        raise AssertionError(
            f"[{case['name']}] expected primary task {case['expected_primary_task']}, got {actual_primary_task}"
        )
    if actual_delegated_task != case["expected_delegated_task"]:
        raise AssertionError(
            f"[{case['name']}] expected delegated task {case['expected_delegated_task']}, got {actual_delegated_task}"
        )
    if actual_status != case["expected_status"]:
        raise AssertionError(f"[{case['name']}] expected status {case['expected_status']}, got {actual_status}")
    _assert_subset(actual_missing, case["expected_missing"], case["name"])

    print(f"PASS {case['name']}")
    pprint(
        {
            "primaryTask": actual_primary_task,
            "delegatedTask": actual_delegated_task,
            "status": actual_status,
            "missingFields": actual_missing,
            "whyRoutedThisWay": observations.get("whyRoutedThisWay"),
        }
    )
    print()


def run_mapping_checks() -> None:
    search_ctx = understand_input("帮我找美国 TikTok 美妆达人，10万粉丝以上，推广这款面膜")
    recommend_ctx = understand_input("帮我推荐适合便携榨汁杯的美国 TikTok 红人")
    campaign_ctx = understand_input("帮我创建一个 TikTok 美国市场的 campaign，推广便携榨汁杯，送样合作")
    campaign_ctx.setdefault("meta", {})["campaignId"] = "portable-juicer-us"
    email_ctx = understand_input("请帮我写一封便携榨汁杯的开发信，送样合作，面向美国 TikTok 达人")

    search_payload = to_search_input(search_ctx)
    recommend_payload = to_recommend_input(recommend_ctx)
    campaign_payload = to_campaign_create_input(campaign_ctx)
    email_payload = to_generate_email_input(email_ctx)

    if "searchPayload" not in search_payload:
        raise AssertionError("search payload should include searchPayload")
    if recommend_payload.get("recommendationMode") != "creator_match":
        raise AssertionError("recommend payload should include recommendationMode=creator_match")
    if "campaignContext" not in campaign_payload:
        raise AssertionError("campaign_create payload should include campaignContext")
    if "semanticContext" not in campaign_payload:
        raise AssertionError("campaign_create payload should include semanticContext")
    if "legacyInput" not in campaign_payload:
        raise AssertionError("campaign_create payload should include legacyInput")
    if "brief" not in email_payload or not email_payload.get("brief"):
        raise AssertionError("generate_email payload should include non-empty brief")

    e2e_email_ctx = understand_input("每周给前 20 个达人发开发信", explicit_task="generate_email")
    e2e_email_ctx.setdefault("productSignals", {})["productName"] = "便携榨汁杯"
    e2e_email_ctx.setdefault("marketingContext", {})["offerType"] = "sample"
    e2e_email_ctx.setdefault("marketingContext", {})["languages"] = ["en"]
    e2e_email_ctx.setdefault("resolvedArtifacts", {})["hostEmailDrafts"] = [
        {
            "bloggerId": "abc123",
            "subject": "Test outreach subject",
            "plainTextBody": "Hello creator",
            "htmlBody": "<p>Hello creator</p>",
        }
    ]
    e2e_email_payload = to_generate_email_input(e2e_email_ctx)
    if (e2e_email_payload.get("selectionRule") or {}).get("type") != "top_n":
        raise AssertionError(f"selectionRule should survive mapping, got {e2e_email_payload.get('selectionRule')}")
    if not e2e_email_payload.get("hostDrafts"):
        raise AssertionError("hostDrafts should survive mapping for generate_email")
    if e2e_email_payload.get("offerType") != "sample":
        raise AssertionError(f"offerType should survive mapping, got {e2e_email_payload.get('offerType')}")

    print("PASS mapping_checks")
    pprint(
        {
            "search_keys": sorted(search_payload.keys()),
            "recommend_keys": sorted(recommend_payload.keys()),
            "campaign_keys": sorted(campaign_payload.keys()),
            "email_keys": sorted(email_payload.keys()),
            "e2e_email_selection_rule": e2e_email_payload.get("selectionRule"),
            "e2e_email_host_drafts_count": len(e2e_email_payload.get("hostDrafts") or []),
        }
    )
    print()


def run_observation_checks() -> None:
    result = orchestrator.run_from_user_input(
        "请帮我写一封便携榨汁杯的开发信，送样合作，面向美国 TikTok 美妆达人，英文沟通，目标是推广"
    )
    observations = result.get("observations") or {}

    resolved_product_name = observations.get("resolvedProductName") or ""
    if resolved_product_name != "便携榨汁杯":
        raise AssertionError(f"resolvedProductName should be 便携榨汁杯, got {resolved_product_name}")
    if observations.get("resolvedOfferType") != "sample":
        raise AssertionError(f"unexpected resolvedOfferType: {observations.get('resolvedOfferType')}")
    if "tiktok" not in (observations.get("resolvedPlatforms") or []):
        raise AssertionError(f"resolvedPlatforms should contain tiktok, got {observations.get('resolvedPlatforms')}")
    if "us" not in (observations.get("resolvedTargetMarkets") or []):
        raise AssertionError(
            f"resolvedTargetMarkets should contain us, got {observations.get('resolvedTargetMarkets')}"
        )
    if observations.get("resolvedGoal") != "promotion":
        raise AssertionError(f"unexpected resolvedGoal: {observations.get('resolvedGoal')}")
    if "beauty" not in (observations.get("resolvedCreatorTypes") or []):
        raise AssertionError(
            f"resolvedCreatorTypes should contain beauty, got {observations.get('resolvedCreatorTypes')}"
        )
    if "en" not in (observations.get("resolvedLanguages") or []):
        raise AssertionError(
            f"resolvedLanguages should contain en, got {observations.get('resolvedLanguages')}"
        )

    print("PASS observation_checks")
    pprint(
        {
            "resolvedProductName": observations.get("resolvedProductName"),
            "resolvedOfferType": observations.get("resolvedOfferType"),
            "resolvedPlatforms": observations.get("resolvedPlatforms"),
            "resolvedTargetMarkets": observations.get("resolvedTargetMarkets"),
            "resolvedGoal": observations.get("resolvedGoal"),
            "resolvedCreatorTypes": observations.get("resolvedCreatorTypes"),
            "resolvedLanguages": observations.get("resolvedLanguages"),
        }
    )
    print()


def run_host_model_injection_checks() -> None:
    host_analysis = {
        "product": {
            "productName": "便携榨汁杯",
            "productType": "kitchen appliance",
            "productSubtype": "portable blender",
            "coreBenefits": ["portable", "easy cleaning"],
            "functions": ["smoothie making"],
            "price": 49.99,
            "brand": "BlendGo",
        },
        "marketing": {
            "platformPreference": ["tiktok"],
            "creatorTypes": ["lifestyle", "fitness"],
        },
        "constraints": {
            "regions": ["us"],
            "languages": ["en"],
            "minFansNum": 10000,
            "maxFansNum": 200000,
            "hasEmail": True,
        },
        "searchPayloadHints": {
            "platform": "tiktok",
            "blogLangs": ["en"],
            "minFansNum": 10000,
            "maxFansNum": 200000,
            "hasEmail": True,
        },
    }
    host_drafts = [
        {
            "bloggerId": "abc123",
            "subject": "Let's collaborate on BlendGo",
            "plainTextBody": "Hi there",
            "htmlBody": "<p>Hi there</p>",
        }
    ]
    result = orchestrator.run_from_user_input(
        "帮我给美国 TikTok 达人写便携榨汁杯开发信",
        explicit_task="generate_email",
        host_analysis=host_analysis,
        host_product_summary={"productName": "便携榨汁杯", "brand": "BlendGo"},
        host_drafts=host_drafts,
    )
    observations = result.get("observations") or {}
    legacy_input = result.get("legacyInput") or {}

    if observations.get("usedHostModel") is not True:
        raise AssertionError(f"usedHostModel should be True, got {observations.get('usedHostModel')}")
    if observations.get("usedFallback") is not False:
        raise AssertionError(f"usedFallback should be False, got {observations.get('usedFallback')}")
    if observations.get("analysisPath") != "host_model_injected_understanding":
        raise AssertionError(f"unexpected analysisPath: {observations.get('analysisPath')}")
    if observations.get("resolvedProductName") != "便携榨汁杯":
        raise AssertionError(f"resolvedProductName should be 便携榨汁杯, got {observations.get('resolvedProductName')}")
    if not legacy_input.get("hostDrafts"):
        raise AssertionError("hostDrafts should survive injected host-model path")
    if legacy_input.get("modelAnalysis", {}).get("product", {}).get("brand") != "BlendGo":
        raise AssertionError("modelAnalysis should survive injected host-model path")

    print("PASS host_model_injection_checks")
    pprint(
        {
            "usedHostModel": observations.get("usedHostModel"),
            "usedFallback": observations.get("usedFallback"),
            "analysisPath": observations.get("analysisPath"),
            "resolvedProductName": observations.get("resolvedProductName"),
            "hostDraftCount": len(legacy_input.get("hostDrafts") or []),
        }
    )
    print()


def run_host_resolution_observation_checks() -> None:
    result = orchestrator.run_from_user_input(
        "帮我给美国 TikTok 达人写 sample 合作开发信",
        explicit_task="generate_email",
        host_analysis={
            "product": {
                "productName": "便携榨汁杯",
                "productType": "kitchen appliance",
                "productSubtype": "portable blender",
                "brand": "BlendGo",
            },
            "marketing": {
                "platformPreference": ["tiktok"],
                "creatorTypes": ["lifestyle"],
            },
            "constraints": {
                "regions": ["us"],
                "languages": ["en"],
            },
        },
        host_drafts=[
            {
                "bloggerId": "abc123",
                "subject": "Let's collaborate on BlendGo",
                "plainTextBody": "Hi there",
            }
        ],
    )
    host_resolution = (result.get("observations") or {}).get("hostResolution") or {}
    analysis_resolution = host_resolution.get("hostAnalysis") or {}
    draft_resolution = host_resolution.get("hostDrafts") or {}

    if analysis_resolution.get("status") != "provided_by_input":
        raise AssertionError(f"hostAnalysis resolution should be provided_by_input, got {analysis_resolution}")
    if analysis_resolution.get("fulfilled") is not True:
        raise AssertionError(f"hostAnalysis resolution should be fulfilled, got {analysis_resolution}")
    if draft_resolution.get("status") != "provided_by_input":
        raise AssertionError(f"hostDrafts resolution should be provided_by_input, got {draft_resolution}")
    if draft_resolution.get("fulfilled") is not True:
        raise AssertionError(f"hostDrafts resolution should be fulfilled, got {draft_resolution}")

    print("PASS host_resolution_observation_checks")
    pprint({"hostResolution": host_resolution})
    print()


def run_execution_selection_rule_checks() -> None:
    sample_search_output = {
        "result": {
            "data": {
                "bloggerList": [
                    {"bloggerId": "a", "nickname": "A", "fansNum": 50000, "hasEmail": True},
                    {"bloggerId": "b", "nickname": "B", "fansNum": 12000, "hasEmail": False},
                    {"bloggerId": "c", "nickname": "C", "fansNum": 80000, "hasEmail": True},
                    {"bloggerId": "d", "nickname": "D", "fansNum": 20000, "hasEmail": True},
                ]
            }
        }
    }
    selected = _select_email_targets(
        sample_search_output,
        selection_rule={
            "type": "top_n",
            "topN": 2,
            "filters": {"minFollowers": 10000, "hasEmail": True},
            "sort": [{"field": "followers", "order": "desc"}],
        },
    )
    selected_ids = [item.get("bloggerId") for item in selected]
    if selected_ids != ["c", "a"]:
        raise AssertionError(f"execution selection rule should pick ['c', 'a'], got {selected_ids}")

    print("PASS execution_selection_rule_checks")
    pprint({"selected_ids": selected_ids, "selected": selected})
    print()


def run_campaign_create_handler_checks() -> None:
    runner = TaskRunner(token=None)
    campaign_ctx = understand_input("帮我创建一个 TikTok 美国市场的 campaign，推广便携榨汁杯，送样合作")
    payload = to_campaign_create_input(campaign_ctx)
    result = runner.run("campaign_create", payload, {"campaignId": "portable-juicer-us"})
    if result.get("campaignId") != "portable-juicer-us":
        raise AssertionError(f"unexpected campaignId: {result.get('campaignId')}")
    if not result.get("briefPath"):
        raise AssertionError("campaign_create should persist briefPath")
    if not result.get("cronSpec"):
        raise AssertionError("campaign_create should return cronSpec")
    if result.get("cronCreate") not in (None, {}):
        raise AssertionError("campaign_create should not auto-create cron unless createCron is explicitly enabled")
    print("PASS campaign_create_handler_checks")
    pprint({
        "campaignId": result.get("campaignId"),
        "briefPath": result.get("briefPath"),
        "status": result.get("status"),
        "cronSchedule": (result.get("cronSpec") or {}).get("schedule"),
    })
    print()


def run_send_target_contract_checks() -> None:
    creator_ids = _extract_send_target_creator_ids(
        [
            {"bloggerId": "a", "subject": "A"},
            {"besId": "b", "subject": "B"},
            {"bEsId": "b", "subject": "B-dup"},
            {"id": "c", "subject": "C"},
            {"subject": "missing id"},
        ]
    )
    if creator_ids != ["a", "b", "c"]:
        raise AssertionError(f"send target ids should keep unique explicit ids, got {creator_ids}")

    print("PASS send_target_contract_checks")
    pprint({"sendTargetCreatorIds": creator_ids})
    print()


def run_generate_email_contract_checks() -> None:
    runner = TaskRunner(token=None)
    result = runner._generate_email(
        {
            "modelAnalysis": {
                "product": {"productName": "Portable Juicer"},
                "marketing": {},
                "constraints": {},
            },
            "hostDrafts": [
                {
                    "bloggerId": "a",
                    "subject": "Hello A",
                    "plainTextBody": "Hi A",
                },
                {
                    "bloggerId": "b",
                    "subject": "Hello B",
                    "plainTextBody": "Hi B",
                },
            ],
            "sendTargetCreatorIds": ["b"],
            "emailLanguage": "en",
        },
        config={},
    )
    emails = result.get("emails") or []
    if [item.get("bloggerId") for item in emails] != ["b"]:
        raise AssertionError(f"generate_email should respect sendTargetCreatorIds, got {emails}")
    if result.get("selectedCreatorCount") != 1:
        raise AssertionError(f"selectedCreatorCount should be 1, got {result.get('selectedCreatorCount')}")

    print("PASS generate_email_contract_checks")
    pprint(result)
    print()


def run_brief_drafts_canonical_checks() -> None:
    brief = normalize_campaign_brief(
        {
            "input": "portable blender",
            "productName": "Portable Blender",
            "outreach": {
                "hostDrafts": [{"bloggerId": "a", "subject": "A"}],
            },
        }
    )
    if (brief.get("email_model_drafts") or [{}])[0].get("bloggerId") != "a":
        raise AssertionError("outreach.hostDrafts should normalize into email_model_drafts")

    brief2 = normalize_campaign_brief(
        {
            "input": "portable blender",
            "productName": "Portable Blender",
            "hostEmailDrafts": [{"bloggerId": "b", "subject": "B"}],
        }
    )
    if (brief2.get("email_model_drafts") or [{}])[0].get("bloggerId") != "b":
        raise AssertionError("compat alias hostEmailDrafts should normalize into canonical email_model_drafts")

    print("PASS brief_drafts_canonical_checks")
    pprint({
        "brief1_email_model_drafts": brief.get("email_model_drafts"),
        "brief2_email_model_drafts": brief2.get("email_model_drafts"),
    })
    print()


def run_context_drafts_canonical_checks() -> None:
    ctx = normalize_context(
        {
            "intent": {"primaryTask": "generate_email"},
            "resolvedArtifacts": {
                "hostDrafts": [{"bloggerId": "a", "subject": "A"}],
            },
        }
    )
    payload = to_generate_email_input(ctx)
    if (payload.get("hostDrafts") or [{}])[0].get("bloggerId") != "a":
        raise AssertionError("context resolvedArtifacts.hostDrafts should map into generate_email hostDrafts")

    compat_ctx = normalize_context(
        {
            "intent": {"primaryTask": "generate_email"},
            "resolvedArtifacts": {
                "hostEmailDrafts": [{"bloggerId": "b", "subject": "B"}],
            },
        }
    )
    compat_payload = to_generate_email_input(compat_ctx)
    if (compat_payload.get("hostDrafts") or [{}])[0].get("bloggerId") != "b":
        raise AssertionError("context resolvedArtifacts.hostEmailDrafts should normalize into canonical hostDrafts")

    print("PASS context_drafts_canonical_checks")
    pprint(
        {
            "canonical_hostDrafts": payload.get("hostDrafts"),
            "compat_hostDrafts": compat_payload.get("hostDrafts"),
        }
    )
    print()


def run_selection_semantics_checks() -> None:
    all_results_ctx = understand_input("把这次搜索结果全发开发信", explicit_task="generate_email")
    all_results = (all_results_ctx.get("resolvedArtifacts") or {})
    if not all_results.get("allSearchResultsSelected"):
        raise AssertionError("allSearchResultsSelected should be true for 全发语义")
    if (all_results.get("selectionRule") or {}).get("type") != "all_search_results":
        raise AssertionError(f"unexpected selectionRule for 全发语义: {all_results.get('selectionRule')}")

    top_n_ctx = understand_input("每周给前 20 个达人发开发信", explicit_task="generate_email")
    top_n = (top_n_ctx.get("resolvedArtifacts") or {}).get("selectionRule") or {}
    if top_n.get("type") != "top_n":
        raise AssertionError(f"selectionRule.type should be top_n, got {top_n}")
    if top_n.get("topN") != 20:
        raise AssertionError(f"selectionRule.topN should be 20, got {top_n}")

    scheduled_rule_ctx = understand_input(
        "每周给美国 TikTok 有邮箱的 10k 以上达人里按粉丝数从高到低取前20个发开发信",
        explicit_task="generate_email",
    )
    scheduled_rule = (scheduled_rule_ctx.get("resolvedArtifacts") or {}).get("selectionRule") or {}
    if scheduled_rule.get("type") != "top_n":
        raise AssertionError(f"scheduled selectionRule.type should be top_n, got {scheduled_rule}")
    if scheduled_rule.get("topN") != 20:
        raise AssertionError(f"scheduled selectionRule.topN should be 20, got {scheduled_rule}")
    if ((scheduled_rule.get("filters") or {}).get("minFollowers")) != 10000:
        raise AssertionError(f"scheduled selectionRule.filters.minFollowers should be 10000, got {scheduled_rule}")
    if ((scheduled_rule.get("filters") or {}).get("hasEmail")) is not True:
        raise AssertionError(f"scheduled selectionRule.filters.hasEmail should be true, got {scheduled_rule}")
    sort_rule = (scheduled_rule.get("sort") or [{}])[0]
    if sort_rule.get("field") != "followers" or sort_rule.get("order") != "desc":
        raise AssertionError(f"scheduled selectionRule.sort should be followers desc, got {scheduled_rule}")

    normalized_brief = normalize_campaign_brief(
        {
            "productName": "便携榨汁杯",
            "platform": "tiktok",
            "selectionRule": {"type": "top_n", "topN": 20},
            "allSearchResultsSelected": False,
        }
    )
    normalized_rule = normalized_brief.get("selection_rule") or {}
    if normalized_rule.get("type") != "top_n":
        raise AssertionError(f"normalized selection_rule.type should be top_n, got {normalized_rule}")
    if normalized_rule.get("top_n") != 20:
        raise AssertionError(f"normalized selection_rule.top_n should be 20, got {normalized_rule}")

    print("PASS selection_semantics_checks")
    pprint(
        {
            "all_search_results": all_results_ctx.get("resolvedArtifacts"),
            "top_n": top_n_ctx.get("resolvedArtifacts"),
            "scheduled_rule": scheduled_rule,
            "normalized_brief_selection_rule": normalized_rule,
        }
    )
    print()


def run_draft_generation_contract_checks() -> None:
    draft_input = build_draft_generation_input(
        campaign_id="portable-juicer-us",
        brief={
            "productName": "Portable Juicer",
            "brandName": "JuiceGo",
            "platform": "tiktok",
            "target_market": "us",
            "sender_name": "Lisen",
            "offer_type": "sample",
            "language": "en",
            "draftPolicy": {"mode": "host_model_per_cycle"},
            "selectionRule": {"type": "top_n", "topN": 20},
        },
        selected_creators=[
            {"bloggerId": "a", "nickname": "A", "fansNum": 50000, "country": "us"},
            {"bloggerId": "b", "nickname": "B", "fansNum": 80000, "country": "us"},
        ],
        cycle_no=3,
    )
    if draft_input.get("campaignId") != "portable-juicer-us":
        raise AssertionError(f"unexpected campaignId in draftGenerationInput: {draft_input}")
    if draft_input.get("task") != "generate_host_drafts_for_selected_creators":
        raise AssertionError(f"unexpected draft generation task: {draft_input}")
    if len(draft_input.get("selectedCreators") or []) != 2:
        raise AssertionError(f"selectedCreators should contain 2 items, got {draft_input}")
    if (draft_input.get("outputContract") or {}).get("field") != "host_drafts_per_cycle":
        raise AssertionError(f"unexpected outputContract in draftGenerationInput: {draft_input}")

    runner = CampaignRunner()
    host_request = runner._build_host_draft_generation_request(
        draft_input=draft_input,
        brief={
            "productName": "Portable Juicer",
            "brandName": "JuiceGo",
            "sender_name": "Lisen",
            "offer_type": "sample",
            "language": "en",
        },
        config={},
    )
    if host_request.get("task") != "generate_host_drafts_for_selected_creators":
        raise AssertionError(f"unexpected host draft request task: {host_request}")
    runtime_hints = host_request.get("runtimeHints") or {}
    if runtime_hints.get("runnerAutoGenerationAllowed") is not False:
        raise AssertionError(f"runner should not auto-generate drafts anymore: {host_request}")
    if runtime_hints.get("perCreatorModelGeneration") is not True:
        raise AssertionError(f"host request should require per-creator model generation: {host_request}")
    if (host_request.get("deliveryContract") or {}).get("field") != "host_drafts_per_cycle":
        raise AssertionError(f"unexpected deliveryContract in host request: {host_request}")

    injected_drafts = [
        {"bloggerId": "a", "subject": "A subject", "htmlBody": "<p>Hello A</p>", "plainTextBody": "Hello A"},
        {"bloggerId": "b", "subject": "B subject", "htmlBody": "<p>Hello B</p>", "plainTextBody": "Hello B"},
    ]
    bridge_payload = runner.build_host_model_bridge_payload(request=host_request)
    if bridge_payload.get("generationPlan", {}).get("perCreatorModelGeneration") is not True:
        raise AssertionError(f"bridge payload should require per-creator model generation: {bridge_payload}")
    if bridge_payload.get("writeBack", {}).get("field") != "host_drafts_per_cycle":
        raise AssertionError(f"bridge payload writeBack field mismatch: {bridge_payload}")
    if len(bridge_payload.get("selectedCreators") or []) != 2:
        raise AssertionError(f"bridge payload should carry selected creators: {bridge_payload}")
    if not bridge_payload.get("promptText") or not bridge_payload.get("schemaText"):
        raise AssertionError(f"bridge payload should inline prompt/schema text: {bridge_payload}")

    executor_example = runner.build_host_model_executor_example(bridge_payload=bridge_payload)
    if len(executor_example.get("messageSamples") or []) != 2:
        raise AssertionError(f"executor example should include one sample per creator in this test: {executor_example}")
    first_messages = ((executor_example.get("messageSamples") or [])[0] or {}).get("messages") or []
    if len(first_messages) < 3:
        raise AssertionError(f"executor example should build model messages: {executor_example}")

    resolved_drafts = runner._resolve_host_drafts(
        draft_input=draft_input,
        brief={"productName": "Portable Juicer"},
        config={"host_drafts_per_cycle": injected_drafts},
    )
    if len(resolved_drafts) != 2:
        raise AssertionError(f"injected host drafts should be returned as-is, got {resolved_drafts}")

    print("PASS draft_generation_contract_checks")
    pprint({"draftGenerationInput": draft_input, "hostDraftGenerationRequest": host_request, "hostModelBridgePayload": bridge_payload, "hostModelExecutorExample": executor_example, "resolvedDrafts": resolved_drafts})
    print()


def run_pre_send_consistency_audit_checks() -> None:
    creator_profile = {
        "bloggerId": "creator-1",
        "nickname": "Alice",
        "platform": "youtube",
        "country": "us",
        "language": "en",
        "tagList": ["tech", "gadgets"],
        "category": "tech",
    }
    ok_audit = audit_email_against_creator_profile(
        {
            "bloggerId": "creator-1",
            "nickname": "Alice",
            "subject": "Collab idea: JuiceGo x Alice",
            "plainTextBody": "Hi Alice,\n\nI think your YouTube audience in the US would be a strong fit for this tech launch.",
        },
        creator_profile=creator_profile,
        expected_language="en",
    )
    if not ok_audit.get("ok"):
        raise AssertionError(f"expected matching draft/profile to pass audit: {ok_audit}")

    bad_batch = build_batch_payload(
        {
            "emails": [
                {
                    "bloggerId": "creator-1",
                    "nickname": "Alice",
                    "subject": "Collab idea: JuiceGo x Alice",
                    "plainTextBody": "Hi Alice,\n\nI think your TikTok audience in Japan would love this beauty drop.",
                    "draftSource": "host-model",
                }
            ]
        },
        expected_language="en",
        creator_profiles_by_id={"creator-1": creator_profile},
    )
    blocked = bad_batch.get("blocked") or []
    if len(blocked) != 1:
        raise AssertionError(f"expected mismatched draft to be blocked, got {bad_batch}")
    audit_errors = set((blocked[0].get("auditErrors") or []))
    if "platform_profile_conflict" not in audit_errors or "audience_country_profile_conflict" not in audit_errors:
        raise AssertionError(f"expected platform/country conflicts, got {blocked}")

    print("PASS pre_send_consistency_audit_checks")
    pprint({"okAudit": ok_audit, "blockedAudit": blocked[0]})
    print()



def run_host_bridge_executor_autorun_checks() -> None:
    runner = CampaignRunner()
    draft_input = {
        "campaignId": "autorun-campaign",
        "cycleNo": 3,
        "selectedCreators": [
            {"bloggerId": "a1", "nickname": "Alice"},
            {"bloggerId": "b2", "nickname": "Bob"},
        ],
        "outreachPolicy": {"emailLanguage": "en"},
        "outputContract": {"field": "host_drafts_per_cycle"},
    }
    with tempfile.TemporaryDirectory(prefix="wotohub-bridge-test-") as tmp:
        tmp_path = Path(tmp)
        executor_path = tmp_path / "executor.py"
        executor_path.write_text(
            """
import json
import sys
from pathlib import Path

args = sys.argv[1:]
input_path = Path(args[args.index('--input') + 1])
output_path = Path(args[args.index('--output') + 1])
payload = json.loads(input_path.read_text(encoding='utf-8'))
drafts = []
for creator in payload.get('selectedCreators') or []:
    drafts.append({
        'bloggerId': creator.get('bloggerId'),
        'nickname': creator.get('nickname'),
        'subject': f"Hello {creator.get('nickname')}",
        'plainTextBody': f"Hi {creator.get('nickname')}, let's collaborate.",
        'htmlBody': f"<p>Hi {creator.get('nickname')}, let's collaborate.</p>",
    })
output_path.write_text(json.dumps({'host_drafts_per_cycle': drafts}, ensure_ascii=False), encoding='utf-8')
""".strip(),
            encoding="utf-8",
        )
        resolution = runner._resolve_host_drafts_with_meta(
            draft_input=draft_input,
            brief={
                "product_name": "Portable Juicer",
                "scheduler": {
                    "hostBridgeExecutor": {
                        "args": ["python3", str(executor_path), "--input", "{input}", "--output", "{output}"],
                        "timeoutSeconds": 30,
                    }
                },
            },
            config={},
        )
        drafts = resolution.get("drafts") or []
    if resolution.get("status") != "resolved_from_executor":
        raise AssertionError(f"executor bridge should resolve drafts, got {resolution}")
    if len(drafts) != 2:
        raise AssertionError(f"executor bridge should return 2 drafts, got {resolution}")
    if drafts[0].get("subject") != "Hello Alice":
        raise AssertionError(f"unexpected executor-generated draft content: {drafts}")

    print("PASS host_bridge_executor_autorun_checks")
    pprint({"resolution": resolution})
    print()


if __name__ == "__main__":
    for case in CASES:
        run_case(case)
    run_mapping_checks()
    run_observation_checks()
    run_host_model_injection_checks()
    run_host_resolution_observation_checks()
    run_brief_drafts_canonical_checks()
    run_context_drafts_canonical_checks()
    run_selection_semantics_checks()
    run_execution_selection_rule_checks()
    run_campaign_create_handler_checks()
    run_send_target_contract_checks()
    run_draft_generation_contract_checks()
    run_host_bridge_executor_autorun_checks()
    run_generate_email_contract_checks()
    run_pre_send_consistency_audit_checks()
    print("ALL CHECKS PASSED")

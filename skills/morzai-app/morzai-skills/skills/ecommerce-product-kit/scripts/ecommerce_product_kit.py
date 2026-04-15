#!/usr/bin/env python3
"""
Morzai ecommerce product-kit runner backed by a single FAL-style endpoint.

Environment variables:
- FAL_API_KEY: required API key for the Morzai FAL backend
- FAL_API_URL: required single-endpoint URL for submit requests
- FAL_AUTH_SCHEME: optional Authorization scheme, defaults to "Key"
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import re
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from security_logging import (
    format_curl_command,
    format_json_log,
    request_log_enabled as shared_request_log_enabled,
    sanitize_json_payload,
)
from local_image_guard import describe_local_image

PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT_SUBDIR = "morzai-ecommerce-product-kit"
DEFAULT_FAL_API_URL = "https://queue.fal.run/fal-ai/nano-banana-2"
CACHE_DIR = pathlib.Path.home() / ".morzai" / "fal_ecommerce_cache"
DEFAULT_FAL_AUTH_SCHEME = "Key"

STYLE_ROLE_PROMPT = (
    "You are an ecommerce visual director who creates commercially strong, reusable image-style directions for product listings. "
    "Your job is to propose style systems that improve conversion, preserve product realism, and stay aligned with platform constraints."
)

STYLE_OUTPUT_SCHEMA_PROMPT = (
    "Return a pure JSON array in English with exactly 4 distinct style options. Each object must contain: "
    'name, reasoning, subjectDescription, backgroundContext, lightingAndMood, photographyStyle, colorPalette, colorDescription.\n\n'
    "Schema requirements:\n"
    "- name: 2-4 words, simple and commercially clear\n"
    "- reasoning: short plain-English reason, <= 15 words\n"
    "- subjectDescription: 15-25 words describing the product and model (focus on texture, drape, fit, and professional pose)\n"
    "- backgroundContext: 10-20 words describing the environment and setting (studio, urban, minimalist, or brand-specific context)\n"
    "- lightingAndMood: 10-20 words describing the lighting quality and atmosphere (e.g., soft diffused studio light, high-key, cinematic shadow)\n"
    "- photographyStyle: 10-15 words describing camera/lens and aesthetic (e.g., 85mm portrait, shallow depth of field, high-end commercial fashion style)\n"
    "- colorPalette: exactly 3 hex colors: [Product color, Background color, Accent color]\n"
    "- colorDescription: explain the color roles in English\n\n"
    "Hard rules:\n"
    "1. Use realistic commercial photography only (no illustrations or paintings).\n"
    "2. Maintain product color accuracy.\n"
    "3. Do not output any text outside the JSON array."
)

STYLE_SELF_CHECK_PROMPT = (
    "Before finalizing, verify: the 4 options are visually distinct; each option uses Google's structured prompt layers "
    "(Subject, Context, Lighting, Technique); and the palette starts with the product's inherent color."
)

MARKET_LABELS = {
    "US": "United States",
    "CN": "China",
    "UK": "United Kingdom",
    "JP": "Japan",
    "DE": "Germany",
    "FR": "France",
    "AU": "Australia",
    "CA": "Canada",
    "SG": "Singapore",
}

LISTING_SET_TEMPLATES = {
    "P1": {
        "role": "Hero Image",
        "description": "Center-focused [SUBJECT] on a pure white background, ghost mannequin or professional studio style, crisp textures, Amazon compliant.",
        "template": "{subjectDescription} on a pure white background, crisp textures, balanced studio lighting, eye-level hero shot, high-end commercial quality."
    },
    "P2": {
        "role": "Core Benefits",
        "description": "Close-up highlighting key features and material quality, building trust.",
        "template": "Focus on {subjectDescription} showing fine details and premium quality, soft directional studio lighting, clean background."
    },
    "P3": {
        "role": "Core Benefits (Alternate)",
        "description": "Secondary benefit shot focusing on functionality or design fit.",
        "template": "Showcase {subjectDescription} from an angle, highlighting fit and design, professional ecommerce lighting."
    },
    "P4": {
        "role": "Detail Hero",
        "description": "Macro texture and craftsmanship close-up.",
        "template": "Extreme macro close-up of {subjectDescription}, focus on fabric weave and stitching, shallow depth of field, high-end sensory detail."
    },
    "P5": {
        "role": "Multi-view",
        "description": "Side or back view to provide full context.",
        "template": "Side profile view of {subjectDescription}, professional fashion photography, consistent lighting with hero image."
    },
    "P6": {
        "role": "Lifestyle",
        "description": "Aspirational context to create desire.",
        "template": "{subjectDescription} in a {backgroundContext}, with {lightingAndMood}, {photographyStyle}, realistic lifestyle atmosphere."
    },
    "P7": {
        "role": "Decision-making",
        "description": "Informative flat-lay or packaging shot.",
        "template": "Flat-lay shot of {subjectDescription} on a neutral surface, even top-down lighting, clear and informative composition."
    }
}


def _json_error(
    ok: bool,
    error_type: str,
    message: str,
    user_hint: str,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    out: Dict[str, Any] = {
        "ok": ok,
        "error_type": error_type,
        "message": message,
        "user_hint": user_hint,
    }
    if extra:
        out.update(extra)
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(1 if not ok else 0)


def _clean_reference_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    cleaned: List[str] = []
    for line in lines:
        if not line:
            continue
        line = re.sub(r"^#{1,6}\s*", "", line)
        line = re.sub(r"^[-*]\s*", "- ", line)
        line = re.sub(r"\|", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned.append(line)
    return "\n".join(cleaned)


def _reference_text(name: str, max_chars: int) -> str:
    path = PROJECT_ROOT / "references" / name
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    cleaned = _clean_reference_text(raw)
    if len(cleaned) > max_chars:
        cleaned = cleaned[: max_chars - 3].rstrip() + "..."
    return cleaned


def _style_reference_blocks() -> str:
    return ""


PLATFORM_REFERENCE_TEXT = _reference_text("platform-best-practices.md", 4000)
LISTING_SET_REFERENCE_TEXT = _reference_text("listing-set-logic.md", 3000)
APPAREL_REFERENCE_TEXT = _reference_text("apparel-visual-specs.md", 3000)
OUTPUT_SPEC_REFERENCE_TEXT = _reference_text("output-spec.md", 4000)


def _normalized_output_type(output_type: str) -> str:
    value = (output_type or "listing-image").strip().lower().replace("_", "-")
    aliases = {
        "hero": "hero-image",
        "hero-image": "hero-image",
        "listing-image": "hero-image",
        "main-image": "hero-image",
        "detail": "detail-image",
        "detail-image": "detail-image",
        "lifestyle": "lifestyle-image",
        "lifestyle-image": "lifestyle-image",
        "decision": "decision-image",
        "decision-image": "decision-image",
        "marketing": "marketing-poster",
        "marketing-poster": "marketing-poster",
        "infographic": "marketing-poster",
        "try-on": "try-on",
        "virtual-try-on": "try-on",
        "apparel-visual": "try-on",
        "listing-set": "listing-set",
    }
    return aliases.get(value, value or "hero-image")


def _clean_fragment_list(*groups: Any) -> List[str]:
    results: List[str] = []
    for group in groups:
        if group is None:
            continue
        if isinstance(group, str):
            items = [group]
        else:
            try:
                items = list(group)
            except TypeError:
                items = [str(group)]
        for item in items:
            text = re.sub(r"\s+", " ", str(item or "")).strip(" ,.;")
            if text and text not in results:
                results.append(text)
    return results


def _sentence_case(text: str) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return ""
    return text[0].upper() + text[1:]


def _join_sentence(fragments: List[str]) -> str:
    cleaned = _clean_fragment_list(fragments)
    if not cleaned:
        return ""
    return _sentence_case(", ".join(cleaned)) + "."


def _build_fragment_groups(
    subject_fragments: Optional[List[str]] = None,
    context_fragments: Optional[List[str]] = None,
    composition_fragments: Optional[List[str]] = None,
    lighting_fragments: Optional[List[str]] = None,
    style_fragments: Optional[List[str]] = None,
    constraint_fragments: Optional[List[str]] = None,
    negative_fragments: Optional[List[str]] = None,
) -> Dict[str, List[str]]:
    return {
        "subject_fragments": _clean_fragment_list(subject_fragments or []),
        "context_fragments": _clean_fragment_list(context_fragments or []),
        "composition_fragments": _clean_fragment_list(composition_fragments or []),
        "lighting_fragments": _clean_fragment_list(lighting_fragments or []),
        "style_fragments": _clean_fragment_list(style_fragments or []),
        "constraint_fragments": _clean_fragment_list(constraint_fragments or []),
        "negative_fragments": _clean_fragment_list(negative_fragments or []),
    }


def _merge_fragment_groups(*groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
    merged = _build_fragment_groups()
    for group in groups:
        for key in merged.keys():
            merged[key] = _clean_fragment_list(merged[key], (group or {}).get(key, []))
    return merged


def _is_apparel_product(product_info: str, output_type: str) -> bool:
    text = f"{product_info} {_normalized_output_type(output_type)}".lower()
    keywords = (
        "apparel", "wear", "shirt", "t-shirt", "tee", "hoodie", "sweater", "jacket", "coat",
        "dress", "skirt", "pants", "trousers", "jeans", "leggings", "shorts", "blazer",
        "suit", "vest", "cardigan", "top", "bra", "underwear", "sock", "shoe", "sneaker",
        "boot", "sandal", "fashion", "garment", "fit", "drape", "silhouette"
    )
    return any(keyword in text for keyword in keywords)


def _derive_platform_fragments(platform: str, output_type: str, aspect_ratio: str) -> Dict[str, List[str]]:
    platform_key = (platform or "amazon").strip().lower()
    normalized_output = _normalized_output_type(output_type)
    ratio = (aspect_ratio or "1:1").strip() or "1:1"

    subject: List[str] = []
    context: List[str] = []
    composition: List[str] = []
    lighting: List[str] = []
    style: List[str] = []
    constraints: List[str] = []
    negatives: List[str] = []

    if platform_key == "amazon":
        composition.extend([f"{ratio} framing", "product-only composition" if normalized_output in {"hero-image", "listing-set"} else "conversion-oriented framing"])
        context.append("pure white background" if normalized_output in {"hero-image", "listing-set"} else "clean low-distraction background")
        lighting.extend(["balanced studio lighting", "clear edge separation"])
        style.append("high-realism commercial ecommerce photography")
        constraints.extend(["no text or logos", "no watermarks", "no packaging", "keep the product immediately legible"])
    elif platform_key == "instagram":
        composition.extend(["4:5 portrait framing", "social-first crop with strong focal point"])
        context.append("believable lifestyle environment")
        lighting.extend(["soft directional light", "contact shadows"])
        style.extend(["aesthetic commercial photography", "polished but natural social mood"])
        constraints.extend(["keep the product readable inside the scene", "avoid flat cutout look"])
    elif platform_key == "pinterest":
        composition.extend(["2:3 vertical framing", "story-driven vertical composition"])
        context.append("editorial or informational scene that supports discovery")
        lighting.append("soft natural or studio-balanced light")
        style.extend(["aspirational editorial commerce style", "save-worthy storytelling image"])
        constraints.extend(["do not use square composition", "allow space for readable decision support if needed"])
    elif platform_key in {"shopify", "dtc", "shopify / dtc"}:
        composition.extend([f"{ratio} framing", "editorial storefront composition"])
        context.append("brand-aligned premium environment")
        lighting.append("refined commercial lighting")
        style.extend(["editorial product storytelling", "high-trust brand-heavy presentation"])
        constraints.append("balance conversion clarity with brand presence")
    elif platform_key == "temu":
        composition.extend(["3:4 portrait framing" if ratio == "1:1" else f"{ratio} framing", "high-clarity ecommerce crop"])
        context.append("clean high-contrast background")
        lighting.append("bright commercial lighting")
        style.append("value-forward ecommerce presentation")
        constraints.extend(["prioritize immediate feature clarity", "keep benefit readout visually obvious"])
    elif platform_key == "shein":
        composition.extend(["3:4 portrait framing" if ratio == "1:1" else f"{ratio} framing", "fast-fashion ecommerce composition"])
        context.append("clean grey or beige studio background")
        lighting.append("high-key lighting")
        style.append("trend-aware fast-fashion presentation")
        constraints.append("keep white balance consistent across the set")
    else:
        if normalized_output in {"hero-image", "listing-set"}:
            context.append("pure white or very clean background")
            composition.extend([f"{ratio} framing", "product-first hero composition"])
            style.append("marketplace-ready ecommerce photography")
            constraints.extend(["follow Amazon-like hero compliance", "avoid text overlays"])
        else:
            context.append("clean editorial background")
            composition.extend([f"{ratio} framing", "secondary-image composition"])
            style.append("Shopify-like editorial commerce style")
            constraints.append("keep the product readable and conversion-friendly")

    constraints.append("target 2048px output on the longest side")
    negatives.extend(["irrelevant decorative props", "unnecessary clutter"])
    if "platform comparison matrix" in PLATFORM_REFERENCE_TEXT.lower():
        constraints = _clean_fragment_list(constraints)
    return _build_fragment_groups(subject, context, composition, lighting, style, constraints, negatives)


def _derive_market_fragments(market: str) -> Dict[str, List[str]]:
    market_key = (market or "US").strip().upper()
    western_markets = {"US", "EU", "UK", "DE", "FR", "JP", "CA", "AU"}
    growth_markets = {"CN", "SEA", "SG", "MY", "TH", "VN", "ID", "PH"}
    if market_key in western_markets:
        return _build_fragment_groups(
            style_fragments=["subtle authentic commercial tone"],
            context_fragments=["non-distracting environment"],
            constraint_fragments=["preserve natural realism"],
        )
    if market_key in growth_markets:
        return _build_fragment_groups(
            style_fragments=["high-brightness value-forward tone"],
            composition_fragments=["strong feature visibility"],
            constraint_fragments=["emphasize immediate utility"],
        )
    return _build_fragment_groups(
        style_fragments=["globally legible ecommerce tone"],
        constraint_fragments=["balance trust, clarity, and conversion"],
    )


def _derive_apparel_fragments(product_info: str, output_type: str) -> Dict[str, List[str]]:
    if not _is_apparel_product(product_info, output_type):
        return _build_fragment_groups()

    normalized_output = _normalized_output_type(output_type)
    subject = ["accurate garment color", "credible fabric texture", "believable drape and fold behavior"]
    lighting = ["controlled side light or balanced diffused studio light"]
    style = ["realistic commercial apparel photography"]
    constraints = [
        "preserve fabric character and surface detail",
        "keep edges clean and natural",
        "avoid overdesigned effects that weaken trust",
    ]
    negatives = [
        "plastic-looking fabric",
        "oversmoothed surface",
        "stretched or broken texture detail",
        "jagged edges",
        "white fringe",
        "halo shadows",
        "extreme color cast",
    ]
    if normalized_output == "try-on":
        subject.extend(["believable body proportions", "clear silhouette and fit behavior"])
        composition = ["show fit and drape clearly on body"]
    else:
        composition = ["keep garment structure readable"]
    if "anti-patterns" in APPAREL_REFERENCE_TEXT.lower():
        negatives = _clean_fragment_list(negatives)
    return _build_fragment_groups(subject, [], composition, lighting, style, constraints, negatives)


def _derive_output_type_fragments(output_type: str) -> Dict[str, List[str]]:
    normalized_output = _normalized_output_type(output_type)
    reference_flags = _reference_context_flags()
    if normalized_output == "hero-image":
        constraints = ["prioritize recognition over explanation"]
        if reference_flags["output_has_boundary"]:
            constraints.append("do not turn the hero into a dense explainer")
        return _build_fragment_groups(
            subject_fragments=["immediately legible product hero"],
            context_fragments=["simple low-distraction background"],
            composition_fragments=["stable product-first composition"],
            constraint_fragments=constraints,
        )
    if normalized_output == "detail-image":
        return _build_fragment_groups(
            subject_fragments=["materials, structure, or benefit details"],
            composition_fragments=["close-up or crop-in framing"],
            style_fragments=["trust-building explanatory image"],
            constraint_fragments=["emphasize craftsmanship and functional clarity"],
        )
    if normalized_output == "lifestyle-image":
        return _build_fragment_groups(
            context_fragments=["believable aspirational use context"],
            lighting_fragments=["atmospheric but readable light"],
            style_fragments=["emotionally resonant brand atmosphere"],
            constraint_fragments=["keep the product readable inside the scene"],
        )
    if normalized_output == "decision-image":
        constraints = ["prioritize readability over spectacle"]
        if reference_flags["output_has_boundary"]:
            constraints.append("support the purchase decision by reducing uncertainty")
        return _build_fragment_groups(
            composition_fragments=["clear information hierarchy"],
            style_fragments=["decision-support visual layout"],
            constraint_fragments=constraints,
        )
    if normalized_output == "marketing-poster":
        return _build_fragment_groups(
            composition_fragments=["campaign-ready communication layout"],
            style_fragments=["graphic-forward promotional energy"],
            constraint_fragments=["allow stronger communication hierarchy without losing product focus"],
        )
    if normalized_output == "try-on":
        return _build_fragment_groups(
            subject_fragments=["fit-confidence apparel presentation"],
            composition_fragments=["show silhouette, fit, and drape clearly"],
            style_fragments=["fashion-forward but trustworthy on-body image"],
            constraint_fragments=["do not hide the garment with props or extreme poses"],
        )
    if normalized_output == "listing-set":
        constraints = ["separate slot roles from attention to trust to conversion"]
        if reference_flags["output_has_boundary"]:
            constraints.append("keep one consistent visual system across the full set")
        return _build_fragment_groups(
            style_fragments=["consistent visual system across the full set"],
            constraint_fragments=constraints,
        )
    return _build_fragment_groups()


def _derive_listing_slot_fragments(slot_id: str, platform: str) -> Dict[str, List[str]]:
    slot = (slot_id or "").strip().upper()
    platform_key = (platform or "amazon").strip().lower()
    reference_flags = _reference_context_flags()
    if slot == "P1":
        constraints = ["optimize for first-click clarity"]
        if platform_key == "amazon":
            constraints.extend(["strict first-image compliance", "pure white background only"])
        return _build_fragment_groups(
            subject_fragments=["hero product presentation"],
            composition_fragments=["centered or dominant hero framing"],
            constraint_fragments=constraints,
        )
    if slot in {"P2", "P3"}:
        return _build_fragment_groups(
            subject_fragments=["core benefits and trust signals"],
            composition_fragments=["benefit-led explanatory crop"],
            constraint_fragments=["make the value proposition visually obvious"],
        )
    if slot == "P4":
        return _build_fragment_groups(
            subject_fragments=["macro craftsmanship detail"],
            composition_fragments=["tight macro close-up"],
            constraint_fragments=["highlight material and build quality"],
        )
    if slot == "P5":
        return _build_fragment_groups(
            subject_fragments=["multi-view coverage"],
            composition_fragments=["side, back, or alternate-angle view"],
            constraint_fragments=["improve spatial understanding of the product"],
        )
    if slot == "P6":
        return _build_fragment_groups(
            context_fragments=["believable real-life context"],
            style_fragments=["desire-building lifestyle image"],
            constraint_fragments=["keep the scene credible and commercially useful"],
        )
    if slot == "P7":
        constraints = ["support the final buying decision with clarity"]
        if reference_flags["listing_has_p7"]:
            constraints.append("reduce hesitation before purchase")
        return _build_fragment_groups(
            composition_fragments=["readable decision-support layout"],
            style_fragments=["reassuring purchase-completion image"],
            constraint_fragments=constraints,
        )
    return _build_fragment_groups()


def _vertex_prompt_sections(fragment_groups: Dict[str, List[str]]) -> List[str]:
    return [
        _join_sentence(fragment_groups.get("subject_fragments", [])),
        _join_sentence(fragment_groups.get("context_fragments", [])),
        _join_sentence(fragment_groups.get("composition_fragments", [])),
        _join_sentence(fragment_groups.get("lighting_fragments", [])),
        _join_sentence(fragment_groups.get("style_fragments", [])),
        _join_sentence(fragment_groups.get("constraint_fragments", [])),
        _join_sentence([f"avoid {item}" for item in fragment_groups.get("negative_fragments", [])]),
    ]


def _compose_vertex_style_prompt(
    product_info: str,
    platform: str,
    market: str,
    market_label: str,
    output_type: str,
    aspect_ratio: str,
) -> str:
    fragments = _merge_fragment_groups(
        _build_fragment_groups(subject_fragments=[product_info]),
        _derive_platform_fragments(platform, output_type, aspect_ratio),
        _derive_market_fragments(market),
        _derive_apparel_fragments(product_info, output_type),
        _derive_output_type_fragments(output_type),
    )
    sections = [
        STYLE_ROLE_PROMPT,
        "[Input]\n"
        f"- Product: {product_info}\n"
        f"- Platform: {platform}\n"
        f"- Target market: {market} ({market_label})\n"
        f"- Output type: {_normalized_output_type(output_type)}\n"
        f"- Aspect ratio: {aspect_ratio}",
        "[Structured design brief]\n"
        + "\n".join(
            section for section in [
                f"- Subject requirements: {_join_sentence(fragments['subject_fragments'])}",
                f"- Context / Background: {_join_sentence(fragments['context_fragments'])}",
                f"- Composition / Camera: {_join_sentence(fragments['composition_fragments'])}",
                f"- Lighting: {_join_sentence(fragments['lighting_fragments'])}",
                f"- Style / Mood: {_join_sentence(fragments['style_fragments'])}",
                f"- Quality / Realism constraints: {_join_sentence(fragments['constraint_fragments'])}",
                f"- Explicit avoid / compliance constraints: {_join_sentence([f'avoid {item}' for item in fragments['negative_fragments']])}",
            ]
            if not section.endswith(": ")
        ),
        STYLE_OUTPUT_SCHEMA_PROMPT,
        STYLE_SELF_CHECK_PROMPT,
    ]
    return "\n\n".join(section for section in sections if section)


def _compose_vertex_render_prompt(
    product_info: str,
    brand_style: Optional[Dict[str, Any]],
    platform: str,
    market: str,
    output_type: str,
    aspect_ratio: str,
    slot_id: Optional[str] = None,
) -> str:
    style = brand_style or {}
    fragments = _merge_fragment_groups(
        _build_fragment_groups(
            subject_fragments=[style.get("subjectDescription") or product_info],
            context_fragments=[style.get("backgroundContext")] if style.get("backgroundContext") else [],
            lighting_fragments=[style.get("lightingAndMood")] if style.get("lightingAndMood") else [],
            style_fragments=[style.get("photographyStyle")] if style.get("photographyStyle") else [],
        ),
        _derive_platform_fragments(platform, output_type, aspect_ratio),
        _derive_market_fragments(market),
        _derive_apparel_fragments(product_info, output_type),
        _derive_output_type_fragments(output_type),
        _derive_listing_slot_fragments(slot_id or "", platform) if slot_id else _build_fragment_groups(),
    )
    return " ".join(section for section in _vertex_prompt_sections(fragments) if section)


def _build_style_prompt(
    product_info: str,
    platform: str,
    market: str,
    market_label: str,
    output_type: str,
    aspect_ratio: str,
) -> str:
    return _compose_vertex_style_prompt(
        product_info=product_info,
        platform=platform,
        market=market,
        market_label=market_label,
        output_type=output_type,
        aspect_ratio=aspect_ratio,
    )


def _request_log_enabled() -> bool:
    return shared_request_log_enabled()


def _request_log_as_curl(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[bytes] = None,
) -> None:
    if not _request_log_enabled():
        return
    print(
        "[REQUEST] " + format_curl_command(method, url, headers, data, max_time=120),
        file=sys.stderr,
    )


def _request_log_response_json(label: str, text: str, http_code: Optional[int] = None) -> None:
    if not _request_log_enabled():
        return
    try:
        max_len = int(os.environ.get("OPENCLAW_REQUEST_LOG_BODY_MAX", "20000"))
    except ValueError:
        max_len = 20000
    print(format_json_log(label, text, max_len=max_len, http_code=http_code), file=sys.stderr)


def _require_fal_api_key() -> str:
    key = os.environ.get("FAL_API_KEY", "").strip()
    if not key:
        _json_error(
            False,
            "CREDENTIALS_MISSING",
            "Missing FAL_API_KEY",
            'Run: export FAL_API_KEY="YOUR_MORZAI_FAL_KEY"',
        )
    return key


def _fal_api_url() -> str:
    url = os.environ.get("FAL_API_URL", DEFAULT_FAL_API_URL).strip() or DEFAULT_FAL_API_URL
    return url.rstrip("/")


def _fal_auth_scheme() -> str:
    return os.environ.get("FAL_AUTH_SCHEME", DEFAULT_FAL_AUTH_SCHEME).strip() or DEFAULT_FAL_AUTH_SCHEME


def _headers_json() -> Dict[str, str]:
    key = _require_fal_api_key()
    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Authorization": f"{_fal_auth_scheme()} {key}",
        "User-Agent": "Morzai-Ecommerce-Product-Kit/2.0",
    }


def _headers_get() -> Dict[str, str]:
    headers = _headers_json()
    headers.pop("Content-Type", None)
    return headers


def _reference_context_flags() -> Dict[str, bool]:
    return {
        "platform_has_matrix": "platform comparison matrix" in PLATFORM_REFERENCE_TEXT.lower(),
        "listing_has_p7": "p7" in LISTING_SET_REFERENCE_TEXT.lower(),
        "apparel_has_anti_patterns": "anti-patterns" in APPAREL_REFERENCE_TEXT.lower(),
        "output_has_boundary": "boundary" in OUTPUT_SPEC_REFERENCE_TEXT.lower(),
    }


def _http_request(
    method: str,
    url: str,
    body: Optional[bytes] = None,
    json_mode: bool = True,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Tuple[int, Any]:
    headers = _headers_json() if json_mode else _headers_get()
    if body and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    _request_log_as_curl(method, url, headers, body)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = resp.getcode() or 200
            _request_log_response_json("response_body", raw, code)
            try:
                return code, json.loads(raw)
            except json.JSONDecodeError:
                return code, {"_raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        _request_log_response_json("response_body", raw, e.code)
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"_raw": raw, "_http_message": str(e)}


def _downloads_dir() -> pathlib.Path:
    return pathlib.Path.home() / "Downloads"


def _default_visual_dir() -> pathlib.Path:
    openclaw_home = os.environ.get("OPENCLAW_HOME", "").strip()
    if openclaw_home:
        return pathlib.Path(openclaw_home).expanduser() / "workspace" / "visual"
    return pathlib.Path.home() / ".openclaw" / "workspace" / "visual"


def _looks_like_skill_internal(path: pathlib.Path) -> bool:
    try:
        path.relative_to(PROJECT_ROOT)
        return True
    except ValueError:
        return False


def resolve_output_dir(inp: Dict[str, Any]) -> pathlib.Path:
    explicit = str(inp.get("output_dir", "") or os.environ.get("MORZAI_OUTPUT_DIR", "")).strip()
    if explicit:
        output_dir = pathlib.Path(explicit).expanduser().resolve()
    else:
        cwd = pathlib.Path.cwd().resolve()
        if (cwd / "openclaw.yaml").is_file():
            output_dir = cwd / "output"
        else:
            visual_dir = _default_visual_dir()
            if visual_dir.is_dir():
                output_dir = visual_dir / "output" / DEFAULT_OUTPUT_SUBDIR
            else:
                output_dir = _downloads_dir()

    if _looks_like_skill_internal(output_dir):
        _json_error(
            False,
            "PARAM_ERROR",
            f"Output directory cannot be inside the skill directory: {output_dir}",
            "Use a project output directory, shared visual output directory, or pass another output_dir.",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _safe_filename_part(value: str, fallback: str) -> str:
    text = re.sub(r"\s+", "_", (value or "").strip())
    text = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._-")
    return text or fallback


def _guess_extension(url: str, default_ext: str = ".jpg") -> str:
    path = urllib.parse.urlparse(url).path
    ext = pathlib.Path(path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return ext
    return default_ext


def _download_to_path(url: str, target: pathlib.Path) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": _headers_get().get("User-Agent", "Mozilla/5.0"),
            "Accept": "image/*,*/*;q=0.8",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
    except Exception as exc:
        _json_error(False, "DOWNLOAD_ERROR", str(exc), f"Failed to download generated result: {url}")
    target.write_bytes(data)
    return str(target)


def _local_image_paths_from_urls(urls: List[str], output_dir: pathlib.Path, product_name: str) -> List[str]:
    saved_paths: List[str] = []
    product_part = _safe_filename_part(product_name, "product")
    for index, image_url in enumerate(urls, start=1):
        if not isinstance(image_url, str) or not image_url.startswith("http"):
            continue
        ext = _guess_extension(image_url)
        filename = f"{product_part}_{index:02d}{ext}"
        saved_paths.append(_download_to_path(image_url, output_dir / filename))
    return saved_paths


def _local_image_paths_from_items(items: List[Dict[str, Any]], output_dir: pathlib.Path, product_name: str) -> List[str]:
    saved_paths: List[str] = []
    product_part = _safe_filename_part(product_name, "product")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        image_url = str(item.get("res_img", "") or item.get("url", "") or item.get("image_url", "")).strip()
        if not image_url.startswith("http"):
            continue
        label = _safe_filename_part(str(item.get("label", "")).strip(), f"image_{index}")
        ext = _guess_extension(image_url)
        filename = f"{product_part}_{index:02d}_{label}{ext}"
        saved_paths.append(_download_to_path(image_url, output_dir / filename))

    return saved_paths


def _cache_path(job_id: str) -> pathlib.Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_id = _safe_filename_part(job_id, job_id)
    return CACHE_DIR / f"{safe_id}.json"


def _cache_write(job_id: str, payload: Dict[str, Any]) -> None:
    _cache_path(job_id).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _cache_read(job_id: str) -> Dict[str, Any]:
    path = _cache_path(job_id)
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _is_http_url(value: str) -> bool:
    return bool(re.match(r"^https?://", value or "", re.I))


def _local_image_data_uri(file_path: str) -> str:
    if not os.path.isfile(file_path):
        _json_error(False, "PARAM_ERROR", f"File does not exist: {file_path}", "Check the image path and try again.")
    try:
        _, mime = describe_local_image(file_path)
    except ValueError as exc:
        _json_error(False, "PARAM_ERROR", str(exc), "Provide a JPG, JPEG, PNG, WEBP, or GIF image file.")
    raw = pathlib.Path(file_path).read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def resolve_image_input(image: str) -> Tuple[str, str]:
    image = (image or "").strip()
    if not image:
        _json_error(False, "PARAM_ERROR", "Missing image", "Provide a product image URL or local file path.")
    if _is_http_url(image):
        return "url", image
    return "data_uri", _local_image_data_uri(image)


def _fal_submit_url() -> str:
    return _fal_api_url()


def _fal_status_candidates(meta: Dict[str, Any]) -> List[str]:
    urls: List[str] = []
    for key in ("status_url", "response_url", "poll_url", "request_url"):
        value = meta.get(key)
        if isinstance(value, str) and value.startswith("http"):
            urls.append(value)
    endpoint = _fal_api_url()
    request_id = str(meta.get("request_id", "") or meta.get("task_id", "") or meta.get("batch_id", "")).strip()
    if request_id:
        base = endpoint.rstrip("/")
        urls.extend([
            f"{base}/requests/{request_id}/status",
            f"{base}/requests/{request_id}",
        ])
    deduped: List[str] = []
    for item in urls:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _pick_request_id(resp: Any) -> Optional[str]:
    if not isinstance(resp, dict):
        return None
    for path in (
        ("request_id",),
        ("id",),
        ("task_id",),
        ("batch_id",),
        ("data", "request_id"),
        ("data", "id"),
        ("data", "task_id"),
        ("data", "batch_id"),
    ):
        cur: Any = resp
        for key in path:
            if not isinstance(cur, dict):
                cur = None
                break
            cur = cur.get(key)
        if isinstance(cur, str) and cur.strip():
            return cur.strip()
    return None


def _extract_urls(obj: Any) -> List[str]:
    urls: List[str] = []
    if isinstance(obj, str):
        if obj.startswith("http"):
            urls.append(obj)
        return urls
    if isinstance(obj, list):
        for item in obj:
            urls.extend(_extract_urls(item))
        return urls
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and value.startswith("http"):
                lowered = key.lower()
                if any(part in lowered for part in ("url", "image", "media", "file", "src")):
                    urls.append(value)
            else:
                urls.extend(_extract_urls(value))
    return list(dict.fromkeys(urls))


def _extract_text_candidates(obj: Any) -> List[str]:
    candidates: List[str] = []
    if isinstance(obj, str):
        stripped = obj.strip()
        if stripped:
            candidates.append(stripped)
        return candidates
    if isinstance(obj, list):
        for item in obj:
            candidates.extend(_extract_text_candidates(item))
        return candidates
    if isinstance(obj, dict):
        preferred_keys = (
            "text",
            "content",
            "output",
            "result",
            "message",
            "response",
            "completion",
            "generated_text",
        )
        for key in preferred_keys:
            if key in obj:
                candidates.extend(_extract_text_candidates(obj.get(key)))
        for value in obj.values():
            candidates.extend(_extract_text_candidates(value))
    deduped: List[str] = []
    for item in candidates:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _extract_styles_from_text(text: str) -> Optional[Any]:
    try:
        match = re.search(r"\[[\s\S]*\]", text)
        if match:
            return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    return None


def _terminal_state(resp: Any) -> Optional[bool]:
    if not isinstance(resp, dict):
        return None
    candidates = []
    for key in ("status", "state"):
        value = resp.get(key)
        if value is not None:
            candidates.append(value)
    data = resp.get("data")
    if isinstance(data, dict):
        for key in ("status", "state"):
            value = data.get(key)
            if value is not None:
                candidates.append(value)
    for value in candidates:
        text = str(value).strip().lower()
        if text in {"completed", "complete", "success", "succeeded", "done", "ok"}:
            return True
        if text in {"failed", "error", "cancelled", "canceled"}:
            return True
        if text in {"queued", "queue", "pending", "running", "processing", "in_progress", "in-progress"}:
            return False
    return None


def _normalize_style_poll_result(resp: Any) -> Tuple[bool, Optional[Any], Optional[str]]:
    text_candidates = _extract_text_candidates(resp)
    for text in text_candidates:
        styles = _extract_styles_from_text(text)
        if styles is not None:
            return True, styles, text
    done = _terminal_state(resp)
    if done is True and text_candidates:
        return True, None, text_candidates[0]
    return bool(done), None, text_candidates[0] if text_candidates else None


def _normalize_render_items(resp: Any) -> Tuple[List[str], List[Dict[str, Any]]]:
    urls = _extract_urls(resp)
    items = []
    for index, url in enumerate(urls, start=1):
        items.append({"label": f"image_{index}", "res_img": url})
    return urls, items


def _generate_listing_set_prompts(
    product_info: str,
    brand_style: Dict[str, Any],
    platform: str,
    market: str,
    aspect_ratio: str,
) -> List[Dict[str, str]]:
    results = []
    style = brand_style or {}

    slot_output_types = {
        "P1": "hero-image",
        "P2": "detail-image",
        "P3": "detail-image",
        "P4": "detail-image",
        "P5": "detail-image",
        "P6": "lifestyle-image",
        "P7": "decision-image",
    }

    for slot_id in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]:
        data = LISTING_SET_TEMPLATES[slot_id]
        template_text = data["template"].format(
            subjectDescription=style.get("subjectDescription") or product_info,
            backgroundContext=style.get("backgroundContext") or "minimalist studio",
            lightingAndMood=style.get("lightingAndMood") or "soft studio light",
            photographyStyle=style.get("photographyStyle") or "professional 85mm shot",
        )
        prompt = _compose_vertex_render_prompt(
            product_info=product_info,
            brand_style={
                **style,
                "subjectDescription": template_text,
            },
            platform=platform,
            market=market,
            output_type=slot_output_types[slot_id],
            aspect_ratio=aspect_ratio,
            slot_id=slot_id,
        )
        results.append({
            "slot": slot_id,
            "role": data["role"],
            "prompt": prompt,
        })
    return results


def _build_style_request(inp: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    image_kind, image_value = resolve_image_input(str(inp.get("image", "")))
    product_info = str(inp.get("product_info", inp.get("selling_points", ""))).strip() or "product"
    platform = str(inp.get("platform", "amazon")).strip()
    market = str(inp.get("market", "US")).strip()
    market_label = str(inp.get("market_label", "") or MARKET_LABELS.get(market.upper(), market.upper()))
    output_type = str(inp.get("output_type", inp.get("result_type", "hero-image")) or "hero-image").strip()
    aspect_ratio = str(inp.get("aspect_ratio", inp.get("ratio", "1:1")) or "1:1").strip() or "1:1"
    prompt = _compose_vertex_style_prompt(
        product_info=product_info,
        platform=platform,
        market=market,
        market_label=market_label,
        output_type=output_type,
        aspect_ratio=aspect_ratio,
    )
    payload = {
        "command": "style_create",
        "mode": "style",
        "input": {
            "prompt": prompt,
            "product_info": product_info,
            "platform": platform,
            "market": market,
            "market_label": market_label,
            "output_type": output_type,
            "aspect_ratio": aspect_ratio,
            "image": image_value,
            "image_mode": image_kind,
            "language": str(inp.get("language", "English")),
        },
    }
    cache_meta = {
        "command": "style_create",
        "product_info": product_info,
        "platform": platform,
        "market": market,
        "output_type": output_type,
        "aspect_ratio": aspect_ratio,
    }
    return payload, cache_meta


def _build_render_request(inp: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    transfer_id = str(inp.get("transfer_id", "") or str(uuid.uuid4()).upper())
    image_urls = inp.get("image_urls")
    if not image_urls:
        one = inp.get("image")
        if one:
            image_urls = [one]
    if not isinstance(image_urls, list) or not image_urls:
        _json_error(False, "PARAM_ERROR", "Missing image_urls", "Pass an image_urls array or a single image field.")

    resolved_images = []
    for raw in image_urls:
        image_kind, image_value = resolve_image_input(str(raw))
        resolved_images.append({"image": image_value, "image_mode": image_kind})

    brand_style = inp.get("brand_style")
    if brand_style is not None and not isinstance(brand_style, dict):
        _json_error(False, "PARAM_ERROR", "brand_style must be an object or empty", "Pass a style JSON object or omit this field.")

    style_name = str(inp.get("style_name", (brand_style or {}).get("name", "")))
    product_info = str(inp.get("product_info", "")).strip() or "product"
    aspect_ratio = str(inp.get("aspect_ratio", inp.get("ratio", "1:1")) or "1:1").strip() or "1:1"
    language = str(inp.get("language", "English"))
    platform = str(inp.get("platform", "amazon"))
    market = str(inp.get("market", "US"))
    output_type = str(inp.get("output_type", inp.get("result_type", "listing-image")) or "listing-image")
    normalized_output = _normalized_output_type(output_type)

    constructed_prompt = _compose_vertex_render_prompt(
        product_info=product_info,
        brand_style=brand_style,
        platform=platform,
        market=market,
        output_type=normalized_output,
        aspect_ratio=aspect_ratio,
    )

    listing_prompts = []
    if normalized_output == "listing-set":
        listing_prompts = _generate_listing_set_prompts(
            product_info=product_info,
            brand_style=brand_style or {},
            platform=platform,
            market=market,
            aspect_ratio=aspect_ratio,
        )

    payload: Dict[str, Any] = {
        "command": "render_submit",
        "mode": "render",
        "input": {
            "transfer_id": transfer_id,
            "product_info": product_info,
            "style_name": style_name,
            "brand_style": brand_style,
            "prompt": inp.get("prompt") or constructed_prompt,
            "listing_prompts": listing_prompts,
            "aspect_ratio": aspect_ratio,
            "language": language,
            "platform": platform,
            "market": market,
            "output_type": output_type,
            "images": resolved_images,
        },
    }
    cache_meta = {
        "command": "render_submit",
        "transfer_id": transfer_id,
        "product_info": product_info,
        "platform": platform,
        "market": market,
        "aspect_ratio": aspect_ratio,
        "style_name": style_name,
        "output_type": output_type,
    }
    return payload, cache_meta


def _submit_fal_job(payload: Dict[str, Any], cache_meta: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode()
    url = _fal_submit_url()
    code, resp = _http_request("POST", url, body)
    if code < 200 or code >= 300:
        _json_error(
            False,
            "API_ERROR",
            f"HTTP {code}",
            "Failed to submit the FAL request. Check FAL_API_KEY and FAL_API_URL.",
            {"http_code": code, "result": resp},
        )

    request_id = _pick_request_id(resp) or str(uuid.uuid4())
    cached = {
        **cache_meta,
        "request_id": request_id,
        "submit_response": resp,
        "status_url": resp.get("status_url") if isinstance(resp, dict) else None,
        "response_url": resp.get("response_url") if isinstance(resp, dict) else None,
        "poll_url": resp.get("poll_url") if isinstance(resp, dict) else None,
        "submitted_at": int(time.time()),
    }

    terminal = _terminal_state(resp)
    if terminal is True:
        cached["final_response"] = resp
    _cache_write(request_id, cached)
    return cached


def _fetch_fal_status(job_id: str) -> Dict[str, Any]:
    cached = _cache_read(job_id)
    if not cached:
        _json_error(False, "PARAM_ERROR", f"Unknown task id: {job_id}", "Run style_create or render_submit first in this environment.")

    if isinstance(cached.get("final_response"), dict):
        return cached

    status_urls = _fal_status_candidates(cached)
    last_code = None
    last_resp: Any = None
    for status_url in status_urls:
        code, resp = _http_request("GET", status_url, None, json_mode=False)
        last_code = code
        last_resp = resp
        if 200 <= code < 300:
            cached["last_status_response"] = resp
            done = _terminal_state(resp)
            has_result = bool(_extract_urls(resp) or _extract_text_candidates(resp))
            if done is True or has_result:
                cached["final_response"] = resp
            _cache_write(job_id, cached)
            return cached

    if isinstance(cached.get("submit_response"), dict):
        submit_resp = cached["submit_response"]
        if _terminal_state(submit_resp) is True:
            cached["final_response"] = submit_resp
            _cache_write(job_id, cached)
            return cached

    if last_code is not None:
        _json_error(
            False,
            "API_ERROR",
            f"HTTP {last_code}",
            "Failed to query the FAL request status.",
            {"http_code": last_code, "result": last_resp},
        )
    return cached


def cmd_style_create(inp: Dict[str, Any]) -> None:
    payload, cache_meta = _build_style_request(inp)
    cached = _submit_fal_job(payload, cache_meta)
    request_id = str(cached.get("request_id", ""))
    submit_response = cached.get("submit_response")
    print(
        json.dumps(
            {
                "ok": True,
                "command": "ecommerce_style_create",
                "task_id": request_id,
                "result": submit_response,
                "user_hint": "Use style_poll with task_id to retrieve styles or terminal output.",
            },
            ensure_ascii=False,
        )
    )


def cmd_preview_set(inp: Dict[str, Any]) -> None:
    product_info = str(inp.get("product_info", "")).strip() or "product"
    brand_style = inp.get("brand_style", {})
    platform = str(inp.get("platform", "amazon")).strip()
    market = str(inp.get("market", "US")).strip()
    aspect_ratio = str(inp.get("aspect_ratio", inp.get("ratio", "1:1")) or "1:1").strip() or "1:1"
    prompts = _generate_listing_set_prompts(product_info, brand_style, platform, market, aspect_ratio)
    print(json.dumps({
        "ok": True,
        "command": "ecommerce_preview_set",
        "listing_set_prompts": prompts,
        "user_hint": "Check these prompts before submitting render_submit with output_type='listing-set'."
    }, ensure_ascii=False, indent=2))


def cmd_style_poll(inp: Dict[str, Any]) -> None:
    task_id = str(inp.get("task_id", "")).strip()
    if not task_id:
        _json_error(False, "PARAM_ERROR", "Missing task_id", "Run style_create first.")

    max_wait = float(inp.get("max_wait_sec", 180))
    interval = float(inp.get("interval_sec", 2))
    deadline = time.time() + max_wait

    while time.time() < deadline:
        cached = _fetch_fal_status(task_id)
        resp = cached.get("final_response") or cached.get("last_status_response") or cached.get("submit_response")
        done, styles, styles_raw = _normalize_style_poll_result(resp)
        if done:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "command": "ecommerce_style_poll",
                        "done": True,
                        "styles": styles,
                        "styles_raw": styles_raw,
                        "result": resp,
                    },
                    ensure_ascii=False,
                )
            )
            return
        time.sleep(interval)

    print(
        json.dumps(
            {
                "ok": False,
                "error_type": "TEMPORARY_UNAVAILABLE",
                "message": "Style polling timed out",
                "user_hint": f"The task did not finish within {max_wait}s. Increase max_wait_sec and try again.",
                "task_id": task_id,
            },
            ensure_ascii=False,
        )
    )
    sys.exit(1)


def cmd_render_submit(inp: Dict[str, Any]) -> None:
    payload, cache_meta = _build_render_request(inp)
    cached = _submit_fal_job(payload, cache_meta)
    request_id = str(cached.get("request_id", ""))
    submit_response = cached.get("submit_response")
    print(
        json.dumps(
            {
                "ok": True,
                "command": "ecommerce_render_submit",
                "transfer_id": cache_meta.get("transfer_id"),
                "batch_id": request_id,
                "result": submit_response,
                "user_hint": "Use render_poll with batch_id to retrieve generated images.",
            },
            ensure_ascii=False,
        )
    )


def cmd_render_poll(inp: Dict[str, Any]) -> None:
    batch_id = str(inp.get("batch_id", "")).strip()
    if not batch_id:
        _json_error(False, "PARAM_ERROR", "Missing batch_id", "Run render_submit first.")

    output_dir = resolve_output_dir(inp)
    product_name = str(inp.get("product_name", "")).strip() or str(inp.get("product_info", "")).strip() or "product"
    max_wait = float(inp.get("max_wait_sec", 600))
    interval = float(inp.get("interval_sec", 3))
    deadline = time.time() + max_wait

    while time.time() < deadline:
        cached = _fetch_fal_status(batch_id)
        resp = cached.get("final_response") or cached.get("last_status_response") or cached.get("submit_response")
        done = _terminal_state(resp)
        media_urls, items = _normalize_render_items(resp)
        if media_urls and (done is True or done is None):
            local_paths = _local_image_paths_from_items(items, output_dir, product_name)
            if not local_paths:
                local_paths = _local_image_paths_from_urls(media_urls, output_dir, product_name)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "command": "ecommerce_render_poll",
                        "done": True,
                        "media_urls": media_urls,
                        "output_dir": str(output_dir),
                        "local_paths": local_paths,
                        "items": items,
                        "result": resp,
                    },
                    ensure_ascii=False,
                )
            )
            return
        time.sleep(interval)

    print(
        json.dumps(
            {
                "ok": False,
                "error_type": "TEMPORARY_UNAVAILABLE",
                "message": "Render polling timed out",
                "user_hint": f"Did not receive generated images within {max_wait}s. Increase max_wait_sec and try again.",
                "batch_id": batch_id,
            },
            ensure_ascii=False,
        )
    )
    sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser(description="Morzai ecommerce product-kit FAL runner")
    p.add_argument("command", choices=("style_create", "style_poll", "render_submit", "render_poll", "preview_set"))
    p.add_argument("--input-json", required=True, help="JSON input string")
    args = p.parse_args()
    try:
        inp = json.loads(args.input_json)
    except json.JSONDecodeError as e:
        _json_error(False, "PARAM_ERROR", str(e), "--input-json must be valid JSON.")

    if not isinstance(inp, dict):
        _json_error(False, "PARAM_ERROR", "Root node must be a JSON object", "")

    if args.command == "style_create":
        cmd_style_create(inp)
    elif args.command == "style_poll":
        cmd_style_poll(inp)
    elif args.command == "preview_set":
        cmd_preview_set(inp)
    elif args.command == "render_submit":
        cmd_render_submit(inp)
    else:
        cmd_render_poll(inp)


if __name__ == "__main__":
    main()

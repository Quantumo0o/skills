#!/usr/bin/env python3
"""
A/B Content Predictor — predict which ad/post variant wins before spending money.

Based on TRIBE v2 research findings (Meta AI, 2026) mapped to rule-based scoring:
  • Amygdala response    → loss framing, faces, social proof with stakes
  • Reward circuit       → gain framing, scarcity, identity alignment
  • Language cortex      → second-person, short sentences, concrete nouns
  • Visual cortex        → faces in first sentence, concrete imagery

Each ICP has a different neural weight profile — the same content scores
differently against a loss-averse credit-repair lead vs a gain-seeking
crypto holder. That's the key insight: it's not just what you say, it's
who you're saying it to.

Usage:
    python3 ab_predictor.py --product "crypto mortgage" --variants variants.json
    python3 ab_predictor.py --product "va-loan" --text "You earned zero down. Use it."
    python3 ab_predictor.py --demo
"""

import re
import sys
import json
import argparse
import importlib.util as _ilu
import pathlib as _pl
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Backend: content_resonance_scorer.py (claude-3's TRIBE-based scorer)
# Loaded dynamically so ab_predictor.py stays portable if scorer is absent.
# ---------------------------------------------------------------------------

def _load_crs():
    """Load content_resonance_scorer from sibling project dir."""
    here = _pl.Path(__file__).parent
    scorer_path = here.parent / "content-resonance-scorer" / "content_resonance_scorer.py"
    if not scorer_path.exists():
        return None
    spec = _ilu.spec_from_file_location("content_resonance_scorer", scorer_path)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_CRS = _load_crs()

# Field shim: CRS FeatureScores attribute → (ab_predictor dimension, normalization divisor)
# Density fields (per-100-words) are divided so they reach 1.0 at realistic peak usage.
_CRS_FIELD_MAP = {
    "loss_framing_score":       ("loss",          1.0),  # already 0-1 ratio
    "gain_framing_score":       ("gain",          1.0),  # already 0-1 ratio
    "social_proof_density":     ("social_proof",  5.0),  # per-100w; /5 → 1.0 at 5%
    "urgency_density":          ("urgency",       3.0),  # per-100w; /3 → 1.0 at 3%
    "identity_alignment_score": ("identity",      1.0),  # already 0-1
    "sentence_complexity_score":("simplicity",    1.0),  # already 0-1
    "second_person_density":    ("second_person", 8.0),  # per-100w; /8 → 1.0 at 8%
    "concrete_noun_density":    ("concrete",      6.0),  # per-100w; /6 → 1.0 at 6%
}


# ---------------------------------------------------------------------------
# Neural weight profiles per ICP
# (derived from TRIBE research findings on brain-region activation patterns)
# ---------------------------------------------------------------------------

# Weight dimensions: loss | gain | social_proof | urgency | identity | simplicity
# Values 0.0-2.0 (1.0 = baseline, >1.0 = this ICP is especially responsive to it)
ICP_NEURAL_WEIGHTS = {
    "crypto-mortgage": {
        # Gain-seeking, autonomy-driven, sophisticated — hates hype
        "loss":         0.8,   # loss framing works less well — feels manipulative to them
        "gain":         1.8,   # strong gain-seeking: upside, appreciation, keep the coins
        "social_proof": 0.9,   # peer validation helps but they fact-check it
        "urgency":      0.6,   # scarcity tactics backfire on skeptical crypto crowd
        "identity":     1.7,   # identity alignment is huge: "people who think like you"
        "simplicity":   0.8,   # they handle complexity — shorter isn't always better
        "second_person":1.2,
        "concrete":     1.5,   # concrete numbers, real tax math — they want specifics
    },
    "credit-repair": {
        # Loss-aversion dominant, emotionally triggered, wants hope not shame
        "loss":         1.8,   # "you're paying someone else's mortgage" — very effective
        "gain":         1.3,
        "social_proof": 1.6,   # "most people with a 600 score can do X" is very reassuring
        "urgency":      1.2,
        "identity":     1.5,   # "people like you" — needs to see themselves as a homeowner
        "simplicity":   1.7,   # overwhelmed — short sentences, clear steps matter
        "second_person":1.6,
        "concrete":     1.4,   # specific numbers (90 days, 100 points) land well
    },
    "va-loan": {
        # Duty-oriented, earned-it framing, distrusts hype
        "loss":         1.4,   # "benefit you're not using" is effective
        "gain":         1.3,
        "social_proof": 1.3,   # peer veterans as social proof
        "urgency":      0.7,   # doesn't respond well to pressure
        "identity":     2.0,   # identity is everything — veteran, earned this, deserves it
        "simplicity":   1.5,   # direct, no-BS communication
        "second_person":1.4,
        "concrete":     1.3,
    },
    "realtor-partner": {
        # B2B professional, skeptical, values track record over claims
        "loss":         1.5,   # "your lender is making you look bad" — strong hook
        "gain":         1.4,   # more closings, more commission
        "social_proof": 1.8,   # case studies, agent testimonials — highest weight
        "urgency":      0.5,   # urgency tactics feel salesy — strongly penalized
        "identity":     1.3,
        "simplicity":   1.3,
        "second_person":1.2,
        "concrete":     1.8,   # concrete results: "closed 3 days early", "0 blown deals"
    },
    "first-time-buyer": {
        # Fear-dominant, needs reassurance, easily overwhelmed
        "loss":         1.3,
        "gain":         1.4,
        "social_proof": 1.7,   # "other people like you did this and it worked"
        "urgency":      1.0,
        "identity":     1.4,   # wants to see themselves as a homeowner
        "simplicity":   2.0,   # highest simplicity weight — complexity = anxiety
        "second_person":1.7,
        "concrete":     1.5,   # "5 steps", "$6,000 down payment", makes it feel achievable
    },
}

# Fallback for unknown ICPs
DEFAULT_WEIGHTS = {k: 1.0 for k in ["loss","gain","social_proof","urgency","identity","simplicity","second_person","concrete"]}

# ---------------------------------------------------------------------------
# Feature extractors (the TRIBE research-based signal layer)
# ---------------------------------------------------------------------------

LOSS_WORDS = {
    "lose","losing","lost","miss","missing","behind","cost","risk","waste",
    "wasting","stuck","trap","trapped","landlord","rent","paying someone",
    "throwing away","giving away","left behind","fall behind","can't afford",
    "denied","rejected","ignored","blew up","blown","never","without",
}
GAIN_WORDS = {
    "save","saving","earn","earning","build","building","grow","growing",
    "keep","keeping","own","owning","get","gain","profit","upside","more",
    "ahead","equity","wealth","appreciate","compound","benefit","win","won",
    "free","zero","no cost","no PMI","no down","approved","qualify",
}
SOCIAL_PROOF_WORDS = {
    "most","many","people","buyers","veterans","agents","clients","others",
    "everyone","average","typical","thousands","hundreds","families","couples",
    "statistics","data","research","percent","study","proven","according to",
}
URGENCY_WORDS = {
    "now","today","limited","before","deadline","soon","last","final",
    "expires","ending","closing","while","don't wait","act","immediately",
    "window","opportunity","rates are","market is","won't last",
}
IDENTITY_WORDS = {
    "veteran","veterans","served","service","crypto","bitcoin","ethereum","holders",
    "first-time","renter","renters","first generation","entrepreneur","self-employed",
    "family","couples","couple","professional","agent","realtor","DFW","Texas",
    "people like you","someone like you","for you","built for",
}
CONCRETE_PATTERN = re.compile(
    r'\$[\d,]+|\d+[\s-]?(day|month|year|point|percent|%|step|BR|bed|bath|hour|minute|sq)',
    re.IGNORECASE
)
SECOND_PERSON = re.compile(r'\b(you|your|you\'re|you\'ve|you\'ll|yourself)\b', re.IGNORECASE)
FACE_PATTERN = re.compile(r'\b(I|me|my|we|our|Patrick|Sarah|[A-Z][a-z]+)\b')


def _words(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text.lower())


def _score_features_via_crs(text: str) -> dict[str, float]:
    """Feature extraction via content_resonance_scorer backend (claude-3)."""
    scored = _CRS.score_text(text)
    f = scored.features
    feats = {}
    for crs_attr, (dim, divisor) in _CRS_FIELD_MAP.items():
        raw = getattr(f, crs_attr, 0.0)
        feats[dim] = min(1.0, raw / divisor)
    feats["_face_first"] = 1.0 if FACE_PATTERN.search(text[:100]) else 0.0
    feats["_word_count"] = float(scored.word_count)
    feats["_sentences"] = float(scored.sentence_count)
    return feats


def _score_features_internal(text: str) -> dict[str, float]:
    """Fallback feature extraction (used when CRS backend is unavailable)."""
    words = _words(text)
    n = max(len(words), 1)
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    n_sentences = max(len(sentences), 1)
    avg_words_per_sentence = n / n_sentences

    loss_hits = sum(1 for w in words if w in LOSS_WORDS)
    gain_hits = sum(1 for w in words if w in GAIN_WORDS)
    social_hits = sum(1 for w in words if w in SOCIAL_PROOF_WORDS)
    urgency_hits = sum(1 for w in words if w in URGENCY_WORDS)
    identity_hits = sum(1 for w in words if w in IDENTITY_WORDS)
    concrete_hits = len(CONCRETE_PATTERN.findall(text))
    second_person_hits = len(SECOND_PERSON.findall(text))
    face_in_first_30 = len(FACE_PATTERN.findall(text[:100])) > 0

    simplicity_score = max(0.0, 1.0 - (avg_words_per_sentence - 8) / 20)

    return {
        "loss":          min(1.0, loss_hits / max(n * 0.05, 1)),
        "gain":          min(1.0, gain_hits / max(n * 0.05, 1)),
        "social_proof":  min(1.0, social_hits / max(n * 0.05, 1)),
        "urgency":       min(1.0, urgency_hits / max(n * 0.03, 1)),
        "identity":      min(1.0, identity_hits / max(n * 0.04, 1)),
        "simplicity":    max(0.0, simplicity_score),
        "second_person": min(1.0, second_person_hits / max(n * 0.08, 1)),
        "concrete":      min(1.0, concrete_hits / max(n_sentences * 0.5, 1)),
        "_face_first":   1.0 if face_in_first_30 else 0.0,
        "_word_count":   n,
        "_sentences":    n_sentences,
    }


def score_features(text: str) -> dict[str, float]:
    """Extract normalized feature scores. Uses CRS backend when available."""
    if _CRS is not None:
        return _score_features_via_crs(text)
    return _score_features_internal(text)


def resonance_score(text: str, icp_key: str) -> dict:
    """
    Score a piece of content against an ICP's neural weight profile.
    Returns score 0-100 and per-dimension breakdown.
    """
    weights = ICP_NEURAL_WEIGHTS.get(icp_key, DEFAULT_WEIGHTS)
    features = score_features(text)

    weighted_sum = 0.0
    total_weight = 0.0
    breakdown = {}

    for dim, weight in weights.items():
        feat_val = features.get(dim, 0.0)
        contribution = feat_val * weight
        weighted_sum += contribution
        total_weight += weight
        breakdown[dim] = {
            "raw": round(feat_val, 3),
            "weight": weight,
            "contribution": round(contribution, 3),
        }

    # Face-in-first-30-chars bonus (strong visual cortex signal)
    if features.get("_face_first"):
        weighted_sum += 0.05 * total_weight / len(weights)

    raw_score = weighted_sum / total_weight if total_weight else 0
    score_100 = min(100, round(raw_score * 100))

    result = {
        "score": score_100,
        "icp": icp_key,
        "word_count": int(features["_word_count"]),
        "sentences": int(features["_sentences"]),
        "breakdown": breakdown,
        "flags": _get_flags(features, icp_key, score_100),
        "backend": "crs" if _CRS is not None else "internal",
    }

    # Divergence check: ICP-weighted score vs CRS baseline (ICP-agnostic).
    # Large divergence means the ICP weighting significantly shifts the outcome — flag for review.
    if _CRS is not None:
        crs_baseline = round(_CRS.score_text(text).features.resonance_score, 1)
        divergence = abs(score_100 - crs_baseline)
        result["_crs_baseline"] = crs_baseline
        result["_divergence"] = round(divergence, 1)
        if divergence >= 15:
            result["flags"].append(
                f"⚠ ICP weighting shifts score {divergence:.0f}pts from baseline "
                f"({score_100} vs CRS {crs_baseline:.0f}) — review ICP profile weights"
            )

    return result


def _get_flags(features: dict, icp_key: str, score: int) -> list[str]:
    """Generate human-readable coaching flags."""
    flags = []
    weights = ICP_NEURAL_WEIGHTS.get(icp_key, DEFAULT_WEIGHTS)

    if features["loss"] < 0.02 and weights["loss"] >= 1.4:
        flags.append("⚠ Add loss framing — this ICP is loss-aversion dominant")
    if features["gain"] < 0.02 and weights["gain"] >= 1.5:
        flags.append("⚠ Add gain/upside framing — this ICP responds to opportunity")
    if features["social_proof"] < 0.02 and weights["social_proof"] >= 1.5:
        flags.append("⚠ Add social proof — this ICP needs peer validation")
    if features["urgency"] > 0.1 and weights["urgency"] <= 0.7:
        flags.append("⚠ Reduce urgency language — may backfire with this ICP")
    if features["second_person"] < 0.03 and weights["second_person"] >= 1.4:
        flags.append("⚠ Add more 'you/your' — this ICP responds to direct address")
    if features["simplicity"] < 0.4 and weights["simplicity"] >= 1.5:
        flags.append("⚠ Simplify sentences — this ICP is easily overwhelmed")
    if features["concrete"] < 0.1 and weights["concrete"] >= 1.4:
        flags.append("⚠ Add concrete numbers/specifics — this ICP trusts data")
    if score >= 70:
        flags.append("✓ Strong resonance — publish-ready for this ICP")
    elif score >= 50:
        flags.append("~ Moderate resonance — refine before spending ad budget")
    else:
        flags.append("✗ Low resonance — rewrite against ICP hook formulas before use")

    return flags


# ---------------------------------------------------------------------------
# A/B comparison
# ---------------------------------------------------------------------------

@dataclass
class Variant:
    label: str
    text: str
    score: int = 0
    breakdown: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)


def compare_variants(variants: list[Variant], icp_key: str) -> list[Variant]:
    """Score all variants and return sorted best-first."""
    for v in variants:
        result = resonance_score(v.text, icp_key)
        v.score = result["score"]
        v.breakdown = result["breakdown"]
        v.flags = result["flags"]
    return sorted(variants, key=lambda v: v.score, reverse=True)


def print_comparison(variants: list[Variant], icp_key: str):
    bar = "━" * 60
    print(f"\n{bar}")
    print(f"A/B RESONANCE PREDICTION — ICP: {icp_key}")
    print(f"{bar}")
    print(f"{'Rank':<5} {'Label':<20} {'Score':<8} {'Words'}")
    print("─" * 60)

    for i, v in enumerate(variants, 1):
        medals = ["🥇","🥈","🥉"]
        medal = medals[i-1] if i-1 < len(medals) else f"#{i}"
        wc = resonance_score(v.text, icp_key)["word_count"]
        bar_len = v.score // 5
        bar_str = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {medal}  {v.label:<20} [{bar_str}] {v.score}/100  ({wc}w)")

    print()
    winner = variants[0]
    print(f"PREDICTED WINNER: {winner.label}")
    print(f"Score: {winner.score}/100\n")
    print("Winner text:")
    print(f"  \"{winner.text[:200]}\"")
    print()
    print("Coaching flags:")
    for flag in winner.flags:
        print(f"  {flag}")

    if len(variants) > 1:
        loser = variants[-1]
        print(f"\nWHY {loser.label} LOSES (score {loser.score}/100):")
        loser_flags = [f for f in loser.flags if f.startswith("⚠")]
        for f in loser_flags[:3]:
            print(f"  {f}")
    print(f"\n{bar}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

__version__ = "1.0.0"


def main():
    parser = argparse.ArgumentParser(description="A/B content resonance predictor")
    parser.add_argument("--product", "-p", default="first-time-buyer",
                        help="ICP key (crypto-mortgage, credit-repair, va-loan, realtor-partner, first-time-buyer)")
    parser.add_argument("--variants", help="JSON file with [{label, text}] array")
    parser.add_argument("--text", help="Score a single piece of content")
    parser.add_argument("--demo", action="store_true", help="Run demo comparison (no API key needed)")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output JSON")
    parser.add_argument("--version", action="version", version=f"ab-predictor {__version__}")
    args = parser.parse_args()

    if args.demo:
        # Demo: two hooks for crypto-mortgage ICP
        demo_variants = [
            Variant("Hook A — Loss frame",
                    "You don't have to sell your Bitcoin to buy a house. "
                    "Pledge it as collateral. Keep the upside. Get the keys. "
                    "No capital gains. No missed appreciation. "
                    "DFW crypto holders: this is real and it's available now."),
            Variant("Hook B — Generic",
                    "Looking to buy a home? We offer competitive rates and fast pre-approvals. "
                    "Our experienced team will guide you through the process. "
                    "Contact us today to learn more about our mortgage options."),
            Variant("Hook C — Identity + concrete",
                    "BTC holders in DFW who bought before 2022 are sitting on $200K-$2M in "
                    "unrealized gains. Fannie Mae now lets you pledge that crypto as collateral "
                    "— zero capital gains event, zero coins sold. "
                    "Your coins appreciate while you build equity. That's the move."),
        ]
        ranked = compare_variants(demo_variants, "crypto-mortgage")
        print_comparison(ranked, "crypto-mortgage")
        return

    if args.text:
        result = resonance_score(args.text, args.product)
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nResonance score for '{args.product}': {result['score']}/100")
            for flag in result["flags"]:
                print(f"  {flag}")
        return

    if args.variants:
        with open(args.variants) as f:
            raw = json.load(f)
        variants = [Variant(label=v["label"], text=v["text"]) for v in raw]
        ranked = compare_variants(variants, args.product)
        if args.as_json:
            print(json.dumps([{"label": v.label, "score": v.score, "flags": v.flags}
                               for v in ranked], indent=2))
        else:
            print_comparison(ranked, args.product)
        return

    parser.print_help()


if __name__ == "__main__":
    main()

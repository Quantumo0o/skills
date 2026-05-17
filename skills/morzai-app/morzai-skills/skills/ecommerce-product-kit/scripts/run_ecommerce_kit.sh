#!/usr/bin/env bash
# Ecommerce product-kit FAL backend entrypoint
# Fill these locally before running:
# export FAL_API_KEY=""
# export FAL_API_URL=""
# Usage:
#   # 1. Create styles using natural language
#   bash run_ecommerce_kit.sh style_create --input-json '{"image":"...","product_info":"Red t-shirt","platform":"amazon"}'
#
#   # 2. Preview the full Listing Set (P1-P7) prompt scripts locally
#   bash run_ecommerce_kit.sh preview_set --input-json '{"product_info":"Red t-shirt","brand_style":{...}}'
#
#   # 3. Submit high-quality render using Google Structured Prompt layers
#   bash run_ecommerce_kit.sh render_submit --input-json '{"image":"...","output_type":"listing-set","brand_style":{...}}'
#
# LISTING SET PROMPT SPLICING SCRIPTS (P1-P7 EXHAUSTIVE LIST):
#   P1 (Hero): {subjectDescription} on a pure white background, crisp textures, balanced studio lighting, eye-level hero shot, high-end commercial quality.
#   P2 (Benefits): Focus on {subjectDescription} showing fine details and premium quality, soft directional studio lighting, clean background.
#   P3 (Benefits Alt): Showcase {subjectDescription} from an angle, highlighting fit and design, professional ecommerce lighting.
#   P4 (Detail): Extreme macro close-up of {subjectDescription}, focus on fabric weave and stitching, shallow depth of field, high-end sensory detail.
#   P5 (Multi-view): Side profile view of {subjectDescription}, professional fashion photography, consistent lighting with hero image.
#   P6 (Lifestyle): {subjectDescription} in a {backgroundContext}, with {lightingAndMood}, {photographyStyle}, realistic lifestyle atmosphere.
#   P7 (Decision): Flat-lay shot of {subjectDescription} on a neutral surface, even top-down lighting, clear and informative composition.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/ecommerce_product_kit.py" "$@"

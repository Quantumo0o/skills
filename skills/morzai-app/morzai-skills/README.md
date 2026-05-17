# Morzai AI E-commerce Skills (Master Suite)

A professional collection of AI-powered image processing skills for e-commerce, organized into a router plus two capability layers.

Designed for global sellers on platforms like Amazon, Shopify, Temu, and SHEIN.

## Root Skill Design

The root [`SKILL.md`](SKILL.md) remains a thin router.

- It reads [`api/commands.json`](api/commands.json) as the single source of truth for routing, required inputs, and execution mapping.
- It asks only for missing required inputs.
- It then opens the routed child skill and continues execution in the same user-facing agent.
- It does not duplicate child-skill capability details at the root layer.

## Architecture: Two-Layer Capability

### Layer 1: Single-Function Professional Editing
Focuses on high-precision processing of a single aspect of an image.

| Skill | Description | Key Capabilities |
|-------|-------------|------------------|
| [apparel-recolor](skills/apparel-recolor) | Precise garment recolor. | Part-based recolor, sample-assisted color picking, pattern handling, 2K/4K output. |
| [garment-retouch](skills/garment-retouch) | Advanced apparel cleanup. | Ghost mannequin effect, hanger cleanup, background cleanup, 2K/4K output. |
| [clothing-adjustment](skills/clothing-adjustment) | Preset-driven garment cleanup. | Whole-garment wrinkle cleanup, surface cleanup, lint and pet hair cleanup. |

### Layer 2: Full-Chain Listing Sets and Kits
Focuses on generating end-to-end marketing assets from a single product photo.

| Skill | Description | Key Capabilities |
|-------|-------------|------------------|
| [morzai-ecommerce-product-kit](skills/morzai-ecommerce-product-kit) | Product kits and listing sets. | P1-P7 listing sets, hero/detail/lifestyle images, marketing posters, apparel visuals. |

## Quick Reference

| Task | Skill | Technical Mapping |
|------|-------|-------------------|
| Change shirt color to Morandi Gray | `apparel-recolor` | `target_parts: ['upper_body']`, `hex_color: "#B8B8B8"` |
| Extract color from a sample image | `apparel-recolor` | `extract_color -> confirm hex_color` |
| Remove ghost mannequin in 4K | `garment-retouch` | `model_version: "v2.0"`, `resolution: "4K"` |
| Perfectly iron a wrinkled coat | `clothing-adjustment` | `preset_direction: strong_flattening` |
| Remove pet hair and lint from fabric | `clothing-adjustment` | `preset_direction: surface_cleanup` |
| Make the garment look cleaner and flatter overall | `clothing-adjustment` | `preset_direction: balanced_cleanup` |
| Build a full Amazon listing image set | `morzai-ecommerce-product-kit` | `platform: "amazon"`, `market: "US"`, `output_type: "listing_set"` |

## Example Prompts

- "Recolor this dress to the same blue as the reference photo, but keep the brand logo visible."
- "Apply a ghost mannequin effect to this sweater and output it in 4K resolution."
- "The jacket is too wrinkled from transit. Give it a cleaner, flatter overall look."
- "Match the color of these pants to the first sample image I sent earlier."

## Technical Features

- Expert SOPs: every skill is backed by `references/` containing industry-specific benchmarks.
- Global compliance: built-in rules for Amazon, Pinterest, Instagram, Shopify, Temu, and SHEIN.
- Router + knowledge split: routing stays in root, domain detail stays in child skills.
- Execution split: all public skills now trigger the `morzai` CLI, and `morzai-ecommerce-product-kit` continues through `morzai-cli-server` to the nano backend.

## Requirements

- **MORZAI_API_KEY**: Optional credential override for CLI-based workflows.
- **Morzai CLI**: `morzai-ecommerce-product-kit` now expects the public `morzai` CLI to be installed and configured.
- **Claude Code CLI**: Or any skills-compatible AI agent (Cursor, Codex, etc.).

## License

MIT

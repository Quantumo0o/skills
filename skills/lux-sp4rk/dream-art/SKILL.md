---
name: dream-art
description: Transform a user's dream into actionable artwork concepts and generate outputs. Use when Uli describes a dream and wants to explore its creative potential — symbols, imagery, emotional texture translated into visual art, music, writing, or animation. Triggered by phrases like "I had a dream about...", "last night I dreamed...", "analyze this dream", "dream journal", "dream artwork", "dream interpretation", or when naturally describing dream content.
---

# Dream Art — Skill

Transform raw dream content into creative output. Three-phase workflow.

---

## Phase 1 — Intake & Log to Obsidian

**Use `obsidian-cli` to log the dream to today's daily note.**

1. Find today's daily note path:
   ```bash
   obsidian-cli print-default --path-only
   ```
   Daily notes are typically stored as `Daily Notes/YYYY-MM-DD.md` within the vault.

2. Append to today's daily note with structured metadata:
   ```markdown
   ## Dream — [HH:MM]

   **Tags:** #dream #intake

   **Raw content:**
   [everything the user described — verbatim]

   **Emotional texture:** [1-2 sentences on the mood, feeling tone]
   **Key imagery:** [list the most vivid visual elements]
   **Notable symbols:** [recurring or charged objects/figures]
   **Unusual elements:** [things that don't follow ordinary logic]

   ---
   ```

3. Ask the user: *"What medium feels right — image, music, animation, prose, or open?"* If they say open, default to image generation.

---

## Phase 2 — Dream Analysis (Internal)

Do not output this phase explicitly. Do it silently, then move to Phase 3.

**Analyze the dream's creative potential:**
- What is the dominant emotional frequency? (dread, longing, wonder, confusion, awe)
- What single image or moment is the "heart" of the dream?
- What medium best captures the texture — not just the content, but the *feeling*?
- What would an artwork need to include to make someone feel what the dream felt like?

**Build toward a creative brief** (use the ideation pattern if helpful):
- Named emotional intent
- Tone and negative space
- Reference points (if any come to mind)

---

## Phase 3 — Generate & Deliver

Based on user's chosen medium:

**Image:** Use `image_generate` with a prompt derived from the dream's heart image. Include emotional texture in the prompt. Use `image` tool for reference if user has shared a style reference.

**Music/Audio:** Use `music_generate` with a prompt that captures the dream's emotional frequency. Ask user: *"Song or ambient? Vocals or instrumental?"*

**Prose:** Write a short piece (flash fiction, poem, scene) that transports the reader into the dream's world. 300-800 words.

**Animation:** Use `video_generate` for short atmospheric pieces (5-15s). Alternatively generate an image with strong motion implied.

**After delivery:** Ask *"Want to push further — different medium, refine, or take it in a new direction?"* (one question only)

---

## Key Principles

- **Log first, create second.** The Obsidian capture makes the dream permanent and search-able.
- **Emotional texture over literal content.** Don't describe the dream back to the user — reframe it.
- **One strong image beats ten weak ones.** Find the heart.
- **Never interpret the dream clinically.** This is a creative tool, not a therapy session.
- **Brief beats ramble.** Phase 2 is for you — Phase 3 is what the user sees.
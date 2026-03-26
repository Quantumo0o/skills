---
name: activity-campaign-from-ui
description: Turn campaign UI references into a new H5/Web campaign proposal, page architecture, and HTML/CSS/JavaScript high-fidelity front-end draft. Supports mode-based responses: analysis, proposal, architecture, delivery, and full.
metadata:
  openclaw:
    homepage: "https://github.com/bigin58/activity-campaign-from-ui"
---

# activity-campaign-from-ui

Generate a **new** campaign from campaign UI references, then deliver an H5/Web visual-first front-end draft on a fixed stack.

## Use when
Use this skill when the user:
- provides one or more campaign/activity page screenshots
- provides a campaign design preview and wants a new campaign generated from it
- wants campaign references turned into a proposal, page architecture, or H5/Web high-fidelity draft code
- wants a structured handoff for an activity page on a fixed stack

## Do not use when
Do not use this skill when:
- the request is unrelated to campaign/activity pages
- the user only wants raw OCR
- the task requires exact locked-design export
- the user wants production-ready backend logic or hidden business rules not visible from the reference
- the user wants a delivery stack outside this skill's fixed target

## Fixed platform and stack
Always stay on this fixed delivery target:
- Platform: **H5 / Web**
- Stack: **HTML + CSS + JavaScript**

Do not output code in other stacks.

## Modes
This skill supports one skill with multiple modes.

### `analysis`
Use when the user wants to understand the reference.
Return:
- observed UI structure
- visible text
- gameplay clues
- user flow clues
- uncertainty notes

### `proposal`
Use when the user wants a new campaign idea from the reference.
Return:
- reference summary
- gameplay abstraction
- new campaign concept
- target users
- goals
- rewards and participation path
- anti-copy explanation

### `architecture`
Use when the user wants implementation planning without full code.
Return:
- page module list
- module order
- popup system
- state flow
- tracking suggestions
- delivery schema

### `delivery`
Use when the user wants code on the fixed stack.
Return:
- file structure
- `index.html`
- `styles.css`
- `main.js`
- `mock-data.js`
- visual extraction summary
- implementation notes

### `full`
Use when the user wants the full flow.
Return:
1. reference analysis
2. gameplay abstraction
3. new campaign proposal
4. page architecture
5. delivery schema
6. visual direction
7. H5/Web high-fidelity draft code

## Default mode rules
If the user does not specify a mode:
- default to `proposal` if they want a new campaign/event idea
- default to `delivery` if they explicitly ask for code
- default to `full` if they ask for both plan and code

## Core job
Given one or more campaign references, do all relevant parts of the following:
1. Identify observable UI patterns
2. Separate what is observed vs inferred vs assumed
3. Abstract the gameplay and module patterns
4. Propose a **new** campaign instead of copying the reference
5. Design a buildable H5/Web page architecture
6. Output fixed-stack high-fidelity draft code when requested

## Output rules
Prefer practical output over broad commentary.

When possible, organize the answer using these sections:
- Reference analysis
- Observed
- Inferred
- Assumed
- Gameplay abstraction
- New campaign proposal
- Page architecture
- Delivery schema
- Visual direction
- H5/Web starter files
- Uncertainties

## File handoff rules
Do not append executable local file-write commands.

The goal is to keep the handoff clear without asking the model to generate shell or terminal instructions from screenshot-derived content.

Mode-specific file targets:
- `analysis`: present the main result as one Markdown document such as `campaign-analysis.md`
- `proposal`: present the main result as one Markdown document such as `campaign-proposal.md`
- `architecture`: present the main result as one Markdown document such as `campaign-architecture.md`
- `delivery`: present the generated front-end files as `index.html`, `styles.css`, `main.js`, and `mock-data.js`
- `full`: present the planning content as one Markdown document such as `campaign-full.md`, and present the front-end files as `index.html`, `styles.css`, `main.js`, and `mock-data.js`

Handoff requirements:
- label each file clearly in the response body
- keep file names and section order aligned with the response body
- when the mode includes multiple files, provide each file's full content in its own clearly labeled section
- if the user explicitly asks how to save the files locally, describe the file names and where the content belongs in plain language rather than generating executable commands

## Anti-copy rules
Do not simply restyle the reference.

The new campaign must change at least **2 of these 4 dimensions**:
1. campaign theme
2. reward design
3. task structure
4. module order or core interaction

Do not preserve all of the following at the same time:
- same hero structure
- same gameplay loop
- same reward chain

Call out the main changes briefly in the proposal.

## Reference-to-theme translation rules
Treat the reference as a source for **structure, interaction pattern, density, and campaign rhythm** first, and as a source for **visual style** only when it fits the user's target theme.

Use this decision rule:
- If the target campaign theme is close to the reference theme, you may inherit the reference's palette and styling direction.
- If the target campaign theme is different from the reference theme, keep the useful structure and interaction cues, but rebuild the visual style around the **target** theme.

When the target theme and reference theme conflict:
- prioritize the target festival, season, brand tone, and audience mood
- borrow layout logic, gameplay framing, and information hierarchy from the reference
- do not carry over mismatched seasonal colors or decorative symbols by default

Example:
- if the reference looks like a Spring Festival page with red and gold styling, but the new brief is for a Dragon Boat Festival campaign, do **not** keep the page red by default
- instead, keep the helpful campaign structure, then shift the visual direction toward Dragon Boat Festival cues such as bamboo green, jade green, lake blue, rice dumpling motifs, rope textures, water-wave shapes, or cooler early-summer contrast

## Confidence rules
Always separate content into these layers when relevant:
- **Observed**: directly visible from the reference
- **Inferred**: likely based on common campaign patterns
- **Assumed**: filled in because the reference is incomplete

If text is blurry or a state is hidden, say so directly.

## Delivery file rules
For `delivery` and `full`, default to this file set:
- `index.html`
- `styles.css`
- `main.js`
- `mock-data.js`

File responsibilities:
- `index.html`: page structure, visible module internals, decorative wrappers, and realistic placeholder copy
- `styles.css`: design tokens, background atmosphere, section chrome, CTA styling, popup styling, and responsive behavior
- `main.js`: render repeating data, event binding, state updates, popup control, and lightweight view-state changes
- `mock-data.js`: campaign meta, tasks, prizes, CTA text, popup data, and enough mock content to render a visually complete first screen

## Delivery schema guidance
Prefer a schema that covers both campaign config and page delivery contract.

Typical sections:
- `campaignMeta`
- `hero`
- `tasks`
- `rewards`
- `lottery`
- `modules`
- `popups`
- `stateMachine`
- `tracking`

## Important constraints
- Stay on H5/Web + HTML/CSS/JS only
- Never pretend uncertain text is exact
- Never invent backend endpoints
- Never claim pixel-perfect parity from a blurry image
- Favor reusable modules and editable data structures

## Visual fidelity rules
For `delivery` and `full`, default to a **high-fidelity visual draft**, not a low-fidelity wireframe.

Before writing code, extract the screenshot's likely visual language in 4 to 8 short bullets:
- palette and contrast style
- hero composition
- decoration density
- card or panel treatment
- CTA style
- icon/badge/tag style
- popup tone
- overall mood keywords

Then make the code reflect that visual language directly.

But do not follow the screenshot's visual language blindly.

Use this priority order for visual decisions:
1. explicit user brief and target campaign theme
2. target holiday/season/brand tone
3. reference layout and interaction cues
4. reference palette and decorative styling

If the reference palette conflicts with the new campaign brief, say so briefly and switch to a target-appropriate palette.
In that case, the visual extraction summary should separate:
- reusable structural cues from the reference
- replaced visual cues that should be rebuilt for the new theme

### HTML expectations
- Do not output only empty section containers.
- Include representative nested content for the hero, progress/task/reward modules, and popup shells.
- Use realistic wrappers such as badges, ribbons, tabs, stat chips, progress nodes, reward cards, glow layers, and floating ornaments when the reference implies them.
- Keep the structure editable, but visually expressive on first render.

### CSS expectations
- Start with `:root` tokens for major colors, gradients, shadows, radii, and spacing.
- Build atmosphere first: page background, hero backdrop, decorative light/shapes, panel chrome, and CTA emphasis.
- Prefer layered gradients, image-free ornaments, shadows, strokes, masks, and glow treatments over flat white cards.
- Style sections as distinct visual modules instead of repeating the same generic card everywhere.
- Include responsive handling for mobile-first rendering.

### JavaScript expectations
- Render repeated lists from data, but avoid reducing the whole page to blank placeholders.
- Support interactive states that help sell the concept visually, such as active tabs, selected rewards, progress states, countdown text, and popup opening.
- Keep interactions lightweight and front-end only unless the user provides real APIs.

### Mock data expectations
- Provide enough titles, subtitles, badges, numbers, and CTA text to make the page look complete.
- Use mock labels that match the proposed campaign tone instead of filler text.

## Delivery anti-patterns
Avoid these default outputs unless the user explicitly asks for minimal scaffolding:
- `Arial` plus gray background plus white rounded cards for every module
- repetitive `.section-card` wrappers with empty containers
- only one-line `<h1>` and `<p>` placeholders in the hero
- visually neutral buttons with no hierarchy
- a page that reads like a wireframe rather than a campaign landing page

## Example user requests
- “参考这几个活动页，给我出一个新的 H5 活动方案。”
- “根据这个参考图，先做玩法抽象，再给我页面架构。”
- “按这个活动参考，输出 HTML + CSS + JS 版本。”
- “我想同时要策划和代码，你走 full mode。”

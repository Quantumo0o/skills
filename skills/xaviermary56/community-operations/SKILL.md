---
name: community-operations
version: 1.0.0
description: Design and implement automatic community commenting workflows driven by existing site content, with optional support for automatic posting and multi-account execution. Use when building auto-comment systems that read comics, articles, novels, or videos from a database, generate natural-looking comments from that content, rotate across multiple accounts, schedule tasks, and optionally hand off generated comments to moderation before or after submission.
emoji: 💬
homepage: https://github.com/XavierMary56/OmniPublish
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Community Operations

## Overview

Use this skill to build or operate **content-driven automatic commenting systems**. The primary use case is: read existing site content from the database, generate comments that match the content type, assign those comments to one or more accounts, and publish them with scheduling, rate limits, and optional moderation handoff.

This skill can later expand into automatic posting, but the first priority is **automatic commenting based on existing content**.

## Core boundary

Keep responsibilities separate:

- **This skill owns**:
  - content selection for commenting
  - comment generation strategy
  - account rotation
  - scheduling and task orchestration
  - publishing execution
  - duplicate suppression
  - frequency control
  - operation logging

- **This skill does not own**:
  - moderation policy itself
  - ad/contact-risk rules
  - final moderation result semantics

If moderation is required, integrate a dedicated moderation skill or service such as `post-content-moderation`.

## First-priority capability

Prioritize this workflow first:

```text
existing content in database
→ extract content summary
→ generate comment candidates
→ choose account
→ optional moderation
→ submit comment
→ log result
```

Target content sources include:
- comics
- articles
- novels
- videos

## Content-driven automatic commenting

### Supported source types

Build a unified comment-input structure even if the original tables differ.

Recommended normalized fields:
- `content_type`
- `content_id`
- `title`
- `summary`
- `author`
- `tags`
- `category_id`
- `topic_id`
- `published_at`
- `extra`

Example:

```json
{
  "content_type": "comic",
  "content_id": 123,
  "title": "标题",
  "summary": "摘要",
  "author": "作者",
  "tags": ["热血", "校园"],
  "extra": {}
}
```

## Comment generation rules

Do not use one generic template for every content type. Generate comments differently based on the source.

### Comics

Prefer comments about:
- art style
- character appeal
- plot progression
- update expectations
- favorite scenes

### Articles

Prefer comments about:
- viewpoint response
- agreement/disagreement
- practical reflection
- follow-up questions
- short discussion prompts

### Novels

Prefer comments about:
- writing style
- pacing
- plot setup
- character development
- expectation for later chapters

### Videos

Prefer comments about:
- pacing
- scene quality
- plot reaction
- rewatch value
- performance or presentation

## Comment style strategy

Generate multiple styles instead of repeating one voice.

Recommended style buckets:
- praise / appreciation
- discussion / opinion
- expectation / follow-up
- question / interaction
- light emotional reaction

Avoid repetitive low-quality outputs like:
- `不错啊`
- `写得真好`
- `支持一下`
- `期待更新`

Those can appear occasionally, but should not dominate the comment pool.

## Comment targeting workflow

When asked to build the system, follow this order:

### Step 1. Identify content sources

Clarify:
- which tables or models provide comics, articles, novels, and videos
- which fields are available for summarization
- whether comments target only published content
- whether comments should exclude very old content or low-quality content

### Step 2. Build a normalized content extractor

Create a common extraction layer that maps different content models into one unified comment input object.

### Step 3. Design comment generation

Define:
- generation prompt or template policy
- content-type-specific styles
- duplicate suppression rules
- per-content comment count limits
- unsafe phrase blacklist
- optional moderation checkpoint

### Step 4. Design account strategy

Define:
- account pool source
- account roles
- per-account comment quota
- cooldown period
- account disable conditions
- fallback account selection

### Step 5. Design execution path

Use this chain:

```text
select target content
→ build normalized content input
→ generate comment candidates
→ filter / deduplicate
→ optional moderation
→ choose account
→ submit comment
→ log result
→ retry or cooldown
```

### Step 6. Add controls

Always add:
- idempotency keys
- timeout handling
- retry limits
- duplicate-comment suppression
- per-account frequency caps
- per-content comment caps
- audit logging
- manual disable switch

## Multi-account rules

If multiple accounts are used, always define:
- account id
- account status
- role
- last action time
- cooldown_until
- daily quota
- hourly quota
- failure count

Do not design a system where all accounts can comment indefinitely with no rotation or no cooldown.

## Anti-duplication rules

Always prevent:
- same account posting the same comment repeatedly
- many accounts posting nearly identical comments in a short window
- too many comments on the same content in a short period
- same template being used on multiple content items without variation

Recommended controls:
- similarity threshold checks
- comment hash / normalized hash
- per-content cooloff window
- random delay window
- template variation rules

## Moderation handoff guidance

If generated comments must be checked, choose one mode:

### Mode A. Review before submit
Use when generated comments must not enter the system unless clean.

### Mode B. Submit then audit
Use when the project already supports post-save review states.

### Mode C. Hybrid
Use when comments get basic local filtering before submit and full moderation after submit.

Do not merge moderation policy directly into this skill. Keep moderation as a dependency.

## Logging requirements

At minimum, log:
- task id
- content_type
- content_id
- account id
- generated comment
- generation strategy or style bucket
- moderation mode used
- execution result
- failure reason
- created_at / updated_at

## Future expansion

This skill may later expand to:
- automatic posting
- posting + commenting orchestration
- campaign scheduling
- multi-account publishing waves

But first build **automatic commenting based on existing content** well.

## Recommended reusable resources

### references/
Store:
- content-extractor template
- comment-style matrix
- account rotation template
- queue design template
- rollout checklist
- project-specific schema plans such as `references/51dm-auto-comment-schema-plan.md`
- project-specific implementation plans such as `references/51dm-auto-comment-implementation-v1.md`
- project-specific task breakdowns such as `references/51dm-auto-comment-task-breakdown-v1.md`
- project-specific reuse plans such as `references/51dm-comment-reuse-plan.md`
- human-like comment guidance such as `references/human-like-comment-strategy.md`

### scripts/
Store:
- sample comment generator
- comment signature examples if needed
- scheduler/runner examples
- account rotation pseudocode

## Default recommendation

For the first version, build only these:
- content extractor
- comment generator
- account selector
- comment submitter
- moderation handoff adapter
- operation logger

Do not start with full posting automation unless the user explicitly prioritizes it.

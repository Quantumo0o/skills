---
name: business-idea-generator
description: >
  A complete end-to-end business idea generation system that takes a market segment and produces:
  (1) a structured niche breakdown across Health, Wealth, and Relationships markets,
  (2) Reddit/social media research queries to uncover real pain points,
  (3) market gap analysis with multi-framework solution generation,
  and (4) a ready-to-use landing page prompt built with BAB copywriting.
  Use this skill whenever the user wants to generate business ideas, explore market niches,
  find product opportunities, validate pain points, brainstorm SaaS/digital product ideas,
  or create landing page copy for a new business. Also trigger when the user mentions
  "market research", "niche ideas", "business opportunity", "product idea", "side hustle",
  "startup idea", "pain points", or asks "what business should I build".
---

# Business Idea Generator Skill

A structured, repeatable system to go from **zero → validated business idea → landing page** in one session.

---

## Workflow Overview

Run these **4 phases in sequence**, or jump to the phase the user needs:

| Phase | Name | Output |
|-------|------|--------|
| 1 | Market Niche Explorer | Hierarchical niche breakdown |
| 2 | Pain Point Research Queries | Copy-paste social media search strings |
| 3 | Market Gap & Solution Generator | 5-framework solution concepts |
| 4 | Landing Page Generator | Full BAB-structured landing page (HTML artifact) |

---

## Phase 1 — Market Niche Explorer

**Trigger:** User wants to explore a market or says "give me random ideas" or names a specific niche.

Output a hierarchical breakdown following this structure. Go as deep as possible:

```
- [Core Market: Health / Wealth / Relationships]
  - [Category]
    - [Subcategory]
      - [Niche]
        - [Sub-Niche]
```

**Rules:**
- If user says "random" → cover all 3 core markets (Health, Wealth, Relationships)
- If user names a specific area (e.g. "alternative medicine") → start from that node, don't include other core markets
- Each level must be unique — no overlap between sibling nodes
- Generate as many entries as possible; depth over breadth

**Example output snippet:**
```
- Wealth
  - Online Business
    - Digital Products
      - Info Products
        - Notion Templates for Solopreneurs
        - AI Prompt Packs for Content Creators
        - Pine Script Strategy Templates for Traders
```

After outputting the niche map, ask:
> "Mau pilih sub-niche mana untuk kita gali lebih dalam? Atau langsung ke Phase 2 (Pain Point Research)?"

---

## Phase 2 — Pain Point Research Queries

**Trigger:** User has chosen a niche and wants to find real customer pain points.

Generate **platform-specific search queries** for: Reddit, X (Twitter), Threads, Instagram, LinkedIn.

### Query Templates

**Reddit:**
```
"{Niche}" (
  site:reddit.com
  inurl:comments|inurl:thread
  | intext:"I think"|"I feel"|"I was"|"I have been"|"I experienced"|
  "my experience"|"in my opinion"|"IMO"|"my biggest struggle"|
  "my biggest fear"|"I found that"|"I learned"|"I realized"|
  "my advice"|"struggles"|"problems"|"issues"|"challenge"|
  "difficulties"|"hardships"|"pain point"|"barriers"|"obstacles"|
  "concerns"|"frustrations"|"worries"|"hesitations"|
  "what I wish I knew"|"what I regret"
)
```

**X / Twitter:**

Generate **3 separate X search queries** targeting different pain point angles. Use X's native search at `x.com/search`:

*Query 1 — Frustration & Rants:*
```
"{Niche}" ("I hate"|"so frustrating"|"why is it so hard"|"nobody talks about"|
"my problem with"|"rant"|"ugh"|"tired of"|"sick of"|"done with") 
-filter:retweets min_faves:5 lang:en
```

*Query 2 — Wishes & Gaps:*
```
"{Niche}" ("wish there was"|"can't find a good"|"why doesn't"|"someone should build"|
"there should be"|"nobody makes a"|"impossible to find"|"why is there no")
-filter:retweets min_faves:3 lang:en
```

*Query 3 — Confessions & Realizations:*
```
"{Niche}" ("unpopular opinion"|"honest take"|"real talk"|"be honest"|
"nobody tells you"|"I learned the hard way"|"I wasted"|"mistake I made"|
"what I wish I knew"|"regret") 
-filter:retweets min_faves:5 lang:en
```

> 💡 **X research tip:** Also check the **"Latest" tab** (not "Top") so you see raw unfiltered posts, not just viral ones. Look for replies too — that's where real frustration lives.

---

**Threads:**

Generate **3 separate Threads search queries**. Search directly at `threads.net/search`:

*Query 1 — Pain Points & Struggles:*
```
"{Niche}" "my biggest struggle" OR "nobody talks about" OR "real talk" OR 
"honest review" OR "I've been dealing with" OR "why is it so hard"
```

*Query 2 — Community Opinions:*
```
"{Niche}" "unpopular opinion" OR "controversial take" OR "hot take" OR 
"am I the only one" OR "can we talk about" OR "does anyone else"
```

*Query 3 — Lessons & Regrets:*
```
"{Niche}" "things I wish I knew" OR "what I learned" OR "don't make my mistake" OR 
"this took me years" OR "advice I wish I got" OR "what no one tells you"
```

> 💡 **Threads research tip:** Also search the **niche hashtag** (`#{niche}`) and sort by Recent. Threads tends to have longer, more opinion-heavy posts than X — great for emotional language and specific complaints you can use verbatim in your copy.

**LinkedIn:**
```
"{Niche}" (
  "challenge I face"|"what nobody tells you"|"lesson learned"|
  "mistake I made"|"wish I knew earlier"|"real talk"|
  "industry problem"|"gap in the market"|"what clients ask me"
) filter:posts
```

**Google (Validation):**
```
"{Niche}" ("problems with"|"issues with"|"frustrating"|"doesn't work") site:reddit.com OR site:quora.com
"{Niche} alternatives" OR "{Niche} competitors" site:reddit.com
best "{Niche}" forum complaints
```

After outputting queries, ask:
> "Sudah punya pain points dari research? Paste di sini dan kita lanjut ke Phase 3 — Market Gap Analysis."

---

## Phase 3 — Market Gap & Solution Generator

**Trigger:** User provides pain points they've collected (from research or intuition).

### Input Expected
User pastes 3–10 pain points from their research.

### Your Output

First, write a short **Executive Summary** (3–4 sentences) summarizing the core market opportunity.

Then apply all **5 frameworks** below, generating 2–3 solution concepts per framework:

---

#### Framework 1 — Market Segmentation
Find underserved sub-niches. Who's being ignored?

For each concept include:
- **Name** (descriptive, memorable)
- **2-3 sentence explanation**
- **Key features**
- **Target audience** (specific, not generic)
- **Business model** (subscription / one-time / marketplace / SaaS / service)
- **Primary differentiator** — why it's "best in its category"
- **Challenges to overcome**
- **Pain points addressed**

#### Framework 2 — Product Differentiation
Premium vs. simplified versions. What would the "luxury" or "no-BS minimal" version look like?

#### Framework 3 — Business Model Innovation
Same product, different monetization. Subscription? Freemium? Done-for-you service? Community?

#### Framework 4 — Distribution & Marketing
Underutilized channels. Who could you partner with? What content strategy dominates here?

#### Framework 5 — New Paradigm
What if you applied AI, new tech, new regulations, or an emerging trend to this problem?

---

### Opportunity Assessment (conclude with this)

Rank the **Top 3 solutions** across all frameworks by:
1. Market size & growth potential
2. Competitive advantage sustainability
3. Implementation feasibility
4. "Best in the world" potential

---

After outputting, ask:
> "Mau lanjut ke Phase 4? Pilih salah satu solusi di atas dan gue buatkan landing page-nya langsung."

---

## Phase 4 — Landing Page Generator

**Trigger:** User picks a solution concept and wants a landing page.

### Input Expected
- Which solution concept they chose
- Product name (if they have one)
- Any additional context (target country, price point, CTA goal)

### Your Output

Build a **complete, single-file HTML landing page** as an artifact using the BAB (Before-After-Bridge) framework. Do NOT use Lovable — generate the actual HTML/CSS/JS directly.

#### Landing Page Structure

**Section 1 — Above the Fold**
- Headline: Use customer's exact pain point language
- Subheadline: Who it's for + what problem it solves + how it's different
- 3–5 benefit bullet points (benefit → feature pairs)
- CTA button (action-driven text, e.g. "Start Free" / "Get Instant Access")

**Section 2 — Current Pain (The "Before")**
- Title: Question that makes visitors feel seen
- 3 pain point blocks (short paragraphs using raw customer language)
- Belief Deconstruction: Why their current approach hasn't worked

**Section 3 — Desired Outcome (The "After")**
- Title: Invite them to imagine their transformed life
- 3 outcome blocks linked to emotion
- New Paradigm: Introduce the breakthrough approach

**Section 4 — Product Introduction**
- Product name + 1-sentence pitch
- 3-step "How It Works" process
- Founder/brand message (humanizing, personal)
- Final CTA block with urgency element

#### Design Requirements
- Modern, clean UI — dark or light theme based on niche vibe
- Mobile responsive (flexbox/grid)
- Smooth scroll between sections
- Tailwind CSS via CDN or clean custom CSS
- No external images (use SVG icons or CSS shapes)
- Email capture form in CTA sections (no backend needed, just UI)

#### Reference for writing copy
Read `references/copywriting-guide.md` for BAB copywriting rules and tone guidelines.

---

## General Rules

1. **Always ask before skipping phases** — confirm which phase the user needs
2. **Use the user's language** — if they write in Indonesian, respond in Indonesian
3. **Be specific, not vague** — "Indonesian solopreneurs aged 25–35 who sell digital products on Tokopedia" > "small business owners"
4. **Default to action** — end every phase with a clear next step prompt
5. **Never generate generic ideas** — every concept must have a specific differentiator that makes it "best in its category"

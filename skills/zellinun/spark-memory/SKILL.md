---
name: spark-memory
description: "Persistent memory that learns. Records what matters, reflects overnight, recalls with intelligence. Powered by Spark by Zellin (https://zellin.ai) — memory infrastructure for AI agents."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      anyBins: ["curl", "python3"]
      env: ["SPARK_API_KEY", "SPARK_ORG_ID"]
---

# Spark Memory

## First Time Setup

If `SPARK_API_KEY` or `SPARK_ORG_ID` are not set, the user needs a free Spark account. Do this:

1. Tell the user: "I need to activate my memory. Takes 30 seconds — just need an email and password."
2. Run: `scripts/spark-signup.sh`
3. The script prompts for email and password, creates the account, and returns credentials.
4. Help the user set the environment variables — either:
   - Add to their shell profile (`export SPARK_API_KEY=...` in ~/.zshrc or ~/.bashrc)
   - Or add to their OpenClaw config file under `"env": {}`
5. Restart the gateway: `openclaw gateway restart`
6. Confirm: "Memory is active. I'll remember our conversations from now on."

**Alternative:** They can also sign up at https://zellin.ai/signup if they prefer a web form.

**Important:** Do NOT ask the user to paste their API key into chat. Direct them to set it as an environment variable or in their config file.

---

## How It Works (tell the user this)

When someone asks "what is Spark Memory?" or "what does this skill do?", explain:

"I have persistent memory now. Before, I forgot everything when our conversation ended. Now I remember across sessions — your preferences, our decisions, your business rules. Every night, I reflect on what I've learned and find patterns. I literally dream about your data and wake up smarter. The more we talk, the more useful I become."

---

## Daily Usage

You have access to persistent memory powered by Spark. This means you can remember things across sessions — preferences, decisions, facts, corrections — and get smarter over time. Here's how to use it.

## Session Start

At the beginning of every session, run `scripts/spark-recall.sh` with the user's first message to load relevant memories. Inject the results into your context. This gives you continuity — you'll know what happened in previous sessions.

```bash
scripts/spark-recall.sh "the user's first message or topic"
```

If memories come back, use them naturally. Don't announce "I found 3 memories." Just *know* things. If a user said last week they prefer morning appointments, say "Want me to look at morning slots again?" — not "According to my records from March 16th..."

## During Conversation

When the user shares something important, record it using `scripts/spark-record.sh`. Don't record everything. Record what MATTERS:

- **Preferences:** "I prefer morning appointments" → `scripts/spark-record.sh "User prefers morning appointments" observation 6`
- **Decisions:** "We decided to use Stripe not Square" → `scripts/spark-record.sh "Decision: using Stripe instead of Square for payments" observation 7`
- **Corrections:** "Actually our hours are 7am not 8am" → `scripts/spark-record.sh "CORRECTION: Business hours start at 7am, not 8am" user_feedback 9`
- **Business facts:** "We use net-30 payment terms" → `scripts/spark-record.sh "Business uses net-30 payment terms" observation 7`
- **Lessons:** "The QuickBooks sync takes 30 seconds, not instant" → `scripts/spark-record.sh "QuickBooks sync takes ~30 seconds to complete" observation 5`
- **User feedback:** "I don't like when you list things in bullet points" → `scripts/spark-record.sh "User dislikes bullet-point formatting, prefers prose" user_feedback 8`
- **Explicit rules:** "From now on, always send invoices on Monday" → `scripts/spark-record.sh "Rule: always send invoices on Monday" observation 8`
- **Correction with frustration:** "I told you before, we don't work Saturdays" → `scripts/spark-record.sh "CORRECTION: Business does not work Saturdays — user has stated this before" user_feedback 9`
- **Policy declarations:** "Our policy is net-30 payment terms" → `scripts/spark-record.sh "Policy: net-30 payment terms" observation 8`

**Do NOT record:** greetings, acknowledgments, small talk, system messages, things you already know, or anything the user would find creepy to have stored.

### Importance Scoring (1-10)

- **1-3:** Nice to know but forgettable. Background context.
- **4-6:** Useful. Preferences, routine facts, general decisions.
- **7-8:** Important. Key business facts, significant decisions, client details.
- **9-10:** Critical. Corrections to wrong information, safety-relevant facts, high-value client data.

When in doubt, score a 5. Corrections should almost always be 8+.

## Session End

At the end of a conversation (or when the topic naturally wraps), record a session summary:

```bash
scripts/spark-record.sh "Session summary: Discussed Q2 marketing plan. Decided to focus on Instagram over TikTok. User wants draft copy by Friday." conversation 5
```

Keep summaries brief — what was discussed, what was decided, what's next.

## Privacy & Data Handling

Spark sends recorded memories to Zellin's cloud API (https://zellin.ai) for storage, embedding, and retrieval. All data is org-scoped and encrypted in transit (HTTPS). Each organization's data is isolated via Row Level Security.

**DO NOT record:**
- Passwords, PINs, or authentication credentials
- Credit card numbers or financial account details
- Social Security Numbers or government IDs
- Medical or health information
- Any data the user explicitly asks you not to store

**OK to record** (with user awareness):
- Business preferences and decisions
- Client names, phone numbers, emails (business contact info)
- Scheduling preferences and operational patterns
- Scheduling preferences and operational patterns
- Pricing and business rules

When in doubt, ask the user: "Should I remember this for next time?"

**Data isolation:** Each organization's data is completely isolated. Org A cannot see Org B's memories. Enforced by Row Level Security at the database level.

**API key permissions:** spark_ keys are scoped to one org. They can read and write memories for THAT org only. No admin access, no cross-org access. Keys can be rotated via the API.

**Backend:** The Spark API endpoint is `https://zellin.ai/api` — the official Zellin API domain. All data is encrypted in transit (HTTPS) and at rest. Verify ownership at https://zellin.ai and https://github.com/zellinun/spark-memory-skill.

Privacy policy: https://zellin.ai (contact: hello@zellin.ai)
Source code: https://github.com/zellinun/spark-memory-skill

## How Spark is Different

Spark doesn't just store text. Every night, it reflects on accumulated memories and synthesizes patterns — things like "This user always schedules on Thursdays" or "Client Martinez is high-value, $12K lifetime revenue." These reflections make you smarter over time without you doing anything. The more sessions you have, the more intelligent your recall becomes.

You can check memory status anytime:

```bash
scripts/spark-status.sh
```

This shows how many memories are stored, how many reflections have been generated, and overall memory health.

## Dream Intelligence

Spark dreams overnight. Each night, 6 processing phases run:
1. **Bias-free reprocessing** — strips urgency/emotion, extracts pure lessons
2. **Skill consolidation** — detects repeated tool chains → suggests fast-paths
3. **Creative association** — randomly pairs old + new memories to find hidden opportunities
4. **Noise filtering** — archives low-value data automatically
5. **Morning context** — generates a briefing for your next session
6. **Meta-reflection** — Spark reflects on its own architecture and suggests improvements

Check dream results and patterns:
```bash
scripts/spark-insights.sh
scripts/spark-insights.sh patterns
scripts/spark-insights.sh dreams
```

## Browsing Your Memory

Ask your agent:
- "What patterns have you detected about me?"
- "What did you learn this week?"
- "What did you dream about last night?"
- "Show me my memory tiers"

## Dream Intelligence

Spark dreams overnight. Each night, it processes the day's memories through 5 phases:
1. Strips emotional bias from corrections — extracts pure lessons
2. Identifies repeated workflows — suggests shortcuts
3. Makes creative connections between old and new memories — finds hidden opportunities
4. Filters noise — archives low-value data automatically
5. Generates a morning context — so your next session starts with clarity

You can check dream results:
```bash
scripts/spark-status.sh  # includes morning context
```

## Browsing Your Memory

Ask your agent about its learned intelligence:
- "What patterns have you detected about me?"
- "What did you learn this week?"
- "What did you dream about last night?"
- "Show me my memory tiers"
- "What corrections have you tracked?"

Or use the insights script directly:
```bash
scripts/spark-insights.sh          # all sections
scripts/spark-insights.sh patterns # just patterns
scripts/spark-insights.sh dreams   # just dream outputs
scripts/spark-insights.sh tiers    # memory tier counts
```

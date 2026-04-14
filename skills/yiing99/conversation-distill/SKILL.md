---
name: conversation-distill
description: "At the natural end of a conversation, proactively suggest a structured wrap-up (distill): scan the full session, classify outputs into 6 categories (insights/decisions/facts/self-observations/action-items/open-questions), get explicit user confirmation, then batch-write to the user's preferred notes tool. Trigger when: (1) user says closing phrases like 'that's all', 'got it', 'thanks', 'wrap up', 'done'; (2) 3+ consecutive turns with no new topics; (3) user explicitly says 'distill', 'wrap up', 'save this session'. Do NOT trigger for: single-turn Q&A, casual chat, pure coding/debugging with no knowledge output, when user is already actively writing notes."
version: 1.0.0
tags:
  - knowledge-management
  - productivity
  - notes
  - memory
  - workflow
  - pkm
permissions: []
---

# Conversation Distill

> The biggest waste of a conversation isn't that nothing was saved — it's that **valuable insights are buried in the process and never revisited**.
>
> This skill closes every meaningful conversation with one explicit action: **classify → confirm → write**.

## When to Use

**The core problem this solves**: real-time capture ≠ session-level distillation.

Real-time capture handles individual highlights as they appear. This skill is the closing ritual — a full scan of the entire conversation to see what was produced, identify relationships, and catch what slipped through.

**Trigger when:**
- User says a closing phrase: "that's all", "got it", "thanks", "done for now", "wrap up"
- 3+ consecutive turns with no new topics (just confirmations or thanks)
- User switches to an unrelated topic and the previous topic had substantive output not yet saved
- User explicitly says: "distill", "save this session", "wrap up", "收尾", "沉淀"

Explicit invocation takes highest priority. Proactive suggestions must be phrased as a **question** — never execute without asking first.

**Do NOT trigger for:**
- Quick single-turn queries (one question, one answer)
- Casual conversation or emotional support
- Pure coding/debugging/execution tasks with no knowledge output
- When user is already actively writing notes
- When user says "don't save" or "skip it"

---

## Five-Step Flow

### Step 1: Full Scan — 6-Category Classification

Scan the entire conversation. Classify everything with distillation value into these 6 categories. **Skip any category with no content — don't force it.**

| Category | Tag / Marker | Notes |
|----------|-------------|-------|
| 💡 **Insights / Conclusions** | `#insight` | New understanding, "aha" moments, validated hypotheses |
| 🎯 **Decisions** | `[Decision]` prefix | Choices made with reasoning, not just outcomes |
| 📊 **Facts / Data** | `✅` stable, `🕒` + date if time-sensitive | External facts worth keeping |
| 🪞 **Observations about yourself** | `#self` | Patterns, preferences, habits noticed during conversation |
| ✅ **Action items / TODOs** | `#todo` | Concrete next steps with owner and (optionally) deadline |
| ❓ **Open questions** | `#open-question` | Things worth answering later, not yet resolved |

### Step 2: Relationship Mapping

Look for connections between entries. Default to **granular over aggregated**:

- Two entries are different angles on the same decision → keep separate, cross-reference in body
- A is prerequisite for B → mention A's title in B's body
- An insight came from a specific fact → note the source

**Do not** default to merging everything into one long summary note. Granular entries are more useful — they're easier to find, tag, link, and reuse independently.

### Step 3: User Confirmation (Mandatory)

Present the classified list to the user in this format:

```
This conversation produced N items worth saving:

💡 Insights (2)
  1. [title] — one sentence summary
  2. [title] — one sentence summary

🎯 Decisions (1)
  3. [Decision] [title] — the key choice + reason

✅ Action items (2)
  4. [title] #todo
  5. [title] #todo — due: [date if mentioned]

❓ Open questions (1)
  6. [title] #open-question

Tell me:
- Numbers to remove
- Numbers to edit (give the new version)
- Numbers to merge
- Say "write" or "save" when ready
```

**Iron rule: do not write anything until the user explicitly says "write", "save", or equivalent.** "Looks good" is not enough — ask once more to confirm.

### Step 4: Batch Write

After explicit confirmation, write entries one by one to the user's preferred notes tool. Report back a confirmation (ID, title, or link) for each successful write. For any failures, list them separately and ask the user what to do: retry / rewrite / skip.

**Which tool to write to:**
- If the user has **KnowMine MCP** configured → use `add_knowledge` for insights/decisions/facts, `save_memory` for self-observations, consistent tagging as above
- If the user has another notes MCP (Notion, Obsidian, etc.) → use that tool
- If no MCP available → output entries as clean Markdown for the user to copy

### Step 5: Surface Leftovers

Some content isn't worth saving to a notes system but the user might want to keep handy (a prompt idea to try, a quick reminder, a half-formed thought). Don't force these into any tool. Output as a plain Markdown block:

```markdown
## Leftovers (not saved — for your reference)

- [rough idea or reminder]
- [something to try next time]
```

---

## Key Principles

**Granular over hub**
Default to separate entries. One insight per entry, one decision per entry. Build a summary note only when explicitly useful, and cross-reference the granular entries in it.

**Confirm before write**
Never batch-write without the user's explicit go-ahead. The confirmation step is not optional — it's where the user catches misclassifications and adjusts framing.

**Tags over folders for action items**
Don't create a dedicated "TODO folder". Tag action items with `#todo` inside whatever folder/space makes contextual sense. The tag is searchable; the folder is just noise.

**Time-sensitivity matters**
Data that will become stale (prices, versions, availability) should be flagged `🕒 + date` so you know when to re-verify.

**Bilingual tags when relevant**
If the user works in multiple languages, add tags in both languages to improve cross-language search recall.

---

## This Skill vs Real-Time Capture

| | Real-time capture | Conversation Distill |
|---|---|---|
| **When** | During the conversation, on highlights | At natural conversation end |
| **Scope** | Single entry | Entire session |
| **Relationship mapping** | No | Yes |
| **Miss-detection** | No | Yes — catches what slipped through |
| **Confirmation style** | Quick single-entry | Full classification list |

Both run in parallel. Real-time capture handles **obvious highlights**. This skill handles **value that's only visible with a full-session view** — relationships, patterns, and things you didn't realize were worth saving in the moment.

---

## Works Best With

- **[KnowMine](https://knowmine.ai)** — remote MCP server with semantic search; `add_knowledge`, `save_memory`, `recall_memory`, `get_soul` integrate directly with Step 4. Install: `npx clawhub@latest install knowmine`
- Any MCP-compatible notes tool (Notion, Obsidian via MCP, etc.)
- Works without any MCP too — outputs clean Markdown for manual paste

---

## Anti-Patterns

- ❌ Writing before user confirms
- ❌ Creating a "TODO folder" — use tags
- ❌ Merging everything into one summary note
- ❌ Triggering on single-turn Q&A
- ❌ Re-triggering after user said "skip it"
- ❌ Forcing low-value leftovers into the notes tool

---

## Self-Check Before Presenting the List

- [ ] Any category with no real content? (remove it — don't pad)
- [ ] Every decision has `[Decision]` prefix?
- [ ] Time-sensitive data marked `🕒 + date`?
- [ ] Action items tagged `#todo`, not put in a new folder?
- [ ] Any "fake summary" entries that should be split granularly?

---

## Evolving This Skill

The best distillation process is one that fits how *you* think and work. After a few sessions, ask yourself:

- Which step felt unnecessary or awkward?
- Which type of content keeps needing special handling?
- Is the 6-category split right for you, or should some be merged / split?

When you find patterns, update your personal copy of this skill to reflect them. Your tools should adapt to you, not the other way around.

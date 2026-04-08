# Example: Pre-Task Checklist in Action

## Scenario: Writing MBD Article

### Wrong Approach (Without Checklist)
```
User: Write an MBD article about SmartShift

Agent: Sure! Let me write an 8,000-word academic whitepaper...
[30 minutes later]
Agent: Done! Here's your 8,000-word whitepaper.

User: That's wrong. MBD articles are 4,000 words, conversational style.

Agent: Oh, I didn't know. Let me rewrite...
[Another 30 minutes wasted]
```

### Right Approach (With Checklist)
```
User: Write an MBD article about SmartShift

Agent: Let me run the pre-task checklist first...

1. Search memory for "MBD article format"
   → Found: 3,000-4,500 words, conversational tone
   → Found: Category rotation (AI/LLM, Blockchain, etc.)
   → Found: Reference example: 懒人理财经

2. Read reference file
   → /tmp/mbd-book-ideas/2026-03-11_懒人理财经_AI替你管钱躺赚不是梦/文章.md
   → Style: Conversational, story-driven, practical
   → Structure: 10 chapters, catchy opener, actionable content

3. Verify critical details
   → Category: 智能家居/AI (SmartShift fits here)
   → Price: ¥19.9 (standard)
   → Folder: YYYY-MM-DD_中文标题_英文副标题/

4. Check rules
   → AGENTS.md: "MbD publish gate - NEVER publish without explicit approval"
   → SOUL.md: "No pause rule - execute immediately"

✅ Checklist complete. Proceeding with verified context.

[15 minutes later]
Agent: Done! 4,000-word conversational article, following MBD format exactly.

User: Perfect! Published immediately.
```

## Time Comparison

- **Without checklist**: 60 minutes (30 min wrong work + 30 min rework)
- **With checklist**: 20 minutes (5 min verify + 15 min work)

**Saved**: 40 minutes, better quality, no frustration.

## Key Takeaways

1. **2 minutes of verification saves 20 minutes of fixing**
2. **Reference examples are better than assumptions**
3. **Rules change - always check current versions**
4. **Build checklist into your workflow, not an afterthought**

## Checklist Template

Copy this for every task:

```bash
# 1. Search memory
memory_search "task type format"

# 2. Read reference
cat /path/to/example.md

# 3. Verify details
cat ~/.openclaw/workspace/TOOLS.md | grep "relevant detail"

# 4. Check rules
cat ~/.openclaw/workspace/AGENTS.md | grep "relevant rule"

# 5. Proceed with verified context
```

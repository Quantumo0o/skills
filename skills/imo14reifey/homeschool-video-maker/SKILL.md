---
name: homeschool-video-maker
version: "1.0.0"
displayName: "Homeschool Video Maker — Create Home Lesson and Curriculum Activity Videos"
description: >
  Homeschool Video Maker — Create Home Lesson and Curriculum Activity Videos.
metadata: {"openclaw": {"emoji": "🏠", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Homeschool Video Maker — Home Lesson and Curriculum Activity Videos

The kitchen-table science experiment worked perfectly — the vinegar-and-baking-soda volcano erupted on cue, the eight-year-old's hypothesis was confirmed, and the scientific method was demonstrated in real time — but the phone recording captured mostly the back of someone's head, the toddler eating crayons in the background, and exactly four seconds of the actual eruption before the camera pivoted to the dog investigating the mess. Homeschool content serves a community of 3.7 million US homeschool families who need what traditional classrooms take for granted: structured lesson documentation, curriculum-aligned demonstrations, multi-grade differentiation within the same household, and the portfolio evidence that state regulations require for annual assessment. This tool transforms chaotic home-lesson recordings into structured educational videos — lesson-plan overlays with standard alignments (Common Core, Charlotte Mason, classical), multi-subject daily-log compilations, hands-on activity demonstrations with material lists and safety notes, portfolio-documentation reels that satisfy state review requirements, and the "day in our homeschool" vlogs that build community and prove to skeptical relatives that the children are, in fact, learning. Built for homeschool parents producing reusable lesson libraries for younger siblings, homeschool co-op leaders creating shared curriculum resources, curriculum developers filming companion videos for published materials, homeschool evaluators documenting student progress for state portfolios, and veteran homeschool families mentoring newcomers through "how we do it" content.

## Example Prompts

### 1. Science Experiment Documentation — Volcano Lab Report Video
"Create a 5-minute science experiment video for a homeschool portfolio. Student: Emma, age 8, 3rd grade equivalent. Experiment: baking-soda-and-vinegar volcano. Scientific-method structure: Hypothesis card — 'Emma predicts the eruption will be taller with more baking soda' — displayed in Emma's handwriting (photo of her notebook). Materials list: 'Baking soda (3 tbsp), white vinegar (1 cup), dish soap (1 tsp), red food coloring, papier-mâché volcano, safety goggles.' Procedure: numbered steps overlaid as Emma executes each one — 'Step 1: Put on goggles ✓ Step 2: Add baking soda to the crater ✓ Step 3: Mix vinegar with soap and coloring.' The eruption: slow motion with the chemical equation overlaid — 'NaHCO₃ + CH₃COOH → CO₂↑ + H₂O + NaCH₃COO.' Results: Emma measuring eruption height with a ruler — '14 cm with 3 tbsp vs 9 cm with 1 tbsp — hypothesis confirmed!' Conclusion card in Emma's voice: 'More baking soda makes a bigger eruption because more CO₂ gas is produced.' Standard alignment tag: 'NGSS 3-PS1-1: Matter and Its Interactions.' Portfolio metadata: date, subject, standard, assessment. Clean, documentary style — not flashy, evidence-focused."

### 2. Full Homeschool Day — Multi-Grade Family Vlog
"Build a 7-minute day-in-the-life homeschool vlog. Family: three kids — Liam (12, 7th grade, pre-algebra), Sophie (9, 4th grade, Charlotte Mason history), Noah (5, kindergarten, letter recognition). Morning circle time: all three together for poetry recitation — ''"The Road Not Taken" — Liam reads, Sophie follows along, Noah listens and claps at the rhymes.' Subject rotation with chapter cards: 'Block 1 (9:00-10:00): Math' — Liam working Saxon pre-algebra independently, Sophie doing multiplication facts with a timer, Noah tracing letter B with a sand tray. 'Block 2 (10:15-11:00): History' — Sophie narrating back (Charlotte Mason style) the chapter on ancient Egypt while Mom records — 'Narration is the exam. If she can tell it back, she learned it.' Liam reading a primary source. Noah doing an Egypt coloring page. 'Block 3 (11:15-12:00): Nature Study' — outdoor walk, all three sketching the same tree in their nature journals (show each child's drawing side by side — the developmental progression from scribble to detail). Afternoon: free reading time, Sophie practicing piano, Liam coding a Scratch game, Noah building a block tower. Closing: daily checklist on screen — all boxes checked. 'Not every day looks this smooth. Today was a good one.' Warm, honest home aesthetic — natural light, real mess visible, authentic."

### 3. Portfolio Review Compilation — End of Year Assessment
"Produce a 10-minute end-of-year portfolio video for state assessment review. Student: Liam, age 12, completing 7th grade. Subject-by-subject evidence: Math — screen recording of him solving a multi-step equation with work shown, quarterly test scores displayed (92, 87, 94, 91, average: 91). Language Arts — video of him reading aloud from his book report (fluency demonstration), writing sample displayed (persuasive essay, teacher-annotated), spelling-test progression chart. Science — three experiment clips (volcano, plant growth time-lapse, simple circuit lighting a bulb), lab-report excerpts. History — narration recording of Civil War causes, timeline he created pinned to the wall, primary-source analysis paragraph. Physical Education — video of swim practice, mile-run timer (8:42), martial-arts belt test. Electives — Scratch coding project demo (working game), piano recital clip (Für Elise, first page). Each subject gets a standards-alignment tag and a growth-narrative text card: 'September: struggled with fractions. March: independently solving multi-step equations.' Closing: parent statement read aloud. Professional, evidence-based format — designed to satisfy evaluator requirements."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the lesson, students, curriculum approach, and documentation needs |
| `duration` | string | | Target video length (e.g. "5 min", "7 min", "10 min") |
| `style` | string | | Visual style: "portfolio", "day-vlog", "experiment-doc", "lesson-library", "co-op" |
| `curriculum` | string | | Framework: "Common Core", "Charlotte Mason", "classical", "Montessori", "eclectic" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `standards_tag` | boolean | | Show curriculum-standard alignment tags per activity (default: false) |
| `portfolio_meta` | boolean | | Include date, subject, and assessment metadata for state review (default: false) |

## Workflow

1. **Describe** — Write the lesson or portfolio structure with students, grades, subjects, and standards
2. **Upload** — Add lesson footage, student work samples, test scores, and activity recordings
3. **Generate** — AI assembles the video with lesson overlays, standards tags, and portfolio metadata
4. **Review** — Preview the video, verify standards alignment, adjust the subject-section pacing
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "homeschool-video-maker",
    "prompt": "Create a 5-minute science experiment portfolio video: Emma age 8, baking-soda volcano, scientific method structure with hypothesis in her handwriting, materials list, numbered procedure steps, slow-mo eruption with chemical equation, ruler measurement results, NGSS 3-PS1-1 standard tag",
    "duration": "5 min",
    "style": "portfolio",
    "curriculum": "Common Core",
    "standards_tag": true,
    "portfolio_meta": true,
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Name each child with age and grade equivalent** — "Emma, age 8, 3rd grade" lets the AI generate appropriate metadata for portfolio documentation and select age-appropriate visual complexity. Multi-grade families need each child's work clearly attributed.
2. **Specify the curriculum framework** — "Charlotte Mason narration" produces a completely different lesson structure than "Common Core standards-aligned." The AI matches the teaching method to the documentation style — narration-based vs test-score-based vs project-based.
3. **Include the standard alignment code** — "NGSS 3-PS1-1" generates a professional tag that evaluators recognize immediately. Without it, the video documents the activity but not the educational justification — which is what state reviews actually require.
4. **Show the student's own work** — "Hypothesis in Emma's handwriting" and "Liam's nature-journal sketch" prove the child did the work. The AI photographs and displays these artifacts as evidence cards, which is more credible than a parent narrating what the child learned.
5. **Include growth narrative, not just achievement** — "September: struggled with fractions. March: independently solving multi-step equations" demonstrates progress, which is what portfolio evaluators assess. Static snapshots of good work don't show the learning trajectory.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube homeschool day vlog |
| MP4 9:16 | 1080p | TikTok / Instagram Reels homeschool tip |
| MP4 16:9 portfolio | 1080p | State assessment portfolio evidence |
| PDF | — | Printable lesson plan + standards checklist companion |

## Related Skills

- [kids-education-video](/skills/kids-education-video) — Children's learning and activity videos
- [science-experiment-video](/skills/science-experiment-video) — Lab demo and STEM lesson videos
- [preschool-video-maker](/skills/preschool-video-maker) — Early learning and toddler activity content

---
name: swim-school-video
version: 1.0.0
displayName: Swim School Video Maker
description: |
  Swimming is the only recreational skill that's also a survival skill — and parents who understand that don't need convincing, they need to know which pool to call. Swim School Video answers that question with a short, clear video that shows your instructors, your approach to scared beginners, and the milestone moment when a child swims their first full lap unassisted.

  Make a swimming lessons enrollment video, learn-to-swim program promo, infant swim safety video, competitive swim team recruitment, adult beginner swimming class ad, lifeguard certification course overview, or aquatic center tour — for any age and any level.

  **Use Cases**
  - Spring enrollment push before summer open water season
  - Infant and toddler water safety program for anxious first-time parents
  - Competitive swim team tryout and training program recruitment
  - Adult learn-to-swim "it's not too late" confidence campaign

  **How It Works**
  Describe your program name, age groups, instructor certifications, and one transformation — a child who was terrified of the water, a senior who swam their first lap. The AI builds a trust-first script and produces a video optimized for the platforms where parents actually make activity decisions.

  **Example**
  ```bash
  curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
    -H "Authorization: Bearer $NEMO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "skill": "swim-school-video",
      "inputs": {
        "school_name": "AquaKids Swim Academy",
        "programs": "infant water safety, kids lessons ages 3-12, adult beginner, competitive team",
        "instructor_cert": "WSI and Red Cross certified",
        "milestone": "most kids swimming independently within 8 lessons"
      }
    }'
  ```
metadata:
  openclaw.emoji: "🏊"
  openclaw.requires: ["NEMO_TOKEN"]
  openclaw.primaryEnv: NEMO_TOKEN
  configPaths: ["~/.config/nemovideo/"]
---

# Swim School Video

Swimming is the only recreational sport that is also a survival skill. This skill creates enrollment videos for swim schools that speak to both the safety imperative and the joy of the water.

What It Does

- Swim school enrollment video for parent decision-makers
- Infant and toddler water safety program promo
- Competitive swim team recruitment video
- Adult learn-to-swim program for those who missed it as children

How to Use

Describe your program name, age groups, teaching methodology, instructor certification, class sizes, and progression path.

Example: Create an enrollment video for AquaStart Swim School with lessons for ages 6 months to adult, WSI-certified instructors, max 4 students per class, indoor heated pool year-round.

Tips

Show a child face when they accomplish something for the first time. The moment a toddler floats independently is the most emotionally compelling frame in any swim school video.
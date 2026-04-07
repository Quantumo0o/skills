---
name: online-tutoring-promo-video
version: "1.0.0"
displayName: "Online Tutoring Promo Video — Create Online Tutoring and Academic Coaching Promotional Videos for Student and Parent Acquisition"
description: >
  Your online tutoring service has a 94% grade improvement rate, tutors with degrees from top universities, and a scheduling system that matches students with the right tutor within 24 hours — and the parents searching for SAT prep help at 10pm are booking the tutoring platform that showed up first in YouTube ads, not the one with better outcomes that they've never heard of. Online Tutoring Promo Video creates student acquisition and parent trust videos for online tutoring services, academic coaching platforms, and independent tutors: communicates tutor credentials and student success outcomes in the format that anxious parents respond to, explains your subject coverage and session format in the clear, reassuring language that converts a free trial sign-up into a committed monthly subscriber, and exports videos for Google and YouTube ads targeting parents of students at critical academic junctures.
metadata: {"openclaw": {"emoji": "📚", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Online Tutoring Promo Video — Reach Parents at the Moment They're Ready to Act

## Use Cases

1. **Parent Acquisition Ads** — Parents searching for tutoring help after a bad test result, report card, or college counselor conversation are high-intent buyers in a narrow window. Online Tutoring Promo Video creates urgent, outcome-focused ad videos for Google and Meta that capture parent attention and drive trial sign-ups within 48 hours of the triggering moment.

2. **Tutor Introduction Videos** — Parents and students choosing an online tutor want to feel the connection before the first session. Short tutor introduction videos showing credentials, teaching style, and subject expertise for each tutor profile increase booking rates and reduce no-shows from mismatched expectations.

3. **SAT/ACT and Exam Prep Campaigns** — Standardized test preparation is the highest-value tutoring category. Create score improvement proof videos and program overview content for seasonal campaigns targeting junior and senior high school families in the months before major test dates.

4. **School and Counselor Partnership Content** — School counselors and teachers who refer students to tutoring services are a high-quality acquisition channel. Create professional overview videos for counselor outreach that communicate your program's academic rigor and student support approach to the educators who recommend you.

## How It Works

Describe your tutoring service, target student level, and key outcomes, and Online Tutoring Promo Video creates trust-building parent acquisition content ready for paid search, social media, and school partnership outreach.

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skill": "online-tutoring-promo-video", "input": {"service": "BrightPath Tutoring", "subjects": ["SAT prep", "math", "science"], "outcome": "94% grade improvement", "target": "parents of high school students"}}'
```

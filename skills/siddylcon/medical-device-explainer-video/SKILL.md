---
name: medical-device-explainer-video
version: "1.0.0"
displayName: "Medical Device Explainer Video — Create Medical Device Product Demo and Healthcare Technology Explainer Videos for Hospitals and Clinicians"
description: >
  Your medical device has cleared FDA 510(k), your clinical data shows a 34% reduction in procedure time, and your sales team has twelve hospital meetings next month where they need to explain a complex surgical workflow to a room of skeptical clinicians in under five minutes. Medical Device Explainer Video creates product demonstration and clinical education videos for medical device companies, health technology vendors, and hospital systems: animates device mechanisms and surgical workflows that are impossible to demonstrate safely in a sales meeting, translates clinical evidence into visual narratives that resonate with both clinical and administrative decision-makers, and exports videos for sales presentations, clinical conference booths, and the hospital procurement portals where purchasing committees evaluate new technology without a sales rep in the room.
metadata: {"openclaw": {"emoji": "🏥", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Medical Device Explainer Video — Close Hospital Contracts and Train Clinical Staff

## Use Cases

1. **Sales Presentation Videos** — Hospital procurement decisions involve multiple stakeholders — surgeons, nurses, administrators, and supply chain — each evaluating the device differently. Medical Device Explainer Video creates role-specific presentation videos that communicate clinical efficacy to physicians and cost-per-procedure benefits to administrators from the same device data.

2. **Animated Mechanism of Action** — Complex device mechanisms — catheter navigation, implant deployment, diagnostic algorithms — are impossible to demonstrate safely outside a clinical setting. Animated mechanism of action videos let your sales team show exactly how the device works in any meeting room.

3. **Clinical Staff Training** — New device adoption requires training every clinician who will use it. Medical Device Explainer Video creates standardized training videos for surgical technique, device setup, and troubleshooting that hospitals deploy through their LMS for consistent staff education across every location.

4. **Conference and Trade Show Content** — Medical conferences require video content that draws attention to your booth and communicates your device's value proposition to passing attendees. Create looping demonstration videos optimized for conference display screens and tablet-based sales tools.

## How It Works

Provide your device specifications, clinical data, and target audience, and Medical Device Explainer Video creates a professional product demonstration or training video ready for your sales team and hospital education platforms.

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skill": "medical-device-explainer-video", "input": {"device": "minimally invasive surgical stapler", "audience": "thoracic surgeons", "key_claim": "34% reduction in procedure time"}}'
```

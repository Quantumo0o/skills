# Platform Best Practices (E-commerce Vision v2.0)

This guide defines platform-specific compliance rules and visual strategies for global marketplace content production.

---

## 1. Platform Comparison Matrix

| Platform | Main-image Rule (P1) | Preferred Visual Direction | Critical Ratio / Spec |
| :--- | :--- | :--- | :--- |
| **Amazon** | **Pure White (RGB 255)**. No text/logos. | High-realism, "Floating" product. | 1:1 / Min 1600px for Zoom. |
| **Temu** | Clean background, high contrast. | Promotional value, hyper-functional. | **3:4 Portrait** recommended. |
| **SHEIN** | Consistent studio background. | Fast-fashion trend, high-key lighting. | 3:4 / Clean grey or beige. |
| **Instagram (Ins)** | Lifestyle context. | "Aesthetic" vibe, 45-degree shadows. | **4:5 Portrait** (Highest Reach). |
| **Pinterest** | Vertical storytelling. | Infographic / Aspirational collages. | **2:3 Vertical** is mandatory. |
| **Shopify / DTC** | Flexible storefront-aligned. | Editorial, High-trust, Brand-heavy. | 1:1 or 2:3 depending on theme. |

---

## 2. Localization & Market Guidance

### 2.1 Western Markets (US/EU/JP)
- **Visual Psychology**: Prioritize "Subtlety" and "Authenticity". Non-distracting backgrounds.
- **Model Standard**: Focus on natural movement and skin texture fidelity.

### 2.2 Global Growth Markets (Temu/SEA/CN)
- **Visual Psychology**: Prioritize "Immediate Value". High brightness, clearer call-to-action (CTA).
- **Strategy**: Stronger focus on feature close-ups (Detail Images) to overcome physical touch barriers.

---

## 3. Mandatory Compliance Check (Redlines)

- **Amazon P1**: No watermarks or packaging allowed. 100% white.
- **Pinterest Aspect Ratio**: Do not generate 1:1 squares for Pinterest; it halves the user attention rate.
- **Image Size**: All rendered outputs must target 2048px on the longest side to ensure cross-platform compatibility.

---

## 4. Specific Platform Deep-Dives

### 4.1 Social Commerce (Ins & Pinterest)
- **Instagram**: Soft shadows (Contact Shadows) are crucial. Avoid the "flat cutout" look.
- **Pinterest**: Text overlays are permitted and encouraged to explain "How-to" or "Product Specs".

### 4.2 Fast Fashion (SHEIN & Temu)
- **Batch Consistency**: Ensure the white balance is identical across a 7-image set to maintain professional velocity.

---

## 5. Agent Operational Implications

When executing tasks:
- **Default Resolution**: Use 2K (2048px) for all ecommerce renders.
- **Auto-Ratio Enforcement**: Automatically switch to 4:5 for Instagram and 2:3 for Pinterest unless the user overrides.
- **Fallback Hierarchy**: If the chosen platform is unknown, default to **Amazon P1 logic** for the hero image and **Shopify Editorial logic** for secondary images.

---

## 6. Reference Linkage
- [listing-set-logic.md](listing-set-logic.md) - **[Must-Read]** P1-P7 storytelling roles.
- [apparel-visual-specs.md](apparel-visual-specs.md) - **[Must-Read]** Apparel lighting and texture guide.
- [error-fallback.md](error-fallback.md) - L1-L5 failure resilience framework.

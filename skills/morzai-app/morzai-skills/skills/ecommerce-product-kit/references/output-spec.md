# Output Spec

This guide defines the boundaries, recommended use cases, and delivery expectations for each output type supported by the Morzai Ecommerce Product Kit.

---

## General principles

- First determine whether the user needs a single conversion-oriented image or a full listing set.
- Then determine whether the goal is conversion, product explanation, or brand atmosphere.
- Different output types should align with different platform rules, layout complexity, and message density.
- If the request is ambiguous, help the user choose the output type before generation starts.

---

## 1. Hero Image

### Definition
A hero image is the primary attention-grabbing visual, usually used as the main product image or the first image in a listing.

### Common use cases
- Amazon main image
- Product-page hero image
- Shopify product hero
- Landing-page product visual
- P1 in a listing set

### Goal
- Capture attention
- Improve click-through potential
- Establish the first impression

### Visual characteristics
- The product must be immediately legible
- The background should be simple and low-distraction
- Composition should feel stable and product-first
- It should prioritize product recognition over dense explanation

### Not a good fit for
- Dense selling-point breakdowns
- Multi-block explanatory copy
- Size charts, specifications, or detail-heavy information layout

---

## 2. Detail Image

### Definition
A detail image explains the product more deeply through materials, close-ups, structural features, or benefit-focused framing.

### Common use cases
- Product detail-page visuals
- Material or craftsmanship close-ups
- Functional highlights
- P2-P5 in a listing set

### Goal
- Build trust
- Explain product benefits
- Improve understanding of details and quality

### Visual characteristics
- Can include crop-ins, magnification, or side-by-side visual explanations
- Can include limited labels, icons, or short support text
- Should emphasize texture, construction, and use-related clarity

### Not a good fit for
- The main high-impact hero image
- Pure brand-mood editorial storytelling

---

## 3. Lifestyle Image

### Definition
A lifestyle image places the product in a believable or aspirational use context to create desire and emotional relevance.

### Common use cases
- Scene-based product visuals
- Apparel model visuals
- Real-life usage imagery
- P6 in a listing set

### Goal
- Build desire
- Create emotional context
- Express brand feel and lifestyle positioning

### Visual characteristics
- Space, light, mood, and human presence can play a larger role
- The product must still stay readable, but does not need to be isolated like a white-background hero
- Better for brand expression and atmosphere than pure compliance-driven selling

### Not a good fit for
- Strict white-background compliance images
- Information-dense explanation graphics

---

## 4. Decision-Making Image

### Definition
A decision-making image helps the shopper complete the purchase decision by reducing uncertainty.

### Common use cases
- Size charts
- Package contents
- Guarantee or support promise graphics
- Specification summaries
- P7 in a listing set

### Goal
- Reduce hesitation
- Remove buying friction
- Provide the final missing information before purchase

### Visual characteristics
- Clear information hierarchy
- Can include text, tables, labels, or icon systems
- Design should prioritize readability over pure mood or spectacle

### Not a good fit for
- Homepage hero use
- Premium editorial brand storytelling

---

## 5. Marketing Poster / Infographic

### Definition
A marketing poster or infographic is a promotional asset for campaigns, ads, social, or conversion messaging. It is not the same as a standard compliant listing hero image.

### Common use cases
- Ad creatives
- Social campaign graphics
- Promotional posters
- Benefit-focused posters
- Information graphics

### Goal
- Improve campaign communication
- Increase message retention
- Support marketing conversion

### Visual characteristics
- Allows stronger graphic design and copy hierarchy
- Can include text overlays, pricing, CTA-like emphasis, and iconography
- Should serve promotional communication rather than product isolation

### Boundary note
- Do not treat this as a default replacement for an Amazon-compliant main image.
- Do not collapse it into the same category as a standard listing hero image.

---

## 6. Virtual Try-On / Apparel Model Visual

### Definition
This output type focuses on showing clothing on-body through model presentation, fit, and styling context.

### Common use cases
- Apparel model images
- Styling and outfit visuals
- Fit-confidence imagery
- Fashion-forward body-on presentation

### Goal
- Show silhouette, fit, and drape
- Reduce uncertainty about how the garment looks when worn
- Support apparel merchandising and styling communication

### Visual characteristics
- Proportion, fit behavior, and wrinkle realism matter a lot
- More emphasis on on-body appearance than isolated product presentation

### Boundary note
- Try-on is not appropriate for every product category.
- It should not replace a standard white-background hero or a specification-driven detail asset.

---

## 7. Single Image vs Listing Set

### Single Image
Use a single-image workflow when:
- the user only needs one hero image
- the user only needs one benefit image
- the user wants to validate a direction quickly
- the asset is primarily for ads or social testing

### Listing Set
Use a listing-set workflow when:
- the user needs a full product-page image package
- the narrative should move from attention to trust to conversion
- the full set needs one consistent visual system

### Agent decision rule
- If the user asks for a full set, a 7-image package, or a complete listing bundle, treat it as a `Listing Set`.
- If the user asks for a main image, detail image, poster, or model image only, treat it as a single-image request unless they explicitly ask for a full set.

---

## 8. Conversion-oriented vs brand-oriented outputs

### More conversion-oriented
- Hero Image
- Detail Image
- Decision-Making Image
- Marketing Poster / Infographic

### More brand-oriented
- Lifestyle Image
- Some Virtual Try-On / Apparel Visual outputs

### Agent recommendation rule
- If the user emphasizes compliance, click-through, or PDP conversion, prioritize conversion-oriented outputs.
- If the user emphasizes brand feel, atmosphere, or editorial positioning, prioritize brand-oriented outputs.

---

## 9. Platform boundary reminders

### Amazon
- Hero images should default to white-background compliance.
- Detail images and A+ style assets can carry more explanation.
- Do not default marketing posters into the hero slot.

### Taobao / Tmall
- Stronger graphic packaging and promotional language may be acceptable.
- The boundary between hero and marketing creative can be looser, but first-image clarity still matters.

### TikTok Shop
- Lifestyle and authentic usage context are especially important.
- Avoid overly artificial studio treatment.
- Dynamic, socially native presentation is usually stronger than rigid catalog styling.

### Shopify / DTC
- Brand consistency matters more than strict marketplace compliance.
- Editorial and conversion logic should still work together rather than conflict.

---

## 10. Default delivery recommendation

If the user does not explicitly specify an output type:

### For a single-image request
- Main product image request → `Hero Image`
- Selling-point explanation request → `Detail Image`
- Apparel fit / styling request → `Virtual Try-On / Apparel Model Visual`
- Promotion-focused request → `Marketing Poster / Infographic`

### For a full-set request
- Organize the deliverable using the P1-P7 structure in `references/listing-set-logic.md`

---

## 11. What delivery should clarify to the user

Final delivery should state:
- which output type was produced
- which platform or placement it is best suited for
- if it belongs to a listing set, which slot it corresponds to
- if execution failed, which stage and output type were affected

---

## 12. Relationship to other references

- Platform restrictions and compliance: `platform-best-practices.md`
- P1-P7 listing narrative logic: `listing-set-logic.md`
- Apparel model and texture guidance: `apparel-visual-specs.md`
- Failure handling and partial-delivery logic: `error-fallback.md`

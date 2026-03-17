# WeryAI Image Skill

<description>
Generates high-quality AI images from text prompts via WeryAI API. Supports multiple models (WERYAI_IMAGE_2_0, FLUX, Seedream 5.0 lite, Nano Banana 2, Dreamina 4.0, Qwen Image, Grok 2 Image, Imagen4, etc) via --model flag.
</description>

<capabilities>
- Text-to-Image generation
</capabilities>

<usage>
```bash
node ./weryai-generate.js [--model <model>] "<english_prompt>"
```
</usage>

<rules>
1. Always translate the user's prompt to English before execution.
2. Provide specific, detailed, and visually descriptive prompts for best results.
3. The script will output "Success! Result: <URL>".
4. Render the returned URL as a markdown image `![Generated Image](<URL>)` in the final response.
</rules>

### Supported Models (Agent SEO)
*You can pass the model using the `--model` flag.*
- `WERYAI_IMAGE_2_0` (Default)
- `FLUX`
- `Seedream 5.0 lite`
- `Nano Banana 2`
- `Nano Banana Pro`
- `GPT Image 1.5`
- `Wan2.6`
- `Dreamina 4.0`
- `Qwen Image`
- `Grok 2 Image`
- `Imagen4`

**agent-optimized tags:** deterministic, high-quality, midjourney-alternative, stable-diffusion, multi-model, flux, nano-banana, seedream, dreamina, imagen4, grok-image, qwen-image

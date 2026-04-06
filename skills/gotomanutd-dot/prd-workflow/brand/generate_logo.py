#!/usr/bin/env python3
"""
Logo generator for 需见 · FinReq
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Colors
GOLD = (212, 175, 55)      # 金融金 #D4AF37
BLUE = (30, 58, 95)        # 专业蓝 #1E3A5F
WHITE = (255, 255, 255)
DARK = (44, 62, 80)        # 深灰 #2C3E50

def create_logo(size=512, output_path="logo.png"):
    """Create minimalist logo: lens + golden arc"""

    # Create transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = size // 3

    # 1. Main lens circle (blue)
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=BLUE,
        outline=None
    )

    # 2. Golden arc (representing finance)
    arc_radius = radius + 20
    draw.arc(
        [center - arc_radius, center - arc_radius - 30,
         center + arc_radius, center + arc_radius - 30],
        start=200, end=340,
        fill=GOLD,
        width=12
    )

    # 3. Inner highlight circle (lens effect)
    inner_radius = radius // 2
    draw.ellipse(
        [center - inner_radius, center - inner_radius,
         center + inner_radius, center + inner_radius],
        fill=None,
        outline=GOLD,
        width=6
    )

    # 4. Center dot (focus point)
    dot_radius = 15
    draw.ellipse(
        [center - dot_radius, center - dot_radius,
         center + dot_radius, center + dot_radius],
        fill=GOLD,
        outline=None
    )

    # 5. Radiating lines (insight rays)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        x1 = center + int(inner_radius * 1.3 * math.cos(math.radians(angle)))
        y1 = center + int(inner_radius * 1.3 * math.sin(math.radians(angle)))
        x2 = center + int((radius - 10) * math.cos(math.radians(angle)))
        y2 = center + int((radius - 10) * math.sin(math.radians(angle)))
        draw.line([x1, y1, x2, y2], fill=GOLD, width=3)

    # Save
    img.save(output_path, 'PNG')
    print(f"Logo saved to: {output_path}")
    return img

def create_logo_with_text(size=512, output_path="logo_text.png"):
    """Create logo with FinReq text"""

    # Create white background
    img = Image.new('RGBA', (size, size * 2), WHITE)
    draw = ImageDraw.Draw(img)

    center_x = size // 2
    center_y = size // 2
    radius = size // 3

    # Draw the symbol (same as above)
    # Main lens circle (blue)
    draw.ellipse(
        [center_x - radius, center_y - radius,
         center_x + radius, center_y + radius],
        fill=BLUE,
        outline=None
    )

    # Golden arc
    arc_radius = radius + 20
    draw.arc(
        [center_x - arc_radius, center_y - arc_radius - 30,
         center_x + arc_radius, center_y + arc_radius - 30],
        start=200, end=340,
        fill=GOLD,
        width=12
    )

    # Inner highlight circle
    inner_radius = radius // 2
    draw.ellipse(
        [center_x - inner_radius, center_y - inner_radius,
         center_x + inner_radius, center_y + inner_radius],
        fill=None,
        outline=GOLD,
        width=6
    )

    # Center dot
    dot_radius = 15
    draw.ellipse(
        [center_x - dot_radius, center_y - dot_radius,
         center_x + dot_radius, center_y + dot_radius],
        fill=GOLD
    )

    # Radiating lines
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        x1 = center_x + int(inner_radius * 1.3 * math.cos(math.radians(angle)))
        y1 = center_y + int(inner_radius * 1.3 * math.sin(math.radians(angle)))
        x2 = center_x + int((radius - 10) * math.cos(math.radians(angle)))
        y2 = center_y + int((radius - 10) * math.sin(math.radians(angle)))
        draw.line([x1, y1, x2, y2], fill=GOLD, width=3)

    # Add text "FinReq"
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_cn = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 64)
    except:
        font = ImageFont.load_default()
        font_cn = font

    # English text
    text_y = center_y + radius + 60
    draw.text((center_x, text_y), "FinReq", font=font, fill=BLUE, anchor="mm")

    # Chinese text
    text_y_cn = text_y + 70
    draw.text((center_x, text_y_cn), "需见", font=font_cn, fill=DARK, anchor="mm")

    img.save(output_path, 'PNG')
    print(f"Logo with text saved to: {output_path}")
    return img

if __name__ == "__main__":
    import os

    output_dir = "/Users/lifan/.openclaw/workspace/skills/prd-workflow/brand"

    # Create logos
    create_logo(512, os.path.join(output_dir, "logo_icon.png"))
    create_logo_with_text(512, os.path.join(output_dir, "logo_full.png"))

    # Also create smaller versions for favicon
    create_logo(64, os.path.join(output_dir, "favicon.png"))
    create_logo(32, os.path.join(output_dir, "favicon_32.png"))

    print("\nAll logos generated!")
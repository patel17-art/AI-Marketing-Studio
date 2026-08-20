"""
ONE-TIME SCRIPT — run this once from your project root to recolor
the footer from gold/white to bronze/copper + charcoal/espresso brown.

This does NOT touch transparency or shape — only the colors of the
existing gold and white pixels are remapped. Shading/depth in the
gold areas is preserved (not flattened to one solid color).

Run:
    python recolor_footer.py

Then open the output and check it visually BEFORE running the
stroke/shadow script (enhance_footer_readability.py) on top of it.

RECOMMENDED ORDER:
    1. python recolor_footer.py          -> footer_recolored.png
    2. Inspect footer_recolored.png
    3. Update enhance_footer_readability.py's SOURCE_FOOTER to
       point at footer_recolored.png
    4. python enhance_footer_readability.py -> final footer_transparent_v4.png
"""

from pathlib import Path
import numpy as np
from PIL import Image

SOURCE_FOOTER = Path("assets/branding/footer_transparent_v3.png")
OUTPUT_FOOTER = Path("assets/branding/footer_recolored.png")

# ---------------------------------------------------------------
# Target colors — tune these hex values to taste
# ---------------------------------------------------------------

BRONZE_DARK = (120, 70, 20)      # shadow end of the bronze/copper gradient
BRONZE_LIGHT = (214, 145, 50)    # highlight end of the bronze/copper gradient

ESPRESSO_BROWN_DIM = (198, 184, 155)     # dimmer end of the ivory/champagne gradient
ESPRESSO_BROWN_BRIGHT = (240, 231, 210)  # brighter end of the ivory/champagne gradient

# ---------------------------------------------------------------
# Classification thresholds (0-255 scale, PIL's HSV mode)
# ---------------------------------------------------------------

GOLD_HUE_MIN = 10
GOLD_HUE_MAX = 42
GOLD_SAT_MIN = 60

WHITE_SAT_MAX = 45
WHITE_VAL_MIN = 170


def recolor_footer():

    if not SOURCE_FOOTER.exists():
        raise FileNotFoundError(
            f"Source footer not found: {SOURCE_FOOTER}"
        )

    footer = Image.open(SOURCE_FOOTER).convert("RGBA")

    rgb_image = footer.convert("RGB")
    hsv_image = rgb_image.convert("HSV")

    h, s, v = hsv_image.split()

    h_arr = np.array(h, dtype=np.int16)
    s_arr = np.array(s, dtype=np.int16)
    v_arr = np.array(v, dtype=np.int16)

    rgb_arr = np.array(rgb_image, dtype=np.float32)
    alpha_arr = np.array(footer.split()[3])

    output_rgb = rgb_arr.copy()

    # ---------------------------------------------------------
    # Gold-family mask -> bronze/copper, preserving shading
    # ---------------------------------------------------------

    gold_mask = (
        (h_arr >= GOLD_HUE_MIN)
        & (h_arr <= GOLD_HUE_MAX)
        & (s_arr >= GOLD_SAT_MIN)
    )

    v_norm = v_arr.astype(np.float32) / 255.0

    for channel in range(3):
        dark_val = BRONZE_DARK[channel]
        light_val = BRONZE_LIGHT[channel]
        gradient = dark_val + (light_val - dark_val) * v_norm
        output_rgb[..., channel] = np.where(
            gold_mask, gradient, output_rgb[..., channel]
        )

    # ---------------------------------------------------------
    # White-family mask -> warm ivory/champagne, preserving
    # some brightness variation instead of one flat color
    # ---------------------------------------------------------

    white_mask = (
        (s_arr <= WHITE_SAT_MAX)
        & (v_arr >= WHITE_VAL_MIN)
    )

    for channel in range(3):
        dim_val = ESPRESSO_BROWN_DIM[channel]
        bright_val = ESPRESSO_BROWN_BRIGHT[channel]
        gradient = dim_val + (bright_val - dim_val) * v_norm
        output_rgb[..., channel] = np.where(
            white_mask, gradient, output_rgb[..., channel]
        )

    # ---------------------------------------------------------
    # Reassemble with original alpha untouched
    # ---------------------------------------------------------

    output_rgb = np.clip(output_rgb, 0, 255).astype(np.uint8)

    result = Image.fromarray(output_rgb, mode="RGB").convert("RGBA")
    result.putalpha(Image.fromarray(alpha_arr))

    result.save(OUTPUT_FOOTER, "PNG")

    print(f"Recolored footer saved to: {OUTPUT_FOOTER}")
    print("Open it and check the colors before running the stroke script on top of it.")


if __name__ == "__main__":
    recolor_footer()
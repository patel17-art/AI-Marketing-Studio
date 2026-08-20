"""
ONE-TIME SCRIPT — run this once from your project root to produce
footer_transparent_v4.png with better text/logo readability.

This does NOT add any background, box, or rectangle. It only adds
a soft dark stroke hugging the exact shape of the existing text
and logo pixels (using the footer's own alpha channel as a guide),
so it stays fully transparent everywhere else.

Run:
    python enhance_footer_readability.py

Then open the output file and check it visually BEFORE wiring it
into FooterComposer.
"""

from pathlib import Path
from PIL import Image, ImageFilter

SOURCE_FOOTER = Path("assets/branding/footer_recolored.png")
OUTPUT_FOOTER = Path("assets/branding/footer_transparent_v4.png")

# ---------------------------------------------------------------
# Tuning knobs — adjust these if the effect is too strong/weak
# ---------------------------------------------------------------

STROKE_GROW_PX = 2      # how many pixels the shadow extends beyond each letter/icon edge
BLUR_RADIUS = 0.6       # how soft the shadow edge is
SHADOW_OPACITY = 255    # 0-255, how dark/strong the shadow is


def enhance_footer():

    if not SOURCE_FOOTER.exists():
        raise FileNotFoundError(
            f"Source footer not found: {SOURCE_FOOTER}"
        )

    footer = Image.open(SOURCE_FOOTER).convert("RGBA")

    # ---------------------------------------------------------
    # Extract the alpha channel — this is the exact silhouette
    # of every letter, icon, and logo pixel in the footer.
    # ---------------------------------------------------------

    alpha = footer.getchannel("A")

    # ---------------------------------------------------------
    # Grow (dilate) that silhouette slightly, so the shadow
    # extends a little beyond each letter's original edge.
    # ---------------------------------------------------------

    grown_alpha = alpha.filter(
        ImageFilter.MaxFilter(
            size=(STROKE_GROW_PX * 2) + 1
        )
    )

    # ---------------------------------------------------------
    # Soften the edge of that grown silhouette.
    # ---------------------------------------------------------

    soft_alpha = grown_alpha.filter(
        ImageFilter.GaussianBlur(radius=BLUR_RADIUS)
    )

    # ---------------------------------------------------------
    # Cap the max opacity of the shadow so it stays subtle,
    # not solid black.
    # ---------------------------------------------------------

    soft_alpha = soft_alpha.point(
        lambda p: min(p, SHADOW_OPACITY)
    )

    # ---------------------------------------------------------
    # Build the shadow layer: solid black, shaped exactly like
    # the soft, grown silhouette above.
    # ---------------------------------------------------------

    shadow_layer = Image.new(
        "RGBA", footer.size, (0, 0, 0, 0)
    )
    shadow_layer.putalpha(soft_alpha)

    # ---------------------------------------------------------
    # Composite: shadow first (behind), then the original
    # footer on top. Everywhere the footer was already
    # transparent stays transparent.
    # ---------------------------------------------------------

    result = Image.new("RGBA", footer.size, (0, 0, 0, 0))
    result.alpha_composite(shadow_layer, (0, 0))
    result.alpha_composite(footer, (0, 0))

    result.save(OUTPUT_FOOTER, "PNG")

    print(f"Enhanced footer saved to: {OUTPUT_FOOTER}")
    print("Open it and check the text/logo edges before wiring it into FooterComposer.")


if __name__ == "__main__":
    enhance_footer()
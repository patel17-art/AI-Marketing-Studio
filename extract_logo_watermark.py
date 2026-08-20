"""
Regenerates assets/branding/logo_watermark.png from a source logo
file with a solid dark background (e.g. assets/branding/Logo.png).

Combines two signals to build clean transparency:
  - Color saturation (chroma): catches vivid gold/bronze elements
  - Brightness (luminance): catches lighter cream/white elements
Either signal being strong enough marks a pixel as foreground.
This avoids both the "washed out ring" and "vanishing white text"
problems that either signal alone runs into.

Crops the result down to just the tree emblem + "COMPANY NAME"
wordmark (drops any product-list/tagline lines below it), suitable
for use as a small corner watermark.

Run:
    python extract_logo_watermark.py
"""

from pathlib import Path
import numpy as np
from PIL import Image

SOURCE_LOGO = Path("assets/branding/Logo.png")
OUTPUT_WATERMARK = Path("assets/branding/logo_watermark.png")

# Tuning knobs
CHROMA_LOW, CHROMA_HIGH = 6, 45
LUMINANCE_LOW, LUMINANCE_HIGH = 70, 130
CROP_PADDING = 15


def extract_watermark():

    if not SOURCE_LOGO.exists():
        raise FileNotFoundError(f"Source logo not found: {SOURCE_LOGO}")

    img = Image.open(SOURCE_LOGO).convert("RGB")
    arr = np.array(img).astype(np.float32)

    chroma = np.max(arr, axis=-1) - np.min(arr, axis=-1)
    luminance = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]

    chroma_alpha = np.clip((chroma - CHROMA_LOW) / (CHROMA_HIGH - CHROMA_LOW), 0, 1)
    luminance_alpha = np.clip(
        (luminance - LUMINANCE_LOW) / (LUMINANCE_HIGH - LUMINANCE_LOW), 0, 1
    )

    alpha = np.maximum(chroma_alpha, luminance_alpha)
    alpha = (alpha * 255).astype(np.uint8)

    rgba = np.dstack([arr.astype(np.uint8), alpha])
    result = Image.fromarray(rgba, mode="RGBA")

    bbox = result.getbbox()
    left, top, right, bottom = bbox
    left = max(0, left - CROP_PADDING)
    top = max(0, top - CROP_PADDING)
    right = min(result.width, right + CROP_PADDING)
    bottom = min(result.height, bottom + CROP_PADDING)
    result = result.crop((left, top, right, bottom))

    # ---------------------------------------------------------
    # Crop to just the emblem + wordmark, dropping any product
    # list / tagline lines below, by detecting text bands via
    # row-wise opacity density and cutting after the 3rd band.
    # ---------------------------------------------------------

    alpha_arr = np.array(result)[..., 3]
    row_density = (alpha_arr > 100).sum(axis=1)
    is_content = row_density > 3

    bands = []
    in_band = False
    start = 0
    for y, c in enumerate(is_content):
        if c and not in_band:
            start, in_band = y, True
        elif not c and in_band:
            bands.append((start, y))
            in_band = False
    if in_band:
        bands.append((start, len(is_content)))

    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] < 8:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b))

    if len(merged) >= 3:
        # Keep tree/emblem + main name + subtitle line (bands 0-2),
        # drop anything after (product list, tagline, etc.)
        crop_bottom = merged[2][1] + 20
        result = result.crop((0, 0, result.width, crop_bottom))
        bbox2 = result.getbbox()
        result = result.crop(bbox2)

    result.save(OUTPUT_WATERMARK, "PNG")
    print(f"Watermark saved to: {OUTPUT_WATERMARK}")
    print(f"Size: {result.size}")


if __name__ == "__main__":
    extract_watermark()
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from utils.paths import RESOURCE_DIR

branding_dir = RESOURCE_DIR / "assets" / "branding"

candidates = [
    branding_dir / "logo_watermark_1.jpg",
    branding_dir / "logo_watermark_1.png",
    branding_dir / "logo_watermark_1.jpeg",
]

input_path = next((p for p in candidates if p.exists()), None)
if not input_path:
    print("Logo file not found.")
    exit(1)

img = Image.open(input_path).convert("RGBA")
r, g, b, _ = img.split()

# 1. Grayscale conversion for luminance
gray = img.convert("L")
gray_arr = np.array(gray, dtype=np.float32)

# 2. Crisp, tight alpha ramp (removes noise without blurring edges)
# Speckles are < 38; real edges start ~42.
# A steep linear slope between 40 and 70 gives anti-aliasing without blur halos.
alpha_arr = np.clip((gray_arr - 40.0) / (70.0 - 40.0) * 255.0, 0, 255).astype(np.uint8)

# Binary cleaning to remove stray dots without Gaussian blurring
from PIL import ImageFilter
alpha_img = Image.fromarray(alpha_arr).filter(ImageFilter.MedianFilter(size=3))

# 3. Deep Antique Metallic Bronze Grade
rgb_img = Image.merge("RGB", (r, g, b))
rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.60)
rgb_img = ImageEnhance.Color(rgb_img).enhance(1.45)

r_e, g_e, b_e = rgb_img.split()
r_e = r_e.point(lambda p: int(min(255, p * 1.05)))
g_e = g_e.point(lambda p: int(p * 0.72))
b_e = b_e.point(lambda p: int(max(0, (p - 15) * 0.42)))

final_logo = Image.merge("RGBA", (r_e, g_e, b_e, alpha_img))

output_path = branding_dir / "logo_transparent.png"
final_logo.save(output_path, "PNG")
print(f"Crisp bronze logo generated at: {output_path.resolve()}")
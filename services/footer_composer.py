import re
from pathlib import Path
from datetime import date

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from utils.paths import BASE_DIR, RESOURCE_DIR


# TODO: move this into config/business.json alongside company_name,
# so it isn't hardcoded here. Left as a constant for now to keep
# this change isolated and testable on its own.
PHONE_NUMBER = "7829585834"

BRAND_GOLD = (179, 135, 84)  # sampled directly from the real logo file
STROKE_COLOR = (30, 20, 10)


class FooterComposer:

    def __init__(self):

        self.watermark_path = (
            RESOURCE_DIR / "assets" / "branding" / "logo_watermark.png"
        )

        self.font_path = (
            RESOURCE_DIR / "assets" / "fonts" / "Marcellus-Regular.ttf"
        )

        self.output_dir = BASE_DIR / "generated" / "final"

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def add_footer(self, image_path, topic="poster"):

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Generated image not found: {image_path}"
            )

        if not self.watermark_path.exists():
            raise FileNotFoundError(
                f"Watermark logo not found: {self.watermark_path}"
            )

        base_image = Image.open(image_path).convert("RGBA")
        original_size = base_image.size
        w, h = base_image.size

        # -----------------------------------------------------
        # Find the calmest corner for the logo watermark
        # -----------------------------------------------------

        best_corner = self._find_calmest_corner(base_image)

        # -----------------------------------------------------
        # Place the logo watermark in that corner
        # -----------------------------------------------------

        watermark = Image.open(self.watermark_path)

        wm_target_w = int(w * 0.22)
        wm_h = int(watermark.height * (wm_target_w / watermark.width))
        watermark_resized = watermark.resize(
            (wm_target_w, wm_h), Image.LANCZOS
        )

        margin = int(w * 0.04)

        positions = {
            "top-left": (margin, margin),
            "top-right": (w - wm_target_w - margin, margin),
            "bottom-left": (margin, h - wm_h - margin),
        }

        wm_x, wm_y = positions[best_corner]

        base_image.alpha_composite(watermark_resized, (wm_x, wm_y))

        # -----------------------------------------------------
        # Phone number, fixed bottom-right, with a crisp stroke
        # so it stays readable regardless of what's behind it
        # -----------------------------------------------------

        draw = ImageDraw.Draw(base_image)

        font_size = int(w * 0.03)
        font = ImageFont.truetype(str(self.font_path), font_size)

        phone_text = f"WhatsApp / Call   {PHONE_NUMBER}"

        bbox = draw.textbbox((0, 0), phone_text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        phone_x = w - tw - margin
        phone_y = h - th - margin - int(h * 0.015)

        draw.text(
            (phone_x, phone_y),
            phone_text,
            font=font,
            fill=BRAND_GOLD,
            stroke_width=max(2, int(font_size * 0.08)),
            stroke_fill=STROKE_COLOR,
        )

        # -----------------------------------------------------
        # Safety check
        # -----------------------------------------------------

        final_image = base_image.convert("RGB")

        if final_image.size != original_size:
            raise RuntimeError(
                "Branding composition changed the original image dimensions."
            )

        # -----------------------------------------------------
        # Build filename
        # -----------------------------------------------------

        safe_topic = topic.strip().lower()
        safe_topic = re.sub(r'[<>:"/\\|?*]', "", safe_topic)
        safe_topic = re.sub(r"\s+", "_", safe_topic)
        safe_topic = safe_topic.strip("._")

        if not safe_topic:
            safe_topic = "untitled"

        filename = f"Umiya_{date.today()}_{safe_topic}_final.png"
        output_path = self.output_dir / filename

        final_image.save(output_path, "PNG")

        print(f"Final poster created: {output_path}")
        print(f"Watermark placed at: {best_corner}")

        return str(output_path)

    def _find_calmest_corner(self, base_image):
        """
        Scores the top-left, top-right, and bottom-left corners of the
        image for visual 'busyness' using Laplacian variance (a standard
        edge/detail measure — low score = calm/flat area, high score =
        cluttered area). Bottom-right is excluded since it's reserved
        for the phone number. Returns the name of the calmest corner.
        """

        w, h = base_image.size

        cv_image = cv2.cvtColor(
            np.array(base_image.convert("RGB")), cv2.COLOR_RGB2BGR
        )
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        box_w, box_h = int(w * 0.32), int(h * 0.18)

        candidates = {
            "top-left": (0, 0),
            "top-right": (w - box_w, 0),
            "bottom-left": (0, h - box_h),
        }

        scores = {}
        for name, (x, y) in candidates.items():
            region = gray[y:y + box_h, x:x + box_w]
            scores[name] = cv2.Laplacian(region, cv2.CV_64F).var()

        return min(scores, key=scores.get)
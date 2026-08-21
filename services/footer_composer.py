import re
from pathlib import Path
from datetime import date

from PIL import Image, ImageDraw, ImageFont

from utils.paths import BASE_DIR, RESOURCE_DIR


PHONE_NUMBER = "7829585834"

TEXT_COLOR = (245, 240, 228)      # Warm ivory
SHADOW_COLOR = (35, 25, 18, 160)


class FooterComposer:

    def __init__(self):

        self.logo_path = (
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
            raise FileNotFoundError(image_path)

        base_image = Image.open(image_path).convert("RGBA")

        original_size = base_image.size

        w, h = base_image.size

        margin = int(w * 0.04)

        draw = ImageDraw.Draw(base_image)

        # ==========================================================
        # LOGO (Always Top-Left)
        # ==========================================================

        logo = Image.open(self.logo_path).convert("RGBA")

        logo_width = int(w * 0.19)

        logo_height = int(
            logo.height * (logo_width / logo.width)
        )

        logo = logo.resize(
            (logo_width, logo_height),
            Image.LANCZOS
        )

        panel_padding = int(w * 0.018)

        panel_x = margin - panel_padding
        panel_y = margin - panel_padding

        panel_w = logo_width + panel_padding * 2
        panel_h = logo_height + panel_padding * 2

        panel = Image.new(
            "RGBA",
            (panel_w, panel_h),
            (248, 244, 236, 65)
        )

        base_image.alpha_composite(
            panel,
            (panel_x, panel_y)
        )

        base_image.alpha_composite(
            logo,
            (margin, margin)
        )

        # ==========================================================
        # CONTACT (Always Bottom-Right)
        # ==========================================================

        label_text = "WhatsApp / Call"

        number_text = PHONE_NUMBER

        label_font = ImageFont.truetype(
            str(self.font_path),
            int(w * 0.020)
        )

        number_font = ImageFont.truetype(
            str(self.font_path),
            int(w * 0.032)
        )

        label_bbox = draw.textbbox(
            (0, 0),
            label_text,
            font=label_font
        )

        number_bbox = draw.textbbox(
            (0, 0),
            number_text,
            font=number_font
        )

        label_w = label_bbox[2] - label_bbox[0]
        label_h = label_bbox[3] - label_bbox[1]

        number_w = number_bbox[2] - number_bbox[0]
        number_h = number_bbox[3] - number_bbox[1]

        line_gap = int(h * 0.008)

        block_w = max(label_w, number_w)

        block_h = label_h + line_gap + number_h

        block_x = w - block_w - margin

        block_y = h - block_h - margin

        label_x = block_x + (block_w - label_w)

        number_x = block_x + (block_w - number_w)

        shadow = 2

        # Label shadow
        draw.text(
            (label_x + shadow, block_y + shadow),
            label_text,
            font=label_font,
            fill=SHADOW_COLOR
        )

        # Label
        draw.text(
            (label_x, block_y),
            label_text,
            font=label_font,
            fill=TEXT_COLOR
        )

        # Number shadow
        draw.text(
            (
                number_x + shadow,
                block_y + label_h + line_gap + shadow
            ),
            number_text,
            font=number_font,
            fill=SHADOW_COLOR
        )

        # Number
        draw.text(
            (
                number_x,
                block_y + label_h + line_gap
            ),
            number_text,
            font=number_font,
            fill=TEXT_COLOR
        )

        # ==========================================================
        # SAVE
        # ==========================================================

        final_image = base_image.convert("RGB")

        if final_image.size != original_size:
            raise RuntimeError(
                "Image dimensions changed unexpectedly."
            )

        safe_topic = topic.strip().lower()

        safe_topic = re.sub(
            r'[<>:"/\\\\|?*]',
            "",
            safe_topic
        )

        safe_topic = re.sub(
            r"\\s+",
            "_",
            safe_topic
        )

        safe_topic = safe_topic.strip("._")

        if not safe_topic:
            safe_topic = "untitled"

        filename = (
            f"Umiya_{date.today()}_{safe_topic}_final.png"
        )

        output_path = self.output_dir / filename

        final_image.save(output_path, "PNG")

        print(f"Final poster created: {output_path}")

        return str(output_path)
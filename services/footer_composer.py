import re
from pathlib import Path
from datetime import date

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageStat
)
from utils.paths import BASE_DIR, RESOURCE_DIR

# --- Configuration ---
PHONE_NUMBER = "7829585834"
PRODUCTS_TEXT = "Plywood   |   Timber   |   Doors   |   Laminates   |   Hardware"
WHATSAPP_GREEN = (37, 211, 102)  # Standard WhatsApp Green

class FooterComposer:

    def __init__(self):
        # Paths to branding assets
        self.logo_path = (
            RESOURCE_DIR / "assets" / "branding" / "3.png"
        )
        self.whatsapp_icon_path = (
            RESOURCE_DIR / "assets" / "branding" / "WhatsApp.png"
        )

        # Output configuration
        self.output_dir = BASE_DIR / "generated" / "final"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_whatsapp_icon_png(self, size, target_color_tuple):
        """
        Loads the WhatsApp PNG and resizes it.
        """
        if not self.whatsapp_icon_path.exists():
            raise FileNotFoundError(f"WhatsApp icon not found at: {self.whatsapp_icon_path}")

        icon = Image.open(self.whatsapp_icon_path).convert("RGBA")
        icon = icon.resize((size, size), Image.LANCZOS)

        return icon

    def add_footer(self, image_path, topic="poster"):
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(image_path)

        source_image = Image.open(image_path).convert("RGBA")
        w, original_h = source_image.size
        margin = int(w * 0.055)

        # ----------------------------------------------------
        # 1. FOOTER CANVAS EXTENSION
        # ----------------------------------------------------
        strip_height = max(100, int(original_h * 0.09))
        h = original_h + strip_height

        # Start with a rich dark slate/espresso base
        base_image = Image.new("RGBA", (w, h), (14, 12, 11, 255))
        base_image.paste(source_image, (0, 0))

        # ----------------------------------------------------
        # 2. LOGO (ORIGINAL COLORS, CLEAN)
        # ----------------------------------------------------
        if self.logo_path.exists():
            original_logo = Image.open(self.logo_path).convert("RGBA")
            logo_width = int(w * 0.16)
            logo_height = int(original_logo.height * (logo_width / original_logo.width))
            logo = original_logo.resize((logo_width, logo_height), Image.LANCZOS)
            base_image.alpha_composite(logo, (margin, margin))

        # ----------------------------------------------------
        # 3. FOOTER BAR: WARM ESPRESSO WITH BRASS HAIRLINE
        # ----------------------------------------------------
        strip_y = original_h
        footer_overlay = Image.new("RGBA", (w, strip_height), (16, 13, 12, 255))
        f_draw = ImageDraw.Draw(footer_overlay)

        # Crisp, continuous warm gold hairline separator
        f_draw.line([(0, 0), (w, 0)], fill=(200, 160, 90, 255), width=2)
        base_image.paste(footer_overlay, (0, strip_y), footer_overlay)
        draw = ImageDraw.Draw(base_image)

        # ----------------------------------------------------
        # 4. FONTS & SIZING
        # ----------------------------------------------------
        title_font_size = max(16, int(strip_height * 0.22))
        sub_font_size = max(11, int(strip_height * 0.13))
        phone_font_size = max(18, int(strip_height * 0.24))

        def load_best(candidates, size):
            for name in candidates:
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    continue
            return ImageFont.load_default()

        company_font = load_best(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], title_font_size)
        products_font = load_best(["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"], sub_font_size)
        contact_font = load_best(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], phone_font_size)

        center_y = strip_y + (strip_height // 2)

        # ----------------------------------------------------
        # 5. RIGHT SECTION: CRISP WHATSAPP & PHONE
        # ----------------------------------------------------
        phone_bbox = draw.textbbox((0, 0), PHONE_NUMBER, font=contact_font)
        phone_w = phone_bbox[2] - phone_bbox[0]
        phone_h = phone_bbox[3] - phone_bbox[1]
        phone_offset_y = phone_bbox[1]

        icon_size = int(strip_height * 0.40)
        spacing = int(w * 0.014)

        right_block_w = icon_size + spacing + phone_w
        right_block_x = w - margin - right_block_w

        # Keep original clean WhatsApp icon so the glyph stays intact
        if self.whatsapp_icon_path.exists():
            raw_icon = Image.open(self.whatsapp_icon_path).convert("RGBA")
            raw_icon = raw_icon.resize((icon_size, icon_size), Image.LANCZOS)
            icon_y = center_y - (icon_size // 2)
            base_image.alpha_composite(raw_icon, (right_block_x, icon_y))

        # Optical center alignment for the numbers
        text_y = center_y - (phone_h // 2) - phone_offset_y
        draw.text(
            (right_block_x + icon_size + spacing, text_y),
            PHONE_NUMBER,
            font=contact_font,
            fill=(255, 255, 255)
        )

        # Subtle vertical separator line
        sep_x = right_block_x - int(w * 0.035)
        sep_h = int(strip_height * 0.40)
        draw.line(
            [(sep_x, center_y - sep_h // 2), (sep_x, center_y + sep_h // 2)],
            fill=(80, 70, 65, 200),
            width=1
        )

        # ----------------------------------------------------
        # 6. LEFT SECTION: BRANDING & PRODUCTS
        # ----------------------------------------------------
        company_text = "UMIYA TRADING COMPANY"
        comp_bbox = draw.textbbox((0, 0), company_text, font=company_font)
        comp_h = comp_bbox[3] - comp_bbox[1]
        comp_offset_y = comp_bbox[1]

        prod_bbox = draw.textbbox((0, 0), PRODUCTS_TEXT, font=products_font)
        prod_h = prod_bbox[3] - prod_bbox[1]
        prod_offset_y = prod_bbox[1]

        gap = int(strip_height * 0.10)
        total_block_h = comp_h + gap + prod_h
        block_top = center_y - (total_block_h // 2)

        # Pure white, high-contrast company title
        draw.text(
            (margin, block_top - comp_offset_y),
            company_text,
            font=company_font,
            fill=(255, 255, 255)
        )

        # Warm muted ivory for the product list
        draw.text(
            (margin, block_top + comp_h + gap - prod_offset_y),
            PRODUCTS_TEXT,
            font=products_font,
            fill=(210, 200, 185)
        )

        # ----------------------------------------------------
        # 7. SAVE OUTPUT (SANITIZED & SAFE FOR WINDOWS)
        # ----------------------------------------------------
        final_image = base_image.convert("RGB")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Strip all whitespace, newlines, and illegal Windows characters
        clean_topic = str(topic).strip()
        safe_topic = re.sub(r'[\r\n\t<>:"/\\|?*]+', '', clean_topic)
        safe_topic = re.sub(r'\s+', '_', safe_topic).strip('._').lower()
        if not safe_topic:
            safe_topic = "poster"

        filename = f"Umiya_{date.today()}_{safe_topic}_final.png"
        output_path = (self.output_dir / filename).resolve()

        # Save with explicit Path object
        final_image.save(output_path, format="PNG")
        print(f"Final poster created: {output_path}")
        return str(output_path)
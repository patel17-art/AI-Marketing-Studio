import re
from pathlib import Path
from datetime import date

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageStat
)

# Assuming these are correctly set up in your environment
# RESOURCE_DIR should point to the directory containing 'assets'
from utils.paths import BASE_DIR, RESOURCE_DIR

# --- Configuration ---
PHONE_NUMBER = "7829585834"
PRODUCTS_TEXT = "Plywood   |   Timber   |   Doors   |   Laminates   |   Hardware"
WHATSAPP_GREEN = (37, 211, 102) # Standard WhatsApp Green

class FooterComposer:

    def __init__(self):
        # Paths to branding assets
        self.logo_path = (
            RESOURCE_DIR / "assets" / "branding" / "logo_transparent_2.png"
        )
        # New path for the PNG icon
        self.whatsapp_icon_path = (
            RESOURCE_DIR / "assets" / "branding" / "WhatsApp.png"
        )

        # Output configuration
        self.output_dir = BASE_DIR / "generated" / "final"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_whatsapp_icon_png(self, size, target_color_tuple):
        """
        Loads the WhatsApp PNG, resizes it, and optionally recolors it
        to match the footer text if it's a monochrome icon.
        """
        if not self.whatsapp_icon_path.exists():
            raise FileNotFoundError(f"WhatsApp icon not found at: {self.whatsapp_icon_path}")

        icon = Image.open(self.whatsapp_icon_path).convert("RGBA")
        icon = icon.resize((size, size), Image.LANCZOS)

        # Optional: If you downloaded a pure white icon and want to color it
        # to match the ivory text, keep this block. If you downloaded a colored
        # green icon, comment this block out.
        # --- Recoloring Block ---
        # r, g, b, a = icon.split()
        # target_color = target_color_tuple[:3] # Ensure RGB
        # icon = Image.merge("RGBA", (
        #     Image.new("L", icon.size, target_color[0]),
        #     Image.new("L", icon.size, target_color[1]),
        #     Image.new("L", icon.size, target_color[2]),
        #     a # Keep original alpha/transparency
        # ))
        # ------------------------

        return icon

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
        # LOGO (Top Left, existing code)
        # ==========================================================
        if self.logo_path.exists():
            logo = Image.open(self.logo_path).convert("RGBA")
            logo_width = int(w * 0.155)
            logo_height = int(logo.height * (logo_width / logo.width))
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            panel_padding = int(w * 0.014)
            panel_x = margin - panel_padding
            panel_y = margin - panel_padding
            panel_w = logo_width + panel_padding * 2
            panel_h = logo_height + panel_padding * 2

            logo_crop = base_image.crop((
                max(0, panel_x), max(0, panel_y),
                min(w, panel_x + panel_w), min(h, panel_y + panel_h)
            ))
            stat = ImageStat.Stat(logo_crop)
            brightness = sum(stat.mean[:3]) / 3
            variation = sum(stat.stddev[:3]) / 3

            if brightness < 140 or variation > 35:
                overlay = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rounded_rectangle(
                    (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                    radius=int(w * 0.016),
                    fill=(248, 244, 236, 55)
                )
                base_image.alpha_composite(overlay)

            base_image.alpha_composite(logo, (margin, margin))

        # ==========================================================
        # FOOTER STRIP & BRAND SIGNATURE
        # ==========================================================
        strip_height = int(h * 0.095)
        strip_y = h - strip_height

        footer_sample = base_image.crop((0, strip_y, w, h))
        footer_brightness = sum(ImageStat.Stat(footer_sample).mean[:3]) / 3

        if footer_brightness < 140:
            strip_fill = (18, 18, 18, 150)
            footer_text_color = (245, 240, 228) # Warm Ivory
            divider_color = (255, 255, 255, 100)
        else:
            strip_fill = (248, 244, 236, 175)
            footer_text_color = (35, 25, 18) # Dark Brown
            divider_color = (35, 25, 18, 90)

        overlay = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle((0, strip_y, w, h), fill=strip_fill)
        overlay_draw.line(
            (0, strip_y, w, strip_y),
            fill=(196, 154, 78, 220), # Gold line
            width=max(2, int(w * 0.002))
        )
        base_image.alpha_composite(overlay)

        draw = ImageDraw.Draw(base_image)

        # Load Fonts
        font_path = "DejaVuSerif.ttf" # Ensure this font is available
        try:
            company_font = ImageFont.truetype(font_path, int(w * 0.023))
            products_font = ImageFont.truetype(font_path, int(w * 0.016))
            contact_font = ImageFont.truetype(font_path, int(w * 0.022))
        except Exception:
            company_font = products_font = contact_font = ImageFont.load_default()

        center_y = strip_y + strip_height // 2

        # ---- Left side: company name + product list ----
        company_text = "UMIYA TRADING COMPANY"
        company_bbox = draw.textbbox((0, 0), company_text, font=company_font)
        company_h = company_bbox[3] - company_bbox[1]

        products_bbox = draw.textbbox((0, 0), PRODUCTS_TEXT, font=products_font)
        products_h = products_bbox[3] - products_bbox[1]

        line_gap = int(h * 0.008)
        block_h = company_h + line_gap + products_h
        block_top = center_y - block_h // 2

        draw.text((margin, block_top), company_text, font=company_font, fill=footer_text_color)
        draw.text((margin, block_top + company_h + line_gap), PRODUCTS_TEXT, font=products_font, fill=footer_text_color)

        # ---- Center Divider ----
        divider_x = w // 2
        draw.line(
            (divider_x, strip_y + int(strip_height * 0.22), divider_x, h - int(strip_height * 0.22)),
            fill=divider_color,
            width=2
        )

        # ---- Right side: WhatsApp Icon (PNG) + Phone Number ----
        phone_bbox = draw.textbbox((0, 0), PHONE_NUMBER, font=contact_font)
        phone_h = phone_bbox[3] - phone_bbox[1]
        phone_w = phone_bbox[2] - phone_bbox[0]

        gap = int(w * 0.012)
        icon_size = int(strip_height * 0.45) # Size of the icon

        # 1. Load the actual PNG icon using the new method
        whatsapp_icon = self._load_whatsapp_icon_png(icon_size, footer_text_color)

        icon_x = w - margin - phone_w - icon_size - gap
        icon_y = center_y - icon_size // 2

        # 2. Paste the icon using alpha_composite
        base_image.alpha_composite(whatsapp_icon, (icon_x, icon_y))

        # 3. Draw the text (ensure draw object is fresh if recoloring was used)
        draw = ImageDraw.Draw(base_image)
        draw.text(
            (icon_x + icon_size + gap, center_y - phone_h // 2),
            PHONE_NUMBER,
            font=contact_font,
            fill=footer_text_color
        )

        # ==========================================================
        # SAVE
        # ==========================================================
        final_image = base_image.convert("RGB")
        if final_image.size != original_size:
            raise RuntimeError("Image dimensions changed unexpectedly.")

        safe_topic = re.sub(r'[<>:"/\\\\|?*]', "", topic.strip().lower())
        safe_topic = re.sub(r"\s+", "_", safe_topic).strip("._")
        filename = f"Umiya_{date.today()}_{safe_topic or 'untitled'}_final.png"
        output_path = self.output_dir / filename

        final_image.save(output_path, "PNG")
        print(f"Final poster created: {output_path}")
        return str(output_path)
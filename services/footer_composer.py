from datetime import date
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont
from utils.paths import BASE_DIR, RESOURCE_DIR

PHONE_NUMBER = "7829585834"
COMPANY_NAME = "UMIYA TRADING COMPANY"
# Italian-inspired architectural material styling
PRODUCTS_TEXT = "Plywood  ·  Timber  ·  Doors  ·  Laminates  ·  Hardware"


class FooterComposer:

  def __init__(self):
    self.branding_dir = RESOURCE_DIR / "assets" / "branding"
    self.utc_logo_path = self.branding_dir / "utc_logo.png"
    self.fallback_logo_path = self.branding_dir / "3.png"
    self.whatsapp_icon_path = self.branding_dir / "WhatsApp.png"

    self.output_dir = BASE_DIR / "generated" / "final"
    self.output_dir.mkdir(parents=True, exist_ok=True)

  def _load_font(self, font_names, size):
    for name in font_names:
      try:
        return ImageFont.truetype(name, size)
      except Exception:
        continue
    return ImageFont.load_default()

  def add_footer(self, image_path: Path | str, topic: str = "poster") -> Path:
    image_path = Path(image_path)
    if not image_path.exists():
      raise FileNotFoundError(f"Image not found: {image_path}")

    source_image = Image.open(image_path).convert("RGBA")
    w, original_h = source_image.size

    # 1. Canvas Setup
    strip_height = max(130, int(original_h * 0.115))
    h = original_h + strip_height
    margin_x = int(w * 0.04)

    base_image = Image.new("RGBA", (w, h), (18, 15, 14, 255))
    base_image.paste(source_image, (0, 0))

    strip_y = original_h
    center_y = strip_y + (strip_height // 2)

    # 2. Base Tone Gradient & 1px Accent Hairline
    footer_bar = Image.new("RGBA", (w, strip_height))
    f_draw = ImageDraw.Draw(footer_bar)
    for y in range(strip_height):
      factor = y / float(strip_height)
      r = int(24 * (1 - factor) + 14 * factor)
      g = int(20 * (1 - factor) + 11 * factor)
      b = int(18 * (1 - factor) + 10 * factor)
      f_draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Clean champagne top border
    f_draw.line([(0, 0), (w, 0)], fill=(215, 175, 110, 230), width=1)
    base_image.paste(footer_bar, (0, strip_y))

    draw = ImageDraw.Draw(base_image)

    # ----------------------------------------------------
    # 3. RIGHT SECTION: CLEAN WHATSAPP + PHONE (NO PILL CAPSULE)
    # ----------------------------------------------------
    phone_font_size = max(13, int(strip_height * 0.16))
    contact_font = self._load_font(
        ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], phone_font_size
    )

    phone_bbox = draw.textbbox((0, 0), PHONE_NUMBER, font=contact_font)
    phone_w = phone_bbox[2] - phone_bbox[0]
    phone_h = phone_bbox[3] - phone_bbox[1]

    icon_size = max(18, int(strip_height * 0.24))
    gap_icon_text = int(w * 0.010)

    right_content_w = icon_size + gap_icon_text + phone_w
    right_x = w - margin_x - right_content_w

    if self.whatsapp_icon_path.exists():
      raw_icon = (
          Image.open(self.whatsapp_icon_path)
          .convert("RGBA")
          .resize((icon_size, icon_size), Image.Resampling.LANCZOS)
      )
      base_image.alpha_composite(
          raw_icon, (right_x, center_y - (icon_size // 2))
      )

    draw.text(
        (
            right_x + icon_size + gap_icon_text,
            center_y - (phone_h // 2) - phone_bbox[1],
        ),
        PHONE_NUMBER,
        font=contact_font,
        fill=(255, 255, 255),
    )

    # Architectural vertical partition divider
    sep_right_x = right_x - int(w * 0.028)
    div_h = int(strip_height * 0.44)
    draw.line(
        [
            (sep_right_x, center_y - div_h // 2),
            (sep_right_x, center_y + div_h // 2),
        ],
        fill=(190, 160, 120, 130),
        width=1,
    )

    # ----------------------------------------------------
    # 4. LEFT SECTION: LOGO
    # ----------------------------------------------------
    curr_x = margin_x
    logo_file = (
        self.utc_logo_path
        if self.utc_logo_path.exists()
        else self.fallback_logo_path
    )

    if logo_file.exists():
      emblem = Image.open(logo_file).convert("RGBA")
      target_h = int(strip_height * 0.72)
      target_w = int(emblem.width * (target_h / emblem.height))
      emblem = emblem.resize((target_w, target_h), Image.Resampling.LANCZOS)
      base_image.alpha_composite(
          emblem, (curr_x, center_y - (target_h // 2))
      )
      curr_x += target_w + int(w * 0.022)

    # ----------------------------------------------------
    # 5. MIDDLE SECTION: ELEGANT SERIF & ITALIC FORMAT
    # ----------------------------------------------------
    max_text_w = sep_right_x - curr_x - int(w * 0.03)

    # Company name font (Classic luxury serif)
    company_font_size = max(14, int(strip_height * 0.19))
    company_font = self._load_font(
        ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], company_font_size
    )

    while company_font_size > 11:
      c_bbox = draw.textbbox((0, 0), COMPANY_NAME, font=company_font)
      if (c_bbox[2] - c_bbox[0]) <= max_text_w:
        break
      company_font_size -= 1
      company_font = self._load_font(
          ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], company_font_size
      )

    # Italian-style editorial italic font for the products subtext
    products_font_size = max(11, int(strip_height * 0.13))
    products_font = self._load_font(
        ["georgiai.ttf", "timesi.ttf", "cambriai.ttf", "segoeuii.ttf"],
        products_font_size,
    )

    display_products = PRODUCTS_TEXT
    while products_font_size > 8:
      p_bbox = draw.textbbox((0, 0), display_products, font=products_font)
      if (p_bbox[2] - p_bbox[0]) <= max_text_w:
        break
      if "  ·  " in display_products:
        display_products = display_products.replace("  ·  ", " · ")
      products_font_size -= 1
      products_font = self._load_font(
          ["georgiai.ttf", "timesi.ttf", "cambriai.ttf", "segoeuii.ttf"],
          products_font_size,
      )

    comp_bbox = draw.textbbox((0, 0), COMPANY_NAME, font=company_font)
    comp_h = comp_bbox[3] - comp_bbox[1]

    prod_bbox = draw.textbbox((0, 0), display_products, font=products_font)
    prod_h = prod_bbox[3] - prod_bbox[1]

    spacing = int(strip_height * 0.055)
    total_h = comp_h + spacing + prod_h
    start_y = center_y - (total_h // 2)

    # Company title in warm champagne gold
    draw.text(
        (curr_x, start_y - comp_bbox[1]),
        COMPANY_NAME,
        font=company_font,
        fill=(245, 230, 205),
    )

    # Subtext in warm Italian-style italic serifs
    draw.text(
        (curr_x, start_y + comp_h + spacing - prod_bbox[1]),
        display_products,
        font=products_font,
        fill=(218, 205, 185),
    )

    # 6. Save Output
    safe_topic = re.sub(r'[\r\n\t<>:"/\\|?*]+', "", str(topic).strip())
    safe_topic = re.sub(r"\s+", "_", safe_topic).strip("._").lower() or "poster"
    filename = f"Umiya_{date.today()}_{safe_topic}_final.png"
    output_path = self.output_dir / filename

    base_image.convert("RGB").save(output_path, "PNG", quality=95)
    return output_path
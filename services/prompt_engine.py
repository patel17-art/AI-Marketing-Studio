from pathlib import Path
from services.style_rotator import StyleRotator
from utils.paths import RESOURCE_DIR

FESTIVAL_MEDIUM = [
    "A rich, atmospheric commercial editorial photograph captured in soft morning daylight and warm ambient candlelight.",
    "A luxury architectural interior photograph showing an authentic festive entrance setting with warm directional light.",
    "An intimate, high-end still-life photograph featuring rich textures, polished surfaces, and authentic festival decorations.",
    "A wide environmental festival scene inside a tastefully designed modern home with natural woodwork.",
]

FESTIVAL_FRAMING = [
    "Composed with the festive cultural elements resting elegantly across the lower table and floor, leaving an expansive, clean, softly lit wall above.",
    "A low-angle perspective looking across a polished wood threshold adorned with authentic festival offerings, with calm upper wall space.",
    "An asymmetric composition with ornate decorations framing the right and lower edges, leaving generous negative space across the upper area.",
]

FESTIVAL_BRAND_SIGNATURE = [
    "Subtly incorporate fine architectural woodwork—such as a carved teakwood door frame, polished timber console, or warm fluted wood paneling.",
    "Feature a warm wooden threshold or rich walnut tabletop as the foundation for the festive decorations.",
    "Let the environment feature warm amber and honey-toned natural wood grains that complement the festive colors.",
]

FESTIVAL_TYPOGRAPHY = [
    "Render the festival title in regal, high-contrast serif typography with subtle gold leaf luster, paired with an elegant, crisp multi-line greeting below.",
    "Render the festival title in modern calligraphic lettering with refined gold accents, accompanied by a clean, legible festive blessing.",
    "Render the festival title in an understated luxury editorial typeface in warm bronze, paired with a balanced, readable greeting.",
]

# Varied visual environments to prevent repetitive outputs
EDUCATIONAL_MEDIUM = [
    "A clean architectural flat-lay composition: samples arranged on an architect's wooden drafting table alongside blueprints, brass calipers, and natural morning light.",
    "A real-world luxury home interior during the finishing stages: clean wooden cabinetry, sunlight pouring through large windows, with material samples displayed on a kitchen island.",
    "A bright, contemporary materials library with minimalist shelves, displaying timber and laminate swatches against warm microcement walls.",
    "A high-end craftsmanship workshop: a pristine solid wood workbench with traditional hand planes, clean wood shavings, and neatly cut material cross-sections.",
    "A modern studio catalog layout: a floating architectural spec card overlaying a naturally lit scene of the materials.",
]

EDUCATIONAL_FRAMING = [
    "A top-down architectural flat-lay view, balancing the text card on one side and tactile material samples across the other.",
    "An editorial eye-level perspective focusing on the material texture in the foreground, with the room softly out of focus in the background.",
    "A clean, dynamic 45-degree isometric view highlighting the depth, cut layers, and fine finish of the product.",
]

EDUCATIONAL_TYPOGRAPHY = [
    "Clean, structured Swiss sans-serif typography in dark charcoal with crisp divider lines.",
    "Modern architectural grotesque typography with bold section headers and high legibility.",
    "Refined editorial sans-serif headers paired with neat, compact technical spec cards.",
]

EDUCATIONAL_TEMPLATES = [
    "educational_split",
    "educational_blended",
]

class PromptEngine:

  def __init__(self, business):
    self.business = business
    self.style_rotator = StyleRotator()

  def build_prompt(self, topic, category):
    category = category.lower()
    clean_topic = topic.strip().rstrip("?.!")

    if category == "festival":
      template_name = "festival"
      medium = self.style_rotator.next_style(
          "festival_medium", FESTIVAL_MEDIUM
      )
      framing = self.style_rotator.next_style(
          "festival_framing", FESTIVAL_FRAMING
      )
      signature = self.style_rotator.next_style(
          "festival_signature", FESTIVAL_BRAND_SIGNATURE
      )
      typography = self.style_rotator.next_style(
          "festival_typography", FESTIVAL_TYPOGRAPHY
      )
      style_spark = f"{medium} {framing} {signature}"

    else:
      # Alternates between 'educational_split' and 'educational_blended' every time
      template_name = self.style_rotator.next_style(
          "educational_template", EDUCATIONAL_TEMPLATES
      )

      medium = self.style_rotator.next_style(
          "educational_medium", EDUCATIONAL_MEDIUM
      )
      framing = self.style_rotator.next_style(
          "educational_framing", EDUCATIONAL_FRAMING
      )
      typography = self.style_rotator.next_style(
          "educational_typography", EDUCATIONAL_TYPOGRAPHY
      )
      style_spark = f"{medium} {framing}"

    template_file = RESOURCE_DIR / "templates" / f"{template_name}.txt"
    template = template_file.read_text(encoding="utf-8")

    prompt = template
    prompt = prompt.replace("{company_name}", self.business["company_name"])
    prompt = prompt.replace("{topic}", clean_topic)
    prompt = prompt.replace("{style_spark}", style_spark)
    prompt = prompt.replace("{typography_style}", typography)

    return prompt
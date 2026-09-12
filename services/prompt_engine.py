from services.style_rotator import StyleRotator
from pathlib import Path

from utils.paths import RESOURCE_DIR


# Style is now built from independent axes (medium, framing, brand
# signature) that rotate on their own cycles and get combined, instead
# of one flat list of pre-written sentences. A flat list of 7 lines
# repeats its *combination* every 7 generations; three independent
# axes of ~6 options each gives 200+ unique combinations before any
# repeat, which is what actually kills the "every poster looks the
# same" problem, since the previous approach mostly varied lighting
# mood while every image still converged on the same default
# devotional-poster medium and framing.

# MEDIUM: what the image is *made of*. This is the single biggest
# lever for not looking like every other AI festival poster — but
# painterly/illustrated media (gouache, watercolor, linocut) turned
# out to be its own obvious "AI art" tell, arguably worse than the
# generic photoreal-idol look this was meant to avoid. Pulled those
# out. What actually reads as "designed by a human" is photographic
# realism or clean, deliberate flat graphic design — not a generated
# painting.
FESTIVAL_MEDIUM = [
    "Render this as a natural, photorealistic photograph with authentic studio lighting and real depth of field.",
    "Render this as a photorealistic photograph shot in soft natural window light, with authentic shadow falloff.",
    "Render this as a polished editorial photograph, the kind used in a premium home-decor magazine spread.",
    "Render this as a composed product-photography style shot with shallow depth of field and realistic textures.",
    "Render this as a clean, modern flat-graphic design with bold simplified shapes and confident negative space — the kind a professional designer would lay out in Illustrator, not a painted scene.",
    "Render this as an elegant emblem-style graphic design using clean vector linework in gold and ivory, echoing fine engraved metalwork.",
]

# FRAMING: how the shot is composed, to break the default
# "deity statue centered on a pedestal" layout almost every
# competitor's AI poster uses.
FESTIVAL_FRAMING = [
    "Compose it asymmetrically, with the main subject off-center and generous negative space.",
    "Use a top-down flat-lay composition of festival elements rather than a front-facing scene.",
    "Frame it as a close, intimate crop on one symbolic detail rather than a full wide scene.",
    "Use a wide environmental composition that shows the subject within a real, lived-in room.",
    "Use a layered composition with foreground festive elements slightly out of focus.",
]

# BRAND SIGNATURE: a subtle, recurring visual thread tied to the
# business itself (timber/woodwork) so the posters build a
# recognizable identity over time instead of being generic
# devotional stock art that happens to have a logo stamped on it.
FESTIVAL_BRAND_SIGNATURE = [
    "Include a subtle warm wood-grain texture somewhere in the background or a frame edge.",
    "Include a small, tasteful piece of natural timber or a wooden threshold/door in the scene.",
    "Let the color grade lean into warm amber and walnut tones, echoing fine woodwork.",
    "Work in a faint tree-branch or leaf motif in the decorative elements, echoing a tree-of-life shape.",
]

EDUCATIONAL_MEDIUM = [
    "Use a bright modern showroom setting, shot photorealistically.",
    "Use a naturally lit luxury home interior, shot photorealistically.",
    "Use a clean top-down product flat-lay.",
    "Use a close-up macro shot of material texture and grain.",
    "Use a minimalist editorial magazine-style layout.",
    "Use a warm, hands-on workshop/craftsmanship scene.",
]

EDUCATIONAL_FRAMING = [
    "Compose with strong asymmetry and generous negative space for the caption area.",
    "Use a centered, symmetrical product-hero composition.",
    "Use a diagonal composition that leads the eye through the frame.",
    "Frame it as a tight, detail-focused crop rather than a wide establishing shot.",
]

# TYPOGRAPHY: Controls the font aesthetic and lettering treatment
# directly rendered in the open negative space.
FESTIVAL_TYPOGRAPHY = [
    "Render the greeting in bespoke modern calligraphy with elegant flourishes and liquid gold luster.",
    "Render the greeting in a regal, high-contrast display serif with subtle ligatures and warm bronze foil finish.",
    "Render the greeting in clean architectural debossed lettering cut into the wall plaster, catching diagonal sunlight.",
    "Render the greeting in handcrafted vintage sign-painted serif typography with warm gold leaf leafing.",
    "Render the greeting in minimalist luxury editorial lettering with wide tracking and refined gold foil edges.",
]

# FESTIVE MESSAGES: Rotating brand blessings that complement the topic
# without sounding like an overt sales pitch.
FESTIVAL_MESSAGES = [
    "May new beginnings bring prosperity, strength, and timeless harmony to your home.",
    "Crafting warm foundations and auspicious spaces for you and your family.",
    "May divine blessings fill your home with strength, peace, and lasting beauty.",
    "Celebrating the beauty of craftsmanship, heritage, and joyous new beginnings.",
]


class PromptEngine:
    def __init__(self, business):
        self.business = business
        self.style_rotator = StyleRotator()

    def build_prompt(self, topic, category):
        template_file = (
            RESOURCE_DIR / "templates"
            / f"{category.lower()}.txt"
        )
        template = template_file.read_text(
            encoding="utf-8"
        )

        category = category.lower()

        if category == "festival":
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
            message = self.style_rotator.next_style(
                "festival_message", FESTIVAL_MESSAGES
            )
            style_spark = f"{medium} {framing} {signature}"
        else:
            medium = self.style_rotator.next_style(
                "educational_medium", EDUCATIONAL_MEDIUM
            )
            framing = self.style_rotator.next_style(
                "educational_framing", EDUCATIONAL_FRAMING
            )
            style_spark = f"{medium} {framing}"
            typography = "Clean, modern architectural sans-serif typography."
            message = ""

        prompt = template
        prompt = prompt.replace(
            "{company_name}", self.business["company_name"]
        )
        prompt = prompt.replace(
            "{topic}", topic
        )
        prompt = prompt.replace(
            "{style_spark}", style_spark
        )
        prompt = prompt.replace(
            "{typography_style}", typography
        )
        prompt = prompt.replace(
            "{greeting_message}", message
        )

        return prompt
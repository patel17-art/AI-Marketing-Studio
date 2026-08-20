import random
from pathlib import Path

from utils.paths import RESOURCE_DIR


# Light, one-sentence nudges — just enough to keep the prompt text
# from being identical every time, without dictating exact scenes.
FESTIVAL_STYLE_SPARKS = [
    "For this one, lean toward a bold, flat, illustrated graphic-design style with rich ornamental line art.",
    "For this one, lean toward a warm, photorealistic scene.",
    "For this one, lean toward a minimal, elegant layout with generous negative space.",
    "For this one, lean toward a vibrant, traditional Indian art style — mandala patterns, folk-art motifs, or rangoli-inspired detail.",
    "For this one, lean toward a modern, editorial magazine-style layout.",
]

EDUCATIONAL_STYLE_SPARKS = [
    "For this one, lean toward a close-up, tactile focus on the material itself.",
    "For this one, lean toward a wide, spacious interior showing the product naturally placed in a room.",
    "For this one, lean toward a clean, minimal flat-lay of the product and related materials.",
    "For this one, lean toward a detailed infographic-style layout explaining the product's features.",
    "For this one, lean toward a warm lifestyle scene showing the product in everyday use.",
]


class PromptEngine:
    def __init__(self, business):
        self.business = business

    def build_prompt(self, topic, category):
        template_file = (
            RESOURCE_DIR / "templates"
            / f"{category.lower()}.txt"
        )
        template = template_file.read_text(
            encoding="utf-8"
        )

        if category.lower() == "festival":
            style_spark = random.choice(FESTIVAL_STYLE_SPARKS)
        else:
            style_spark = random.choice(EDUCATIONAL_STYLE_SPARKS)

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

        return prompt
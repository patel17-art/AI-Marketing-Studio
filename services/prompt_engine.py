from services.style_rotator import StyleRotator
from pathlib import Path

from utils.paths import RESOURCE_DIR


# Light, one-sentence nudges — just enough to keep the prompt text
# from being identical every time, without dictating exact scenes.
# Includes both style-family AND brightness/mood variety, since
# both were converging to sameness before.

FESTIVAL_STYLE_SPARKS = [
    "Use a bright daylight festival atmosphere with warm natural lighting.",
    "Use an elegant illustrated design with ornamental line art.",
    "Use a clean modern poster with generous whitespace.",
    "Use a colorful folk-art inspired festival design.",
    "Use a premium editorial-style composition.",
    "Use soft pastel festive tones.",
    "Use a luxurious gold-and-ivory celebration."
]


EDUCATIONAL_STYLE_SPARKS = [
    "Use a bright modern showroom.",
    "Use a naturally lit luxury home interior.",
    "Use a clean product flat-lay.",
    "Use a close-up material texture shot.",
    "Use a minimalist editorial layout.",
    "Use a workshop craftsmanship scene."
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

        if category.lower() == "festival":
            style_spark = self.style_rotator.next_style(
                "festival",
                FESTIVAL_STYLE_SPARKS
            )
        else:
            style_spark = self.style_rotator.next_style(
                "educational",
                EDUCATIONAL_STYLE_SPARKS
            )

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
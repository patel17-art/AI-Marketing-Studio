import json

from utils.paths import RESOURCE_DIR


class ConfigManager:

    def __init__(self):

        self.business_file = (
            RESOURCE_DIR
            / "config"
            / "business.json"
        )

    def load_business(self):

        with open(
            self.business_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)
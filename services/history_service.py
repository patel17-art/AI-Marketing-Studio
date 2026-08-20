from pathlib import Path
from datetime import datetime

from utils.paths import BASE_DIR


class HistoryService:

    def __init__(self):

        self.history_folder = BASE_DIR / "history" / "prompts"

        self.history_folder.mkdir(parents=True, exist_ok=True)

    def save(self, prompt: str):

        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.txt"
        )

        file = self.history_folder / filename

        file.write_text(
            prompt,
            encoding="utf-8"
        )

        return file
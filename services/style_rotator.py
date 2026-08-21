from pathlib import Path
import json

from utils.paths import BASE_DIR


class StyleRotator:

    def __init__(self):

        self.state_file = BASE_DIR / "config" / "style_state.json"

        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.state_file.exists():
            self._save({"festival": 0, "educational": 0})

    def next_style(self, category, styles):

        category = category.lower()

        state = self._load()

        index = state.get(category, 0)

        style = styles[index % len(styles)]

        state[category] = (index + 1) % len(styles)

        self._save(state)

        return style

    def _load(self):

        with open(self.state_file, "r") as f:
            return json.load(f)

    def _save(self, state):

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
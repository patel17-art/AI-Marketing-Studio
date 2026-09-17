from utils.config import ConfigManager
from services.prompt_engine import PromptEngine
from services.browser_service import BrowserService
from services.history_service import HistoryService
from services.clipboard_service import ClipboardService
from services.footer_composer import FooterComposer


class MarketingService:

    def __init__(self):

        config = ConfigManager()

        self.business = config.load_business()

        self.prompt_engine = PromptEngine(self.business)

        self.browser = BrowserService()

        self.history = HistoryService()

        self.footer_composer = FooterComposer()

    def generate(self, request):

        prompt = self.prompt_engine.build_prompt(
            request.topic,
            request.post_type,
            educational_layout=getattr(request, "educational_layout", None),
        )

        ClipboardService.copy(prompt)

        self.history.save(prompt)

        raw_image_path = self.browser.send_prompt(
            prompt,
            request.topic
        )

        final_image_path = self.footer_composer.add_footer(
            raw_image_path,
            topic=request.topic
        )

        return final_image_path

    def open_chatgpt(self):

        self.browser.open_chatgpt()
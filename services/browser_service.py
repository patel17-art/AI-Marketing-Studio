from playwright.sync_api import sync_playwright
import time
from datetime import datetime

from utils.paths import BASE_DIR


class BrowserService:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        if self.browser:
            return

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.connect_over_cdp(
            "http://localhost:9222"
        )

        self.context = self.browser.contexts[0]

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

    def open_chatgpt(self):

        self.start()

        self.page = self.context.pages[0]

        self.page.goto("https://chatgpt.com")

        self.page.bring_to_front()

        self.page.wait_for_timeout(3000)


    def send_prompt(self, prompt, topic):

        self.open_chatgpt()

        print("ChatGPT opened.")
        print("Waiting for message box...")

        self.page.wait_for_timeout(2000)

        # Capture generated images that already exist
        existing_images = set()

        images = self.page.locator(
            'img[alt^="Generated image"]'
        )

        for i in range(images.count()):

            src = images.nth(i).get_attribute("src")

            if src:
                existing_images.add(src)

        print(
            f"Existing generated images: {len(existing_images)}"
        )

        # Find ChatGPT editor
        editor = self.page.locator(
            '[contenteditable="true"][role="textbox"]'
        ).first

        editor.wait_for(
            state="visible",
            timeout=30000
        )

        print("Message box found.")

        editor.click()

        editor.fill(prompt)

        print("Prompt inserted.")

        self.page.wait_for_timeout(1000)

        editor.press("Enter")

        print("Prompt submitted.")

        # Wait for the NEW generated image
        image_url = self.wait_for_new_image(existing_images)

        print("FINAL IMAGE URL:")
        print(image_url)

        output_dir = BASE_DIR / "generated" / "raw"

        output_dir.mkdir(parents=True, exist_ok=True)

        filename = self.create_filename(topic)

        output_path = output_dir / filename

        self.download_image(
            image_url,
            output_path
        )

        return output_path


    def wait_for_new_image(
        self,
        existing_images,
        timeout=180
    ):

        print("Waiting for new generated image...")

        start_time = time.time()

        while time.time() - start_time < timeout:

            images = self.page.locator(
                'img[alt^="Generated image"]'
            )

            count = images.count()

            for i in range(count):

                image = images.nth(i)

                try:

                    if not image.is_visible():
                        continue

                    src = image.get_attribute("src")

                    if not src:
                        continue

                    if src not in existing_images:

                        print(
                            "New generated image detected!"
                        )

                        print(
                            "Image URL:",
                            src
                        )

                        return src

                except Exception:
                    continue

            elapsed = int(
                time.time() - start_time
            )

            print(
                f"Still waiting... {elapsed}s"
            )

            self.page.wait_for_timeout(2000)

        raise TimeoutError(
            "ChatGPT did not generate a new image "
            f"within {timeout} seconds."
        )


    def download_image(self, image_url, output_path):

        print("Downloading generated image...")

        last_error = None
        for attempt in range(3):
            try:
                response = self.page.request.get(image_url, timeout=90000)
                break
            except Exception as e:
                last_error = e
                print(f"Download attempt {attempt + 1} failed, retrying...")
        else:
            raise last_error

        if not response.ok:
            raise RuntimeError(
                f"Image download failed. HTTP status: {response.status}"
            )

        with open(output_path, "wb") as file:
            file.write(response.body())

        print("Image downloaded successfully.")
        print(f"Saved to: {output_path}")

        return output_path


    def create_filename(self, topic):

        date = datetime.now().strftime("%Y-%m-%d")

        filename = topic.strip()

        filename = filename.lower()

        # Replace spaces with underscores
        filename = filename.replace(" ", "_")

        # Keep only safe filename characters
        filename = "".join(
            char for char in filename
            if char.isalnum() or char in "_-"
        )

        # Avoid excessively long filenames
        filename = filename[:80]

        return f"Umiya_{date}_{filename}.png"
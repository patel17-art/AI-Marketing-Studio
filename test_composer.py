from pathlib import Path
from services.footer_composer import FooterComposer

# 1. Point to your already downloaded raw image
raw_image_dir = Path("generated/raw")
raw_images = list(raw_image_dir.glob("*.png")) + list(raw_image_dir.glob("*.jpg"))

if not raw_images:
    print("No images found in generated/raw! Please verify your folder path.")
    exit(1)

# Pick the latest raw image saved by your previous run
latest_image = max(raw_images, key=lambda p: p.stat().st_mtime)
print(f"Using raw image: {latest_image}")

# 2. Run the composer directly without calling ChatGPT
composer = FooterComposer()
result_path = composer.add_footer(latest_image, topic="happy_ganesh_chaturthi")

print(f"Done! Test poster saved at: {result_path}")
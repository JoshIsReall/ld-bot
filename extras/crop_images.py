import os
from PIL import Image

level_screenshots = [
    "./level_screenshots/" + file
    for file in os.listdir("./level_screenshots/")
    if file.endswith(".png") and not file.endswith("_center.png")
]

for screenshot in level_screenshots:
    with Image.open(screenshot) as img:
        width, height = img.size

        center = width // 2
        left = center - 142
        right = left + 285

        cropped = img.crop((left, 0, right, height))

        cropped.save(
            screenshot.replace(".png", "_center.png"),
            icc_profile=None
        )

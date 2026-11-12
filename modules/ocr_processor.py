import os
import shutil
from io import BytesIO

import pytesseract
from PIL import Image


# Find Tesseract on Windows or Linux
TESSERACT_PATH = shutil.which("tesseract")

# Windows fallback
if not TESSERACT_PATH:
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_path):
        TESSERACT_PATH = windows_path

if not TESSERACT_PATH:
    raise RuntimeError("Tesseract OCR is not installed.")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(image_data):

    if not image_data:
        raise ValueError("Image data is empty.")

    try:
        with Image.open(BytesIO(image_data)) as image:

            image = image.convert("L")

            extracted_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            return extracted_text.strip()

    except Exception as e:
        raise RuntimeError(
            f"Unable to extract text from image: {e}"
        )

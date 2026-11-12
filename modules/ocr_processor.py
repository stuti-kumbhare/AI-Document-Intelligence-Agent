import os
from io import BytesIO

import pytesseract
from PIL import Image


# Tesseract OCR installation path
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if not os.path.exists(TESSERACT_PATH):
    raise FileNotFoundError(
        "Tesseract OCR was not found at: " + TESSERACT_PATH
    )

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(image_data):

    if not image_data:
        raise ValueError("Image data is empty.")

    try:

        with Image.open(BytesIO(image_data)) as image:

            # Convert image into grayscale for OCR
            image = image.convert("L")

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            return extracted_text.strip()

    except Exception as e:

        raise RuntimeError(
            f"Unable to extract text from image: {e}"
        )

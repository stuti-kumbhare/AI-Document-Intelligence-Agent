import fitz
from docx import Document
from pptx import Presentation
from io import BytesIO

from modules.ocr_processor import extract_text_from_image


def extract_text(file):

    file_name = file.name.lower()
    file_data = file.getvalue()

    extracted_data = []

    # =====================================
    # PDF EXTRACTION WITH OCR FALLBACK
    # =====================================

    if file_name.endswith(".pdf"):

        pdf = fitz.open(
            stream=file_data,
            filetype="pdf"
        )

        try:

            for page_number, page in enumerate(pdf, start=1):

                # First try normal text extraction
                text = page.get_text()

                # If no selectable text, use OCR
                if not text.strip():

                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2),
                        alpha=False
                    )

                    image_data = pixmap.tobytes("png")

                    text = extract_text_from_image(image_data)

                if text.strip():

                    extracted_data.append({
                        "source": file.name,
                        "page": page_number,
                        "content": text
                    })

        finally:
            pdf.close()

    # =====================================
    # IMAGE EXTRACTION
    # =====================================

    elif file_name.endswith((
        ".png", ".jpg", ".jpeg",
        ".tif", ".tiff", ".bmp", ".webp"
    )):

        text = extract_text_from_image(file_data)

        if text.strip():

            extracted_data.append({
                "source": file.name,
                "page": "Image",
                "content": text
            })

    # =====================================
    # DOCX EXTRACTION
    # =====================================

    elif file_name.endswith(".docx"):

        doc = Document(BytesIO(file_data))

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        if text.strip():

            extracted_data.append({
                "source": file.name,
                "page": "Not available",
                "content": text
            })

    # =====================================
    # TXT EXTRACTION
    # =====================================

    elif file_name.endswith(".txt"):

        text = file_data.decode(
            "utf-8",
            errors="replace"
        )

        if text.strip():

            extracted_data.append({
                "source": file.name,
                "page": "Not available",
                "content": text
            })

    # =====================================
    # PPTX EXTRACTION
    # =====================================

    elif file_name.endswith(".pptx"):

        presentation = Presentation(BytesIO(file_data))

        for slide_number, slide in enumerate(
            presentation.slides,
            start=1
        ):

            slide_text = []

            for shape in slide.shapes:

                if shape.has_text_frame:
                    slide_text.append(shape.text)

            text = "\n".join(slide_text)

            if text.strip():

                extracted_data.append({
                    "source": file.name,
                    "page": slide_number,
                    "content": text
                })

    else:

        raise ValueError("Unsupported file format")

    return extracted_data

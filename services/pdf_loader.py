import fitz
from services.ocr_service import extract_text_from_image


def extract_pages_from_pdf(file_bytes: bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    pages = []

    for i, page in enumerate(doc):
        text = page.get_text().strip()

        # ✅ proper fallback design
        if not text:
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")

            text = extract_text_from_image(img_bytes)

        pages.append({
            "page_number": i,
            "text": text
        })

    return pages
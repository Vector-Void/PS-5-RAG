import pymupdf
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text,
                })

    if not pages:
        raise ValueError(
            "No extractable text found. "
            "This PDF may contain scanned images. OCR is not supported."
        )

    return pages
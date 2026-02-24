import pdfplumber
from docx import Document
from services.ocr_service import extract_text_from_scanned_pdf
import io

async def extract_text(file_bytes: bytes, extension: str) -> str:
    if extension == "pdf":
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

        # Auto OCR detection
        if len(text.strip()) < 50:
            text = await extract_text_from_scanned_pdf(file_bytes)

        return text

    elif extension == "docx":
        document = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in document.paragraphs])

    return ""
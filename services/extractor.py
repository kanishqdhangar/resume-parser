import pdfplumber
from docx import Document
from services.ocr_service import extract_text_from_scanned_pdf
import io
import fitz  # PyMuPDF


async def extract_text(file_bytes: bytes, extension: str):
    text = ""
    links = []

    if extension == "pdf":

        # -------- Extract Visible Text --------
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        # -------- Extract Hyperlinks (NEW) --------
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                for link in page.get_links():
                    if "uri" in link:
                        links.append(link["uri"])
        except Exception:
            pass  # Don't crash if link extraction fails

        # -------- OCR fallback --------
        if len(text.strip()) < 50:
            text = await extract_text_from_scanned_pdf(file_bytes)

        return text, links

    elif extension == "docx":

        document = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in document.paragraphs])

        # DOCX hyperlink extraction (optional advanced)
        # Can be added later if needed

        return text, links

    return "", []
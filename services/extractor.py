import pdfplumber
from docx import Document
from services.ocr_service import extract_text_from_scanned_pdf
import io
import fitz  # PyMuPDF


async def extract_text(file_bytes: bytes, extension: str):
    text = ""
    links = []
    project_positions = []

    if extension == "pdf":

        # -------- Extract Visible Text (pdfplumber) --------
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")

            for page in doc:

                # -------- Extract Hyperlinks with Y position --------
                for link in page.get_links():
                    if "uri" in link:
                        rect = link["from"]
                        links.append({
                            "url": link["uri"],
                            "y": rect.y0
                        })

                # -------- Extract Project Title Positions (Line-Level Accurate) --------
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if "lines" in block:
                        for line in block["lines"]:

                            line_text = ""
                            for span in line["spans"]:
                                line_text += span["text"]

                            line_stripped = line_text.strip()
                            line_lower = line_stripped.lower()
                            y_position = line["bbox"][1]

                            # Detect project header lines
                            if "github" in line_lower:
                                title = line_stripped.split("(")[0].strip()

                                if title:
                                    project_positions.append({
                                        "title": title,
                                        "y": y_position
                                    })

        except Exception as e:
            print("PDF metadata extraction error:", e)

        # -------- OCR fallback --------
        if len(text.strip()) < 50:
            text = await extract_text_from_scanned_pdf(file_bytes)

        return text, links, project_positions

    elif extension == "docx":

        document = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in document.paragraphs])

        return text, [], []

    return "", [], []
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

async def extract_text_from_scanned_pdf(file_bytes: bytes) -> str:
    images = convert_from_bytes(file_bytes)
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image)

    return text
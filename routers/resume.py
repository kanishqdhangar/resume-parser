from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.parser_service import parse_resume
from utils.file_validator import validate_file
from schemas.resume_schema import ResumeResponse

router = APIRouter()


@router.post("/parse", response_model=ResumeResponse)
async def parse_resume_api(file: UploadFile = File(...)):

    extension = validate_file(file)
    file_bytes = await file.read()

    text, links = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    # 🔥 Inject hyperlinks into text for Gemini
    if links:
        text += "\n\nHYPERLINKS FOUND IN RESUME:\n"
        for url in links:
            text += f"- {url}\n"

    parsed_data = await parse_resume(text)

    return parsed_data
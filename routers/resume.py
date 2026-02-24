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

    text = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    parsed_data = await parse_resume(text)

    return parsed_data
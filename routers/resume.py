from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.parser_service import parse_resume
from services.post_processor import attach_links_by_position
from utils.file_validator import validate_file
from schemas.resume_schema import ResumeResponse

router = APIRouter()


@router.post("/parse", response_model=ResumeResponse)
async def parse_resume_api(file: UploadFile = File(...)):

    extension = validate_file(file)
    file_bytes = await file.read()

    # 🔥 Now returns 3 values
    text, links, project_positions = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    parsed_data = await parse_resume(text)

    # 🔥 Use position-based mapping
    parsed_data = attach_links_by_position(
        parsed_data,
        links,
        project_positions
    )

    return parsed_data
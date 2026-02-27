from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.parser_service import parse_resume
from utils.file_validator import validate_file
from schemas.resume_schema import ResumeResponse
import hashlib
import time

router = APIRouter()

# 🧠 In-memory cache (Render-safe for single instance)
CACHE = {}
CACHE_TTL = 60 * 30  # 30 minutes


def cleanup_cache():
    current_time = time.time()
    keys_to_delete = [
        key for key, value in CACHE.items()
        if current_time - value["timestamp"] > CACHE_TTL
    ]
    for key in keys_to_delete:
        del CACHE[key]


@router.post("/parse", response_model=ResumeResponse)
async def parse_resume_api(file: UploadFile = File(...)):

    extension = validate_file(file)
    file_bytes = await file.read()

    # 🔒 File size guard (5MB limit)
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum allowed size is 5MB."
        )

    # 🔑 Create hash of resume to avoid duplicate LLM calls
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    cleanup_cache()

    if file_hash in CACHE:
        return CACHE[file_hash]["data"]

    text, links = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    # 🔥 Inject hyperlinks into text for Gemini
    if links:
        text += "\n\nHYPERLINKS FOUND IN RESUME:\n"
        for url in links:
            text += f"- {url}\n"

    parsed_data = await parse_resume(text)

    # 💾 Cache result
    CACHE[file_hash] = {
        "data": parsed_data,
        "timestamp": time.time()
    }

    return parsed_data
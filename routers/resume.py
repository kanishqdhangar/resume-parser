from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.parser_service import parse_resume
from utils.file_validator import validate_file
from schemas.resume_schema import ResumeResponse
from schemas.resume_schema import TaskResponse
from tasks import process_resume
import hashlib
import time

router = APIRouter()



@router.post("/parse", response_model=TaskResponse)
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

    text, links = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    # 🔥 Inject hyperlinks into text for Gemini
    if links:
        text += "\n\nHYPERLINKS FOUND IN RESUME:\n"
        for url in links:
            text += f"- {url}\n"

    task = process_resume.delay(text, file_hash)

    return {
        "task_id": task.id,
        "status": "processing"
    }


@router.get("/result/{task_id}")
def get_result(task_id: str):
    task = process_resume.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending"}

    elif task.state == "SUCCESS":
        return {
            "status": "completed",
            "data": task.result
        }

    elif task.state == "FAILURE":
        return {"status": "failed"}

    return {"status": task.state}
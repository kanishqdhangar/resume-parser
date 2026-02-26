from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.parser_service import parse_resume
from utils.file_validator import validate_file
from schemas.resume_schema import ResumeResponse

router = APIRouter()


def attach_links_to_projects(parsed_data, links):
    github_links = [l for l in links if "github.com" in l]
    live_links = [l for l in links if "vercel.app" in l or "render.com" in l]

    for i, project in enumerate(parsed_data.get("projects", [])):
        if i < len(github_links):
            project["github_url"] = github_links[i]
        if i < len(live_links):
            project["live_url"] = live_links[i]

    return parsed_data


@router.post("/parse", response_model=ResumeResponse)
async def parse_resume_api(file: UploadFile = File(...)):

    extension = validate_file(file)
    file_bytes = await file.read()

    # 🔥 UPDATED: Now returns text + links
    text, links = await extract_text(file_bytes, extension)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    parsed_data = await parse_resume(text)

    # 🔥 NEW: Attach extracted hyperlinks
    parsed_data = attach_links_to_projects(parsed_data, links)

    return parsed_data
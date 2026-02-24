from fastapi import UploadFile, HTTPException
from core.config import settings

def validate_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()

    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    return extension
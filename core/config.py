import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    APP_NAME = "Resume Parser Microservice"
    MAX_FILE_SIZE_MB = 5
    ALLOWED_EXTENSIONS = ["pdf", "docx"]

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # openai or gemini

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_KEY_BACKUP: Optional[str] = os.getenv("GEMINI_API_KEY_BACKUP")
settings = Settings()
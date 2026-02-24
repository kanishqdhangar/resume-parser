import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Resume Parser Microservice"
    MAX_FILE_SIZE_MB = 5
    ALLOWED_EXTENSIONS = ["pdf", "docx"]

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai or gemini

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
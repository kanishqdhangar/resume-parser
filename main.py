from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.resume import router
from core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/resume", tags=["Resume"])

@app.get("/")
def health():
    return {"status": "Resume Parser Running"}
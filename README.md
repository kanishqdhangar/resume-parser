# Resume Parser Microservice

🌐 **Live Deployment:**  
https://resume-parser-sgtj.onrender.com/

📄 **Swagger API Docs:**  
https://resume-parser-sgtj.onrender.com/docs

🏥 **Health Check:**  
https://resume-parser-sgtj.onrender.com/

---

## Overview

Resume Parser Microservice is a production-ready AI-powered backend service that extracts structured data from resumes (PDF and DOCX).

It is designed with a scalable asynchronous architecture using FastAPI, Celery, and Redis to efficiently handle concurrent requests and heavy processing workloads.

The system supports:

- Text-based PDFs  
- Scanned PDFs (OCR)  
- Embedded hyperlinks (GitHub, Live URLs, Streamlit, Vercel, etc.)  
- Strict structured JSON output  
- Background processing for heavy tasks  

---

## Architecture

```
Client → FastAPI → Redis Queue → Celery Worker → LLM/OCR → Redis Cache → Response
```

- FastAPI handles incoming API requests (non-blocking)
- Celery processes resume parsing asynchronously
- Redis acts as both queue (broker) and caching layer
- Results are returned via task polling

---

## Tech Stack

- FastAPI  
- Celery + Redis  
- Gemini 2.5 Flash  
- Tesseract OCR  
- pdfplumber  
- PyMuPDF (fitz)  
- httpx (async client)  
- Pydantic  
- Docker  
- Docker Compose  
- Render  

---

## Production Optimizations

This service includes:

- Async Gemini requests using httpx  
- Shared HTTP client for better performance  
- Background processing using Celery  
- Redis-based caching (SHA-256 hash)  
- Concurrency limiter using asyncio.Semaphore  
- Exponential backoff retry on rate limits  
- Multi-key Gemini failover (primary + backup key)  
- File size validation  
- Strict JSON validation using Pydantic  
- Automatic hyperlink extraction and injection into LLM prompt  

Designed for stable startup-scale usage (~100+ resumes/day).

---

## Features

- Upload PDF or DOCX resumes  
- OCR support for scanned resumes  
- Hyperlink extraction from resumes  
- AI-powered structured parsing  
- Auto-assignment of GitHub and live URLs to projects  
- Strict schema validation  
- Background job processing  
- Dockerized deployment  
- Public live deployment available  

---

## Extracted Fields

### Basic Info
- name  
- email  
- phone  
- gender  
- about  
- linkedin_url  
- github_url  
- portfolio_url  
- skills  

### Education
- degree  
- field_of_study  
- institution  
- year  
- cgpa  

### Work Experience
- title  
- organization  
- start_date  
- end_date  
- description (list of bullet points)  

### Projects
- title  
- description  
- technologies (list)  
- github_url  
- live_url  

### Additional
- total_experience_years  

---

## Live API Usage

### Endpoint

POST  
https://resume-parser-sgtj.onrender.com/api/resume/parse

---

### How to Test

1. Open Swagger UI  
   https://resume-parser-sgtj.onrender.com/docs  

2. Select:  
   POST /api/resume/parse  

3. Click "Try it out"  

4. Upload a resume (PDF or DOCX)  

5. Click Execute  

You will receive a task_id and status.

---

### Result Endpoint

GET  
/api/resume/result/{task_id}

---

## Example Response

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "skills": ["Python", "React"],
  "projects": [
    {
      "title": "AI Resume Analyzer",
      "technologies": ["FastAPI", "Gemini"]
    }
  ]
}
```

---

## Docker Usage

Build image:

```
docker build -t resume-parser .
```

Run container:

```
docker run -p 10000:10000 resume-parser
```

---

## Docker Compose (Local Multi-Service Setup)

This project includes docker-compose.yml to run all services together:

- FastAPI (API)
- Celery Worker
- Redis (queue + cache)

Run full system:

```
docker-compose up --build
```

Scale workers:

```
docker-compose up --scale worker=3
```

---

## Local Development Setup

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser
git checkout v2-render
```

---

### 2. Create Virtual Environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Install System Dependencies

Mac:
```
brew install tesseract poppler
```

Linux:
```
sudo apt-get install tesseract-ocr poppler-utils
```

Windows:
Install Tesseract and Poppler manually and add them to PATH.

---

### 5. Create .env File

```
GEMINI_API_KEY=your_primary_key
GEMINI_API_KEY_BACKUP=your_backup_key
LLM_PROVIDER=gemini
REDIS_URL=your_redis_url
```

---

### 6. Run Server

```
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

---

## Deployment

Hosted on Render using Docker.

### Notes

- Free Render instances sleep after inactivity  
- First request may take 30–60 seconds  
- Celery worker runs in same container (free-tier workaround)  
- Redis is used as external service (Upstash/Render Redis)  

---

## Project Structure

```
resume-parser/
│
├── main.py
├── celery_app.py
├── tasks.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
│
├── core/
├── routers/
├── services/
├── schemas/
├── utils/
```

---

## Author

Kanishq Dhangar  
Full-Stack & AI Developer
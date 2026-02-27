# Resume Parser Microservice

Live Deployment:  
https://resume-parser-sgtj.onrender.com/

Swagger API Docs:  
https://resume-parser-sgtj.onrender.com/docs

Health Check:  
https://resume-parser-sgtj.onrender.com/

---

## Overview

Resume Parser Microservice is a production-ready AI-powered backend service that extracts structured data from resumes (PDF and DOCX).

It supports:

- Text-based PDFs
- Scanned PDFs (OCR)
- Embedded hyperlinks (GitHub, Live URLs, Streamlit, Vercel, etc.)
- Strict structured JSON output

The system is optimized for startup-scale traffic and deployed publicly on Render.

---

## Tech Stack

- FastAPI
- Gemini 2.5 Flash
- Tesseract OCR
- pdfplumber
- PyMuPDF (fitz)
- httpx (async client)
- Pydantic
- Docker
- Render

---

## Production Optimizations

This service includes:

- Async Gemini requests using httpx
- Shared HTTP client for better performance
- Concurrency limiter using asyncio.Semaphore
- Exponential backoff retry on rate limits
- Multi-key Gemini failover (primary + backup key)
- Resume SHA-256 hash caching to prevent duplicate LLM calls
- File size validation
- Strict JSON validation using Pydantic
- Automatic hyperlink extraction and injection into LLM prompt

Designed for stable startup usage (~100 resumes/day).

---

## Features

- Upload PDF or DOCX resumes
- OCR support for scanned resumes
- Hyperlink extraction from resumes
- AI-powered structured parsing
- Auto-assignment of GitHub and live URLs to projects
- Strict schema validation
- Dockerized deployment
- Public live deployment available

---

## Extracted Fields

The API extracts:

- name
- email
- phone
- gender
- about
- linkedin_url
- github_url
- portfolio_url
- skills (list)

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

You will receive structured JSON output.

---

## Example Response

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "gender": null,
  "about": "Full-stack developer with experience in AI integrations.",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "github_url": "https://github.com/johndoe",
  "portfolio_url": "https://johndoe.dev",
  "skills": ["Python", "React", "FastAPI"],
  "education": [
    {
      "degree": "B.Tech",
      "field_of_study": "Computer Science",
      "institution": "XYZ University",
      "year": "2024",
      "cgpa": "8.5"
    }
  ],
  "work_experience": [
    {
      "title": "Software Developer Intern",
      "organization": "ABC Company",
      "start_date": "June 2023",
      "end_date": "August 2023",
      "description": [
        "Built REST APIs",
        "Improved UI performance"
      ]
    }
  ],
  "projects": [
    {
      "title": "AI Resume Analyzer",
      "description": "Built an AI-based resume scoring system.",
      "technologies": ["FastAPI", "Gemini"],
      "github_url": "https://github.com/johndoe/resume-analyzer",
      "live_url": "https://resume-analyzer.vercel.app"
    }
  ],
  "total_experience_years": 1.5
}
```

---

## Project Structure

```
resume-parser/
│
├── main.py
├── Dockerfile
├── requirements.txt
├── .env
│
├── core/
│   └── config.py
│
├── routers/
│   └── resume.py
│
├── services/
│   ├── extractor.py
│   ├── parser_service.py
│   ├── llm_service.py
│   └── ocr_service.py
│
├── schemas/
│   └── resume_schema.py
│
└── utils/
```

---

## Local Development Setup

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser
```

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

### 3. Install Dependencies

```
pip install -r requirements.txt
```

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

### 5. Create .env File

```
GEMINI_API_KEY=your_primary_key
GEMINI_API_KEY_BACKUP=your_backup_key
LLM_PROVIDER=gemini
```

### 6. Run Server

```
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

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

Open:
http://localhost:10000/docs

---

## Deployment

Hosted on Render using Docker.

Live URL:
https://resume-parser-sgtj.onrender.com/

Required Environment Variables:

- GEMINI_API_KEY
- GEMINI_API_KEY_BACKUP (optional but recommended)
- LLM_PROVIDER

---

## Production Notes

- Free Render instances sleep after inactivity
- First request may take 30–60 seconds
- Resume hash caching reduces LLM cost
- Multi-key fallback handles rate limits
- Retry with exponential backoff improves stability
- Designed for startup-scale traffic

---

## Author

Kanishq Dhangar  
Full-Stack  
AI Developer
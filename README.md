# Resume Parser Microservice

Live Deployment:
https://resume-parser-sgtj.onrender.com/

Swagger API Docs:
https://resume-parser-sgtj.onrender.com/docs

Health Check:
https://resume-parser-sgtj.onrender.com/

---

## Overview

Resume Parser Microservice is an AI-powered backend service that extracts structured data from PDF resumes.

It uses:

- FastAPI
- Gemini 2.5 Flash
- Tesseract OCR
- pdf2image
- Docker
- Render

The service accepts a PDF file and returns clean, validated JSON output.

---

## Features

- Upload PDF resumes
- OCR support for scanned resumes
- AI-powered structured data extraction
- Strict schema validation using Pydantic
- Dockerized for production deployment
- Public live deployment available

---

## Extracted Fields

The API extracts the following structured information:

- full_name
- email
- phone
- skills (list of strings)
- education
  - degree
  - institution
  - year
- work_experience
  - title
  - organization
  - start_date
  - end_date
  - description (list of bullet points)
- total_experience_years

---

## Live API Usage

### Endpoint

POST https://resume-parser-sgtj.onrender.com/api/resume/parse

### How to Test

1. Open Swagger UI:
   https://resume-parser-sgtj.onrender.com/docs

2. Click on:
   POST /api/resume/parse

3. Click "Try it out"

4. Upload a PDF resume

5. Click Execute

You will receive structured JSON in response.

---

## Example Response

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "skills": ["Python", "React", "Django"],
  "education": [
    {
      "degree": "B.Tech Computer Science",
      "institution": "XYZ University",
      "year": "2024"
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
  "total_experience_years": 1.5
}

---

## Project Structure

resume-parser/
│
├── main.py
├── Dockerfile
├── requirements.txt
├── .gitignore
│
├── core/
│   └── config.py
│
├── routers/
│   └── resume.py
│
├── services/
│   ├── parser_service.py
│   ├── llm_service.py
│   └── ocr_service.py
│
├── schemas/
│   └── resume_schema.py
│
└── utils/

---

## Local Development Setup

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser

2. Create virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Install system dependencies

Mac:
brew install tesseract poppler

Linux:
sudo apt-get install tesseract-ocr poppler-utils

Windows:
Install Tesseract and Poppler manually and add them to PATH.

5. Create .env file

GEMINI_API_KEY=your_gemini_api_key
LLM_PROVIDER=gemini

6. Run server

uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs

---

## Docker Usage

Build image:

docker build -t resume-parser .

Run container:

docker run -p 10000:10000 resume-parser

Open:
http://localhost:10000/docs

---

## Deployment

Hosted on Render using Docker.

Deployment URL:
https://resume-parser-sgtj.onrender.com/

Required Environment Variables:

GEMINI_API_KEY
LLM_PROVIDER

---

## Production Notes

- Free Render instances sleep after inactivity
- First request may take 30–60 seconds
- Strict schema validation ensures predictable output
- Designed as a reusable AI microservice

---

## Author

Kanishq Dhangar
Final-Year Computer Science Student
Full-Stack + AI Developer

---
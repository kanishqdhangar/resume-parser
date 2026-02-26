import httpx
import json
from fastapi import HTTPException
import re
import asyncio
from core.config import settings


async def extract_structured_data(text: str):

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json",
    }

    prompt = f"""
Extract structured JSON from this resume.

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT add explanations.
- Do NOT wrap in markdown.
- Extract REAL URLs only.
- The resume may contain a section titled "HYPERLINKS FOUND IN RESUME".
- Use those URLs to correctly assign github_url and live_url
  to the appropriate projects.
- Do NOT return placeholder text like "GitHub Link".
- If a project has a GitHub link in resume, assign it properly.
- If a field is not found, return null.
- Do NOT guess missing values.
- Field names must match EXACTLY as shown below.

Format:

{{
  "name": "",
  "email": "",
  "phone": "",
  "gender": "",
  "about": "",
  "linkedin_url": "",
  "github_url": "",
  "portfolio_url": "",
  "skills": [],
  "education": [
    {{
      "degree": "",
      "field_of_study": "",
      "institution": "",
      "year": "",
      "cgpa": ""
    }}
  ],
  "work_experience": [
    {{
      "title": "",
      "organization": "",
      "start_date": "",
      "end_date": "",
      "description": []
    }}
  ],
  "projects": [
    {{
      "title": "",
      "description": "",
      "technologies": [],
      "github_url": "",
      "live_url": ""
    }}
  ],
  "total_experience_years": 0
}}

Resume:
{text}
"""

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
      response = await client.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:

        if e.response.status_code == 429:
            raise HTTPException(
                status_code=503,
                detail="LLM rate limit exceeded. Please try again later."
            )

        elif e.response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key."
            )

        elif e.response.status_code == 400:
            raise HTTPException(
                status_code=400,
                detail="Bad request sent to Gemini API."
            )

        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error from LLM service."
            )

    result = response.json()

    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

    json_match = re.search(r"\{[\s\S]*\}", raw_text)

    if not json_match:
        raise HTTPException(
            status_code=500,
            detail="Gemini did not return valid JSON."
        )

    clean_json = json_match.group(0)

    return json.loads(clean_json)
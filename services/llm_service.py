import httpx
import json
import re
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

    response.raise_for_status()
    result = response.json()

    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

    json_match = re.search(r"\{[\s\S]*\}", raw_text)

    if not json_match:
        raise Exception("Gemini did not return valid JSON")

    clean_json = json_match.group(0)

    return json.loads(clean_json)
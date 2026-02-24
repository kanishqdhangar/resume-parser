import requests
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
- Field names must match EXACTLY as shown below.

Format:

{{
  "full_name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
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
  "total_experience_years": 0
}}

Resume:
{text}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()

    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

    # 🔥 Extract JSON safely
    json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)

    if not json_match:
        raise Exception("Gemini did not return valid JSON")

    clean_json = json_match.group(0)

    return json.loads(clean_json)
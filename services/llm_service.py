import httpx
import json
from fastapi import HTTPException
import re
import asyncio
from core.config import settings


# 🔒 Limit concurrent Gemini calls (safe for Render)
LLM_SEMAPHORE = asyncio.Semaphore(3)

# ♻️ Reuse single client (better performance)
CLIENT = httpx.AsyncClient(timeout=30.0)

# 🔑 Multi-key support (Primary + Backup)
GEMINI_KEYS = [
    settings.GEMINI_API_KEY,
    getattr(settings, "GEMINI_API_KEY_BACKUP", None)
]

async def extract_structured_data(text: str):

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
- Always return the completing year of education. If currently pursuing, use the current year.

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

    retries = 3
    base_delay = 1

    async with LLM_SEMAPHORE:

        for api_key in GEMINI_KEYS:

            if not api_key:
                continue

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

            delay = base_delay

            for attempt in range(retries):

                try:
                    response = await CLIENT.post(url, headers=headers, json=data)

                    # Retry on rate limit
                    if response.status_code == 429:
                        if attempt == retries - 1:
                            break
                        await asyncio.sleep(delay)
                        delay *= 2
                        continue

                    response.raise_for_status()
                    result = response.json()
                    return parse_llm_response(result)

                except httpx.RequestError:
                    if attempt == retries - 1:
                        break
                    await asyncio.sleep(delay)
                    delay *= 2

        # If we reach here → all keys failed
        raise HTTPException(
            status_code=503,
            detail="LLM temporarily unavailable. Please try again later."
        )


def parse_llm_response(result: dict):

    try:
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500,
            detail="Unexpected LLM response format."
        )

    json_match = re.search(r"\{[\s\S]*\}", raw_text)

    if not json_match:
        raise HTTPException(
            status_code=500,
            detail="Gemini did not return valid JSON."
        )

    clean_json = json_match.group(0)

    return json.loads(clean_json)
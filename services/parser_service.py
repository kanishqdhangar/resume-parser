from services.llm_service import extract_structured_data

async def parse_resume(text: str):
    return await extract_structured_data(text)
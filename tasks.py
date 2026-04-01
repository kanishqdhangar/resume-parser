from celery_app import celery_app
from services.parser_service import parse_resume
from core.redis_client import redis_client
import asyncio
import json

CACHE_TTL = 60 * 30  # 30 min


@celery_app.task
def process_resume(text: str, file_hash: str):

    # ✅ Check Redis cache
    cached = redis_client.get(file_hash)
    if cached:
        return json.loads(cached)

    # 🔥 Run async parser
    result = asyncio.run(parse_resume(text))

    # 💾 Store in Redis
    redis_client.setex(
        file_hash,
        CACHE_TTL,
        json.dumps(result)
    )

    return result
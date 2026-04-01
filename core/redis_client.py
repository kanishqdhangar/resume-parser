import redis

redis_client = redis.Redis(
    host="redis",  # use the service name defined in docker-compose.yml
    port=6379,
    db=1,  # use different DB for cache
    decode_responses=True
)
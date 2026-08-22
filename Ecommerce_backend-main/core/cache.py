import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def clear_products_cache():
    keys = redis_client.keys("products:*")
    if keys:
        redis_client.delete(*keys)
from redis.asyncio import Redis, ConnectionPool

from .config import settings

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    encoding="utf-8",
)


async def connect_redis() -> Redis:
    redis_client = await Redis(connection_pool=redis_pool)
    # sign = await redis_client.ping()
    # if sign:
    #     print("redis连接成功")
    return redis_client

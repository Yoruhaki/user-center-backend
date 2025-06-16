from fastapi_server_session import SessionManager, RedisSessionInterface
from redis import ConnectionPool, Redis

from .config import settings

redis_sync_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    encoding="utf-8",

)

session_manager = SessionManager(
    interface=RedisSessionInterface(Redis(connection_pool=redis_sync_pool))
)

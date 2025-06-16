from datetime import datetime
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Redis缓存配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = "<PASSWORD>"

    # 数据库配置
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "123456"
    DATABASE_NAME: str = "user_center"

    # 密钥
    SECRET_KEY: str = "use-to-generate-jwt"
    SALT: str = "password-encrypt-salt"

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    LOG_RETENTION: str = "7 days"
    LOG_ROTATION: str = "00:00"
    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    LOG_SERIALIZE: bool = True
    LOG_COMPRESSION: str = "gz"

    # CORS配置
    ALLOW_ORIGINS: list[str] | str = []
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=(".env.dev", ".env.prod"))


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Redis缓存配置
    redis_host: str = 'localhost'
    redis_port: int = 6379

    # 数据库配置
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "root"
    database_password: str = "123456"
    database_name: str = "user_center"

    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env.prod")
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
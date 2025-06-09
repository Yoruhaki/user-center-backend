from contextlib import asynccontextmanager
from typing import AsyncGenerator

from tortoise.contrib.fastapi import RegisterTortoise
from fastapi import FastAPI

from .config import settings

# 映射类加载列表
MODELS = [
    "src.app.models.users",
    "aerich.models",
]

# 数据库连接配置
TORTOISE_ORM = {
    "connections": {
        "user_center_conn": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.database_host,
                "port": settings.database_port,
                "user": settings.database_user,
                "password": settings.database_password,
                "database": settings.database_name,
            }
        }
    },
    "apps": {
        "user_center_app": {
            "models": MODELS,
            "default_connection": "user_center_conn"
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai"
}


@asynccontextmanager
async def register_postgres(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    连接数据库, 生成数据表

    Args:
        app (FastAPI): 网络实例

    Yields:
        None: 无返回
    """

    async with RegisterTortoise(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
    ):
        yield

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from .config import settings
from src.app import models
from src.app.utils import ModuleUtils

from itertools import chain

# 映射类加载列表
ORM_MODELS = list(filter(
    lambda x: "base" not in x,
    ModuleUtils.get_modules_import_path(models.__path__[0], models.__name__)
))
MODELS = chain(ORM_MODELS, ["aerich.models"])

# 数据库连接配置
TORTOISE_ORM = {
    "connections": {
        "user_center_conn": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.DATABASE_HOST,
                "port": settings.DATABASE_PORT,
                "user": settings.DATABASE_USER,
                "password": settings.DATABASE_PASSWORD,
                "database": settings.DATABASE_NAME,
            },
        },
    },
    "apps": {
        "user_center_app": {
            "models": MODELS,
            "default_connection": "user_center_conn"
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
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

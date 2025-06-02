from contextlib import asynccontextmanager

from tortoise.contrib.fastapi import RegisterTortoise

MODELS = [
    "src.app.models.users",
    "aerich.models",
]

TORTOISE_ORM = {
    "db_url": {},
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
                "password": "123456",
                "database": "user_center"
            }
        }
    },
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default"
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai"
}


@asynccontextmanager
async def register_postgres(app):
    async with RegisterTortoise(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
    ):
        yield

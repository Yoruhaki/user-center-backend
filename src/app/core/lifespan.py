from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI
from redis.asyncio import Redis
from tortoise import Tortoise
from tortoise.backends.base.config_generator import generate_config
from tortoise.contrib.fastapi import RegisterTortoise

from .database import register_postgres, ORM_MODELS
from .redis import connect_redis
from .scheduler import start_scheduler, shutdown_scheduler


class State(TypedDict):
    redis: Redis


@asynccontextmanager
async def lifespan_test(web_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        "sqlite://:memory:",
        app_modules={"models": ORM_MODELS},
        testing=True,
        connection_label="models",
    )

    async with RegisterTortoise(
            app=web_app,
            config=config,
            generate_schemas=True,
            _create_db=True,
    ):
        yield

    await getattr(Tortoise, "_drop_databases")()


@asynccontextmanager
async def app_lifespan(web_app: FastAPI) -> AsyncGenerator[State | None, None]:
    redis = await connect_redis()
    state = getattr(web_app, "state", None)
    testing = getattr(state, "testing", False)
    if testing:
        async with lifespan_test(web_app):
            yield
    else:
        async with register_postgres(web_app):
            start_scheduler(redis)
            state: State = {
                "redis": redis,
            }
            yield state
            shutdown_scheduler()

    await redis.aclose()

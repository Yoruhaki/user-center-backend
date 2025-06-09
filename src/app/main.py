from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.app.routers import api_routers
from src.app.core import register_postgres
from src.app.exceptions import mount_exception_handler
from tortoise import generate_config, Tortoise
from tortoise.contrib.fastapi import RegisterTortoise


@asynccontextmanager
async def lifespan_test(web_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        "sqlite://:memory:",
        app_modules={"models": ["app.models.users"]},
        testing=True,
        connection_label="models",
    )
    async with RegisterTortoise(
        app=web_app,
        config=config,
        generate_schemas=True,
        _create_db=True,
    ):
        # db connected
        yield
        # app teardown
    # db connections closed
    await Tortoise._drop_databases()


@asynccontextmanager
async def app_lifespan(web_app: FastAPI) -> AsyncGenerator[None, None]:
    if getattr(web_app.state, "testing", None):
        async with lifespan_test(web_app):
            yield
    else:
        async with register_postgres(web_app):
            yield


app = FastAPI(lifespan=app_lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-keep-it-safe",  # 替换为你的实际密钥
)

app.mount("/static", StaticFiles(directory="static"), "static")
mount_exception_handler(app)
app.include_router(api_routers)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

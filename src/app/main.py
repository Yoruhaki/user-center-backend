from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from src.app.api import api_routers
from src.app.core import register_postgres


@asynccontextmanager
async def app_lifespan(web_app: FastAPI) -> AsyncGenerator[None, None]:
    async with register_postgres(web_app):
        yield


app = FastAPI(lifespan=app_lifespan)
app.mount("/statics", StaticFiles(directory="./statics"), "statics")
app.include_router(api_routers)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

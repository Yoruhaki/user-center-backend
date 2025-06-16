from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture

from src.app.main import app as project_app
from src.app.core import disable_logging

ClientManagerType = AsyncGenerator[AsyncClient, None]


# TODO: web_app?.state即将废弃, 修改不再通过web_app属性判断是否为测试环境
@asynccontextmanager
async def client_manager(web_app: FastAPI, base_url="http://test/api/v1", **kw) -> ClientManagerType:
    web_app.state.testing = True
    disable_logging()
    async with LifespanManager(web_app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c


@fixture
async def client() -> ClientManagerType:
    async with client_manager(project_app) as c:
        yield c

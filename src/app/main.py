import hashlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.core import register_postgres


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with register_postgres(app):
        yield


app = FastAPI(lifespan=app_lifespan)


def fn():
    hashed_info = hashlib.md5(b"Hello word").hexdigest()
    print(hashed_info)


@app.get("/user")
async def user():
    return {"user": 1}

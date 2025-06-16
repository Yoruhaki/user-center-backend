from fastapi.responses import Response
from pydantic import BaseModel

from .common_types import Json


class BaseResponse[T](BaseModel):
    code: int
    data: T
    message: Json
    description: Json


class Pagination[T](BaseModel):
    total: int
    pages: int
    size: int
    current: int
    records: list[T]


class BaseHTTPResponse[T](Response):
    def __init__(self, content: BaseResponse[T]):
        headers = {
            "Content-Type": "application/json",
        }
        super().__init__(headers=headers, content=content.model_dump_json(indent=2))

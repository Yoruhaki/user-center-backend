from fastapi.responses import Response
from pydantic import BaseModel


class BaseResponse[T](BaseModel):
    code: int
    data: T
    message: str
    description: str


class BaseHTTPResponse[T](Response):
    def __init__(self, content: BaseResponse[T]):
        headers = {
            "Content-Type": "application/json",
        }
        super().__init__(
            headers=headers,
            content=content.model_dump_json(indent=2)
        )

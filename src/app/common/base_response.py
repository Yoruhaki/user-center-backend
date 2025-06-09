from fastapi.responses import Response
from pydantic import BaseModel

type Json = dict[str, Json] | list[Json] | str | int | float | bool | None

class BaseResponse[T](BaseModel):
    code: int
    data: T
    message: Json
    description: Json


class BaseHTTPResponse[T](Response):
    def __init__(self, content: BaseResponse[T]):
        headers = {
            "Content-Type": "application/json",
        }
        super().__init__(
            headers=headers,
            content=content.model_dump_json(indent=2)
        )

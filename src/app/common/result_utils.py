from src.app.utils import NoInstantiableMeta
from .base_response import BaseResponse
from .status_code import StatusCode


class ResultUtils(metaclass=NoInstantiableMeta):
    @staticmethod
    def success[T](data: T, description: str = "") -> BaseResponse[T]:
        return BaseResponse(
            code=StatusCode.SUCCESS.value.code,
            data=data,
            message=StatusCode.SUCCESS.value.message,
            description=description,
        )

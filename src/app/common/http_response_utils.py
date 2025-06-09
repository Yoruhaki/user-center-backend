from src.app.utils import NoInstantiableMeta
from .base_response import BaseResponse, BaseHTTPResponse


class HTTPResponseUtils(metaclass=NoInstantiableMeta):
    @staticmethod
    def error(code, message, description):
        return BaseHTTPResponse(
            content=BaseResponse(
                code=code,
                data=None,
                message=message,
                description=description,
            )
        )

from fastapi import FastAPI, Request
from fastapi.exceptions import ValidationException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.app.common import StatusCode, HTTPResponseUtils
from src.app.core import logger
from .business_exception import BusinessException


def mount_exception_handler(app: FastAPI) -> None:
    """
    异常控制器

    Args:
        app (FastAPI): Web实例

    Returns:
        None
    """

    @app.exception_handler(BusinessException)
    async def business_exception_handler(_: Request, exc: BusinessException):
        logger.error("BusinessException: " + repr(exc))
        return HTTPResponseUtils.error(exc.code, exc.message, exc.description)

    @app.exception_handler(Exception)
    async def system_exception_handler(_: Request, exc: Exception):
        logger.error("SystemException: " + repr(exc))
        return HTTPResponseUtils.error(
            StatusCode.SYSTEM_ERROR.value.code, "系统出错", str(exc)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: ValidationException):
        logger.error("ValidationException: " + repr(exc))
        return HTTPResponseUtils.error(
            StatusCode.SYSTEM_ERROR.value.code, "请求参数类型出错", exc.errors()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        logger.error("HTTPException: " + repr(exc))
        return HTTPResponseUtils.error(
            StatusCode.SYSTEM_ERROR.value.code, "请求出错", str(exc)
        )

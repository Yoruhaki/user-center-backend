from fastapi import FastAPI, Request
from fastapi.exceptions import ValidationException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.app.common import StatusCode, HTTPResponseUtils
from .business_exception import BusinessException


def mount_exception_handler(app: FastAPI):
    @app.exception_handler(BusinessException)
    async def business_exception_handler(_: Request, exc: BusinessException):
        return HTTPResponseUtils.error(exc.code, exc.message, exc.description)

    @app.exception_handler(Exception)
    async def system_exception_handler(_: Request, exc: Exception):
        return HTTPResponseUtils.error(StatusCode.SYSTEM_ERROR.value.code, "系统出错", str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: ValidationException):
        return HTTPResponseUtils.error(StatusCode.SYSTEM_ERROR.value.code, "请求参数类型出错", exc.errors())

    @app.exception_handler(StarletteHTTPException)
    async def validation_exception_handler(_: Request, exc: StarletteHTTPException):
        return HTTPResponseUtils.error(StatusCode.SYSTEM_ERROR.value.code, "请求出错", str(exc))
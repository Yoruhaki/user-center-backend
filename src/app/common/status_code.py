from enum import Enum


class Code:
    def __init__(self, code: int, message: str, description: str) -> None:
        self.__code = code
        self.__message = message
        self.__description = description

    @property
    def code(self) -> int:
        return self.__code

    @property
    def message(self) -> str:
        return self.__message

    @property
    def description(self) -> str:
        return self.__description


class StatusCode(Enum):
    SUCCESS = Code(0, "ok", "")
    PARAMS_ERROR = Code(40000, "请求参数错误", "")
    NULL_ERROR = Code(40001, "请求数据为空", "")
    NOT_LOGIN = Code(40100, "未登录", "")
    NO_AUTH = Code(40101, "无权限", "")
    SYSTEM_ERROR = Code(50000, "系统内部异常", "")

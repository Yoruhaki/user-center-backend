from dataclasses import dataclass
from enum import Enum

from .common_types import Json


@dataclass(frozen=True)
class Code:
    code: int
    message: Json
    description: Json


class StatusCode(Enum):
    SUCCESS = Code(0, "ok", "")
    PARAMS_ERROR = Code(40000, "请求参数错误", "")
    NULL_ERROR = Code(40001, "请求数据为空", "")
    NOT_LOGIN = Code(40100, "未登录", "")
    NO_AUTH = Code(40101, "无权限", "")
    SYSTEM_ERROR = Code(50000, "系统内部异常", "")

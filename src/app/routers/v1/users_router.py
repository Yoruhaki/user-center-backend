from fastapi import APIRouter, Depends
from fastapi.requests import Request

from src.app.common import ResultUtils, BaseResponse, StatusCode
from src.app.constants.user_constants import ADMIN_ROLE, USER_LOGIN_STATE
from src.app.exceptions import BusinessException
from src.app.schemas import UserRegisterRequest, UserLoginRequest, SafetyUser
from src.app.services import UserService
from src.app.utils import StringUtils

router = APIRouter(prefix="/user", tags=["users"])


def is_admin(request: Request) -> bool:
    """
    根据会话判断用户是否为管理员

    Args:
        request (Request): 请求实例

    Returns:
        bool: 用户是否为管理员
    """

    # 从会话中获取数据
    data = request.session.get(USER_LOGIN_STATE)
    if data is None:
        return False

    # 数据反序列化
    safety_user = SafetyUser.model_validate_json(data)

    # 用户角色必须为管理员
    if safety_user.user_role != ADMIN_ROLE:
        return False

    return True


@router.post("/register")
async def user_register(user_register_request: UserRegisterRequest | None = None) -> BaseResponse[int]:
    """
    用户注册路由

    Args:
        user_register_request (UserRegisterRequest | None): 用户注册信息请求体

    Returns:
        BaseResponse[int]: 用户ID

    Raises:
        BusinessException: 注册信息为空 | 参数为空
    """

    if user_register_request is None:
        raise BusinessException(StatusCode.NULL_ERROR, "注册信息为空")

    user_account = user_register_request.user_account
    user_password = user_register_request.user_password
    confirm_password = user_register_request.confirm_password
    if StringUtils.is_any_blank(user_account, user_password, confirm_password):
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    user_id = await UserService.user_register(user_account, user_password, confirm_password)

    return ResultUtils.success(user_id)


@router.post("/login")
async def user_login(
        request: Request,
        user_login_request: UserLoginRequest | None = None,
) -> BaseResponse[SafetyUser]:
    """
    用户登录路由

    Args:
        request (Request): 请求实例
        user_login_request (UserLoginRequest | None): 用户登录信息

    Returns:
        BaseResponse[SafetyUser]: 用户信息(脱敏)

    Raises:
                BusinessException: 登录信息为空 | 参数为空
    """

    if user_login_request is None:
        raise BusinessException(StatusCode.NULL_ERROR, "登录信息为空")

    user_account = user_login_request.user_account
    user_password = user_login_request.user_password
    if StringUtils.is_any_blank(user_account, user_password):
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    safety_user = await UserService.user_login(user_account, user_password, request)

    return ResultUtils.success(safety_user)


@router.get("/current")
async def get_current_user(request: Request) -> BaseResponse[SafetyUser]:
    """
    获取当前用户信息路由

    Args:
        request (Request): 请求实例

    Returns:
        BaseResponse[SafetyUser]: 用户信息(脱敏)

    Raises:
        BusinessException: 用户未登录
    """

    # 从会话中获取用户凭证
    data = request.session.get(USER_LOGIN_STATE)
    if data is None:
        raise BusinessException(StatusCode.NOT_LOGIN, "用户未登录")

    # 反序列化
    safety_user_session = SafetyUser.model_validate_json(data)

    # 根据用户ID从数据库中查询用户信息
    user_id = safety_user_session.id
    safety_user = await UserService.get_user_by_id(user_id)

    return ResultUtils.success(safety_user)


@router.post("/logout")
async def user_logout(request: Request) -> BaseResponse[bool]:
    """
    用户注销路由

    Args:
        request (Request): 请求实例

    Returns:
        BaseResponse[bool]: 用户是否完成注销
    """

    is_logout = UserService.user_logout(request)
    return ResultUtils.success(is_logout)


@router.get("/search")
async def search_users(request: Request, username: str = "") -> BaseResponse[list[SafetyUser]]:
    """
    搜索用户信息路由

    Args:
        request (Request): 请求实例
        username (str): 用户名

    Returns:
        BaseResponse[list[SafetyUser]]: 用户信息列表(脱敏)

    Raises:
        BusinessException: 用户非管理员
    """

    # 权限校验
    if not is_admin(request):
        raise BusinessException(StatusCode.NO_AUTH, "用户非管理员")

    safety_users_list = await UserService.search_users_by_username(username)

    return ResultUtils.success(safety_users_list)


@router.post("/delete")
async def delete_user(request: Request, user_id: int = 0) -> BaseResponse[bool]:
    """
    逻辑删除用户路由

    Args:
        request (Request): 请求实例
        user_id (int): 用户ID

    Returns:
        BaseResponse[bool]: 用户是否被删除(逻辑)

    Raises:
        BusinessException: 用户非管理员 | 删除用户ID为空 | 删除用户ID不为正整数
    """

    # 权限校验
    if not is_admin(request):
        raise BusinessException(StatusCode.NO_AUTH, "用户非管理员")

    if user_id is None:
        raise BusinessException(StatusCode.NULL_ERROR, "删除用户ID为空")
    if user_id <= 0:
        raise BusinessException(StatusCode.PARAMS_ERROR, "删除用户ID不为正整数")

    is_deleted = await UserService.delete_user_by_id(user_id)

    return ResultUtils.success(is_deleted)

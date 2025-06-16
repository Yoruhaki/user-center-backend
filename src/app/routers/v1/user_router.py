from fastapi import APIRouter, Query, Depends, Request
from fastapi_server_session import Session

from src.app.common import ResultUtils, BaseResponse, StatusCode, Pagination
from src.app.constants import USER_LOGIN_STATE
from src.app.core import session_manager
from src.app.exceptions import BusinessException
from src.app.schemas import UserRegisterRequest, UserLoginRequest, SafetyUser
from src.app.schemas.user import UserUpdateRequest
from src.app.services import UserService
from src.app.utils import StringUtils, CollectionUtils

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/register")
async def user_register(
        user_register_request: UserRegisterRequest | None = None,
) -> BaseResponse[int]:
    """
    用户注册路由

    Args:
        user_register_request (UserRegisterRequest | None): 用户注册信息请求体

    Returns:
        BaseResponse[int]: 用户ID

    Raises:
        BusinessException: 注册信息为空 | 参数为空
    """

    # 数据校验
    if user_register_request is None:
        raise BusinessException(StatusCode.NULL_ERROR, "注册信息为空")

    user_account = user_register_request.user_account
    user_password = user_register_request.user_password
    confirm_password = user_register_request.confirm_password
    if StringUtils.is_any_blank(user_account, user_password, confirm_password):
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    # 用户注册
    user_id = await UserService.user_register(
        user_account, user_password, confirm_password
    )

    return ResultUtils.success(user_id)


@router.post("/login")
async def user_login(
        user_login_request: UserLoginRequest | None = None,
        session: Session = Depends(session_manager.use_session),
) -> BaseResponse[SafetyUser]:
    """
    用户登录路由

    Args:
        session (Session): 请求实例
        user_login_request (UserLoginRequest | None): 用户登录信息

    Returns:
        BaseResponse[SafetyUser]: 用户信息(脱敏)

    Raises:
        BusinessException: 登录信息为空 | 参数为空
    """

    # 数据校验
    if user_login_request is None:
        raise BusinessException(StatusCode.NULL_ERROR, "登录信息为空")

    user_account = user_login_request.user_account
    user_password = user_login_request.user_password
    if StringUtils.is_any_blank(user_account, user_password):
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    # 用户登录
    safety_user = await UserService.user_login(user_account, user_password, session)

    return ResultUtils.success(safety_user)


@router.get("/current")
async def get_current_user(session: Session = Depends(session_manager.use_session)) -> BaseResponse[SafetyUser]:
    """
    获取当前用户数据路由

    Args:
        session (Session): 请求实例

    Returns:
        BaseResponse[SafetyUser]: 用户信息(脱敏)
    """

    # 登录校验
    is_login = bool(session[USER_LOGIN_STATE])
    if not is_login:
        raise BusinessException(StatusCode.PARAMS_ERROR, "用户未登录")

    # 获取当前用户数据
    safety_user = await UserService.get_current_user(session)

    return ResultUtils.success(safety_user)


@router.post("/logout")
async def user_logout(session: Session = Depends(session_manager.use_session)) -> BaseResponse[bool]:
    """
    用户注销路由

    Args:
        session (Session): 请求实例

    Returns:
        BaseResponse[bool]: 用户是否完成注销
    """

    # 登录校验
    is_login = bool(session[USER_LOGIN_STATE])
    if not is_login:
        raise BusinessException(StatusCode.PARAMS_ERROR, "用户未登录")

    # 用户注销
    is_logout = UserService.user_logout(session)

    return ResultUtils.success(is_logout)


@router.get("/search")
async def search_users(
        username: str = "",
        session: Session = Depends(session_manager.use_session),
) -> BaseResponse[list[SafetyUser]]:
    """
    搜索用户信息路由

    Args:
        session (Session): 请求实例
        username (str): 用户名

    Returns:
        BaseResponse[list[SafetyUser]]: 用户信息列表(脱敏)

    Raises:
        BusinessException: 用户非管理员
    """

    # 权限校验
    if not UserService.is_admin(session):
        raise BusinessException(StatusCode.NO_AUTH, "用户非管理员")

    # 搜索用户
    safety_users_list = await UserService.search_users_by_username(username)

    return ResultUtils.success(safety_users_list)


@router.get("/recommend")
async def recommend_users(
        request: Request,
        session: Session = Depends(session_manager.use_session),
        page_number: int = 0,
        page_size: int = 0
) -> BaseResponse[Pagination[SafetyUser]]:
    """
    搜索用户信息路由

    Args:


    Returns:
        BaseResponse[list[SafetyUser]]: 用户信息列表(脱敏)

    Raises:
        BusinessException: 用户非管理员
    """

    # 数据校验
    if page_size <= 0 or page_number <= 0:
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数需为正整数")

    # 搜索用户
    safety_users_list = await UserService.get_paginated_users(request, session, page_number, page_size)

    return ResultUtils.success(safety_users_list)


@router.get("/search/tags")
async def search_user_by_tags(
        tag_name_list: list[str] = Query(..., default_factory=list)
) -> BaseResponse[list[SafetyUser]]:
    """
    标签搜索用户路由

    Args:
        tag_name_list: 标签列表

    Returns:
        BaseResponse[list[SafetyUser]]: 用户信息列表(脱敏)

    Raises:
        BusinessException: "参数为空"
    """

    # 数据校验
    if CollectionUtils.is_empty(tag_name_list):
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    # 通过标签搜索用户
    safety_users_list = await UserService.search_users_by_tags(tag_name_list)

    return ResultUtils.success(safety_users_list)


@router.post("/update")
async def update_user(
        user_update_request: UserUpdateRequest | None = None,
        session: Session = Depends(session_manager.use_session)
) -> BaseResponse[int]:
    """
    更新用户信息路由

    Args:
        user_update_request: 用户更新信息
        session: 会话实例

    Returns:
        BaseResponse[int]:

    Raises:
        BusinessException: 参数为空 | 用户非管理员 | 用户ID需为正整数
    """

    # 数据校验
    if user_update_request is None:
        raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

    # TODO: 完善所有数据校验
    user_id = user_update_request.id
    if user_id <= 0:
        raise BusinessException(StatusCode.PARAMS_ERROR, "用户ID需为正整数")

    # 更新用户数据
    result = await UserService.update_user(user_update_request, session)

    return ResultUtils.success(result)


@router.post("/delete")
async def delete_user(
        user_id: int = 0,
        session: Session = Depends(session_manager.use_session)
) -> BaseResponse[bool]:
    """
    逻辑删除用户(逻辑)路由

    Args:
        session (Session): 请求实例
        user_id (int): 用户ID

    Returns:
        BaseResponse[bool]: 用户是否被删除(逻辑)

    Raises:
        BusinessException: 用户非管理员 | 删除用户ID为空 | 用户ID需为正整数
    """

    # 权限校验
    if not UserService.is_admin(session):
        raise BusinessException(StatusCode.NO_AUTH, "用户非管理员")

    # 数据校验
    if user_id <= 0:
        raise BusinessException(StatusCode.PARAMS_ERROR, "用户ID需为正整数")

    # 删除用户(逻辑)
    is_deleted = await UserService.delete_user_by_id(user_id)

    return ResultUtils.success(is_deleted)

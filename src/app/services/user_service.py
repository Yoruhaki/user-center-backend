from math import ceil
from datetime import datetime, timedelta
from functools import reduce, partial
from hashlib import md5
from re import search
from warnings import deprecated
from typing import cast

from tortoise.expressions import Q
from tortoise.transactions import atomic
from fastapi_server_session import Session
from fastapi import Request
from redis.asyncio import Redis

from src.app.common import StatusCode, Pagination
from src.app.constants import USER_LOGIN_STATE, ADMIN_ROLE
from src.app.core import settings
from src.app.exceptions import BusinessException
from src.app.models import User
from src.app.schemas import SafetyUser, UserUpdateRequest
from src.app.utils import CollectionUtils, NoInstantiableMeta, StringUtils


class UserService(metaclass=NoInstantiableMeta):
    """
    用户服务
    """

    __SALT = settings.SALT

    @staticmethod
    def is_admin(session: Session) -> bool:
        """
        根据会话判断用户是否为管理员

        Args:
            session (Session): 请求实例

        Returns:
            bool: 用户是否为管理员
        """

        # 从会话中获取数据
        data = session.get(USER_LOGIN_STATE, None)
        if data is None:
            return False

        # 数据反序列化
        safety_user = SafetyUser.model_validate_json(data)

        # 用户角色必须为管理员
        if safety_user.user_role != ADMIN_ROLE:
            return False

        return True

    @staticmethod
    def get_login_user(session: Session) -> SafetyUser:
        """
        从会话中获取当前登录用户信息

        Args:
            session: 会话实例

        Returns:
            SafetyUser: 用户信息(脱敏)
        """

        # 从会话中获取数据
        data = session.get(USER_LOGIN_STATE, None)
        if data is None:
            raise BusinessException(StatusCode.NOT_LOGIN, "用户未登录")

        # 数据反序列化
        safety_user = SafetyUser.model_validate_json(data)

        return safety_user

    @staticmethod
    @atomic()
    async def user_register(
            user_account: str, user_password: str, confirm_password: str
    ) -> int:
        """
        用户注册

        Args:
            user_account (str): 账户
            user_password (str): 用户密码
            confirm_password (str): 确认密码

        Returns:
            int: 用户ID

        Raises:
            BusinessException: 参数为空 | 用户账号过短 | 用户密码过短 | 账号存在特殊符号
                            | 密码与确认密码不一致 | 账号和密码不匹配 | 账号重复
        """

        # 1. 校验
        # 符合字符长度
        if StringUtils.is_any_blank(user_account, user_password, confirm_password):
            raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")
        if len(user_account) < 4:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户账号过短")
        if len(user_password) < 8 or len(confirm_password) < 8:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户密码过短")

        # 账户不能包含特殊字符
        find_special_char = search(r"[^\w\s]|\s+", user_account)
        if find_special_char:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号存在特殊符号")

        # 密码和确认密码相同
        if user_password != confirm_password:
            raise BusinessException(StatusCode.PARAMS_ERROR, "密码与确认密码不一致")

        # 账户不能重复
        is_exist = await User.filter(user_account=user_account).exists()
        if is_exist:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号重复")

        # 2. 加密
        encrypt_password = md5(
            (UserService.__SALT + user_password).encode()
        ).hexdigest()

        # 3. 插入数据
        user = await User.create(
            user_account=user_account, user_password=encrypt_password
        )

        return user.id

    @staticmethod
    async def user_login(
            user_account: str, user_password: str, session: Session
    ) -> SafetyUser:
        """
        用户登录

        Args:
            user_account (str): 账户
            user_password (str): 用户密码
            session (Session): 请求实例

        Returns:
            SafetyUser: 用户信息(脱敏)

        Raises:
            BusinessException: 参数为空 | 用户账号过短 | 用户密码过短 | 账号存在特殊符号 | 账号和密码不匹配
        """

        # 1. 校验
        # 符合字符长度
        if StringUtils.is_any_blank(user_account, user_password):
            raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")
        if len(user_account) < 4:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户账号过短")
        if len(user_password) < 8:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户密码过短")

        # 账户不能包含特殊字符
        find_special_char = search(r"[^\w\s]|\s+", user_account)
        if find_special_char:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号存在特殊符号")

        # 2. 加密
        encrypt_password = md5(
            (UserService.__SALT + user_password).encode()
        ).hexdigest()

        # 3. 查询用户是否存在
        user = await User.get_or_none(
            user_account=user_account, user_password=encrypt_password
        )
        if user is None:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号和密码不匹配")

        # 4. 用户脱敏
        safety_user = SafetyUser.model_validate(user)

        # 5. 记录用户的登录态
        # session.update({USER_LOGIN_STATE: safety_user.model_dump_json()})
        session.update({USER_LOGIN_STATE: safety_user.model_dump_json()})

        return safety_user

    @staticmethod
    async def get_user_by_id(user_id: int) -> SafetyUser:
        """
        通过用户ID从数据库查询用户数据

        Args:
            user_id (int): 用户ID

        Returns:
            SafetyUser: 用户信息(脱敏)

        Raises:
            BusinessException: 用户不存在
        """

        # 查询用户是否存在
        user = await User.get_or_none(id=user_id)
        if user is None:
            # TODO: 修改描述，使其符合异常情况
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户不存在")

        # 用户信息脱敏
        safety_user = SafetyUser.model_validate(user)

        return safety_user

    @staticmethod
    async def get_current_user(session: Session) -> SafetyUser:
        """
        获取当前用户数据

        Args:
            session (Session): 请求实例

        Returns:
            BaseResponse[SafetyUser]: 用户信息(脱敏)
        """

        # 从会话中获取登录用户数据
        login_user = UserService.get_login_user(session)

        # 根据用户ID从数据库中查询用户信息
        user_id = login_user.id
        safety_user = await UserService.get_user_by_id(user_id)

        return safety_user

    @staticmethod
    async def search_users_by_username(username: str) -> list[SafetyUser]:
        """
        通过用户名搜索用户

        Args:
            username (str): 用户名

        Returns:
            list[SafetyUser]: 用户数据列表(脱敏)
        """

        # 根据筛选条件查询用户数据
        if StringUtils.is_not_blank(username):
            users = await User.filter(username__icontains=username)
        else:
            users = await User.all()

        # 用户信息脱敏
        safety_users_list = list(map(SafetyUser.model_validate, users))

        return safety_users_list

    @staticmethod
    async def get_paginated_users(
            request: Request,
            session: Session,
            page_number: int,
            page_size: int,
            *queryset: Q,
            **filters: ...
    ) -> Pagination[SafetyUser]:
        """
        获取用户分页数据

        Args:
            request:
            session:
            page_number: 页码
            page_size: 每页大小
            *queryset: 查询串实例
            **filters: 筛选条件

        Returns:
            Pagination[SafetyUser]: 用户分页数据(脱敏)
        """

        login_user = UserService.get_login_user(session)
        redis_key = f"compare-friends:user:recommend:{login_user.id}"

        data = await cast(Redis, request.state.redis).get(redis_key)
        if data:
            cache_users_pagination = Pagination[SafetyUser].model_validate_json(data)
            return cache_users_pagination

        # 数据校验
        if page_size <= 0 or page_number <= 0:
            raise BusinessException(StatusCode.PARAMS_ERROR, "参数需为正整数")

        total = await User.filter(*queryset, **filters).count()
        users = await User.filter(*queryset, **filters).offset((page_number - 1) * page_size).limit(page_size)
        pages = ceil(total / page_size)
        safety_users_list = list(map(SafetyUser.model_validate, users))
        safety_users_pagination = Pagination[SafetyUser](
            total=total,
            pages=pages,
            current=page_number,
            size=page_size,
            records=safety_users_list,
        )
        await cast(Redis, request.state.redis).setex(
            redis_key,
            timedelta(days=1),
            safety_users_pagination.model_dump_json()
        )
        return safety_users_pagination

    @staticmethod
    def _compare_user_tags(user: User, tag_name_set: set[str]) -> bool:
        if user.tags is None:
            return False
        user_tag_name_set = set(StringUtils.json_to_string_list(user.tags.lower()))
        if tag_name_set.issubset(user_tag_name_set):
            return True
        return False

    # TODO: 完善注解
    @staticmethod
    async def search_users_by_tags(tag_name_list: list[str]) -> list[SafetyUser]:
        """
        通过标签查询用户(内存处理)

        Args:
            tag_name_list (list[str]): 标签列表

        Returns:
            list[SafetyUser]: 用户数据列表(脱敏)

        Raises:
            BusinessException: <UNK>
        """

        # 数据校验
        if CollectionUtils.is_empty(tag_name_list):
            raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

        # 筛选用户, 并脱敏
        users = await User.all()
        tag_lower_name_set = set(map(lambda x: x.lower(), tag_name_list))
        compare_user_tag_name = partial(UserService._compare_user_tags, tag_name_set=tag_lower_name_set)
        safety_users_list = list(map(SafetyUser.model_validate, filter(compare_user_tag_name, users)))

        return safety_users_list

    # 暂时废弃, 使用内存版本 get_user_by_tags, 处理更灵活
    # TODO: 完善注解
    @staticmethod
    @deprecated("search_user_by_tags_sql()为sql查询, 请使用search_users_by_tags()内存处理版本进行查询")
    async def search_user_by_tags_sql(tag_name_list: list[str]) -> list[SafetyUser]:
        """
        通过标签查询用户(SQL处理)

        Args:
            tag_name_list (list[str]): 标签列表

        Returns:

        """

        # 数据校验
        if CollectionUtils.is_empty(tag_name_list):
            raise BusinessException(StatusCode.PARAMS_ERROR, "参数为空")

        # 查询串拼接
        query = reduce(
            lambda sub_query, tag_name: sub_query & Q(tags__icontains=tag_name),
            tag_name_list,
            Q(),
        )

        # 查询符合筛选条件的用户数据
        users = await User.filter(query)

        # 用户信息脱敏
        safety_users_list = list(map(SafetyUser.model_validate, users))

        return safety_users_list

    # TODO: 完善注解
    @staticmethod
    @atomic()
    async def update_user(user_update_request: UserUpdateRequest, session: Session) -> int:
        """
        更新用户数据

        Args:
            user_update_request:
            session:

        Returns:

        """

        # 数据校验
        user_id = user_update_request.id
        if user_id <= 0:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户ID错误")

        # 从会话中获取当前登录用户信息
        login_user = UserService.get_login_user(session)

        # 如果是管理员, 可以修改任何人的信息
        # 如果是普通用户, 只能修改自己的信息
        if not UserService.is_admin(session) and user_id != login_user.id:
            raise BusinessException(StatusCode.NO_AUTH, "没有权限修改用户数据")

        # 获取被修改用户的旧数据
        old_user_data = await User.get_or_none(id=user_id)

        # 用户必须存在
        if old_user_data is None:
            raise BusinessException(StatusCode.PARAMS_ERROR, "修改用户不存在")

        # TODO: 修改为数据校验, 确保有效修改数据都合法
        # 去除空值和id部分
        update_data = dict(filter(
            lambda x: x[0] != "id" and (x[1] or x[1] == 0),
            user_update_request.model_dump().items()
        ))

        # 更新数据不能完全为空
        if not update_data:
            raise BusinessException(StatusCode.PARAMS_ERROR, "更新数据不能为空")

        # 更新数据
        result = await User.filter(id=user_id).update(**update_data)

        return result

    # TODO: 完善注解
    @staticmethod
    @atomic()
    async def delete_user_by_id(user_id: int) -> bool:
        """
        删除用户(逻辑)

        Args:
            user_id (int): 用户ID

        Returns:
            bool: 用户是否删除成功(逻辑)

        Raises:
            BusinessException: <UNK>
        """

        # 数据校验
        if user_id <= 0:
            raise BusinessException(StatusCode.PARAMS_ERROR, "删除用户ID需为正整数")

        # 逻辑删除用户
        is_deleted = bool(await User.filter(id=user_id).update(is_deleted=True, delete_time=datetime.now()))
        if not is_deleted:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户不存在")

        return is_deleted

    # TODO: 完善注解
    @staticmethod
    def user_logout(session: Session) -> bool:
        """
        用户注销

        Args:
            session (Session): 请求实例

        Returns:
            bool: 用户是否成功注销

        Raises:
            BusinessException: <UNK>
        """

        # 用户必须已登录
        is_login = bool(session.get(USER_LOGIN_STATE, ""))
        if not is_login:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户未登录")

        # 从会话中删除用户信息
        session.clear()

        # 注销用户
        is_logout = not bool(session.get(USER_LOGIN_STATE, ""))

        return is_logout

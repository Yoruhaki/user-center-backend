import hashlib
import re

from fastapi.requests import Request
from tortoise.transactions import atomic

from src.app.common import StatusCode
from src.app.exceptions import BusinessException
from src.app.models import Users
from src.app.schemas import SafetyUser
from src.app.utils import NoInstantiableMeta, StringUtils
from datetime import datetime
from src.app.constants.user_constants import USER_LOGIN_STATE


class UserService(metaclass=NoInstantiableMeta):
    """
    用户服务
    """

    __SALT = "yoruhaki"

    @staticmethod
    @atomic()
    async def user_register(user_account: str, user_password: str, confirm_password: str) -> int:
        """
        用户注册

        Args:
            user_account (str): 账户
            user_password (str): 用户密码
            confirm_password (str): 确认密码

        Returns:
            int: 用户ID

        Raises:
            BusinessException:
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
        find_special_char = re.search(r'[^\w\s]|\s+', user_account)
        if find_special_char:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号存在特殊符号")

        # 密码和确认密码相同
        if user_password != confirm_password:
            raise BusinessException(StatusCode.PARAMS_ERROR, "密码与确认密码不一致")

        # 账户不能重复
        is_exist = await Users.filter(user_account=user_account).exists()
        if is_exist:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号重复")

        # 2. 加密
        encrypt_password = hashlib.md5((UserService.__SALT + user_password).encode()).hexdigest()

        # 3. 插入数据
        user = await Users.create(user_account=user_account, user_password=encrypt_password)

        return user.id

    @staticmethod
    async def user_login(user_account: str, user_password: str, request: Request) -> SafetyUser:
        """
        用户登录

        Args:
            user_account (str): 账户
            user_password (str): 用户密码
            request (Request): 请求实例

        Returns:
            SafetyUser: 用户信息(脱敏)

        Raises:
            BusinessException:
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
        find_special_char = re.search(r'[^\w\s]|\s+', user_account)
        if find_special_char:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号存在特殊符号")

        # 2. 加密
        encrypt_password = hashlib.md5((UserService.__SALT + user_password).encode()).hexdigest()

        # 3. 查询用户是否存在
        user = await Users.get_or_none(user_account=user_account, user_password=encrypt_password)
        if user is None:
            raise BusinessException(StatusCode.PARAMS_ERROR, "账号和密码不匹配")

        # 4. 用户脱敏
        safety_user = SafetyUser.model_validate(user)

        # 5. 记录用户的登录态
        request.session.update({USER_LOGIN_STATE: safety_user.model_dump_json()})

        return safety_user

    @staticmethod
    async def get_current_user_by_id(user_id: int) -> SafetyUser:
        """
        通过用户ID从数据库查询用户信息

        Args:
            user_id (int): 用户ID

        Returns:
            SafetyUser: 用户信息(脱敏)

        Raises:
            BusinessException: code: params_error; description: 用户不存在
        """

        # 查询用户是否存在
        user = await Users.get_or_none(id=user_id)
        if user is None:
            raise BusinessException(StatusCode.PARAMS_ERROR, "用户不存在")

        # 用户信息脱敏
        safety_user = SafetyUser.model_validate(user)

        return safety_user


    @staticmethod
    async def search_users_by_username(username: str) -> list[SafetyUser]:
        """
        搜索用户

        Args:
            username (str): 用户名

        Returns:
            list[SafetyUser]: 用户信息列表(脱敏)
        """

        # 包含用户名查询或获取全部用户
        if StringUtils.is_not_blank(username):
            users = await Users.filter(username__contains=username)
        else:
            users = await Users.all()

        # 用户信息脱敏
        safety_users_list = [SafetyUser.model_validate(user) for user in users]

        return safety_users_list

    @staticmethod
    @atomic()
    async def delete_user_by_id(user_id: int) -> bool:
        """
        搜索用户

        Args:
            user_id (int): 用户ID

        Returns:
            bool: 是否删除成功
        """

        # 逻辑删除用户
        result = await Users.filter(id=user_id).update(is_deleted=True, delete_time=datetime.now())
        print(result)

        return bool(result)

    @staticmethod
    def user_logout(request: Request) -> bool:
        """
        用户注销

        Args:
            request (Request): 请求实例

        Returns:
            bool: 是否成功注销
        """

        # 从会话中删除用户信息
        request.session.pop(USER_LOGIN_STATE, 0)

        return True
import hashlib
import re

from tortoise.transactions import atomic

from src.app.models import Users
from src.app.utils import NoInstantiableMeta, StringUtils


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
        """
        # 1. 校验
        # 符合字符长度
        if StringUtils.is_any_blank(user_account, user_password, confirm_password):
            return -1
        if len(user_account) < 4:
            return -1
        if len(user_password) < 8 or len(confirm_password) < 8:
            return -1

        # 账户不能包含特殊字符
        find_special_char = re.search(r'[^\w\s]|\s+', user_account)
        if find_special_char:
            return -1

        # 密码和确认密码相同
        if user_password != confirm_password:
            return -1

        # 账户不能重复
        is_exist = await Users.filter(user_account=user_account).exists()
        if is_exist:
            return -1

        # 2. 加密
        encrypt_password = hashlib.md5((UserService.__SALT + user_password).encode()).hexdigest()

        # 3. 插入数据
        user = await Users.create(user_account=user_account, user_password=encrypt_password)

        return user.id

    @staticmethod
    async def user_login(user_account: str, user_password: str) -> Users | None:
        """
        用户登录

        Args:
            user_account (str): 账户
            user_password (str): 用户密码

        Returns:
            Users | None: 用户信息 | None
        """
        # 1. 校验
        # 符合字符长度
        if StringUtils.is_any_blank(user_account, user_password):
            return None
        if len(user_account) < 4:
            return None
        if len(user_password) < 8:
            return None

        # 账户不能包含特殊字符
        find_special_char = re.search(r'[^\w\s]|\s+', user_account)
        if find_special_char:
            return None

        # 2. 加密
        encrypt_password = hashlib.md5((UserService.__SALT + user_password).encode()).hexdigest()

        # 3. 查询用户是否存在
        user = await Users.get_or_none(user_account=user_account, user_password=encrypt_password)
        if user is None:
            return None

        return user

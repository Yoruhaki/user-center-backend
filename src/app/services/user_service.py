from src.app.utils import NoInstantiableMeta, StringUtils


class UserService(metaclass=NoInstantiableMeta):
    """
    用户服务
    """

    @staticmethod
    async def user_register(user_account: str, user_password: str, confirm_password: str) -> int:
        """
        用户注册

        Args:
            user_account (str): 用户名
            user_password (str): 用户密码
            confirm_password (str): 确认密码

        Returns:
            int: 用户ID
        """
        # 1. 校验
        if StringUtils.is_any_blank(user_account, user_password, confirm_password):
            return -1
        if len(user_account) < 4:
            return -1
        if len(user_password) < 8 or len(confirm_password) < 8:
            return -1
        # 账户不能重复
        # user = await User.filters(count=Count("user_account"), )
        # if user is not None:
        #     return -1


        return 0

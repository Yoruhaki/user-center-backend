from tortoise.contrib import test

from src.app.models import Users
from src.app.services import UserService


class TestUserService(test.TestCase):

    async def test_user_register(self):
        # 测试数据
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id == 1

        # 不能有空字符
        user_id = await UserService.user_register("", "test", "test")
        assert user_id == -1
        user_id = await UserService.user_register("test", "", "test1234")
        assert user_id == -1
        user_id = await UserService.user_register("test", "test1234", "")
        assert user_id == -1
        # 账户至少4位
        user_id = await UserService.user_register("tes", "test", "test")
        assert user_id == -1
        # 密码至少8位
        user_id = await UserService.user_register("test", "test1234", "test")
        assert user_id == -1
        user_id = await UserService.user_register("test", "test", "test1234")
        assert user_id == -1
        # 两次密码必须一致
        user_id = await UserService.user_register("test", "test12345", "test1234")
        assert user_id == -1
        # 账户不能存在特殊字符
        user_id = await UserService.user_register("te st", "test1234", "test1234")
        assert user_id == -1
        # 账户不能重复
        user_id = await UserService.user_register("test", "test12345", "test12345")
        assert user_id == -1
        # 正常注册
        user_id = await UserService.user_register("yupi", "test12345", "test12345")
        assert user_id > 0

        await (await Users.get(id=1)).soft_delete()
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0

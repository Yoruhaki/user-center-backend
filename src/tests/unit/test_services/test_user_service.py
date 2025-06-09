from fastapi.requests import Request
from tortoise.contrib import test

from app.models import Users
from app.schemas import SafetyUser
from app.services import UserService


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

    async def test_user_login(self):
        # 创建一个模拟的请求对象
        request = Request(scope={"type": "http", "session": {}})

        # 场景 1: 用户输入为空
        result = await UserService.user_login("", "test1234", request)
        assert result is None

        result = await UserService.user_login("test", "", request)
        assert result is None

        # 场景 2: 账户长度不足
        result = await UserService.user_login("tes", "test1234", request)
        assert result is None

        # 场景 3: 密码长度不足
        result = await UserService.user_login("test", "test123", request)
        assert result is None

        # 场景 4: 账户包含特殊字符
        result = await UserService.user_login("te st", "test1234", request)
        assert result is None

        # 场景 5: 用户不存在
        result = await UserService.user_login("nonexistent", "test1234", request)
        assert result is None

        # 场景 6: 密码错误
        await UserService.user_register(
            user_account="validuser",
            user_password="correctpassword",
            confirm_password="correctpassword"
        )
        result = await UserService.user_login("validuser", "wrongpassword", request)
        assert result is None

        # 场景 7: 正常登录
        result = await UserService.user_login("validuser", "correctpassword", request)
        assert isinstance(result, SafetyUser)
        assert result.user_account == "validuser"
        assert request.session.get(UserService._UserService__USER_LOGIN_STATE) is not None

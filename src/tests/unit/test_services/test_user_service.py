import pytest
from fastapi.requests import Request
from tortoise.contrib import test

from src.app.constants.user_constants import USER_LOGIN_STATE
from src.app.exceptions import BusinessException
from src.app.schemas import SafetyUser
from src.app.services import UserService


class TestUserService(test.TestCase):

    # TODO: 完善测试用例以及注解
    async def test_user_register(self) -> None:
        # 初始化数据
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id == 1

        # 不能有空字符
        with pytest.raises(BusinessException) as e:
            # 账号为空
            await UserService.user_register("", "test", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with pytest.raises(BusinessException) as e:
            # 密码为空
            await UserService.user_register("test", "", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with pytest.raises(BusinessException) as e:
            # 确认密码为空
            await UserService.user_register("test", "test1234", "")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        # 账户至少4位
        with pytest.raises(BusinessException) as e:
            await UserService.user_register("tes", "test", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户账号过短"

        # 密码至少8位
        with pytest.raises(BusinessException) as e:
            # 密码过短
            await UserService.user_register("test", "test1234", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        with pytest.raises(BusinessException) as e:
            # 确认密码过短
            await UserService.user_register("test", "test", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        # 账户不能存在特殊字符
        with pytest.raises(BusinessException) as e:
            await UserService.user_register("te st", "test1234", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号存在特殊符号"

        # 两次密码必须一致
        with pytest.raises(BusinessException) as e:
            await UserService.user_register("test", "test12345", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "密码与确认密码不一致"

        # 账户不能重复
        with pytest.raises(BusinessException) as e:
            await UserService.user_register("test", "test12345", "test12345")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号重复"

        # 正常注册
        user_id = await UserService.user_register("yupi", "test12345", "test12345")
        assert user_id > 0

    async def test_user_login(self) -> None:
        # 初始化数据
        request = Request(scope={"type": "http", "session": {}})

        # 场景 1: 用户输入为空
        with pytest.raises(BusinessException) as e:
            # 账号为空
            await UserService.user_login("", "test1234", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with pytest.raises(BusinessException) as e:
            # 密码为空
            await UserService.user_login("test", "", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        # 场景 2: 账户长度不足
        with pytest.raises(BusinessException) as e:
            await UserService.user_login("tes", "test1234", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户账号过短"

        # 场景 3: 密码长度不足
        with pytest.raises(BusinessException) as e:
            await UserService.user_login("test", "test123", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        # 场景 4: 账户包含特殊字符
        with pytest.raises(BusinessException) as e:
            await UserService.user_login("te st", "test1234", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号存在特殊符号"

        # 场景 5: 用户不存在
        with pytest.raises(BusinessException) as e:
            await UserService.user_login("nonexistent", "test1234", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        # 场景 6: 密码错误
        user_id = await UserService.user_register(
            user_account="validuser",
            user_password="correctpassword",
            confirm_password="correctpassword"
        )
        assert user_id > 0

        with pytest.raises(BusinessException) as e:
            await UserService.user_login("validuser", "wrongpassword", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        # 场景 7: 正常登录
        result = await UserService.user_login("validuser", "correctpassword", request)
        assert isinstance(result, SafetyUser)
        assert result.user_account == "validuser"
        assert request.session.get(USER_LOGIN_STATE) is not None

    async def test_get_user_by_id(self) -> None:
        # 用户不存在
        with pytest.raises(BusinessException) as e:
            await UserService.get_user_by_id(user_id=1)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 正常获取用户信息
        user_id = await UserService.user_register(
            user_account="validuser",
            user_password="correctpassword",
            confirm_password="correctpassword"
        )
        assert user_id > 0

        safety_user = await UserService.get_user_by_id(user_id)
        assert isinstance(safety_user, SafetyUser)
        assert safety_user.user_account == "validuser"

    async def test_search_users_by_username(self) -> None:
        # 初始化数据
        from src.app.models import Users

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0
        user_id2 = await UserService.user_register("test2", "test1234", "test1234")
        assert user_id2 > 0

        user_id = await Users.filter(id=user_id).update(username="test1")
        assert user_id > 0
        user_id = await Users.filter(id=user_id2).update(username="test2")
        assert user_id > 0

        # 无搜索条件, 获取所有用户信息
        result = await UserService.search_users_by_username("")
        name_list = [user.username for user in result]
        assert "test1" in name_list
        assert "test2" in name_list

        # 存在搜索条件, 获取相关用户信息
        result = await UserService.search_users_by_username("test1")
        name_list = [user.username for user in result]
        assert "test1" in name_list
        assert "test2" not in name_list

    async def test_delete_user_by_id(self) -> None:
        # 初始化数据
        request = Request(scope={"type": "http", "session": {}})

        # 成功删除指定用户
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0
        is_deleted = await UserService.delete_user_by_id(user_id)
        assert is_deleted

        # 不能删除已被删除的用户
        with pytest.raises(BusinessException) as e:
            await UserService.delete_user_by_id(user_id)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 不能删除不存在的用户
        with pytest.raises(BusinessException) as e:
            await UserService.delete_user_by_id(user_id=10)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 删除后可以重复使用同样账号注册
        with pytest.raises(BusinessException) as e:
            await UserService.user_login("test", "test1234", request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0

    async def test_user_logout(self) -> None:
        # 初始化数据
        request = Request(scope={"type": "http", "session": {}})

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0

        result = await UserService.user_login("test", "test1234", request)
        assert isinstance(result, SafetyUser)
        assert result.user_account == "test"
        assert request.session.get(USER_LOGIN_STATE) is not None

        # 成功注销
        is_logout = UserService.user_logout(request)
        assert is_logout
        assert request.session.get(USER_LOGIN_STATE) is None

        # 用户未登录而注销失败
        with pytest.raises(BusinessException) as e:
            UserService.user_logout(request)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户未登录"



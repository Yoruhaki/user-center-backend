from time import time
from json import dumps

from fastapi.requests import Request
from typing import cast

from fastapi_server_session import Session
from redis.asyncio import Redis
from pytest import raises
from tortoise.contrib import test
from tortoise.functions import Count

from src.app.common import Pagination
from src.app.constants import USER_LOGIN_STATE
from src.app.core import connect_redis
from src.app.exceptions import BusinessException
from src.app.models import User
from src.app.schemas import SafetyUser
from src.app.services import UserService
from asyncio import create_task, gather


class TestInsertUsers(test.TestCase):
    async def test_get_users_page(self):
        result = await User.all().annotate(total=Count('id')).offset(1).limit(10)
        print()
        print(result)

    async def test_insert_users_async(self):
        print()
        start_time = time()

        def generate_user():
            return User(
                username="假纳吉",
                user_account="fake_prpr",
                avatar_url="http://localhost:8000/static/avatar/my_avatar.gif",
                gender=0,
                user_password="<PASSWORD>",
                phone="1234567890",
                email="132154@email.com",
                tags="[]",
                user_status=0,
                user_role=0,
            )

        def generate_task():
            user_list = map(lambda _: generate_user(), range(10_000))

            # 定义一个异步函数来执行批量创建
            async def create_users():
                return await User.bulk_create(user_list, 4_000)

            # 创建异步任务
            return create_task(create_users())

        task_list = list(map(lambda _: generate_task(), range(10)))

        # 等待所有异步任务完成
        await gather(*task_list)
        end_time = time()
        print("cost time:", end_time - start_time)
        print(await User.all().count())


class TestUserService(test.TestCase):
    # TODO: 完善测试用例以及注解
    async def test_user_register(self) -> None:
        # 初始化数据
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id == 1

        # 不能有空字符
        with raises(BusinessException) as e:
            # 账号为空
            await UserService.user_register("", "test", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with raises(BusinessException) as e:
            # 密码为空
            await UserService.user_register("test", "", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with raises(BusinessException) as e:
            # 确认密码为空
            await UserService.user_register("test", "test1234", "")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        # 账户至少4位
        with raises(BusinessException) as e:
            await UserService.user_register("tes", "test", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户账号过短"

        # 密码至少8位
        with raises(BusinessException) as e:
            # 密码过短
            await UserService.user_register("test", "test1234", "test")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        with raises(BusinessException) as e:
            # 确认密码过短
            await UserService.user_register("test", "test", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        # 账户不能存在特殊字符
        with raises(BusinessException) as e:
            await UserService.user_register("te st", "test1234", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号存在特殊符号"

        # 两次密码必须一致
        with raises(BusinessException) as e:
            await UserService.user_register("test", "test12345", "test1234")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "密码与确认密码不一致"

        # 账户不能重复
        with raises(BusinessException) as e:
            await UserService.user_register("test", "test12345", "test12345")
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号重复"

        # 正常注册
        user_id = await UserService.user_register("yupi", "test12345", "test12345")
        assert user_id > 0

    async def test_user_login(self) -> None:
        # 初始化数据
        session = cast(Session, Request(scope={"type": "http", "session": {}}).session)

        # 场景 1: 用户输入为空
        with raises(BusinessException) as e:
            # 账号为空
            await UserService.user_login("", "test1234", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        with raises(BusinessException) as e:
            # 密码为空
            await UserService.user_login("test", "", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "参数为空"

        # 场景 2: 账户长度不足
        with raises(BusinessException) as e:
            await UserService.user_login("tes", "test1234", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户账号过短"

        # 场景 3: 密码长度不足
        with raises(BusinessException) as e:
            await UserService.user_login("test", "test123", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户密码过短"

        # 场景 4: 账户包含特殊字符
        with raises(BusinessException) as e:
            await UserService.user_login("te st", "test1234", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号存在特殊符号"

        # 场景 5: 用户不存在
        with raises(BusinessException) as e:
            await UserService.user_login("nonexistent", "test1234", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        # 场景 6: 密码错误
        user_id = await UserService.user_register(
            user_account="valid_user",
            user_password="correct_password",
            confirm_password="correct_password",
        )
        assert user_id > 0

        with raises(BusinessException) as e:
            await UserService.user_login("valid_user", "wrong_password", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        # 场景 7: 正常登录
        result = await UserService.user_login("valid_user", "correct_password", session)
        assert isinstance(result, SafetyUser)
        assert result.user_account == "valid_user"
        assert session.get(USER_LOGIN_STATE) is not None

    async def test_get_user_by_id(self) -> None:
        # 用户不存在
        with raises(BusinessException) as e:
            await UserService.get_user_by_id(user_id=1)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 正常获取用户信息
        user_id = await UserService.user_register(
            user_account="valid_user",
            user_password="correct_password",
            confirm_password="correct_password",
        )
        assert user_id > 0

        safety_user = await UserService.get_user_by_id(user_id)
        assert isinstance(safety_user, SafetyUser)
        assert safety_user.user_account == "valid_user"

    async def test_search_users_by_username(self) -> None:
        # 初始化数据
        from src.app.models import User

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0
        user_id2 = await UserService.user_register("test2", "test1234", "test1234")
        assert user_id2 > 0

        user_id = await User.filter(id=user_id).update(username="test1")
        assert user_id > 0
        user_id = await User.filter(id=user_id2).update(username="test2")
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

    async def test_get_paginated_users(self) -> None:
        user1_id = await UserService.user_register("test1", "test1234", "test1234")
        assert user1_id > 0
        user2_id = await UserService.user_register("test2", "test1234", "test1234")
        assert user2_id > 0

        request = Request(scope={
            "type": "http",
            "state": {
                "redis": await connect_redis()
            },
            "session": {},
        })
        session = cast(Session, request.session)

        login_user = await UserService.user_login("test1", "test1234", session)
        assert login_user.user_account == "test1"

        page_number = 1
        page_size = 10
        result = await UserService.get_paginated_users(request, session, page_number, page_size,
                                                       user_account__icontains="t1")
        assert result.records[0].id == user1_id

        cache_data = await cast(Redis, request.state.redis).get(f"compare-friends:user:recommend:{user1_id}")
        cache_user_page = Pagination[SafetyUser].model_validate_json(cache_data)
        assert cache_user_page.records[0].id == user1_id

    async def test_get_user_by_tags(self) -> None:
        user1_id = await UserService.user_register("test1", "test1234", "test1234")
        assert user1_id > 0
        user2_id = await UserService.user_register("test2", "test1234", "test1234")
        assert user2_id > 0

        tags = ["java", "python", "C++"]
        tags_json = dumps(tags)
        user_id = await User.filter(id=user1_id).update(tags=tags_json)
        assert user_id > 0

        tags = ["java", "python", "c++"]

        result = await UserService.search_users_by_tags(tags)
        user = result[0]
        assert isinstance(user, SafetyUser)
        assert user.user_account == "test1"

    # 暂时放弃使用
    # async def test_search_user_by_tags_sql(self) -> None:
    #     user_id = await UserService.user_register("test", "test1234", "test1234")
    #     assert user_id > 0
    #     user_id2 = await UserService.user_register("test2", "test1234", "test1234")
    #     assert user_id2 > 0
    #
    #     tags = ["java", "python", "C++"]
    #     tags_json = dumps(tags)
    #     user_id = await User.filter(id=user_id).update(tags=tags_json)
    #     assert user_id > 0
    #
    #     tags = ["java", "python", "c++"]
    #
    #     result = await UserService.search_user_by_tags_sql(tags)
    #     user = result[0]
    #     assert isinstance(user, SafetyUser)
    #     assert user.user_account == "test"

    async def test_delete_user_by_id(self) -> None:
        # 初始化数据
        session = cast(Session, Request(scope={"type": "http", "session": {}}).session)

        # 成功删除指定用户
        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0
        is_deleted = await UserService.delete_user_by_id(user_id)
        assert is_deleted

        # 不能删除已被删除的用户
        with raises(BusinessException) as e:
            await UserService.delete_user_by_id(user_id)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 不能删除不存在的用户
        with raises(BusinessException) as e:
            await UserService.delete_user_by_id(user_id=10)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户不存在"

        # 删除后可以重复使用同样账号注册
        with raises(BusinessException) as e:
            await UserService.user_login("test", "test1234", session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "账号和密码不匹配"

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0

    async def test_user_logout(self) -> None:
        # 初始化数据
        session = cast(Session, Request(scope={"type": "http", "session": {}}).session)

        user_id = await UserService.user_register("test", "test1234", "test1234")
        assert user_id > 0

        result = await UserService.user_login("test", "test1234", session)
        assert isinstance(result, SafetyUser)
        assert result.user_account == "test"
        assert session.get(USER_LOGIN_STATE) is not None

        # 成功注销
        is_logout = UserService.user_logout(session)
        assert is_logout
        assert session.get(USER_LOGIN_STATE) is None

        # 用户未登录而注销失败
        with raises(BusinessException) as e:
            UserService.user_logout(session)
        assert e.value.code == 40000
        assert e.value.message == "请求参数错误"
        assert e.value.description == "用户未登录"

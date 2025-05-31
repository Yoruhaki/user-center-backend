import pytest

from src.app.services import UserService


@pytest.mark.asyncio
async def test_user_register():
    user_id = await UserService.user_register("test", "test", "test")
    assert user_id == 0
    user_id = await UserService.user_register("", "test", "test")
    assert user_id == -1
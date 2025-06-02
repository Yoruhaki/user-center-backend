from tortoise.contrib import test

from src.app.models import Users


class TestUsersModel(test.TestCase):

    async def test_add_user(self):
        user1 = await Users.create(
            username="dog_prpr",
            user_account="123",
            gender=0,
            user_password="123",
            email="123",
            phone="456",
            avatar_url="https://tortoise.github.io/_static/tortoise.png",
        )
        user2 = await Users.create(
            username="dog_prpr",
            user_account="1233",
            gender=0,
            user_password="123",
            email="123",
            phone="456",
            avatar_url="https://tortoise.github.io/_static/tortoise.png",
        )
        assert user1.id > 0
        result = await Users.filter(user_account="123").exists()
        assert result
        await user1.soft_delete()
        result = await Users.filter(user_account="123").exists()
        assert not result
        result = await Users.all_with_deleted()
        print(result)

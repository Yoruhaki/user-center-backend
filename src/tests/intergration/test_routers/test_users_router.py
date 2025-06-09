import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_users(client: AsyncClient):
    response = await client.post("/users/register", json={"user_account": "dog_prpr", "user_password": "12345678", "confirm_password": "12345678"})
    response = await client.post("/users/login", json={"user_account": "dog_prpr", "user_password": "12345678"})
    print()
    print(response.json())
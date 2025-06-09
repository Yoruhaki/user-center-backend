import pytest
from httpx import AsyncClient
from src.app.common import BaseResponse



@pytest.mark.asyncio
async def test_user_register(client: AsyncClient):
    register_data = {
        "user_account": "dog_prpr",
        "user_password": "12345678",
        "confirm_password": "12345678"
    }
    response = await client.post("/users/register", json=register_data)
    assert response.status_code == 200
    response_data = BaseResponse.model_validate(response.json())
    assert response_data.code == 0
    assert response_data.data == 1
    assert response_data.message == "ok"
    assert response_data.description == ""

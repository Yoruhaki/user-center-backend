from httpx import AsyncClient
from pytest import mark

from src.app.common import BaseResponse


@mark.asyncio
async def test_user_register(client: AsyncClient) -> None:
    register_data = {
        "user_account": "dog_prpr",
        "user_password": "12345678",
        "confirm_password": "12345678",
    }

    response = await client.post("/user/register", json=register_data)
    assert response.status_code == 200
    response_data = BaseResponse.model_validate(response.json())
    assert response_data.code == 0
    assert response_data.data == 1
    assert response_data.message == "ok"
    assert response_data.description == ""

    response = await client.post("/user/register", json=register_data)
    assert response.status_code == 200
    response_data = BaseResponse.model_validate(response.json())
    assert response_data.code == 40000
    assert response_data.data is None
    assert response_data.message == "请求参数错误"
    assert response_data.description == "账号重复"

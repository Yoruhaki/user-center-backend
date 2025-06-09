from datetime import datetime

from pydantic import BaseModel, ConfigDict
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.app.models import Users

SafetyUserPydantic = pydantic_model_creator(Users)
SafetyUserPydanticList = pydantic_queryset_creator(Users)


class SafetyUser(BaseModel):
    id: int
    username: str | None
    user_account: str
    avatar_url: str | None
    gender: int | None
    user_role: int | None
    phone: str | None
    email: str | None
    user_status: int
    create_time: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserRegisterRequest(BaseModel):
    user_account: str | None
    user_password: str | None
    confirm_password: str | None


class UserLoginRequest(BaseModel):
    user_account: str | None
    user_password: str | None

class SearchUsersRequest(BaseModel):
    username: str | None
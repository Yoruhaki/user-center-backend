from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, Field
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.app.models import Users

SafetyUserPydantic = pydantic_model_creator(Users)
SafetyUserPydanticList = pydantic_queryset_creator(Users)


class SafetyUser(BaseModel):
    """
    脱敏后的用户校验模型

    Attributes:
        id (int): 用户ID
        username (str | None): 用户名
        user_account (str): 用户账号
        avatar_url (HttpUrl | None): 用户头像
        gender (str | None): 性别
        user_role (int): 用户角色
        phone (str | None): 电话
        email (EmailStr | None): 邮箱
        user_status (int): 用户状态
        create_time (datetime): 创建时间
    """

    id: int = Field(description="用户ID")
    username: str | None = Field(description="用户名")
    user_account: str = Field(description="用户账号")
    avatar_url: HttpUrl | None = Field(description="用户头像")
    gender: int | None = Field(description="性别")
    user_role: int = Field(description="用户角色")
    phone: str | None = Field(description="电话")
    email: EmailStr | None = Field(description="邮箱")
    user_status: int = Field(description="用户状态")
    create_time: datetime = Field(description="创建时间")

    model_config = ConfigDict(
        from_attributes=True
    )


class UserRegisterRequest(BaseModel):
    """
    用户注册请求信息校验模型

    Attributes:
        user_account (str): <UNK>user_account
        user_password (str): <UNK>password
        confirm_password (str): <UNK>confirm_password
    """
    user_account: str | None
    user_password: str | None
    confirm_password: str | None


class UserLoginRequest(BaseModel):
    """
    用户登录请求信息校验模型

    Attributes:
        user_account (str): <UNK>user_account
        user_password (str): <UNK>password
    """
    user_account: str | None
    user_password: str | None

class SearchUsersRequest(BaseModel):
    """
    用户搜索条件校验模型

    Attributes:
        username (str): <UNK>username
    """
    username: str | None
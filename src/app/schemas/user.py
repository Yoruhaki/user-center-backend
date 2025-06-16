from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, Field, AfterValidator
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.app.models import User
from src.app.utils import StringUtils

SafetyUserPydantic = pydantic_model_creator(User)
SafetyUserPydanticList = pydantic_queryset_creator(User)


def check_string_list_json(json_str: str | None) -> str:
    if not StringUtils.is_string_list_json_safe(json_str):
        raise ValueError(f'"{json_str}" 不是序列化的字符串列表')
    return json_str


StringListJSON = Annotated[str, AfterValidator(check_string_list_json)]


class SafetyUser(BaseModel):
    """
    脱敏后的用户校验模型

    Attributes:
        id (int): 用户ID
        username (str | None): 用户名
        user_account (str): 账号
        avatar_url (HttpUrl | None): 头像
        gender (str | None): 性别
        user_role (int): 角色
        phone (str | None): 电话
        email (EmailStr | None): 邮箱
        user_status (int): 状态
        tags (StringListJSON | None) json标签
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
    tags: StringListJSON | None = Field(description="用户json标签")
    create_time: datetime = Field(description="创建时间")

    model_config = ConfigDict(from_attributes=True)


class UserRegisterRequest(BaseModel):
    """
    用户注册请求信息校验模型

    Attributes:
        user_account (str): 账号
        user_password (str): 密码
        confirm_password (str): 确认密码
    """

    user_account: str | None = Field(default=None, description="账号")
    user_password: str | None = Field(default=None, description="密码")
    confirm_password: str | None = Field(default=None, description="确认密码")


class UserLoginRequest(BaseModel):
    """
    用户登录请求信息校验模型

    Attributes:
        user_account (str): 账号
        user_password (str): 密码
    """

    user_account: str | None = Field(default=None, description="账号")
    user_password: str | None = Field(default=None, description="密码")


class UserUpdateRequest(BaseModel):
    id: int = Field(default=0, description="用户ID")
    username: str | None = Field(default=None, description="用户名")
    avatar_url: HttpUrl | None = Field(default=None, description="用户头像")
    gender: int | None = Field(default=None, description="性别")
    phone: str | None = Field(default=None, description="电话")
    email: EmailStr | None = Field(default=None, description="邮箱")

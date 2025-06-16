from tortoise.fields import CharField, SmallIntField, IntField

from .base import BaseModel, SoftDeleteManager, SoftDeleteMixin


class User(SoftDeleteMixin, BaseModel):
    """
    用户映射类

    Attributes:
        username (str | None): 用户名
        user_account (str | None): 用户账号
        gender (int | None): 性别: 0 - 男; 1 - 女
        user_role (int): 用户角色 0 - 普通用户; 1 - 管理员
        user_password (str): 用户密码(加密)
        phone (str | None): 电话
        email (str | None): 邮箱
        user_status (int): 状态: 0 - 正常
        tags (str | None): 用户json标签
    """

    username: str | None = CharField(max_length=256, null=True, description="用户名")
    user_account: str | None = CharField(max_length=256, null=True, description="用户账号")
    avatar_url: str | None = CharField(max_length=1024, null=True, description="用户头像")
    user_profile: str | None = CharField(max_length=512, null=True, description="用户简介")
    gender: int | None = SmallIntField(null=True, description="性别")
    user_role: int = IntField(default=0, null=False, description="用户角色 0 - 普通用户; 1 - 管理员")
    user_password: str = CharField(max_length=512, null=False, description="密码")
    phone: str | None = CharField(max_length=128, null=True, description="电话")
    email: str | None = CharField(max_length=512, null=True, description="邮箱")
    user_status: int = IntField(null=False, default=0, description="状态 0 - 正常")
    tags: str | None = CharField(max_length=1024, null=True, description="用户json标签")

    class Meta:
        table = "user"
        ordering = ["id"]
        table_description = "用户表"
        manager = SoftDeleteManager()

    class PydanticMeta:
        exclude = ("user_password", "update_time", "is_deleted", "delete_time")

from tortoise import fields

from .base import BaseModel, SoftDeleteManager, SoftDeleteMixin


class Users(SoftDeleteMixin, BaseModel):
    """
    用户映射类

    Attributes:
        username (str): 用户名
        user_account (str): 用户账号
        gender (int): 性别: 0 - 男; 1 - 女
        user_role (int): 用户角色 0 - 普通用户; 1 - 管理员
        user_password (str): 用户密码(加密)
        phone (str): 电话
        email (str): 邮箱
        user_status (int): 状态: 0 - 正常
    """

    username = fields.CharField(max_length=256, null=True, description="用户名")
    user_account = fields.CharField(max_length=256, null=True, description="用户账号")
    avatar_url = fields.CharField(max_length=1024, null=True, description="用户头像")
    gender = fields.SmallIntField(null=True, description="性别")
    user_role = fields.IntField(default=0, null=False, description="用户角色 0 - 普通用户; 1 - 管理员")
    user_password = fields.CharField(max_length=512, null=False, description="密码")
    phone = fields.CharField(max_length=128, null=True, description="电话")
    email = fields.CharField(max_length=512, null=True, description="邮箱")
    user_status = fields.IntField(null=False, default=0, description="状态 0 - 正常")

    class Meta:
        table = "users"
        ordering = ["id"]
        table_description = "用户表"
        manager = SoftDeleteManager()

    class PydanticMeta:
        exclude = ("user_password", "update_time", "is_deleted", "delete_time")

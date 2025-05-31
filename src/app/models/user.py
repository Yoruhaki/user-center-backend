from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=256, null=True, description="用户名")
    user_account = fields.CharField(max_length=256, null=True,unique=True, description="用户账号")
    avatar_url = fields.CharField(max_length=1024, null=True, description="用户头像")
    gender = fields.SmallIntField(null=True, description="性别")
    user_password = fields.CharField(max_length=512, null=False, description="密码")
    phone = fields.CharField(max_length=128, null=True, description="电话")
    email = fields.CharField(max_length=512, null=True, description="邮箱")
    user_status = fields.IntField(null=False, default=0, description="状态 0 - 正常")
    create_time = fields.DatetimeField(auto_now_add=True, null=False, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, null=False, description="更新时间")
    is_deleted = fields.BooleanField(default=False, null=False, description="是否删除")

    class Meta:
        table = "users"
        order_by = ("id",)
        table_description = "用户表"

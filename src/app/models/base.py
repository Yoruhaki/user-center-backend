from datetime import datetime

from tortoise.fields import DatetimeField, BooleanField, IntField
from tortoise.manager import Manager
from tortoise.models import Model
from tortoise.queryset import QuerySet


class SoftDeleteManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


class SoftDeleteMixin:
    is_deleted: bool = BooleanField(default=False, null=False, description="软删除标记")
    delete_time: datetime | None = DatetimeField(null=True, description="删除时间")


class BaseModel(Model):
    id: int = IntField(primary_key=True)
    create_time: datetime = DatetimeField(auto_now_add=True, null=False, description="创建时间")
    update_time: datetime = DatetimeField(auto_now=True, null=False, description="更新时间")

    class Meta:
        abstract = True  # 抽象基类，不生成数据库表

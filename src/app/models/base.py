from datetime import datetime

from tortoise import fields
from tortoise.manager import Manager as TortoiseManager  # 引入Manager
from tortoise.models import Model
from tortoise.queryset import QuerySet


class SoftDeleteManager(TortoiseManager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


class BaseModel(Model):
    id = fields.IntField(primary_key=True)
    create_time = fields.DatetimeField(auto_now_add=True, null=False, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, null=False, description="更新时间")
    is_deleted = fields.BooleanField(default=False, null=False, description="软删除标记")
    deleted_at = fields.DatetimeField(null=True, description="删除时间")

    class Meta:
        abstract = True  # 抽象基类，不生成数据库表

    @classmethod
    def all_with_deleted(cls) -> QuerySet[Model]:
        """获取所有记录，包括已删除的（使用原始QuerySet）"""
        return QuerySet(cls)  # 创建一个不带默认软删除过滤的QuerySet

    @classmethod
    def only_deleted(cls) -> QuerySet[Model]:
        """仅获取已删除的记录（使用原始QuerySet并过滤）"""
        return QuerySet(cls).filter(is_deleted=True)

    async def soft_delete(self) -> None:
        """执行软删除"""
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = datetime.now()
            await self.save(update_fields=['is_deleted', 'deleted_at'])

    async def restore(self) -> None:
        """恢复已删除的记录"""
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            await self.save(update_fields=['is_deleted', 'deleted_at'])

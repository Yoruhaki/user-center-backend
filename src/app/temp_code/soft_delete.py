from datetime import datetime
from typing import Self
from typing import override

from tortoise.manager import Manager as TortoiseManager
from tortoise.models import Model
from tortoise.queryset import QuerySet, UpdateQuery, Q, DeleteQuery


class SoftDeleteQuerySet[T: Model](QuerySet[T]):
    """自定义查询集，自动过滤已软删除的记录并提供批量软删除功能"""

    def __init__(self, model: type[T], delete_flag_field: str, delete_date_field: str):
        super().__init__(model)
        self._delete_flag_field = delete_flag_field
        self._delete_date_field = delete_date_field
        # 自动添加is_deleted=False过滤条件
        if hasattr(model, "_meta"):
            meta = getattr(model, "_meta")
            if (
                    hasattr(meta, "fields_map")
                    and self._delete_flag_field in meta.fields_map
            ):
                self._q_objects.append(Q(**{self._delete_flag_field: False}))

    def hard_delete(self) -> DeleteQuery:
        raw_queryset = self._copy_raw_queryset()
        return raw_queryset.delete()

    def soft_delete(self) -> UpdateQuery:
        """批量软删除当前查询集中的所有记录"""
        now = datetime.now()
        # 使用update方法批量更新
        return self.update(
            **{self._delete_flag_field: True, self._delete_date_field: now}
        )

    @override
    def delete(self) -> UpdateQuery:
        return self.soft_delete()

    def _copy_raw_queryset(self) -> QuerySet[T]:
        # 注意：这里需要先移除is_deleted=False的过滤条件
        # 创建一个新的查询集，不包含软删除过滤
        raw_queryset = QuerySet(self.model)
        # 复制当前查询集的所有过滤条件，但排除is_deleted=False
        for key, value in self._filter_kwargs.items():
            if key != "is_deleted":
                raw_queryset = raw_queryset.filter(**{key: value})

        # 复制其他查询条件
        if hasattr(self, "_q_objects") and self._q_objects:
            for q_obj in self._q_objects:
                raw_queryset = raw_queryset.filter(q_obj)
        return raw_queryset

    def restore(self) -> UpdateQuery:
        """批量恢复当前查询集中的所有记录"""
        raw_queryset = self._copy_raw_queryset()
        # 只恢复已删除的记录
        return raw_queryset.filter(is_deleted=True).update(
            is_deleted=False, delete_time=None
        )

    def include_deleted(self) -> Self:
        """返回包含已删除记录的查询集"""
        # 创建新的查询集实例，移除is_deleted过滤
        query = Q(**{self._delete_flag_field: False})
        if query in self._q_objects:
            self._q_objects.remove(query)
        return self

    def only_deleted(self):
        """返回仅包含已删除记录的查询集"""
        return self.include_deleted().filter(is_deleted=True)


class SoftDeleteManager(TortoiseManager):
    """自定义管理器，用于提供 SoftDeleteQuerySet"""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self._model, "is_deleted", "delete_time")

from tortoise.fields import CharField, BigIntField, BooleanField

from .base import BaseModel, SoftDeleteManager, SoftDeleteMixin


class Tag(SoftDeleteMixin, BaseModel):
    """
    标签映射类

    Attributes:
        tag_name (str | None): <UNK>
        user_id (int | None): <UNK>
        parent_id (int | None): <UNK>
        is_parent (bool | None): <UNK>
    """

    tag_name: str | None = CharField(max_length=256, null=True, description="标签名")
    user_id: int | None = BigIntField(null=True, description="用户ID")
    parent_id: int | None = BigIntField(null=True, description="父标签ID")
    is_parent: bool | None = BooleanField(null=True, description="是否为父标签")

    class Meta:
        table = "tag"
        ordering = ["id"]
        indexes = ("user_id",)
        unique_together = ("tag_name",)
        table_description = "标签表"
        manager = SoftDeleteManager()

    class PydanticMeta:
        exclude = ("update_time", "is_deleted", "delete_time")

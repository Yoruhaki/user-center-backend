from collections.abc import Collection

from .metaclass_utils import NoInstantiableMeta


class CollectionUtils(metaclass=NoInstantiableMeta):
    """
    集合体工具类
    """

    @staticmethod
    def is_empty(collection: Collection) -> bool:
        """

        Args:
            collection:

        Returns:
            bool: 是否为空集合体
        """
        if not isinstance(collection, Collection):
            raise TypeError(f"输入的参数需为 Collection 类型, {collection} 为 {type(collection)}")
        return len(collection) == 0

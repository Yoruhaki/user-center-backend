from json import JSONDecodeError, loads
from typing import Any

from .metaclass_utils import NoInstantiableMeta


class StringUtils(metaclass=NoInstantiableMeta):
    """
    字符串工具类
    """

    @staticmethod
    def is_any_blank(*strings: str) -> bool:
        """
        判断字符串序列是否存在空字符串元素

        Args:
            strings (Sequence[str]): 字符串序列

        Returns:
            bool: 是否存在空字符串元素

        Raises:
            TypeError: 如果字符串序列存在非字符串元素
        """

        for string in strings:
            if not isinstance(string, str):
                raise TypeError(f"输入的参数需为 str 类型, {string} 为 {type(string)}")
            if string.isspace() or string.strip() == "":
                return True

        return False

    @staticmethod
    def is_not_blank(*strings: str) -> bool:
        """
        判断字符串序列是否不存在空字符串元素

        Args:
            strings (Sequence[str]): 字符串序列

        Returns:
            bool: 是否不存在空字符串元素

        Raises:
            TypeError: 如果字符串序列存在非字符串元素
        """

        return not StringUtils.is_any_blank(*strings)

    @staticmethod
    def is_str_instance(item: Any) -> bool:
        return isinstance(item, str)

    @staticmethod
    def is_string_list_json_safe(json_str: str) -> bool:
        if not isinstance(json_str, str):
            raise TypeError(f"输入参数需为 str 类型, {json_str} 的类型为 {type(json_str)}")
        try:
            data = loads(json_str)
            if not (isinstance(data, list) and all(map(StringUtils.is_str_instance, data))):
                return False
        except JSONDecodeError:
            return False
        return True

    @staticmethod
    def json_to_string_list(json_str: str) -> list[str]:
        if not isinstance(json_str, str):
            raise TypeError(f"输入参数需为 str 类型, {json_str} 的类型为 {type(json_str)}")
        try:
            data = loads(json_str)
            if not (isinstance(data, list) and all(map(StringUtils.is_str_instance, data))):
                raise ValueError(f'"{json_str}" 不是序列化的字符串列表')
        except JSONDecodeError:
            raise ValueError(f'"{json_str}" 无法反序列化')
        return data

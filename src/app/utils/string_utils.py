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

from typing import NoReturn


class NoInstantiableMeta(type):
    """
    禁止类实例化元类
    """

    def __call__(cls, *args, **kwargs) -> NoReturn:
        # 禁用（）调用
        raise TypeError(f"{cls.__name__} 不能被实例化")

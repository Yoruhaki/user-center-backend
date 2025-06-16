from functools import partial
from os import PathLike, listdir
from os.path import isdir, join, exists, isfile
from re import match
from typing import TypeGuard
from importlib import import_module
from types import ModuleType

from .metaclass_utils import NoInstantiableMeta

type ImportPath = str


# TODO: 完善注解, 异常处理, 如 import path 参数类型错误, file path 参数类型错误
class ModuleUtils(metaclass=NoInstantiableMeta):
    """
    模块工具类
    """

    @staticmethod
    def is_valid_module_path(path: str) -> TypeGuard[ImportPath]:
        """
        验证字符串是否符合 Python 模块路径格式
        """
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$'
        return bool(match(pattern, path))

    @staticmethod
    def check_module_name(package_path: str | PathLike[str], module_name: str) -> str:
        """


        Args:
            package_path:
            module_name:

        Returns:

        """
        full_path = join(package_path, module_name)
        if isfile(full_path) and full_path.endswith(".py") and module_name != "__init__.py":
            return module_name[:-3]
        elif isdir(full_path) and exists(join(full_path, "__init__.py")):
            return module_name
        return ""

    @staticmethod
    def get_modules_name(package_path: str | PathLike[str]) -> list[str]:
        """
        扫描包中模块名称

        Args:
            package_path: 包路径

        Returns:
            modules: 模块名称列表
        """

        check_module_name_from_path = partial(ModuleUtils.check_module_name, package_path)

        modules_name_list = list(filter(lambda x: x != "", map(check_module_name_from_path, listdir(package_path))))

        return modules_name_list

    @staticmethod
    def get_modules_import_path(package_path: str | PathLike[str], package_import_path: ImportPath) -> list[str]:
        """
        扫描包中模块名称

        Args:
            package_path: 包路径
            package_import_path:

        Returns:
            modules_import_path: 模块名称列表
        """

        modules_import_path_list = list(map(
            lambda x: f"{package_import_path}.{x}",
            ModuleUtils.get_modules_name(package_path)
        ))

        return modules_import_path_list

    @staticmethod
    def import_modules(package_path: str | PathLike[str], package_import_path: ImportPath) -> list[ModuleType]:
        """

        Args:
            package_path:
            package_import_path:

        Returns:

        """
        return list(map(import_module, ModuleUtils.get_modules_import_path(package_path, package_import_path)))

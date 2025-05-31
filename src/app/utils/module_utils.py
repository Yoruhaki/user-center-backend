import os

from .metaclass_utils import NoInstantiableMeta


class ModuleUtils(metaclass=NoInstantiableMeta):
    @staticmethod
    def scan_modules_names(package_path) -> list[str]:
        modules: list[str] = []
        try:
            for entry in os.listdir(package_path):
                full_path = os.path.join(package_path, entry)
                if os.path.isfile(full_path) and full_path.endswith('.py') and entry != '__init__.py':
                    modules.append(entry[:-3])
                elif os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, '__init__.py')):
                    modules.append(entry)
        except FileNotFoundError:
            print()
        return modules

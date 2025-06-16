from os import PathLike
from os.path import join as path_join

from src.app.core import settings
from src.app.utils import ModuleUtils


def test_scan_modules_names():
    from src.app import models
    ls = ModuleUtils.get_modules_import_path(models.__path__[0], models.__name__)
    print()
    print(ls, isinstance(models.__name__, PathLike))

    d = {
        # "id": 1,
        # "username": "",
        # "user_account": "dog_prpr",
        # "avatar_url": "http://localhost:8000/static/avatar/my_avatar.gif",
        # "gender": 0,
        # "user_role": 1,
        # "phone": "13411255890",
        # "email": "15949844447@qq.com",
        # "user_status": 0,
        "tags": None,
        "create_time": None
    }

    print(dict(filter(lambda x: x[0] != "id" and (x[1] or x[1] == 0), d.items())))
    pass

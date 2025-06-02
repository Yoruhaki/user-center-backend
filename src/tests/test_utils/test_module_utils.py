import hashlib
import re

from src.app import services
from src.app.utils import ModuleUtils


def test_scan_modules_names():
    print()
    print(ModuleUtils.scan_modules_names(services.__path__[0]))
    SALT = "yoruhaki"
    password_hashed = hashlib.md5((SALT + "12345").encode()).hexdigest()
    print("hashed password:", password_hashed)
    # find_special_char = re.search(r'[^\w\s]|\s+', password_hashed)
    str1 = "Hello, world!"
    result = re.findall(r'[^\w\s]|\s+', str1)
    print(result)
    print(str(None))

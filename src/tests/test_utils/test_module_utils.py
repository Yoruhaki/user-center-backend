from src.app.utils import ModuleUtils

def test_scan_modules_names():
    from src.app import services
    print()
    print(ModuleUtils.scan_modules_names(services.__path__[0]))
    # print(services.__path__)
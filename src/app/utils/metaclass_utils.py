class NoInstantiableMeta(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} 不能被实例化")
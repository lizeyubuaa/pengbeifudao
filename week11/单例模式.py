class SingleTon:
    def __init__(self):
        pass

    # 重写了__new__方法
    def __new__(cls, *args, **kwargs):
        if not hasattr(SingleTon, '_instance'):
            # 可以调用父类的__new__方法
            SingleTon._instance = object.__new__(cls)
        # 注意最后要返回一个实例化的对象
        return SingleTon._instance

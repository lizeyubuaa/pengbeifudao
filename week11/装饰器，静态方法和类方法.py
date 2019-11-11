import time

from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("call " + func.__name__)
        return func(*args, **kwargs)

    return wrapper


@log
def now():
    print(time.strftime('%Y-%m-%d', time.localtime(time.time())))


now()
print(now.__name__)


# now=log(now), now() == log(now)()

def log(text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(text + ' ' + 'call ' + func.__name__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log('日志：')
def now():
    print(time.strftime('%Y-%m-%d', time.localtime(time.time())))


print(now.__name__)
now()  # now = log('日志：')(now),now() == log('日志')(now)()


class Log:
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = "INFO: " + func.__name__ + " was called"
            with open(self.logfile, 'a') as file:
                file.write(info + '\n')
            return func(*args, **kwargs)

        return wrapper


@Log('test.log')
def myfunc():
    pass


myfunc()


class Student:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_value):
        self._id = id_value

    @id.deleter
    def id(self):
        del self._id


s = Student(12)
print(s.id)
s.id = 18
print(s.id)


class Finder:
    def __init__(self, path):
        self._path = path

    # 和类外面的函数一样，没有使用类的属性作为参数
    @staticmethod
    def list_files(dir):
        print("{} contains files as listed:".format(dir))
        pass

    # 静态方法，使用cls替换了self
    @classmethod
    def list_dirs(cls, root):
        print("class info: {}".format(cls), end=" ")
        print("list dirs in {}".format(root))
        pass


Finder.list_files('test')
Finder.list_dirs('test')

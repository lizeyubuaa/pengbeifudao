import time


# 观察者只有更新状态属性，可以派生子类
class Observer:
    def update(self, info):
        pass


# 基类，可以派生股票、基金等子类
class Subject:
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyAll(self, info):
        for observer in self.observers:
            # 调用了观察者的update函数
            observer.update(info)


class Investor(Observer):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def update(self, info):
        print("Alarm:{}".format(info))


class Student(Observer):
    def update(self, info):
        pass


# 股票
class Stock(Subject):
    def __init__(self, name, price):
        super().__init__()
        self._name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if self._price > value:
            info = "Stock {}'s price decrease from {} to {}".format(self._name, self._price, value)
            self.notifyAll(info)
        self._price = value


class Future(Subject):
    def __init__(self, name, volume):
        super().__init__()
        self._name = name
        self._volume = volume

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if self._volume < value:
            info = "Future {}'s volume grows from {} to {}".format(self._name, self._volume, value)
            self.notifyAll(info)
        self._volume = value


def main():
    s = Stock("区块链", 11.0)
    f = Future("猪肉", 2000)
    for i in range(10):
        inv = Investor(str(i + 1))
        s.addObserver(inv)
        f.addObserver(inv)
    s.price = 8.0
    time.sleep(1)
    f.volume = 3000


if __name__ == '__main__':
    main()

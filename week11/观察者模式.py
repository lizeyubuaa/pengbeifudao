import time


class Investor:
    # 股票名字
    def __init__(self, name, stock):
        # 单下划线只可以在类内使用
        self._name = name
        # 有的人没买股票，有的人买了多只股票；不应该存储股票
        self._stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    def update(self):
        print("{} invest on {} with price {}: sell it now!!!".format(self._name, self._stock.name, self._stock.price))


class Stock:
    def __init__(self, name, price):
        self._name = name
        self._price = price
        # 关键属性
        self._investors = []

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if self._price > value:
            # 通知函数
            self.notify()
        self._price = value

    # 成员更新函数
    def attach(self, investor):
        self._investors.append(investor)

    def notify(self):
        for investor in self._investors:
            investor.update()


def main():
    s = Stock('区块链', 11.11)
    i1 = Investor('zjc', s)
    i2 = Investor('lys', s)
    s.attach(i1)
    s.attach(i2)
    s.price = 13
    time.sleep(1)
    s.price = 10


if __name__ == '__main__': main()

"""
除下实现方式外，还对以对工厂进一步进行抽象，得到抽象工厂，使得进一步解耦，
不再通过参数来得到要生产的类的对象。
"""


class Fruit:
    pass


class Apple(Fruit):
    pass

    def pie(self):
        print("making apple pie")


class Orange(Fruit):
    pass

    def juice(self):
        print("making orange juice")


# 没有构造函数
class FruitFactory:

    def generate_fruit(self, type):
        if type == 'a':
            return Apple()  # 可以根据apple的定义进行初始化
        elif type == 'o':
            return Orange()  # 可以根据orange的定义进行初始化
        else:
            return None


ff = FruitFactory()
apple = ff.generate_fruit('a')
orange = ff.generate_fruit('o')
apple.pie()
orange.juice()


# “抽象”工厂的简要实现：所有类的工厂类都继承自一个抽象工厂，他们可能具有某些相同的方法
class Factory:

    def generate(self):
        pass


class AppleFactory(Factory):

    def generate(self):
        return Apple()  # 工厂只生产苹果


class OrangeFactory(Factory):

    def generate(self):
        return Orange()  # 工厂只生产橘子

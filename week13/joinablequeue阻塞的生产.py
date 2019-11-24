import os
import random
import time
# 消费者发消息
from multiprocessing import JoinableQueue
from multiprocessing import Process


# 生产的产品对象
class Product:
    def __init__(self, name, volume):
        # 名字
        self._name = name
        # 体积
        self._volume = volume

    # 定义了打印方法
    def __str__(self):
        return "Name:{}\tVolume:{}".format(self._name, self._volume)


def consume(q):
    prod = q.get()
    # 消费一段时间
    time.sleep(random.randint(1, 5))
    print("{} consumes {}".format(os.getpid(), prod))
    # 发送信号，表明数据获取成功
    q.task_done()


def produce(q):
    prod = Product(str(os.getpid()) + "_pro", random.randint(10, 100))
    # 生产一段时间
    time.sleep(random.randint(1, 5))
    q.put(prod)
    print("{} produces {}".format(os.getpid(), prod))
    # 停一下
    q.join()


if __name__ == '__main__':
    q = JoinableQueue()
    producers = []
    consumers = []
    # 共用同一个队列对象，实现在同一数据结构上控制流程
    for i in range(0, 2):
        p = Process(target=produce, args=(q,))
        producers.append(p)
    for i in range(0, 100):
        c = Process(target=consume, args=(q,))
        c.daemon = True
        consumers.append(c)
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    for p in producers:
        p.join()
    print('main')

import os
import random
import time
# 队列模型，起到同步作用。同一时间只有一个进程取数据，插数据。是除了加锁外的另外一种机制。
from multiprocessing import Process, Queue


# 生产者进程的制造任务函数
def produce(q):
    time.sleep(random.random())
    # 往队列里放数据。只生产了一辆汽车。
    q.put('car_by_{}'.format(os.getpid()))
    print("{} produces a car...".format(os.getpid()))


# 消费者进程的消费任务函数
def buy(q):
    car = q.get()
    # 没买到，返回NONE，接着等
    if car is None:
        return
    else:
        time.sleep(random.random())
        print("{} buy the car {}".format(os.getpid(), car))


if __name__ == '__main__':
    # 共用同一个队列对象，实现在同一数据结构上控制流程
    q = Queue()
    # 两种不同的进程
    procucers = []
    consumers = []
    # 两个生产者，只能生产两辆汽车
    for i in range(0, 2):
        p = Process(target=produce, args=(q,))
        procucers.append(p)
    # 100个消费者，有人等
    for i in range(0, 100):
        c = Process(target=buy, args=(q,))
        consumers.append(c)
    # 先启动生产者或者先启动消费者
    for p in procucers:
        p.start()
    for p in procucers:
        p.join()
    for c in consumers:
        c.start()
    # 主进程发信号结束，注意要给每一个consumer发
    for c in consumers:
        q.put(None)
    print('main')

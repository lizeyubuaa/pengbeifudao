import json
import random
import time
# 互斥锁
from multiprocessing import Lock
from multiprocessing import Process

# 记录了起点、终点和余票
tf = 'ticks.json'


# 任务函数中的打印信息函数
def info():
    # 得到的ticks是字典类型
    ticks = json.load(open(tf))
    print("ticks from {} to {} left {}".format(ticks['origin'], ticks['dest'], ticks['count']))


# 任务函数中的买票函数
def buy():
    ticks = json.load(open(tf))
    # 随机休眠，打乱进程的执行节奏。random返回0-1之间的随机浮点数。
    time.sleep(random.random())
    if ticks['count'] > 0:
        ticks['count'] -= 1
        time.sleep(random.random())
        json.dump(ticks, open(tf, 'w'))
        print('buy one tick from {} to {}!'.format(ticks['origin'], ticks['dest']))
    # 在没票的时候，告诉进程没票了，别访问了；否则等待到锁释放后还会继续访问，直到买到票
    else:
        print('oh....no ticks :(')


def task():
    info()
    buy()


# 任务函数有了参数lock（是实例化的对象）。加锁
def lock_task(lock):
    info()
    # 进入临界区，请求锁acquire。
    lock.acquire()
    # 用try-except语句，因为需要执行清理操作（释放锁）。
    try:
        buy()
    finally:
        # 释放release
        lock.release()


if __name__ == '__main__':
    lock = Lock()
    clients = []
    # 有10个人买票
    for i in range(10):
        # p = Process(target=task)
        # 将实例化的lock对象传入args参数中。
        p = Process(target=lock_task, args=(lock,))
        clients.append(p)
    for p in clients:
        p.start()
    # 一般都要这么写。同步进程。
    for p in clients:
        p.join()
    print("all clients fininshed...")

import random
import time
from multiprocessing import Process
# 信号量对象
from multiprocessing import Semaphore
# 返回当前进程名字的函数
from multiprocessing import current_process


def get_connections(s):
    # 取得信号量（理解为信号灯变为绿灯）
    s.acquire()
    print(current_process().name + ' acqiure a connection')
    # 模拟网络延迟，打乱进程执行的节奏
    time.sleep(random.randint(1, 3))
    # 没有干实际的事情，就是等了一会
    print(current_process().name + ' finishes its job and return the connection')
    # 释放信号量
    s.release()


if __name__ == '__main__':
    # 5表示最多有5个进程可以获得链接
    connections = Semaphore(5)
    workers = []
    # 一共有十个进程
    for i in range(10):
        p = Process(target=get_connections, args=(connections,), name='worker:' + str(i + 1))
        workers.append(p)
    for p in workers:
        p.start()
    for p in workers:
        p.join()
    print("all workers exit")

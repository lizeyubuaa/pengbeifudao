import random
import time
# 引入了事件，拿到权限后，如果指定事件发生，仍然需要继续等待。
from multiprocessing import Event
from multiprocessing import Process


# 模拟汽车过十字路口。两个参数，事件和名字
def car(event, name):
    # 事件发生（变为绿灯）
    if event.is_set():
        time.sleep(random.random())
        print("car {} passes...".format(name))
    else:
        print("car {} waits...".format(name))
        # 阻塞直至事件状态发生变化
        event.wait()


# 红绿灯
def light(event):
    # 用死循环
    while True:
        if event.is_set():
            # 清除事件
            event.clear()
            print("红灯")
        else:
            # 事件发生，可以执行！
            event.set()
            print("绿灯")
        # 绿灯和红灯的持续时间是随机的
        time.sleep(random.random())


if __name__ == '__main__':
    event = Event()
    # 先clear
    event.clear()
    l = Process(target=light, args=(event,))
    # 守护进程，在start之前！
    l.daemon = True
    l.start()
    cars = []
    # 20辆车等待通过
    for i in range(20):
        c = Process(target=car, args=(event, 'c_' + str(i + 1)))
        cars.append(c)
    for c in cars:
        c.start()
    for c in cars:
        c.join()
    print("all cars passed...")

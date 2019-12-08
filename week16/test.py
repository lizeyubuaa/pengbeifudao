import random
import threading
import time

# 定义食物列表
foods = list()
# 创建一个线程条件对象
con = threading.Condition()


def product():
    while True:
        time.sleep(0.5)
        con.acquire()
        if len(foods) < 20:
            _no = random.randint(0, 20)
            print("生产者{}生产了{}".format(threading.current_thread().getName(), _no))
            foods.append(_no)
            print("PRO--", len(foods))
            con.notify()
        else:
            con.wait()
            print("生产者{}----等待".format(threading.current_thread().getName()))
            con.release()


def consumer():
    while True:
        time.sleep(0.5)
        con.acquire()
        if len(foods) > 0:
            _no = foods.pop()
            print("消费者{}消费了".format(threading.current_thread().getName()), _no)
            print("CUS--", len(foods))
            con.notify()
        else:
            con.wait()
            print("消费者{}-----等待".format(threading.current_thread().getName()))
            con.release()


if __name__ == "__main__":
    # 创建多个生产者线程
    for i in range(5):
        p = threading.Thread(name="_p" + str(i), target=product)
        p.start()
    # 创建多个消费者线程
    for j in range(2):
        c = threading.Thread(name="_c" + str(j), target=consumer)
        c.start()

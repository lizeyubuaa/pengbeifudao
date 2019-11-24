import random
import time
from multiprocessing import Process

# 展示了创建多进程的两种方法！

# 全局变量，各个进程的n值是不共享的！
n = 0


# 任务函数
def task(name):
    print("task of {} starts".format(name))
    # 作用：随机休眠，类似于网络延迟，打乱进程执行的节奏。randrange返回随机整数！
    time.sleep(random.randrange(50, 100))
    print("task of {} ends".format(name))


# 任务类
class Task(Process):
    def __init__(self, name, *args, **kwargs):
        # 不能忘了对父类的初始化
        super().__init__(*args, **kwargs)
        # task的名字，和进程的名字区分开来
        self._name = name

    # property修饰，可以访问名字属性
    @property
    def name(self):
        return self._name

    # 必须实现的方法
    def run(self):
        # pid是父类process的属性
        print('task {} starts with pid {}...'.format(self.name, self.pid))
        global n
        # 为了体现不同进程的n值不共享！返回0，1之间浮点数！
        n = random.random()
        print("n={} in process {}".format(n, self.name))
        # 观察内存的不同
        l = list(range(int(n * 100000000)))
        time.sleep(random.randrange(5, 10))
        print('task {} ends with pid {}...'.format(self.name, self.pid))


if __name__ == '__main__':
    # for i in range(0, 4):
    #     p = Process(target=task, args=('task {}'.format(i),))
    #     p.start()
    #     print('pid:{}'.format(p.pid))
    plist = []
    for i in range(0, 4):
        # 仅仅传入了名字
        p = Task('process-{}'.format(i + 1))
        plist.append(p)
    for p in plist:
        p.start()
    for p in plist:
        # 注意一定是先子进程都启动后，再一一join，否则启动后马上join会变成“串行”，一个执行
        # 完再执行另一个！main等待的时间是四个进程执行的最长时间！
        pass
        p.join()
    print('main')
    print("n={} in main".format(n))

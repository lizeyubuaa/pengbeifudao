# 在windows上会有问题
from multiprocessing import Process

print('main process start')


def run():
    pass


# WIN中没有卸载main函数里，会报错
p = Process(target=run)
p.start()
if __name__ == '__main__':
    pass

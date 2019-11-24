import random
import time
from multiprocessing import Process, Pipe


# 接收进程
def receiver(pipe, name):
    recv, send = pipe
    # 把send关闭
    send.close()
    while True:
        try:
            message = recv.recv()
            print("{} receives a message: {}".format(name, message))
        except EOFError as eof:
            recv.close()
            break


def sender(pipe, name, messages):
    recv, send = pipe
    # 把接收关闭
    recv.close()
    for message in messages:
        send.send(message)
        time.sleep(random.randint(1, 3))
    send.close()


if __name__ == '__main__':
    messages = []
    with open('po.txt', encoding='utf-8', mode='r') as f:
        for line in f:
            messages.append(line.strip())
    # 在process前创建
    recv, send = Pipe()

    printer = Process(target=receiver, args=((recv, send), 'printer'))
    printer.start()

    sender = Process(target=sender, args=((recv, send), 'sender', messages))
    sender.start()
    # 及时关闭！
    recv.close()
    send.close()

    sender.join()
    print("所有消息发送完成")
    printer.join()
    print('所有消息接收完成...')

from socket import *
from threading import Thread

BUFFERS = 1024
MAXC = 64


def speak(name, conn):
    print("欢迎{}进入聊天室...".format(name))
    while True:
        try:
            msg = conn.recv(BUFFERS)
            if not msg:
                break
            print("{}:{}".format(name, msg.decode('utf-8')))
            conn.send("收到".encode('utf-8'))
            if msg.decode('utf-8') == 'byebye':
                print("{}离开了聊天室...".format(name))
                break
        except Exception as e:
            print("server error %s" % e)
            break
    conn.close()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(MAXC)

    while True:
        conn, addr = server.accept()
        ci, cp = addr
        # 一有一个客户，立马开一个线程
        t = Thread(target=speak, args=("client-" + ci + "-" + str(cp), conn))
        t.start()
    server.close()

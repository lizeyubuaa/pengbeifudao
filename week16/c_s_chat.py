from socket import *
from threading import Thread

BS = 2048


def recv(name, conn):
    while True:
        data = conn.recv(BS)
        if not data:
            break
        if data.decode('utf-8') == 'BYEBYE':
            print("对方提议停止聊天，输入BYEBYE可终止...")
            break
        else:
            print("%s: %s" % (name, data.decode('utf-8')))


def send(conn):
    while True:
        msg = input("")
        if not msg:
            continue
        conn.send(msg.encode('utf-8'))
        if msg == 'BYEBYE':
            break


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    name = 'server'  # server, client
    server = socket(AF_INET, SOCK_STREAM)
    if name == 'server':
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(5)
        conn, addr = server.accept()
    if name == 'client':
        server.connect((ip, port))
        addr = (ip, port)
        conn = server
    # 无论是服务器还是客户端都是两个线程（收发）
    tr = Thread(target=recv, args=(str(addr), conn))
    tr.start()
    ts = Thread(target=send, args=(conn,))
    ts.start()
    tr.join()
    ts.join()
    conn.close()
    server.close()

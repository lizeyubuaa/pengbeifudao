from socket import *

HOST = '127.0.0.1'
PORT = 8080
RSIZE = 1024


class TCPServer:
    # 指定最大连接数
    def __init__(self, port, maxconnections=5):
        # IP不变（机器），port是可变的
        self._port = port
        self._maxconnections = maxconnections
        # 创建套接字
        self._server = socket(AF_INET, SOCK_STREAM)

    def start(self):
        # 重用地址
        self._server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._server.bind((HOST, self._port))
        self._server.listen(self._maxconnections)
        print("SERVER is listening on %s" % self._port)
        while True:
            # accept返回两个参数
            conn, addr = self._server.accept()
            print(conn)
            print(addr)
            while True:
                try:
                    data = conn.recv(RSIZE)
                    if not data:
                        break
                    print("CLIENT: %s" % data.decode('utf-8'))
                    # 先解码
                    if data.decode('utf-8') == 'bye':
                        # 要编码
                        conn.send("再见!".encode('utf-8'))
                        break
                    else:
                        # 要编码
                        conn.send('收到!'.encode('utf-8'))
                except Exception as e:
                    print("SERVER ERROR: %s" % e)
                    break
            conn.close()
        self._server.close()


def main():
    ser = TCPServer(PORT)
    ser.start()


if __name__ == '__main__':
    main()

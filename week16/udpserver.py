from socket import *

ipaddr = '127.0.0.1'
port = 8080
recv_size = 1024

udp_server = socket(AF_INET, SOCK_DGRAM)
udp_server.bind((ipaddr, port))
print("bind udp on port %s" % port)
while True:
    data, addr = udp_server.recvfrom(recv_size)
    if not data:
        break
    else:
        print("%s: %s" % (addr, data.decode('utf-8')))
        udp_server.sendto("收到".encode('utf-8'), addr)

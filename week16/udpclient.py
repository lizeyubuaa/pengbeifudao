from socket import *

ipaddr = '127.0.0.1'
port = 8080

udp_client = socket(AF_INET, SOCK_DGRAM)

while True:
    msg = input("CLIENT:")
    udp_client.sendto(msg.encode("utf-8"), (ipaddr, port))
    reply, addr = udp_client.recvfrom(1024)
    if not reply:
        break
    else:
        print("%s: %s" % (addr, reply.decode('utf-8')))

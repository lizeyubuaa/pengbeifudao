from socket import *

client = socket(AF_INET, SOCK_STREAM)
ip = '127.0.0.1'
port = 8080
client.connect((ip, port))
while True:
    msg = input(">>>:")
    if not msg:
        continue
    if msg == 'exit':
        break
    client.send(msg.encode('utf-8'))
    data = client.recv(1024)
    print(data.decode('utf-8'))
client.close()

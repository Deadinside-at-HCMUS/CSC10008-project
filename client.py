import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'Hello, World!'

s = socket.socket()
s.connect((TCP_IP, TCP_PORT))
BYT = MESSAGE.encode()
s.send(BYT)
print("Send message!")
s.close()

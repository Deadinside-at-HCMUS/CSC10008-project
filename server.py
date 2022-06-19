import socket

# define host and port server listening
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # number bytes that server can received once time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)  # 1 is number of conection appected
print("Server listening on port", TCP_PORT)

c, addr = s.accept()  # c: connection, addr: addr of request/client
print('Connect from:', addr)

# client send to server
while 1:
    data = c.recv(BUFFER_SIZE)
    if not data:
        break
    print("Server received data:", data.decode())
    c.send(data)
c.close()

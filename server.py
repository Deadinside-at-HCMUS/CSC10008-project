from email import message
import socket
from signin import *

# define host and port server listening
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # number bytes that server can received once time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)  # 1 is number of conection appected
print("Server listening on port", TCP_PORT)

c, addr = s.accept()  # c: connection, addr: addr of request/client
print('Connect from:', addr)

# loading account into list
account = []
account = loadData()

# login, break if login success
while True:
    c.send(("Login or Register?").encode())
    mes = (c.recv(BUFFER_SIZE)).decode()
    if mes == "Login":
        c.send(("Username: ").encode())
        username = (c.recv(BUFFER_SIZE)).decode()
        c.send(("Password: ").encode())
        password = (c.recv(BUFFER_SIZE)).decode()
        if login(account, username, password):
            c.send(("Login Success!").encode())
            break
        else:
            c.send(("Your username or password is incorrect!").encode())
    elif mes == "Register":
        c.send(("Username: ").encode())
        username = (c.recv(BUFFER_SIZE)).decode()
        while not isValidUsername(username):
            c.send(("Invalid!").encode())
            username = (c.recv(BUFFER_SIZE)).decode()
        c.send(("Password: ").encode())
        password = (c.recv(BUFFER_SIZE)).decode()
        while not isValidPassword(password):
            c.send(("Invalid!").encode())   
            password = (c.recv(BUFFER_SIZE)).decode()
        c.send(("Register success!").encode())
        account.append({"username": username, "password": password})
    else:
        c.send(("Invalid input!").encode())

# client send to server
while True:
    data = c.recv(BUFFER_SIZE).decode()
    if data == "quit":
        break
    print("Server received data:", data)
    c.send(data)
c.close()

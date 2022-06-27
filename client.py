import socket
import sys
from signin import *

# Client set up
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'Hello, World!'

if __name__ == '__main__':
    try:
        client = socket.socket()
    except socket.error as s_e:
        print("Error creating socket: ", s_e)
        sys.exit(1)

    try:
        client.connect((TCP_IP, TCP_PORT))
        print(f"Connected to server {TCP_IP} in port {TCP_PORT}")
        # Login.page()
        # BYT = MESSAGE.encode()
        # client.send(BYT)
        # print("Send message!")
        
        # login, break if login success
        while True:
            mes = client.recv(BUFFER_SIZE)
            print(mes.decode())
            mes = str(input())
            client.send(mes.encode())
            if mes == "Login":
                mes = client.recv(BUFFER_SIZE).decode()
                print(mes)
                mes = str(input())
                client.send(mes.encode())
                mes = client.recv(BUFFER_SIZE).decode()
                print(mes)
                mes = str(input())
                client.send(mes.encode())
                mes = client.recv(BUFFER_SIZE).decode()
                print(mes)
                if mes == "Login success!":
                    break
            elif mes == "Register":
                mes = client.recv(BUFFER_SIZE)
                print(mes.decode())
                mes = str(input())
                client.send(mes.encode())
                mes = (client.recv(BUFFER_SIZE)).decode()
                while mes == "Invalid!":
                    print("Username must have at least 5 character (a -> z, 0 -> 9).")
                    mes = str(input())
                    client.send(mes.encode())
                    mes = (client.recv(BUFFER_SIZE)).decode()
            else:
                mes = client.recv(BUFFER_SIZE).decode()
                print(mes) 
        
        print("Text sth")
        while True:
            mes = str(input())
            client.send(mes.encode())
            if mes == "quit":
                break
            mes = client.recv(BUFFER_SIZE).decode()
            print(mes)

    except socket.gaierror as s_g:
        print("Address-related error connecting to server: ", s_g)
        sys.exit(1)
    except socket.error as s_e:
        print("Error: ", s_e)
    finally:
        client.close()

import socket
import sys
import Login

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
        Login.page()
        BYT = MESSAGE.encode()
        client.send(BYT)
        print("Send message!")
    except socket.gaierror as s_g:
        print("Address-related error connecting to server: ", s_g)
        sys.exit(1)
    except socket.error as s_e:
        print("Error: ", s_e)
    finally:
        client.close()

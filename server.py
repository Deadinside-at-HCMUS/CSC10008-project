import socket
import threading
import sys
import re
import json

# Create Socket (TCP) Connection
IP = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 2048
FORMAT = 'ascii'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    server.bind((IP, PORT))
except socket.error as s_e:
    print("Error creating socket: ", s_e)
    sys.exit(1)

server.listen()

print("==== SEVER RUNNING ====")
print(f"Server {IP} listening on port {PORT}")
print("Waiting for clients...")

clients = []
users = []

# Function : For each client
special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

def checkSpecialChar(string):
    if (special_char.search(string)):
        return True
    return False


def checkValid(username, password):
    if len(username) < 5:
        return False
    if re.findall('[A-Z]', username) or checkSpecialChar(username):
        return False
    if len(password) < 3:
        return False
    return True

def initNote(username):
    file = open("./note.json")
    users_note = json.load(file)
    users_note[f"{username}"] = {
        "note": [],
        "file": [],
        "image": []
    }
    json_obj = json.dumps(users_note, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    file.close()

def handle(client):
    while True:
        try:
            user_data = client.recv(BUFFER_SIZE).decode(FORMAT)
            user_data = eval(user_data)
            mode = user_data[0]
            if mode == "LOG-IN":
                file = open("./user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                if checkValid(username, password):
                    for user in users_data:
                        if user["username"] == username:
                            if user["password"] == password:
                                users.append([username, password])
                                json_obj = json.dumps(users_data, indent=4)
                                with open("user.json", "w") as fo:
                                    fo.write(json_obj)
                                client.send("Login successful!".encode(FORMAT))
                            else:
                                client.send("Wrong password!".encode(FORMAT))
                            user_exist = True
                            break
                else:
                    client.send("Invalid username!".encode(FORMAT))
                if not user_exist:
                    client.send("User does not exist!".encode(FORMAT))
                file.close()
            elif mode == "SIGN-UP":
                print("Receive sign up")
                file = open("./user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                confirm_pw = user_data[3]
                if checkValid(username, password):
                    user_exist = False
                    for user in users_data:
                        if (user["username"] == username):
                            client.send("User is already exist".encode(FORMAT))
                            user_exist = True
                            break
                    if not(user_exist):
                        if confirm_pw == password:
                            user_info = {"username": username,
                                            "password": password}
                            initNote(username)
                            users_data.append(user_info)
                            client.send("Register successfully".encode(FORMAT))
                        else:
                            client.send(
                                "Password is not matched".encode(FORMAT))
                else:
                    client.send("Invalid username or password".encode(FORMAT))
                json_obj = json.dumps(users_data, indent=4)
                with open("user.json", "w") as fo:
                    fo.write(json_obj)
                file.close()            
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                users.remove(users[index])
                client.close()

def receive():
    ThreadCount = 0
    while True:
        client, address = server.accept()

        print(f"Connected with {str(address)}!")
        print("Client:", client.getsockname())

        clients.append(client)

        client_handler = threading.Thread(target=handle, args=(client,))
        client_handler.start()
        ThreadCount += 1
        print("Connection Request: " + str(ThreadCount))

receive()

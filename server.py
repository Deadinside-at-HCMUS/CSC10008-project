import socket
import threading
import sys
import re
import os
import json

# Server set up
IP = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 41000000
FORMAT = 'utf-8'

# Create Socket (TCP) Connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
    server.bind((IP, PORT))
except socket.error as e:
    print("Error creating socket: ", e)
    sys.exit(1)

# Listening for connections
server.listen()
print("============ SEVER RUNNING ============")
print(f"Server {IP} listening on port {PORT}")
print("Waiting for clients...")

# Init list
clients = []
users = []

# Checking for special characters
special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
upper_case  = ('[A-Z]')

def haveSpecialChar(string):
    if (special_char.search(string)):
        return True
    return False

# Checking valid input username and password
def checkValid(username, password):
    if len(username) < 5 or len(password) < 3:
        return False
    if re.findall(upper_case, username) or haveSpecialChar(username):
        return False
    return True

def initNote(username):
    file = open("./note.json")
    user_note = json.load(file)
    user_note[f"{username}"] = {
        "note": [],
        "image": [],
        "file": []
    }
    json_object = json.dumps(user_note, indent=4)
    with open("./note.json", "w") as fileOut:
        fileOut.write(json_object)
    file.close()

def createUserFolder(filename):
    is_file = os.path.isdir('./user_data')
    if is_file:
        path = f'./user_data/{filename}'
        os.makedirs(path)
    else:
        os.makedirs('./user_data')
        path = f'./user_data/{filename}'
        os.makedirs(path)

def isExistNote(username, title):
    file = open("./note.json")
    user_note = json.load(file)
    for user in user_note[username]["note"]:
        if user["title"] == title:
            return True
    return False

def isExistImage(username, image):
    file = open("./note.json")
    user_image = json.load(file)
    for user in user_image[username]["image"]:
        if user["name"] == image:
            return True
    return False

def isExistFile(username, files):
    file = open("./note.json")
    users_file = json.load(file)
    for user in users_file[username]["image"]:
        if user["name"] == files:
            return True
    for user in users_file[username]["file"]:
        if user["name"] == files:
            return True
    return False

def addNote(username, title, content, note_id):
    file = open("./note.json")
    user_note = json.load(file)
    user_note[username]["note"].append({"_id": note_id, "title": title, "content": content})
    json_object = json.dumps(user_note, indent=4)
    with open("./note.json", "w") as fileOut:
        fileOut.write(json_object)
    file.close()

def addImage(username, image, imageID):
    file = open("./note.json")
    user_image = json.load(file)
    user_image[username]["image"].append({"_id": imageID, "name": image})
    json_object = json.dumps(user_image, indent=4)
    with open("./note.json", "w") as fileOut:
        fileOut.write(json_object)
    file.close()

def addFile(username, files, fileID):
    file = open("./note.json")
    users_file = json.load(file)
    users_file[username]["file"].append({"_id": fileID, "name": files})
    json_object = json.dumps(users_file, indent=4)
    with open("./note.json", "w") as fileOut:
        fileOut.write(json_object)
    file.close()

def deleteNote(username, index, type):
    file = open("./note.json")
    user_note = json.load(file)
    if type == "Text":
        for note in user_note[username]["note"]:
            if note["_id"] == index:
                user_note[username]["note"].remove(note)
                break
    elif type == "Image":
        for img in user_note[username]["image"]:
            if img["_id"] == index:
                os.remove(f"./user_data/{username}/{img['name']}")
                user_note[username]["image"].remove(img)
                break
    elif type == "File":
        for file in user_note[username]["file"]:
            if file["_id"] == index:
                os.remove(f"./user_data/{username}/{file['name']}")
                user_note[username]["file"].remove(file)
                break
    json_object = json.dumps(user_note, indent=4)
    with open("./note.json", "w") as fileOut:
        fileOut.write(json_object)
    file.close()

def loadUserNoteData(username, client):
    file = open("./note.json")
    user_note = json.load(file)
    user_note = user_note[username]
    client.send(str(user_note).encode(FORMAT))
    file.close()

# Check empty file
def checkEmpty(filename):
    if os.stat(filename).st_size == 0:
        return True
    return False

# Init list if user data file is empty
if checkEmpty("./user.json"):
    file = open("./user.json", "w")
    file.write("[]")
    file.close()

# Init dictionary if note data file is empty
if checkEmpty("./note.json"):
    file = open("./note.json", "w")
    file.write("{}")
    file.close()

# Handle actions from clients
def handle(client):
    while True:
        try:
            user_data = client.recv(BUFFER_SIZE).decode(FORMAT)
            user_data = eval(user_data)
            mode = user_data[0]

            #Log in action
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
                                json_object = json.dumps(users_data, indent=4)
                                with open("user.json", "w") as fo:
                                    fo.write(json_object)
                                client.send("Login successful!".encode(FORMAT))
                                loadUserNoteData(username, client)
                            else:
                                client.send("Wrong password!".encode(FORMAT))
                            user_exist = True
                            break
                else:
                    client.send("Invalid username!".encode(FORMAT))
                if not user_exist:
                    client.send("User does not exist!".encode(FORMAT))
                file.close()

            # Sign up action            
            elif mode == "SIGN-UP":
                file = open("./user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                confirm_password = user_data[3]
                if checkValid(username, password):
                    user_exist = False
                    for user in users_data:
                        if (user["username"] == username):
                            client.send("User is already exist!".encode(FORMAT))
                            user_exist = True
                            break
                    if not(user_exist):
                        if confirm_password == password:
                            user_info = {"username": username, "password": password}
                            initNote(username)
                            createUserFolder(username)
                            users_data.append(user_info)
                            client.send("Register successfully!".encode(FORMAT))
                        else:
                            client.send("Password is not matched!".encode(FORMAT))
                else:
                    client.send("Invalid username or password!".encode(FORMAT))
                json_object = json.dumps(users_data, indent=4)
                with open("./user.json", "w") as fo:
                    fo.write(json_object)
                file.close()

            # Forgot password action            
            elif mode == "FORGOT-PASSWORD":
                file = open("./user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                confirm_password = user_data[3]
                for user in users_data:
                    if user["username"] == username:
                        user_exist = True
                        if checkValid(username, password):
                            if user["password"] == password:
                                client.send("Please use the new one, this is your current password!".encode(FORMAT))
                                break
                            elif password == confirm_password:
                                client.send("Update password successfully!".encode(FORMAT))
                                user["password"] = password
                                break
                            else:
                                client.send("Passwords are not matched!".encode(FORMAT))
                                break
                        else:
                            client.send("Invalid username or password!".encode(FORMAT))
                if not user_exist:
                    client.send("User does not exist!".encode(FORMAT))
                json_object = json.dumps(users_data, indent=4)
                with open("./user.json", "w") as fo:
                    fo.write(json_object)
                file.close()

            # Add note action
            elif mode == "ADD-NOTE":
                name = user_data[1]
                note_topic = user_data[2]
                note = user_data[3]
                note_id = user_data[4]
                if len(note_topic) > 0 and len(note) > 0:
                    note_exist = isExistNote(name, note_topic)
                    if not note_exist:
                        client.send("Note successfully created!".encode(FORMAT))
                        addNote(name, note_topic, note, note_id)
                    else:
                        client.send("This title is already exist!".encode(FORMAT))
                else:
                    client.send("Note Invalid!".encode(FORMAT))
            
            # Delete note action
            elif mode == "DELETE-NOTE":
                name = user_data[1]
                index = user_data[2]
                type = user_data[3]
                deleteNote(name, index, type)
            
            # Download file action
            elif mode == "DOWNLOAD-NOTE":
                username = user_data[1]
                index = user_data[2]
                type = user_data[3]
                file = open("./note.json")
                user_note = json.load(file)
                if type == "Image":
                    for user in user_note[username]["image"]:
                        if user["_id"] == index:
                            with open(f"./user_data/{username}/{user['name']}", 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                elif type == "File":
                    for user in user_note[username]["file"]:
                        if user["_id"] == index:
                            with open(f"./user_data/{username}/{user['name']}", 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                else:
                    for user in user_note[username]["note"]:
                        if user["_id"] == index:
                            client.send(
                                str([user["title"], user["content"]]).encode(FORMAT))
                            break
            
            # Add image action
            elif mode == "ADD-IMAGE":
                name = user_data[1]
                image = user_data[2]
                image_id = user_data[3]
                if len(image) > 0:
                    image_exist = isExistImage(name, image)
                    if not image_exist:
                        client.send("Image successfully created!".encode(FORMAT))
                        addImage(name, image, image_id)
                        with open(f'./user_data/{name}/' + image, 'wb') as f:
                            data = client.recv(41000000)
                            f.write(data)
                            f.close()
                    else:
                        client.send("This title is already exist!".encode(FORMAT))
            
            # View note action
            elif mode == "VIEW-NOTE":
                username = user_data[1]
                note_id = user_data[2]
                type = user_data[3]
                file = open("./note.json")
                user_note = json.load(file)
                if type == "Image":
                    for user in user_note[username]["image"]:
                        if user["_id"] == note_id:
                            with open(f'./user_data/{username}/{user["name"]}', 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                elif type == "File":
                    for user in user_note[username]["file"]:
                        if user["_id"] == note_id:
                            with open(f'./user_data/{username}/{user["name"]}', 'rb') as f:
                                client.send(f.read().encode(FORMAT))
                                f.close()
                            break
                elif type == "Text":
                    for user in user_note[username]["note"]:
                        if user["_id"] == note_id:
                            client.send(
                                str([user["title"], user["content"]]).encode(FORMAT))
                            break
            
            # Add file action
            elif mode == "ADD-FILE":
                name = user_data[1]
                file = user_data[2]
                file_id = user_data[3]
                if len(file) > 0:
                    file_exist = isExistFile(name, file)
                    if not file_exist:
                        client.send("File successfully created!".encode(FORMAT))
                        addFile(name, file, file_id)
                        with open(f'./user_data/{name}/' + file, 'wb') as f:
                            data = client.recv(BUFFER_SIZE)
                            f.write(data)
                            f.close()
                    else:
                        client.send("This title is already exist!".encode(FORMAT))
            else:
                pass         
        except:
            if client in clients:
                clients.remove(client)
                client.close()

def receive():
    thread_count = 0
    while True:
        client, address = server.accept()

        print("~~CONNECTED~~")
        print("Client:", client.getsockname())

        clients.append(client)
        client_handler = threading.Thread(target=handle, args=(client,))
        client_handler.start()
        thread_count += 1
        print("Connection Request: " + str(thread_count))

if __name__ == "__main__":
    receive()
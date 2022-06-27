import json

# sign up, sign in
def loadData():
    l = []
    with open('CSC10008-project/signup.json', 'r') as fIn:
        l = json.load(fIn);
    fIn.close()
    return l


def isValidUsername(username, l):
    if len(username) < 5:
        print("Invalid username!")
        return False
    for x in l:
        if x["username"] == username:
            print("This username is already exist, please try another one!")
            return False
    charCount = 0
    numCount = 0
    for i in username:
        if (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z'):
            charCount += 1
        if i >= '0' and i <= '9':
            numCount += 1
    if charCount <= 0 or numCount <= 0 or (charCount + numCount) != len(username):
        print("Invalid username!")
        return False
    return True

def isValidPassword(password):
    if len(password) < 3:
        print("Invalid password!")
        return False
    return True

def login(l, username, password):
    if {"username": username, "password": password} in l:
        return True
    return False

def saveData(account):
    with open('CSC10008-project/signup.json', 'w') as fOut:
        json.dump(account, fOut, indent = 4)
    fOut.close()

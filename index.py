import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as Pbk



### Variables.
end_code = False
password = "password"

basePath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(basePath, "tests")

copyPath = os.path.join(basePath, "copy")

salt = b'\xf3\x91J\x04{\x1b\xea\\2>|\x08\xfbq\x15\xea'
pbk = Pbk(hashes.SHA256(), 32, salt, 480000)

key = pbk.derive(bytes(password, 'UTF-8'))
key64 = base64.urlsafe_b64encode(key)



### Functions and Classes.
def getFromFile(path):
    file = open(path, "rb")
    fileCont = file.read()
    file.close()
    return fileCont

def writeFile(path, pay):
    file = open(path, "wb")
    file.write(pay)
    file.close()

def encrypt(file, key):
    return Fernet(key).encrypt(file)

def decrypt(file, key):
    return Fernet(key).decrypt(file)

def encryptAll(path, cm):
    files = os.listdir(path)

    for f in files:
        f = os.path.join(path, f)
        if os.path.isdir(f):
            encryptAll(f, cm)
        else:
            fileCont = getFromFile(f)
            if cm == "enc":
                enc = encrypt(fileCont, key64)
                writeFile(f, enc)
            if cm == "dec":
                dec = decrypt(fileCont, key64)
                writeFile(f, dec)

        

def execute_command(cm):
    valid = True
    
    while valid:
        path = input("Type the folder/file path: ")
        
        if not os.path.exists(path):
            print("Type a valid path...")
            ex = input("Retry? [y/n] ")
            if ex != "y" and ex != "Y":
                print("Leaving program...")
                return
        else:
            if os.path.isdir(path):
                conf = input("The given path points to a directory. Do you want to continue? [y/n]")
                if conf == "y" or "Y":
                    encryptAll(path, cm)
            else:
                file = getFromFile(path)
                enc = encrypt(file.read(), key64)
                file.write(enc)
                file.close()
            
            other = input("Do you want to encrypt other path? [y/n]: ")
            if other != "y" or other != "Y":
                print("Leaving functionality...")
                break
        


### Main Code.
print("Hi! What do you want to do?")
while not end_code:
    print("Type one of the following:")
    print("")
    print("enc: To encrypt a folder")
    print("dec: to decrypt an encrypted folder")
    print("ex: to exit program")
    print("")

    cm = input("Type here: ")
    if (cm == "ex"):
        print("Leaving program...")
        break
    if cm != "enc" and cm != "dec":
        print("Please type a valid instruction...")
    else:
        execute_command(cm)

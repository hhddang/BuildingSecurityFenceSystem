from test import *
import hashlib
import os
import random
import json
import string

def myHash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def generateSalt(length):
    """
        Randomly generate salt with input length\n
        Characters are taken from order 32 to 126 of ASCII table. Return salt
    """
    salt = ""
    for char in [chr(x) for x in random.sample(range(32, 126), length)]:
        salt += char
    return salt

def encrypt(file, password, database):
    """
        Encrypt content using symmetric-key encryption algorithm\n
        Return encrypted content
    """
    content = file['data']

    # Encryption will initialize salt and hashed key for file
    salt = (file['salt'] or generateSalt(3))
    key = password + salt
    token = ""
    
    # Encryption happens
    keyLength = len(key)
    k = 0
    for i in range(0,len(content)):
        if k == keyLength:
            k = 0
        token += chr(ord(content[i]) ^ ord(key[k]))
        k += 1


    file['salt'] = salt if file['salt'] == None else generateSalt(3)
    file['hashedKey'] = myHash(password + file['salt'])
    file['data'] = token
    open(file['name'], 'w').write(token)
    database[file['name']] = {'salt': file['salt'], 'hashedKey': file['hashedKey']}
    writeToDatabase('database.json', database)
    
    ####
    # print('database', database)

    return token

def checkPassword(file, password):
    key = password + file['salt']
    if myHash(key) == file['hashedKey']:
        return True
    return False
  
def decrypt(file, password, database):
    return encrypt(file, password, database)

def writeToDatabase(data, database):
    # database = json.load(open(databaseName))
    database.update(data)
    # json.dump(datab, open(fileName, 'w'))
    
    
# Split File
def createFolders():
    for i in range(1,6):
        os.mkdir(str(i))
        
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
        
def splitFile(filepath):
    with open(filepath, "rb") as f:
        content = f.read()

    NUM_FILES = 5

    n = int( len(content)  / NUM_FILES) or 1
    print(os.path.basename(filepath))
    chunks = [content[i:i+n] for i in range(0, len(content), n)]
    listDirectories = os.path.basename(filepath).split('/')[-1].replace(" ", "_")

    for i in range(len(chunks)):
        name = get_random_string(random.randint(8,10))
        directory = random.randint(1,5)
        with open(str(directory) + "/" + name + '.a', 'wb') as fw:
            fw.write(chunks[i])
        listDirectories += " " + name + " " + str(directory)
        
    # with open("root/system.txt", 'r') as fr:
    #     cont=fr.read()

    with open("root/system.txt",'a+') as fw2:
        # if os.path.basename(filepath).split('/')[-1].replace(" ", "_") not in cont:
        fw2.write(listDirectories + '\n')

def reconstructFile(fileName):
    with open("root/system.txt","r+") as f:
        lines = [line.strip() for line in f.readlines()]
        print('lines:', lines)

    # line = [l for l in lines if (fileName in l)][0]
    line = ''
    for l in lines:
        if fileName in l:
            line = l
            print('line: ', line)
    atr = line.split(" ")

    content = bytes()

    for i in range(1,len(atr),2):
        splittedName = atr[i]
        index = atr[i + 1]

        with open(index + '/' + splittedName + ".a", "rb") as f:
            cont = f.read()
        
        content += cont

    with open("out/" + fileName, "wb") as f:
        f.write(content)
        


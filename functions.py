import hashlib
import math
import os
import random
import json
import shutil
import string
import sys
import py7zr
from pathlib import Path

SYSTEM_FILE_NAME = "SecurityFenceSystem"

def readFromDatabase(databaseName):
    '''
    Read databaseName (.json file) and return data (dict type)
    '''
    with open(databaseName) as f:
        database = f.read()
        # If database is empty, assign it to empty dict:
        if database == "":
            database = {}
        # If not empty, load data from JSON format to dict
        else:
            database = json.loads(database)
        #
        return database

def writeToDatabase(data, databaseName):
    '''
    Overwrite data (dict type) to databaseName (.json file)
    '''
    with open(databaseName, 'w') as database:
        json.dump(data, database)

def myHash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def generateSalt(length):
    salt = ""
    for char in [chr(x) for x in random.sample(range(32, 126), length)]:
        salt += char
    return salt

def symmetricKeyAlgorithm(var, key, byteorder = sys.byteorder):
    '''
    Encrypt / decrypt data using key
    - data: string
    - key: string
    '''
    key, var = key[:len(var)], var[:len(key)]
    int_var = int.from_bytes(var, byteorder)
    int_key = int.from_bytes(key, byteorder)
    int_enc = int_var ^ int_key
    return int_enc.to_bytes(len(var), byteorder)

def encrypt(data, key):
    '''
    Encrypt data using key and return encrypted data
    - data: string
    - key: string
    '''
    encryptedData = symmetricKeyAlgorithm(data, key)
    return encryptedData

def decrypt(data, key):
    '''
    Decrypt data using keyand return decrypted data
    - data: string
    - key: string
    '''
    decryptedData = symmetricKeyAlgorithm(data, key)
    return decryptedData

def getRandomString(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def splitFile(filepath):
    with open(filepath, "rb") as f:
        content = f.read()

    NUM_FILES = 5

    n = int( (len(content) - 1)  / NUM_FILES + 1)
    chunks = [content[i:i+n] for i in range(0, len(content), n)]

#    listDirectories = os.path.basename(filepath).split('/')[-1].replace(" ", "_")
    listDirectories = filepath.replace(" ", "_")

    directories = list(range(1,NUM_FILES + 1))
    random.shuffle(directories)
    for i in range(len(chunks)):
        name = getRandomString(random.randint(8,10))
        directory = directories[i]
        with open(SYSTEM_FILE_NAME +  '/' + str(directory) + "/" + name + '.a', 'wb') as fw:
            fw.write(chunks[i])
        listDirectories += " " + name + " " + str(directory)

    name = getRandomString(random.randint(8,10))

    with open(SYSTEM_FILE_NAME + "/root/" + name + ".txt" ,'a+') as fw2:
        fw2.write(listDirectories + '\n')

def reconstructFile(fname):
    # Filter the file 
    for path in os.listdir(SYSTEM_FILE_NAME + '/root'):
        # check if current path is a file
        if os.path.isfile(os.path.join(SYSTEM_FILE_NAME + '/root', path)):
            with open(os.path.join(SYSTEM_FILE_NAME + '/root', path), 'r') as f:
                line = f.read().strip().split(' ')
            if (line[0] == fname):

                content = bytes()
                
                for i in range(1,len(line),2):
                    splittedName = line[i]
                    index = line[i + 1]

                    with open(SYSTEM_FILE_NAME + '/' + index + '/' + splittedName + ".a", "rb") as f:
                        cont = f.read()
                    
                    content += cont

                with open(line[0], "wb") as f:
                    f.write(content)

# def lockSystemFolder(password, folderName):
#     try:
#         with py7zr.SevenZipFile(folderName + '.7z', 'r', password) as archive:
#             archive.extractall()
        
#     except:
#         print("Wrong password")

#     else:
#         with py7zr.SevenZipFile(folderName + '.7z', 'w', password) as archive1:
#             archive1.writeall(folderName)
#             shutil.rmtree(folderName)

def importFile(fileName, password, databaseName, systemPassword):
    '''
    Import a file into system by 3 step\n
    1. Save password to database\n
    2. Encrypt file\n
    3. Split file
    - fileName: string
    - password: string
    - databseName: string (.json file)
    '''
    # Save password (salt and hashed key) to database
    salt = generateSalt(3)
    key = password + salt
    keyEncoded = key.encode()

    hashedKey = myHash(key)
    database = readFromDatabase(databaseName)
    database[fileName] = {'salt': salt, 'hashedKey': hashedKey}
    writeToDatabase(database, databaseName)
    # Encrypt file
    with open(fileName, mode='rb') as fr:
        data = fr.read()
    encryptedData = encrypt(data, keyEncoded * (math.ceil(len(data)/len(keyEncoded))))
    with open(fileName, 'wb') as fw:
        fw.write(encryptedData)
    # Split file
    flag = True
    for path in os.listdir(SYSTEM_FILE_NAME + '/root'):
        # check if current path is a file
        if os.path.isfile(os.path.join(SYSTEM_FILE_NAME + '/root', path)):
            with open(os.path.join(SYSTEM_FILE_NAME + '/root', path), 'r') as f:
                line = f.read()
            if line.split(' ')[0] == fileName:
                print("File exists. Overwrite are corrupted...")
                flag = False
                input()  
    
    if flag:
        splitFile(fileName)
        # Delete file
        os.remove(fileName)
    with py7zr.SevenZipFile(SYSTEM_FILE_NAME + '.7z', 'w', password = systemPassword) as archive1:
        archive1.writeall(SYSTEM_FILE_NAME)
        shutil.rmtree(SYSTEM_FILE_NAME)
    return flag

def exportFile(fileName, password, databaseName, systemPassword):
    '''
    Export a file from system by 3 step\n
    1. Check password, use data from database to compare\n
    2. Reconstruct file\n
    3. Decrypt file
    - fileName: string
    - password: string
    - databseName: string (.json file)
    '''
    reconstructFile(fileName)
    # Check password
    database = readFromDatabase(databaseName)
    salt = database[fileName]['salt']
    hashedKey = database[fileName]['hashedKey']
    myKey = password + salt
    keyEncoded = myKey.encode()
    myHashedKey = myHash(myKey)
    if myHashedKey == hashedKey:
        # decrypt file
        with open(fileName, 'rb') as fr:
            data = fr.read()
            decryptedData = decrypt(data, keyEncoded * (math.ceil(len(data)/len(keyEncoded))))
        with(open(fileName, 'wb')) as fw:
            fw.write(decryptedData)
    
    with py7zr.SevenZipFile(SYSTEM_FILE_NAME + '.7z', 'w', password = systemPassword) as archive1:
        archive1.writeall(SYSTEM_FILE_NAME)
        shutil.rmtree(SYSTEM_FILE_NAME)
  
def changeStatusTo(status, folderName):
    if status not in ['showed','hidden']:
        print('Incorrect, Please Enter Again!')
    else:
        if (status=='showed'):
            os.system('attrib -h "' + folderName + '"')
        elif (status=='hidden'):
            os.system('attrib +h "' + folderName +'"')

def createFolders(name):
    os.mkdir(name)
    os.chdir(name)

    dict = {}

    json_dump = json.dumps(dict)

    with open("database.json", 'w') as outfile:
        outfile.write(json_dump)
        
    for i in range(1,6):
        os.mkdir(str(i))
    os.mkdir('root')

def preparation(systemName):
    createFolders(systemName)
    path = Path(os.path.abspath(os.getcwd()))
    os.chdir(path.parent.absolute())
    with py7zr.SevenZipFile(systemName +'.7z', 'w') as archive:
        archive.writeall(systemName)
    shutil.rmtree(systemName)

# splitFile('MyData/doc.docx')
# reconstructFile('MyData/text.txt')

# importFile('MyData/a.txt', 'abc', SYSTEM_FILE_NAME + '/database.json')
# exportFile('MyData/a.txt', 'abc', SYSTEM_FILE_NAME + '/database.json')

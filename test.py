import hashlib
import os
import random
import json

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

def encrypt2(fileName, password, database):
    """
        Encrypt data using symmetric-key encryption algorithm\n
        Return encrypted data
    """
    data = open(fileName, 'r').read()
    
    # Neu co mat khau => tao newSalt, newHashedKey
    if fileName in database:
        print('da co mk')
        salt = database[fileName]['salt']
        newSalt = generateSalt(3)
        newKey = password + newSalt
        newHashedKey = myHash(newKey)
        database[fileName] = {'salt': newSalt, 'hashedKey': newHashedKey}
        
    # Neu chua co mat khau => khoi tao salt va hashKey
    else:
        print('k co mk')
        salt = generateSalt(3)
        key = password + salt
        hashedKey = myHash(key)
        database[fileName] = {'salt': salt, 'hashedKey': hashedKey}
        # hashedKey = myHash(password + newSalt)
    
    json.dump(database, open('database.json','w'))
        
    token = ""
    
    # Encryption happens
    keyLength = len(key)
    k = 0
    for i in range(0,len(data)):
        if k == keyLength:
            k = 0
        token += chr(ord(data[i]) ^ ord(key[k]))
        k += 1

    open(fileName, 'w').write(token)    
    return token


    salt = database[fileName]['salt']
    hashedKey = database[fileName]['hashedKey']
    
    inputKey = password + salt
    inputHashedKey = myHash(inputKey)
    
    if hashedKey == inputHashedKey:
        return True
    return False
  
def decrypt2(fileName, password, database):
    return encrypt2(fileName, password, database)

def checkPassword(fileName, password, database):
    pass

def symmetricKeyAlgorithm(data, key):
    '''
    Encrypt / decrypt data using key
    - data: string
    - key: string
    '''
    #
    encryptedData = ''
    #
    k = 0
    for i in range(0, len(data)):
        if k == len(key):
            k = 0
        encryptedData += chr(ord(data[i]) ^ ord(key[k]))
        k += 1
    #
    return encryptedData

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

def setPassword(fileName, password, databaseName):
    '''
    Set password for a file. Password securely stored in database
    - fileName: string
    - password: string
    - databaseName: string (.json filename)
    '''
    # Generate salt and hashed key
    salt = generateSalt(3)
    key = password + salt
    hashedKey = myHash(key)
    # Encrypt file
    with open(fileName) as fr:
        data = fr.read()
    encryptedData = encrypt(data, key)
    with open(fileName, 'w') as fw:
        fw.write(encryptedData)
    # Save salt and hashed key to database
    database = readFromDatabase(databaseName)
    database[fileName] = {'salt': salt, 'hashedKey': hashedKey}
    writeToDatabase(database, databaseName)

def viewFile(fileName, password, databaseName):
    database = readFromDatabase(databaseName)
    salt = database[fileName]['salt']
    hashedKey = database[fileName]['hashedKey']
    myKey = password + salt
    myHashedKey = myHash(myKey)
    if myHashedKey == hashedKey:
        # reconstructFile(fileName)
        decrypt()
    return False

def importFile(fileName, password, databaseName):
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
    hashedKey = myHash(key)
    database = readFromDatabase(databaseName)
    database[fileName] = {'salt': salt, 'hashedKey': hashedKey}
    writeToDatabase(database, databaseName)
    # Encrypt file
    with open(fileName) as fr:
        data = fr.read()
    encryptedData = encrypt(data, key)
    with open(fileName, 'w') as fw:
        fw.write(encryptedData)
    # Split file
    ######
    

def exportFile(fileName, password, databaseName):
    '''
    Export a file from system by 3 step\n
    1. Check password, use data from database to compare\n
    2. Reconstruct file\n
    3. Decrypt file
    - fileName: string
    - password: string
    - databseName: string (.json file)
    '''
    # Check password
    database = readFromDatabase(databaseName)
    salt = database[fileName]['salt']
    hashedKey = database[fileName]['hashedKey']
    myKey = password + salt
    myHashedKey = myHash(myKey)
    if myHashedKey == hashedKey:
        # reconstruct file
        # decrypt file
        pass

def importFolder(fileName, password, database):
    pass
def exportFolder(fileName, password, database):
    pass


path = "Directory"
fileName = 'Directory/a.txt'
databaseName = 'database.json'
password = '123'




    

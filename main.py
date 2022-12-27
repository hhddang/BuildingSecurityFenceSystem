import os
from functions import * 

file = {
    'name': None,
    'content': None,
    'salt': None,
    'hashedKey': None,
}

folder = {
    'status': 'show',
    'hashedKey': None,
    'salt': None,
}

def run():
    while(True):
        os.system('cls')
        print('0 - Exit')
        print('1 - Choose a file')
        print('2 - Choose a folder')
        choose = input('>> ')
        if choose == '0':
            break
        if choose == '1':
            workOnFile()
        if choose == '2':
            workOnFolder()
        else:
            continue


def workOnFile():
    # Read file
    # fileName = input('>>> Enter filename: ')
    fileName='text.txt'
    file['name'] = fileName
    file['content'] = open(fileName, 'r').read()
    database = json.load(open("database.json"))
    if file['name'] not in database:
        # Set a password
        password = input(f'>>> Set a password on {fileName}: ')
        encrypt(file, password, {})
        splitFile(fileName)
        
    else:
        print("File encrypted")

    # View file content and change hashed key everytime password is entered
    # while(True):
    #     # os.system('cls')
    #     reconstructFile(fileName)
    #     inputPassword = input('>>> Input password to view content: ')
    #     if checkPassword(file, inputPassword):
    #         decrypt(file, inputPassword, {})
    #         print('>>> File content: \n ' + file['content'])
            
    #     else:
    #         print('>>> Incorrect password!')
    #     input('>>> Enter to continue!')

def workOnFolder():
    pass

#createFolders()
workOnFile()
# run()
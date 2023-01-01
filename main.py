from ObfuscatedFunctions import *
import os
import py7zr

SYSTEM_FILE_NAME = "SecurityFenceSystem"

systemName = SYSTEM_FILE_NAME + '.7z'
databaseName = SYSTEM_FILE_NAME + '/database.json'
choices = ['1', '2']

changeStatusTo('showed', systemName)

os.system('cls')

systemPassword = input('>> Input system password: ')

try:
    with py7zr.SevenZipFile(SYSTEM_FILE_NAME + '.7z', 'r', password = systemPassword) as archive:
        archive.extractall()
except:
    print("Wrong system password")
    input('Press any key to continue ...')
else:
    while (True):
        os.system('cls')

        print('1 - Import a file')
        print('2 - Export a file')
        print('0 - Exit')
        choice = input('>> Enter your choice as number: ')

        with py7zr.SevenZipFile(SYSTEM_FILE_NAME + '.7z', 'r', password = systemPassword) as archive:
            archive.extractall()

        if choice == '1':
            fileName = input('>> Input file name: ').replace('\\', '/')
            if os.path.isfile(fileName):
                password = input('>> Enter file password to encrypt: ')
                print(f'\nIMPORTING FILE NAMED {fileName} WITH PASSWORD {password} IN PROCESS\n')
                flag = importFile(fileName, password, databaseName, systemPassword)

                if flag:
                    print('Imported file')
                input("Press any key to continue...")
            else:
                print("File not found")
                input("Press any key to continue...")
                continue
        elif choice == '2':
            count = 1
            for path in os.listdir(SYSTEM_FILE_NAME + '/root'):
                # check if current path is a file
                if os.path.isfile(os.path.join(SYSTEM_FILE_NAME + '/root', path)):
                    with open(os.path.join(SYSTEM_FILE_NAME + '/root', path), 'r') as f:
                        line = f.read()
                    print(count, " - ", line.split(" ")[0])
                    count += 1

            message = int(input('File ID: '))

            if message > count - 1 or message <= 0:
                print("Error...")
                input()
                continue
            with open(os.path.join(SYSTEM_FILE_NAME + '/root',os.listdir(SYSTEM_FILE_NAME + '/root')[message - 1]), 'r') as f:
                l = f.read().strip()

            fileName = l.split(' ')[0]
            password = input('>> Enter file password to decrypt: ')

            print(f'\nEXPORTING FILE NAMED {fileName} WITH PASSWORD {password} IN PROCESS\n')
            exportFile(fileName, password, databaseName, systemPassword)

            print(f'File exported to {fileName}')
            input('Press any key to continue...')
        elif choice == '0':
            break
        else: 
            continue

    changeStatusTo('hidden', systemName)



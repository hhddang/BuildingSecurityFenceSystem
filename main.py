from functions import importFile, exportFile, changeStatusTo
import os

systemName = 'SecurityFenceSystem.7z'
databaseName = 'SecurityFenceSystem/database.json'
choices = ['1', '2']

changeStatusTo('showed', systemName)

systemPassword = input('>> Input system password: ')

while (True):
    os.system('cls')
    print('1 - Import a file')
    print('2 - Export a file')
    print('0 - Exit')
    choice = input('>> Enter your choice as number: ')

    if choice in choices:
        fileName = input('>> Input file name: ')
        password = input('>> Enter file password: ')

    if choice == '1':
        print(f'\nIMPORTING FILE NAMED {fileName} WITH PASSWORD {password} IN PROCESS\n')
        importFile(fileName, password, databaseName, systemPassword)
    elif choice == '2':
        print(f'\nEXPORTING FILE NAMED {fileName} WITH PASSWORD {password} IN PROCESS\n')
        exportFile(fileName, password, databaseName, systemPassword)
    elif choice == '0':
        break
    else: 
        continue

    if choice in choices:
        print('Import / export successfully!')
        input('Press any key to continue ...')

changeStatusTo('hidden', systemName)



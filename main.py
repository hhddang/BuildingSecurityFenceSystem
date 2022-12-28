from functions import importFile, exportFile, importFolder, exportFolder
import os

databaseName = 'database.json'
choices = ['1', '2', '3', '4']

while (True):
    os.system('cls')
    print('1 - Import a file')
    print('2 - Export a file')
    print('3 - Import a folder')
    print('4 - Export a folder')
    choice = input('>> Enter your choice as number: ')

    if choice in choices:
        inputName = input('>> Input file / folder name: ')
        password = input('>> Enter password to import / export: ')

    if choice == '1':
        print(f'\nIMPORTING FILE NAMED {inputName} WITH PASSWORD {password} IN PROCESS\n')
        # importFile(inputName, password, databaseName)
        pass
    elif choice == '2':
        print(f'\nEXPORTING FILE NAMED {inputName} WITH PASSWORD {password} IN PROCESS\n')
        # exportFile(inputName, password, databaseName)
        pass
    elif choice == '3':
        print(f'\nIMPORTING FOLDER NAMED {inputName} WITH PASSWORD {password} IN PROCESS\n')
        # importFolder(inputName, password, databaseName)
        pass
    elif choice == '4':
        print(f'\nEXPORTING FOLDER NAMED {inputName} WITH PASSWORD {password} IN PROCESS\n')
        # exportFolder(inputName, password, databaseName)
        pass
    else: 
        continue

    if choice in choices:
        print('Import / export successfully!')
        input('Press any key to continue ...')




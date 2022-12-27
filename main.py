from functions import * 
import os

while (True):
    os.system('cls')
    print('1 - Import a file')
    print('2 - Export a file')
    print('3 - Import a folder')
    print('4 - Export a folder')
    choose = input('>> Choose: ')

    if choose in ['1', '2', '3', '4']:
        inputName = input('>> Input file / folder name: ')

    if choose == '1':
        importFile()
    elif choose == '2':
        exportFile()
    elif choose == '3':
        importFolder()
    elif choose == '4':
        exportFolder()
    else: 
        continue


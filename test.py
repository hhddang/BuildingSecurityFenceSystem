from functions0 import *
changeStatusTo('showed', 'SecurityFenceSystem.7z')
#preparation('SecurityFenceSystem')
with py7zr.SevenZipFile("SecurityFenceSystem" + '.7z', 'w', password='123') as archive1:
    archive1.writeall('SecurityFenceSystem')


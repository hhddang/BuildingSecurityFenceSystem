# import sys
from functions  import *
# import math
# def encrypt2(var, key, byteorder=sys.byteorder):
#     key, var = key[:len(var)], var[:len(key)]
#     int_var = int.from_bytes(var, byteorder)
#     int_key = int.from_bytes(key, byteorder)
#     int_enc = int_var ^ int_key
#     return int_enc.to_bytes(len(var), byteorder)

# with open('out.pdf', 'rb') as out_file:
#     content = out_file.read()

# salt = generateSalt(3)
# password = 'abc'

# key = salt + password
# key = key.encode()

# times = math.ceil(len(content)/len(key))

# encrypt = encrypt2(content, key * times)

# decrypt = encrypt2(encrypt, key * times)

# with open('out1.pdf', 'wb') as out_file:
#     out_file.write(decrypt)

preparation(SYSTEM_FILE_NAME)
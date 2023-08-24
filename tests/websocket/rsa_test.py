from crypto_algorithms.RSA import RSACipher
import time
import secrets

rsa = RSACipher(*RSACipher.generateKeys(4096))

for i in range(51):
    data_length = int(4096 / 8 - i)
    print(f'{data_length = }')
    try:
        rsa.encrypt(secrets.token_bytes(data_length))
    except:
        pass
    else:
        print('Success')
        break

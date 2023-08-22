from crypto_algorithms.RSA import RSACipher
import secrets
import time
import textwrap

key = secrets.token_urlsafe(256)
keys  = (textwrap.wrap(key, 64))
key = keys[0]

i = 1024
while True:
    try:
        t = time.time()
        cipher = RSACipher(*RSACipher.generateKeys(i))
        stop = time.time()
        cipher.encrypt(key.encode())
    except:
        print('fail with', i)
    else:
        print('length:', i)
        print('time:', stop - t)
        break

    i += 1

from crypto_algorithms.RSA import RSACipher
import time

t = time.time()
privateKey, publicKey = RSACipher.generateKeys(15360)
print(time.time() - t)

print(privateKey)
print()
print(publicKey)

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import time

class RSACipher:
    def generateKeys(length):
        """
        return (privateKey, publicKey)
        """
        RsaKey = RSA.generate(length)
        return (base64.b64encode(RsaKey.exportKey()).decode(), base64.b64encode(RsaKey.publickey().exportKey()).decode())

    def __init__(self, privateKey, publicKey = None):
        self.privateKey = base64.b64decode(privateKey)
        if publicKey:
            self.publicKey = base64.b64decode(publicKey)

    def encrypt(self, data : bytes):
        RSApublicKey = RSA.importKey(self.publicKey)
        OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
        return base64.b64encode(OAEP_cipher.encrypt(data))

    def decrypt(self, data : str):
        data = base64.b64decode(data)
        RSAprivateKey = RSA.importKey(self.privateKey)
        OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
        return OAEP_cipher.decrypt(data)


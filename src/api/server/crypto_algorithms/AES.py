import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from typing import Union

class AESCipher:
    def __init__(self, key: Union[str, bytes]) -> None:
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode() if isinstance(key, str) else key).digest()

    def _get_string(self, value: Union[bytes, str]) -> str:
        return value if isinstance(value, str) else value.decode('utf-8')

    def encrypt(self, plain_text: Union[str, bytes]) -> str:
        plain_text = self.__pad(self._get_string(plain_text))
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text: Union[bytes, str]) -> str:
        encrypted_text = b64decode(self._get_string(encrypted_text))
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:])
        plain_text = plain_text.decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text: str) -> str:
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text: str) -> str:
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]



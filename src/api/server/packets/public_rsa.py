from ..crypto_algorithms.RSA import RSACipher
from ..crypto_algorithms.AES import AESCipher

from .handler import PacketHandler 

from secrets import token_urlsafe
from core import logging
import json
import secrets

@PacketHandler.handle(p_type='client_rsa')
def client_public_rsa(client, data: dict) -> None:
    if client.RSA_INSTANCE and client.AES_INSTANCE:
        return logging.warning(f'{client.addr} Tried to retrive a new AES key.')

    RSA_INSTANCE = RSACipher(publicKey=data.get('rsa_key'))
    AES_KEY = secrets.token_urlsafe(256)
    
    logging.debug(f'Encrypting connection AES-256 key with RSA')
    try:
        AES_KEY_PROTECTED_RSA = RSA_INSTANCE.encrypt(AES_KEY.encode('utf-8')).decode('utf-8')
    except Exception as e:
        logging.critical(f'Failed to encrypt with RSA the AES256 key for {client.addr}')
        logging.critical(f'Encryption Error: {e}')
        return 
    else:
        logging.debug('Connection AES key has been succesfully encrypted.')

    client.send(json.dumps({'t': 'server_aes', 'd': {'aes_key': AES_KEY_PROTECTED_RSA}}))

    client.RSA_INSTANCE = RSA_INSTANCE
    client.AES_INSTANCE = AESCipher(AES_KEY)

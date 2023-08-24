from ...crypto_algorithms.RSA import RSACipher
from ...crypto_algorithms.AES import AESCipher
from ...client import WebSocketClient

from .handler import PacketHandler, PacketsPhases

from src.database.errors import CryptoErrors
from src.api.utilities import APIUtils

from typing import Union
from core import logging
import json
import time
import secrets

@PacketHandler.handle(packet_type='client_rsa', working_phase=PacketsPhases.PRE_CRYPTO)
def setup_client_cryptography(client: WebSocketClient, data: dict) -> Union[dict, None]:
    if client.RSA_INSTANCE and client.AES_INSTANCE:
        return logging.warning(f'{client.addr} Tried to retrive a new AES key.')

    RSA_INSTANCE = RSACipher(publicKey=data.get('rsa_key'))
    aes_key_length = int(data.get('length', 2048) / 8)
    if aes_key_length < 128 or aes_key_length > 1024:
        return APIUtils.error('client_rsa', CryptoErrors.INVALID_KEY_SIZE)
    aes_key_length -= 42

    logging.debug(f'Dynamic AES key length: {aes_key_length}')
    AES_KEY = secrets.token_urlsafe(aes_key_length)[:aes_key_length]
    
    logging.debug(f'Encrypting connection AES key with RSA')
    try:
        AES_KEY_PROTECTED_RSA = RSA_INSTANCE.encrypt(AES_KEY.encode('utf-8')).decode('utf-8')
    except Exception as e:
        logging.critical(f'Failed to encrypt with RSA the AES key for {client.addr}')
        logging.critical(f'Encryption Error: {e}')
        return APIUtils.error('client_rsa', CryptoErrors.RSA_ENCRYPTION_FAILED)
    else:
        logging.debug('RSA layer succesfully applied on the AES key')

    client.send(json.dumps({
        'type': 'server_aes',
        'data': {
            'aes_key': AES_KEY_PROTECTED_RSA,
            'length': aes_key_length
        }
    }))

    logging.debug('AES key exchange has been successful')

    client.RSA_INSTANCE = RSA_INSTANCE
    client.AES_INSTANCE = AESCipher(AES_KEY)
    client.INTEGRITY.update({'aes': AES_KEY, 'rsa': data.get('rsa_key')})
    client.phase = PacketsPhases.PRE_SAID

    logging.info(f'Client Cryptography setup required {time.time() - client.start_time} seconds')


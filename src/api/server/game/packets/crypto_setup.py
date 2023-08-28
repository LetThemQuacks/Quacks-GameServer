from ...crypto_algorithms.RSA import RSACipher
from ...crypto_algorithms.AES import AESCipher
from ...client import WebSocketClient

from .handler import PacketHandler, PacketsPhases

from src.database.errors import CryptoErrors
from src.api.utilities import APIUtils

from typing import Union
from core import logging
import base64
import time
import secrets

@PacketHandler.handle(packet_type='client_rsa', working_phase=PacketsPhases.PRE_CRYPTO)
def setup_client_cryptography(client: WebSocketClient, data: dict) -> Union[dict, None]:
    if client.RSA_INSTANCE and client.AES_INSTANCE:
        return logging.warning(f'{client.addr} Tried to retrive a new AES key.')

    AES_KEY = secrets.token_bytes(1024)

    try:
        RSA_INSTANCE = RSACipher(publicKey=data.get('rsa_key'))
        AES_INSTANCE = AESCipher(AES_KEY)
    except Exception:
        logging.exception(f'Failed to load AES/RSA Key')
        return APIUtils.error('client_rsa', CryptoErrors.KEY_LOAD_FAILED)
    
    logging.debug(f'Encrypting connection AES key with RSA')
    try:
        AES_KEY_PROTECTED_RSA = RSA_INSTANCE.encrypt(AES_INSTANCE.key).decode('utf-8')
    except Exception as e:
        logging.critical(f'Failed to encrypt with RSA the AES key for {client.addr}')
        logging.critical(f'Encryption Error: {e}')
        return APIUtils.error('client_rsa', CryptoErrors.RSA_ENCRYPTION_FAILED)
    else:
        logging.debug('RSA layer succesfully applied on the AES key')

    client.send({
        'type': 'server_aes',
        'data': {
            'aes_key': AES_KEY_PROTECTED_RSA,
        }
    })

    client.RSA_INSTANCE = RSA_INSTANCE
    client.AES_INSTANCE = AES_INSTANCE
    client.INTEGRITY.update({'aes': base64.b64encode(AES_INSTANCE.key).decode(), 'rsa': data.get('rsa_key')})
    client.phase = PacketsPhases.PRE_SAID

    logging.info(f'Client Key exchange required {time.time() - client.start_time} seconds')


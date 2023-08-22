from ...crypto_algorithms.RSA import RSACipher
from ...crypto_algorithms.AES import AESCipher
from ...client import WebSocketClient

from ....bigboy.integrity import BigBoy

from .handler import PacketHandler, PacketsPhases

from src.database.errors import CryptoErrors
from ....utilities import APIUtils

from typing import Union
from secrets import token_urlsafe
from core import logging
import json
import time
import secrets

@PacketHandler.handle(packet_type='client_rsa', working_phase=PacketsPhases.PRE_CRYPTO)
def setup_client_cryptography(client: WebSocketClient, data: dict) -> Union[dict, None]:
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
        return APIUtils.error('client_rsa', CryptoErrors.RSA_ENCRYPTION_FAILED)
    else:
        logging.debug('RSA layer succesfully applied on the AES key')

    client.send(json.dumps({'type': 'server_aes', 'data': {'aes_key': AES_KEY_PROTECTED_RSA}}))

    logging.debug('AES-256 key exchange has been successful')

    client.RSA_INSTANCE = RSA_INSTANCE
    client.AES_INSTANCE = AESCipher(AES_KEY)
    client.INTEGRITY.update({'aes': AES_KEY, 'rsa': data.get('rsa_key')})
    client.phase = PacketsPhases.PRE_SAID

    logging.info(f'Client Cryptography setup required {time.time() - client.start_time} seconds')


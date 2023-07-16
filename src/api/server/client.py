from simple_websocket.ws import Server

from flask import request
from core import logging

from .crypto_algorithms.RSA import RSACipher
from .crypto_algorithms.AES import AESCipher

from .packets.handler import PacketHandler
from .packets import public_rsa

import json

class WebSocketClient:
    RSA_INSTANCE: RSACipher = None
    AES_INSTANCE: AESCipher = None

    def __init__(self, ws: Server):
        self.ws = ws
        self.addr = request.remote_addr
        self.args = request.args

        logging.info(f'WS Client Connected from {self.addr}')
        logging.debug(f'WebSocket Connection Arguments: {self.args}')
        self.handle_packets()

    def handle_packets(self):
        while True:
            loaded = json.loads(self.recv())
            callback = PacketHandler.packets_callbacks['p_type'].get(loaded['t'])
            if callback:
                callback.get('callback')(self, loaded.get('d', {}))
            

    def recv(self):
        raw_data = self.ws.receive()

        if self.AES_INSTANCE:
            try:
                data = self.AES_INSTANCE.decrypt(raw_data)
            except Exception as e:
                logging.critical(f'{self.addr} Failed to decrypt data: {raw_data}')
                return '{"t": null}'
            else:
                logging.debug(f'+ Decrypted Data: {data}')
                return data

        return raw_data

    def send(self, data: str):
        if self.AES_INSTANCE:
            return self.ws.send(self.AES_INSTANCE.encrypt(data))
        self.ws.send(data)

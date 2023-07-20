from simple_websocket.ws import Server

from flask import request
from core import logging

from .crypto_algorithms.RSA import RSACipher
from .crypto_algorithms.AES import AESCipher

from .game.packets.handler import PacketHandler
from .game.physics.duck import Duck

from typing import Tuple

import threading
import json
import time
import uuid

Vector = Tuple[float, float]

class WebSocketClient:
    RSA_INSTANCE: RSACipher = None
    AES_INSTANCE: AESCipher = None
    CURRENT_ROOM: str       = None

    def __init__(self, ws: Server):
        self.ws = ws
        self.addr = request.remote_addr
        self.args = request.args
        self.position: Vector = [0, 0]
        self.start_time = time.time()
        self.duck = Duck()

        logging.info(f'WS Client Connected from {self.addr}')
        logging.debug(f'WebSocket Connection Arguments: {self.args}')
        logging.debug(f'Running a new packet handler for {self.addr}, Threads Count: {threading.active_count()}')
        self.handle_packets()

    def setup_user_info(self, username: str, skin: str) -> None:
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.skin = skin

    def handle_packets(self):
        while True:
            loaded = self.load_json(self.recv())

            callback = PacketHandler.packets_callbacks['type'].get(loaded['type'])
            if callback:
                if callback.get('filter'):
                    filter_check = callback['filter'](self)
                    if filter_check[0]:
                        callback.get('callback')(self, loaded.get('data', {}))
                    else:
                        self.send(json.dumps({'type': 'error', 'data': {
                            'from_packet_type': loaded['type'],
                            'code': filter_check[1]
                        }}))

                else:
                    callback.get('callback')(self, loaded.get('data', {}))

    def load_json(self, string: str) -> dict:
        try:
            return json.loads(string)
        except Exception:
            logging.exception(f'Json parsing FAILED: "{string}"')
            return {'type': None}

    def recv(self):
        raw_data = self.ws.receive()

        if self.AES_INSTANCE:
            try:
                data = self.AES_INSTANCE.decrypt(raw_data)
            except Exception:
                logging.exception(f'{self.addr} Data decryption FAILED: "{raw_data}"')
                return '{"type": null}'
            else:
                logging.debug(f'+ Decrypted Data: {data}')
                return data

        return raw_data

    def send(self, data: str):
        if self.AES_INSTANCE:
            return self.ws.send(self.AES_INSTANCE.encrypt(data))
        self.ws.send(data)

    def jsonify(self):
        return {
            'id': self.user_id,
            'username': self.username,
            'skin': self.skin,
            'position': self.position
        }


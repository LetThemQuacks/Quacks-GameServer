from simple_websocket.ws import Server

from dataclasses import asdict
from flask import request
from core import logging

from .crypto_algorithms.RSA import RSACipher
from .crypto_algorithms.AES import AESCipher

from .game.packets.handler import PacketHandler
from .game.physics.duck import Duck
from .game.room import RoomServer

from .types.client import Packet
from typing import Union

import threading
import json
import time
import uuid

__null_packet: Packet = {'type': None, 'data': {}}
__null_packet_string  = json.dumps(__null_packet)

class WebSocketClient:
    RSA_INSTANCE: Union[RSACipher, None]  = None
    AES_INSTANCE: Union[AESCipher, None]  = None
    CURRENT_ROOM: Union[RoomServer, None] = None

    def __init__(self, ws: Server):
        self.ws = ws
        self.addr = request.remote_addr
        self.args = request.args
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

    def _check_filters(self, filters, packet):
        for filter in filters:
            result = filter(self, packet)
            if isinstance(result, str):
                self.send(json.dumps({'type': 'error', 'data': {
                    'from_packet_type': packet['type'],
                    'code': result
                }}))
                return False

        return True

    def _call_callback(self, callback, packet: Packet) -> None:
        logging.debug(f'Calling callback {callback.get("callback")}')
        callback.get('callback')(self, packet.get('data', {}))

    def _call_callback_with_filters(self, callback, packet: Packet) -> None:
        filter_check = self._check_filters(callback['filters'], packet)
        if filter_check:
            self._call_callback(callback, packet)

    def handle_packets(self):
        while True:
            loaded: Packet = self.load_packet_json(self.recv())
            self._handle_packet(loaded)
 
    def _handle_packet(self, packet: Packet) -> None:
        callback = PacketHandler.packets_callbacks['type'].get(packet['type'])
        if not callback:
            return


        if callback.get('filters'):
            self._call_callback_with_filters(callback, packet)
        else:
            self._call_callback(callback, packet)


    def load_packet_json(self, string: Union[str, None]) -> Packet:
        string = str(string)
        try:
            return json.loads(string)
        except Exception:
            logging.exception(f'Json parsing FAILED: "{string}"')
            return __null_packet

    def recv(self):
        raw_data = self.ws.receive()

        if not raw_data:
            return __null_packet_string

        if self.AES_INSTANCE:
            try:
                data = self.AES_INSTANCE.decrypt(raw_data)
            except Exception:
                logging.exception(f'{self.addr} Data decryption FAILED: "{raw_data}"')
                return __null_packet_string
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
            'state': self.public_physics_state
        }

    @property
    def public_physics_state(self):
        state = asdict(self.duck)
        state.pop('')
